"""Offline-slice fixtures: isolated home dir, store, and evidence pack loader.

All offline tests run with ``RESEARCH_DESK_HOME`` pointed at a per-test temp
dir, so the real user ledger in ``~/.research_desk`` is never touched and no
test order depends on shared state. The stock fixture packs under
``test/fixtures/packs`` are imported read-only.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from research_desk.config import ResearchDeskSettings
from research_desk.evidence import EvidencePackIO
from research_desk.storage import ResearchDeskStore

FIXTURES = {
    "aapl_buy": "aapl_buy_complete",
    "msft_review": "msft_review",
    "tsla_hold": "tsla_hold",
    "nvda_compact_memory": "nvda_compact_memory",
}


@pytest.fixture()
def desk_home(tmp_path):
    home = tmp_path / "desk"
    home.mkdir()
    yield str(home)


@pytest.fixture()
def settings(desk_home):
    s = ResearchDeskSettings(home=desk_home)
    s.ensure_dirs()
    return s


@pytest.fixture()
def store(settings):
    st = ResearchDeskStore(settings.db_path)
    yield st
    st.close()


@pytest.fixture()
def pack_io():
    return EvidencePackIO()


@pytest.fixture(params=["aapl_buy", "msft_review", "tsla_hold", "nvda_compact_memory"])
def fixture_pack(request, pack_io):
    """Each of the four committed fixture packs, imported read-only."""
    return pack_io.import_pack(f"test/fixtures/packs/{FIXTURES[request.param]}")


@pytest.fixture()
def aapl_pack(pack_io):
    return pack_io.import_pack("test/fixtures/packs/aapl_buy_complete")


@pytest.fixture()
def mock_llm_client():
    """Patch the LLM factory so graph construction needs no live API.

    ``TradingAgentsGraph`` binds ``create_llm_client`` into its own module
    namespace at import time, so the patch target is that binding (the factory
    attribute patch in the upstream conftest would not redirect the graph).
    """
    client = MagicMock()
    client.get_llm.return_value = MagicMock()
    with patch(
        "tradingagents.graph.trading_graph.create_llm_client",
        return_value=client,
    ):
        yield client
