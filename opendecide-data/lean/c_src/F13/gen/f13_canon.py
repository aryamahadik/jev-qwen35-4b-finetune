"""F13 canonical structure + hashes (G0 7.2 #6 structure_hash, g12_hash). Pure data functions over the fact-dict
schema documented in f13_model (the generator's model and the parser's output share that DATA schema; this module
holds no grammar and no semantics). Used by the generator (on the model) and by G3 (on the parse)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re

INERT_FT = ("inert",)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")


def _d(x):
    if x is None:
        return None
    return x.isoformat() if isinstance(x, dt.date) else str(x)


def norm_fact(f: dict) -> tuple:
    ft = f["ft"]
    if ft == "rule":
        return ("rule", f["rid"], f["vid"], int(f["rev"]), f.get("scope"), f["status"], _d(f.get("eff")),
                tuple(_d(x) for x in f["end"]), tuple((a["attr"], a["op"], a["val"]) for a in f["conds"]),
                f["join"], f["outcome"], f["form"], f.get("amends"))
    if ft == "effreg":
        return ("effreg", f["vid"], f["rid"], _d(f["eff"]))
    if ft == "void":
        return ("void", f["target"])
    if ft == "exc":
        return ("exc", f["eid"], f["rid"], tuple((a["attr"], a["op"], a["val"]) for a in f["conds"]), f["join"],
                f.get("scope"), f["status"], _d(f["eff"]), tuple(_d(x) for x in f["end"]))
    if ft == "case":
        return ("case", f.get("cid"), tuple(sorted((k, v if not isinstance(v, dict) else "T") for k, v in
                                                   f["attrs"].items())), f["scope"], _d(f["gdate"]))
    if ft == "inert":
        return ("inert", f["text"])
    if ft == "generic":
        return ("generic",) + tuple(f["key"])
    # S2-S6 fact kinds (f13_lc, f13_tab, f13_log): every key of the shared DATA schema, exact
    return (ft,) + tuple(sorted((k, json.dumps(v, sort_keys=True, default=str)) for k, v in f.items() if k != "ft"))


def norm_trace(t):
    if not t:
        return None
    return (t["label"], t["scope_label"])


def norm_section(s: dict) -> tuple:
    return (slug(s["heading"]), s.get("scope"), _d(s.get("mdate")), tuple(s.get("period") or ()),
            norm_trace(s.get("trace")),
            tuple(norm_fact(f) for f in s["facts"]) if not s.get("trace") else ())


def norm_query(q: dict) -> tuple:
    keys = ("qk", "form", "neg", "inner_neg", "case_ref", "unit", "date", "rid", "matter", "noun", "eid", "aid",
            "holder", "table", "period", "measure", "filt", "cfg", "site", "ent", "ent2", "op", "thr")
    out = [(k, _d(q.get(k)) if k == "date" else q.get(k)) for k in keys if q.get(k) not in (None, False, 0)]
    if q.get("form") in ("yn", "establish", "settle") and q.get("claim"):
        out.append(("claim", q["claim"].get("value")))
    if q.get("cases"):
        out.append(("cases", tuple(norm_fact({**c, "ft": "case"}) for c in q["cases"])))
    if q.get("case"):
        out.append(("case", norm_fact({**q["case"], "ft": "case"})))
    return tuple(out)


def full_canon(doc: dict) -> str:
    """Exact canonical document + query (G3 equality; headings slugged, inert text kept)."""
    return json.dumps({"title": slug(doc.get("title") or ""),
                       "sections": [norm_section(s) for s in doc["sections"]],
                       "query": norm_query(doc["query"])}, sort_keys=True, default=str)


# ------------------------------------------------------------------------------------------------ abstraction
_ID_RE = re.compile(r"^[A-Z]{1,4}-[0-9A-Z]{2,6}(?:\.\d+)?$")


class _Abs:
    def __init__(self, ref_date):
        self.m = {}
        self.ref = ref_date

    def tok(self, kind, v):
        if v is None:
            return None
        k = (kind, v)
        if k not in self.m:
            self.m[k] = f"{kind}{sum(1 for x in self.m if x[0] == kind)}"
        return self.m[k]

    def date(self, v):
        if v is None:
            return None
        try:
            return (dt.date.fromisoformat(str(v)) - self.ref).days
        except ValueError:
            return v

    def walk(self, x, key=None):
        if isinstance(x, (list, tuple)):
            return [self.walk(y) for y in x]
        if isinstance(x, str):
            if re.match(r"^\d{4}-\d{2}-\d{2}$", x):
                return self.date(x)
            if _ID_RE.match(x):
                return self.tok("ID", x)
            return self.tok("W", x)
        return x


def _ref_date(doc):
    q = doc["query"]
    if q.get("date"):
        return dt.date.fromisoformat(_d(q["date"]))
    for s in doc["sections"]:
        for f in s["facts"]:
            if f["ft"] == "case":
                return dt.date.fromisoformat(_d(f["gdate"]))
    c = q.get("case") or doc.get("case")
    if c:
        return dt.date.fromisoformat(_d(c["gdate"]))
    return dt.date(2000, 1, 1)


def _keep_word(w: str) -> bool:
    return w in ("in force", "draft", "proposed", "void", "all", "any", "ge", "le", "gt", "lt", "eq", "clause",
                 "amend", "none", "through", "repealed", "rule", "effreg", "exc", "case", "generic", "choice", "yn",
                 "establish", "settle", "inverted", "T")


def _abstract(obj, A: _Abs):
    if isinstance(obj, (list, tuple)):
        return [_abstract(y, A) for y in obj]
    if isinstance(obj, str):
        if _keep_word(obj) or obj.startswith(("q", "ag")) and "_" in obj:
            return obj
        return A.walk(obj)
    return obj


def structure_hash(doc: dict, roles: dict | None = None) -> str:
    """7.2 #6 canonical form: rule graph + facts + query; names abstracted (IDs, units, outcomes, attribute names, pack
    words -> role tokens by first appearance), dates as day offsets from the row date; inert facts and headings out."""
    A = _Abs(_ref_date(doc))
    q = _abstract(norm_query(doc["query"]), A)
    facts = []
    for s in doc["sections"]:
        if s.get("trace"):
            facts.append(["trace", A.walk(s["trace"]["scope_label"])])
            continue
        for f in s["facts"]:
            if f["ft"] in INERT_FT:
                continue
            facts.append(_abstract(norm_fact(f), A))
    blob = json.dumps({"q": q, "f": facts}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:60]


def g12_hash(doc: dict, decisive: list, near: list, world: str, card_keys: list) -> str:
    """Decisive + near-miss facts + query + world + card line set, names abstracted (G12 sidecar key)."""
    A = _Abs(_ref_date(doc))
    q = _abstract(norm_query(doc["query"]), A)
    pick = []
    for s in doc["sections"]:
        if s["sid"] in decisive or s["sid"] in near:
            tag = "D" if s["sid"] in decisive else "N"
            if s.get("trace"):
                pick.append([tag, "trace", A.walk(s["trace"]["scope_label"])])
            else:
                pick.append([tag] + [_abstract(norm_fact(f), A) for f in s["facts"] if f["ft"] not in INERT_FT])
    blob = json.dumps({"q": q, "s": pick, "w": world, "c": sorted(card_keys)}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:40]
