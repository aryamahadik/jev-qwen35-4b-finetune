"""Shared loaders for the independent COMMIT QC checker (check:COMMIT, c-lanes-v3). Imports nothing from
c_src/COMMIT/gen or c_src/COMMIT/solverB. Prints counts only, never row text."""
import hashlib, json, math, re, string, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
FAM = LEAN / "c_src/COMMIT"
OUT = FAM / "out"
QC = FAM / "qc"
TMP = FAM / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)


def load(name):
    rows = [json.loads(l) for l in open(OUT / f"{name}.jsonl")]
    side = {}
    p = OUT / f"{name}.sidecar.jsonl"
    if p.exists():
        for l in open(p):
            s = json.loads(l); side[s["id"]] = s
    return rows, side


def load_rel(name):
    p = OUT / f"{name}.rel.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() and p.stat().st_size else []


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def dio():
    if str(LEAN) not in sys.path:
        sys.path.insert(0, str(LEAN))
    import decoder_io as d
    d.STYLE, d.LAYOUT = "cygnet", "schema_branch_mark"
    if len(d.WIDE) < 100:
        U = string.ascii_uppercase
        d.WIDE = list(U) + [a + b for a in U for b in U]
    return d


def model_view(r, perm=None):
    """Exactly what the model sees: decoder_io.user_msg under cygnet + schema_branch_mark."""
    return dio().user_msg(r, perm)


def is_yn(r):
    return r["qtype"] == "noul"


def gold_index(r):
    return r["options"].index(r["gold"])


def gold_letter(r):
    d = dio()
    if is_yn(r):
        return "A" if r["gold"] == 1 else "B"
    return d.label(gold_index(r))


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-12" if k <= 12 else "13+"


def ctype(r, side):
    return (side.get(r["id"]) or {}).get("commit_type", "?")


def view(r):
    return r["meta"].get("input_view", "?")


# ---------------------------------------------------------------- visible-text helpers (checker's own parsing)
NUM_RX = re.compile(r"\d+(?:\.\d+)?")


def split_q(ins):
    """question paragraph = last paragraph of `instructions` holding '?'; rest = the other paragraphs."""
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi], "\n\n".join(paras[:qi] + paras[qi + 1:])


def opt_defs(r):
    return dio().card_defs(r.get("card"))


def shown_opts(r):
    """option lines as decoder_io prints them in the schema (option text + ': ' + card definition when defined)."""
    if is_yn(r):
        return ["Yes", "No"]
    d = opt_defs(r)
    return [f"{o}: {d[o]}" if o in d else o for o in r["options"]]


def visible_card(r):
    """card-side text the model sees, minus the question: yes/no rows print the card whole; choice rows print only
    the option definition lines (A16.1 g) - those are in the option lines, so only `instructions` minus question."""
    q, rest = split_q(r["instructions"])
    if is_yn(r):
        return ((r.get("card") or "") + "\n\n" + rest).strip()
    return rest


def views(r):
    q, rest = split_q(r["instructions"])
    return {"q": q, "cardnoq": visible_card(r), "state": r["state"], "opts": shown_opts(r)}


DIFF_START = re.compile(r"^(```diff|~{4,}|@@|diff --git|\+\+\+ |--- )")


def message_of(state):
    """the commit message part of `state` (everything before the first diff/stat block line)."""
    out = []
    for ln in state.split("\n"):
        if DIFF_START.match(ln) or re.match(r"^\s*\d+\s+\d+\s+\S", ln) or ln.strip().lower().startswith(("```stat", "numstat")):
            break
        out.append(ln)
    return "\n".join(out)


def diff_stats(state):
    ls = state.split("\n")
    plus = sum(1 for l in ls if l.startswith("+") and not l.startswith("+++"))
    minus = sum(1 for l in ls if l.startswith("-") and not l.startswith("---"))
    seps = sum(1 for l in ls if re.match(r"^(~{4,}|diff --git|\+\+\+ )", l))
    hunks = sum(1 for l in ls if l.startswith("@@"))
    numstat = sum(1 for l in ls if re.match(r"^\s*(\d+|-)\s+(\d+|-)\s+\S", l))
    cut = sum(1 for l in ls if re.search(r"(?i)lines? (left out|omitted|cut)", l))
    return {"plus": plus, "minus": minus, "file_seps": seps, "hunks": hunks, "numstat_lines": numstat, "cut_marks": cut,
            "lines": len(ls)}


def word_hit(name, text):
    """name hit: a word of the name equals a message word or word part (case aside, one final s ignored)."""
    toks = [t for t in re.split(r"[^a-z0-9]+", name.lower()) if len(t) >= 3]
    if not toks:
        return False
    words = set()
    for w in re.findall(r"[A-Za-z0-9]+", text):
        for part in re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", w) + [w]:
            p = part.lower()
            words.add(p); words.add(p[:-1] if p.endswith("s") else p)
    return any(t in words or (t[:-1] if t.endswith("s") else t) in words for t in toks)


def first_hit_pos(name, text):
    toks = [t for t in re.split(r"[^a-z0-9]+", name.lower()) if len(t) >= 3]
    best = None
    tl = text.lower()
    for t in toks:
        for v in {t, t[:-1] if t.endswith("s") else t}:
            m = re.search(r"(?<![a-z0-9])" + re.escape(v) + r"s?(?![a-z0-9])", tl)
            if m and (best is None or m.start() < best):
                best = m.start()
    return best


# visible metadata only (FIX RULE "G6 metadata = only what the model sees"), plus the design fields the spec lists for
# G6 (d) (sampler id, template / wording id, repo, language, source, view, M hits, diff length, files changed).
# Label-derived or hidden sidecar fields (gold_*, describes, msg_record, deciding, case_records, hold, level,
# yes_rate_drawn, twin_flag, rule_id, rubric_id, extra_records, group) are never used.
SIDE_CAT = ("commit_type", "repo_group", "language", "card_form", "polarity", "qid", "frame")  # card_variant excluded: match negatives carry the source record id
SIDE_NUM = ("k_syn", "counted_tokens")


def meta_feats(r, s=None):
    m = r["meta"]; s = s or {}
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style", "sampler", "input_view")}
    cat["depth"] = str(m.get("depth")); cat["deep"] = str(m.get("deep"))
    cat["source"] = str((m.get("text_source") or {}).get("dataset"))
    cat["edge"] = ",".join(sorted(map(str, m.get("edge") or [])))
    for k in SIDE_CAT:
        if k in s:
            v = s.get(k)
            cat["sc_" + k] = json.dumps(v, sort_keys=True) if isinstance(v, (list, dict)) else str(v)
    ds = diff_stats(r["state"]); msg = message_of(r["state"])
    num = {"len_state": float(len(r["state"])), "len_ins": float(len(r["instructions"])),
           "len_card": float(len(r.get("card") or "")), "len_msg": float(len(msg)),
           "k_opts": float(len(r["options"]) if not is_yn(r) else 2),
           "n_trigger": float(len(m.get("trigger_entities") or [])) if m.get("trigger_entities") is not None else -1.0}
    num.update({"d_" + k: float(v) for k, v in ds.items()})
    for k in SIDE_NUM:
        x = s.get(k)
        num["sc_" + k] = float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else -1.0
    nums = [float(x) for x in NUM_RX.findall(msg)][:30]
    num["msg_n_numbers"] = float(len(nums)); num["msg_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    if not is_yn(r):
        L = [len(o) for o in shown_opts(r)]
        num["opt_len_mean"] = float(sum(L) / len(L)); num["opt_len_max"] = float(max(L))
    return cat, num
