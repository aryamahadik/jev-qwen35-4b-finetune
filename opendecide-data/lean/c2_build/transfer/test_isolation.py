"""transfer/test_isolation.py: the transfer-dev families stay apart from training (C2_DATA_SPEC 2.2, 3.20; A37 d).

  registry   every transfer plugin is tier transfer_dev in the kit registry
  registers  no transfer register name is a register of any trained family (read from families/*/plugin.py with ast,
             never imported), and no two transfer families share one
  dev-only   every row a transfer plugin renders is meta.dev_only, so rows.validate_row(training=True) refuses it
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from transfer.T19 import fixtures as F19, plugin as P19  # noqa: E402
from transfer.T20 import fixtures as F20, plugin as P20  # noqa: E402
from transfer.T21 import fixtures as F21, plugin as P21  # noqa: E402
from transfer.T36 import fixtures as F36, plugin as P36  # noqa: E402

PLUGINS = ((P36.T36Plugin, F36), (P19.T19Plugin, F19), (P21.T21Plugin, F21), (P20.T20Plugin, F20))


def _training_registers() -> set:
    out = set()
    for p in sorted((C2_BUILD / "families").glob("T*/plugin.py")):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for st in node.body:
                    if isinstance(st, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "REGISTERS"
                                                          for t in st.targets):
                        try:
                            out |= set(ast.literal_eval(st.value))
                        except ValueError:
                            pass
    return out


def test_transfer_plugins_are_transfer_dev():
    for cls, _fx in PLUGINS:
        assert cls.TIER == "transfer_dev" == KP.FAMILIES[cls.FAMILY]


def test_transfer_registers_are_never_training_registers():
    train = _training_registers()
    assert len(train) > 20
    seen = set()
    for cls, fx in PLUGINS:
        regs = set(cls.REGISTERS)
        assert not regs & train, (cls.FAMILY, sorted(regs & train))
        assert not regs & seen, (cls.FAMILY, sorted(regs & seen))
        seen |= regs
        ctx = fx.ctx()
        used = {s.register for s in ctx.skins.values() if s.kind == "skin"}
        assert used <= regs, (cls.FAMILY, sorted(used - regs))


@pytest.mark.parametrize("cls,fx", PLUGINS, ids=[c.FAMILY for c, _ in PLUGINS])
def test_every_rendered_row_is_dev_only(cls, fx):
    ctx = fx.ctx()
    pl = cls(lexicon=ctx.lexicon)
    for seed in range(30):
        for smp in pl.SAMPLERS:
            row = pl.render(pl.sample(seed, smp), ctx).row
            assert row["meta"]["dev_only"] is True
            assert any("dev-only" in p for p in R.validate_row(row, training=True))
