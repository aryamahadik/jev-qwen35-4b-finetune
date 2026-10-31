"""canonical_spec(row): the name-keyed, id-free form of a row's spec that solver B must recover by parsing the stem text
(gate G-A2, render parse-back). Everything B needs is in the stem text; B never sees the generator's internal ids.

Output is plain JSON types only. Numbers are strings in the canonical row format (fmt_num). Lists keep stem order where the
stem order is meaningful and are sorted where it is not (stated in SCHEMA.md).
"""
from gen_common import dec, fmt_num


def _arith(spec):
    nm = spec["names"]
    out = {"form": spec["form"], "count_noun": spec.get("count_noun"),
           "bases": [{"name": nm[b["id"]], "value": b["value"], "unit": b["unit"]} for b in spec["base"]],
           "steps": [{"out": nm[s["id"]], "op": s["op"], "args": [nm[a] for a in s["args"]], "param": s["param"]} for s in spec["steps"]],
           "final": nm[spec["final"]]}
    if "f2" in spec:
        out["f2"] = {"cmp": spec["f2"]["cmp"], "thr": spec["f2"]["thr"]}
    if "f3" in spec:
        out["f3_lines"] = [{"out": nm[l["id"]], "op": l["op"], "args": [nm[a] for a in l["args"]], "param": l["param"], "value": l["value"], "unit": l["unit"]}
                           for l in spec["f3"]["lines"]]
    return out


def _atom(spec, a):
    a = tuple(a)
    if a[0] == "P":
        return {"pred": spec["pred_names"][a[1]], "entity": spec["ent_names"][a[2]]}
    return {"rel": spec["rel_name"], "from": spec["ent_names"][a[1]], "to": spec["ent_names"][a[2]]}


def _logic(spec):
    if spec["form"] == "LG-L3":
        nm = spec["item_names"]
        cons = []
        for c in spec["constraints"]:
            d = {"t": c["t"], "a": nm[c["a"]]}
            if "b" in c:
                d["b"] = nm[c["b"]]
            if "pos" in c:
                d["pos"] = c["pos"]
            cons.append(d)
        return {"form": "LG-L3", "items": list(nm), "constraints": cons}
    out = {"form": spec["form"], "entities": list(spec["ent_names"]), "preds": list(spec["pred_names"]), "rel": spec.get("rel_name"),
           "facts": [{"atom": _atom(spec, a), "sign": bool(s)} for a, s in spec["facts"]],
           "rules": [{"kind": r["kind"], "body": [spec["pred_names"][p] for p in r["body"]], "head": {"pred": spec["pred_names"][r["head"][0]], "sign": bool(r["head"][1])}}
                     for r in spec["rules"]]}
    if spec["form"] in ("LG-L1", "LG-L4"):
        a, s = spec["query"]
        out["query"] = {"atom": _atom(spec, a), "sign": bool(s)}
    else:
        out["options"] = [{"atom": _atom(spec, a), "sign": bool(s)} for a, s in spec["options"]]
    return out


def _causal(spec):
    nm = spec["var_names"]
    parents = {int(k): v for k, v in spec["parents"].items()}
    form = spec["form"]
    edges = sorted([nm[a], nm[b]] for b, ps in parents.items() for a in ps)
    if form in ("CA-C1", "CA-C2"):
        fn = {int(k): v for k, v in spec["fn"].items()}
        out = {"form": form, "vars": list(nm), "functions": {nm[j]: {"parents": [nm[p] for p in parents[j]], **fn[j]} for j in fn},
               "do": {"var": nm[spec["do"]["var"]], "val": spec["do"]["val"]}, "target": nm[spec["target"]]}
        if form == "CA-C1":
            out["roots"] = {nm[int(j)]: v for j, v in spec["roots"].items()}
        else:
            out["observed"] = {nm[int(j)]: v for j, v in spec["obs"].items()}
        return out
    out = {"form": form, "vars": list(nm), "edges": edges}
    if form == "CA-C3":
        out.update({"z": nm[spec["z"]], "t": nm[spec["t"]], "o": nm[spec["o"]]})
    elif form == "CA-C4":
        out.update({"t": nm[spec["t"]], "o": nm[spec["o"]], "options": [sorted(nm[j] for j in Z) for Z in spec["options"]]})
    else:
        out.update({"x": nm[spec["x"]], "y": nm[spec["y"]], "given": sorted(nm[j] for j in spec["z"])})
    return out


def _temporal(spec):
    form = spec["form"]
    if form == "TM-T1":
        return {"form": form, "start": spec["start"], "ops": spec["ops"], "month_rule": spec["month_rule"],
                "weekend": sorted(spec["weekend"]) if any(o["unit"] == "business_day" for o in spec["ops"]) else None,
                "holidays": sorted(spec["holidays"]) if any(o["unit"] == "business_day" for o in spec["ops"]) else None}
    if form == "TM-T2":
        return {"form": form, "events": {spec["names"][0]: spec["t1"], spec["names"][1]: spec["t2"]}, "from": spec["names"][0], "to": spec["names"][1], "fmt": spec["fmt"]}
    if form == "TM-T3":
        return {"form": form, "intervals": {spec["names"][0]: spec["iv1"], spec["names"][1]: spec["iv2"]}, "asked": [spec["names"][0], spec["names"][1]]}
    if spec["variant"] == "plan":
        return {"form": form, "variant": "plan", "window": [spec["win_start"], spec["win_end"]],
                "tasks": sorted(({"name": t["name"], "dur": t["dur"], "after": sorted(t["after"])} for t in spec["tasks"]), key=lambda x: x["name"])}
    return {"form": form, "variant": "overlap", "bookings": {spec["names"][0]: spec["b1"], spec["names"][1]: spec["b2"]}, "asked": [spec["names"][0], spec["names"][1]]}


def _table(spec):
    out = {"form": spec["form"], "tables": [{"label": t["label"], "columns": [[c["name"], c["type"]] for c in t["columns"]], "rows": t["rows"]} for t in spec["tables"]],
           "query": spec["query"]}
    if "claim" in spec:
        out["claim"] = spec["claim"]
    return out


def canonical_spec(spec):
    f = spec["form"]
    if f.startswith("AR"):
        return _arith(spec)
    if f.startswith("LG"):
        return _logic(spec)
    if f.startswith("CA"):
        return _causal(spec)
    if f.startswith("TM"):
        return _temporal(spec)
    return _table(spec)
