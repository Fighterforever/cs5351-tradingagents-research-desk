"""End-to-end CLI vertical slice on fixture evidence (zero external calls).

Drives the real CLI commands (export -> replay -> propose -> review -> execute
-> ledger) against a fixture pack under an isolated desk home, verifying the
whole evidence -> review -> ledger flow works from the operator's terminal.
"""

from __future__ import annotations

import shutil

from typer.testing import CliRunner

from research_desk.cli import app

runner = CliRunner()


def _seed_run(desk_home):
    """Copy the committed aapl fixture into the isolated runs dir under its run_id."""
    from research_desk.config import ResearchDeskSettings

    settings = ResearchDeskSettings(home=desk_home)
    settings.ensure_dirs()
    src = "test/fixtures/packs/aapl_buy_complete"
    dest = settings.runs_dir / "fixture-aapl-buy"
    shutil.copytree(src, dest)
    return settings


def test_cli_vertical_slice(desk_home, monkeypatch):
    monkeypatch.setenv("RESEARCH_DESK_HOME", desk_home)
    settings = _seed_run(desk_home)
    run_id = "fixture-aapl-buy"
    proposal_id = "prop-pl-buy"

    # export -> portable ZIP
    zip_out = str(settings.runs_dir / f"{run_id}.zip")
    r = runner.invoke(app, ["export", run_id, "--out", zip_out])
    assert r.exit_code == 0, r.output
    import os

    assert os.path.exists(zip_out)

    # replay -> offline rebuild with zero external calls, signal reproduced
    r = runner.invoke(app, ["replay", zip_out, "--ledger"])
    assert r.exit_code == 0, r.output
    assert "signal: Buy" in r.output
    assert "external calls: 0" in r.output
    assert "max 100 shares by 10% cap" in r.output

    # propose -> register the pack's PENDING_REVIEW proposal in the store
    r = runner.invoke(app, ["propose", run_id])
    assert r.exit_code == 0, r.output
    assert proposal_id in r.output

    # review approve
    r = runner.invoke(app, ["review", "approve", proposal_id, "--shares", "100", "--operator", "leo"])
    assert r.exit_code == 0, r.output

    # execute -> simulated buy, cash debited
    r = runner.invoke(app, ["execute", proposal_id, "--operator", "leo"])
    assert r.exit_code == 0, r.output
    assert "cash now" in r.output

    # ledger -> state shows the result
    r = runner.invoke(app, ["ledger"])
    assert r.exit_code == 0, r.output
    assert "90,000.00" in r.output  # 100000 - 100*100
    assert "AAPL" in r.output

    # re-execute -> idempotent, no double debit
    r = runner.invoke(app, ["execute", proposal_id, "--operator", "leo"])
    assert r.exit_code == 0, r.output
    r = runner.invoke(app, ["ledger"])
    assert "90,000.00" in r.output


def test_cli_reject_leaves_ledger_untouched(desk_home, monkeypatch):
    monkeypatch.setenv("RESEARCH_DESK_HOME", desk_home)
    _seed_run(desk_home)
    proposal_id = "prop-pl-buy"
    runner.invoke(app, ["propose", "fixture-aapl-buy"])
    r = runner.invoke(app, ["review", "reject", proposal_id, "--operator", "leo"])
    assert r.exit_code == 0, r.output
    r = runner.invoke(app, ["execute", proposal_id, "--operator", "leo"])
    assert r.exit_code == 0, r.output
    r = runner.invoke(app, ["ledger"])
    assert "100,000.00" in r.output  # unchanged


def test_cli_replay_incomplete_fails(desk_home, monkeypatch, tmp_path):
    monkeypatch.setenv("RESEARCH_DESK_HOME", desk_home)
    from research_desk.evidence import EvidencePackError

    bad = tmp_path / "bad"
    shutil.copytree("test/fixtures/packs/aapl_buy_complete", bad)
    (bad / "usage.json").unlink()
    r = runner.invoke(app, ["replay", str(bad)])
    assert r.exit_code != 0
    assert isinstance(r.exception, EvidencePackError)
    assert "missing required files" in str(r.exception)


def test_cli_ledger_report_renders(desk_home, monkeypatch):
    monkeypatch.setenv("RESEARCH_DESK_HOME", desk_home)
    _seed_run(desk_home)
    runner.invoke(app, ["propose", "fixture-aapl-buy"])
    runner.invoke(app, ["review", "approve", "prop-pl-buy", "--shares", "100", "--operator", "leo"])
    runner.invoke(app, ["execute", "prop-pl-buy", "--operator", "leo"])
    r = runner.invoke(app, ["ledger", "--report"])
    assert r.exit_code == 0
    assert "Positions" in r.output  # Rich renders the markdown heading without '##'
    assert "Transactions" in r.output
