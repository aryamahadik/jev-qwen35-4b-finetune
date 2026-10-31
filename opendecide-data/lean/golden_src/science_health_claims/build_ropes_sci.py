"""Build raw rows for ropes_sci (ROPES: Reasoning Over Paragraph Effects in Situations; Lin, Tafjord, Clark & Gardner,
MRQA 2019) as yes/no verification of a proposed answer.

Source : HF allenai/ropes pinned to revision d59f1e2ee2b423d7c6ba71edd47fceb4158b07dd,
         plain_text/train-00000-of-00001.parquet ONLY (validation/test never downloaded).
Licence: CC BY 4.0 (dataset card of allenai/ropes, the authors' org: 'license: cc-by-4.0', 'Licensing Information:
         The data is distributed under the CC BY 4.0 license').
Texts  : background passages (science textbooks and Wikipedia; physical science, life science incl. health) with a
         crowd-written situation and question; the answer is a crowd-written span. Human-written.
Framing: ROPES questions compare two entities or two directions ("Will cell X have a larger or smaller surface
         area?", "Which county polluted more rivers?"). We keep a question only when its single wrong alternative is
         certain: (a) the question itself offers the two alternatives ("more or less", "..., A or B?") and the
         answer is exactly one of them; or (b) the answer is an entity from the situation that has exactly ONE
         parallel entity there (same head word or same following word, e.g. 'Hill village'/'Low village', 'team
         Alpha'/'team Beta', 'Ben'/'Dan' in 'Ben ... while Dan ...'), differing in a capitalised / letter / number
         token. The proposed answer is the gold answer (yes) or that alternative (no), seeded 50/50.
         One question per situation (situations never repeat, so states are unique).
Review fix (strict reviewer, 29 Sep): the first build's regex took everything after the first comma as one side
         ('reaction B, will occur at a faster rate', 'would species C population increase') and split 'X or not X'
         / 'more fur or less fur' / 'the ones from the Ozarks, or the ones from the Rockies' wrongly, giving
         proposals such as 'not', 'the', 'fur'; the situation rule also accepted sentence-initial words ('This week
         Jim' -> 'This', 'What', 'Both', '2'). Alternatives now come from a token-level alignment around 'or'
         (determiner / shared prefix / shared suffix / 'not X' handled; the other side must be a parallel content
         phrase ending at a phrase boundary unless the pair is a known antonym pair), and situation candidates that
         are function words, sentence-initial words or a number against a name are rejected. Questions that do not
         align cleanly are not used.
Question: "Based on the background and the situation, is the proposed answer correct?"
Dedupe : exact / near-duplicate states; decontamination (label-NLI incl. quarel, local train/dev/eval, JevBench
         public) and a cross-check against other v14 golden parts.
Key    : 'ropes_sci' so it never collides with a possible 'ropes' part of another family.
Deterministic (seed 20261121). CPU only.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "ropes_sci"
SEED = 20261121
REV = "d59f1e2ee2b423d7c6ba71edd47fceb4158b07dd"
URL = f"https://huggingface.co/datasets/allenai/ropes/resolve/{REV}/"
FILES = {"plain_text/train-00000-of-00001.parquet": "5dd4781f69556326f366989e1e5df6603b43269388d5c2e22e0a7229c08df687",
         "README.md": "1aecbb6621fdedcf3cf5d899f838012f32a8cdc588a7b2f4dcf5fcb476abc3b5"}
LICENCE = (f"CC BY 4.0 (dataset card https://huggingface.co/datasets/allenai/ropes/blob/{REV}/README.md: 'The data is "
           "distributed under the CC BY 4.0 license')")
DATASET = "allenai/ropes (ROPES)"
QUESTION = "Based on the background and the situation, is the proposed answer correct?"
DEFS = {
    "yes": "Applying the cause-and-effect relationships stated in the background to the facts of the situation leads "
           "to the proposed answer (the right entity, or the right direction such as more / less, higher / lower, "
           "increase / decrease).",
    "no": "Applying the background's relationships to the situation leads to the other alternative, so the proposed "
          "entity or direction is the wrong one (watch for questions asking about less, fewer, lower or which one "
          "did NOT show an effect).",
}
STOP = {"the", "a", "an", "and", "of", "in", "to", "with", "was", "is", "were", "at", "for", "on", "but", "while",
        "than", "as", "from", "by", "had", "has", "have", "did", "does", "would", "will", "which", "who", "that",
        "or", "not", "it", "they", "he", "she", "his", "her", "their", "be", "been", "are"}
TOK = re.compile(r"[A-Za-z0-9][\w'-]*")
SENT_WORDS = {"what", "why", "how", "when", "where", "all", "each", "every", "some", "any", "many", "most", "few",
              "none", "two", "three", "yes", "however", "also", "after", "before", "during", "since", "while"}


QTOK = re.compile(r"[A-Za-z0-9][\w'’-]*|[,?.;:!]")
DET = {"the", "a", "an"}
FUNC = {"the", "a", "an", "not", "no", "do", "does", "did", "will", "would", "is", "are", "was", "were", "be", "it",
        "they", "which", "who", "what", "whom", "whose", "that", "this", "these", "those", "he", "she", "his", "her",
        "their", "its", "or", "and", "of", "in", "on", "at", "to", "for", "by", "with", "from", "than", "as", "if",
        "have", "has", "had", "can", "could", "should", "may", "might", "one", "ones", "both", "either", "neither",
        "there", "here", "then", "so", "but", "more", "less"}
ANTONYM = {}
for x, y in [("more", "less"), ("more", "fewer"), ("higher", "lower"), ("increase", "decrease"),
             ("increased", "decreased"), ("increases", "decreases"), ("increasing", "decreasing"),
             ("faster", "slower"), ("larger", "smaller"), ("bigger", "smaller"), ("greater", "smaller"),
             ("greater", "lesser"), ("stronger", "weaker"), ("longer", "shorter"), ("warmer", "cooler"),
             ("hotter", "colder"), ("warmer", "colder"), ("up", "down"), ("yes", "no"), ("better", "worse"),
             ("easier", "harder"), ("thicker", "thinner"), ("heavier", "lighter"), ("older", "younger"),
             ("earlier", "later"), ("wider", "narrower"), ("deeper", "shallower"), ("richer", "poorer"),
             ("high", "low"), ("more likely", "less likely"), ("raise", "lower"), ("rise", "fall"),
             ("stronger", "weaker"), ("expand", "contract"), ("expanded", "contracted"), ("gain", "lose"),
             ("positive", "negative"), ("closer", "farther"), ("closer", "further"), ("brighter", "dimmer"),
             ("acidic", "basic"), ("left", "right"), ("above", "below"), ("inside", "outside")]:
    ANTONYM.setdefault(x, set()).add(y)
    ANTONYM.setdefault(y, set()).add(x)
LEFT_BOUND = {",", ":", ";", "which", "who", "whom", "whose", "what", "where", "when", "the", "a", "an", "in", "at",
              "on", "to", "from", "for", "by", "with", "between", "either", "is", "are", "was", "were", "be", "been",
              "will", "would", "could", "can", "should", "did", "does", "do", "have", "has", "had", "than", "or", "and",
              "use", "uses", "used", "choose", "pick", "select", "prefer", "been"}
BOUND = {",", "?", ".", ";", ":", "!", "than", "compared", "relative", "when", "if", "after", "before", "during",
         "in", "at", "for", "to", "on"}


def _toks(s):
    return QTOK.findall(s)


def alt_from_question(q, a):
    """The single alternative that the question itself offers against the answer ('X or Y'), or (None, None).

    Token-level alignment around ' or ': the answer must be one side of the pair (allowing a determiner and a
    shared prefix/suffix such as 'the ones from the Ozarks or the ones from the Rockies', 'more fur or less fur',
    'maximize or not maximize'); the other side must be a parallel phrase of the same length made of content
    tokens (never a bare function word), and, unless the pair is a known antonym pair, must end at a phrase
    boundary. Anything that does not align cleanly returns None (the question is then not used)."""
    T = _toks(q)
    low = [t.lower().replace("’", "'") for t in T]
    A = [t.lower().replace("’", "'") for t in _toks(a) if t not in ",?.;:!"]
    while A and A[0] in DET and len(A) > 1:
        A = A[1:]
    n = len(A)
    if not n or n > 4:
        return None, None
    words = lambda xs: all(re.match(r"[a-z0-9]", x) for x in xs)
    found = set()
    for i, t in enumerate(low):
        if t != "or":
            continue
        L = low[:i]
        if L and L[-1] == ",":
            L = L[:-1]
        R = low[i + 1:]
        Rorig = T[i + 1:]
        Lorig = [x for x in T[:i]]
        if Lorig and Lorig[-1] == ",":
            Lorig = Lorig[:-1]
        # --- case 1: answer is the LEFT side (directly before 'or')
        if L[-n:] == A:
            before = L[:-n]
            if R[:1] == ["not"] and R[1:1 + n] == A:
                found.add(("not " + " ".join(A), "q-not"))
                continue
            p = 0
            if R[:1] != A[:1]:
                for k in range(min(5, len(before), len(R)), 0, -1):
                    if before[-k:] == R[:k]:
                        p = k
                        break
                if p == 0 and R[:1] and R[0] in DET:
                    p = 1
            alt, altorig, nxt = R[p:p + n], Rorig[p:p + n], (R[p + n] if len(R) > p + n else "?")
        # --- case 2: answer is the RIGHT side (directly after 'or', possibly after a determiner / shared prefix)
        else:
            j = None
            for p in range(0, 6):
                if R[p:p + n] == A and (p == 0 or all(x in DET or x in L for x in R[:p])):
                    j = p
                    break
            if j is None:
                continue
            after = R[j + n:]
            s = 0
            for k in range(min(4, len(after)), 0, -1):
                if after[:k] == L[-k:] and after[:k] != A[-k:]:
                    s = k
                    break
            LL = L[:len(L) - s] if s else L
            LLo = Lorig[:len(Lorig) - s] if s else Lorig
            if j and R[0] == "not" and LL[-n:] == A:
                continue
            if A[0] == "not" and LL[-(n - 1):] == A[1:]:
                found.add((" ".join(LLo[-(n - 1):]), "q-not"))
                continue
            alt, altorig = LL[-n:], LLo[-n:]
            nxt = R[j + n] if len(R) > j + n else "?"
            # the left phrase must START where the alternative starts ('San Francisco or Baltimore' is not
            # 'Francisco'; 'clear skies or overcast' is not 'skies'), unless the pair is a known antonym pair
            prv = LL[-n - 1] if len(LL) > n else ","
            if prv not in LEFT_BOUND and " ".join(alt) not in ANTONYM.get(" ".join(A), ()):
                continue
            # the answer side must itself end at a boundary unless it is a known antonym pair
        if len(alt) != n or not words(alt) or alt == A:
            continue
        if n == 1 and alt[0] in FUNC and not (alt[0] in ANTONYM.get(A[0], ())):
            continue
        if n >= 2 and sum(x != y for x, y in zip(alt, A)) != 1 and alt[0] != A[0]:
            continue
        anto = " ".join(alt) in ANTONYM.get(" ".join(A), ()) or (n == 1 and alt[0] in ANTONYM.get(A[0], ()))
        if not anto and nxt not in BOUND:
            continue
        found.add((" ".join(altorig), "question-or"))
    if len(found) == 1:
        alt, how = found.pop()
        return alt, "question-or"
    return None, None


def is_id_token(t):
    return t[:1].isupper() or (len(t) == 1 and t.isalnum()) or t.isdigit()


def alt_from_situation(sit, a):
    a = a.strip().rstrip(".")
    at = TOK.findall(a)
    if not at or len(at) > 3:
        return None
    toks = TOK.findall(sit)
    low = [t.lower() for t in toks]
    atl = [t.lower() for t in at]
    k = len(at)
    pos = [i for i in range(len(low) - k + 1) if low[i:i + k] == atl]
    if not pos:
        return None
    cands = set()
    for i in pos:
        prev = low[i - 1] if i > 0 else None
        nxt = low[i + k] if i + k < len(low) else None
        for j in range(len(toks) - k + 1):
            span = toks[j:j + k]
            sl = [s.lower() for s in span]
            if sl == atl:
                continue
            p2 = low[j - 1] if j > 0 else None
            n2 = low[j + k] if j + k < len(low) else None
            ctx = (prev is not None and prev not in STOP and p2 == prev) or \
                  (nxt is not None and nxt not in STOP and n2 == nxt)
            if not ctx:
                continue
            diff = [idx for idx in range(k) if sl[idx] != atl[idx]]
            if k == 1:
                ok = is_id_token(span[0]) and is_id_token(at[0]) and span[0].lower() not in STOP
            else:
                ok = len(diff) == 1 and is_id_token(span[diff[0]]) and is_id_token(at[diff[0]])
            if ok:
                cands.add(" ".join(span))
    cands = {c for c in cands if c.lower() != a.lower()}
    # review fix: a candidate made of a function word or a sentence-initial word ('This week', 'What', 'Both') or a
    # bare number standing against a name is not a parallel entity
    def ok_shape(c):
        ct = TOK.findall(c)
        if len(ct) == 1:
            if ct[0].lower() in FUNC or ct[0].lower() in SENT_WORDS:
                return False
        elif any(x.lower() in FUNC for x, y in zip(ct, at) if x.lower() != y.lower()):
            return False
        if any(t.isdigit() for t in ct) != any(t.isdigit() for t in at):
            return False
        return True
    cands = {c for c in cands if ok_shape(c)}
    return cands.pop() if len(cands) == 1 else None


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "ropes"
    paths = {f: C.fetch(URL + f, cache / Path(f).name, sha) for f, sha in FILES.items()}
    df = pd.read_parquet(paths["plain_text/train-00000-of-00001.parquet"])
    stats = collections.Counter()
    by_sit = collections.defaultdict(list)
    for r in df.to_dict("records"):
        ans = [a for a in r["answers"]["text"]]
        if len(ans) != 1 or not ans[0].strip():
            stats["drop_answer_shape"] += 1
            continue
        a = C.clean(ans[0])
        q = C.clean(r["question"])
        alt, how = alt_from_question(q, a)
        if alt is None:
            alt = alt_from_situation(r["situation"], a)
            how = "situation-entity" if alt else None
        if alt is None:
            stats["drop_no_certain_alternative"] += 1
            continue
        by_sit[C.norm(r["situation"])].append({"rid": r["id"], "bg": C.clean(r["background"]),
                                               "sit": C.clean(r["situation"]), "q": q, "a": a, "alt": alt,
                                               "how": how})
    recs = []
    for k in sorted(by_sit):
        cands = sorted(by_sit[k], key=lambda x: x["rid"])
        recs.append(rng.choice(cands))
    stats["situations"] = len(recs)
    hits = C.decon({r["rid"]: [r["bg"], r["sit"], r["q"]] for r in recs}, cache_name=KEY)
    xhits = C.cross_v14({r["rid"]: [r["sit"] + " " + r["q"]] for r in recs}, own_keys={KEY})
    recs = [r for r in recs if r["rid"] not in hits and r["rid"] not in xhits]
    recs.sort(key=lambda r: r["rid"])
    rng.shuffle(recs)
    rows = []
    for j, r in enumerate(recs):
        is_yes = j % 2 == 0
        prop = r["a"] if is_yes else r["alt"]
        state = (f"Background:\n{r['bg']}\n\nSituation:\n{r['sit']}\n\nQuestion: {r['q']}\n"
                 f"Proposed answer: {prop}")
        e = C.edge(r["q"], order=("double_negation", "negation"))
        q_wo_alts = re.sub(r"\b\w+\s+or\s+\w+\b", " ", r["q"])  # 'more or less', 'increase or decrease' are neutral
        if e is None and re.search(r"\b(less|fewer|lower|smaller|decrease[sd]?|weaker|slower)\b", q_wo_alts, re.I):
            e = "implicit"  # the question asks about the lesser / decreasing side, reversing the obvious reading
        rows.append({
            "key": KEY, "rid": r["rid"], "state": state, "instructions": QUESTION, "options": C.YN,
            "gold": "yes" if is_yes else "no", "soft": None,
            "meta": {"dataset": DATASET, "config": "plain_text train",
                     "revision": f"hf:{REV}; sha256:{FILES['plain_text/train-00000-of-00001.parquet']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"answer": r["a"], "alternative": r["alt"], "alternative_from": r["how"]},
                     "family": C.FAMILY, "edge": e},
        })
    rows = C.near_dup_filter(rows, lambda x: x["state"], thresh=0.97)
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits), "| cross_v14:", len(xhits))
    print("alternative source:", dict(collections.Counter(x["meta"]["orig_label"]["alternative_from"] for x in rows)))
    C.show_samples(rows, n=5, seed=12)
    C.append_manifest(C.manifest_record(
        KEY, DATASET + ", train split", LICENCE, rows, "yesno",
        "Science/health background + situation + question; proposed answer = gold or its single certain alternative "
        "(offered in the question, or the one parallel entity in the situation); one question per situation; "
        "alternatives from a token-level alignment around 'or' (garbled / function-word proposals removed).", st))


if __name__ == "__main__":
    main()
