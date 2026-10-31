"""LIC head of solver B: re-read the four axes from the RENDERED licence card and look the cell up in the hashed Opus table T63-LIC-TABLE.
The table is handed in (never read from a file by B) as a plain mapping {(dependency_id, project_id, usage_id, distribution_id): label} with the
G0-lite ids LC-USE-1..5 / LC-DIST-1..3 (a table keyed by the rendered phrases is accepted as well). Stdlib only."""
from .common import Abstain, norm_ws, require_sha

# G0-lite 2.3 order of the phrases = order of the ids.
USE_ID = {"vendored source copy": "LC-USE-1", "static link": "LC-USE-2", "dynamic link": "LC-USE-3", "separate process": "LC-USE-4",
          "dev-time tool only": "LC-USE-5"}
DIST_ID = {"distributed to others": "LC-DIST-1", "internal only": "LC-DIST-2", "offered as a network service": "LC-DIST-3"}
LABELS = ("COMPATIBLE", "REVIEW", "INCOMPATIBLE")
REQUIRED_DEFS = (
    "this is a policy table for a coding agent, not legal advice",
    "compatible: the dependency may be used under these terms without further review",
    "review: a human licence review is needed first",
    "incompatible: the dependency may not be used under these terms",
)


def check_definitions(context):
    flat = norm_ws(context).lower()
    for clause in REQUIRED_DEFS:
        if clause not in flat:
            raise Abstain("defs_mismatch")


def read_card(context):
    """-> dict(dep, project, use_phrase, dist_phrase) from the last 'Licence card' block."""
    lines = context.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln.strip() == "Licence card"]
    if len(idx) != 1:
        raise Abstain("card_count")
    got = {}
    for ln in lines[idx[0] + 1:]:
        for key, field in (("Dependency licence: ", "dep"), ("Project licence: ", "project"), ("Usage: ", "use"), ("Distribution: ", "dist")):
            if ln.startswith(key):
                if field in got:
                    raise Abstain("card_dup_field")
                got[field] = ln[len(key):].strip()
    if sorted(got) != ["dep", "dist", "project", "use"]:
        raise Abstain("card_fields")
    return got


def lookup(table, dep, project, use_phrase, dist_phrase):
    if table is None:
        raise Abstain("no_table_source")
    if use_phrase not in USE_ID or dist_phrase not in DIST_ID:
        raise Abstain("axis_phrase")
    for key in ((dep, project, USE_ID[use_phrase], DIST_ID[dist_phrase]), (dep, project, use_phrase, dist_phrase)):
        if key in table:
            label = table[key]
            if label not in LABELS:
                raise Abstain("table_label")
            return label
    raise Abstain("cell_missing")


def solve(bview, table, table_sha=None, fixture=False, allow_fixture=False):
    ctx, qtext = bview["rendered"]["context"], bview["rendered"].get("question") or ""
    check_definitions(ctx)
    card = read_card(ctx)
    w = bview.get("witness_inputs") or {}
    # Opus ruling Q3a (18 Oct): the hashed T63-LIC-TABLE and its sha are MANDATORY: no table, no configured sha, a fixture, a witness without a
    # sha or a different sha -> abstain (never "check the sha only if one is configured").
    if table is None:
        raise Abstain("no_table_source")
    require_sha("table", table_sha, w.get("table_sha"), fixture, allow_fixture)
    if card["dep"] not in qtext or card["project"] not in qtext:
        raise Abstain("question_context_mismatch")
    return lookup(table, card["dep"], card["project"], card["use"], card["dist"]), "lic_cell"
