"""T63 render round trip (generator-side render-fidelity check; NOT solver B). The shown table / listing / card re-parses to the spec and
SOLVER A on the parsed record equals the stored gold. Returns a list of problem strings ([] = ok)."""
from . import config as C
from . import exists, lic, near
from . import render as R


def _norm_entries(es):
    return sorted((e["name"], e["registry"], e["publisher"], e["age"], e["dl"], e.get("fork_of") or "") for e in es)


def check(rec):
    spec, text, bad = rec["spec"], rec["rendered"]["context"], []
    head = spec["head"]
    if head == "NEAR":
        fmt = rec["meta"]["fmt"]
        p = R.parse_near_context(text, fmt)
        if _norm_entries(p["entries"]) != _norm_entries(spec["entries"]):
            bad.append("entries")
        if p["card"] != {k: spec["card"][k] for k in ("display", "reserved", "internal_registry", "resolve_order", "own_org")}:
            bad.append("card")
        if p["query"] != spec["query"]:
            bad.append("query")
        if p["registries"] != spec["registries"]:
            bad.append("registries")
        if near.gold_label({"entries": p["entries"], "card": p["card"], "query": p["query"], "registries": p["registries"]}) != rec["gold"]:
            bad.append("parsed_label")
        if len(spec["entries"]) > C.MAX_TABLE_ENTRIES:
            bad.append("table_len")
    elif head == "LIC":
        p = R.parse_lic_context(text)
        if any(p[k] != spec[k] for k in ("dep", "project", "use", "dist")):
            bad.append("card")
    else:
        sub = spec["sub"]
        if sub == "EX-A1":
            blocks = {b["registry"]["id"]: b for b in R.parse_exists_context(text, sub)}
            asked = blocks.get(spec["registry"]["id"])
            if asked is None or asked["listing"] != spec["listing"] or asked["range"] != spec["range"] or asked["registry"] != spec["registry"]:
                bad.append("listing")
            if bool(spec.get("other")) != (len(blocks) == 2) or (spec.get("other") and (spec["other"]["registry"]["id"] not in blocks or
                                                                  blocks[spec["other"]["registry"]["id"]]["listing"] != spec["other"]["listing"])):
                bad.append("other_listing")
            if asked is not None:
                q = spec["query_name"]
                lo, hi = asked["range"]
                if not (lo <= q <= hi):
                    bad.append("outside_range")
                if ("YES" if q in asked["listing"] else "NO") != rec["gold"]:
                    bad.append("parsed_label")
        elif sub == "EX-A2":
            p = R.parse_exists_context(text, sub)
            if p["exports"] != spec["exports"] or p["library"] != spec["library"] or p["version"] != spec["version"]:
                bad.append("exports")
            if ("YES" if spec["query_symbol"] in p["exports"].get(spec["query_module"], ()) else "NO") != rec["gold"]:
                bad.append("parsed_label")
        elif spec["view"] == "B1":
            p = R.parse_exists_context(text, sub)
            if not p or p["shown"] != spec["shown"] or p["range"] != spec["range"] or p["module"] != spec["module"]:
                bad.append("shown")
            else:
                q = spec["query_name"]
                lo, hi = (p["shown"][0], p["shown"][-1]) if p["range"] is None else p["range"]
                if not (lo <= q <= hi):
                    bad.append("outside_range")
                if ("YES" if q in p["shown"] else "NO") != rec["gold"]:
                    bad.append("parsed_label")
    return bad
