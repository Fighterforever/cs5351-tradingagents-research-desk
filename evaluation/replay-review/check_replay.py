"""Check the 12 archived release packs through the replay CLI in fresh interpreters.

Run from the project root with its virtual-environment Python. Set
REPLAY_CHECK_RECORD to write the measured results as JSON.
"""

import json
import os
import re
import runpy
import subprocess
import sys
import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path

SYMBOLS = ("AAPL", "AMZN", "GOOGL", "META", "MSFT", "NVDA")
MODES = ("baseline", "compact")


def run_child():
    pack, output, audit_file = map(Path, sys.argv[2:])
    blocked = []
    watched = {
        "socket.connect", "socket.getaddrinfo", "socket.gethostbyname",
        "socket.gethostbyaddr", "socket.getnameinfo", "socket.sendto",
        "socket.sendmsg", "subprocess.Popen", "os.fork", "os.posix_spawn", "os.exec",
    }

    def guard(event, args):
        if event in watched:
            blocked.append(event)
            raise PermissionError(f"Offline replay blocked {event}")

    sys.addaudithook(guard)
    sys.argv = ["research-desk", "replay", str(pack), "--out", str(output), "--ledger"]
    try:
        runpy.run_module("research_desk.cli", run_name="__main__")
    finally:
        audit_file.write_text(json.dumps(blocked), encoding="utf-8")


class ReleaseReplay(unittest.TestCase):
    def test_fixed_cases(self):
        root = Path.cwd()
        record = {
            "check": "Replay archived signals and check reported buy limits against the fixed teaching policy",
            "reference": "Stored signal in the run manifest; calculated limits for an empty USD 100,000 account, a 10% purchase cap and the frozen case price",
            "runs": [],
        }
        for ticker in SYMBOLS:
            for mode in MODES:
                with self.subTest(ticker=ticker, mode=mode), tempfile.TemporaryDirectory() as tmp:
                    arm = root / "evaluation" / "release" / ticker / mode
                    pack = arm / "run"
                    temp = Path(tmp)
                    report = temp / "report"
                    audit_file = temp / "audit.json"
                    env = {
                        "PATH": os.defpath,
                        "TMPDIR": str(temp),
                        "RESEARCH_DESK_HOME": str(temp / "ledger"),
                        "PYTHONDONTWRITEBYTECODE": "1",
                        "COLUMNS": "160",
                    }
                    start = time.monotonic()
                    proc = subprocess.run(
                        [sys.executable, str(Path(__file__).resolve()), "--child",
                         str(pack), str(report), str(audit_file)],
                        env=env, capture_output=True, text=True, check=False, timeout=30,
                    )
                    elapsed = round(time.monotonic() - start, 4)
                    signal = json.loads((pack / "manifest.json").read_text())["signal"]
                    expected_report = report / "complete_report.md"
                    row = {"ticker": ticker, "mode": mode, "archived_signal": signal,
                           "exit_code": proc.returncode, "elapsed_seconds": elapsed,
                           "within_two_seconds": elapsed < 2.0}
                    record["runs"].append(row)
                    self.assertTrue(audit_file.is_file(), proc.stderr)
                    row["blocked_events"] = json.loads(audit_file.read_text())
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertEqual(row["blocked_events"], [])
                    match = re.search(r"^signal: (.+)$", proc.stdout, re.MULTILINE)
                    row["replayed_signal"] = match.group(1).strip() if match else None
                    self.assertEqual(row["replayed_signal"], signal)
                    self.assertTrue(expected_report.is_file() and expected_report.stat().st_size > 0)
                    proposal = pack / "proposal.json"
                    if signal == "Hold":
                        self.assertFalse(proposal.is_file())
                        self.assertNotIn("policy:", proc.stdout)
                        row["policy"] = "No trade proposal"
                    else:
                        p = json.loads(proposal.read_text())
                        self.assertEqual(p["signal"], signal)
                        self.assertIsNone(p["shares"])
                        expected_side = {"Overweight": "buy", "Underweight": "sell"}[signal]
                        self.assertEqual(p["side"], expected_side)
                        price = Decimal(str(json.loads((arm / "case.json").read_text())["latest_close"]))
                        proposal_price = Decimal(str(p["price"]))
                        cent = Decimal("0.01")
                        self.assertEqual(proposal_price.quantize(cent), price.quantize(cent))
                        cap = int(Decimal(10000) // price)
                        cash = int(Decimal(100000) // price)
                        self.assertIn(f"policy: max {cap} shares by 10% cap, max {cash} by cash", proc.stdout)
                        self.assertIn("policy allowed: False", proc.stdout)
                        row.update({"policy": "Purchase bounds; quantity unspecified",
                                    "proposal_side": expected_side,
                                    "case_price_usd": str(price), "proposal_price_usd": str(proposal_price),
                                    "max_additional_buy_by_position_cap": cap, "max_buy_by_cash": cash})
                    row["passed"] = True
        if destination := os.environ.get("REPLAY_CHECK_RECORD"):
            Path(destination).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--child"]:
        run_child()
    else:
        unittest.main()
