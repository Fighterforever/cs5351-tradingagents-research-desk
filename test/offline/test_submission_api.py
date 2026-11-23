import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from check_static import api_incompatibilities  # noqa: E402


def _src(sig):
    return "def f" + sig + ": pass"


@pytest.mark.parametrize(
    "before,after,expected",
    [
        ("(a=0)", "(a)", True),
        ("(a)", "(a, /)", True),
        ("(a)", "(a, *, b)", True),
        ("(*, count=3)", "(*, count)", True),
        ("(*args)", "()", True),
        ("(a)", "(a, *, note=None)", False),
        ("(a, /)", "(a)", False),
        ("(a)", "(a)", False),
    ],
)
def test_signature_compat(before, after, expected):
    assert bool(api_incompatibilities(_src(before), _src(after))) is expected


def test_required_constructor_and_required_argument():
    before = ("def f(a):\n    return a\n")
    after = ("def f(a, b):\n    return a + b\n")
    assert len(api_incompatibilities(before, after)) == 1

    before = ("def f(*, note=None):\n    return note\n")
    after = ("def f():\n    return None\n")
    assert len(api_incompatibilities(before, after)) == 1

    before = (
        "class C:\n"
        "    def __init__(self, x):\n"
        "        self.x = x\n"
        "    def m(self):\n"
        "        return self.x\n"
    )
    after = (
        "class C:\n"
        "    def __init__(self, x, y):\n"
        "        self.x = x\n"
        "        self.y = y\n"
    )
    assert len(api_incompatibilities(before, after)) == 2
