#!/usr/bin/env python3
"""s00_env: assert the build environment and the internal consistency of build/config.yaml (DESIGN 13 step 0).

Checks (any failure exits non-zero):
  * python 3.12; exact pins datasets==4.8.5, transformers==4.57.6, gliclass==0.1.17, typesafe-sdk==0.7.1
  * required packages installed (sentence-transformers, datasketch, spacy + en_core_web_sm, ...); versions recorded
  * installed packages match build/requirements.lock.txt (drift is reported; an exact-pin drift fails)
  * sentence-transformers/all-MiniLM-L6-v2 present in the HF cache at the pinned sha (config models.minilm)
  * typesafe_sdk._schemas.models.SystemOneRequest importable (else deviation D6 applies; recorded, not fatal)
  * spaCy en_core_web_sm loads and tags a proper noun NNP (the 3.3 lowercasing rule depends on it)
  * seed / id rules reproduce the DESIGN formulas
  * every total declared in config.yaml equals the sum of its parts, and matches design/design_plan.py
Writes data/reports/env.json. Heavy imports (torch, gliclass) happen only with --deep.

authored_by: llm:claude:foundation-engineer-1
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.metadata as md
import platform
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common  # noqa: E402

STEP = "s00_env"


class Checks:
    def __init__(self, log):
        self.log = log
        self.results: list[dict] = []

    def check(self, name: str, ok: bool, detail: object = "", *, fatal: bool = True) -> bool:
        status = "pass" if ok else ("fail" if fatal else "warn")
        self.results.append({"check": name, "status": status, "detail": detail})
        (self.log.info if ok else (self.log.error if fatal else self.log.warning))("%s %s %s", status.upper(), name,
                                                                                    detail if detail != "" else "")
        return ok

    @property
    def failed(self) -> list[str]:
        return [r["check"] for r in self.results if r["status"] == "fail"]


def dist_version(name: str) -> str | None:
    for cand in (name, name.replace("-", "_"), name.replace("_", "-"), name.lower()):
        try:
            return md.version(cand)
        except md.PackageNotFoundError:
            continue
    return None


def canon(name: str) -> str:
    return name.lower().replace("_", "-").replace(".", "-")


def check_packages(c: Checks) -> dict:
    versions = {}
    py = platform.python_version()
    c.check("python_version", py.startswith(str(common.cfg("env", "python")) + "."), py)
    for pkg, want in common.cfg("env", "packages_exact").items():
        got = dist_version(pkg)
        versions[pkg] = got
        c.check(f"pin:{pkg}", got == str(want), f"installed {got}, required {want}")
    for pkg in common.cfg("env", "packages_required"):
        got = dist_version(pkg)
        versions[pkg] = got
        c.check(f"present:{pkg}", got is not None, got or "missing")
    # drift against requirements.lock.txt
    lock_path = common.ROOT / common.cfg("env", "requirements_lock")
    if c.check("requirements_lock_exists", lock_path.exists(), common.rel(lock_path)):
        locked = {}
        for line in lock_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "==" in line:
                n, v = line.split("==", 1)
                locked[canon(n)] = v.strip()
            elif " @ " in line:
                locked[canon(line.split(" @ ", 1)[0])] = "@url"
        installed = {canon(d.metadata["Name"]): d.version for d in md.distributions() if d.metadata["Name"]}
        drift = {n: {"lock": v, "installed": installed.get(n)} for n, v in sorted(locked.items())
                 if v != "@url" and installed.get(n) != v}
        missing = sorted(n for n, v in locked.items() if n not in installed)
        extra = sorted(n for n in installed if n not in locked)
        c.check("requirements_lock_match", not drift and not missing,
                {"drift": drift, "missing": missing, "extra_not_in_lock": extra}, fatal=False)
    return versions


def check_minilm(c: Checks) -> None:
    m = common.cfg("models", "minilm")
    repo, sha = m["repo"], m["revision"]
    snap = common.HF_HOME / "hub" / ("models--" + repo.replace("/", "--")) / "snapshots" / sha
    need = ["config.json", "modules.json", "sentence_bert_config.json", "tokenizer.json", "model.safetensors",
            "1_Pooling/config.json"]
    missing = [f for f in need if not (snap / f).exists()]
    c.check("minilm_cached_at_pin", not missing, {"snapshot": str(snap), "missing": missing})


def check_typesafe(c: Checks) -> None:
    try:
        mod = importlib.import_module("typesafe_sdk._schemas.models")
        ok = hasattr(mod, "SystemOneRequest")
    except Exception as exc:  # D6: fall back to a local schema from docs.typesafe.ai
        ok, exc_s = False, repr(exc)
    else:
        exc_s = ""
    c.check("typesafe_request_schema", ok, exc_s or "typesafe_sdk._schemas.models.SystemOneRequest", fatal=False)


def check_spacy(c: Checks) -> str | None:
    try:
        import spacy
        nlp = spacy.load(common.cfg("env", "spacy_model"), disable=["parser", "ner", "lemmatizer"])
        tags = [t.tag_ for t in nlp("Paris is where the bank sent my card.")]
        c.check("spacy_tagger", tags[0] == "NNP", tags)
        return nlp.meta.get("version")
    except Exception as exc:
        c.check("spacy_tagger", False, repr(exc))
        return None


def check_seed_rules(c: Checks) -> None:
    s = 20260925
    want = int(hashlib.sha256(f"{s}:s04_sample_eval:banking77:g:banking77:test:1742".encode()).hexdigest()[:16], 16)
    c.check("sub_seed_rule", common.sub_seed("s04_sample_eval", "banking77", "g:banking77:test:1742", seed=s) == want)
    key = "E:banking77:test:1742#s0/q3"
    c.check("row_id_rule", common.row_id(key, seed=s) == "r_" + hashlib.sha1(f"{s}|{key}".encode()).hexdigest()[:12])
    st = "Customer message:\nI am still waiting on my card?"
    c.check("call_id_rule", common.call_id("eval", st, seed=s) ==
            "c_" + hashlib.sha1(f"{s}|eval|{st}".encode()).hexdigest()[:12])
    g1 = common.rng("t", "x", "y", seed=s).integers(0, 2**31, 3).tolist()
    g2 = common.rng("t", "x", "y", seed=s).integers(0, 2**31, 3).tolist()
    c.check("rng_deterministic", g1 == g2, g1)
    c.check("norm_text_rule", common.norm_text("Ｃａｒｄ  isn't—HERE!") == "card isn t here", common.norm_text("Ｃａｒｄ  isn't—HERE!"))


def _sum(d: dict, key: str | None = None) -> int:
    return sum((v[key] if key else v) for v in d.values())


def check_config_totals(c: Checks) -> None:
    cf = common.load_config()
    tr = cf["train"]
    c.check("train.L0_rows", _sum(tr["sources"], "rows") == tr["layers"]["L0_base"],
            f"{_sum(tr['sources'], 'rows')} vs {tr['layers']['L0_base']}")
    l2 = {k: v for k, v in tr["L2_consistency"].items()}
    c.check("train.L2_rows", _sum(l2, "rows") == tr["layers"]["L2_consistency"], _sum(l2, "rows"))
    st = l2["score_transforms"]
    c.check("train.score_transforms", st["polarity_reversal"] + st["rebin"] + st["threshold"] == st["rows"])
    l3 = {k: v for k, v in tr["L3_robustness"].items() if isinstance(v, dict)}
    c.check("train.L3_rows", _sum(l3, "rows") == tr["layers"]["L3_robustness"], _sum(l3, "rows"))
    inj = l3["injection_targeted"]
    c.check("train.targeted_family_rows", sum(inj["family_rows"].values()) == inj["rows"])
    c.check("train.targeted_echo_parity", inj["rows"] == l3["echo_controls"]["rows"])
    c.check("train.rows_total", sum(tr["layers"].values()) == tr["rows_total"], sum(tr["layers"].values()))
    mix = tr["question_type_mix"]
    c.check("train.type_mix", abs(mix["noul"] + mix["choice"] + mix["score"] - 1) < 1e-9)
    dm = tr["sources"]["drug"]["score_k_mix"]
    c.check("train.drug_k_mix", abs(sum(dm.values()) - 1) < 1e-9)
    ab = tr["ablations"]["recipes"]
    c.check("train.ablation_rows", ab["A0"]["rows"] == tr["layers"]["L0_base"]
            and ab["A2a"]["rows"] == tr["layers"]["L0_base"] + tr["layers"]["L2_consistency"]
            and ab["A3"]["rows"] == tr["rows_total"])
    dev, dz = cf["dev"], cf["dev_zs"]
    c.check("dev.rows", sum(dev["layers"].values()) == dev["rows_total"])
    c.check("dev_zs.rows", _sum(dz["sources"], "rows") == dz["rows_total"])
    tdd = tr["rows_total"] + dev["rows_total"] + dz["rows_total"]
    c.check("cap.train_dev_devzs", tdd <= cf["caps"]["train_dev_devzs_rows"], f"{tdd} <= {cf['caps']['train_dev_devzs_rows']}")

    ev = cf["eval"]
    ds = ev["datasets"]
    per_dataset: dict[str, int] = {}
    for name, d in ds.items():
        c.check(f"eval.{name}.rows", d["noul"] + d["choice"] + d["score"] == d["rows"])
        per_dataset[d.get("dataset", name)] = per_dataset.get(d.get("dataset", name), 0) + d["states"]
    for name, n in per_dataset.items():      # trap blocks count toward their parent dataset (condaqa, vitaminc)
        c.check(f"eval.{name}.floor", n >= cf["caps"]["per_dataset_state_floor"], n)
    for tname in ("ID", "ZS", "FR"):
        t = ev["tracks"][tname]
        sub = [d for d in ds.values() if d["track"] == tname]
        c.check(f"eval.track.{tname}", sum(d["states"] for d in sub) == t["states"] and sum(d["rows"] for d in sub) == t["rows"],
                f"states {sum(d['states'] for d in sub)}/{t['states']} rows {sum(d['rows'] for d in sub)}/{t['rows']}")
        share = max(d["states"] for d in sub) / t["states"]
        c.check(f"eval.track.{tname}.max_share", share <= cf["caps"]["per_dataset_track_share_max"] + 1e-9 or tname == "FR",
                round(share, 3), fatal=False)
    core_states = sum(d["states"] for d in ds.values())
    core_rows = sum(d["rows"] for d in ds.values())
    c.check("eval.core", core_states == ev["planned_totals"]["core"]["states"] and core_rows == ev["planned_totals"]["core"]["rows"],
            f"{core_states} states, {core_rows} rows")
    dec = ev["planned_totals"]["decisions"]
    c.check("eval.decisions", sum(d["noul"] for d in ds.values()) == dec["noul"] and sum(d["choice"] for d in ds.values()) == dec["choice"]
            and sum(d["score"] for d in ds.values()) == dec["score"] and sum(d["hard_noul"] for d in ds.values()) == dec["hard_noul_headline"])
    rel_sum: dict[str, int] = {}
    for d in ds.values():
        for k, v in d["relations"].items():
            rel_sum[k] = rel_sum.get(k, 0) + v
    rp = ev["relations_planned"]
    mapping = {"complement": "complement_template", "dneg": "double_negation", "trap": "undecidable_trap",
               "edit_contrast": "edit_contrast_groups", "human_complement": "human_complement_planned"}
    bad = {k: (v, rp.get(mapping.get(k, k))) for k, v in rel_sum.items() if rp.get(mapping.get(k, k)) != v}
    c.check("eval.relations", not bad, bad or rel_sum)
    inj, dist = cf["injection"], cf["distractor"]
    inj_calls, inj_rows = sum(a[0] for a in inj["arms"].values()), sum(a[0] * a[1] for a in inj["arms"].values())
    c.check("inj.arms", inj_calls == ev["tracks"]["INJ"]["calls"] and inj_rows == ev["tracks"]["INJ"]["rows"], f"{inj_calls}/{inj_rows}")
    items = inj["eval_items"]
    n_items = sum(sum(items[k].values()) for k in ("choice", "noul", "score"))
    c.check("inj.items", n_items == items["total"] == ev["tracks"]["INJ"]["items"], n_items)
    c.check("inj.e5_attacks", sum(inj["arms"][a][0] for a in ("C_authority_meta", "D_argue_selflabel", "F_encoding_multilingual",
                                                              "H_structured_field")) == inj["e5_attacks"])
    c.check("inj.h_items", sum(inj["h_items"].values()) == inj["arms"]["H_structured_field"][0])
    d_calls, d_rows = sum(a[0] for a in dist["arms"].values()), sum(a[0] * a[1] for a in dist["arms"].values())
    c.check("dist.arms", d_calls == ev["tracks"]["DIST"]["calls"] and d_rows == ev["tracks"]["DIST"]["rows"], f"{d_calls}/{d_rows}")
    c.check("dist.items", sum(dist["eval_items"]["per_dataset"].values()) == dist["eval_items"]["total"])
    cmp_ = cf["comparability"]
    c.check("cmp_anc", cmp_["cmp_b77"]["calls"] + cmp_["anc"]["calls"] == ev["tracks"]["CMP_ANC"]["calls"]
            and cmp_["cmp_b77"]["rows"] + cmp_["anc"]["rows"] == ev["tracks"]["CMP_ANC"]["rows"])
    c.check("rel", cmp_["rel"]["test_retest"]["calls"] + cmp_["rel"]["unbundled"]["calls"] == ev["tracks"]["REL"]["calls"])
    calls = core_states + inj_calls + d_calls + ev["tracks"]["CMP_ANC"]["calls"] + ev["tracks"]["REL"]["calls"]
    jev_rows = core_rows + inj_rows + d_rows + ev["tracks"]["CMP_ANC"]["rows"]
    diag = sum(v["rows"] for v in ev["diag"].values() if isinstance(v, dict))
    c.check("eval.jev_calls", calls == ev["jev_calls"] and calls <= cf["caps"]["jev_calls"], calls)
    c.check("eval.jev_rows", jev_rows == ev["jev_rows"], jev_rows)
    c.check("eval.diag_rows", diag == ev["local_only_rows"] == ev["tracks"]["DIAG"]["rows"], diag)
    c.check("eval.total_rows", jev_rows + diag == ev["rows_total_with_diag"] <= cf["caps"]["eval_plus_diag_rows"], jev_rows + diag)
    wb = cf["wording_banks"]
    aff = wb["aff"]
    per = aff["wordings_per_trainable_style"]
    n_tr = len(aff["styles_trainable"])
    c.check("banks.aff", aff["train"] == n_tr * per["train"] and aff["dev"] == n_tr * per["dev"] + sum(aff["styles_dev_only"].values())
            and aff["eval"] == n_tr * per["eval"] + sum(aff["styles_eval_only"].values())
            and aff["train"] + aff["dev"] + aff["eval"] == wb["asset_counts"]["aff"])
    for bank in ("neg", "qn"):
        b = wb[bank]
        for pool in ("train", "dev", "eval"):
            c.check(f"banks.{bank}.{pool}", sum(v.get(pool, 0) for v in b["classes"].values()) == b[pool])
        c.check(f"banks.{bank}.asset", b["train"] + b["dev"] + b["eval"] == wb["asset_counts"][bank])
    fr = cf["fresh"]
    c.check("fresh.items", fr["accepted_per_family"] * len(fr["families"]) == fr["eval_items"] == ev["tracks"]["FR"]["states"])


def check_design_plan(c: Checks) -> None:
    """Cross-check config.yaml against design/design_plan.py (the calculator DESIGN 10 is produced by)."""
    path = common.ROOT / "design" / "design_plan.py"
    if not path.exists():
        c.check("design_plan", False, "design/design_plan.py missing", fatal=False)
        return
    import importlib.util
    spec = importlib.util.spec_from_file_location("design_plan", path)
    dp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dp)
    ep, tp = dp.eval_plan(), dp.train_plan()
    cf = common.load_config()
    name_map = {"drug_reviews": "drug", "civil_comments": "civil"}
    diffs = {}
    for name, d in dp.C.items():
        cd = cf["eval"]["datasets"].get(name_map.get(name, name))
        if cd is None:
            diffs[name] = "missing in config"
            continue
        for k in ("states", "rows", "noul", "choice", "score", "hard_noul"):
            if cd[k] != d[k]:
                diffs[f"{name}.{k}"] = (cd[k], d[k])
        rel_cd = {k: v for k, v in cd["relations"].items()}
        if rel_cd != d["rel"]:
            diffs[f"{name}.relations"] = (rel_cd, d["rel"])
    c.check("design_plan.eval_datasets", not diffs, diffs)
    c.check("design_plan.totals", ep["total_calls"] == cf["eval"]["jev_calls"] and ep["total_rows"] == cf["eval"]["rows_total_with_diag"],
            {"calls": ep["total_calls"], "rows": ep["total_rows"]})
    c.check("design_plan.train", tp["train_rows"] == cf["train"]["rows_total"] and tp["by_layer"]["L0_base"] == cf["train"]["layers"]["L0_base"]
            and tp["by_layer"]["L2_consistency"] == cf["train"]["layers"]["L2_consistency"]
            and tp["by_layer"]["L3_injection"] + tp["by_layer"]["L3_distractor"] == cf["train"]["layers"]["L3_robustness"],
            tp["by_layer"])


def run(args, log):
    c = Checks(log)
    versions = check_packages(c)
    check_minilm(c)
    check_typesafe(c)
    spacy_model = check_spacy(c)
    check_seed_rules(c)
    check_config_totals(c)
    try:
        check_design_plan(c)
    except Exception as exc:
        c.check("design_plan", False, repr(exc), fatal=False)
    if args.deep:
        try:
            import gliclass  # noqa: F401  (imports torch + transformers)
            from gliclass import GLiClassModel, ZeroShotClassificationPipeline  # noqa: F401
            c.check("gliclass_import", True, "gliclass imports with the pinned transformers")
        except Exception as exc:
            c.check("gliclass_import", False, repr(exc))
    du = shutil.disk_usage(str(common.ROOT))
    report = {
        "step": STEP,
        "python": platform.python_version(),
        "interpreter": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "versions": versions,
        "spacy_model_version": spacy_model,
        "minilm": common.cfg("models", "minilm"),
        "disk_free_gb": round(du.free / 2**30, 1),
        "master_seed": common.master_seed(),
        "checks": c.results,
        "failed": c.failed,
    }
    out = common.write_json(common.REPORTS / "env.json", report)
    if c.failed:
        return {"ok": False, "error": f"failed checks: {c.failed}", "outputs": [out["path"]]}
    inputs = [common.ROOT / common.cfg("env", "requirements_lock"), common.ROOT / "design" / "design_plan.py"]
    return {"outputs": [out["path"]], "inputs": inputs, "info": {"n_checks": len(c.results),
                                               "warnings": [r["check"] for r in c.results if r["status"] == "warn"]}}


if __name__ == "__main__":
    ap = common.step_argparser(__doc__.splitlines()[0])
    ap.add_argument("--deep", action="store_true", help="also import gliclass (loads torch + transformers)")
    sys.exit(common.step_main(STEP, __file__, run, parser=ap))
