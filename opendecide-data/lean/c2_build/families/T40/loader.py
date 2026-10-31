"""families/T40/loader.py: registers T40 with the pilot at RUNTIME (pilot_loaders.py and c2_kit are never edited).

register() adds "T40" to c2_kit.plugin.FAMILIES (tier agent; the kit registry has no entry yet: kit candidate, BUILD_NOTES) and
pilot_loaders.LOADERS["T40"] (the plugin over the program-authored fixtures; no frozen pool exists for T40 yet).
"""
from __future__ import annotations

import contextlib
import sys
from pathlib import Path

C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot_loaders as PL  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402


@contextlib.contextmanager
def _t40():
    from families.T40 import fixtures
    from families.T40.plugin import T40Plugin
    ctx = fixtures.make_ctx()
    yield PL.FamilyKit("T40", PL.family_dir("T40"), T40Plugin(lexicon=ctx.lexicon), ctx,
                       "families/T40/fixtures.make_ctx(): program-authored wordings and headers (stand-in admissions)",
                       "none (program text)", ["no Haiku pool yet: wordings admitted by program stand-in extractors"])


def register() -> None:
    KP.FAMILIES.setdefault("T40", "agent")
    PL.LOADERS["T40"] = _t40
    if "T40" not in PL.PROGRAM_FAMILIES:
        PL.PROGRAM_FAMILIES = tuple(PL.PROGRAM_FAMILIES) + ("T40",)
