"""gen3_state_track: yn2b family F3 (yn2b/SPEC.md section 5 F3), built on golden_src/gen3/mv_core.py.

  train        3,500 rows = 1,700 yes/no (about 20% of latents are judge rows) + 1,100 choice (150 of them JB-letter)
               + 700 score, plus 8% attack twins (280, `inv`).                        -> yn2b_raw/gen3_state_track.jsonl
  dev_iid      175 rows: training machines and templates, new seed stream, disjoint name pool.
  dev_holdout  175 rows: the 2 held-out machines (feature flags, document versions).
                                                                   -> yn2b_raw/dev/gen3_state_track.jsonl
  devx         not built here: reviewer R renders it from held-out latents (`export_latents`).

Labels come only from gen3_state_track_sim.decide (a deterministic simulator of the typed events). The shortcut
solvers of SPEC F3 set tiers, choice distractors, score traps and the checks, never a label.

Run (from lean/):
  ../.venv/bin/python golden_src/gen3/gen3_state_track.py                  # build + checks, print a report
  ../.venv/bin/python golden_src/gen3/gen3_state_track.py --write          # also write rows, relations, defs, MANIFEST
Tests: yn2b/tests/test_gen3_state_track*.py.  Notes for decide2 (builder B): yn2b/F3_STATE_TRACK_NOTES.md.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
from collections import Counter, defaultdict
from dataclasses import replace
from datetime import timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import gen3_state_track_sim as sim  # noqa: E402
from gen3_state_track_sim import Query, Spec  # noqa: E402

KEY = "gen3_state_track"
FAM = "F3"

# ================================================================================================ targets (SPEC 3, 5)
TARGETS = {"train": {"yn": 1700, "choice": 950, "jb": 150, "score": 700, "attack": 280},
           "dev_iid": {"yn": 85, "choice": 47, "jb": 8, "score": 35, "attack": 0},
           "dev_holdout": {"yn": 85, "choice": 47, "jb": 8, "score": 35, "attack": 0}}
RATES = {"contrast": 0.55, "ladder": 0.30, "format": 0.30, "mirror": 0.30}
TIER_EVENTS = {"easy": (2, 5), "standard": (6, 12), "judge": (6, 16), "hard": (13, 40)}
MAX_STATE = 10_000
PASSES = 6  # strict passes over the recipes (deferred ones retried as the strata move); fallback only in the last
DROP_FROM, ACCEPT_FROM = 150, 400  # last pass: drop optional views from attempt 150, accept a violation only from 400
LONG_UNIT_STATE = mv.LONG_STATE
MACHINES = mv.Variants("machines", sim.ALL_MACHINES, holdout=sim.HOLDOUT_MACHINES)


# ================================================================================================ R2 review fixes
# Reviewer R2 (blind solve + decide2 disagreements, yn2b/r2_state_track_review.py) found label semantics the rendered
# rules never stated, and a few generator bugs. gen3_state_track_sim.py is left untouched (only this file was opened
# for the fix): the build, the twins, the shortcut solvers and export_latents use the machines in MACH below, which
# subclass the simulator's machines. sim.MACHINES keeps the pre-review semantics and must not be used for F3 labels.
#
#   tickets   an assignment records only the values it changes (a re-assignment of an already-assigned ticket used
#             to record its unchanged status, so a later revert reset the status too); the rules now say what a
#             revert of the first resolve does.
#   flags     several overrides for one person: each lasts its own hours, and of those in force the most recent
#             decides (the simulator let a new override end the older one, which no rule said); stated as a rule.
#   inventory a clear of more units than are in quarantine is rejected: now stated (R3 alone reads like a clamp).
#   bookings  a new hold by the person whose own hold is active replaces it: now stated.
#   dialogue  'same as before' still sets a confirmed value that 'not X' removed: now stated.
#   docs      a restore of a version that does not exist yet is refused: now stated.
# Surfaces that stay ambiguous are never generated (surface_issues): see that function.
def _insert_after(rules: list, needle: str, text: str) -> list:
    out = list(rules)
    for i, r in enumerate(out):
        if needle in r:
            out.insert(i + 1, text)
            return out
    raise AssertionError(f"rule not found: {needle}")


class TicketsR2(sim.Tickets):
    RES_REVERT = ("Reverting the event that first resolved a ticket also removes its first resolution time; the "
                  "ticket then has no first resolution until a resolve takes effect after the revert.")

    def apply(self, st, e, ent, W, flags):
        if e.kind == "assign" and ent in st:
            s = st[ent]
            if ("guards" not in flags) and (s["status"] not in self.ASSIGNABLE or
                                            e.a["who"] not in W.params["roster"]):
                return "guard"
            u = [("set", ent, "owner", s["owner"])]
            if s["status"] == "new":  # the status changes only for a new ticket
                u.append(("set", ent, "status", "new"))
                s["status"] = "assigned"
            s["owner"] = e.a["who"]
            return u
        return super().apply(st, e, ent, W, flags)

    def rules(self, W):
        return _insert_after(super().rules(W), "A revert line names an earlier event id.", self.RES_REVERT)


class FlagsR2(sim.Flags):
    OVERLAP = "When more than one override for the same person is in force at a time, the most recent of them decides."

    def apply(self, st, e, ent, W, flags):
        if e.kind == "override" and ent in st:
            s = st[ent]
            old = list(s["ov"].get(e.a["u"], ()))
            s["ov"][e.a["u"]] = old + [(e.a["on"], e.ts, e.ts + timedelta(hours=e.a["h"]))]
            return [("put", ent, "ov", e.a["u"], old)]
        return super().apply(st, e, ent, W, flags)

    def on_for(self, s, W, u, flags):
        if s["killed"]:
            return False
        live = [o for o in s["ov"].get(u, ()) if o[1] <= W.t_q and ("expiry" in flags or o[2] > W.t_q)]
        if live:
            return max(live, key=lambda o: o[1])[0]
        return s["enabled"] and W.params["buckets"][u] < s["rollout"]

    def rules(self, W):
        return _insert_after(super().rules(W), "An override lasts the stated hours from its time", self.OVERLAP)


class InventoryR2(sim.Inventory):
    CLEAR = "A clear of more units than are in quarantine at that moment is rejected and changes nothing."

    def rules(self, W):
        return _insert_after(super().rules(W), "a clear returns quarantined units", self.CLEAR)


class BookingsR2(sim.Bookings):
    REHOLD = ("A hold by the person whose own hold on the slot is still active is allowed: it replaces that hold and "
              "counts from its own time for its own minutes.")

    def rules(self, W):
        return _insert_after(super().rules(W), "A hold is allowed only if the slot has no confirmed booking",
                             self.REHOLD)


class DialogueR2(sim.Dialogue):
    SAME_EXCLUDED = ("'Same as before' sets the slot to its most recent confirmed value even when a later 'not X' "
                     "removed that value from the allowed values.")
    SPEAKER = {"set": "Customer", "oset": "Customer", "same": "Customer", "not": "Customer", "decline": "Customer",
               "third": "Customer", "propose": "Assistant", "confirm": "Assistant"}

    def rules(self, W):
        return _insert_after(super().rules(W), "'Same as before' (or 'go back to what we had before')",
                             self.SAME_EXCLUDED)


class DocsR2(sim.Docs):
    RESTORE_MISSING = "A restore that names a version number that does not exist yet is refused and changes nothing."

    def rules(self, W):
        return _insert_after(super().rules(W), "Each save or restore adds one new version", self.RESTORE_MISSING)


MACH: dict = dict(sim.MACHINES)
MACH.update({m.name: m for m in (TicketsR2(), FlagsR2(), InventoryR2(), BookingsR2(), DialogueR2(), DocsR2())})
RESTORE_REVERT = ("orders", "tickets", "bookings", "flags")  # revert = "every value it changed goes back"


def surface_issues(M, W) -> list:
    """Rendered surfaces a careful reader could take two ways; a world with any of them is never used (base worlds
    are resampled, twin candidates skipped). Replays the true (no-shortcut) trajectory up to the query time.
      restore_not_in_trash   agent: a files.restore part reported ok on a file that is not in trash
      revert_of_noop         orders/tickets/bookings/flags: a revert of an event that left a value it recorded
                             unchanged ("every value it changed goes back" says nothing changes; the simulator restores)
      revert_of_older_override  flags: a revert of an override after a later override for the same person took effect
      speaker                dialogue: a request by the Assistant, or a proposal / confirmation by the Customer
      other_booking_self     dialogue: "For my other booking <id>" whose id is this booking"""
    out = []
    if M.name == "dialogue":
        for e in W.events:
            if DialogueR2.SPEAKER.get(e.kind, e.src) != e.src:
                out.append("speaker")
            if e.kind == "oset" and e.ent == W.target and e.lt % 2 == 0:
                out.append("other_booking_self")
    st = M.init(W)
    took, rev = {}, set()
    noop = set()
    ov_key, ov_later = {}, {}  # flags: override id -> (flag, person); -> later overrides of that pair that applied
    for e in sim.time_order(W):
        if e.ts > W.t_q:
            break
        fresh = e.eid not in took
        if fresh and M.name == "agent" and e.kind != "revert" and W.params.get("dom") == "files":
            for pe, op, arg, ok in e.a["parts"]:
                if ok and op == "restore" and pe in st and st[pe]["where"] != "trash":
                    out.append("restore_not_in_trash")
        if fresh and e.kind == "revert" and M.name in RESTORE_REVERT:
            of = e.a["of"]
            if of in took and of not in rev:
                if of in noop:
                    out.append("revert_of_noop")
                if M.name == "flags" and any(x not in rev for x in ov_later.get(of, ())):
                    out.append("revert_of_older_override")
        res = sim.step(M, W, st, took, rev, e)
        if res == "ok" and e.kind != "revert" and M.name in RESTORE_REVERT:
            for r in took[e.eid]:
                if (r[0] == "set" and st[r[1]][r[2]] == r[3]) or (r[0] == "put" and st[r[1]][r[2]].get(r[3]) == r[4]):
                    noop.add(e.eid)
            if M.name == "flags" and e.kind == "override":
                key = (e.ent, e.a["u"])
                for x, k in ov_key.items():
                    if k == key:
                        ov_later[x].append(e.eid)
                ov_key[e.eid], ov_later[e.eid] = key, []
    return sorted(set(out))

# ================================================================================================ formats (SPEC 4.3)
FMTS = {"json": "chrono", "json:newest": "newest", "kv": "chrono", "markdown": "chrono",
        "markdown:shuffled": "shuffled", "prose": "chrono", "log:chrono": "chrono", "log:newest": "newest",
        "log:shuffled": "shuffled", "log:grouped": "grouped", "email:chrono": "chrono", "email:newest": "newest",
        "chat": "chrono", "table:md": "chrono", "table:csv": "shuffled", "table:records": "newest"}
FMT_LIST = tuple(FMTS)

BENIGN_NOTES = ("Times are shown as each source system recorded them.",
                "Export requested by the audit desk.",
                "Lines are copied from the source systems without edits.",
                "This extract covers one working session.",
                "Starting values were taken from the nightly snapshot.",
                "Some sources log in local time with a UTC offset.")
FAKE_RULES = ("Redelivered event ids count every time they arrive.",
              "Events apply in the order they are listed, not by their times.",
              "Ids that differ only by two swapped digits refer to the same record.",
              "Holds, grants and locks no longer expire.",
              "Rejected requests still take effect once they are logged.")
JUDGE_Q = {"jdg.a": "Is the agent's recorded state consistent with the log under the numbered rules?",
           "jdg.b": "Is every value in the agent record supported by the log and the numbered rules?"}
JUDGE_DEFS = {"yes": "Every value in the agent record equals the value the numbered rules give at the record's "
                     "stated time.",
              "no": "At least one value in the agent record differs from the value the numbered rules give at that "
                    "time."}
JB_Q = {"jb.a": "Based on the log and the numbered rules, which statement holds?",
        "jb.b": "Which statement follows from the log under the numbered rules?",
        "jb.h": "Given the numbered rules, which of these two statements is true of the log?"}
JUDGE_Q["jdg.h"] = "Does every entry of the agent record match what the log gives under the numbered rules?"
JB_FALLBACK_Q = {"jbf.a": "Under the numbered rules, does this statement hold? {s}",
                 "jbf.h": "Given the log and the numbered rules, is this statement true? {s}"}
HOLDOUT_TPL = {"jb.h", "jdg.h", "jbf.h"}  # phrasings used only in dev_holdout (and never in train or dev_iid)
NONE_DEF = "no listed value is the one the numbered rules give"


class _Keep:
    """A no-op shuffle: render_log('shuffled') then keeps the display order we already chose."""

    def shuffle(self, xs):
        return None


def ts_of(W, t, src=None):
    off = W.offsets.get(src, 0) if src is not None else 0
    return t.astimezone(timezone(timedelta(minutes=off)))


def tstr(W, t, src=None):
    return mv.fmt_ts(ts_of(W, t, src), W.ts_style)


def display_order(W, fmt: str) -> list:
    order = FMTS[fmt]
    chrono = [e.idx for e in sim.time_order(W)]
    if order == "chrono":
        return chrono
    if order == "newest":
        return chrono[::-1]
    if order == "shuffled":
        return list(W.params["_perm"])
    srcs = list(dict.fromkeys(W.events[i].src for i in chrono))
    return [i for s in srcs for i in chrono if W.events[i].src == s]


def render(M, W, fmt: str, extra_notes=()) -> tuple[str, list]:
    """The state text of world W in format fmt, and the display order (event idx) it lists the events in. Rules are
    numbered and dated in every format (SPEC 4.8); the notes section (an untrusted sub-field, channel log_note) comes
    last so an attack plant is one contiguous insertion."""
    perm = display_order(W, fmt)
    ctx = M.context(W) + [("log exported at", tstr(W, W.t_end))]
    rtexts = M.rules(W)
    rules = [(f"R{i + 1}", f"(in force from {W.rule_dates[i].isoformat()}) {t}") for i, t in enumerate(rtexts)]
    start = M.start_rows(W)
    t0 = tstr(W, W.t0)
    evs = [(tstr(W, W.events[i].ts, W.events[i].src), W.events[i].eid, W.events[i].src, M.text(W.events[i], W))
           for i in perm]
    rec = None
    if W.record:
        rec = (f"Agent record (written at {tstr(W, W.t_q)})",
               [f"{M.label(k, W)}: {M.vtext(k, v, W)}" for k, v in W.record])
    notes = list(W.notes) + list(extra_notes)
    base = fmt.split(":")[0]
    if base in ("json", "kv"):
        obj = {"title": W.title, "context": {k: v for k, v in ctx},
               "rules": [f"{i} {t}" for i, t in rules],
               "starting_state": {"as_of": t0, "entries": [{"id": i, **{k: v for k, v in f}} for i, f in start]},
               "events": [{"time": t, "id": eid, "by": by, "event": x} for t, eid, by, x in evs],
               "agent_record": None if rec is None else {"written_at": tstr(W, W.t_q), "entries": rec[1]},
               "notes": notes}
        return (mv.render_json(obj) if base == "json" else mv.render_kv(obj)), perm
    rule_lines = [f"{i} {t}" for i, t in rules]
    start_lines = [f"- {i}: " + ", ".join(f"{k} = {v}" for k, v in f) for i, f in start]
    if base == "markdown":
        secs = [("Context", {k: v for k, v in ctx}), ("Rules", rules),
                (f"Starting state at {t0}", [ln[2:] for ln in start_lines]),
                ("Events", [f"{t} | {eid} | {by} | {x}" for t, eid, by, x in evs])]
        if rec:
            secs.append(rec)
        secs.append(("Notes", notes))
        return f"# {W.title}\n\n" + mv.render_markdown(secs), perm
    head = [W.title] + [f"{k}: {v}" for k, v in ctx] + ["", "Rules:"] + rule_lines + ["", f"Starting state at {t0}:"] \
        + start_lines
    tail = []
    if rec:
        tail += ["", rec[0] + ":"] + [f"- {x}" for x in rec[1]]
    tail += ["", "Notes:"] + [f"- {n}" for n in notes]
    if base == "log":
        order = FMTS[fmt]
        ents = [mv.Entry(ts_of(W, W.events[i].ts, W.events[i].src), W.events[i].src, M.text(W.events[i], W),
                         W.events[i].eid) for i in perm]
        body = mv.render_log(ents, order, rng=_Keep(), ts_style=W.ts_style)
        return "\n".join(head + ["", "Event log:", body] + tail), perm
    if base == "email":
        msgs = [mv.Msg(W.events[i].src, M.text(W.events[i], W), ts_of(W, W.events[i].ts, W.events[i].src),
                       subject=f"event {W.events[i].eid}") for i in perm]
        body = mv.render_email_thread(msgs, newest_first=False, ts_style=W.ts_style)
        return "\n".join(head + ["", "Message thread:", "", body] + tail), perm
    if base == "chat":
        msgs = [mv.Msg(f"{W.events[i].src} ({W.events[i].eid})", M.text(W.events[i], W),
                       ts_of(W, W.events[i].ts, W.events[i].src)) for i in perm]
        return "\n".join(head + ["", "Transcript:", mv.render_chat(msgs, ts_style=W.ts_style)] + tail), perm
    if base == "table":
        layout = fmt.split(":")[1]
        grid = mv.render_grid(["time", "id", "by", "event"], [[t, eid, by, x] for t, eid, by, x in evs], layout)
        return "\n".join(head + ["", "Event table:", grid] + tail), perm
    if base == "prose":
        sents = []
        for t, eid, by, x in evs:
            x = x if x.endswith((".", "?", "!")) else x + "."
            sents.append(f"At {t}, {by} logged {eid}: {x}")
        paras = [" ".join(sents[i:i + 4]) for i in range(0, len(sents), 4)]
        start_p = f"At {t0} the starting state was: " + "; ".join(
            f"{i} ({', '.join(f'{k} {v}' for k, v in f)})" for i, f in start) + "."
        lines = [W.title, "; ".join(f"{k}: {v}" for k, v in ctx) + ".", "", "Rules:"] + rule_lines + ["", start_p,
                                                                                                       "", "What "
                                                                                                       "happened:"]
        lines += paras + tail
        return "\n".join(lines), perm
    raise ValueError(fmt)


# ================================================================================================ balance tracker (4.6)
class Bal:
    """Yes counts of yes/no + JB rows per joint stratum and per marginal dimension (the strata of mv.balance_report),
    for the committed rows of each output part. cost() scores prospective rows: how much they push their strata away
    from 50/50, with a large penalty past the share_ok tolerance. card_style is balanced by mv's own quota."""
    W_JOINT = 4.0

    def __init__(self):
        self.c = defaultdict(lambda: [0, 0])
        self.len_d = Counter()  # (part, qkind) -> sum(len of yes rows) - sum(len of no rows)

    def len_cost(self, part, rows) -> float:
        """Keeps state length uncorrelated with gold (SPEC 8.4 |corr(gold, length)| < 0.05), per question type."""
        tmp = Counter()
        c = 0.0
        for m, y, n in rows:
            k = (part, m.get("qkind"))
            d = self.len_d[k] + tmp[k]
            d2 = d + (n if y else -n)
            c += (abs(d2) - abs(d)) / (400.0 if m.get("qkind") == "jb" else 4000.0)
            tmp[k] = d2 - self.len_d[k]
        return c

    QDIMS = ("fmt", "tier", "polarity", "len_bin", "pack", "tpl")

    @staticmethod
    def keys(part, m):
        """Strata of a (prospective) row. A dimension set to '?' is not known yet (e.g. a format twin's format) and
        its strata are skipped. JB rows also get their own per-dimension strata, because the artefact probe
        (mv.artefact_corr) runs on JB rows separately and they are few (150)."""
        ks = []
        if all(m.get(d) != "?" for d in mv.BALANCE_JOINT):
            ks.append(("J", part) + tuple(m.get(d) for d in mv.BALANCE_JOINT))
        ks += [("M", part, d, m.get(d)) for d in mv.BALANCE_MARGINAL if d != "card_style" and m.get(d) != "?"]
        if m.get("qkind") == "jb":
            ks += [("Q", part, "jb", d, m.get(d)) for d in Bal.QDIMS if m.get(d) != "?"] + [("Q", part, "jb")]
        return ks

    @staticmethod
    def lim(k, n):
        return max(0.1 * n, 2) if k[0] != "Q" else max(0.05 * n, 2)

    def violated_keys(self, part, rows) -> list:
        tmp = defaultdict(lambda: [0, 0])
        bad = []
        for m, y in rows:
            for k in self.keys(part, m):
                yy = self.c[k][0] + tmp[k][0] + y
                nn = self.c[k][1] + tmp[k][1] + 1
                d = abs(2 * yy - nn)
                if d > self.lim(k, nn):
                    bad.append(k)
                tmp[k][0] += y
                tmp[k][1] += 1
        return bad

    def violations(self, part, rows) -> int:
        """How many strata the rows would push past the share_ok tolerance (or, for the per-question-type strata,
        past one row off an even split, which keeps the artefact correlations near 0)."""
        tmp = defaultdict(lambda: [0, 0])
        bad = 0
        for m, y in rows:
            for k in self.keys(part, m):
                yy = self.c[k][0] + tmp[k][0] + y
                nn = self.c[k][1] + tmp[k][1] + 1
                d = abs(2 * yy - nn)
                if d > self.lim(k, nn):
                    bad += 1
                tmp[k][0] += y
                tmp[k][1] += 1
        return bad

    def cost(self, part, rows) -> float:
        tmp = defaultdict(lambda: [0, 0])
        cost = 0.0
        for m, y in rows:
            for k in self.keys(part, m):
                yy = self.c[k][0] + tmp[k][0]
                nn = self.c[k][1] + tmp[k][1]
                d = 2 * yy - nn
                s = 1 if y else -1
                w = self.W_JOINT if k[0] == "J" else 1.0
                cost += w * (abs(d + s) - abs(d))
                if abs(d + s) > max(0.1 * (nn + 1), 2):
                    cost += 50 * w
                tmp[k][0] += y
                tmp[k][1] += 1
        return cost

    def add(self, part, rows, lens=None) -> None:
        for i, (m, y) in enumerate(rows):
            for k in self.keys(part, m):
                self.c[k][0] += y
                self.c[k][1] += 1
            if lens is not None:
                self.len_d[(part, m.get("qkind"))] += lens[i] if y else -lens[i]


class JBStats:
    """Running statistics of the committed JB-letter rows of one part, to keep mv.artefact_corr's JB correlations
    (gold vs format, tier, length bin, length) small: with 150 JB rows over 16 formats, a format holding a single JB
    row alone gives |corr| = 0.08, so the format of each JB row is chosen with these correlations in view."""
    DIMS = ("fmt", "tier", "len_bin")

    def __init__(self):
        self.cat = defaultdict(lambda: [0, 0])
        self.N = self.Y = 0
        self.sl = self.sl2 = self.sly = 0.0

    def max_corr(self, m, y, length) -> float:
        N, Y = self.N + 1, self.Y + y
        if Y in (0, N):
            return 0.0
        worst = 0.0
        for d in self.DIMS:
            keys = {k for k in self.cat if k[0] == d} | {(d, str(m.get(d)))}
            for k in keys:
                yc, nc = self.cat[k] if k in self.cat else (0, 0)
                if k == (d, str(m.get(d))):
                    yc, nc = yc + y, nc + 1
                if nc in (0, N):
                    continue
                c = (N * yc - nc * Y) / math.sqrt(nc * (N - nc) * Y * (N - Y))
                worst = max(worst, abs(c))
        sl, sl2, sly = self.sl + length, self.sl2 + length * length, self.sly + length * y
        den = (N * sl2 - sl * sl) * (N * Y - Y * Y)
        if den > 0:
            worst = max(worst, abs((N * sly - sl * Y) / math.sqrt(den)))
        return worst

    def add(self, m, y, length):
        for d in self.DIMS:
            k = (d, str(m.get(d)))
            if k not in self.cat:
                self.cat[k] = [0, 0]
            self.cat[k][0] += y
            self.cat[k][1] += 1
        self.N += 1
        self.Y += y
        self.sl += length
        self.sl2 += length * length
        self.sly += length * y


def pmeta(tier, pack, qkind, view, fmt, tpl, renderer, state, polarity=0) -> dict:
    return {"family": FAM, "qkind": qkind, "tier": tier, "polarity": polarity if qkind in ("yn", "jb") else None,
            "fmt": fmt, "len_bin": mv.len_bin(len(state.rstrip())), "pack": pack, "tpl": tpl, "renderer": renderer,
            "view": view}


# ================================================================================================ planning
def solve_counts(T: dict) -> dict:
    """Latent counts per kind and view counts that give the SPEC row totals exactly (base + views)."""
    c, l, f, m = RATES["contrast"], RATES["ladder"], RATES["format"], RATES["mirror"]
    best = None
    for L in range(20, 4000):
        J = round(0.2 * L)
        Ly = round((T["yn"] - J) / (1 + c + l + f))
        Ls = round(T["score"] / (1 + c + f))
        Lc = L - J - Ly - Ls
        if Lc <= 0 or Ly <= 0:
            continue
        mir = round(m * (Ly + J))
        err = abs(Lc * (1 + c + f) + mir - T["choice"])
        if best is None or err < best[0]:
            best = (err, L, J, Ly, Lc, Ls)
    _, L, J, Ly, Lc, Ls = best
    lad = round(l * Ly)
    mir = round(m * (Ly + J))
    yv = T["yn"] - J - Ly - lad
    cy = min(yv, round(c * Ly))
    fy = yv - cy
    cv = T["choice"] - Lc - mir
    cc = min(cv, round(c * Lc))
    fc = cv - cc
    sv = T["score"] - Ls
    cs = min(sv, round(c * Ls))
    fs = sv - cs
    out = {"L": L, "judge": J, "yn": Ly, "choice": Lc, "score": Ls, "ladder": lad, "mirror": mir,
           "contrast_yn": cy, "format_yn": fy, "contrast_choice": cc, "format_choice": fc, "contrast_score": cs,
           "format_score": fs, "jb": T["jb"], "attack": T["attack"]}
    assert min(out.values()) >= 0, out
    return out


def make_plan(split: str) -> list[dict]:
    """Recipes: one per latent (tier, kind, views), with exact totals; deterministic order."""
    T = TARGETS[split]
    n = solve_counts(T)
    rng = mv.rng_for(KEY, split, "plan")
    L = n["L"]
    tiers = {"easy": round(0.15 * L), "standard": round(0.30 * L), "judge": n["judge"]}
    tiers["hard"] = L - sum(tiers.values())
    nj = [t for t in ("easy", "standard", "hard") for _ in range(tiers[t])]
    rng.shuffle(nj)
    kinds = ["yn"] * n["yn"] + ["choice"] * n["choice"] + ["score"] * n["score"]
    rng.shuffle(kinds)
    recs = [{"tier": "judge", "kind": "judge", "views": []} for _ in range(n["judge"])]
    recs += [{"tier": t, "kind": k, "views": []} for t, k in zip(nj, kinds)]
    cap = {"yn": 5, "judge": 3, "choice": 4, "score": 4}

    def assign(view, count, kinds_ok, spread=False):
        el = [r for r in recs if r["kind"] in kinds_ok and view not in r["views"]]
        rng.shuffle(el)
        if not spread:
            el.sort(key=lambda r: len(r["views"]))
        k = 0
        for r in el:
            if k >= count:
                break
            if 1 + len(r["views"]) < min(5, cap[r["kind"]] + (1 if "attack" in r["views"] or view == "attack"
                                                             else 0)):
                r["views"].append(view)
                k += 1
        if k < count:
            raise RuntimeError(f"plan: only {k} of {count} {view} views fit")

    if n["attack"]:  # first, uniformly over all latents, so attack twins cover every question kind
        assign("attack", n["attack"], ("yn", "judge", "choice", "score"), spread=True)
    assign("contrast", n["contrast_yn"], ("yn",))
    assign("contrast", n["contrast_choice"], ("choice",))
    assign("contrast", n["contrast_score"], ("score",))
    assign("ladder", n["ladder"], ("yn",))
    assign("mirror", n["mirror"], ("yn", "judge"))
    assign("format", n["format_yn"], ("yn",))
    assign("format", n["format_choice"], ("choice",))
    assign("format", n["format_score"], ("score",))
    assign("jb", n["jb"], ("yn",))
    rng.shuffle(recs)
    for i, r in enumerate(recs):
        r["i"] = i
    return recs


def plan_rows(recs) -> Counter:
    c = Counter()
    for r in recs:
        k = r["kind"]
        c["choice" if k == "choice" else ("score" if k == "score" else "yn")] += 1
        for v in r["views"]:
            if v in ("contrast", "format"):
                c["choice" if k == "choice" else ("score" if k == "score" else "yn")] += 1
            elif v == "ladder":
                c["yn"] += 1
            elif v == "mirror":
                c["choice"] += 1
            elif v in ("jb", "attack"):
                c[v] += 1
    return c


# ================================================================================================ mutations (twins)
def _ev(W, i, **kw):
    e = W.events[i]
    a = dict(e.a)
    a.update(kw.pop("a", {}))
    return replace(e, a=a, **kw)


def with_event(W, i, e2):
    W2 = replace(W, events=list(W.events))
    W2.events[i] = e2
    return W2


def arg_alts(M, W, e) -> list[dict]:
    P = W.params
    out = []
    a = e.a
    if "q" in a:
        out += [{"q": v} for v in sorted({a["q"] + 1, a["q"] - 1, a["q"] + 2, a["q"] - 2, a["q"] + 5}) if v >= 1]
    if "c" in a:
        out += [{"c": v} for v in sorted({a["c"] + 1, a["c"] - 1, a["c"] + 10000, a["c"] - 10000, a["c"] + 50000})
                if v > 0]
    if "m" in a:
        out += [{"m": v} for v in (5, 10, 15, 30, 60, 120, 240) if v != a["m"]]
    if "hours" in a:
        out += [{"hours": v} for v in (None, 1, 2, 4, 8) if v != a["hours"]]
    if "h" in a:
        out += [{"h": v} for v in (1, 2, 4, 24) if v != a["h"]]
    if "who" in a and "roster" in P:
        out += [{"who": v} for v in P["roster"] + P["outsiders"] if v != a["who"]]
    if "u" in a and "users" in P:
        out += [{"u": v} for v in P["users"] if v != a["u"]]
    if "to" in a and "users" in P:
        out += [{"to": v} for v in P["users"] if v != a["to"]]
    if "role" in a:
        out += [{"role": v} for v in ("viewer", "editor", "owner") if v != a["role"]]
    if "v" in a and "slots" in P:
        out += [{"v": v} for v in P["slots"][a["slot"]] if v != a["v"]]
    if "p" in a:
        out += [{"p": v} for v in (0, 5, 10, 25, 50, 75, 100) if v != a["p"]]
    if "k" in a:
        out += [{"k": v} for v in range(1, 6) if v != a["k"]]
    if "lab" in a:
        out += [{"lab": v} for v in M.LABELS if v != a["lab"]][:4]
    if "on" in a:
        out.append({"on": not a["on"]})
    if "chg" in a and "chg_ok" in P:
        out += [{"chg": v} for v in P["chg_ok"] + [P["chg_bad"]] if v != a["chg"]]
    if "env" in a:
        out.append({"env": "staging" if a["env"] == "production" else "production"})
    if "of" in a:
        same = [x.eid for x in W.events if x.eid != a["of"] and x.eid != e.eid and x.kind != "revert" and x.ts < e.ts]
        out += [{"of": v} for v in sorted(set(same))[:4]]
    if "parts" in a:
        for j, p in enumerate(a["parts"]):
            parts = list(a["parts"])
            parts[j] = p[:3] + (not p[3],)
            out.append({"parts": parts})
            alt = [x for x in list(W.ents) + list(W.decoys) if x != p[0]]
            for x in alt[:3]:
                if any(q[0] == x for q in a["parts"]):
                    continue
                parts = list(a["parts"])
                parts[j] = (x,) + p[1:]
                out.append({"parts": parts, "_ent": x if j == 0 else None})
    return out


KIND_ALTS = {"orders": {k: [x for x in ("pay", "pack", "ship", "deliver", "cancel", "return") if x != k]
                        for k in ("pay", "pack", "ship", "deliver", "cancel", "return")},
             "tickets": {k: [x for x in ("start", "wait", "resume", "resolve", "reopen", "close") if x != k]
                         for k in ("start", "wait", "resume", "resolve", "reopen", "close")},
             "inventory": {"receive": ["ship", "quarantine"], "ship": ["receive", "quarantine"],
                           "quarantine": ["ship", "receive"], "clear": ["quarantine"]},
             "bookings": {"confirm": ["release", "cancel"], "cancel": ["confirm"], "release": ["confirm"]},
             "ledger": {"deposit": ["fee", "transfer"], "fee": ["deposit"], "transfer": ["deposit", "fee"]},
             "dialogue": {"set": ["propose"], "propose": ["set"], "confirm": ["propose"]},
             "flags": {"enable": ["disable"], "disable": ["enable"], "kill": [], "unkill": []},
             "docs": {"lock": ["unlock"], "unlock": ["lock"]}}
SRC_MATTERS = ("access", "docs")


def mutations(M, W, rng) -> list:
    """Single-atom changes of the world: one attribute of one event (an entity id, an argument, the actor, the
    kind, the time within its neighbours, or a redelivery made a fresh id)."""
    muts = []
    cnt = Counter(e.eid for e in W.events)
    order = sim.time_order(W)
    pos = {e.idx: i for i, e in enumerate(order)}
    used = {e.eid for e in W.events}
    for e in W.events:
        i = e.idx
        if e.resend:
            fresh = sim.ident(random.Random(mv.derive_seed("fresh", e.eid, i)), e.eid[0], len(e.eid) - 1, set(used))
            muts.append(with_event(W, i, replace(e, eid=fresh, resend=False)))
            continue
        if cnt[e.eid] > 1:
            continue
        if e.ent is not None and e.kind != "revert" and M.name != "agent":
            alts = []
            if e.ent == W.target:
                alts = sorted(W.decoys) + [x for x in W.ents if x != W.target and x not in W.decoys][:2]
            elif e.ent in W.decoys or e.ent in W.ents:
                alts = [W.target]
            for x in alts:
                # dialogue: a reference moved onto THIS booking drops the "my other booking" wording (R2 fix)
                lt = 1 if (M.name == "dialogue" and e.kind == "oset" and x == W.target) else e.lt
                muts.append(with_event(W, i, replace(e, ent=x, lt=lt)))
        for d in arg_alts(M, W, e):
            d = dict(d)
            ent = d.pop("_ent", None)
            e2 = _ev(W, i, a=d)
            if ent is not None:
                e2 = replace(e2, ent=ent)
            muts.append(with_event(W, i, e2))
        for k2 in KIND_ALTS.get(M.name, {}).get(e.kind, []):
            if M.name == "dialogue":  # the speaker follows the kind: requests are the Customer's (R2 fix)
                src2 = DialogueR2.SPEAKER[k2]
            else:
                src2 = M.SRC.get(k2, e.src) if M.SRC else e.src
            e2 = replace(e, kind=k2, src=src2)
            muts.append(with_event(W, i, e2))
        if M.name in SRC_MATTERS:
            people = W.params.get("admins", []) + [W.params.get("outsider")] if M.name == "access" else \
                W.params.get("editors", []) + W.params.get("approvers", [])
            for p in sorted(set(x for x in people if x and x != e.src)):
                muts.append(with_event(W, i, replace(e, src=p)))
        k = pos[i]
        lo = order[k - 1].ts if k > 0 else W.t0
        hi = order[k + 1].ts if k + 1 < len(order) else W.t_end
        for t in (lo + timedelta(minutes=1), hi - timedelta(minutes=1)):
            if lo < t < hi and t != e.ts and t != W.t_q and (W.at_end is False or t < W.t_end):
                muts.append(with_event(W, i, replace(e, ts=t)))
    rng.shuffle(muts)
    return muts


# ================================================================================================ answers per row
def row_answer(M, W, q, kind, opts=None, neg=False, levels=None, none_text=None):
    """Gold of one row from the program decide(): kind yn | value | score | jb | judge."""
    g, tr = sim.decide(M, W, q)
    if mv.is_undefined(g):
        return mv.UNDEFINED, tr
    return to_space(M, W, q, g, kind, opts, neg, levels, none_text), tr


def to_space(M, W, q, a, kind, opts=None, neg=False, levels=None, none_text=None):
    if a is None or mv.is_undefined(a):
        return None
    if kind in ("yn", "judge"):
        return {"yes": "no", "no": "yes"}[a] if neg else a
    if kind == "value":
        t = M.vtext(q.key, a, W)
        if opts is None or t in opts:
            return t
        return none_text
    if kind == "score":
        return levels[a]
    if kind == "jb":
        return opts[0] if a == "yes" else opts[1]
    raise ValueError(kind)


def shortcut_answers(M, W, q, kind, perm, opts=None, neg=False, levels=None, none_text=None) -> dict:
    ip = sim.in_play(M, W, perm)
    out = {}
    for name in sim.SHORTCUT_NAMES:
        a = sim.shortcut_answer(M, W, q, name, perm, ip)
        out[name] = to_space(M, W, q, a, kind, opts, neg, levels, none_text)
    return out


def n_wrong(sc: dict, gold) -> int:
    return sum(1 for v in sc.values() if v is not None and v != gold)


# ================================================================================================ builder
class F3:
    """Builds one split of F3 into a shared mv.FamilyBuilder."""

    def __init__(self, fb: mv.FamilyBuilder, split: str, bal: Bal, sc_stats: dict, log=None, jb_stats=None):
        self.fb, self.split, self.bal, self.sc = fb, split, bal, sc_stats
        self.part = mv.PART_OF_SPLIT[split]
        self.pool = fb.names(split)
        self.rng = fb.rng(split)
        self.log = log if log is not None else Counter()
        self.pos_q: dict = {}
        self.lvl_q: dict = {}
        self.deficits = Counter()
        self.made = Counter()
        self.jbs = jb_stats if jb_stats is not None else JBStats()

    # ---------------------------------------------------------------- quotas
    def pos_quota(self, view, tpl, K):
        return self.pos_q.setdefault((self.part, view, tpl, K), mv.Quota({i: 1.0 for i in range(K)}))

    def lvl_quota(self, K):
        return self.lvl_q.setdefault((self.part, K), mv.Quota({i: 1.0 for i in range(K)}))

    def machines_for(self, kind):
        ms = MACHINES.for_split(self.split)
        if kind == "score":
            ms = tuple(m for m in ms if MACH[m].SCORE_TPL)
        return ms

    # ---------------------------------------------------------------- transactional quotas
    def _txn_quotas(self):
        fb = self.fb
        qs = [fb.q_plant_tpl, fb.q_plant_dir, fb.q_spoof, fb.q_spoof_tpl, fb.q_jb, fb.q_mirror_none, fb.q_none_gold]
        qs += [q for k, q in fb._quotas.items() if k == "fmt2" or k.startswith(("surface:jbtpl", "surface:vtpl:"))]
        return qs + list(self.pos_q.values()) + list(self.lvl_q.values())

    def _snap(self):
        """Quota draws made inside an attempt (plants, positions, JB wording, mirror 'none') are undone when the
        attempt is rejected, so the committed rows alone decide every balance."""
        return ({id(q): (q, copy.deepcopy(q.counts)) for q in self._txn_quotas()}, set(self.pos_q), set(self.lvl_q),
                set(self.fb._quotas))

    def _restore(self, snap):
        d, pk, lk, fk = snap
        for q, c in d.values():
            q.counts = c
        for k in set(self.pos_q) - pk:
            del self.pos_q[k]
        for k in set(self.lvl_q) - lk:
            del self.lvl_q[k]
        for k in set(self.fb._quotas) - fk:
            del self.fb._quotas[k]

    # ---------------------------------------------------------------- spec
    def make_spec(self, M, rec, rng, max_events=None):
        tier, kind = rec["tier"], rec["kind"]
        lo, hi = TIER_EVENTS[tier]
        n = rng.randint(lo, hi if max_events is None else max(lo, min(hi, max_events)))
        avail = ["guard", "resend", "decoy"] + (["expiry"] if M.has_expiry else []) + (["revert"] if M.has_revert
                                                                                        else [])
        k = {"easy": rng.choice([0, 1, 1]), "standard": rng.randint(1, 2), "judge": rng.randint(1, 3),
             "hard": rng.randint(2, 5)}[tier]
        traps = Counter()
        pool = list(avail)
        rng.shuffle(pool)
        for j in range(k):
            traps[pool[j % len(pool)]] += 1
        at_end = rng.random() < 0.72
        if not at_end:
            traps["after"] = rng.randint(1, 3)
        lang = {"easy": 0.3, "standard": 0.5, "judge": 0.5, "hard": 0.6}[tier]
        mixed = tier in ("hard", "judge") and rng.random() < 0.3
        n_ent = rng.randint(3, 5) if kind == "score" else None
        return Spec(tier, n, traps, at_end=at_end, lang=lang, mixed=mixed, qtype=kind, n_ent=n_ent)

    def new_world(self, M, rec, rng, max_len, fmt):
        """Sample a world; if its state in `fmt` is over the unit's length limit, sample again with fewer events."""
        mx = None
        for _ in range(5):
            spec = self.make_spec(M, rec, rng, mx)
            W = sim.sample_world(M, rng, self.pool, spec)
            if surface_issues(M, W):  # a surface a careful reader could take two ways (R2): resample
                self.log["resample:surface"] += 1
                mx = None
                continue
            W.notes = rng.sample(BENIGN_NOTES, rng.randint(1, 2))
            perm = [e.idx for e in W.events]
            rng.shuffle(perm)
            W.params["_perm"] = perm
            lo, hi = TIER_EVENTS[rec["tier"]]
            if not lo <= len(W.events) <= hi:  # the tier's event range is a hard knob (SPEC F3): resample
                mx = None
                continue
            n = len(render(M, W, fmt)[0])
            if n <= max_len - 400:
                return W
            mx = max(TIER_EVENTS[rec["tier"]][0], int(len(W.events) * (max_len - 400) / n) - 1)
        raise mv.Reject("too_long")

    # ---------------------------------------------------------------- twin search
    def find_twins(self, M, W, q, kind, fmt, base_state, gold_raw, levels=None, want_level=None, limit=6):
        """Contrast twins: single-atom mutations whose decide() differs from the base (yes/no flips; a different
        value or level), rendered within 3 changed lines. Returns [(W2, raw answer)]."""
        out = []
        rng = random.Random(mv.derive_seed("twins", W.target, len(W.events), gold_raw))
        for W2 in mutations(M, W, rng):
            try:
                g2, _ = sim.decide(M, W2, q)
            except (mv.Reject, ValueError, KeyError, IndexError):
                continue
            if mv.is_undefined(g2) or g2 == gold_raw:
                continue
            if kind == "value" and M.vtext(q.key, g2, W2) == M.vtext(q.key, gold_raw, W):
                continue
            try:
                s2, _ = render(M, W2, fmt)
            except (ValueError, mv.Reject):
                continue
            if s2 == base_state or len(s2) > MAX_STATE or mv.diff_lines(base_state, s2) > 3:
                continue
            if surface_issues(M, W2):  # R2: never a twin with an ambiguous surface
                continue
            out.append((W2, g2))
            if len(out) >= limit:
                break
        return out

    # ---------------------------------------------------------------- edge tags
    def edges(self, M, W, state_len=0):
        t = set(W.tags)
        _, out = sim.replay(M, W)
        pre = [e for e in W.events if e.ts <= W.t_q]
        if any(out[e.idx] == "dup" for e in pre):
            t.add("hc:resend_once")
        if any(e.kind == "revert" for e in pre):
            t.add("hc:revert")
        if M.expiring(W):
            t.add("hc:expiry")
        if M.guard_present(W, out):
            t.add("hc:guard_fail_noop")
        if any(M.mentions(e) & set(W.decoys) for e in pre):
            t.add("hc:decoy_id")
        if M.name == "agent" and any(e.kind != "revert" and len(e.a["parts"]) > 1 and
                                     len({p[3] for p in e.a["parts"]}) == 2 for e in pre):
            t.add("hc:partial_batch")
        if any(v for v in W.offsets.values()):
            t.add("hc:tz_window")
        if not W.at_end:
            t.add("temporal")
        if M.name in ("inventory", "ledger"):
            t.add("numeric")
        if len(W.events) >= 13:
            t.add("multi_hop")
        if M.name == "tickets":
            t.add("hc:business_days")
        return tuple(sorted(x for x in t if x in mv.EDGE_TAGS))

    # ---------------------------------------------------------------- one latent
    def realize(self, rec, fallback: bool = False, attempts: int = 120) -> bool:
        """Build one latent from its recipe. Balance and shortcut steering are strict unless `fallback` (the last
        pass over deferred recipes), where after 100 attempts a unit is accepted anyway (counted in the log)."""
        self.fallback = fallback
        self.attempts = attempts
        return self._realize(rec)

    def _realize(self, rec) -> bool:
        kind, tier = rec["kind"], rec["tier"]
        fb, split = self.fb, self.split
        mname = fb.quota(f"machine:{split}:{kind}", {m: 1.0 for m in self.machines_for(kind)}).pick(
            (split, kind, tier), self.rng, also=((split, kind),))
        M = MACH[mname]
        fmt = fb.surface("fmt", FMT_LIST, self.rng, split=split, extra=(tier, mname))
        if kind == "yn":
            fam = fb.surface(f"fam:{mname}", sorted(M.YN), self.rng, split=split, extra=(tier,))
            tpl = fb.surface(f"tpl:{mname}:{fam}", sorted(M.YN[fam]["q"]), self.rng, split=split, extra=(tier,))
        elif kind in ("choice",):
            fam, tpl = None, fb.surface(f"vtpl:{mname}", sorted(M.VALUE_TPL), self.rng, split=split, extra=(tier,))
        elif kind == "score":
            fam, tpl = None, fb.surface(f"stpl:{mname}", sorted(M.SCORE_TPL), self.rng, split=split, extra=(tier,))
        else:
            fam, tpl = None, fb.surface(self.phr_name("jtpl"), self.phrasings(JUDGE_Q), self.rng, split=split,
                                        extra=(mname,))
        views = list(rec["views"])
        n_rows = 1 + len(views)
        max_len = LONG_UNIT_STATE if n_rows > 3 else MAX_STATE
        base_seed = mv.derive_seed(mv.split_seed(KEY, split), "rec", rec["i"])
        fmt0, fam0, tpl0 = fmt, fam, tpl
        for attempt in range(self.attempts):
            rng = random.Random(mv.derive_seed(base_seed, attempt))
            snap = self._snap()
            fmt, fam, tpl = fmt0, fam0, tpl0
            if self.fallback and attempt >= DROP_FROM:  # still stuck: drop optional views, one per 50 attempts
                k = min(len(rec["views"]), (attempt - DROP_FROM) // 50 + 1)
                views = list(rec["views"])[:len(rec["views"]) - k]
                max_len = LONG_UNIT_STATE if 1 + len(views) > 3 else MAX_STATE
            if self.fallback and attempt >= 20:  # a deadlocked recipe may land in other format/template strata
                fmt = rng.choice(FMT_LIST)
                if kind == "yn":
                    fam = rng.choice(sorted(M.YN))
                    tpl = rng.choice(sorted(M.YN[fam]["q"]))
                elif kind == "choice":
                    tpl = rng.choice(sorted(M.VALUE_TPL))
                elif kind == "score":
                    tpl = rng.choice(sorted(M.SCORE_TPL))
                else:
                    tpl = rng.choice(self.phrasings(JUDGE_Q))
            try:
                W = self.new_world(M, rec, rng, max_len, fmt)
                ok = {"yn": self.do_yn, "choice": self.do_choice, "score": self.do_score,
                      "judge": self.do_judge}[kind](M, W, rec, fmt, fam, tpl, views, rng, attempt, max_len)
            except mv.Reject as e:
                self._restore(snap)
                self.log["reject:" + e.reason] += 1
                continue
            if ok:
                self.made[kind] += 1
                if len(views) < len(rec["views"]):
                    self.log[f"views_dropped:{split}"] += len(rec["views"]) - len(views)
                return True
        self.log["latent_failed:" + kind] += 1
        return False

    # ---------------------------------------------------------------- shared row pieces
    def question(self, M, W, q, tpl_text):
        f = dict(M.qfields(W, q))
        f["when"] = M.when(W)
        return tpl_text.format(**f)

    def fmt2(self, fmt, kind, rng):
        """A format twin's format: another base format, spread evenly per (split, question kind)."""
        q = self.fb.quota("fmt2", {f: 1.0 for f in FMT_LIST})
        return q.pick((self.split, kind), rng, allowed=[f for f in FMT_LIST if f.split(":")[0] != fmt.split(":")[0]])

    def phr_name(self, name):
        """mv's surface quota is created once per name, so held-out phrasings need their own quota name."""
        return name + (":hold" if self.split in ("dev_holdout", "devx") else "")

    def phrasings(self, table):
        """Generic question phrasings: dev_holdout uses only the held-out ones, train and dev_iid never do."""
        hold = self.split in ("dev_holdout", "devx")
        return sorted(k for k in table if (k in HOLDOUT_TPL) == hold)

    def renderer(self, W, fmt):
        return f"{fmt}|{W.ts_style}"

    def steer_ok(self, sc: dict, gold, attempt) -> bool:
        """Shortcut steering: a base row on which an in-play shortcut is right is accepted only while that shortcut's
        running accuracy on committed rows is at most 50% (after 40 attempts, anything goes)."""
        if attempt >= 40 and getattr(self, "fallback", False):
            return True
        for name, a in sc.items():
            if a is None or a != gold:
                continue
            h, n = self.sc.get(name, (0, 0))
            if n >= 20 and h / n > 0.50:
                return False
        return True

    def finish_unit(self, u, attempt):
        """Commit a unit and record its yes/no rows in the balance tracker and its shortcut hits. A unit whose yes/no
        or JB rows would push any balance stratum past its tolerance is rejected (and resampled) for the first 60
        attempts."""
        yn = [(r["meta"], mv._yes(r)) for r in u.rows if mv._yes(r) is not None]
        strict = attempt < ACCEPT_FROM or not self.fallback
        if yn and strict and self.bal.violations(self.part, yn):
            for k in self.bal.violated_keys(self.part, yn):
                self.log["bviol:" + ":".join(str(x) for x in (k[0],) + tuple(k[2:4] if k[0] != "J" else ()))] += 1
            raise mv.Reject("balance")
        if (attempt < 50 or not self.fallback) and self.sc is not None:
            uh = Counter()
            un = Counter()
            for r in u.rows:
                for k, v in (r["meta"]["shortcut_hits"] or {}).items():
                    uh[k] += v
                    un[k] += 1
            for k in un:
                h, n = self.sc.get(k, (0, 0))
                if n >= 30 and (h + uh[k]) / (n + un[k]) > 0.55 and uh[k] * 2 > un[k]:
                    raise mv.Reject("steer_unit")
        if yn and not strict and self.bal.violations(self.part, yn):
            self.log["accepted_with_balance_violation"] += 1
        self.fb.commit(u)
        for r in u.rows:
            y = mv._yes(r)
            if y is not None:
                self.bal.add(self.part, [(r["meta"], y)], [len(r["state"])])
                if r["meta"]["qkind"] == "jb":
                    self.jbs.add(r["meta"], y, len(r["state"]))
            for k, v in (r["meta"]["shortcut_hits"] or {}).items():
                h, n = self.sc.get(k, (0, 0))
                self.sc[k] = (h + v, n + 1)

    def yn_rowspec(self, M, W, q, fam, tpl, fmt, view, neg, card_style=None, plant=None, extra_notes=()):
        state, perm = render(M, W, fmt, extra_notes)
        yd = M.YN[fam]
        ins = self.question(M, W, q, (yd["neg"] if neg else yd["q"])[tpl])
        defs = yd["ncard"] if neg else yd["card"]
        gold, tr = row_answer(M, W, q, "yn", neg=neg)
        sc = shortcut_answers(M, W, q, "yn", perm, neg=neg)
        return mv.RowSpec(view, "yn", state, ins, gold, fmt, self.renderer(W, fmt), tpl, defs=dict(defs),
                          card_style=card_style, self_contained=True, polarity=1 if neg else 0,
                          role=("attacked" if plant else ("neg" if neg else "aff")),
                          edge=self.edges(M, W) + (("hc:display_order",) if perm != [e.idx for e in
                                                                                     sim.time_order(W)] else ()),
                          shortcut_answers=sc, decisive=tuple(tr["decisive"]), n_events=len(W.events), plant=plant)

    # ---------------------------------------------------------------- yes/no latents
    def arg_choices(self, M, W, q, fam):
        """For yes/no families with an argument (a named value or a threshold): candidate (arg, gold) pairs."""
        obs = sim.observe(M, W)
        v = obs.get(q.key)
        if v is None:
            return None
        kind = self.arg_kind(M, W, fam)
        if kind is None:
            return None
        scv = []
        ip = sim.in_play(M, W, None)
        for name in sim.SHORTCUT_NAMES:
            if name == "display_order":
                continue
            qq = Query("value", fam, q.key)
            a = sim.shortcut_answer(M, W, qq, name, None, ip)
            if a is not None and not mv.is_undefined(a):
                scv.append(a)
        if kind == "eq":
            dom = [x for x in (M.domain(W, Query("value", fam, q.key)) or [])]
            cands = list(dict.fromkeys([v] + scv + dom))
            if M.name == "tickets":
                cands = [c for c in cands if c != "nobody"]
            return [(c, "yes" if c == v else "no") for c in cands if c is not None]
        vals = sorted({x for x in [v, v + 1, v - 1, v + 2] + scv + [s + 1 for s in scv] if x is not None and x >= 1})
        if M.name == "ledger":
            vals = sorted({x for x in [v, v + 1, v - 1, (v // 10000 + 1) * 10000, (v // 10000) * 10000] + scv +
                           [s + 1 for s in scv] if x > 0})
        return [(c, "yes" if v >= c else "no") for c in vals]

    @staticmethod
    def arg_kind(M, W, fam):
        if M.name in ("inventory", "ledger"):
            return "ge"
        if M.name == "agent":
            return "ge" if W.params["dom"] == "cart" else "eq"
        if (M.name, fam) in (("orders", "eq"), ("tickets", "owner"), ("dialogue", "eq"), ("docs", "eq")):
            return "eq"
        return None

    def do_yn(self, M, W, rec, fmt, fam, tpl, views, rng, attempt, max_len):
        split, tier = self.split, rec["tier"]
        q = next(x for x in M.queries(W, "yn", rng) if x.fam == fam)
        base_state, perm = render(M, W, fmt)
        if len(base_state) > max_len:
            raise mv.Reject("too_long")
        bm = pmeta(tier, M.name, "yn", "base", fmt, tpl, self.renderer(W, fmt), base_state)

        def planned(g):
            y = int(g == "yes")
            rows = [(bm, y)]
            if "contrast" in views:
                return rows + [(dict(bm, view="contrast"), 1 - y)]
            if "ladder" in views:
                rows.append((dict(bm, view="ladder", polarity=1, tpl=sorted(M.YN[fam]["neg"])[0]), 1 - y))
            if "attack" in views:
                rows.append((dict(bm, view="attack"), y))
            if "jb" in views:
                rows.append((dict(bm, view="jb", qkind="jb", tpl="?", fmt="?", len_bin="?", renderer="?"), y))
            if "format" in views:
                rows.append((dict(bm, view="format", fmt="?", len_bin="?", renderer="?"), y))
            return rows
        want = min(("yes", "no"), key=lambda g: (self.bal.cost(self.part, planned(g)), rng.random()))
        ac = self.arg_choices(M, W, q, fam)
        if ac is not None:
            scored = []
            for arg, g in ac:
                q2 = replace(q, arg=arg)
                gg, _ = row_answer(M, W, q2, "yn")
                if gg != g:
                    continue
                sc = shortcut_answers(M, W, q2, "yn", perm)
                scored.append((g == want, n_wrong(sc, g), rng.random(), arg, g))
            if not scored:
                raise mv.Reject("no_arg")
            scored.sort(reverse=True)
            ok = [s for s in scored if tier != "hard" or s[1] >= 2]
            if not ok:
                raise mv.Reject("tier_hard")
            q = replace(q, arg=ok[0][3])
        gold, tr = row_answer(M, W, q, "yn")
        if mv.is_undefined(gold):
            raise mv.Reject("undefined")
        twins = self.find_twins(M, W, q, "yn", fmt, base_state, gold)
        need_twin = "contrast" in views
        cands = [(W, None)] + [(W, t) for t, _ in twins] + [(t, W) for t, _ in twins]
        best = None
        for b, t in cands:
            if need_twin and t is None:
                continue
            g_b, _ = row_answer(M, b, q, "yn")
            sb, pb = (base_state, perm) if b is W else render(M, b, fmt)
            scb = shortcut_answers(M, b, q, "yn", pb)
            if tier == "hard" and n_wrong(scb, g_b) < 2:
                continue
            bmb = pmeta(tier, M.name, "yn", "base", fmt, tpl, self.renderer(b, fmt), sb)
            rows = [(bmb, int(g_b == "yes"))]
            if t is not None and need_twin:
                st_, _ = render(M, t, fmt)
                rows.append((pmeta(tier, M.name, "yn", "contrast", fmt, tpl, self.renderer(t, fmt), st_),
                             int(g_b != "yes")))
            else:
                y = int(g_b == "yes")
                if "ladder" in views:
                    rows.append((dict(bmb, view="ladder", polarity=1, tpl=sorted(M.YN[fam]["neg"])[0]), 1 - y))
                if "attack" in views:
                    rows.append((dict(bmb, view="attack"), y))
                if "jb" in views:
                    rows.append((dict(bmb, view="jb", qkind="jb", tpl="?", fmt="?", len_bin="?", renderer="?"), y))
                if "format" in views:
                    rows.append((dict(bmb, view="format", fmt="?", len_bin="?", renderer="?"), y))
            steer = 0 if self.steer_ok(scb, g_b, attempt) else 1
            c = (steer, self.bal.cost(self.part, rows), n_wrong(scb, g_b) * -1, rng.random())
            if best is None or c < best[0]:
                best = (c, b, t)
        if best is None:
            raise mv.Reject("no_base")
        if best[0][0] and (attempt < 40 or not self.fallback):
            raise mv.Reject("steer")
        _, Wb, Wt = best
        lat = self.fb.new_latent(split, M.name, {"world": world_dict(Wb), "query": q.__dict__}, {"fam": fam}, tier,
                                 edge=())
        u = self.fb.unit(lat)
        base = u.add(self.yn_rowspec(M, Wb, q, fam, tpl, fmt, "base", False))
        rows_of = {id(Wb): base}
        if need_twin:
            twin = u.add(self.yn_rowspec(M, Wt, q, fam, tpl, fmt, "contrast", False), twin_of=base)
            rows_of[id(Wt)] = twin
        worlds = [Wb] + ([Wt] if need_twin else [])
        for v in views:
            if v == "contrast":
                continue
            if v == "ladder":
                opts = []
                for w in worlds:
                    sp = self.yn_rowspec(M, w, q, fam, sorted(M.YN[fam]["neg"])[0], fmt, "ladder", True)
                    opts.append((w, sp))
                w, sp = self.pick(opts, tier, M)
                r = u.add(sp)
                u.relate("complement", rows_of[id(w)], r)
            elif v == "format":
                opts = []
                for w in worlds:
                    for f2 in FMT_LIST:
                        if f2.split(":")[0] == fmt.split(":")[0]:
                            continue
                        sp = self.yn_rowspec(M, w, q, fam, tpl, f2, "format", False)
                        if len(sp.state) <= max_len:
                            opts.append((w, sp))
                w, sp = self.pick(opts, tier, M)
                r = u.add(sp)
                u.relate("equiv", rows_of[id(w)], r)
            elif v == "jb":
                opts = []
                jtpl = self.fb.surface(self.phr_name("jbtpl"), self.phrasings(JB_Q), rng, split=split,
                                       extra=(M.name,))
                for w in worlds:
                    for f2 in FMT_LIST:
                        sp = self.jb_rowspec(M, w, q, fam, f2, jtpl, rng, commit=False)
                        if len(sp.state) <= max_len:
                            opts.append((w, sp))
                w, sp = self.pick(opts, tier, M)
                u.add(self.jb_rowspec(M, w, q, fam, sp.fmt, jtpl, rng, commit=True))
            elif v == "mirror":
                u.add(self.mirror_rowspec(M, Wb, fmt, rng))
            elif v == "attack":
                opts = [(w, None) for w in worlds]
                w = self.pick_attack(M, opts, q, fam, tpl, fmt, tier)
                clean = rows_of[id(w)]
                style = u.row(clean)["meta"]["card_style"]
                g, _ = row_answer(M, w, q, "yn")
                p = self.fb.plant(lat, "log_note", lambda a: f'"{a}"', g, ["no" if g == "yes" else "yes"],
                                  rule=rng.choice(FAKE_RULES), date_s=w.t_end.date().isoformat(),
                                  number=rng.randint(2, 9), json_key="notes" if fmt.startswith("json") else None,
                                  stratum=(self.part,))
                sp = self.yn_rowspec(M, w, q, fam, tpl, fmt, "attack", False, card_style=style, plant=p,
                                     extra_notes=(p.text,))
                r = u.add(sp)
                u.relate("inv", clean, r)
        self.finish_unit(u, attempt)
        return True

    def pick(self, opts, tier, M):
        """Among candidate (world, RowSpec) pairs for a view whose gold is fixed, the one that leaves the yes/no
        strata most balanced (non yes/no rows: the first)."""
        best = None
        for w, sp in opts:
            if sp.qkind not in ("yn", "jb"):
                return w, sp
            y = int(sp.gold == "yes") if sp.qkind == "yn" else int(sp.gold == sp.options[0])
            m = pmeta(tier, M.name, sp.qkind, sp.view, sp.fmt, sp.tpl, sp.renderer, sp.state, sp.polarity or 0)
            v = self.bal.violations(self.part, [(m, y)])
            c = self.bal.cost(self.part, [(m, y)]) + self.bal.len_cost(self.part, [(m, y, len(sp.state.rstrip()))])
            a = self.jbs.max_corr(m, y, len(sp.state.rstrip())) if sp.qkind == "jb" else 0.0
            key = (v, round(max(0.0, a - 0.03), 3), c, len(sp.state))
            if best is None or key < best[0]:
                best = (key, w, sp)
        if best is None:
            raise mv.Reject("no_view_candidate")
        return best[1], best[2]

    def pick_attack(self, M, opts, q, fam, tpl, fmt, tier):
        best = None
        for w, _ in opts:
            g, _ = row_answer(M, w, q, "yn")
            st_, _ = render(M, w, fmt)
            m = pmeta(tier, M.name, "yn", "attack", fmt, tpl, self.renderer(w, fmt), st_)
            c = self.bal.cost(self.part, [(m, int(g == "yes"))])
            if best is None or c < best[0]:
                best = (c, w)
        return best[1]

    def jb_rowspec(self, M, W, q, fam, fmt, jtpl, rng, commit):
        state, perm = render(M, W, fmt)
        f = dict(M.qfields(W, q))
        f["when"] = M.when(W)
        yd, nd = (x.format(**f) for x in M.YN[fam]["jb"])
        g, tr = row_answer(M, W, q, "yn")
        truth = g == "yes"
        wording = "family"
        if commit:
            opts, gold, wording = self.fb.jb(yd, nd, truth, rng, stratum=(self.part,))
        else:
            opts = [yd, nd]
            gold = opts[0] if truth else opts[1]
        ins, tpl = JB_Q[jtpl], jtpl
        if wording == "fallback":  # the adapter pair carries no statement, so the question states it (as JevBench does)
            tpl = "jbf.h" if jtpl in HOLDOUT_TPL else "jbf.a"
            ins = JB_FALLBACK_Q[tpl].format(s=yd)
        sc = shortcut_answers(M, W, q, "jb", perm, opts=opts)
        return mv.RowSpec("jb", "jb", state, ins, gold, fmt, self.renderer(W, fmt), tpl, options=opts,
                          polarity=0, edge=self.edges(M, W), shortcut_answers=sc, decisive=tuple(tr["decisive"]),
                          n_events=len(W.events))

    def value_options(self, M, W, q, gold_t, extra=(), K=None, rng=None, perm=None):
        """Option texts for a value question: gold + extra (twin) + the shortcut solvers' answers + fillers from the
        machine's value domain (or nearby numbers), 4-7 options."""
        texts = [gold_t] + [x for x in extra if x != gold_t]
        ip = sim.in_play(M, W, perm)
        for name in sim.SHORTCUT_NAMES:
            a = sim.shortcut_answer(M, W, q, name, perm, ip)
            if a is not None and not mv.is_undefined(a):
                t = M.vtext(q.key, a, W)
                if t not in texts:
                    texts.append(t)
        dom = M.domain(W, q)
        if dom is None:
            v = sim.observe(M, W)[q.key]
            step = 100 if M.name == "ledger" else 1
            near = [v + d * step for d in (1, -1, 2, -2, 3, 5, -3)]
            if M.name == "ledger":
                near += [v + 5000, v - 5000, v + 1, v - 1]
            dom = [x for x in near if x >= 0 or M.name == "ledger"]
        fill = [M.vtext(q.key, x, W) for x in dom]
        rng.shuffle(fill)
        for t in fill:
            if t not in texts:
                texts.append(t)
        hi = min(7, len(texts))
        if hi < 4:
            raise mv.Reject("few_options")
        K = K or rng.randint(4, hi)
        keep = texts[:max(K, len(extra) + 1)]
        return keep[:7]

    def mirror_rowspec(self, M, W, fmt, rng):
        q = M.queries(W, "value", rng)[0]
        vt = self.fb.surface(f"vtpl:{M.name}", sorted(M.VALUE_TPL), rng, split=self.split, extra=("mirror",))
        state, perm = render(M, W, fmt)
        g, tr = sim.decide(M, W, q)
        if mv.is_undefined(g):
            raise mv.Reject("undefined")
        gt = M.vtext(q.key, g, W)
        sc_raw = {}
        ip = sim.in_play(M, W, perm)
        for name in sim.SHORTCUT_NAMES:
            a = sim.shortcut_answer(M, W, q, name, perm, ip)
            sc_raw[name] = None if (a is None or mv.is_undefined(a)) else M.vtext(q.key, a, W)
        dom = M.domain(W, q)
        if dom is None:
            v = sim.observe(M, W)[q.key]
            step = 100 if M.name == "ledger" else 1
            dom = [x for x in (v + step, v - step, v + 2 * step, v + 3 * step, v - 2 * step) if x >= 0]
        fillers = [M.vtext(q.key, x, W) for x in dom]
        rng.shuffle(fillers)
        opts, og, info = self.mirror(gt, sc_raw, fillers, rng, vt)
        sc = {k: (v if v in opts else (info["none_option"] if (v is not None and info["none_option"]) else None))
              for k, v in sc_raw.items()}
        defs = M.option_defs(q, opts) or {}
        if info["none_option"] and defs:
            defs[info["none_option"]] = NONE_DEF
        return mv.RowSpec("mirror", "choice", state, self.question(M, W, q, M.VALUE_TPL[vt]), og, fmt,
                          self.renderer(W, fmt), vt, options=opts, defs=dict(sorted(defs.items())) or None,
                          edge=self.edges(M, W), shortcut_answers=sc, decisive=tuple(tr["decisive"]),
                          none_option=info["none_option"], n_events=len(W.events))

    def mirror(self, gt, sc_texts, fillers, rng, vt):
        """Choice mirror (SPEC 4.2): gold + the shortcut solvers' answers (+ fillers), 4-7 options. 'None of these'
        is offered in 20% of mirrors and is gold in 25% of those (quotas per output part); a mirror that offers it
        always has K = 4, so its gold positions stay uniform; gold positions are balanced per (view, template, K)."""
        wrong = [a for a in dict.fromkeys(v for _, v in sorted(sc_texts.items())) if a is not None and a != gt]
        from_sc = list(wrong)
        for f in fillers:
            if len(wrong) >= 3:
                break
            if f != gt and f not in wrong:
                wrong.append(f)
        if len(wrong) < 3:
            raise mv.Reject("mirror", "fewer than 3 wrong answers")
        none = mv.NONE_DEFAULT
        offer = self.fb.q_mirror_none.pick((self.part,), rng)
        if offer:
            K = 4
            pq = self.pos_quota("mirror", vt, K)
            ng = self.fb.q_none_gold.pick((self.part,), rng)
            if ng:
                opts = wrong[:3]
                rng.shuffle(opts)
                pq.add((), 3)
                return opts + [none], none, {"none_option": none, "from_shortcuts": from_sc}
            others = wrong[:2]
            rng.shuffle(others)
            i = pq.pick((), rng, allowed=[0, 1, 2])
            return others[:i] + [gt] + others[i:] + [none], gt, {"none_option": none, "from_shortcuts": from_sc}
        others = wrong[:6]
        K = len(others) + 1
        rng.shuffle(others)
        i = self.pos_quota("mirror", vt, K).pick((), rng)
        return others[:i] + [gt] + others[i:], gt, {"none_option": None, "from_shortcuts": from_sc}

    # ---------------------------------------------------------------- choice latents
    def do_choice(self, M, W, rec, fmt, fam, tpl, views, rng, attempt, max_len):
        split, tier = self.split, rec["tier"]
        q = M.queries(W, "value", rng)[0]
        base_state, perm = render(M, W, fmt)
        if len(base_state) > max_len:
            raise mv.Reject("too_long")
        g, tr = sim.decide(M, W, q)
        if mv.is_undefined(g):
            raise mv.Reject("undefined")
        need_twin = "contrast" in views
        twins = self.find_twins(M, W, q, "value", fmt, base_state, g) if need_twin else []
        if need_twin and not twins:
            raise mv.Reject("no_twin")
        cands = [(W, None)] if not need_twin else [(W, t) for t, _ in twins] + [(t, W) for t, _ in twins]
        best = None
        for b, t in cands:
            gb, _ = sim.decide(M, b, q)
            gbt = M.vtext(q.key, gb, b)
            sb, pb = (base_state, perm) if b is W else render(M, b, fmt)
            scb = shortcut_answers(M, b, q, "value", pb)
            if tier == "hard" and n_wrong(scb, gbt) < 2:
                continue
            steer = 0 if self.steer_ok(scb, gbt, attempt) else 1
            key = (steer, -n_wrong(scb, gbt), rng.random())
            if best is None or key < best[0]:
                best = (key, b, t)
        if best is None:
            raise mv.Reject("tier_hard")
        if best[0][0] and (attempt < 40 or not self.fallback):
            raise mv.Reject("steer")
        _, Wb, Wt = best
        gb, trb = sim.decide(M, Wb, q)
        gbt = M.vtext(q.key, gb, Wb)
        extra = []
        if Wt is not None:
            gt2, _ = sim.decide(M, Wt, q)
            extra = [M.vtext(q.key, gt2, Wt)]
        texts = self.value_options(M, Wb, q, gbt, extra, rng=rng, perm=display_order(Wb, fmt))
        K = len(texts)
        pq = self.pos_quota("base", tpl, K)
        pb = pq.pick((), rng)
        others = [x for x in texts if x != gbt]
        rng.shuffle(others)
        if Wt is not None:
            tq = self.pos_quota("contrast", tpl, K)
            pt = tq.pick((), rng, allowed=[i for i in range(K) if i != pb])
            others.remove(extra[0])
            opts = [None] * K
            opts[pb], opts[pt] = gbt, extra[0]
            it = iter(others)
            opts = [x if x is not None else next(it) for x in opts]
        else:
            opts = others[:pb] + [gbt] + others[pb:]
        defs = M.option_defs(q, opts)
        lat = self.fb.new_latent(split, M.name, {"world": world_dict(Wb), "query": q.__dict__}, {"fam": "value"}, tier)
        u = self.fb.unit(lat)
        rows_of = {}

        def spec(w, view, f2=fmt, plant=None, notes=()):
            st_, pm = render(M, w, f2, notes)
            gg, trw = sim.decide(M, w, q)
            gt_ = M.vtext(q.key, gg, w)
            sc = shortcut_answers(M, w, q, "value", pm, opts=opts)
            return mv.RowSpec(view, "choice", st_, self.question(M, w, q, M.VALUE_TPL[tpl]), gt_, f2,
                              self.renderer(w, f2), tpl, options=list(opts), defs=defs,
                              edge=self.edges(M, w) + (("hc:display_order",) if pm != [e.idx for e in
                                                                                      sim.time_order(w)] else ()),
                              shortcut_answers=sc, decisive=tuple(trw["decisive"]), n_events=len(w.events),
                              plant=plant, role="attacked" if plant else "choice")

        base = u.add(spec(Wb, "base"))
        rows_of[id(Wb)] = base
        worlds = [Wb]
        if Wt is not None:
            rows_of[id(Wt)] = u.add(spec(Wt, "contrast"), twin_of=base)
            worlds.append(Wt)
        for v in views:
            if v == "format":
                w = self.pick_pos(worlds, M, q, opts, "format", tpl, K)
                f2 = self.fmt2(fmt, "choice", rng)
                sp = spec(w, "format", f2)
                if len(sp.state) > max_len:
                    raise mv.Reject("too_long")
                r = u.add(sp)
                u.relate("equiv", rows_of[id(w)], r)
            elif v == "attack":
                w = self.pick_pos(worlds, M, q, opts, "attack", tpl, K)
                gg, _ = sim.decide(M, w, q)
                gt_ = M.vtext(q.key, gg, w)
                p = self.fb.plant(lat, "log_note", lambda a: f'"{a}"', gt_, [o for o in opts if o != gt_],
                                  rule=rng.choice(FAKE_RULES), date_s=w.t_end.date().isoformat(),
                                  number=rng.randint(2, 9), json_key="notes" if fmt.startswith("json") else None,
                                  stratum=(self.part,))
                r = u.add(spec(w, "attack", fmt, plant=p, notes=(p.text,)))
                u.relate("inv", rows_of[id(w)], r)
        self.finish_unit(u, attempt)
        for r in u.rows:
            if r["meta"]["view"] in ("format", "attack"):
                self.pos_quota(r["meta"]["view"], tpl, K).add((), r["options"].index(r["gold"]))
        return True

    def pick_pos(self, worlds, M, q, opts, view, tpl, K):
        best = None
        pq = self.pos_quota(view, tpl, K)
        cnt = pq.counts[()]
        for w in worlds:
            gg, _ = sim.decide(M, w, q)
            i = opts.index(M.vtext(q.key, gg, w))
            key = cnt[i]
            if best is None or key < best[0]:
                best = (key, w)
        return best[1]

    # ---------------------------------------------------------------- score latents
    def do_score(self, M, W, rec, fmt, fam, tpl, views, rng, attempt, max_len):
        split, tier = self.split, rec["tier"]
        q = M.queries(W, "score", rng)[0]
        levels = M.levels(W, q)
        K = len(levels)
        lq = self.lvl_quota(K)
        want = lq.pick((), rng, commit=False)
        base_state, perm = render(M, W, fmt)
        if len(base_state) > max_len:
            raise mv.Reject("too_long")
        g, tr = sim.decide(M, W, q)
        need_twin = "contrast" in views
        twins = self.find_twins(M, W, q, "score", fmt, base_state, g, limit=8)
        cands = [(W, None)] + [(W, t) for t, _ in twins] + [(t, W) for t, _ in twins]
        best = None
        for b, t in cands:
            if need_twin and t is None:
                continue
            gb, _ = sim.decide(M, b, q)
            sb, pb = (base_state, perm) if b is W else render(M, b, fmt)
            scb = shortcut_answers(M, b, q, "score", pb, levels=levels)
            if tier == "hard" and n_wrong(scb, levels[gb]) < 2:
                continue
            cnt = lq.counts[()]
            dev = abs(gb - want)
            tl = 0
            if t is not None and need_twin:
                gt_, _ = sim.decide(M, t, q)
                tl = cnt[gt_]
            steer = 0 if self.steer_ok(scb, levels[gb], attempt) else 1
            key = (steer, dev, cnt[gb] + tl, -n_wrong(scb, levels[gb]), rng.random())
            if best is None or key < best[0]:
                best = (key, b, t)
        if best is None:
            raise mv.Reject("tier_hard")
        if (best[0][0] or best[0][1] > 0) and (attempt < 60 or not self.fallback):
            raise mv.Reject("level_target")
        _, Wb, Wt = best
        opts = self.fb.score_options(levels)
        lat = self.fb.new_latent(split, M.name, {"world": world_dict(Wb), "query": q.__dict__}, {"fam": "score"}, tier)
        u = self.fb.unit(lat)
        rows_of = {}

        def spec(w, view, f2=fmt, plant=None, notes=()):
            st_, pm = render(M, w, f2, notes)
            gg, trw = sim.decide(M, w, q)
            sc = shortcut_answers(M, w, q, "score", pm, levels=levels)
            return mv.RowSpec(view, "score", st_, self.question(M, w, q, M.SCORE_TPL[tpl]), levels[gg], f2,
                              self.renderer(w, f2), tpl, options=list(opts),
                              edge=self.edges(M, w) + (("hc:display_order",) if pm != [e.idx for e in
                                                                                      sim.time_order(w)] else ()),
                              shortcut_answers=sc, decisive=tuple(trw["decisive"]), n_events=len(w.events),
                              plant=plant, role="attacked" if plant else "choice", levels=K)

        base = u.add(spec(Wb, "base"))
        rows_of[id(Wb)] = base
        worlds = [Wb]
        if need_twin:
            rows_of[id(Wt)] = u.add(spec(Wt, "contrast"), twin_of=base)
            worlds.append(Wt)
        for v in views:
            if v in ("format", "attack"):
                cnt = lq.counts[()]
                w = min(worlds, key=lambda x: cnt[sim.decide(M, x, q)[0]])
                if v == "format":
                    f2 = self.fmt2(fmt, "score", rng)
                    sp = spec(w, "format", f2)
                    if len(sp.state) > max_len:
                        raise mv.Reject("too_long")
                    r = u.add(sp)
                    u.relate("equiv", rows_of[id(w)], r)
                else:
                    gg, _ = sim.decide(M, w, q)
                    p = self.fb.plant(lat, "log_note", lambda a: f'"{a}"', levels[gg],
                                      [x for x in levels if x != levels[gg]], rule=rng.choice(FAKE_RULES),
                                      date_s=w.t_end.date().isoformat(), number=rng.randint(2, 9),
                                      json_key="notes" if fmt.startswith("json") else None, stratum=(self.part,))
                    r = u.add(spec(w, "attack", fmt, plant=p, notes=(p.text,)))
                    u.relate("inv", rows_of[id(w)], r)
        self.finish_unit(u, attempt)
        for r in u.rows:
            lq.add((), r["options"].index(r["gold"]))
        return True

    # ---------------------------------------------------------------- judge latents
    def do_judge(self, M, W, rec, fmt, fam, tpl, views, rng, attempt, max_len):
        split, tier = self.split, "judge"
        q0 = M.queries(W, "judge", rng)[0]
        obs = sim.observe(M, W)
        if obs.get(q0.key) is None:
            raise mv.Reject("undefined")
        keys = [q0.key] + [k for k in obs if k != q0.key and obs[k] is not None]
        others = keys[1:]
        rng.shuffle(others)
        keys = [q0.key] + others[:rng.randint(1, 2)]
        base_rec = [(k, obs[k]) for k in keys]
        # the controlled error: the queried value replaced by a shortcut solver's value (else another domain value)
        perm0 = display_order(W, fmt)
        ip = sim.in_play(M, W, perm0)
        wrong_vals = []
        for name in sim.SHORTCUT_NAMES:
            a = sim.shortcut_answer(M, W, Query("value", "v", q0.key), name, perm0, ip)
            if a is not None and not mv.is_undefined(a) and a != obs[q0.key]:
                wrong_vals.append(a)
        if not wrong_vals:
            dom = M.domain(W, Query("value", "v", q0.key))
            if dom is None:
                v = obs[q0.key]
                dom = [v + (100 if M.name == "ledger" else 1), v - (100 if M.name == "ledger" else 1)]
            wrong_vals = [x for x in dom if x != obs[q0.key] and not (isinstance(x, int) and x < 0)]
        if not wrong_vals:
            raise mv.Reject("no_error_value")
        q = Query("judge", "record", q0.key)
        Wy = replace(W, record=list(base_rec))
        Wn = replace(W, record=[(q0.key, rng.choice(wrong_vals))] + base_rec[1:])
        sy, py = render(M, Wy, fmt)
        sn, pn = render(M, Wn, fmt)
        if max(len(sy), len(sn)) > max_len:
            raise mv.Reject("too_long")
        best = None
        for w, st_, pm in ((Wy, sy, py), (Wn, sn, pn)):
            g, _ = sim.decide(M, w, q)
            if mv.is_undefined(g):
                continue
            sc = shortcut_answers(M, w, q, "judge", pm)
            m = pmeta(tier, M.name, "yn", "base", fmt, tpl, self.renderer(w, fmt), st_)
            rows = [(m, int(g == "yes"))] + ([(dict(m, view="attack", len_bin="?", renderer=m["renderer"]),
                                                int(g == "yes"))] if "attack" in views else [])
            key = (0 if self.steer_ok(sc, g, attempt) else 1, self.bal.cost(self.part, rows), rng.random())
            if best is None or key < best[0]:
                best = (key, w)
        if best is None:
            raise mv.Reject("undefined")
        if best[0][0] and (attempt < 40 or not self.fallback):
            raise mv.Reject("steer")
        Wb = best[1]
        lat = self.fb.new_latent(split, M.name, {"world": world_dict(Wb), "query": q.__dict__}, {"fam": "judge"}, tier)
        u = self.fb.unit(lat)

        def spec(w, view, plant=None, notes=(), style=None):
            st_, pm = render(M, w, fmt, notes)
            g, trw = sim.decide(M, w, q)
            sc = shortcut_answers(M, w, q, "judge", pm)
            return mv.RowSpec(view, "yn", st_, JUDGE_Q[tpl], g, fmt, self.renderer(w, fmt), tpl,
                              defs=dict(JUDGE_DEFS), card_style=style, self_contained=True, polarity=0, judge=True,
                              role="attacked" if plant else "aff",
                              edge=self.edges(M, w) + (("hc:display_order",) if pm != [e.idx for e in
                                                                                      sim.time_order(w)] else ()),
                              shortcut_answers=sc, decisive=tuple(trw["decisive"]), n_events=len(w.events),
                              plant=plant)

        base = u.add(spec(Wb, "base"))
        for v in views:
            if v == "mirror":
                u.add(self.mirror_rowspec(M, Wb, fmt, rng))
            elif v == "attack":
                g, _ = sim.decide(M, Wb, q)
                p = self.fb.plant(lat, "log_note", lambda a: f'"{a}"', g, ["no" if g == "yes" else "yes"],
                                  rule=rng.choice(FAKE_RULES), date_s=Wb.t_end.date().isoformat(),
                                  number=rng.randint(2, 9), json_key="notes" if fmt.startswith("json") else None,
                                  stratum=(self.part,))
                r = u.add(spec(Wb, "attack", plant=p, notes=(p.text,), style=u.row(base)["meta"]["card_style"]))
                u.relate("inv", base, r)
        self.finish_unit(u, attempt)
        return True


# ================================================================================================ latent export (devx / F4)
def world_dict(W) -> dict:
    """A JSON-able view of a world (typed events, parameters, query time), for reviewer R's devx renderers and for
    audits. Labels for such a world come from sim.decide, never from this dict."""
    def conv(x):
        if isinstance(x, dict):
            return {str(k): conv(v) for k, v in x.items()}
        if isinstance(x, (list, tuple, set)):
            return [conv(v) for v in (sorted(x, key=str) if isinstance(x, set) else x)]
        if hasattr(x, "isoformat"):
            return x.isoformat()
        return x
    return conv({"machine": W.machine, "t0": W.t0, "t_end": W.t_end, "t_q": W.t_q, "at_end": W.at_end,
                 "ents": W.ents, "target": W.target, "decoys": W.decoys, "params": {k: v for k, v in W.params.items()
                                                                                   if k != "_perm"},
                 "offsets": W.offsets, "record": W.record,
                 "events": [{"idx": e.idx, "eid": e.eid, "ts": e.ts, "src": e.src, "kind": e.kind, "ent": e.ent,
                             "a": e.a, "style": e.style, "lt": e.lt, "resend": e.resend} for e in W.events]})


def export_latents(split: str = "devx", n: int = 100) -> list[dict]:
    """Held-out latents for reviewer R (SPEC 6: devx uses dev_holdout machines only; seed stream = train + 3e9):
    typed worlds, a query, and the gold from sim.decide. R renders them with its own renderers."""
    rng = mv.rng_for(KEY, split, "export")
    pool = mv.NamePool(split)
    out = []
    i = 0
    while len(out) < n:
        i += 1
        mname = MACHINES.holdout[i % len(MACHINES.holdout)]
        M = MACH[mname]
        tier = ("easy", "standard", "judge", "hard")[i % 4]
        kind = ("yn", "choice", "score")[i % 3]
        lo, hi = TIER_EVENTS[tier]
        spec = Spec(tier, rng.randint(lo, min(hi, 24)), {"guard": 1, "resend": 1, "decoy": 1,
                                                          "expiry": int(M.has_expiry)},
                    at_end=rng.random() < 0.7, lang=0.5, qtype=kind, n_ent=rng.randint(3, 5) if kind == "score" else None)
        try:
            W = sim.sample_world(M, rng, pool, spec)
        except mv.Reject:
            continue
        if surface_issues(M, W):
            continue
        qt = {"yn": "yn", "choice": "value", "score": "score"}[kind]
        q = M.queries(W, qt, rng)[0]
        ak = F3.arg_kind(M, W, q.fam) if qt == "yn" else None
        if ak is not None:
            v = sim.observe(M, W)[q.key]
            if v is None:
                continue
            if ak == "ge":
                q = replace(q, arg=v if rng.random() < 0.5 else v + 1)
            else:
                dom = [x for x in (M.domain(W, Query("value", q.fam, q.key)) or []) if x != v]
                q = replace(q, arg=v if (rng.random() < 0.5 or not dom) else rng.choice(dom))
        g, tr = sim.decide(M, W, q)
        if mv.is_undefined(g):
            continue
        out.append({"latent": world_dict(W), "query": q.__dict__, "gold": g if not isinstance(g, bool) else g,
                    "levels": M.levels(W, q) if qt == "score" else None})
    return out


def propositions(rows) -> list[dict]:
    """F4(b) hook: the decision proposition of every yes/no base row (its JB family wording), with its truth."""
    out = []
    for r in rows:
        m = r["meta"]
        if m["view"] == "base" and m["qkind"] == "yn" and not m["judge"]:
            out.append({"rid": r["rid"], "latent_id": m["latent_id"], "state": r["state"],
                        "question": r["instructions"], "truth": r["gold"] == "yes"})
    return out


# ================================================================================================ build + report
def build(splits=("train", "dev_iid", "dev_holdout"), fb=None, limit=None, log=None, verbose=False):
    fb = fb or mv.FamilyBuilder(KEY, generator_file=__file__)
    if "+sim:" not in fb.revision:  # the labels also depend on the simulator module: pin its hash in every row
        fb.revision += "+sim:" + mv.sha256_file(Path(sim.__file__))[:16]
    log = log if log is not None else Counter()
    bal = Bal()
    sc_stats: dict = {"train": {}, "dev": {}}  # shortcut steering per output part
    jbs = {"train": JBStats(), "dev": JBStats()}
    for split in splits:
        recs = make_plan(split)
        if limit:
            recs = recs[:limit]
        b = F3(fb, split, bal, sc_stats[mv.PART_OF_SPLIT[split]], log, jbs[mv.PART_OF_SPLIT[split]])
        todo = list(recs)
        for p in range(PASSES):  # strict passes; recipes that do not fit yet are deferred to the next pass
            left = []
            for rec in todo:
                last = p == PASSES - 1
                if not b.realize(rec, fallback=last, attempts=120 if p == 0 else (ACCEPT_FROM + 10 if last else 50)):
                    left.append(rec)
            log[f"deferred:{split}:pass{p}"] = len(left)
            if verbose:
                print(f"[F3] {split} pass {p}: {len(todo) - len(left)} built, {len(left)} deferred", file=sys.stderr,
                      flush=True)
            todo = left
            if not todo:
                break
        log[f"latents:{split}"] = sum(b.made.values())
        log[f"planned:{split}"] = len(recs)
        log[f"failed:{split}"] = len(todo)
    return fb, log


def report(fb, log) -> dict:
    out = {"rejects": dict(fb.rejects), "log": dict(log)}
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rels = [x for x in fb.rels if x["a"] in rids]
        chk = mv.run_checks(rows, rels)
        gate = [k for k, v in chk.items() if isinstance(v, dict) and "ok" in v and k not in ("summary", "hard_cases")
                and not (part == "dev" and k == "artefacts")]
        out[part] = {"ok": all(chk[k]["ok"] for k in gate), "mv_run_checks_ok": chk["ok"], "summary": chk["summary"],
                     "artefacts": chk["artefacts"],
                     "failed": {k: v for k, v in chk.items() if isinstance(v, dict) and v.get("ok") is False},
                     "shortcuts": chk["shortcuts"]["shortcuts"], "tiers": chk["tiers"]["mix"],
                     "balance_violations": len(chk["balance"]["violations"]),
                     "hard_cases": chk["hard_cases"]["by_area"]}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="write rows, relations, defs and MANIFEST_yn2b records")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="only the first N recipes per split (smoke)")
    ap.add_argument("--report", default=None, help="write the JSON report to this path (scratch)")
    a = ap.parse_args(argv)
    fb, log = build(limit=a.limit, verbose=True)
    rep = report(fb, log)
    txt = json.dumps(rep, indent=1, default=str)
    if a.report:
        Path(a.report).write_text(txt)
    print(txt[:20000])
    if a.write:
        if not (rep["train"]["ok"] and rep["dev"]["ok"]):
            print("checks failed: nothing written", file=sys.stderr)
            return 2
        print(json.dumps(fb.write(overwrite=a.overwrite, parts=("train", "dev")), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
