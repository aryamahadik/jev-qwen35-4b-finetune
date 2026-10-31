"""A54 (4): rebuild ONLY a family's mixdev (spec 7.1) after the held-out wording patch; candidates stay untouched.
Mirrors gen_full_c2.run (same exclusions, redraw and mixdev seed base from the family's GEN_REPORT) and
qc_full_c2.apply_drops (the G5-H quarantined templates also leave the mixdev). Backs up the old mixdev files first,
rewrites out/mixdev_S5.jsonl, qc/_generated/mixdev_S5.jsonl, the MANIFEST mixdev entry and GEN_REPORT/DROPS mixdev
counts, then checks the A53 precondition (g13_c2.A53Context) against the family's candidates.
Run from lean/c2_build:  ../../.venv/bin/python -B zed_orch/a54_rebuild_mixdev.py T23 [--check-only]"""
import json, shutil, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'zed_orch'))
import gen_full_c2 as G  # noqa: E402
import qc_full_c2 as Q  # noqa: E402
import g13_c2 as X  # noqa: E402
import a54_heldout_overlay as OV  # noqa: E402
from c2_kit import paths  # noqa: E402


def precondition(fam, mix_rows):
    L = G.layout(fam)
    cand = [json.loads(x) for x in L["cand"].read_text().splitlines() if x.strip()]
    ctx = X.A53Context(fam, cand, X.block_dir(fam))
    for r in mix_rows:
        r.setdefault("meta", {})
    return ctx.precondition(mix_rows)


def rebuild(fam, extract_root=None):
    t0 = time.time()
    ov = {}
    L = G.layout(fam)
    gen = json.loads(L["gen"].read_text())
    mix_base = gen["seeds"]["mixdev"]
    src = G.quarantine_sources(fam)
    banned = set().union(*map(set, src.values()))
    with G.loader_patch(fam), OV.patched(fam, extract_root, ov):
        with G.PL.open_family(fam) as kit0:
            kit, xrep = G.apply_exclusions(kit0, banned)
            rd = G.Redraw(kit.plugin, xrep["dead_qforms"]) if (fam not in G.FALLBACK_FAMILIES and xrep["dead_qforms"]) else None
            try:
                mix_rows, mix_rep = G.build_mixdev(kit, G.MIXDEV_N, seed_base=mix_base)
            finally:
                if rd:
                    rd.restore()
    drops = json.loads((L["qc"] / "DROPS.json").read_text())
    quarantined = set(drops.get("quarantined_templates") or [])
    _k, _r, kmix, _o = Q.apply_drops([], [], mix_rows, set(), quarantined)
    pre = precondition(fam, kmix)
    res = {"family": fam, "mixdev_built": len(mix_rows), "mixdev_after_quarantine": len(kmix), "attempts": mix_rep.get("attempts"),
           "drops": mix_rep.get("drops"), "not_dev_only": mix_rep.get("not_dev_only"), "a53_precondition": pre,
           "overlay": ov, "wording_ids_mixdev": len({r["meta"]["wording_id"] for r in kmix}), "seconds": round(time.time() - t0, 1)}
    if L["mixdev"].exists():
        dump = lambda r: json.dumps(r, sort_keys=True, ensure_ascii=False)  # noqa: E731
        res["equals_mixdev_on_disk"] = [dump(r) for r in kmix] == [dump(json.loads(x)) for x in L["mixdev"].read_text().splitlines() if x.strip()]
    if "--check-only" in sys.argv or not pre["ok"] and "--force" not in sys.argv:
        res["written"] = False
        return res
    bk = L["out"].parent / "out" / "_backup_a54" if "out" in L else L["mixdev"].parent / "_backup_a54"
    bk.mkdir(exist_ok=True)
    shutil.copy2(L["mixdev"], bk / "mixdev_S5.jsonl")
    shutil.copy2(L["gendir"] / "mixdev_S5.jsonl", bk / "generated_mixdev_S5.jsonl")
    shutil.copy2(L["man"], bk / "MANIFEST.json")
    paths.write_jsonl(L["gendir"] / "mixdev_S5.jsonl", mix_rows)
    paths.write_jsonl(L["mixdev"], kmix)
    man = json.loads(L["man"].read_text())
    man["mixdev"] = {"mixdev_S5.jsonl": {"sha256": G.sha_file(L["mixdev"]), "rows": len(kmix)}}
    paths.write_json(L["man"], man)
    gen["mixdev"] = {**G._clean(mix_rep), "a54_rebuilt": True}
    paths.write_json(L["gen"], gen)
    drops["mixdev_after"] = len(kmix)
    paths.write_json(L["qc"] / "DROPS.json", drops)
    res["written"] = True
    return res


if __name__ == "__main__":
    er = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--extract-root=")), None)
    for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
        print(json.dumps(rebuild(f, er), default=str), flush=True)
