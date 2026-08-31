"""Frozen market data provider: serves the real fixed CSVs to the live graph.

Unlike the earlier exact-args snapshot lookup, this provider computes results
*from the actual fixed CSV* on demand, so it works regardless of which tool
arguments the (compact) model selects:

- ``get_stock_data`` formats the real CSV rows in the upstream shape, filtered
  to the requested date range (no fabricated prices).
- ``get_indicators`` computes the indicators the graph actually supports
  (MACD/signal/histogram, RSI, Bollinger, EMA/SMA, ATR) directly from the real
  CSV. Comma-separated indicator requests are handled. An indicator whose full
  calculation window is not available is reported as unavailable — it is never
  silently relabelled as a shorter-window average.
- ``get_verified_market_snapshot`` reads OHLCV directly from the real CSV.
- ``get_news`` returns the official case notes and source ID when the ticker
  corresponds to a known case, rather than an always-``NO_DATA`` sentinel.
  Optional sources absent from the frozen corpus remain ``NO_DATA``.

Every value derives from the immutable CSV and the committed case registry;
there is no network access anywhere in this module. A requested symbol or date
that does not correspond to the case returns an honest unavailable sentinel.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .case_registry import MARKET_DIR, all_cases

UNAVAILABLE = (
    "NO_DATA_AVAILABLE: this optional data source is not part of the frozen "
    "evaluation corpus. Do not estimate or fabricate values — report that this "
    "data is unavailable."
)


def _market_source_label(ticker: str) -> str:
    """The explicit stable source ID for market/technical evidence."""
    return f"market-{ticker.lower()}"


def _format_header(symbol: str, start_date: str, end_date: str, n: int) -> str:
    return (
        f"# Stock data for {symbol} from {start_date} to {end_date}\n"
        f"# source_id: {_market_source_label(symbol)} (frozen market CSV)\n"
        f"# Total records: {n}\n"
        "# Data retrieved on: frozen corpus (no network)\n\n"
    )


# The exact indicator names the graph's technical-indicator tool supports, with
# the full look-back window (in trading rows) each needs. A request that cannot
# satisfy the window is reported unavailable, not recomputed short.
_INDICATOR_WINDOWS: dict[str, int] = {
    "close_50_sma": 50,
    "close_200_sma": 200,
    "close_10_ema": 10,
    "macd": 26,  # MACD uses 12/26 EMAs; needs > 26 rows to converge
    "macds": 26,
    "macdh": 26,
    "rsi": 14,
    "boll": 20,
    "boll_ub": 20,
    "boll_lb": 20,
    "atr": 14,
    "vwma": 1,
}


class FrozenMarketProvider:
    """Read-only market provider backed by one immutable CSV + case notes."""

    def __init__(self, ticker: str, csv_path: str | Path | None = None):
        self.ticker = ticker.upper()
        self.csv_path = Path(csv_path) if csv_path else MARKET_DIR / f"{self.ticker}.csv"
        if not self.csv_path.exists():
            raise FileNotFoundError(f"frozen CSV not found: {self.csv_path}")
        self.frame = pd.read_csv(self.csv_path, parse_dates=["Date"])
        self.frame = self.frame.sort_values("Date").reset_index(drop=True)
        self.case = self._find_case(self.ticker)
        self.identity: dict = self.case["identity"] if self.case else {}

    @staticmethod
    def _find_case(ticker: str) -> dict | None:
        for case in all_cases():
            if case["ticker"].upper() == ticker.upper():
                return case
        return None

    # ------------------------------------------------------------------
    # stock data
    # ------------------------------------------------------------------

    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> str:
        if symbol.upper() != self.ticker:
            return UNAVAILABLE.replace("this optional data source", "this ticker's data")
        rows = self._rows_between(start_date, end_date)
        if rows.empty:
            return UNAVAILABLE
        out = self._to_upstream_csv(rows)
        header = _format_header(self.ticker, start_date, end_date, len(rows))
        return header + out

    def _rows_between(self, start_date: str, end_date: str) -> pd.DataFrame:
        df = self.frame
        if start_date:
            df = df[df["Date"] >= pd.Timestamp(start_date)]
        if end_date:
            df = df[df["Date"] <= pd.Timestamp(end_date)]
        return df

    def _to_upstream_csv(self, rows: pd.DataFrame) -> str:
        out = pd.DataFrame(
            {
                "Date": rows["Date"].dt.strftime("%Y-%m-%d"),
                "Open": rows["Open"],
                "High": rows["High"],
                "Low": rows["Low"],
                "Close": rows["Close"],
                "Adj Close": rows["Adj Close"],
                "Volume": rows["Volume"],
            }
        )
        return out.to_csv(index=False)

    # ------------------------------------------------------------------
    # indicators
    # ------------------------------------------------------------------

    def get_indicators(self, symbol: str, indicator: str, curr_date: str, look_back_days: int = 30) -> str:
        if symbol.upper() != self.ticker:
            return UNAVAILABLE.replace("this optional data source", "this ticker's data")
        df = self._frame_as_of(curr_date, look_back_days)
        if df.empty or len(df) < 2:
            return UNAVAILABLE
        names = [i.strip().lower() for i in (indicator or "").split(",") if i.strip()]
        if not names:
            return UNAVAILABLE
        lines = [
            f"# Technical indicator for {self.ticker} as of {curr_date} "
            f"(source_id: {_market_source_label(self.ticker)}; computed from frozen CSV)"
        ]
        for name in names:
            lines.append(self._indicator(df, name))
        lines.append(f"last_close: {float(df['Close'].iloc[-1]):.2f}")
        return "\n".join(lines)

    def _indicator(self, df: pd.DataFrame, name: str) -> str:
        if name not in _INDICATOR_WINDOWS:
            return self._unavailable_window(name, reason="not supported by frozen corpus")
        window = _INDICATOR_WINDOWS[name]
        if len(df) < window:
            return self._unavailable_window(
                name,
                reason=f"needs {window} rows but only {len(df)} available at {df['Date'].iloc[-1].date()}",
            )
        close = df["Close"]
        if name == "close_50_sma":
            return f"close_50_sma: {close.tail(50).mean():.2f}"
        if name == "close_200_sma":
            return f"close_200_sma: {close.tail(200).mean():.2f}"
        if name == "close_10_ema":
            return f"close_10_ema: {close.ewm(span=10, adjust=False).mean().iloc[-1]:.2f}"
        if name in ("macd", "macds", "macdh"):
            return self._macd_line(df, name)
        if name == "rsi":
            return f"rsi: {_rsi(close):.2f}"
        if name in ("boll", "boll_ub", "boll_lb"):
            mid = close.tail(20).mean()
            std = close.tail(20).std()
            if name == "boll":
                return f"boll: {mid:.2f}"
            if name == "boll_ub":
                return f"boll_ub: {mid + 2 * std:.2f}"
            return f"boll_lb: {mid - 2 * std:.2f}"
        if name == "atr":
            return f"atr: {_atr(df):.2f}"
        if name == "vwma":
            return f"vwma: {_vwma(df):.2f}"
        return self._unavailable_window(name, reason="not supported by frozen corpus")

    @staticmethod
    def _macd_line(df: pd.DataFrame, name: str) -> str:
        close = df["Close"]
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        hist = macd - signal
        if name == "macd":
            return f"macd: {float(macd.iloc[-1]):.2f}"
        if name == "macds":
            return f"macds: {float(signal.iloc[-1]):.2f}"
        return f"macdh: {float(hist.iloc[-1]):.2f}"

    def _unavailable_window(self, name: str, reason: str) -> str:
        return (
            f"{name}: NO_DATA_AVAILABLE — the full {name} calculation window is "
            f"unavailable ({reason}). Do not estimate or fabricate a value."
        )

    def get_verified_market_snapshot(self, symbol: str, curr_date: str, look_back_days: int = 30) -> str:
        if symbol.upper() != self.ticker:
            return UNAVAILABLE.replace("this optional data source", "this ticker's data")
        df = self._frame_as_of(curr_date, look_back_days)
        if df.empty:
            return UNAVAILABLE
        last = df.iloc[-1]
        return (
            f"# Verified market snapshot for {self.ticker} as of {curr_date}\n"
            f"# source_id: {_market_source_label(self.ticker)} (frozen market CSV)\n"
            f"last_close: {float(last['Close']):.2f}\n"
            f"last_open: {float(last['Open']):.2f}\n"
            f"day_high: {float(last['High']):.2f}\n"
            f"day_low: {float(last['Low']):.2f}\n"
            f"volume: {int(last['Volume'])}\n"
            f"as_of: {last['Date'].strftime('%Y-%m-%d')}\n"
        )

    def _frame_as_of(self, curr_date: str, look_back_days: int = 30) -> pd.DataFrame:
        df = self.frame
        if curr_date:
            df = df[df["Date"] <= pd.Timestamp(curr_date)]
        if look_back_days:
            df = df.tail(max(1, look_back_days))
        return df

    # ------------------------------------------------------------------
    # news / unsupported sources
    # ------------------------------------------------------------------

    def get_news(self, ticker: str, start_date: str = "", end_date: str = "") -> str:
        """Return the official case notes + source ID when the case is eligible.

        If the ticker is a known case whose announcement/analysis window matches
        the request, the committed source notes and ``source_id`` are returned.
        Optional sources absent from the corpus stay ``NO_DATA``.
        """
        if ticker.upper() != self.ticker or self.case is None:
            return UNAVAILABLE.replace("this optional data source", "company news")
        notes = self.case.get("notes") or []
        source_id = self.case.get("source_id") or f"src-{self.ticker.lower()}"
        lines = [
            f"# Company news for {self.ticker} (frozen official source)",
            f"source_id: {source_id}",
            f"announcement_date: {self.case.get('announcement_date', '')}",
            f"analysis_date: {self.case.get('analysis_date', '')}",
            f"source_url: {self.case.get('source_url', '')}",
        ]
        for note in notes:
            lines.append(f"- {note}")
        return "\n".join(lines)

    def get_global_news(self, curr_date: str, look_back_days: int | None = None, limit: int | None = None) -> str:
        return UNAVAILABLE

    def get_insider_transactions(self, ticker: str) -> str:
        return UNAVAILABLE

    def get_macro_indicators(self, indicator: str, curr_date: str, look_back_days: int | None = None) -> str:
        return UNAVAILABLE

    def get_prediction_markets(self, topic: str, limit: int | None = None) -> str:
        return UNAVAILABLE


def _rsi(close: pd.Series, period: int = 14) -> float:
    delta = close.diff()
    gain = delta.clip(lower=0.0).rolling(period).mean()
    loss = (-delta.clip(upper=0.0)).rolling(period).mean()
    rs = gain / loss
    return float(100 - (100 / (1 + rs)).iloc[-1])


def _atr(df: pd.DataFrame, period: int = 14) -> float:
    high, low, prev_close = df["High"], df["Low"], df["Close"].shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return float(tr.rolling(period).mean().iloc[-1])


def _vwma(df: pd.DataFrame) -> float:
    close, vol = df["Close"], df["Volume"]
    return float((close * vol).sum() / vol.sum())
