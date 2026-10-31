"""Spec-list metadata for G6 (d) (repair3). Spec 8 G6 (d): 'metadata only (depth, rule count, length, option lengths,
number magnitudes, name pool, template id, sampler id, repo)'. Orchestrator ruling for round 1: the (d) features are
only what the model can see in the prompt (the spec list), never hidden construction tags. This keeps qc_lib's
text-derived and row-meta spec-list fields and drops the QC-sidecar tags (sc_*: mechanisms, polarity, decile, qt,
planned_mech, ...) and the construction field meta.edge. Used by g6_specmeta.py; qc_lib.meta_feats is unchanged."""
import math
import qc_lib as L

SPEC_CAT = ("sampler", "format_style", "wording_id", "defs_style", "domain_pack")


def meta_feats_spec(r, s=None):
    m = r["meta"]; v = L.views(r)
    cat = {k: str(m.get(k)) for k in SPEC_CAT}            # sampler id, template ids, name pool
    cat["deep"] = str(m.get("deep"))                       # depth
    num = {"depth": m.get("depth") or 0,                   # depth
           "len_state": len(r["state"]), "len_ins": len(r["instructions"]), "len_card": len(r.get("card") or ""),
           "n_rule_lines": r["instructions"].count("\n") + (r.get("card") or "").count("\n"),   # rule count
           "k_opts": len(v["opts"]) if not L.is_yn(r) else 2}                                   # option count
    nums = [float(x.replace(",", "")) for x in L.NUM_RX.findall(v["q"])][:20]                  # number magnitudes
    num["q_n_numbers"] = len(nums); num["q_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    num["state_n_ids"] = len(set(L.ID_RX.findall(r["state"])))
    num["q_n_ids"] = len(set(L.ID_RX.findall(v["q"])))
    return cat, num
