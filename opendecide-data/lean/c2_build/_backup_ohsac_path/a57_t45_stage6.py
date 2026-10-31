"""A57 step 6 for T45 PROGRAM TEXT (no Haiku pool): final admission of the family's program templates / text against the
OHS-AC FINAL hash export (sealed_hashes_ac, MANIFEST fadec66f..., final suite c2dfefa6...; the post-freeze export holds the
12,680 frozen items + 1,727 post-freeze items, source_manifest_sha256 fcf4b384...). Counts, ids and shas only. Writes nothing
but logs/a57/T45_step6_*.json. Run from c2_build:
  HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 ../../.venv/bin/python -B zed_orch/a57_t45_stage6.py [units|check]
"""
import hashlib, json, re, sys, time
from collections import Counter, defaultdict
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
import g13_c2 as G
import a57_hashcheck_ac as HC
from families.T45 import texts as TX

OUT = C2 / "logs" / "a57"
FINAL_MANIFEST = "fadec66fdb3824ca3e81096c65b15d5e8cac7998a05fc964d0ce1b4fdb36cd9b"
FINAL_SUITE = "c2dfefa685e18a5fac8e2310b409d05a4fb5731fdca7732565405e30d9ccfbaf"
POST_FREEZE_MANIFEST = "305356b695ec591b3529c3649052c8c87c74512c4c15e84bea8b8e8daef20121"
TRAIN_REG = tuple(r for r in TX.REGISTERS if r not in TX.HELD_OUT_REGISTERS)


def program_units():
    """id -> (class, text). class: 'training' (reaches training rows) or 'heldout_register' (dev / sealed only, report only)."""
    U = {}
    for qf, ws in TX.WORDINGS.items():
        for i, w in enumerate(ws):
            U[f"wording.{qf}.{i}"] = ("training", w)
    for qf, t in TX.HEAD_RULES.items():
        U[f"rules_template.{qf}"] = ("training", t)
    for lid in range(TX.N_LEGENDS):
        for qf in TX.QFORMS:
            U[f"rules.{qf}.L{lid:02d}"] = ("training", TX.rules_text(qf, lid))
    for g, ph in TX.GROUP_TEXT.items():
        for i, p in enumerate(ph):
            U[f"group_text.{g}.{i}"] = ("training", p)
    for lab, d in TX.DEFS.items():
        U[f"def.{lab}"] = ("training", d)
        U[f"cardline.{lab}"] = ("training", f"- {TX.DISPLAY[lab]}: {d}")
    for k, c in TX.PLANNED.items():
        U[f"planned.{k}"] = ("training", c)
    for r, lay in TX.LAYOUTS.items():
        cls = "heldout_register" if r in TX.HELD_OUT_REGISTERS else "training"
        for j, p in enumerate(lay):
            if p.strip():
                U[f"layout.{r}.{j}"] = (cls, p)
        U[f"layout.{r}.all"] = (cls, "\n".join(lay))
    return U


def code_units():
    """Program literals of plugin.py (the G13 seed rule: 2+ words) and of texts.py / scenarios.py (same extractor)."""
    out = {}
    for name in ("plugin.py", "scenarios.py", "texts.py"):
        p = G.block_dir("T45") / name
        for i, (t, ln, rt) in enumerate(G.g._seed_texts(p)):
            if len(G.g.words(t)) >= 2:
                out[f"code.{name}#{i}"] = ("training", t)
    return out


def exports():
    ex = HC.ExportsAC()
    st = HC.selftest(ex)
    assert all(st.values()), st
    man = ex.manifest
    meta = {"manifest_sha256": ex.shas["manifest"], "final_suite_sha256": man.get("final_suite_sha256"),
            "post_freeze_manifest_sha256": man.get("post_freeze_manifest_sha256"),
            "source_manifest_sha256": man.get("source_manifest_sha256"), "stage": man.get("stage"), "calls": man.get("calls"),
            "selftest_ok": True}
    # the tool's own is_final only knows the stage names 'final'/'post_surface_final'; the binding record is the addendum shas
    meta["final_by_addendum"] = (meta["manifest_sha256"] == FINAL_MANIFEST and meta["final_suite_sha256"] == FINAL_SUITE
                                 and meta["post_freeze_manifest_sha256"] == POST_FREEZE_MANIFEST)
    meta["tool_is_final_flag"] = ex.is_final
    return ex, meta


def main(which):
    U = dict(program_units()); U.update(code_units())
    OUT.mkdir(exist_ok=True)
    if which == "units":
        print(Counter(c for c, _ in U.values()), len(U)); return
    ex, meta = exports()
    assert meta["final_by_addendum"], meta
    t0 = time.time()
    ids = sorted(U)
    units = [{"key": i, "texts": [("text", U[i][1])] + [("line", ln) for ln in U[i][1].split("\n") if ln.strip() and "\n" in U[i][1]],
              "template": True} for i in ids]
    r = HC.run(units, ex)
    hit = set(r["hit_ids"])
    # per-method detail (which method, which unit), to tell template-sentence hits from anything else
    hits, rep = G.ohs4_hash_hits(units, ex)
    by_unit = defaultdict(list)
    for m, v in hits.items():
        for k in v:
            by_unit[k].append(m)
    rows = [{"id": i, "call_id": i, "state": U[i][1]} for i in ids]
    ac_rows = G.run_checker(G.LEAN / "ohs_ac_sealed" / "tools" / "g13_ohsac_check.py", "--rows", rows)
    trecs = [{"id": i, "text": G.SLOT_RE.sub("{X}", U[i][1])} for i in ids]
    ac_tpl = G.run_checker(G.LEAN / "ohs_ac_sealed" / "tools" / "gtpl_check_ac.py", "--templates", trecs,
                           extra=["--min-shared", "1", "--parts", "all"])
    def pack(x):
        return {k: x.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids", "hit_ids_by_method")}
    res = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "wall_s": round(time.time() - t0),
           "export": meta, "units": len(ids), "by_class": dict(Counter(c for c, _ in U.values())),
           "c2_hash_compare": {"manifest_verified": r["manifest_verified"], "complete": r["complete"], "counts": r["counts"],
                                "hit_ids": r["hit_ids"]},
           "hit_unit_methods": {k: sorted(v) for k, v in sorted(by_unit.items())},
           "ohsac_rows": pack(ac_rows), "ohsac_templates": pack(ac_tpl),
           "unit_sha256": {i: hashlib.sha256(U[i][1].encode()).hexdigest()[:16] for i in ids}}
    (OUT / "T45_step6_program_text.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    show = {k: v for k, v in res.items() if k not in ("unit_sha256", "hit_unit_methods")}
    print(json.dumps(show, default=str)[:4000])
    print("c2 hit units by class:", Counter(U[i][0] for i in hit))
    print("hit prefix counts:", Counter(i.split(".")[0] + "." + (i.split(".")[1] if i.startswith(("layout", "def", "group", "wording", "rules")) else "") for i in hit))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "check")
