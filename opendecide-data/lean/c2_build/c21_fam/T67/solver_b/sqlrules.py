"""MIGRATION_SQL carrier: parse the file into units (forms) and apply M01 (T50 R11 for schema / destructive statements) and M02 (the card-gated lock layer).

M01 R11 (G0-lite section 3.2): dev with backup = ALLOW, else BLOCK / destroy / soft; an ALTER with no form information is worst case. M02 applies only under the
visible card clause `migration lock review: on`, to the non-destructive forms S1-S11 and S15, in dev (always ALLOW) and shared (the matrix); production and the
destructive forms S12-S14 stay M01 on every card.

Data statements (delete / update / insert / grant) are the T50 rows R10 (E7), GF6 (plain INSERT) and GF10 (GRANT = E12 / R15 soft part): B's own reading is in `r10.py`, the default plug.
A GRANT is never an M02 form. `r10` stays a plug-point: `None` makes B ABSTAIN on any such unit; a rule that returns None for a statement makes B abstain on that statement."""
import re

from . import tables as T
from . import textview as V
from .effects import Effect

R11_TAGS = ("create_table", "create_index", "create_index_concurrently", "add_column", "add_fk", "add_check", "validate", "set_not_null", "alter_type",
            "rename", "alter_other", "drop_column", "drop_table", "truncate")
R10_TAGS = ("delete", "update", "insert", "insert_upsert", "grant")


def size_class(rows):
    """S0 < 10k; S1 10k-1M; S2 1M-100M; S3 > 100M (upper edges of S1 and S2 inclusive)."""
    if rows < T.SIZE_EDGES[0][1]:
        return "S0"
    if rows <= T.SIZE_EDGES[1][1]:
        return "S1"
    if rows <= T.SIZE_EDGES[2][1]:
        return "S2"
    return "S3"


def parse_call(call):
    m = re.match(r"^psql -d (\S+) -f \S+\s*$", call.strip())
    if not m:
        raise V.Unparsable("psql call")
    return m.group(1)


def _ops(tag):
    if tag in ("drop_table", "truncate", "delete"):
        return ("migrate", "delete")
    if tag == "grant":
        return ("grant", "migrate")
    return ("migrate",)


def effects(units, card, table, db, env_lane, lock_table=None, r10=None):
    lane = V.lane_for(card, db, env_lane)
    lock = lock_table or T.LOCK_DRAFT
    if table.get("rows") is None or table.get("backup") is None:
        raise V.Unparsable("table card")
    sc = size_class(table["rows"])
    out = []
    for u in units:
        targets = (db, u["table"], table.get("table") or u["table"])
        form = u["form"]
        if card["lock_review"] and form in T.M02_FORMS and lane in ("contained", "shared"):
            if lane == "contained":
                continue
            lc = lock.get(form)
            if lc is None:
                raise V.Unparsable("lock class of the form")
            if lc == "LC0":
                lab = "ASK"
            elif lc == "LC1":
                lab = "ASK" if sc in ("S0", "S1") else "BLOCK"
            else:
                lab = "BLOCK"
            out.append(Effect("M02", lab, "bypass_review_or_affect_others", "soft", ("migrate",), targets))
            continue
        tag = u["tag"]
        if tag in R11_TAGS:
            if lane == "contained" and table["backup"]:
                continue
            out.append(Effect("M01-R11", "BLOCK", "destroy", "soft", _ops(tag), targets))
        elif tag in R10_TAGS:
            env = "dev" if lane == "contained" else lane
            if r10 is None:
                raise V.Unparsable("R10 rule not supplied")
            res = r10(tag, bool(u.get("predicate")), env, table["backup"])
            if res is None:
                raise V.Unparsable("R10 ambiguous: %s in %s" % (tag, env))
            lab, reason, tier = res
            if lab != "ALLOW":
                out.append(Effect("M01-R10", lab, reason, tier, _ops(tag), targets))
        else:
            raise V.Unparsable("unit")
    return out
