"""c2_kit/g3h.py: G3-H, the LLM round trip for free-form (Mode F) text (C2_DATA_SPEC 6.3; also T32 and T33 claims).

An independent Haiku extractor reads the filled free-form text and returns the structured facts named by a field
schema. The program compares them with the generator's facts (plugin.extract_view). Bars: a mismatched row is always
dropped; a template (skin) whose rows match < 98% is quarantined (all its rows dropped).

The extractor sees only the text and the schema (field names, types, short descriptions, closed choices): never the
question, the options, the gold or the generator's values (extraction_item() checks the schema holds no value).

Field kinds and how answers are normalised before the exact comparison:
  date / datetime / cents / count / category  slots.parse (any form of the kind; a category may also be given by its
                                              key); numbers given as JSON numbers are refused for cents (ambiguous
                                              scale) and accepted for counts when integral
  id / name / glob / url / str                exact string after trimming outer whitespace
  bool                                        true / false (also "yes" / "no")
  enum                                        one of the field's choices, exact text
  list:<kind>                                 a list, compared in order (or as a multiset with ordered=False)
"""
from __future__ import annotations

from dataclasses import dataclass

from . import slots as S

PASS_RATE = 0.98
SCALAR = ("date", "datetime", "cents", "count", "category", "id", "name", "glob", "url", "str", "bool", "enum")


@dataclass(frozen=True)
class Field:
    name: str
    kind: str                  # one of SCALAR or "list:<scalar>"
    describe: str = ""
    params: tuple = ()         # slot params (currency, unit, category surfaces)
    choices: tuple = ()        # enum choices
    ordered: bool = True       # lists

    @property
    def base(self) -> str:
        return self.kind.split(":", 1)[1] if self.kind.startswith("list:") else self.kind


class Mismatch(ValueError):
    pass


def extraction_item(text: str, fields: list) -> dict:
    """The gold-free item for one text: {"text", "schema": [...]}. Category choices are surfaces, never keys."""
    sch = []
    for f in fields:
        if f.base not in SCALAR:
            raise ValueError(f"field {f.name}: kind {f.kind}")
        d = {"field": f.name, "type": f.kind, "describe": f.describe}
        if f.base == "enum":
            d["choices"] = list(f.choices)
        if f.base == "category":
            d["choices"] = sorted({s for _, ss in dict(f.params).get("surfaces", ()) for s in ss})
        sch.append(d)
    return {"text": text, "schema": sch}


def _norm_scalar(f: Field, raw):
    k = f.base
    if raw is None:
        return None
    if k == "bool":
        if isinstance(raw, bool):
            return raw
        s = str(raw).strip().lower()
        if s in ("true", "yes"):
            return True
        if s in ("false", "no"):
            return False
        raise Mismatch(f"{f.name}: not a boolean {raw!r}")
    if k == "enum":
        if raw not in f.choices:
            raise Mismatch(f"{f.name}: {raw!r} not in choices")
        return raw
    if k in ("id", "name", "glob", "url", "str"):
        if not isinstance(raw, str):
            raise Mismatch(f"{f.name}: expected text")
        return raw.strip()
    if k == "count" and isinstance(raw, int) and not isinstance(raw, bool):
        return raw
    if k == "count" and isinstance(raw, float) and raw.is_integer():
        return int(raw)
    if not isinstance(raw, str):
        raise Mismatch(f"{f.name}: expected the value as written (text), got {type(raw).__name__}")
    txt = raw.strip()
    if k == "category":
        keys = [kk for kk, _ in dict(f.params).get("surfaces", ())]
        if txt in keys:
            return txt
    try:
        return S.canonical(S.Slot(k, S.parse(k, txt, f.params)))
    except S.SlotError as e:
        raise Mismatch(f"{f.name}: {e}") from None


def normalize(f: Field, raw):
    if f.kind.startswith("list:"):
        if not isinstance(raw, list):
            raise Mismatch(f"{f.name}: expected a list")
        vals = [_norm_scalar(f, x) for x in raw]
        return vals if f.ordered else sorted(vals, key=repr)
    return _norm_scalar(f, raw)


def compare(expected: dict, extracted: dict, fields: list) -> tuple:
    """(ok, diffs). expected: canonical values (plugin.extract_view); extracted: the extractor's raw answer."""
    diffs = []
    if not isinstance(extracted, dict):
        return False, ["extraction is not an object"]
    for f in fields:
        want = expected.get(f.name)
        if f.kind.startswith("list:") and not f.ordered and isinstance(want, list):
            want = sorted(want, key=repr)
        try:
            got = normalize(f, extracted.get(f.name))
        except Mismatch as e:
            diffs.append(str(e))
            continue
        if got != want:
            diffs.append(f"{f.name}: extracted {got!r}, generator {want!r}")
    extra = set(extracted) - {f.name for f in fields}
    if extra:
        diffs.append(f"unexpected fields {sorted(extra)}")
    return not diffs, diffs


def template_report(results: list) -> dict:
    """results: [(template_id, row_id, ok)]. Per template pass rate; < 98% quarantines it; mismatches always drop."""
    per: dict = {}
    for tid, rid, ok in results:
        d = per.setdefault(tid, {"n": 0, "ok": 0})
        d["n"] += 1
        d["ok"] += bool(ok)
    for d in per.values():
        d["rate"] = d["ok"] / d["n"]
        d["quarantined"] = d["rate"] < PASS_RATE
    quarantined = sorted(t for t, d in per.items() if d["quarantined"])
    drop = sorted({rid for tid, rid, ok in results if not ok or tid in quarantined})
    return {"gate": "G3-H", "bar": PASS_RATE, "templates": per, "quarantined": quarantined, "drop_rows": drop,
            "all_templates_pass": not quarantined}
