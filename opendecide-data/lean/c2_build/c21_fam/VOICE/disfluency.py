"""Rule-based disfluency (no LLM): fillers, repeats, false starts, self-repairs, dropped politeness.
Operates on a SpokenDoc and keeps the segment map and the decision-span token ranges consistent. Never inserts inside a
decision span and never touches a span token. The table is closed and hashed (Haiku medium authors the real one; TEST table here)."""
import copy

from vcommon import DISFLUENCY_RATE, FILLERS, VoiceError

TEST_TABLE = {"version": "test-only", "fillers": ["um", "uh", "er"], "politeness": ["please"], "repair_words": ["no"],
              "false_start_max": 2, "rate": DISFLUENCY_RATE}


def _protected(doc):
    prot = set()
    for sp in doc["spans"]:
        prot |= set(range(sp["tok"][0], sp["tok"][1]))
    return prot


def _shift(doc, at, n):
    """Insert n token slots at position `at`: shift segments and spans that start at or after `at`."""
    for seg in doc["segments"]:
        a, b = seg["tok"]
        if a >= at:
            seg["tok"] = [a + n, b + n]
        elif b > at:                              # insertion inside a segment: only legal for non-protected callers
            raise VoiceError("insertion inside a segment")
    for sp in doc["spans"]:
        a, b = sp["tok"]
        if a >= at:
            sp["tok"] = [a + n, b + n]
        elif b > at:
            raise VoiceError("insertion inside a span")


def _boundaries(doc):
    """Token positions where an insertion keeps every segment whole and is outside every span."""
    seg_starts = {s["tok"][0] for s in doc["segments"]} | {len(doc["tokens"])}
    prot = _protected(doc)
    return [p for p in sorted(seg_starts) if p not in prot or p == 0 and False]


def _span_interior(doc):
    inside = set()
    for sp in doc["spans"]:
        inside |= set(range(sp["tok"][0] + 1, sp["tok"][1]))
    return inside


def apply_disfluency(doc, table, rng, rate=None):
    """Returns (new_doc, list of applied ops). With probability `rate` the doc gets 1-2 operations."""
    rate = table.get("rate", DISFLUENCY_RATE) if rate is None else rate
    d = copy.deepcopy(doc)
    ops = []
    if rng.random() >= rate:
        return d, ops
    for _ in range(rng.choice([1, 1, 2])):
        kind = rng.choice(["filler", "repeat", "false_start", "self_repair", "drop_politeness"])
        interior = _span_interior(d)
        bounds = [p for p in sorted({s["tok"][0] for s in d["segments"]} | {len(d["tokens"])}) if p not in interior]
        # an insertion at a span start would land between preceding text and the span: allowed (outside the span)
        if kind == "filler" and bounds:
            at = rng.choice(bounds)
            w = rng.choice(table["fillers"])
            _shift(d, at, 1)
            d["tokens"].insert(at, w)
            d["segments"].append({"kind": "disfl", "tok": [at, at + 1], "src": None, "style": "filler"})
            ops.append(("filler", at, w))
        elif kind == "repeat":
            cand = [s for s in d["segments"] if s["kind"] == "word" and s["src"] is not None and not any(sp["tok"][0] <= s["tok"][0] < sp["tok"][1] for sp in d["spans"])]
            if cand:
                s = rng.choice(cand)
                a, b = s["tok"]
                w = d["tokens"][a:b]
                _shift(d, b, len(w))
                d["tokens"][b:b] = w
                d["segments"].append({"kind": "disfl", "tok": [b, b + len(w)], "src": None, "style": "repeat"})
                ops.append(("repeat", b, " ".join(w)))
        elif kind == "false_start":
            first = [s for s in d["segments"] if s["kind"] == "word" and s["tok"][0] == 0]
            if first and not any(sp["tok"][0] == 0 for sp in d["spans"]):
                k = min(table.get("false_start_max", 2), len(d["segments"]))
                end = 0
                n_ok = 0
                for s in sorted(d["segments"], key=lambda x: x["tok"][0]):
                    if s["tok"][0] == end and s["kind"] == "word" and n_ok < k and not any(sp["tok"][0] <= s["tok"][0] < sp["tok"][1] for sp in d["spans"]):
                        end = s["tok"][1]
                        n_ok += 1
                    else:
                        break
                if n_ok:
                    w = d["tokens"][0:end]
                    _shift(d, 0, len(w))
                    d["tokens"][0:0] = w
                    d["segments"].append({"kind": "disfl", "tok": [0, len(w)], "src": None, "style": "false_start"})
                    ops.append(("false_start", 0, " ".join(w)))
        elif kind == "self_repair":
            cand = [s for s in d["segments"] if s["kind"] == "word" and s["src"] is not None and not any(sp["tok"][0] <= s["tok"][0] < sp["tok"][1] for sp in d["spans"])]
            if cand:
                s = rng.choice(cand)
                a, b = s["tok"]
                w = d["tokens"][a:b]
                ins = w + [rng.choice(table["repair_words"])]
                _shift(d, b, len(ins))
                d["tokens"][b:b] = ins
                d["segments"].append({"kind": "disfl", "tok": [b, b + len(ins)], "src": None, "style": "self_repair"})
                ops.append(("self_repair", b, " ".join(ins)))
        elif kind == "drop_politeness":
            pol = set(table.get("politeness", []))
            for s in sorted(d["segments"], key=lambda x: -x["tok"][0]):
                if s["kind"] == "word" and d["tokens"][s["tok"][0]] in pol and not any(sp["tok"][0] <= s["tok"][0] < sp["tok"][1] for sp in d["spans"]):
                    a, b = s["tok"]
                    del d["tokens"][a:b]
                    d["segments"].remove(s)
                    n = b - a
                    for t in d["segments"]:
                        if t["tok"][0] >= b:
                            t["tok"] = [t["tok"][0] - n, t["tok"][1] - n]
                    for sp in d["spans"]:
                        if sp["tok"][0] >= b:
                            sp["tok"] = [sp["tok"][0] - n, sp["tok"][1] - n]
                    ops.append(("drop_politeness", a, d["source_tokens"][s["src"]] if s["src"] is not None else ""))
                    d["dropped_src"] = d.get("dropped_src", []) + [s["src"]]
                    break
    d["tts_text"] = " ".join(d["tokens"])
    d["disfluency"] = ops
    return d, ops
