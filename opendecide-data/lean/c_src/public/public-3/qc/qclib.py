"""Shared helpers for the public-3 independent QC scripts (prep5/B4). Own code; reads the builder's wrap templates
(lib/pools.py *_STYLES) only to take the record text back out of a row's state. Never prints row text."""
import hashlib, json, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
P3 = HERE.parent
OUT = P3 / "out"
sys.path.insert(0, str(P3 / "lib"))
import pools as _P  # noqa: E402

MIXED = ("public3_rows_r1.jsonl", "public3_reserve.jsonl")
_NW = re.compile(r"[^\w]+")
TOK = re.compile(r"\w+")


def loose(s):
    s = unicodedata.normalize("NFKC", s or "").casefold()
    return _NW.sub(" ", s).replace("_", " ").strip()


def h(s):
    return hashlib.blake2b(s.encode("utf-8"), digest_size=8).digest()


def load(name):
    return [json.loads(l) for l in open(OUT / name, encoding="utf-8")]


def _rx(wrap):
    out = ""
    for p in re.split(r"(\{text\}|\{text_json\}|\{quoted\})", wrap):
        if p == "{text}":
            out += r"(?P<t>[\s\S]*)"
        elif p == "{text_json}":
            out += r"(?P<j>\"[\s\S]*\")"
        elif p == "{quoted}":
            out += r"(?P<q>> [\s\S]*)"
        else:
            out += re.escape(p.replace("{{", "{").replace("}}", "}"))
    return re.compile(out)


STYLES = {st["id"]: _rx(st["wrap"]) for pool in (_P.XED_STYLES, _P.MAMS_STYLES, _P.SAR_STYLES, _P.POST_STYLES)
          for st in pool}


def record_texts(r):
    """The human record text(s) a row shows: the state with its wrap template removed (when the row's format_style
    template matches), else the whole state; plus the options of choice rows whose options are records (several
    record ids; their state is then a framing, not a record).""" 
    out = []
    rx = STYLES.get(r["meta"].get("format_style"))
    m = rx.fullmatch(r["state"] or "") if rx else None
    if m and m.group(m.lastgroup) is not None:
        g = m.groupdict()
        if g.get("t") is not None:
            out.append(g["t"])
        elif g.get("j") is not None:
            try:
                out.append(json.loads(g["j"]))
            except ValueError:
                out.append(g["j"])
        elif g.get("q") is not None:
            out.append("\n".join(x[2:] if x.startswith("> ") else x for x in g["q"].split("\n")))
        matched = True
    uid = r["meta"].get("record_uid")
    multi = r["qtype"] == "choice" and isinstance(uid, list) and len(uid) > 1
    if not m or m.group(m.lastgroup) is None:
        matched = False
        if r["state"] and not multi:
            out.append(r["state"])
    if multi:
        out += list(r["options"])
    return [t for t in out if t and t.strip()], matched


def twin_key(r):
    return r["meta"].get("twin_of") or r["id"]
