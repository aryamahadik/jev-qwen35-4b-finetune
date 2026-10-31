"""opt2_launch.py: the g13_c2 wrapper for owner option 2 (and option 3's capture), all default OFF.

  --frame-excuse RID [--frame-scope code|code+pools]   option 2 (a): frame_excuse.py; RID must carry OHSAC_FRAME_EXCUSE (scope code+pools: also OHSAC_FRAME_POOLS)
  --kw-narrow RID [--kw-dir DIR]                      option 2 (b): keyword_narrow.py; RID must carry OHSAC_KW_NARROW; DIR defaults to c2_build/sealed_hashes_ac_kw2
  --ohsac-report-only RID                              option 3's capture (ac_report_only.py); RID must carry OHSAC_REPORT_ONLY
The three flags are independent (any subset). With none of them, g13_c2.main(argv) runs exactly as before. Every id is checked against
PREREG_FINAL.md before anything is patched; a refusal changes nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ruling_gate as rg  # noqa: E402


def launch(argv: list[str] | None = None, prereg_text: str | None = None):
    cb = rg.lean_on_path()
    argv = list(sys.argv[1:] if argv is None else argv)
    argv, frame = rg.pop_flag(argv, "--frame-excuse")
    argv, scope = rg.pop_flag(argv, "--frame-scope")
    argv, kw = rg.pop_flag(argv, "--kw-narrow")
    argv, kwdir = rg.pop_flag(argv, "--kw-dir")
    argv, rep = rg.pop_flag(argv, "--ohsac-report-only")
    if scope and not frame:
        raise SystemExit("--frame-scope needs --frame-excuse (default OFF)")
    if kwdir and not kw:
        raise SystemExit("--kw-dir needs --kw-narrow (default OFF)")
    f_info = rg.require(frame, rg.FRAME_MARKER, prereg_text) if frame else None
    k_info = rg.require(kw, rg.KW_MARKER, prereg_text) if kw else None
    r_info = rg.require(rep, rg.OPT3_MARKER, prereg_text) if rep else None
    scope = scope or "code"
    if f_info is not None:
        import frame_excuse as fe
        if scope not in fe.SCOPES:
            raise SystemExit(f"--frame-scope must be one of {fe.SCOPES}")
        if scope == "code+pools" and not rg.block_contains(frame, fe.POOLS_MARKER, prereg_text):
            raise SystemExit(f"--frame-scope code+pools needs the ruling {frame} to carry {fe.POOLS_MARKER}. Nothing was changed.")
    import g13_c2 as G
    if f_info is not None:
        fe.install(G, f_info, scope)
    if k_info is not None:
        import keyword_narrow as kn
        kn.install(G, k_info, Path(kwdir) if kwdir else None)
    if r_info is not None:
        import ac_report_only as opt3
        opt3.install_g13_capture(G, r_info)
    return G.main(argv)
