"""Install the T27 G11 fix round 2 into families/T27: the generator change and the new ch_next + yn_beyond wordings. RUN ONLY AFTER THE G13
RUN ENDS (g13_c2.py snapshots families/T27/plugin.py and pools_v2/ and flags any change). install.py calls this first.

What it does (every step is refused when already done; originals go to families/T27/_backup_g11_r2/):
  1. copies wording_balance.py and test_wording_balance.py into families/T27/ (byte-identical to the staged files);
  2. plugin.py: `from . import wording_balance as WB` and the bodies of ctx_for / _pick_wording delegate to
     WB.ctx_for / WB.pick_wording (exact-text replacement; refused when the old text is not found exactly once);
  3. pools_v2: appends admitted_wordings.json (redo5: wordings and their lexicon forms, 2/2 G-LEX) to wordings.json and
     lexicon.json (the pool files were built against exactly the shas the payload records), re-pins bytes / records / sha256 in
     MANIFEST.json and adds a "g11_fix_r2" block (A54 merge style, same JSON layout as the freeze);
  4. with --verify: regenerates the first rows from the INSTALLED code (no overlay) at the candidates base and compares their
     ids with the staged candidates (the digest check A54 uses): the installed generator must equal the overlay.

  ../../.venv/bin/python -B zed_orch/t27_fix_r2/install_code.py [--fam-dir DIR] [--dry-run] [--verify] [--no-pools]   (from c2_build)
--fam-dir: a copy of families/T27 (tests); default the real one.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
DEFAULT_FAM = C2 / "families" / "T27"
ADMITTED = HERE / "admitted_wordings.json"
FILES = ("wording_balance.py", "test_wording_balance.py")
IMPORT_OLD = "from . import vocab as V\n"
IMPORT_NEW = "from . import vocab as V\nfrom . import wording_balance as WB\n"
CTX_FOR_NEW = '''    def ctx_for(self, spec: Spec, ctx: KitCtx) -> KitCtx:
        """The kit context with only the carrier skins whose slot layout fits this spec (wordings, attack lines and
        other families' skins pass through), without the wordings that break the polarity rule, so neither render() nor
        the pipeline's complement partner can pick one. G11 fix r2 (16 Oct 2026): the context balances the training
        wordings of each question form (wording_balance.py: least-loaded pick)."""
        return WB.ctx_for(self, spec, ctx)
'''
PICK_NEW = '''    def _pick_wording(self, ctx: KitCtx, spec: Spec, key: str, held: bool):
        """S5 prefers held-out wordings (mixdev); training rows never use them. A wording that breaks the polarity rule
        is never picked (Stage B fix F3). G11 fix r2 (16 Oct 2026): a training row takes the least-loaded wording of its
        question form (wording_balance.py)."""
        return WB.pick_wording(self, ctx, spec, key, held)
'''


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(obj) -> str:
    return json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True) + "\n"


def method_span(src: str, name: str) -> tuple:
    m = list(re.finditer(rf"^    def {re.escape(name)}\(", src, re.M))
    if len(m) != 1:
        raise SystemExit(f"plugin.py: expected exactly one 'def {name}(' found {len(m)}")
    start = m[0].start()
    nxt = re.search(r"^    def |^class |^def ", src[m[0].end():], re.M)
    end = m[0].end() + nxt.start() if nxt else len(src)
    return start, end


def patch_plugin(src: str) -> str:
    if "wording_balance" in src:
        raise SystemExit("plugin.py already imports wording_balance: the code is installed")
    if src.count(IMPORT_OLD) != 1:
        raise SystemExit("plugin.py: the vocab import line is not found exactly once")
    src = src.replace(IMPORT_OLD, IMPORT_NEW)
    for name, new in (("ctx_for", CTX_FOR_NEW), ("_pick_wording", PICK_NEW)):
        a, b = method_span(src, name)
        old = src[a:b]
        gap = old[len(old.rstrip("\n")):]                       # keep the blank line(s) after the method
        src = src[:a] + new.rstrip("\n") + gap + src[b:]
    return src


def merge_pools(pools: Path, pay: dict) -> dict:
    man_p, w_p, l_p = pools / "MANIFEST.json", pools / "wordings.json", pools / "lexicon.json"
    want = pay["pools_sha256"]
    if sha(w_p) != want["wordings.json"] or sha(l_p) != want["lexicon.json"]:
        raise SystemExit("the pools differ from the ones the admitted payload was built against: redo the admission")
    w, lex, man = json.loads(w_p.read_text()), json.loads(l_p.read_text()), json.loads(man_p.read_text())
    if "g11_fix_r2" in man:
        raise SystemExit("MANIFEST.json already holds g11_fix_r2: the pools are merged")
    have = {r["piece_id"] for r in w["records"]}
    have_f = {f["form_id"] for f in lex["forms"]}
    if any(r["piece_id"] in have or r["form_id"] in have_f for r in pay["wordings"]):
        raise SystemExit("a payload wording is already in the pools")
    before = {n: sha(pools / n) for n in ("wordings.json", "lexicon.json")}
    w["records"] = list(w["records"]) + list(pay["wordings"])
    w["count"] = len(w["records"])
    lex["forms"] = list(lex["forms"]) + list(pay["forms"])
    w_p.write_text(dump(w), encoding="utf-8")
    l_p.write_text(dump(lex), encoding="utf-8")
    for n, recs in (("wordings.json", len(w["records"])), ("lexicon.json", len(lex["forms"]))):
        man["pool_files"][n] = {"bytes": (pools / n).stat().st_size, "records": recs, "sha256": sha(pools / n)}
    by_q = dict(sorted(Counter(r["qform"] for r in pay["wordings"]).items()))
    man["g11_fix_r2"] = {"ruling": "PREREG A52 d (generator-fix round)", "added_wordings": len(pay["wordings"]),
                         "added_by_qform": by_q, "qforms": sorted(by_q), "held_out": False, "files_before": before,
                         "files_after": {n: sha(pools / n) for n in before},
                         "source": "zed_orch/t27_fix_r2/admitted_wordings.json (redo5: Haiku authoring, family lint, 2/2 G-LEX)",
                         "payload_sha256": sha(ADMITTED) if ADMITTED.is_file() else None}
    man_p.write_text(dump(man), encoding="utf-8")
    return {"added": len(pay["wordings"]), "sha_before": before, "sha_after": man["g11_fix_r2"]["files_after"]}


def install(fam: Path, *, dry: bool, pools: bool) -> dict:
    bk = fam / "_backup_g11_r2"
    if bk.exists():
        raise SystemExit(f"{bk} exists: already installed")
    plugin = fam / "plugin.py"
    new_src = patch_plugin(plugin.read_text(encoding="utf-8"))
    pay = json.loads(ADMITTED.read_text()) if (pools and ADMITTED.is_file()) else None
    if pools and pay is None:
        raise SystemExit("admitted_wordings.json is missing (use --no-pools to install the code only)")
    rep = {"plugin_sha_before": sha(plugin)}
    if dry:
        return {**rep, "dry_run": True, "plugin_lines_changed": abs(new_src.count("\n") - plugin.read_text().count("\n")),
                "pool_wordings_to_add": len(pay["wordings"]) if pay else 0}
    bk.mkdir()
    shutil.copy2(plugin, bk / "plugin.py")
    for n in ("wordings.json", "lexicon.json", "MANIFEST.json"):
        if (fam / "pools_v2" / n).is_file():
            shutil.copy2(fam / "pools_v2" / n, bk / n)
    for n in FILES:
        shutil.copy2(HERE / n, fam / n)
        if sha(HERE / n) != sha(fam / n):
            raise SystemExit(f"{n}: copy differs")
    plugin.write_text(new_src, encoding="utf-8")
    rep["plugin_sha_after"] = sha(plugin)
    rep["wording_balance_sha"] = sha(fam / "wording_balance.py")
    if pay:
        rep["pools"] = merge_pools(fam / "pools_v2", pay)
        man_p = fam / "pools_v2" / "MANIFEST.json"
        man = json.loads(man_p.read_text())
        man.setdefault("code", {})["plugin.py"] = rep["plugin_sha_after"]
        man["code"]["wording_balance.py"] = rep["wording_balance_sha"]
        man_p.write_text(dump(man), encoding="utf-8")
    return rep


def verify(rows_n: int = 80) -> dict:
    """The INSTALLED generator (no overlay) rebuilds the first rows of the staged candidates (same base, same order)."""
    sys.path.insert(0, str(C2))
    import gen_full_c2 as G
    import pilot
    cand = HERE / "gen_root" / "T27" / "out" / "candidates_c2.jsonl"
    if not cand.is_file():
        return {"verify": "skipped: no staged candidates yet"}
    staged = [json.loads(l)["id"] for l in cand.open()][:rows_n]
    src = G.quarantine_sources("T27")
    banned = set().union(*map(set, src.values()))
    with G.loader_patch("T27"):
        with G.PL.open_family("T27") as kit0:
            kit, _x = G.apply_exclusions(kit0, banned)
            b = pilot.build_pilot(kit, rows_n, seed_base=72_000_000, run_g15=False)
    got = [i.row["id"] for i in b.infos][:len(staged)]
    return {"verify": "equal" if got == staged else "DIFFERENT", "rows_compared": len(staged),
            "first_difference": next((i for i, (x, y) in enumerate(zip(got, staged)) if x != y), None)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fam-dir", default=str(DEFAULT_FAM))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-pools", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args(argv)
    rep = install(Path(a.fam_dir), dry=a.dry_run, pools=not a.no_pools)
    if a.verify and not a.dry_run:
        rep.update(verify())
    print(json.dumps(rep, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
