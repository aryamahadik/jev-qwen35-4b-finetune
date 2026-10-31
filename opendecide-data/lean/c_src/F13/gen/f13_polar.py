"""F13 per-row polarity (G0 10 "Yes = bad", F13R1-27 / F13R2-17, XF04; sidecar `polarity`). Repair r6.

polarity(row) in {adverse, favourable, neutral}, yes/no rows only (None on choice rows):
(1) template class (step 5 tag): slot-polar = the yes answer asserts that the slotted outcome, state, holder or
    criterion holds (qp_outcome, qr_decision, lg_status, tp_outcome, qr_holder, tq_crit); neutral = comparison of two
    records or a ranking (tq_cmp, tq_argmax) and version-in-force predicates (lg_version, qr_version);
(2) slot-polar rows take the adverse flag of the slotted value: the pack's own flag where the pack carries one
    (packs-2 outcome sets: `adverse`; packs-3 measure `direction`), else the build's flag for that pack value: the G0 10
    adverse list (sanction, denial, referral, active hold or condition, open action item, failing a criterion) by
    lexicon, favourable by lexicon, else a fixed per-(pack, value) hash draw (never per row). Holder claims (an action
    item held: "open action item") are adverse. A criterion claim "<E> has <measure> of <op> <T>" is adverse when it
    puts E on the bad side of the measure (high side of a high-is-bad measure, low side of a low-is-bad one);
(3) flipped once per negation in the polarity scope (SEM-45): yn neg 1 / 2 = 1 / 2 flips; establish / settle: inner
    negation + frame negation ("fail to"), so double negation restores it. Neutral stays neutral.
Audit-only: never rendered, never a G6 input beyond the listed metadata feature."""
from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache

import f13_base as B

SLOT_VALUE = ("qp_outcome", "qr_decision", "lg_status", "tp_outcome")
NEUTRAL = ("tq_cmp", "tq_argmax", "lg_version", "qr_version", "ag2_version", "ag2_config", "ag2_decision")
ADV_RE = re.compile(
    r"\b(?:den(?:y|ied|ial)|reject|refus|refer|escalat|hold|held|suspen|revok|revoc|sanction|fine[sd]?\b|penal|terminat"
    r"|cancel|withh[oe]ld|return|declin|block|ban(?:ned)?\b|halt|stop|remov|expel|evict|flag|audit|investigat|warn"
    r"|restrict|condition|probation|fail|overdue|laps|expir|void|freez|frozen|quarantin|recall|disqualif|exclu|downgrad"
    r"|demot|dismiss|write.?off|seiz|impound|lock|reprimand|caution|breach|violat|non.?complian|arrears|unpaid|delay"
    r"|defer|postpon|skip|deduct|clos|shut|ground|barred|forfeit|rework|redo|retest|re-?inspect|remedia|correct"
    r"|deficien|insufficient|incomplete|send (?:to|back)|hand (?:to|off|over)|pass to|forward|transfer|board|review)",
    re.I)
FAV_RE = re.compile(
    r"\b(?:approv|grant|renew|accept|admit|allow|clear|pass|permit|issu|award|releas|restor|reinstat|certif|confirm"
    r"|enrol|register|pay|paid|credit|keep|continu|proceed|waiv|eligib|qualif|complet|resolv|sign.?off|authori|fund"
    r"|accredit|licen|post|count toward|retain|extend|upgrad|promot|hire|launch|open|publish|book|schedul|go ahead"
    r"|spray|widen|now)", re.I)


def _h(*key) -> float:
    return int(hashlib.sha256("|".join(map(str, ("f13-polarity",) + key)).encode()).hexdigest()[:12], 16) / 16 ** 12


@lru_cache(maxsize=1)
def _pack_flags() -> dict:
    """pack_id -> {"out": {value: bool adverse}, "dir": {measure: 'high' | 'low'}} from the packs' own fields."""
    out = {}
    for rel in ("packs-3/packs-3.jsonl", "packs-1/packs.jsonl", "packs-2/packs.jsonl"):
        for line in open(B.PACKS / rel):
            p = json.loads(line)
            fl = {"out": {}, "dir": {}}
            for s in p.get("outcome_sets") or []:
                for o in (s.get("outcomes") if isinstance(s, dict) else s) or []:
                    if isinstance(o, dict) and isinstance(o.get("adverse"), bool) and isinstance(o.get("name"), str):
                        fl["out"][o["name"].strip().lower()] = o["adverse"]
            for e in p.get("entity_types") or []:
                for f in e.get("fields") or []:
                    d = (f.get("direction") or "").lower()
                    if isinstance(f.get("name"), str) and d in ("high is bad", "low is bad"):
                        fl["dir"][f["name"].replace("_", " ")] = "high" if d.startswith("high") else "low"
            out[p.get("id")] = fl
    return out


def value_flag(pack_id: str, value: str) -> bool:
    """True = adverse. Pack flag, else the G0 10 adverse list / favourable lexicon, else a fixed hash draw."""
    v = (value or "").strip().lower()
    fl = _pack_flags().get(pack_id, {}).get("out", {})
    if v in fl:
        return fl[v]
    if ADV_RE.search(v):
        return True
    if FAV_RE.search(v):
        return False
    return _h(pack_id, "value", v) < 0.5


def bad_side(pack_id: str, measure: str) -> str:
    d = _pack_flags().get(pack_id, {}).get("dir", {}).get(measure)
    return d or ("high" if _h(pack_id, "measure", measure) < 0.5 else "low")


def inner_polarity(card: dict, q: dict) -> str:
    qk = q["qk"]
    if qk in NEUTRAL or qk not in SLOT_VALUE + ("qr_holder", "tq_crit"):
        return "neutral"
    if qk == "qr_holder":
        return "adverse"
    if qk == "tq_crit":
        side = "high" if q.get("op") in ("ge", "gt") else "low"
        return "adverse" if side == bad_side(card["pack_id"], q["measure"]) else "favourable"
    return "adverse" if value_flag(card["pack_id"], q["claim"]["value"]) else "favourable"


def flips(q: dict) -> int:
    if q["form"] == "yn":
        return int(q.get("neg", 0))
    return int(bool(q.get("inner_neg"))) + int(q.get("neg", 0)) % 2


def row_polarity(doc: dict) -> str | None:
    q = doc["query"]
    if q.get("form") not in ("yn", "establish", "settle"):
        return None
    p = inner_polarity(doc["card"], q)
    if p == "neutral" or flips(q) % 2 == 0:
        return p
    return "favourable" if p == "adverse" else "adverse"
