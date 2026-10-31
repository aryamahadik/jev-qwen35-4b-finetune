"""dx_state_track: reviewer R's devx renderer + parse-back for F3 `gen3_state_track` (yn2b/SPEC.md sections 5 F3, 6).

Latents: gen3_state_track.export_latents("devx", n) (the two held-out machines, feature flags and document versions,
devx seed stream and name pool). Labels: gen3_state_track_sim.decide with gen3_state_track.MACH (the machines with the
R2 rule fixes) only. Everything a reader sees (rule texts, event lines, starting-state layout, questions, level names,
option texts, cards) was written for devx from the simulator's typed semantics (apply / observe / queries), not from
the training renderers or rule texts.

Views (one row per latent): yes/no (flag on for a person; current content equals a label), with an inverse wording
for balance; JB-letter; choice (rollout value / current content); score (rollout band / number of versions).
Formats: log (oldest first), log newest first, json (canonical), and a per-person layout with each person's local
UTC offset (the rules say to convert).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import dx_common as dx  # noqa: E402
import gen3_state_track_sim as sim  # noqa: E402  (typed simulator: World, Ev, Query, decide)

KEY = "gen3_state_track"
UTC = timezone.utc
FMTS = ("oldest", "newest", "json", "people")
FMT_META = {"oldest": "log:chrono", "newest": "log:newest", "json": "json", "people": "log:grouped"}
N_EXPORT = 220


def _g3():
    import gen3_state_track as g3   # its latent export and its fixed machines (MACH) only
    return g3


# ------------------------------------------------------------------------------------------------ time text
def off_text(m: int) -> str:
    if m == 0:
        return "UTC"
    s = "+" if m > 0 else "-"
    m = abs(m)
    return f"UTC{s}{m // 60:02d}:{m % 60:02d}"


def ts_text(t: datetime, off: int = 0) -> str:
    loc = t.astimezone(timezone(timedelta(minutes=off)))
    return f"{loc:%Y-%m-%d %H:%M} {off_text(off)}"


def parse_ts_text(s: str) -> datetime:
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC(?:([+-])(\d{2}):(\d{2}))?", s.strip())
    if not m:
        raise ValueError(f"time {s!r}")
    off = 0 if not m.group(2) else (1 if m.group(2) == "+" else -1) * (int(m.group(3)) * 60 + int(m.group(4)))
    loc = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M").replace(tzinfo=timezone(timedelta(minutes=off)))
    return loc.astimezone(UTC)


# ------------------------------------------------------------------------------------------------ worlds
def world_from_dict(d: dict) -> sim.World:
    t = lambda s: datetime.fromisoformat(s)  # noqa: E731
    evs = [sim.Ev(e["idx"], e["eid"], t(e["ts"]), e["src"], e["kind"], e["ent"], dict(e["a"]), e["style"], e["lt"],
                  e["resend"]) for e in d["events"]]
    return sim.World(d["machine"], t(d["t0"]), t(d["t_end"]), t(d["t_q"]), d["at_end"], dict(d["ents"]), d["target"],
                     dict(d["decoys"]), evs, dict(d["params"]), "", [], dict(d["offsets"]), "iso", [],
                     d.get("record"))


def query_from_dict(q: dict) -> sim.Query:
    return sim.Query(q["qtype"], q["fam"], tuple(q["key"]) if q["key"] else None, q["arg"], tuple(q.get("keys") or ()))


def machine(name: str):
    return _g3().MACH[name]


def gold_of(W, q):
    g, _ = sim.decide(machine(W.machine), W, q)
    return g


# ------------------------------------------------------------------------------------------------ rules (devx text)
COMMON = [
    "Every log line asks for one change. A request that the rules do not allow at its own timestamp is refused and "
    "changes nothing.",
    "Requests take effect in order of their timestamps, earliest first, whatever order the lines are printed in. A time "
    "written with an offset from UTC is converted to UTC before times are compared.",
    "An event id can take effect only once: a later line that repeats an id which already took effect is a duplicate "
    "and changes nothing. A line whose earlier copy was refused is judged on its own.",
    "Only the ids listed in the starting state exist. A line about any other id changes nothing, even if it differs "
    "from a listed id by a single character.",
    "A question about a stated time counts only the lines timestamped at or before that time.",
]
FLAG_RULES = [
    "In production, switching a flag on or off, setting its rollout percentage, or releasing its kill switch needs "
    "one of the approved change tickets listed in the starting state; a request without one (or with any other "
    "ticket) is refused.",
    "A request for any environment other than production needs no ticket and leaves every production value unchanged.",
    "Pulling the kill switch needs no ticket. While the kill switch is pulled the flag is off for every person, "
    "whatever any override says.",
    "A pin sets the flag on or off for one person for the stated number of hours, counted from the pin's timestamp; "
    "at exactly that many hours later it has ended. When several pins for the same person are in force, the most "
    "recent one decides.",
    "With no pin in force (and the kill switch not pulled), the flag is on for a person when it is switched on in "
    "production and that person's bucket number is lower than the production rollout percentage.",
    "An undo line names an earlier event id. If that event took effect and has not been undone yet, everything it "
    "changed goes back to how it was just before it (undoing a pin cancels that pin); otherwise the undo changes "
    "nothing. An undo needs no ticket.",
]
DOC_RULES = [
    "Each document starts with version 1, whose content is shown in the starting state. A save adds a new version "
    "with the saved content. A restore of version k adds a new version whose content is that of version k; a restore "
    "naming a version number that does not exist yet is refused.",
    "A lock is held by the person who set it for {lock} minutes from its timestamp; at exactly {lock} minutes it has "
    "ended. While a lock is held, saves and restores by anyone else are refused, and every new lock request is "
    "refused (also one from the holder). An unlock ends the lock only when it comes from the holder while the lock is "
    "held; otherwise it is refused.",
    "Only the listed approvers can approve. An approval names a version number that must already exist; otherwise it "
    "is refused. The current version counts as approved when its version number has been approved.",
]


def rules(W) -> list:
    if W.machine == "flags":
        return COMMON + FLAG_RULES
    return COMMON + [r.format(lock=W.params["lock_min"]) for r in DOC_RULES]


# ------------------------------------------------------------------------------------------------ event lines
def ev_text(e, W) -> str:
    """One event as text: structured (style s) or a sentence (style l)."""
    a, by, ent = e.a, e.src, e.ent
    if W.machine == "flags":
        tk = a.get("chg")
        tkt = f"ticket {tk}" if tk else "no ticket"
        if e.style == "s":
            if e.kind in ("enable", "disable"):
                return f"by {by}: {'switch on' if e.kind == 'enable' else 'switch off'} {ent} in {a['env']} ({tkt})"
            if e.kind == "rollout":
                return f"by {by}: rollout of {ent} in {a['env']} set to {a['p']}% ({tkt})"
            if e.kind == "kill":
                return f"by {by}: kill switch pulled on {ent}"
            if e.kind == "unkill":
                return f"by {by}: kill switch released on {ent} ({tkt})"
            if e.kind == "override":
                return f"by {by}: pin {ent} {'on' if a['on'] else 'off'} for {a['u']}, {_hours(a['h'])}"
            if e.kind == "revert":
                return f"by {by}: undo {a['of']} on {ent}"
        else:
            if e.kind in ("enable", "disable"):
                return (f"{by} wrote: please turn {ent} {'on' if e.kind == 'enable' else 'off'} in {a['env']}"
                        + (f", ticket {tk}." if tk else ", no ticket."))
            if e.kind == "rollout":
                return f"{by} wrote: please move {ent} to {a['p']}% in {a['env']}" + (f", ticket {tk}." if tk else
                                                                                       ", no ticket.")
            if e.kind == "kill":
                return f"{by} wrote: pull the kill switch on {ent} now."
            if e.kind == "unkill":
                return f"{by} wrote: release the kill switch on {ent}" + (f", ticket {tk}." if tk else ", no ticket.")
            if e.kind == "override":
                return (f"{by} wrote: pin {ent} to {'on' if a['on'] else 'off'} for {a['u']} for the next "
                        f"{_hours(a['h'])}.")
            if e.kind == "revert":
                return f"{by} wrote: undo event {a['of']} on {ent}."
    else:
        if e.style == "s":
            if e.kind == "save":
                return f"by {by}: save {ent}, content \"{a['lab']}\""
            if e.kind == "restore":
                return f"by {by}: restore {ent} to version {a['k']}"
            if e.kind == "lock":
                return f"by {by}: lock {ent}"
            if e.kind == "unlock":
                return f"by {by}: unlock {ent}"
            if e.kind == "approve":
                return f"by {by}: approve {ent} version {a['k']}"
        else:
            if e.kind == "save":
                return f"{by} saved a new version of {ent} reading \"{a['lab']}\"."
            if e.kind == "restore":
                return f"{by} asked to bring {ent} back to version {a['k']}."
            if e.kind == "lock":
                return f"{by} took the lock on {ent}."
            if e.kind == "unlock":
                return f"{by} let go of the lock on {ent}."
            if e.kind == "approve":
                return f"{by} signed off version {a['k']} of {ent}."
    raise ValueError((W.machine, e.kind, e.style))


def _hours(h: int) -> str:
    return f"{h} hour" if h == 1 else f"{h} hours"


def _h(s: str) -> int:
    m = re.fullmatch(r"(\d+) hours?", s)
    return int(m.group(1))


EV_PATTERNS = {
    "flags": [
        (r"by (?P<by>.+?): (?P<w>switch on|switch off) (?P<e>\S+) in (?P<env>\S+) \((?P<t>ticket \S+|no ticket)\)",
         lambda m: ("enable" if m["w"] == "switch on" else "disable", {"env": m["env"], "chg": _tk(m["t"])}, "s")),
        (r"by (?P<by>.+?): rollout of (?P<e>\S+) in (?P<env>\S+) set to (?P<p>\d+)% \((?P<t>ticket \S+|no ticket)\)",
         lambda m: ("rollout", {"env": m["env"], "p": int(m["p"]), "chg": _tk(m["t"])}, "s")),
        (r"by (?P<by>.+?): kill switch pulled on (?P<e>\S+)", lambda m: ("kill", {}, "s")),
        (r"by (?P<by>.+?): kill switch released on (?P<e>\S+) \((?P<t>ticket \S+|no ticket)\)",
         lambda m: ("unkill", {"chg": _tk(m["t"])}, "s")),
        (r"by (?P<by>.+?): pin (?P<e>\S+) (?P<on>on|off) for (?P<u>.+?), (?P<h>\d+ hours?)",
         lambda m: ("override", {"u": m["u"], "on": m["on"] == "on", "h": _h(m["h"])}, "s")),
        (r"by (?P<by>.+?): undo (?P<of>\S+) on (?P<e>\S+)", lambda m: ("revert", {"of": m["of"]}, "s")),
        (r"(?P<by>.+?) wrote: please turn (?P<e>\S+) (?P<on>on|off) in (?P<env>\S+), (?P<t>ticket \S+|no ticket)\.",
         lambda m: ("enable" if m["on"] == "on" else "disable", {"env": m["env"], "chg": _tk(m["t"])}, "l")),
        (r"(?P<by>.+?) wrote: please move (?P<e>\S+) to (?P<p>\d+)% in (?P<env>\S+), (?P<t>ticket \S+|no ticket)\.",
         lambda m: ("rollout", {"env": m["env"], "p": int(m["p"]), "chg": _tk(m["t"])}, "l")),
        (r"(?P<by>.+?) wrote: pull the kill switch on (?P<e>\S+) now\.", lambda m: ("kill", {}, "l")),
        (r"(?P<by>.+?) wrote: release the kill switch on (?P<e>\S+), (?P<t>ticket \S+|no ticket)\.",
         lambda m: ("unkill", {"chg": _tk(m["t"])}, "l")),
        (r"(?P<by>.+?) wrote: pin (?P<e>\S+) to (?P<on>on|off) for (?P<u>.+?) for the next (?P<h>\d+ hours?)\.",
         lambda m: ("override", {"u": m["u"], "on": m["on"] == "on", "h": _h(m["h"])}, "l")),
        (r"(?P<by>.+?) wrote: undo event (?P<of>\S+) on (?P<e>\S+)\.", lambda m: ("revert", {"of": m["of"]}, "l")),
    ],
    "docs": [
        (r"by (?P<by>.+?): save (?P<e>\S+), content \"(?P<lab>[^\"]+)\"", lambda m: ("save", {"lab": m["lab"]}, "s")),
        (r"by (?P<by>.+?): restore (?P<e>\S+) to version (?P<k>\d+)", lambda m: ("restore", {"k": int(m["k"])}, "s")),
        (r"by (?P<by>.+?): lock (?P<e>\S+)", lambda m: ("lock", {}, "s")),
        (r"by (?P<by>.+?): unlock (?P<e>\S+)", lambda m: ("unlock", {}, "s")),
        (r"by (?P<by>.+?): approve (?P<e>\S+) version (?P<k>\d+)", lambda m: ("approve", {"k": int(m["k"])}, "s")),
        (r"(?P<by>.+?) saved a new version of (?P<e>\S+) reading \"(?P<lab>[^\"]+)\"\.",
         lambda m: ("save", {"lab": m["lab"]}, "l")),
        (r"(?P<by>.+?) asked to bring (?P<e>\S+) back to version (?P<k>\d+)\.",
         lambda m: ("restore", {"k": int(m["k"])}, "l")),
        (r"(?P<by>.+?) took the lock on (?P<e>\S+)\.", lambda m: ("lock", {}, "l")),
        (r"(?P<by>.+?) let go of the lock on (?P<e>\S+)\.", lambda m: ("unlock", {}, "l")),
        (r"(?P<by>.+?) signed off version (?P<k>\d+) of (?P<e>\S+)\.", lambda m: ("approve", {"k": int(m["k"])}, "l")),
    ],
}


def _tk(s: str):
    return None if s == "no ticket" else s[len("ticket "):]


def parse_ev_text(machine_name: str, text: str):
    for pat, fn in EV_PATTERNS[machine_name]:
        m = re.fullmatch(pat, text)
        if m:
            kind, a, style = fn(m.groupdict())
            return kind, m["e"], m["by"], a, style
    raise ValueError(f"event text not parsed: {text!r}")


# ------------------------------------------------------------------------------------------------ starting state
def start_lines(W) -> list:
    P = W.params
    if W.machine == "flags":
        out = [f"Flag {k}: production {'on' if v['enabled'] else 'off'}, rollout {v['rollout']}%, kill switch not "
               f"pulled" for k, v in W.ents.items()]
        out += [f"Person {u}: bucket {P['buckets'][u]}" for u in P["users"]]
        out += [f"Approved change tickets: {', '.join(P['chg_ok'])}"]
        return out
    out = [f"Document {k}: version 1 reads \"{v['v1']}\"; not locked" for k, v in W.ents.items()]
    out += [f"Editors: {', '.join(P['editors'])}", f"Approvers: {', '.join(P['approvers'])}",
            f"Lock length: {P['lock_min']} minutes"]
    return out


def parse_start(machine_name: str, lines: list) -> tuple[dict, dict]:
    ents, P = {}, {}
    if machine_name == "flags":
        P = {"users": [], "buckets": {}}
        for ln in lines:
            m = re.fullmatch(r"Flag (\S+): production (on|off), rollout (\d+)%, kill switch not pulled", ln)
            if m:
                ents[m.group(1)] = {"enabled": m.group(2) == "on", "rollout": int(m.group(3))}
                continue
            m = re.fullmatch(r"Person (.+?): bucket (\d+)", ln)
            if m:
                P["users"].append(m.group(1))
                P["buckets"][m.group(1)] = int(m.group(2))
                continue
            m = re.fullmatch(r"Approved change tickets: (.+)", ln)
            if m:
                P["chg_ok"] = m.group(1).split(", ")
                continue
            raise ValueError(f"start line {ln!r}")
        return ents, P
    for ln in lines:
        m = re.fullmatch(r"Document (\S+): version 1 reads \"([^\"]+)\"; not locked", ln)
        if m:
            ents[m.group(1)] = {"v1": m.group(2)}
            continue
        m = re.fullmatch(r"(Editors|Approvers): (.+)", ln)
        if m:
            P[m.group(1).lower()] = m.group(2).split(", ")
            continue
        m = re.fullmatch(r"Lock length: (\d+) minutes", ln)
        if m:
            P["lock_min"] = int(m.group(1))
            continue
        raise ValueError(f"start line {ln!r}")
    return ents, P


# ------------------------------------------------------------------------------------------------ the state
TITLE = {"flags": "FEATURE FLAG SERVICE - change requests", "docs": "DOCUMENT STORE - edit requests"}


def person_offsets(W, rng) -> dict:
    people = sorted({e.src for e in W.events})
    choices = [0, 60, 120, -300, -240, 330, 540, -420]
    return {p: choices[rng.randrange(len(choices))] for p in people}


def render_state(W, fmt: str, rng) -> str:
    rl = rules(W)
    st = start_lines(W)
    evs = sorted(W.events, key=lambda e: (e.ts, e.idx))
    exp = ts_text(W.t_end)
    if fmt == "json":
        obj = {"system": TITLE[W.machine], "exported_at": exp,
               "rules": [f"{i}. {r}" for i, r in enumerate(rl, 1)], "starting_state": st,
               "requests": [{"time": ts_text(e.ts), "event_id": e.eid, "request": ev_text(e, W)} for e in evs]}
        return mv.render_json(obj)
    head = [TITLE[W.machine], f"Log exported at {exp}.", "", "RULES"] + [f"{i}. {r}" for i, r in enumerate(rl, 1)]
    head += ["", "STARTING STATE"] + [f"- {x}" for x in st]
    if fmt in ("oldest", "newest"):
        seq = evs if fmt == "oldest" else list(reversed(evs))
        order = "oldest first" if fmt == "oldest" else "newest first"
        body = ["", f"REQUEST LOG ({order})"] + [f"{ts_text(e.ts)} | {e.eid} | {ev_text(e, W)}" for e in seq]
        return "\n".join(head + body)
    # people: grouped by the person who sent the request, local clock of each person
    offs = person_offsets(W, rng)
    body = ["", "REQUESTS BY PERSON (each person's own clock)"]
    for p in sorted(offs, key=lambda x: (min(e.ts for e in evs if e.src == x), x)):
        body += ["", f"{p} (clock {off_text(offs[p])}):"]
        body += [f"  {ts_text(e.ts, offs[p])} | {e.eid} | {ev_text(e, W)}" for e in evs if e.src == p]
    return "\n".join(head + body)


def parse_state(text: str) -> dict:
    if text.startswith("{"):
        o = json.loads(text)
        mach = "flags" if o["system"] == TITLE["flags"] else "docs"
        start = o["starting_state"]
        lines = [(r["time"], r["event_id"], r["request"]) for r in o["requests"]]
        t_end = parse_ts_text(o["exported_at"])
        rules_txt = [re.sub(r"^\d+\. ", "", r) for r in o["rules"]]
    else:
        L = text.split("\n")
        mach = "flags" if L[0] == TITLE["flags"] else "docs"
        t_end = parse_ts_text(re.fullmatch(r"Log exported at (.+)\.", L[1]).group(1))
        i = L.index("RULES") + 1
        rules_txt = []
        while L[i]:
            rules_txt.append(re.sub(r"^\d+\. ", "", L[i]))
            i += 1
        i = L.index("STARTING STATE") + 1
        start = []
        while i < len(L) and L[i].startswith("- "):
            start.append(L[i][2:])
            i += 1
        lines = []
        for ln in L[i:]:
            m = re.fullmatch(r"\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC\S*) \| (\S+) \| (.+)", ln)
            if m:
                lines.append((m.group(1), m.group(2), m.group(3)))
    ents, P = parse_start(mach, start)
    evs = []
    for k, (ts, eid, txt) in enumerate(sorted(lines, key=lambda x: parse_ts_text(x[0]))):
        kind, ent, by, a, style = parse_ev_text(mach, txt)
        evs.append(sim.Ev(k, eid, parse_ts_text(ts), by, kind, ent, a, style))
    lock = None
    for r in rules_txt:
        m = re.search(r"for (\d+) minutes from its timestamp", r)
        if m:
            lock = int(m.group(1))
    return {"machine": mach, "t_end": t_end, "ents": ents, "params": P, "events": evs, "rules": rules_txt,
            "lock_rule": lock}


# ------------------------------------------------------------------------------------------------ questions
def when(W) -> str:
    return "at the end of the log" if W.at_end else f"as of {ts_text(W.t_q)}"


LEVELS = {"flags": ["0% (nobody)", "1% to 24%", "25% to 49%", "50% to 99%", "100% (everybody)"],
          "docs": ["only version 1", "2 versions", "3 versions", "4 versions", "5 versions or more"]}


def yn_question(W, q, neg: bool) -> str:
    if q.fam == "on":
        return (f"Following the numbered rules, is flag {W.target} {'off' if neg else 'on'} for {q.key[1]} "
                f"{when(W)}?")
    return (f"Following the numbered rules, does the current version of {W.target} {when(W)} "
            f"{'read something other than' if neg else 'read'} \"{q.arg}\"?")


def yn_defs(W, q, neg: bool) -> dict:
    if q.fam == "on":
        on = f"the rules leave flag {W.target} on for {q.key[1]} at that time"
        off = f"the rules leave flag {W.target} off for {q.key[1]} at that time"
        return {"yes": off if neg else on, "no": on if neg else off}
    same = f"after replaying the requests, the current version's content is exactly \"{q.arg}\""
    other = f"the current version's content is something other than \"{q.arg}\""
    return {"yes": other if neg else same, "no": same if neg else other}


def jb_descs(W, q) -> tuple:
    if q.fam == "on":
        return (f"Flag {W.target} is on for {q.key[1]} {when(W)}.", f"Flag {W.target} is off for {q.key[1]} {when(W)}.")
    return (f"The current version of {W.target} reads \"{q.arg}\" {when(W)}.",
            f"The current version of {W.target} does not read \"{q.arg}\" {when(W)}.")


def jb_question(W, q, wording: str) -> str:
    if wording == "fallback":
        s = jb_descs(W, q)[0]
        return f"Statement: {s[0].lower() + s[1:]} Replaying the log under the numbered rules, which option fits?"
    return "Replaying the log under the numbered rules, which statement holds?"


def value_question(W, q) -> str:
    if q.fam == "rollout":
        return f"Following the numbered rules, what is the production rollout percentage of {W.target} {when(W)}?"
    return f"Following the numbered rules, what does the current version of {W.target} read {when(W)}?"


def score_question(W, q) -> str:
    if q.fam == "band":
        return f"Following the numbered rules, which band holds the production rollout of {W.target} {when(W)}?"
    return f"Following the numbered rules, how many versions does {W.target} have {when(W)}?"


Q_PATTERNS = [
    ("yn_on", r"Following the numbered rules, is flag (?P<e>\S+) (?P<w>on|off) for (?P<u>.+?) (?P<when>at the end of the log|as of .+)\?"),
    ("yn_eq", r"Following the numbered rules, does the current version of (?P<e>\S+) (?P<when>at the end of the log|as of .+?) (?P<w>read something other than|read) \"(?P<s>[^\"]+)\"\?"),
    ("jb", r"Replaying the log under the numbered rules, which statement holds\?"),
    ("jbf", r"Statement: (?P<s>.+) Replaying the log under the numbered rules, which option fits\?"),
    ("value_rollout", r"Following the numbered rules, what is the production rollout percentage of (?P<e>\S+) (?P<when>at the end of the log|as of .+)\?"),
    ("value_content", r"Following the numbered rules, what does the current version of (?P<e>\S+) read (?P<when>at the end of the log|as of .+)\?"),
    ("score_band", r"Following the numbered rules, which band holds the production rollout of (?P<e>\S+) (?P<when>at the end of the log|as of .+)\?"),
    ("score_nvers", r"Following the numbered rules, how many versions does (?P<e>\S+) have (?P<when>at the end of the log|as of .+)\?"),
]


def parse_question(s: str):
    for k, pat in Q_PATTERNS:
        m = re.fullmatch(pat, s)
        if m:
            return k, m.groupdict()
    raise ValueError(f"question {s!r}")


JB_PATTERNS = [
    ("on", r"Flag (?P<e>\S+) is on for (?P<u>.+?) (?P<when>at the end of the log|as of .+)\."),
    ("eq", r"The current version of (?P<e>\S+) reads \"(?P<s>[^\"]+)\" (?P<when>at the end of the log|as of .+)\."),
]


# ------------------------------------------------------------------------------------------------ load + plan
TIERS = ("easy", "standard", "judge", "hard")


def tier_of(W, qtype: str) -> str:
    """export_latents draws machine = holdout[i % 2], tier = TIERS[i % 4], kind = (yn, choice, score)[i % 3] from one
    attempt counter i and does not return the tier: recover it from (machine, kind) (i mod 6) and the event count
    (the two tiers left, i mod 12, have disjoint event ranges)."""
    g3 = _g3()
    kinds = ("yn", "value", "score")
    n = len(W.events)
    cands = []
    for r in range(12):
        if g3.MACHINES.holdout[r % len(g3.MACHINES.holdout)] == W.machine and kinds[r % 3] == qtype:
            t = TIERS[r % 4]
            lo, hi = g3.TIER_EVENTS[t]
            cands.append((t, lo <= n <= max(hi, lo)))
    ok = sorted({t for t, fits in cands if fits})
    return ok[0] if len(ok) == 1 else "standard"


def load(n: int = N_EXPORT) -> list:
    xs = _g3().export_latents("devx", n)
    items = []
    for i, x in enumerate(xs):
        W, q = world_from_dict(x["latent"]), query_from_dict(x["query"])
        g = gold_of(W, q)
        assert g == x["gold"], (i, g, x["gold"])
        tier = tier_of(W, q.qtype)
        items.append(dx.Item(f"f3-dx-{i:06d}", tier, W.machine, q.qtype, x["latent"], x["query"], g,
                             {"levels": x["levels"]}))
    return items


LAST_PLAN_REPORT: dict = {}


def plan(items: list, rng) -> list:
    """100 latents in export order: 34 yes/no-type latents (26 yes/no rows with on/off or read/other wording for
    balance + 8 JB-letter rows), 33 choice, 33 score. Formats rotate; yes/no gold balanced by dx.balance_assign."""
    yn_l = [it for it in items if it.kind == "yn"]
    ch_l = [it for it in items if it.kind == "value"][:33]
    # score: levels as even as the export allows (SPEC 4.6), taken in export order with a cap per level
    sc_l, lv = [], Counter()
    for cap in (7, 8, 9, 99):
        for it in items:
            if it.kind == "score" and it not in sc_l and len(sc_l) < 33 and lv[(it.pack, it.gold0)] < cap / 2 + 0.5:
                sc_l.append(it)
                lv[(it.pack, it.gold0)] += 1
    # yes/no-type latents: take them in export order until the truth values are balanced (17 / 17)
    pick, cnt = [], Counter()
    for it in yn_l:
        t = it.gold0 == "yes"
        if cnt[t] < 17:
            pick.append(it)
            cnt[t] += 1
    jb = [it for it in pick if it.gold0 == "yes"][:4] + [it for it in pick if it.gold0 == "no"][:4]
    yn = [it for it in pick if it not in jb]
    rot = dx.Rotor(rng)
    out = []
    for it in ch_l:
        out.append((it, {"v": "choice", "fmt": rot.pick("fmt", FMTS, ("choice",))}))
    for it in sc_l:
        out.append((it, {"v": "score", "fmt": rot.pick("fmt", FMTS, ("score",))}))
    units, meta = [], []
    for it in jb:
        t = it.gold0 == "yes"
        units.append([({"qk": "jb", "fmt": f, "tier": it.tier, "pack": it.pack, "pol": 0}, t) for f in FMTS])
        meta.append((it, [("jb", f, False) for f in FMTS]))
    for it in yn:
        t = it.gold0 == "yes"
        cands, cm = [], []
        for neg in (False, True):
            for f in FMTS:
                cands.append(({"qk": "yn", "fmt": f, "tier": it.tier, "pack": it.pack, "pol": int(neg),
                               "tpl": (it.query["fam"], neg)}, t != neg))
                cm.append(("yn", f, neg))
        units.append(cands)
        meta.append((it, cm))
    ch = dx.balance_assign(units, rng)
    for (it, cm), i in zip(meta, ch):
        v, f, neg = cm[i]
        out.append((it, {"v": v, "fmt": f, "neg": neg}))
    LAST_PLAN_REPORT.clear()
    LAST_PLAN_REPORT.update({"views": dict(Counter(v["v"] for _, v in out))})
    out.sort(key=lambda x: x[0].lid)
    return out


# ------------------------------------------------------------------------------------------------ render
def edges(W) -> tuple:
    M = machine(W.machine)
    _, out = sim.replay(M, W)
    tags = set()
    if any(v == "dup" for v in out.values()):
        tags.add("hc:resend_once")
    if any(v == "guard" for v in out.values()):
        tags.add("hc:guard_fail_noop")
    if any(v == "unknown" for v in out.values()) or W.decoys:
        tags.add("hc:decoy_id")
    if M.expiring(W):
        tags.add("hc:expiry")
    if any(e.kind == "revert" for e in W.events):
        tags.add("hc:revert")
    return tuple(sorted(tags))


def distractors(W, q, gold, pool_fn) -> list:
    """Wrong options: answers of the simulator's misreadings (shortcut solvers), then values that appear in the log."""
    M = machine(W.machine)
    disp = [e.idx for e in sorted(W.events, key=lambda e: (e.ts, e.idx))]
    ip = sim.in_play(M, W, disp)
    out = []
    for name in sim.SHORTCUT_NAMES:
        try:
            a = sim.shortcut_answer(M, W, q, name, disp, ip)
        except Exception:  # noqa: BLE001
            a = None
        if a is not None and a != gold and a not in out:
            out.append(a)
    for v in pool_fn():
        if v != gold and v not in out:
            out.append(v)
    return out


def render(it: dx.Item, view: dict, fb, rng) -> mv.RowSpec:
    W, q = world_from_dict(it.facts), query_from_dict(it.query)
    fmt = view["fmt"]
    state = render_state(W, fmt, rng)
    e = edges(W)
    ne = len(W.events)
    if view["v"] == "yn":
        neg = view["neg"]
        g = (it.gold0 == "yes") != neg
        return mv.RowSpec("base", "yn", state, yn_question(W, q, neg), "yes" if g else "no", FMT_META[fmt],
                          "dx3_" + fmt, f"dx3.yn_{q.fam}{'_neg' if neg else ''}", defs=yn_defs(W, q, neg),
                          polarity=int(neg), role="neg" if neg else "aff", edge=e, n_events=ne)
    if view["v"] == "jb":
        y, n = jb_descs(W, q)
        opts, gold, wording = fb.jb(y, n, it.gold0 == "yes", rng, stratum=("dx3",))
        return mv.RowSpec("jb", "jb", state, jb_question(W, q, wording), gold, FMT_META[fmt], "dx3_" + fmt,
                          "dx3.jb" + ("f" if wording == "fallback" else ""), options=opts, polarity=0, edge=e,
                          n_events=ne)
    if view["v"] == "choice":
        g = it.gold0
        if q.fam == "rollout":
            def pool():
                vals = [x["rollout"] for x in W.ents.values()] + [ev.a["p"] for ev in W.events if ev.kind == "rollout"]
                return vals + [0, 10, 25, 50, 75, 100]
            wrong = distractors(W, q, g, pool)[:4]
            txt = lambda v: f"rollout at {v}%"  # noqa: E731
        else:
            def pool():
                return [x["v1"] for x in W.ents.values()] + [ev.a["lab"] for ev in W.events if ev.kind == "save"] + \
                    list(machine("docs").LABELS)
            wrong = distractors(W, q, g, pool)[:4]
            txt = lambda v: v  # noqa: E731
        opts = fb.place(txt(g), [txt(w) for w in wrong], rng, stratum=("dx3", "value", q.fam))
        return mv.RowSpec("base", "choice", state, value_question(W, q), txt(g), FMT_META[fmt], "dx3_" + fmt,
                          f"dx3.value_{q.fam}", options=opts, edge=e, n_events=ne)
    levels = LEVELS[W.machine]
    opts = fb.score_options(list(levels))
    return mv.RowSpec("base", "score", state, score_question(W, q), levels[it.gold0], FMT_META[fmt], "dx3_" + fmt,
                      f"dx3.score_{q.fam}", options=opts, levels=len(levels), edge=e, n_events=ne)


# ------------------------------------------------------------------------------------------------ parse-back
def _when(W_end, s: str):
    if s == "at the end of the log":
        return True, W_end
    return False, parse_ts_text(s[len("as of "):])


def parse(g: dict) -> dict:
    st = parse_state(g["state"])
    k, d = parse_question(g["instructions"])
    out = {"st": st, "qk": k}
    if k in ("jb", "jbf"):
        s = g["options"][0] if k == "jb" else d["s"]
        if k == "jbf":
            s = s[0].upper() + s[1:]
        for fam, pat in JB_PATTERNS:
            m = re.fullmatch(pat, s)
            if m:
                d = m.groupdict()
                out["fam"] = fam
                break
        else:
            raise ValueError(f"jb statement {s!r}")
    else:
        out["fam"] = {"yn_on": "on", "yn_eq": "eq", "value_rollout": "rollout", "value_content": "content",
                      "score_band": "band", "score_nvers": "nvers"}[k]
    out["at_end"], out["t_q"] = _when(st["t_end"], d["when"])
    out["target"] = d["e"]
    out["user"] = d.get("u")
    out["arg"] = d.get("s")
    out["neg"] = d.get("w") in ("off", "read something other than")
    out["options"] = g["options"]
    if g["card"]:
        out["card"] = mv.card_defs(g["card"])
    return out


def parsed_world(p: dict) -> tuple:
    st = p["st"]
    P = dict(st["params"])
    if st["machine"] == "flags":
        P["user"] = p["user"] or P["users"][0]
        P.setdefault("eng", [])
        P.setdefault("chg_bad", "")
    else:
        P["lock_min"] = st["lock_rule"] if st["lock_rule"] is not None else P["lock_min"]
    W = sim.World(st["machine"], st["t_end"], st["t_end"], p["t_q"], p["at_end"], st["ents"], p["target"], {},
                  st["events"], P, "", [], {}, "iso", [], None)
    fam = p["fam"]
    if fam == "on":
        q = sim.Query("yn", "on", ("on", p["user"]))
    elif fam == "eq":
        q = sim.Query("yn", "eq", ("content", p["target"]), p["arg"])
    elif fam == "rollout":
        q = sim.Query("value", "rollout", ("rollout", p["target"]))
    elif fam == "content":
        q = sim.Query("value", "content", ("content", p["target"]))
    elif fam == "band":
        q = sim.Query("score", "band", ("rollout", p["target"]))
    else:
        q = sim.Query("score", "nvers", ("nvers", p["target"]))
    return W, q


def relabel(p: dict, g: dict):
    W, q = parsed_world(p)
    v = gold_of(W, q)
    if mv.is_undefined(v):
        raise ValueError("decide undefined on the parsed world")
    k = p["qk"]
    if k in ("yn_on", "yn_eq"):
        return "yes" if ((v == "yes") != p["neg"]) else "no"
    if k in ("jb", "jbf"):
        return p["options"][0] if v == "yes" else p["options"][1]
    if k == "value_rollout":
        return f"rollout at {v}%"
    if k == "value_content":
        return v
    return LEVELS[W.machine][v]


def project(it: dx.Item) -> dict:
    W = world_from_dict(it.facts)
    return _proj(W, query_from_dict(it.query))


def project_parsed(p: dict) -> dict:
    W, q = parsed_world(p)
    return _proj(W, q)


def _proj(W, q) -> dict:
    P = W.params
    if W.machine == "flags":
        params = (tuple(P["users"]), tuple(sorted(P["buckets"].items())), tuple(P["chg_ok"]))
    else:
        params = (tuple(P["approvers"]), P["lock_min"], tuple(P["editors"]))
    evs = tuple(sorted((e.ts.isoformat(), e.eid, e.src, e.kind, e.ent, json.dumps(e.a, sort_keys=True))
                       for e in W.events))
    return {"machine": W.machine, "ents": json.dumps(W.ents, sort_keys=True), "target": W.target,
            "t_q": W.t_q.isoformat(), "at_end": W.at_end, "params": params, "events": evs,
            "query": (q.fam, q.key, q.arg if q.fam == "eq" else None)}
