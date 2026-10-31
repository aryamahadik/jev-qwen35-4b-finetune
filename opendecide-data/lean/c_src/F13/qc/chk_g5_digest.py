"""G5 reading aid (check:F13): a search view over ONE rendered model prompt (tmp/chk/g5/rows/<i>.txt), never gold.
Prints the question, options, the card lines that are not in the common convention set (tmp/chk/g5/common_card.txt,
read once), and the document sections that contain a key token of the question (IDs, table / rule / item names, quoted
values, extra regexes given on the command line), plus every line holding a marked unknown ('illegible',
'not included in this copy'). Sections are cut at heading-like lines; markup is stripped and long records joined.
Usage: chk_g5_digest.py <i> [--all] [--re REGEX ...] [--max N]   (--all: whole document, compacted)"""
import re, sys, html
from pathlib import Path

D = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F13/tmp/chk/g5")
COMMON = D / "common_card.txt"


def norm(l):
    s = html.unescape(re.sub(r"</?[a-z][a-z0-9]*(?:\s[^<>]*)?/?>", " ", l))
    s = s.strip().strip("`").strip()
    s = re.sub(r"^(?:>\s*)+", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def is_head(raw, s):
    if not s:
        return False
    if re.match(r"^\s*(#{1,6}\s|<h[1-6]|<section|<tr><th|\*\*[^*]+\*\*\s*$)", raw):
        return True
    if not raw.lstrip().startswith(("- ", "* ", '"- ')) and len(s) < 70 and not re.search(r"\b[A-Z]{1,5}-\w*\d", s) and (re.match(r"^\d+(?:\.\d+)*\.\s+[A-Z][^.:|]{1,60}$", s) or re.match(r"^[A-Z][^.:|]{1,60}\s\(\d+\):?$", s) or re.match(r"^(?:Part \d+ of )?[Tt]able [A-Z0-9]+(?: \(continued\))?:?$", s)):
        return True
    t = s.strip('"{[,: ').strip()
    if raw.rstrip().endswith((":", ": {", ": [", "{", "[")) and 0 < len(t) < 70 and not re.search(r"\.\s", t):
        return True
    return False


def load(i):
    t = (D / "rows" / f"{int(i):03d}.txt").read_text()
    a = t.index("<<<UNTRUSTED TEXT START>>>"); b = t.index("<<<UNTRUSTED TEXT END>>>")
    head, doc = t[:a], t[a + 26:b]
    return head, doc.split("\n")


def sections(lines):
    """-> list of (start, end) line ranges cut at heading-like lines of the shallowest heading indent (after line 3)."""
    heads = [(j, len(l) - len(l.lstrip())) for j, l in enumerate(lines) if is_head(l, norm(l))]
    if not heads:
        return [(0, len(lines))]
    inds = sorted({d for j, d in heads if j > 2})
    cuts = []
    for lvl in inds:
        cuts = [j for j, d in heads if d <= lvl]
        if len(cuts) >= 8:
            break
    cuts = sorted(set([0] + cuts))
    return [(a, b) for a, b in zip(cuts, cuts[1:] + [len(lines)])]


STOP = {"Is", "Does", "Do", "What", "Which", "How", "Who", "Under", "The", "In", "For", "As", "Of", "Is it", "Question",
        "Answer", "Read", "Yes", "No", "Long", "Document", "Put", "Study", "This", "Go", "Look", "Please", "Based", "Using",
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
        "December", "Mon", "Group", "It", "Outcomes", "Sample", "Definitions", "Options", "Does the", "A", "An", "Report", "Table", "Part", "Rule"}


def flex(k):
    return r"(?<![\w-])" + r"[\s_-]?".join(re.escape(w) for w in k.split()) + r"(?![\w-])"


def keys_of(q, extra):
    """-> (strong, weak) compiled keys. strong: IDs, table / rule / item names, the item phrase of a version question,
    quoted values, the action-item / motion / hold kind; weak: capitalised names (scope units, holders)."""
    st = set(re.findall(r"\b[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+\b", q))
    st |= {m.lower() for m in re.findall(r"\b(?:[Tt]able|[Rr]ule|[Ss]chedule|[Ss]egment|[Mm]otion|[Ii]tem|[Ss]ection|[Cc]lause|[Aa]ttachment|[Cc]riterion) [A-Z0-9][A-Za-z0-9.-]*\b", q)}
    st |= set(re.findall(r"'([^']{3,60})'", q)) | set(re.findall(r'"([^"]{3,60})"', q))
    m = re.search(r"\bversion of (?:the )?([a-z][a-z ]{2,40}?) (?:is|was|in|for|that|applies)\b", q)
    if m:
        st.add(m.group(1))
    if re.search(r"(?i)\b(?:outcome|decision|result|status) (?:for|on|of)\b", q):
        st.add(r"rule"); st.add("version"); st.add("exception"); st.add("amendment")
    for kind in ("action item", "motion", "hold", "exception", "exclusion", "log entr"):
        if re.search(r"\b" + kind, q, re.I):
            st.add(kind)
    wk = set()
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+(?:[A-Z][a-z]+|[A-Z]\b|of|and)){0,3})", q):
        w = m.group(1).strip()
        w = re.sub(r"\s+(?:of|and)$", "", w)
        if w not in STOP and w.split()[0] not in STOP and len(w) > 2:
            wk.add(w)
    S = [re.compile(flex(k), re.I) for k in st] + [re.compile(x, re.I) for x in extra]
    W = [re.compile(flex(k), re.I) for k in wk]
    return S, W


def compact(lines, a, b, maxl=60):
    """markup stripped; a record ('- ' item, or a JSON / HTML object) and its deeper field lines joined by ' | '."""
    out, rind = [], None
    for l in lines[a:b]:
        s = norm(l)
        if not s or s in ("{", "}", "[", "]", "},", "],"):
            continue
        ind = len(l) - len(l.lstrip())
        st = l.lstrip().lstrip(">").lstrip()
        if rind is not None and ind > rind and not st.startswith(("- ", "* ")) and not is_head(l, s) and out:
            out[-1] = (out[-1] + " | " + s)[:400]
            continue
        rind = ind if st.startswith(("- ", "* ", "{")) else None
        out.append(s[:400])
    if len(out) > maxl:
        out = out[:maxl] + [f"... [{len(out) - maxl} more lines]"]
    return out


AGG = re.compile(r"(?i)\bhow many\b|\btotal\b|\bhighest\b|\blowest\b|\blargest\b|\bsmallest\b|\bmost\b|\bfewest\b|\bwhich\b[^?]*\b(?:in|of) (?:table|the table)\b|\bwhich (?:records|items|entries|rows)\b")
MARK = re.compile(r"(?i)void|draft|proposed|correct|amend|repeal|effective|valid|continued|total|exception|exclusion|rollback|roll back|status|part \d|precedence|scope|group|zone|region|period|meeting|motion|action item|hold|version|rule|applies|default|criteria|criterion|illegible|not included")


def focus(lines, a, b, ks, mx):
    """non-aggregate questions: keep key lines, heading / mark lines and records holding a key; others counted."""
    out, skipped = [], 0
    for s in compact(lines, a, b, 10 ** 6):
        rec = s.startswith(("- ", "* ")) and len(s) > 60
        if any(k.search(s) for k in ks) or MARK.search(s) or not rec:
            if skipped:
                out.append(f"[{skipped} other records]"); skipped = 0
            out.append(s)
        else:
            skipped += 1
    if skipped:
        out.append(f"[{skipped} other records]")
    return out[:mx] + ([f"... [{len(out) - mx} more lines]"] if len(out) > mx else [])


def main():
    argv = sys.argv[1:]
    idx = [x for x in argv if x.isdigit()]
    for i in idx:
        one([i] + [x for x in argv if not x.isdigit()])
        print()


def one(args):
    i = args[0]; extra = []; full = "--all" in args; mx = 60
    if "--re" in args:
        extra = [x for x in args[args.index("--re") + 1:] if not x.startswith("--") and not x.isdigit()]
    mx = int(next((x.split("=")[1] for x in args if x.startswith("--max=")), 60))
    head, lines = load(i)
    hl = head.split("\n")
    common = set(COMMON.read_text().split("\n")) if COMMON.exists() else set()
    print(hl[0])
    qi = next(j for j, l in enumerate(hl) if l.startswith("Options:")) if any(l.startswith("Options:") for l in hl) else len(hl)
    card = [norm(l) for l in hl[1:qi] if norm(l)]
    qlines = card[-2:]
    import json as _j
    sp = D / "seen_cards.json"
    seen = _j.loads(sp.read_text()) if sp.exists() else {}
    cid = hl[0].split("card ")[-1].rstrip(")")
    mine = [c for c in card[:-2] if c not in common and not c.startswith("Definitions:")]
    new = [c for c in mine if c not in set(seen.get(cid, []))]
    if cid in seen:
        print(f"CARD {cid}: {len(mine) - len(new)} lines as seen before; new:", " || ".join(c[:400] for c in new)[:3500])
    else:
        print("CARD (non-common, first view):", " || ".join(c[:600] for c in mine)[:6000])
    seen[cid] = sorted(set(seen.get(cid, [])) | set(mine)); sp.write_text(_j.dumps(seen))
    print("Q:", " // ".join(qlines))
    print("OPTIONS:", " | ".join(norm(l) for l in hl[qi + 1:] if norm(l) and not norm(l).startswith(("Text:",)))[:1500])
    qtext = " ".join(card[-6:])
    if full:
        for s in compact(lines, 0, len(lines), 10 ** 6):
            print(s)
        return
    opt_line = " ".join(norm(l) for l in hl[qi + 1:])
    oid = set(re.findall(r"\b[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9.]*[A-Za-z0-9])+\b", opt_line))
    S_, W_ = keys_of(qtext, extra + [flex(x) for x in oid])
    ks = S_ + W_
    print("KEYS strong:", [k.pattern for k in S_][:12], "weak:", [k.pattern for k in W_][:8])
    secs = sections(lines)
    sc = []
    for a, b in secs:
        blk = "\n".join(lines[a:b])
        s1 = sum(1 for k in S_ if k.search(blk)); s2 = sum(1 for k in W_ if k.search(blk))
        sc.append((s1, s2, a, b))
    if any(x[0] for x in sc):
        best2 = max(x[1] for x in sc if x[0]) if W_ else 0
        pick = [x for x in sc if x[0] and (x[1] >= best2 - 1 or not W_ or x[0] >= 2)]
    else:
        best2 = max((x[1] for x in sc), default=0)
        pick = [x for x in sc if best2 and x[1] == best2]
    pick = pick[:int(next((x.split("=")[1] for x in args if x.startswith("--secs=")), 14))]
    shown = 0
    starts = [x[0] for x in secs]
    for s1, s2, a, b in pick:
        j = starts.index(a)
        if j > 0:
            pa, pb = secs[j - 1]
            mk = [x for x in compact(lines, pa, pb, 10 ** 6)[-6:] if MARK.search(x) and len(x) < 160]
            if mk:
                print(f"  (marks just before [{a}]: " + " / ".join(mk) + ")")
        c = compact(lines, a, b, mx) if (AGG.search(qtext) or "--wide" in args) else focus(lines, a, b, ks, mx)
        print(f"--- [{a}-{b}] " + " / ".join(c[:1]))
        for s in c[1:]:
            print("  " + s)
        shown += 1
    tr = [norm(l)[:200] for l in lines if re.search(r"illegible|not included in this copy", l, re.I)]
    print(f"--- sections shown {shown}/{len(secs)}; marked unknowns: " + " || ".join(tr))


if __name__ == "__main__":
    main()
