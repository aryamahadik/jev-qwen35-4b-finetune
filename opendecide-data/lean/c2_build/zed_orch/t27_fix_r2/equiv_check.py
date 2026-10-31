"""The installed code path equals the overlay path: builds the first rows at the candidates base 72,000,000 either with
overlay.patched() on the real families/T27 ("overlay") or with a PATCHED COPY of families/T27 substituted for the package
("installed": install_code.install on a scratch copy, no overlay) and prints a digest of the row ids.
  equiv_check.py overlay|installed [--n 60]      (two separate processes: install_vocab runs once per process)"""
import hashlib, json, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    sys.path.insert(0, p)
mode = sys.argv[1]
n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 60
if mode == "installed":
    import install_code as IC
    root = HERE / "scratch" / "equiv_pkg"
    shutil.rmtree(root, ignore_errors=True)
    fam = root / "T27"
    fam.mkdir(parents=True)
    for f in IC.DEFAULT_FAM.glob("*.py"):
        shutil.copy2(f, fam / f.name)
    shutil.copy2(IC.DEFAULT_FAM / "G0_SPEC.md", fam / "G0_SPEC.md")
    shutil.copytree(IC.DEFAULT_FAM / "pools_v2", fam / "pools_v2")
    (fam / "haiku" / "ovl_i2" / "admitted").mkdir(parents=True)
    shutil.copy2(IC.DEFAULT_FAM / "haiku" / "ovl_i2" / "admitted" / "lexicon_supplement.json", fam / "haiku" / "ovl_i2" / "admitted")
    IC.install(fam, dry=False, pools=False)
    import families
    families.__path__.insert(0, str(root))
import gen_full_c2 as G
import pilot
import contextlib
cm = contextlib.nullcontext()
if mode == "overlay":
    import overlay as O
    cm = O.patched(wordings=False)
src = G.quarantine_sources("T27")
banned = set().union(*map(set, src.values()))
with cm:
    with G.loader_patch("T27"):
        with G.PL.open_family("T27") as kit0:
            import families.T27.plugin as P
            where = P.__file__
            kit, _x = G.apply_exclusions(kit0, banned)
            b = pilot.build_pilot(kit, n, seed_base=72_000_000, run_g15=False)
ids = [i.row["id"] for i in b.infos]
print(json.dumps({"mode": mode, "plugin_file_is_scratch": "equiv_pkg" in where, "rows": len(ids),
                  "digest": hashlib.sha256("\n".join(ids).encode()).hexdigest()[:16]}))
