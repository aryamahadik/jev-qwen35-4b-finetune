"""Shared helpers of solver B: result dicts, lettered-option recovery, line utilities. Stdlib only."""


class Abstain(Exception):
    """B cannot decide from the rendered row (unparsable, ambiguous, or a source it needs is not configured). Carries a short reason code."""

    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


# Opus ruling Q3a (18 Oct): the sha-bound sources (the L-0 image-record stdlib export for EX-B1 / EX-B2, the hashed Opus table T63-LIC-TABLE for LIC)
# are checked against the row's witness sha ALWAYS. A sha that is not configured, a witness without a sha, a different sha, or a FIXTURE source /
# sha (non-production, build-stage evidence only) is an abstain; B never labels from an unverified source.
FIXTURE_MARKERS = ("fixture", "standin", "stand-in", "stand_in", "placeholder", "dummy", "test")


def is_fixture_marked(sha):
    low = str(sha).lower()
    return any(m in low for m in FIXTURE_MARKERS)


def _blank(x):
    return not isinstance(x, str) or not x.strip()


def require_sha(kind, configured, witnessed, fixture=False, allow_fixture=False):
    """kind = "export" | "table". Raises Abstain unless `configured` (the sha recorded by the L-0 image record / the Opus table record, handed to B as
    configuration) is present, is not a fixture, and equals the sha the row's witness carries. `fixture` = the caller declares the source a fixture;
    only an explicit `allow_fixture` (the build-stage CPU harness) lets a fixture source through."""
    if _blank(configured):
        raise Abstain("no_%s_sha" % kind)
    marked = bool(fixture) or is_fixture_marked(configured) or (not _blank(witnessed) and is_fixture_marked(witnessed))
    if marked and not allow_fixture:
        raise Abstain("fixture_%s_source" % kind)
    if _blank(witnessed):
        raise Abstain("witness_%s_sha_missing" % kind)
    if witnessed != configured:
        raise Abstain("%s_sha_mismatch" % kind)


def ok(label, letter, reason=None, **extra):
    d = {"status": "ok", "label": label, "letter": letter, "reason": reason}
    d.update(extra)
    return d


def abstain(reason):
    return {"status": "abstain", "label": None, "letter": None, "reason": reason}


def parse_options_text(options_text):
    """'A) YES\\nB) NO' -> [('A', 'YES'), ('B', 'NO')]; any line that is not a lettered option raises Abstain."""
    out = []
    for raw in str(options_text).split("\n"):
        line = raw.strip()
        if not line:
            continue
        if len(line) < 3 or line[1] != ")" or not ("A" <= line[0] <= "Z"):
            raise Abstain("option_line")
        out.append((line[0], line[2:].strip()))
    if not out:
        raise Abstain("no_options")
    return out


def letter_for(label, bview):
    """The option letter whose text is `label`, recovered from the RENDERED options text and cross-checked with the b-view option list."""
    pairs = parse_options_text(bview["rendered"]["options_text"])
    listed = [(o["letter"], o["text"].strip()) for o in bview["options"]]
    if pairs != listed:
        raise Abstain("options_disagree")
    hits = [lt for lt, tx in pairs if tx == label]
    if len(hits) != 1:
        raise Abstain("label_not_offered")
    return hits[0]


def split_blocks(text):
    """Blank-line separated blocks of a context (a block keeps its inner newlines)."""
    return [b for b in text.split("\n\n") if b.strip()]


def norm_ws(s):
    return " ".join(str(s).split())
