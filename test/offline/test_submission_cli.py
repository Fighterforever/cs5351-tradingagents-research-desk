"""Focused contracts for replay, evaluate-case and judge-case CLI status/options."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from research_desk.cli import app
from research_desk.eval import live
from research_desk.eval.live import PROVENANCE_FILENAME, run_judge_case
from research_desk.models import LedgerPosition, LedgerState
from research_desk.replay import ReplayEngine

runner = CliRunner()

AAPL_PACK = "test/fixtures/packs/aapl_buy_complete"


def _evaluate_summary(outcome: str, *, error=None, pack_complete=True) -> dict:
    return {
        "ticker": "AAPL",
        "analysis_date": "2026-07-31",
        "context_mode": "baseline",
        "outcome": outcome,
        "signal": "Hold" if outcome == "budget_stopped" else "Buy",
        "stop_reason": "budget_exhausted" if outcome == "budget_stopped" else "completed",
        "calls": 2,
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
        "wall_seconds": 0.1,
        "error": error,
        "pack_complete": pack_complete,
        "run_dir": "/tmp/run",
    }


def _prepare_judge_runs(monkeypatch, out: Path, modes=("baseline", "compact")) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(live, "_current_source_fingerprint", lambda root: "sha256:current")

    pack = SimpleNamespace(
        manifest=SimpleNamespace(outcome="completed"),
        final_state={"final_trade_decision": "decision"},
        input=SimpleNamespace(available_sources={}),
        events=[],
    )
    from research_desk.evidence import EvidencePackIO

    monkeypatch.setattr(EvidencePackIO, "import_pack", lambda self, source: pack)
    monkeypatch.setattr(live, "_report_text_with_identity", lambda pack: "report")
    monkeypatch.setattr(live, "_deterministic_checks", lambda case, pack, ticker: [])

    for mode in modes:
        (out / "AAPL" / mode / "run").mkdir(parents=True)
        (out / "AAPL" / mode / PROVENANCE_FILENAME).write_text(
            json.dumps({"source_fingerprint": "sha256:current"}), encoding="utf-8"
        )


def _good_score() -> dict:
    return {"support": 0.9, "relevance": 0.8, "error": False}


def test_replay_report_files_are_unique_and_ignore_unrelated_output(aapl_pack, tmp_path):
    out = tmp_path / "reports"
    out.mkdir()
    unrelated = out / "unrelated.txt"
    unrelated.write_text("keep me", encoding="utf-8")

    result = ReplayEngine().replay(
        aapl_pack, out, ledger=LedgerState(cash=100000.0)
    )

    assert result.error is None
    assert all(isinstance(path, str) for path in result.report_files)
    assert len(result.report_files) == len(set(result.report_files))
    complete = out / "complete_report.md"
    assert str(complete) in result.report_files
    assert result.report_files.count(str(complete)) == 1
    assert str(unrelated) not in result.report_files
    assert all(Path(path).exists() for path in result.report_files)


def test_cli_replay_rebuild_failure_is_nonzero_without_success_banner(monkeypatch, tmp_path):
    def _boom(*args, **kwargs):
        raise RuntimeError("cannot rebuild report")

    monkeypatch.setattr("research_desk.replay.write_report_tree", _boom)
    result = runner.invoke(
        app, ["replay", AAPL_PACK, "--out", str(tmp_path / "rebuilt")]
    )

    assert result.exit_code != 0
    assert "report rebuild failed" in result.output
    assert "Replayed" not in result.output


def test_replay_sell_bounds_are_owned_and_nonnegative(aapl_pack, tmp_path):
    pack = copy.deepcopy(aapl_pack)
    pack.proposal.side = "sell"
    pack.proposal.ticker = "AAPL"
    pack.proposal.shares = 10
    pack.proposal.price = 200.0
    ledger = LedgerState(
        cash=90000.0,
        positions={"AAPL": LedgerPosition(ticker="AAPL", shares=100, avg_price=100.0)},
    )

    result = ReplayEngine().replay(pack, tmp_path / "reports", ledger=ledger)

    assert result.error is None
    assert result.signal == pack.manifest.signal
    assert result.policy_bounds["side"] == "sell"
    assert result.policy_bounds["max_sell"] == 100
    assert result.policy_bounds["max_by_cap"] >= 0
    assert result.policy_bounds["max_by_cash"] >= 0
    assert result.policy_verdict.allowed is True


def test_cli_evaluate_case_failed_is_nonzero(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "research_desk.eval.live.run_evaluate_case",
        lambda *args, **kwargs: _evaluate_summary("failed", error="boom"),
    )

    result = runner.invoke(
        app, ["evaluate-case", "AAPL", "--out", str(tmp_path)]
    )

    assert result.exit_code != 0
    assert "outcome=failed" in result.output
    assert "boom" in result.output


def test_cli_evaluate_case_budget_stopped_is_accurate_and_not_success(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "research_desk.eval.live.run_evaluate_case",
        lambda *args, **kwargs: _evaluate_summary("budget_stopped"),
    )

    result = runner.invoke(
        app, ["evaluate-case", "AAPL", "--out", str(tmp_path)]
    )

    assert result.exit_code == 0
    assert "outcome=budget_stopped" in result.output
    assert "outcome=completed" not in result.output
    assert "Budget stopped" in result.output


def test_cli_evaluate_case_completed_with_incomplete_pack_is_nonzero(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "research_desk.eval.live.run_evaluate_case",
        lambda *args, **kwargs: _evaluate_summary("completed", pack_complete=False),
    )

    result = runner.invoke(
        app, ["evaluate-case", "AAPL", "--out", str(tmp_path)]
    )

    assert result.exit_code != 0
    assert "incomplete" in result.output.lower()


def test_cli_judge_case_empty_is_nonzero(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "research_desk.eval.live.run_judge_case",
        lambda *args, **kwargs: {"ticker": "AAPL", "arms": {}},
    )

    result = runner.invoke(app, ["judge-case", "AAPL", "--out", str(tmp_path)])

    assert result.exit_code != 0
    assert "incomplete" in result.output.lower()


def test_cli_judge_case_failed_arm_is_nonzero(monkeypatch, tmp_path):
    arms = {
        "baseline": _good_score(),
        "compact": {"support": None, "relevance": None, "error": True},
    }
    monkeypatch.setattr(
        "research_desk.eval.live.run_judge_case",
        lambda *args, **kwargs: {"ticker": "AAPL", "arms": arms},
    )

    result = runner.invoke(app, ["judge-case", "AAPL", "--out", str(tmp_path)])

    assert result.exit_code != 0
    assert "failed" in result.output.lower()


def test_cli_judge_case_complete_pair_succeeds(monkeypatch, tmp_path):
    arms = {"baseline": _good_score(), "compact": _good_score()}
    monkeypatch.setattr(
        "research_desk.eval.live.run_judge_case",
        lambda *args, **kwargs: {"ticker": "AAPL", "arms": arms},
    )

    result = runner.invoke(app, ["judge-case", "AAPL", "--out", str(tmp_path)])

    assert result.exit_code == 0


def test_judge_max_calls_zero_makes_no_requests(monkeypatch, tmp_path):
    out = tmp_path / "out"
    _prepare_judge_runs(monkeypatch, out)
    calls: list[dict] = []

    def _fake_judge(*args, **kwargs):
        calls.append(kwargs)
        return {}, _good_score()

    monkeypatch.setattr(live, "_llm_judge", _fake_judge)

    result = run_judge_case("AAPL", out, max_calls=0)

    assert calls == []
    assert set(result["arms"]) == {"baseline", "compact"}
    assert all("error" in result["arms"][mode] for mode in ("baseline", "compact"))
    assert not (out / "judge" / "AAPL" / "baseline" / "judge.json").exists()


def test_judge_max_calls_one_uses_only_baseline_and_disables_retries(monkeypatch, tmp_path):
    out = tmp_path / "out"
    _prepare_judge_runs(monkeypatch, out)
    calls: list[dict] = []

    def _fake_judge(*args, **kwargs):
        calls.append(kwargs)
        return {}, _good_score()

    monkeypatch.setattr(live, "_llm_judge", _fake_judge)

    result = run_judge_case("AAPL", out, max_calls=1)

    assert len(calls) == 1
    assert calls[0]["max_retries"] == 0
    assert result["arms"]["baseline"]["error"] is False
    assert "error" in result["arms"]["compact"]
    assert not (out / "judge" / "AAPL" / "compact" / "judge.json").exists()


def test_judge_omitted_max_calls_judges_full_pair_with_default_retries(monkeypatch, tmp_path):
    out = tmp_path / "out"
    _prepare_judge_runs(monkeypatch, out)
    calls: list[dict] = []

    def _fake_judge(*args, **kwargs):
        calls.append(kwargs)
        return {}, _good_score()

    monkeypatch.setattr(live, "_llm_judge", _fake_judge)

    result = run_judge_case("AAPL", out)

    assert len(calls) == 2
    assert calls[0]["max_retries"] is None
    assert result["arms"]["baseline"]["error"] is False
    assert result["arms"]["compact"]["error"] is False


def test_judge_failed_request_still_counts_against_the_cap(monkeypatch, tmp_path):
    out = tmp_path / "out"
    _prepare_judge_runs(monkeypatch, out)
    calls: list[dict] = []

    def _fake_judge(*args, **kwargs):
        calls.append(kwargs)
        raise RuntimeError("network down")

    monkeypatch.setattr(live, "_llm_judge", _fake_judge)

    result = run_judge_case("AAPL", out, max_calls=2)

    assert len(calls) == 2
    assert result["arms"]["baseline"]["error"] is True
    assert result["arms"]["compact"]["error"] is True
    baseline_judge = json.loads(
        (out / "judge" / "AAPL" / "baseline" / "judge.json").read_text(encoding="utf-8")
    )
    assert baseline_judge["error"] is True
    assert baseline_judge["support"] is None


def test_llm_judge_passes_zero_retries_only_when_capped(monkeypatch):
    seen: dict = {}

    class _FakeLLM:
        def __init__(self):
            self.extra_body = None

        def with_structured_output(self, schema, include_raw=False):
            def invoke(_prompt):
                from langchain_core.messages import AIMessage

                parsed = live.JudgeScore(
                    support=1.0,
                    relevance=1.0,
                    cited_claim_count=0,
                    supported_cited_claim_count=0,
                    semantic_valid=True,
                )
                return {"raw": AIMessage(content=""), "parsed": parsed, "parsing_error": None}

            return type("SO", (), {"invoke": staticmethod(invoke)})()

    class _FakeClient:
        def get_llm(self):
            return _FakeLLM()

    def _fake_create(provider, model, **kwargs):
        seen.update(kwargs)
        return _FakeClient()

    monkeypatch.setattr("tradingagents.llm_clients.create_llm_client", _fake_create)

    case = {
        "ticker": "AAPL",
        "analysis_date": "2026-07-31",
        "latest_close": 308.91,
        "source_id": "src-aapl",
        "notes": [],
    }
    live._llm_judge(
        case, "report", [], available_sources={}, events=[], max_retries=0
    )
    assert seen["max_retries"] == 0

    seen.clear()
    live._llm_judge(case, "report", [], available_sources={}, events=[])
    assert "max_retries" not in seen
