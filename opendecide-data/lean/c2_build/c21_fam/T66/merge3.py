"""Our own 3-way merge and conflict renderer (git is NEVER invoked: T66-B8). Line based, git-like: two hunks that overlap OR TOUCH (adjacent base lines, or
two insertions at one position) conflict; hunks of one side only merge cleanly. Output segments:
  ("ok", [lines])                       text both sides agree on (clean merges applied)
  ("conflict", base_seg, ours_seg, theirs_seg)
`render_view` writes the diff3-style conflict view the row shows."""
import difflib

MARK_OURS, MARK_BASE, MARK_SEP, MARK_THEIRS = "<<<<<<< ours", "||||||| base", "=======", ">>>>>>> theirs"


def hunks(base, other):
    sm = difflib.SequenceMatcher(None, base, other, autojunk=False)
    return [(i1, i2, other[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]


def _apply(base_seg, lo, hs):
    out, pos = [], 0
    for i1, i2, new in sorted(hs):
        out += base_seg[pos:i1 - lo]
        out += new
        pos = i2 - lo
    out += base_seg[pos:]
    return out


def merge3(base, a, b):
    ha = [(i1, i2, new, "A") for i1, i2, new in hunks(base, a)]
    hb = [(i1, i2, new, "B") for i1, i2, new in hunks(base, b)]
    allh = sorted(ha + hb, key=lambda h: (h[0], h[1]))
    clusters = []
    for h in allh:
        if clusters and h[0] <= clusters[-1]["hi"]:
            c = clusters[-1]
            c["hs"].append(h)
            c["hi"] = max(c["hi"], h[1])
        else:
            clusters.append({"lo": h[0], "hi": h[1], "hs": [h]})
    segs, pos = [], 0
    for c in clusters:
        if c["lo"] > pos:
            segs.append(("ok", base[pos:c["lo"]]))
        lo, hi = c["lo"], c["hi"]
        sides = {h[3] for h in c["hs"]}
        bseg = base[lo:hi]
        if len(sides) == 1:
            segs.append(("ok", _apply(bseg, lo, [(h[0], h[1], h[2]) for h in c["hs"]])))
        else:
            oa = _apply(bseg, lo, [(h[0], h[1], h[2]) for h in c["hs"] if h[3] == "A"])
            ob = _apply(bseg, lo, [(h[0], h[1], h[2]) for h in c["hs"] if h[3] == "B"])
            segs.append(("ok", oa) if oa == ob else ("conflict", bseg, oa, ob))
        pos = hi
    if pos < len(base):
        segs.append(("ok", base[pos:]))
    # coalesce adjacent ok segments
    out = []
    for s in segs:
        if out and s[0] == "ok" and out[-1][0] == "ok":
            out[-1] = ("ok", out[-1][1] + s[1])
        else:
            out.append(s)
    return out


def conflicts(segs):
    return [s for s in segs if s[0] == "conflict"]


def resolve(segs, choice):
    """Full text lines with every conflict replaced by choice(conflict_index, segment) -> lines."""
    out, k = [], 0
    for s in segs:
        if s[0] == "ok":
            out += s[1]
        else:
            out += choice(k, s)
            k += 1
    return out


def render_view(segs):
    out = []
    for s in segs:
        if s[0] == "ok":
            out += s[1]
        else:
            out += [MARK_OURS] + s[2] + [MARK_BASE] + s[1] + [MARK_SEP] + s[3] + [MARK_THEIRS]
    return "\n".join(out) + "\n"


def parse_view(text):
    """Inverse of render_view: segments from the rendered conflict view (round trip)."""
    segs, ok, mode, cur = [], [], None, None
    for ln in text.rstrip("\n").split("\n"):
        if ln == MARK_OURS:
            if ok:
                segs.append(("ok", ok))
                ok = []
            mode, cur = "ours", {"ours": [], "base": [], "theirs": []}
        elif mode and ln == MARK_BASE:
            mode = "base"
        elif mode and ln == MARK_SEP:
            mode = "theirs"
        elif mode and ln == MARK_THEIRS:
            segs.append(("conflict", cur["base"], cur["ours"], cur["theirs"]))
            mode, cur = None, None
        elif mode:
            cur[mode].append(ln)
        else:
            ok.append(ln)
    if ok:
        segs.append(("ok", ok))
    return segs
