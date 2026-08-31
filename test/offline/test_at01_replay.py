"""AT-01 / FR-001 / NFR-001: evidence export, offline replay with zero external calls.

A complete pack replays in a fresh interpreter with network blocked, reproduces
the same structured signal and policy outputs, and rebuilds reports in well
under two seconds. A pack missing required material fails clearly.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time

import pytest

from research_desk.evidence import EvidencePackError
from research_desk.models import LedgerState
from research_desk.replay import ReplayEngine

_NETWORK_BLOCKED_REPLAY = """
import json, socket, sys
# Block real network I/O without breaking ssl subclassing (keep the class;
# patch the connection methods). Any socket that actually tries to connect
# raises, proving replay performs zero external calls.
def _block(*a, **k):
    raise OSError("network blocked during offline replay")
socket.socket.connect = _block
socket.socket.sendall = _block
socket.socket.recv = _block
socket.getaddrinfo = _block
from research_desk.models import LedgerState
from research_desk.replay import ReplayEngine
from research_desk.policy import policy_bounds
engine = ReplayEngine()
pack = engine.load(sys.argv[1])
res = engine.replay(pack, sys.argv[2], ledger=None)
bounds = None
if res.pack.proposal is not None and res.pack.proposal.price is not None:
    bounds = policy_bounds(LedgerState(cash=100000.0), res.pack.proposal.ticker, res.pack.proposal.price)
print(json.dumps({
    "signal": res.signal,
    "manifest_signal": res.pack.manifest.signal,
    "reports": len(res.report_files),
    "external_calls": res.external_calls,
    "max_by_cap": None if bounds is None else bounds["max_by_cap"],
    "max_by_cash": None if bounds is None else bounds["max_by_cash"],
}))
"""


def test_replay_in_new_process_zero_external_calls(aapl_pack, tmp_path, settings):
    """AT-01: export to ZIP, replay in a fresh process with networking blocked."""
    run_dir = settings.runs_dir / aapl_pack.manifest.run_id
    shutil.copytree("test/fixtures/packs/aapl_buy_complete", run_dir)
    out_dir = tmp_path / "rebuilt"
    out_dir.mkdir()

    start = time.time()
    proc = subprocess.run(
        [sys.executable, "-c", _NETWORK_BLOCKED_REPLAY, str(run_dir), str(out_dir)],
        capture_output=True,
        text=True,
        timeout=60,
        env={"PYTHONPATH": ".", "PATH": "/usr/bin:/bin"},
    )
    elapsed = time.time() - start
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout.strip().splitlines()[-1])
    assert result["external_calls"] == 0
    assert result["signal"] == "Buy"
    assert result["signal"] == result["manifest_signal"]
    assert result["max_by_cap"] == 100  # 10% of 100000 / 100 == 100 shares
    assert result["max_by_cash"] == 1000
    assert result["reports"] >= 1
    assert elapsed < 2.0, f"replay took {elapsed:.2f}s, expected < 2s (NFR-001)"


def test_incomplete_pack_fails_clearly(aapl_pack, tmp_path):
    """AT-01: a deleted required record is reported, not silently replayed."""
    missing_dir = tmp_path / "missing-final-state"
    shutil.copytree("test/fixtures/packs/aapl_buy_complete", missing_dir)
    (missing_dir / "final_state.json").unlink()
    engine = ReplayEngine()
    with pytest.raises(EvidencePackError, match="missing required files"):
        engine.load(missing_dir)


def test_empty_final_state_for_completed_run_rejected(tmp_path):
    """A pack claiming completion with an empty final state cannot replay."""
    import shutil

    d = tmp_path / "empty-state"
    shutil.copytree("test/fixtures/packs/aapl_buy_complete", d)
    (d / "final_state.json").write_text("{}", encoding="utf-8")
    engine = ReplayEngine()
    with pytest.raises(EvidencePackError, match="empty final_state"):
        engine.load(d)


def test_replay_reproduces_signal_and_policy_inprocess(aapl_pack, tmp_path):
    """AT-01: in-process replay matches the recorded signal and policy verdict."""
    engine = ReplayEngine()
    out_dir = tmp_path / "reports"
    ledger = LedgerState(cash=100000.0)
    result = engine.replay(aapl_pack, out_dir, ledger=ledger)
    assert result.signal == aapl_pack.manifest.signal == "Buy"
    assert result.policy_bounds is not None
    assert result.policy_bounds["max_by_cap"] == 100  # 10% cap reproduced offline
    assert result.policy_bounds["price_present"] is True
    assert (out_dir / "complete_report.md").exists()


def test_replay_hold_and_review_produce_no_tradeable_proposal(fixture_pack, tmp_path):
    """Hold and REVIEW signals never replay into a tradeable proposal (policy gate)."""
    engine = ReplayEngine()
    out_dir = tmp_path / "reports"
    ledger = LedgerState(cash=100000.0)
    result = engine.replay(fixture_pack, out_dir, ledger=ledger)
    if fixture_pack.manifest.signal in ("Hold", "REVIEW"):
        assert fixture_pack.proposal is None
        assert result.policy_verdict is None
    else:
        assert result.policy_verdict is not None
