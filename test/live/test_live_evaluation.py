"""Opt-in live integration test of the ``evaluate-case`` entry point.

This thin test drives the *existing* ``run_evaluate_case`` application entry
point (the same code the six-case CLI matrix uses) for one frozen AAPL
baseline run, then asserts the actual completed evidence pack is importable and
carries real numeric usage and a final decision.

It is a live test: the model is NOT mocked and no production logic is
duplicated. It is skipped by default and only runs when BOTH of the following
are set in the environment:

- ``RESEARCH_DESK_LIVE_TESTS=1``   (opt-in switch)
- ``DEEPSEEK_API_KEY``            (host-injected credential)

Optional:
- ``DEEPSEEK_BASE_URL``           (host-injected, e.g. a gateway)
- ``RESEARCH_DESK_LIVE_OUT``      (explicit output dir; otherwise a pytest
  ``tmp_path`` is used). ``evaluation/final`` is never touched.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from research_desk.evidence import EvidencePackIO

pytestmark = pytest.mark.skipif(
    os.environ.get("RESEARCH_DESK_LIVE_TESTS") != "1",
    reason="opt-in live test; set RESEARCH_DESK_LIVE_TESTS=1 and DEEPSEEK_API_KEY",
)


def _live_out(tmp_path: Path) -> Path:
    explicit = os.environ.get("RESEARCH_DESK_LIVE_OUT")
    if explicit:
        d = Path(explicit)
        d.mkdir(parents=True, exist_ok=True)
        return d
    return tmp_path


def test_one_frozen_aapl_baseline(tmp_path):
    if "DEEPSEEK_API_KEY" not in os.environ:
        pytest.skip("DEEPSEEK_API_KEY not set; skipping live call")

    from research_desk.eval.live import run_evaluate_case

    out = _live_out(tmp_path)
    summary = run_evaluate_case("AAPL", "baseline", out, max_calls=None)

    # The actual graph must have completed (a failed setup is never 'completed').
    assert summary["outcome"] == "completed", summary

    # The completed pack must import cleanly and carry real material.
    pack = EvidencePackIO().import_pack(Path(summary["run_dir"]))
    assert pack.manifest.outcome == "completed"
    assert pack.manifest.ticker == "AAPL"
    assert pack.manifest.context_mode == "baseline"
    # Real numeric usage from the provider (not a fabricated placeholder).
    assert pack.usage.calls > 0
    assert pack.usage.total_tokens > 0
    assert pack.usage.output_tokens > 0
    # A completed run must carry a final decision.
    assert pack.final_state.get("final_trade_decision"), "completed run lacks a final decision"
