"""v12 card swap: replace legacy (other-model-written) label definitions in
data/train_2b.jsonl with Claude-written ones from assets/cards_claude/<source>.json.

Outputs
  data/v12_parts/card_swap.json                     {old definition text: new definition}
  data/v12_parts/train_2b_cards_swapped_sample.jsonl 30 swapped rows for review

A card line is "- <label>: <definition>". <label> is either the plain label
(e.g. "follows from the passage", "0: 1 star: very negative") or an opaque code
(e.g. "Label-Q"). The old definition text identifies the underlying label; codes
are kept as they are and only the text after "- <label>: " is replaced.

../assets/cards/*.json (legacy card files) are read only to cross-check the
label <-> definition correspondence; none of their wording is reused.
"""
import collections
import glob
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = os.path.join(HERE, "data/train_2b.jsonl")
NEW_DIR = os.path.join(HERE, "assets/cards_claude")
LEGACY_DIR = os.path.join(HERE, "../assets/cards")
OUT_DIR = os.path.join(HERE, "data/v12_parts")
SWAP_OUT = os.path.join(OUT_DIR, "card_swap.json")
SAMPLE_OUT = os.path.join(OUT_DIR, "train_2b_cards_swapped_sample.jsonl")

# source families whose cards are Claude-authored or handled elsewhere
EXCLUDED_PREFIX = ("tb_", "hard_", "std_", "binj_", "judge_", "pg_", "lah_", "meta", "wiki")
CODE_RE = re.compile(r"^- ((?:Label|Class|Option)[- ][A-Z0-9]{1,3}): ")
BANNED = re.compile(r"closing administrator|ignore the discussion above|has confirmed this article|"
                    r"annotation team|QA reviewer|only sensible reading|really about|re-labelled|relabel", re.I)


def is_carded_source(src):
    return not src.startswith(EXCLUDED_PREFIX)


def split_line(line, candidates):
    """Return (label, definition) for one card line."""
    for lab in candidates:
        pre = "- " + lab + ": "
        if line.startswith(pre):
            return lab, line[len(pre):]
    m = CODE_RE.match(line)
    if m:
        return m.group(1), line[m.end():]
    m = re.match(r"^- (.*?): (.*)$", line, re.S)
    if not m:
        raise ValueError("unparseable card line: %r" % line[:80])
    return m.group(1), m.group(2)


def load_new():
    new = {}
    for p in sorted(glob.glob(os.path.join(NEW_DIR, "*.json"))):
        new[os.path.basename(p)[:-5]] = json.load(open(p))
    return new


def rows():
    with open(TRAIN) as f:
        for line in f:
            r = json.loads(line)
            if r.get("card") and is_carded_source(r["source"]):
                yield r


def row_lines(r, new):
    under = list(new.get(r["source"], {}))
    cands = sorted(set((r.get("options") or []) + under), key=len, reverse=True)
    return [split_line(cl, cands) for cl in r["card"].split("\n")]


def ngrams(text, n=5):
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def main():
    new = load_new()
    ok = True

    # ---- pass 1: old definition text -> underlying label, per source
    def_labels = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    sources = collections.Counter()
    for r in rows():
        s = r["source"]
        sources[s] += 1
        if s not in new:
            print("MISSING new card file for carded source:", s)
            ok = False
            continue
        for lab, d in row_lines(r, new):
            def_labels[s][d][lab] += 1

    old2label = {}  # (source, old def) -> underlying label
    for s, dd in def_labels.items():
        for d, labs in dd.items():
            real = {l for l in labs if l in new[s]}
            if len(real) != 1:
                print("UNRESOLVED/AMBIGUOUS definition in %s: labels=%s def=%r" % (s, sorted(labs), d[:50]))
                ok = False
                continue
            old2label[(s, d)] = real.pop()
        # every new label should be used
        used = {old2label[(s, d)] for d in dd if (s, d) in old2label}
        extra = set(new[s]) - used
        if extra:
            print("note: %s new labels never seen in train_2b cards: %s" % (s, sorted(extra)))

    # ---- cross-check against legacy card files (correspondence only)
    legacy = collections.defaultdict(set)  # old def prefix -> labels
    for p in glob.glob(os.path.join(LEGACY_DIR, "*.json")):
        c = json.load(open(p)).get("cards", {})
        for lab, v in c.items():
            if isinstance(v, dict) and v.get("definition"):
                legacy[v["definition"].strip()].add(lab)
    agree = disagree = unmatched = 0
    for (s, d), lab in old2label.items():
        hits = {l for ld, ls in legacy.items() if d.startswith(ld) for l in ls}
        if not hits:
            unmatched += 1
        elif lab in hits:
            agree += 1
        else:
            disagree += 1
            print("LEGACY DISAGREES %s: %s vs %s" % (s, lab, sorted(hits)))
            ok = False
    print("legacy cross-check: agree=%d disagree=%d not-in-legacy=%d" % (agree, disagree, unmatched))

    # ---- new definition checks
    old_grams = set()
    for (s, d) in old2label:
        old_grams |= ngrams(d)
    for s, dd in new.items():
        for lab, nd in dd.items():
            nw = len(nd.split())
            if not 8 <= nw <= 35:
                print("WORDCOUNT %s/%s: %d" % (s, lab, nw)); ok = False
            if BANNED.search(nd) or "\n" in nd:
                print("BANNED/NEWLINE %s/%s" % (s, lab)); ok = False
            shared = ngrams(nd) & old_grams
            if shared:
                print("OVERLAP (5-gram with legacy) %s/%s: %s" % (s, lab, sorted(shared)[:3])); ok = False

    # ---- swap map
    swap = {}
    for (s, d), lab in sorted(old2label.items()):
        nd = new[s][lab]
        if d in swap and swap[d] != nd:
            print("CONFLICT: same old text maps to two new defs (%s)" % s); ok = False
        swap[d] = nd
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(swap, open(SWAP_OUT, "w"), indent=1, ensure_ascii=False)

    # ---- pass 2: apply + verify every carded row
    n_rows = n_lines = n_lines_ok = n_rows_ok = n_code_rows = n_code_ok = 0
    per_src = collections.Counter()
    by_src = collections.defaultdict(list)
    for r in rows():
        s = r["source"]
        parts = row_lines(r, new)
        out_lines, row_ok = [], True
        for lab, d in parts:
            n_lines += 1
            if d in swap:
                n_lines_ok += 1
                out_lines.append("- %s: %s" % (lab, swap[d]))
            else:
                row_ok = False
                out_lines.append("- %s: %s" % (lab, d))
        new_card = "\n".join(out_lines)
        # label prefixes (incl. renamed codes) unchanged, same line count
        old_pref = [l for l, _ in parts]
        new_pref = [l for l, _ in row_lines(dict(r, card=new_card), new)]
        if old_pref != new_pref:
            row_ok = False
        codes = [l for l in old_pref if CODE_RE.match("- %s: " % l)]
        if codes:
            n_code_rows += 1
            opts = r.get("options") or []
            code_ok = new_pref == old_pref and (not opts or set(codes) <= set(opts))
            if code_ok:
                n_code_ok += 1
            else:
                row_ok = False
        if any(d in new_card for _, d in parts):
            row_ok = False
        n_rows += 1
        n_rows_ok += row_ok
        per_src[s] += row_ok
        out = dict(r, card=new_card)
        out.setdefault("meta", {})
        out["meta"] = dict(out["meta"] or {}, card_src="claude_v12")
        by_src[s].append((bool(codes), out))

    print("\ncarded sources (%d):" % len(sources))
    for s in sorted(sources):
        print("  %-16s rows=%5d swapped_ok=%5d labels=%d" % (s, sources[s], per_src[s], len(new.get(s, {}))))
    print("labels: %d   distinct old texts mapped: %d" % (sum(len(new[s]) for s in sources if s in new), len(swap)))
    print("line coverage: %d/%d = %.2f%%" % (n_lines_ok, n_lines, 100.0 * n_lines_ok / max(n_lines, 1)))
    print("row coverage:  %d/%d = %.2f%%" % (n_rows_ok, n_rows, 100.0 * n_rows_ok / max(n_rows, 1)))
    print("renamed-code rows keeping codes: %d/%d" % (n_code_ok, n_code_rows))
    if n_lines_ok != n_lines or n_rows_ok != n_rows or n_code_ok != n_code_rows:
        ok = False

    # ---- review sample: 30 rows spread over sources, codes included where present
    rng = random.Random(12)
    srcs = sorted(by_src)
    sample = []
    for s in srcs:
        items = by_src[s]
        coded = [o for c, o in items if c]
        plain = [o for c, o in items if not c]
        if coded:
            sample.append(rng.choice(coded))
        if plain:
            sample.append(rng.choice(plain))
    rest = [o for s in srcs for _, o in by_src[s] if o not in sample]
    rng.shuffle(rest)
    sample = (sample + rest)[:30]
    with open(SAMPLE_OUT, "w") as f:
        for o in sample:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print("wrote", SWAP_OUT, "and", SAMPLE_OUT, "(%d rows)" % len(sample))
    print("ALL CHECKS PASS" if ok else "CHECKS FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
