"""Hand-built rendered fixtures (no generator involved)."""

DEFS_M = "Definitions. A merge conflict shows the file."
OPTS_YN = "A) YES\nB) NO"


def merge_ctx(stem, view, test_a, test_b, resolution):
    return "\n\n".join([DEFS_M, "Conflict view of %s.py:\n%s" % (stem, view), "Tests of side A (test_%s_a.py):\n%s" % (stem, test_a),
                        "Tests of side B (test_%s_b.py):\n%s" % (stem, test_b), "Proposed resolution of %s.py:\n%s" % (stem, resolution)])


def semver_ctx(stem, old, new, callers, bump=None):
    parts = ["Definitions.", "Old API (%s.py):\n%s" % (stem, old), "New API (%s.py):\n%s" % (stem, new),
             "Callers written against the old API (test_%s_callers.py):\n%s" % (stem, callers)]
    if bump:
        parts.append("Declared version bump: %s" % bump)
    return "\n\n".join(parts)


def msg_ctx(diff, message):
    return "Definitions.\n\nDiff:\n%s\n\nCommit message: %s" % (diff.rstrip("\n"), message)


def bview(head, context, options=(("A", "YES"), ("B", "NO")), question="Q?"):
    opts = [{"letter": l, "text": t} for l, t in options]
    block = "\n".join("%s) %s" % (l, t) for l, t in options)
    return {"row_id": "b-0", "head": head, "sub_block": head, "rendered": {"context": context, "question": question, "options_text": block,
                                                                         "text": "\n\n".join([context, question, block])},
            "options": opts, "witness_inputs": {"head": head, "lang": "python"}}


def diff_of(body, name="m.py", old_start=1, new_start=1):
    return "--- a/%s\n+++ b/%s\n@@ -%d,6 +%d,6 @@\n%s" % (name, name, old_start, new_start, body.strip("\n"))
