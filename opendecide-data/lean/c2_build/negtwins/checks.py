"""negtwins/checks.py: single-predicate-change checker, card rule, twin rows and G-TW (A42-D 7.3, 7.5).

check_pair(base_core, twin_core, pattern, pair=None)
  An INDEPENDENT reader (it never calls core.rewrite and shares no code with it beyond the closed word tables): it
  lemmatises both cores, strips the pattern's frame, and reads the edit script with difflib. It returns
  (ok, problems, report) where report holds `predicate_changes` (clusters of edited non-auxiliary tokens, must be
  exactly what the operator declares), `layers` (negation layers added, counted from the token evidence) and
  `relation` (complement when the layers are odd). The declared relation of the pattern must equal the read one.

twin_row(...) builds the new row; labels are never set by hand: gold = 1 - base gold (complement) or the base gold.
g_tw(pairs): gold(Q) = not gold(not-Q) for complements, equal gold for equivalence twins, 100% or the gate fails.
"""
from __future__ import annotations

import difflib
import re
from collections import Counter

from . import core as C
from t37b import select as SEL  # noqa: E402

AUXL = {"do", "be", "have", "there"} | set(C.AUX_MOD)
_LEMMA = {"does": "do", "did": "do", "do": "do", "is": "be", "are": "be", "was": "be", "were": "be", "has": "have",
          "had": "have", "have": "have", "lacks": "lack", "lacked": "lack"}
for _b, (_s, _p) in C.VERB_FORMS.items():
    _LEMMA.setdefault(_s, _b)
    _LEMMA.setdefault(_p, _b)
_LEMMA["does"] = "do"
_LEMMA["did"] = "do"
LAYER_TOKENS = {"not", "fail", "lack"}
AUX_RAW = set(C.AUX_DO + C.AUX_COP + C.AUX_HAVE + C.AUX_MOD)


def _lemmas(text: str, extra: dict | None = None) -> list:
    out = []
    for t in C.tokens(text):
        t = (extra or {}).get(t, t)
        out.append(_LEMMA.get(t, t))
    return out


def _pair_lemmas(pair: dict | None) -> dict:
    """form -> base for both sides of a lexical pair, so 'omitted' and 'omit' read as one lemma."""
    m = {}
    for side in ("a", "b"):
        for k, v in (pair or {}).get(side, {}).items():
            if v and (pair or {}).get(side, {}).get("base"):
                m[v.lower()] = pair[side]["base"].lower()
    return m


_SITE_TOKEN = re.compile(r"[A-Za-z0-9_'\u2019\-]+|[^\sA-Za-z0-9_]")
_SITE_FUNCTION_WORDS = frozenset({"the", "a", "an", "of", "to", "in", "on", "at", "by", "for", "with", "from", "and", "or", "being", "that",
                                  "this", "these", "those", "its", "their", "his", "her", "any", "each", "every", "no", "than", "as"})
_BEING_AUX = re.compile(r"\bbeing\s+(is|are|was|were|has|have|had|does|do|did|can|could|will|would)\b", re.I)


def bad_edit_site(base_core: str, twin_core: str) -> bool:
    """A48 (h) (iv), found by the pooled audit (16 Oct 2026): an inserted or replaced word that lands right after a function word
    (the, of, to, a, ...) or after "being" cuts a noun phrase in two ("the stated distance to the is named place", "the action being
    is judged"): the subject boundary of the core was mis-parsed. Precision on the audit sample 9/9 flagged, 0/151 clean; a
    program refusal (the twin is dropped, never repaired). Edits at the very start of the core (frames) are not sites."""
    if _BEING_AUX.search(twin_core):
        return True
    a, b = _SITE_TOKEN.findall(base_core), _SITE_TOKEN.findall(twin_core)
    sm = difflib.SequenceMatcher(a=[x.lower() for x in a], b=[x.lower() for x in b], autojunk=False)
    for tag, _i1, _i2, j1, _j2 in sm.get_opcodes():
        if tag in ("insert", "replace") and j1 > 0 and b[j1 - 1].lower() in _SITE_FUNCTION_WORDS:
            return True
    return False


def check_pair(base_core: str, twin_core: str, p: C.Pattern, pair: dict | None = None) -> tuple:
    probs = []
    extra = _pair_lemmas(pair)
    lb, lt = _lemmas(base_core, extra), _lemmas(twin_core, extra)
    if p.frame:
        f = _lemmas(p.frame)
        if lt[:len(f)] != f:
            return False, [f"the twin does not start with the frame {p.frame!r}"], {}
        lt = lt[len(f):]
    if twin_core.count("?") != 1 or not twin_core.endswith("?") or "\n" in twin_core:
        probs.append("the twin is not one question on one line")
    cb, ct = Counter(lb), Counter(lt)
    add, rem = ct - cb, cb - ct
    ops = [o for o in difflib.SequenceMatcher(None, lb, lt, autojunk=False).get_opcodes() if o[0] != "equal"]
    layers = 0
    ex_add, ex_rem = Counter(), Counter()
    op = p.op
    if op == "FRAME_NOT":
        ex_add, layers = Counter({"not": 1}), 1
    elif op in ("NEG_FRAME", "POS_FRAME"):
        layers = 1 if op == "NEG_FRAME" else 0
    elif op == "FAIL_TO":
        ex_add, layers = Counter({"fail": 1, "to": 1}), 1
    elif op == "DNEG_FAIL":
        ex_add, layers = Counter({"not": 1, "fail": 1, "to": 1}), 2
    elif op == "LACK":
        ex_add, ex_rem, layers = Counter({"lack": 1}), Counter({p.verb: 1}), 1
    elif op in ("LEX_PAIR", "DNEG_PAIR") and pair:
        a, b = (_LEMMA.get(pair[k]["base"].lower(), pair[k]["base"].lower()) for k in ("a", "b"))
        if op == "LEX_PAIR":
            a, b = (a, b) if p.direction == "a>b" else (b, a)
            layers = 1
        else:
            layers, ex_add = 2, Counter({"not": 1})
        ex_add += Counter({b: 1})
        ex_rem = Counter({a: 1})
    else:
        probs.append(f"unknown operator {op}")
    # a wrapped (declarative) form may drop the do-auxiliary; every other token change must be the operator's
    allowed_rem = Counter({"do": 1}) if p.frame and op in ("NEG_FRAME", "POS_FRAME", "FAIL_TO", "LACK", "DNEG_FAIL") \
        else Counter()
    if add != ex_add:
        probs.append(f"tokens added {dict(add)} != the operator's {dict(ex_add)}")
    if (rem - allowed_rem) != ex_rem:
        probs.append(f"tokens removed {dict(rem)} != the operator's {dict(ex_rem)}")
    optoks = set(ex_add) | set(ex_rem)
    toks_of = lambda o: lb[o[1]:o[2]] + lt[o[3]:o[4]]          # noqa: E731
    aux_only = [o for o in ops if all(t in AUXL for t in toks_of(o))]
    op_ops = [o for o in ops if o not in aux_only and all(t in optoks | AUXL for t in toks_of(o))]
    unexplained = [o for o in ops if o not in aux_only and o not in op_ops]
    if unexplained:
        probs.append(f"edits outside the operator: {[toks_of(o) for o in unexplained][:3]}")
    clusters = []
    for o in sorted(op_ops, key=lambda o: (o[1], o[3])):
        if clusters and o[1] - clusters[-1][2] <= 0:
            clusters[-1] = (clusters[-1][0], min(clusters[-1][1], o[1]), max(clusters[-1][2], o[2]))
        else:
            clusters.append(("c", o[1], o[2]))
    want = 0 if op in ("NEG_FRAME", "POS_FRAME") else 1
    if len(clusters) != want:
        probs.append(f"{len(clusters)} predicate edit clusters; the operator declares {want}")
    # tense / number must survive: the raw auxiliaries (or, for a declarative do-question, the verb form) are unchanged
    q0 = C.parse(base_core)
    vforms = set(C.VERB_FORMS.get(q0.verb, ())) | {q0.verb} if q0 is not None and q0.cls == "DO" else set()
    rb = [t for t in C.tokens(base_core)[:1] + [x for x in C.tokens(base_core)[1:] if x not in vforms] if t in AUX_RAW]
    rt = [t for t in C.tokens(twin_core[len(p.frame):] if p.frame else twin_core) if t in AUX_RAW and t not in vforms]
    if Counter(rb) != Counter(rt):
        base_aux = rb[0] if rb else ""
        q = C.parse(base_core)
        okv = False
        if q is not None and q.cls == "DO" and Counter(rt) == Counter(rb) - Counter([base_aux]):
            carrier = {"FAIL_TO": "fail", "LACK": "lack"}.get(op, q.verb)
            f3, past = C.VERB_FORMS.get(carrier, ("lacks", "lacked") if carrier == "lack" else (None, None))
            want = {"does": f3, "did": past, "do": carrier}.get(base_aux)
            okv = bool(want) and want in C.tokens(twin_core) and not (base_aux == "did" and f3 in C.tokens(twin_core))
        if not okv:
            probs.append(f"tense or number changed: auxiliaries {rb} -> {rt}")
    if op == "FRAME_NOT":
        i = [k for k, t in enumerate(lt) if t == "not"]
        if len(i) != 1 or i[0] == 0 or lt[i[0] - 1] not in AUXL:
            probs.append("'not' does not directly follow the auxiliary")
    if op in ("FAIL_TO", "DNEG_FAIL") and not any(lt[k] == "fail" and lt[k + 1] == "to" for k in range(len(lt) - 1)):
        probs.append("no 'fail to' in the twin")
    changes = len(clusters)
    relation = "complement" if layers % 2 else "equiv"
    if relation != p.relation:
        probs.append(f"token evidence reads {relation}; the pattern declares {p.relation}")
    return (not probs), probs, {"layers": layers, "relation": relation, "clusters": changes,
                                "added": dict(add), "removed": dict(rem)}


# ------------------------------------------------------------------------------------------------ card rule

_YES_ONLY = re.compile(r"- yes: ([^\n]+)")
_ANSWER_LEAD = re.compile(r"^(?:yes|no)[,:]?\s+(?:if|when|only if)\s+", re.I)


def one_sided_body(card: str):
    """The condition of a yes-only card ('- yes: Yes if the text asks ...' -> 'the text asks ...'), else None."""
    m = _YES_ONLY.fullmatch((card or "").strip())
    if not m:
        return None
    body = _ANSWER_LEAD.sub("", m.group(1).strip()).rstrip(". ")
    return body or None


def twin_card(card: str, relation: str):
    """The twin's card: kept for equiv; for a complement the definitions are exchanged (two-line card, only when neither
    names an answer word, T37b swap rule) or, for a yes-only card (G-block wave 1), built by one outer negation:
        - yes: It is not the case that <condition>.      - no: <condition>.
    which is exact by construction (the base's no is the condition failing). None = no complement card exists."""
    if relation == "equiv" or not (card or "").strip():       # a card-free base keeps no card: nothing to swap or wrap
        return card
    d = SEL.parse_card(card)
    if d is not None:
        return f"- yes: {d[1]}\n- no: {d[0]}" if SEL.swap_safe(d) else None
    body = one_sided_body(card)
    if body is None or SEL.ANSWER_WORD.search(body):
        return None
    if re.search(r"\byes\b", body, re.I) or re.match(r"(?:pick|choose|select|answer|mark|reply)\b", body, re.I):
        return None                   # an answer directive ("Pick yes when ...", "Yes means ..."), not a condition: no wrap
    if C.has_negation(body):          # Ruling A48 (c): the wrap is admitted only when <condition> has no negation cue (negcount 0)
        return None
    return f"- yes: It is not the case that {body}.\n- no: {body[0].upper() + body[1:]}."


def twin_row(base: dict, pre: str, twin_core: str, p: C.Pattern, *, seed: int = 20261013, block: str = "gblock") -> dict:
    if p.held_out or p.source == "heldout" or str(p.pid).startswith("H:"):        # A42-D 7.4: held-out patterns never train
        raise ValueError(f"held-out pattern {p.pid} cannot make a training row")
    card = twin_card(base["card"], p.relation)
    if card is None and (base.get("card") or "").strip():
        raise ValueError("base card cannot be swapped")
    gold = 1 - base["gold"] if p.relation == "complement" else base["gold"]
    tid = f"negtwin:{block}:{C.sha(base['id'] + '|' + p.pid + '|' + twin_core)[:16]}"
    bm = dict(base.get("meta") or {})
    return {"id": tid, "group_id": base.get("group_id"), "call_id": base.get("call_id"), "source": base.get("source", block),
            "state": base["state"], "qtype": "noul", "instructions": pre + twin_core, "options": None, "gold": gold,
            "role": p.relation, "card": card,
            "meta": {**bm, "twin_of": base["id"], "twin_kind": p.relation, "negtwin":
                     {"pattern": p.pid, "op": p.op, "kind": p.kind, "frame": p.frame, "cls": p.cls, "block": block,
                      "base_id": base["id"], "base_gold": base["gold"], "seed": seed}}}


def relation_edge(row: dict) -> dict:
    return {"a": row["meta"]["negtwin"]["base_id"], "b": row["id"], "type": row["role"]}


# ------------------------------------------------------------------------------------------------ G-TW

def g_tw(pairs: list) -> dict:
    """pairs: [(base_row, twin_row)]. 100% or the gate fails (A42-D 7.3)."""
    bad = []
    by_base: dict = {}
    for b, t in pairs:
        n = (t.get("meta") or {}).get("negtwin") or {}
        rel = t.get("role")
        want = 1 - b["gold"] if rel == "complement" else b["gold"] if rel == "equiv" else None
        pre_b, core_b = C.split_instruction(b["instructions"]) or ("", "")
        pre_t, core_t = C.split_instruction(t["instructions"]) or ("", "")
        probs = []
        if want is None or t["gold"] != want:
            probs.append(f"gold {t['gold']} != {want} for role {rel}")
        if n.get("base_id") != b["id"] or t["meta"].get("twin_of") != b["id"]:
            probs.append("twin does not name its base")
        if pre_b != pre_t or not core_b or b["state"] != t["state"]:
            probs.append("preamble or state differs from the base")
        if t["card"] != twin_card(b["card"], rel if rel in ("equiv", "complement") else "equiv"):
            probs.append("card is not the base card (equiv) or its exchange / negation wrap (complement)")
        if probs:
            bad.append({"base": b["id"], "twin": t["id"], "problems": probs})
        by_base.setdefault(b["id"], []).append((rel, t["gold"]))
    for bid, lst in by_base.items():
        for r in ("complement", "equiv"):
            if len({g for rr, g in lst if rr == r}) > 1:
                bad.append({"base": bid, "problems": [f"twins of role {r} disagree on gold"]})
    return {"n_pairs": len(pairs), "violations": len(bad), "pass": not bad, "examples": bad[:10]}
