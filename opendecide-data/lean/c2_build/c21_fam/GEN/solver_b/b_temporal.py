"""GEN solver B, TEMPORAL sub-block (TM-T1 .. TM-T4).

Method (G0-lite section 2, solver B column): civil-day-number integer arithmetic (NO calendar library: no datetime, no calendar module),
weekday by modular arithmetic, feasibility by TIME-STEPPED SIMULATION (one minute per step, unlimited parallel workers).

Semantics (SCHEMA.md section 2): proleptic Gregorian, 24-hour clock, fixed UTC offsets.
    TM-T1 offsets are applied in order; a month step keeps the day of month (clamp: use the last day of the month when the day is missing;
          roll: days beyond the month end spill into the next month); business days skip the stated weekend days and holidays and do not count
          the start day.
    TM-T2 duration between two timestamps in absolute time, in the stated format.
    TM-T3 half-open intervals; relations: disjoint with a gap / touching end to start / partial overlap / one contains the other.
    TM-T4 feasible iff all tasks can finish inside the window (earliest start = window start, prerequisites respected); or two half-open
          bookings overlap.
"""
import re

from b_questions import read_question
from bcommon import ParseFail, Reject, statements, pick_unique, norm_text, name_list

# ---------------------------------------------------------------------------------------------------------------------
# civil-day arithmetic (days since 1970-01-01, proleptic Gregorian)


def days_from_civil(y, m, d):
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def civil_from_days(z):
    z += 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    return y + (m <= 2), m, d


def is_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def month_len(y, m):
    if m == 2:
        return 29 if is_leap(y) else 28
    return 30 if m in (4, 6, 9, 11) else 31


def weekday(z):
    """Monday = 0 .. Sunday = 6 (1970-01-01 was a Thursday)."""
    return (z + 3) % 7


def iso(z):
    y, m, d = civil_from_days(z)
    return "%04d-%02d-%02d" % (y, m, d)


DAY_NUM = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}

DATE_RE = re.compile(r"^(\d{4})-(\d\d)-(\d\d)$")
TS_RE = re.compile(r"(\d{4})-(\d\d)-(\d\d) (\d\d):(\d\d) UTC([+-])(\d\d):(\d\d)")
TS_FULL = re.compile(r"^" + TS_RE.pattern + r"$")


def parse_date(s):
    m = DATE_RE.match(s.strip())
    if not m:
        raise ParseFail("bad_date", s)
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not (1 <= mo <= 12 and 1 <= d <= month_len(y, mo)):
        raise ParseFail("impossible_date", s)
    return days_from_civil(y, mo, d)


class TS(object):
    def __init__(self, text):
        m = TS_FULL.match(text.strip())
        if not m:
            raise ParseFail("bad_timestamp", text)
        y, mo, d, hh, mm = [int(m.group(i)) for i in range(1, 6)]
        if not (1 <= mo <= 12 and 1 <= d <= month_len(y, mo) and hh < 24 and mm < 60):
            raise ParseFail("impossible_timestamp", text)
        off = int(m.group(7)) * 60 + int(m.group(8))
        if m.group(6) == "-":
            off = -off
        self.z = days_from_civil(y, mo, d)
        self.hm = "%02d:%02d" % (hh, mm)
        self.minute_of_day = hh * 60 + mm
        self.off = off
        self.date = "%04d-%02d-%02d" % (y, mo, d)

    @property
    def utc_minutes(self):
        return self.z * 1440 + self.minute_of_day - self.off

    def canon(self):
        return {"date": self.date, "hm": self.hm, "off": self.off}


# ---------------------------------------------------------------------------------------------------------------------
# shared sentences

CAL_SENTENCES = [
    re.compile(r"^Use the proleptic Gregorian calendar and a 24-hour clock with no daylight-saving changes$"),
    re.compile(r"^Dates follow the Gregorian calendar extended to all years; the clock is 24-hour and has no daylight-saving shifts$"),
]
HALF_OPEN = [
    re.compile(r"^An interval runs from its start up to but not including its end$"),
    re.compile(r"^Each interval includes its start and excludes its end$"),
]
MONTH_RULE_HEAD = re.compile(r"^(?:A month step keeps the day of month|Adding months keeps the day number)")


def month_rule_of(sentence):
    """The month-step sentence: clamp if it names the month's last day as the fallback, roll if it says days spill / roll over."""
    low = sentence.lower()
    clamp = "last day" in low
    roll = ("spill" in low) or ("roll" in low)
    if clamp == roll:
        raise ParseFail("month_rule_unclear", sentence)
    return "clamp" if clamp else "roll"


WEEKEND_SENT = [re.compile(r"^Weekend days are (?P<d>.+)$"), re.compile(r"^The days off each week are (?P<d>.+)$")]
HOLIDAY_SENT = [re.compile(r"^Holidays are (?P<d>.+)$"), re.compile(r"^These dates are holidays: (?P<d>.+)$")]
NO_HOLIDAY = [re.compile(r"^No date is a holiday$"), re.compile(r"^There are no holidays$")]

TSX = r"\d{4}-\d\d-\d\d \d\d:\d\d UTC[+-]\d\d:\d\d"
NM = r"[a-z][a-z0-9_]*"


def _strip_common(stmts, accept_half_open=False):
    out = []
    for s in stmts:
        if any(r.match(s) for r in CAL_SENTENCES):
            continue
        if accept_half_open and any(r.match(s) for r in HALF_OPEN):
            continue
        out.append(s)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# TM-T1

def _day_list(text):
    out = []
    for w in name_list(text):
        k = w.strip().lower()
        if k not in DAY_NUM:
            raise ParseFail("unknown_weekday", w)
        out.append(DAY_NUM[k])
    return sorted(set(out))


def _date_list(text):
    out = []
    for w in name_list(text):
        out.append(w.strip())
        parse_date(w.strip())
    return out


OFF_PART = re.compile(r"^(\d+) (business days?|days?|weeks?|months?)$")


def parse_offsets(text):
    ops = []
    for part in re.split(r",\s*then\s+", text.strip()):
        m = OFF_PART.match(part.strip())
        if not m:
            raise ParseFail("offset_part", part)
        unit = m.group(2)
        unit = "business_day" if unit.startswith("business") else unit.rstrip("s")
        ops.append({"n": int(m.group(1)), "unit": unit})
    return ops


def add_months(z, n, rule):
    y, m, d = civil_from_days(z)
    t = (y * 12 + (m - 1)) + n
    y2, m2 = t // 12, t % 12 + 1
    dim = month_len(y2, m2)
    if d <= dim:
        return days_from_civil(y2, m2, d)
    if rule == "clamp":
        return days_from_civil(y2, m2, dim)
    if rule == "roll":
        return days_from_civil(y2, m2, 1) + (d - 1)
    raise ParseFail("month_rule_missing", "")


def add_business_days(z, n, weekend, holidays):
    count = 0
    while count < n:
        z += 1
        if weekday(z) in weekend:
            continue
        if z in holidays:
            continue
        count += 1
    return z


def solve_t1(stem, options):
    key, qs, remainder = read_question("q.TM-T1", stem)
    stmts = _strip_common(statements(remainder))
    month_rule, weekend, holidays_txt, q, rest = None, None, None, qs, []
    for s in stmts:
        if MONTH_RULE_HEAD.match(s):
            if month_rule is not None:
                raise ParseFail("month_rule_stated_twice", s)
            month_rule = month_rule_of(s)
            continue
        hit = False
        for rx in WEEKEND_SENT:
            m = rx.match(s)
            if m:
                weekend = _day_list(m.group("d"))
                hit = True
        if hit:
            continue
        for rx in HOLIDAY_SENT:
            m = rx.match(s)
            if m:
                holidays_txt = _date_list(m.group("d"))
                hit = True
        if hit:
            continue
        if any(r.match(s) for r in NO_HOLIDAY):
            holidays_txt = []
            continue
        rest.append(s)
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    ops = parse_offsets(q["offset"])
    start = parse_date(q["start"])
    has_b = any(o["unit"] == "business_day" for o in ops)
    has_m = any(o["unit"] == "month" for o in ops)
    if has_m and month_rule is None:
        raise ParseFail("month_rule_not_stated", "")
    if has_b and weekend is None:
        raise ParseFail("weekend_not_stated", "")
    if has_b and holidays_txt is None:
        raise ParseFail("holidays_not_stated", "")
    hol = set(parse_date(h) for h in (holidays_txt or []))
    z = start
    for o in ops:
        u, n = o["unit"], o["n"]
        if u == "day":
            z += n
        elif u == "week":
            z += 7 * n
        elif u == "month":
            z = add_months(z, n, month_rule)
        elif u == "business_day":
            z = add_business_days(z, n, set(weekend), hol)
    ans = iso(z)
    idx = pick_unique([i for i, o in enumerate(options) if o.strip() == ans], ans)
    pb = {"form": "TM-T1", "start": iso(start), "ops": ops, "month_rule": month_rule if has_m else month_rule,
          "weekend": weekend, "holidays": sorted(holidays_txt) if holidays_txt is not None else None}
    return {"answer_index": idx, "answer_text": ans, "parse": pb, "info": {}}


# ---------------------------------------------------------------------------------------------------------------------
# TM-T2

EVENT_FRAMES = [
    re.compile(r"^(%s) happens at (%s)$" % (NM, TSX)),
    re.compile(r"^(%s) is (%s)$" % (NM, TSX)),
    re.compile(r"^The time of (%s) is (%s)$" % (NM, TSX)),
    re.compile(r"^(%s): (%s)$" % (NM, TSX)),
]
FMT_CODE = {"days, hours and minutes": "dhm", "hours and minutes": "hm", "minutes": "min"}
DUR_PART = re.compile(r"(\d+) (days?|hours?|minutes?)")


def solve_t2(stem, options):
    key, q, remainder = read_question("q.TM-T2", stem)
    stmts = _strip_common(statements(remainder))
    ev, rest = {}, []
    for s in stmts:
        hit = False
        for rx in EVENT_FRAMES:
            m = rx.match(s)
            if m:
                if m.group(1) in ev:
                    raise ParseFail("event_defined_twice", m.group(1))
                ev[m.group(1)] = TS(m.group(2))
                hit = True
                break
        if hit:
            continue
        rest.append(s)
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    a, b, fmt = q["t1"], q["t2"], q["fmt"].strip()
    if a not in ev or b not in ev:
        raise ParseFail("event_not_defined", "")
    if fmt not in FMT_CODE:
        raise ParseFail("unknown_format", fmt)
    total = ev[b].utc_minutes - ev[a].utc_minutes
    if total < 0:
        raise Reject("negative_duration", "")
    code = FMT_CODE[fmt]
    if code == "dhm":
        want = (total // 1440, (total % 1440) // 60, total % 60)
    elif code == "hm":
        want = (0, total // 60, total % 60)
    else:
        want = (0, 0, total)
    hits = []
    for i, o in enumerate(options):
        parts = DUR_PART.findall(o)
        if not parts or DUR_PART.sub("", o).strip():
            raise ParseFail("option_not_a_duration", o)
        d = h = mi = 0
        for n, u in parts:
            if u.startswith("day"):
                d = int(n)
            elif u.startswith("hour"):
                h = int(n)
            else:
                mi = int(n)
        if (d, h, mi) == want:
            hits.append(i)
    idx = pick_unique(hits, str(want))
    pb = {"form": "TM-T2", "events": dict((k, v.canon()) for k, v in ev.items()), "fmt": code, "from": a, "to": b}
    return {"answer_index": idx, "answer_text": options[idx], "parse": pb, "info": {}}


# ---------------------------------------------------------------------------------------------------------------------
# TM-T3

IV_FRAMES = [
    re.compile(r"^(%s): (%s) until (%s)$" % (NM, TSX, TSX)),
    re.compile(r"^(%s) begins (%s) and finishes (%s)$" % (NM, TSX, TSX)),
    re.compile(r"^(%s) runs from (%s) to (%s)$" % (NM, TSX, TSX)),
    re.compile(r"^The span (%s) starts at (%s) and ends at (%s)$" % (NM, TSX, TSX)),
]
RELATIONS = ["disjoint with a gap", "touching end to start", "partial overlap", "one contains the other"]


def relation(s1, e1, s2, e2):
    if e1 <= s2 or e2 <= s1:
        return "touching end to start" if (e1 == s2 or e2 == s1) else "disjoint with a gap"
    if (s1 <= s2 and e2 <= e1) or (s2 <= s1 and e1 <= e2):
        return "one contains the other"
    return "partial overlap"


def solve_t3(stem, options):
    key, q, remainder = read_question("q.TM-T3", stem)
    stmts = _strip_common(statements(remainder), accept_half_open=True)
    iv, rest = {}, []
    for s in stmts:
        hit = False
        for rx in IV_FRAMES:
            m = rx.match(s)
            if m:
                if m.group(1) in iv:
                    raise ParseFail("interval_defined_twice", m.group(1))
                iv[m.group(1)] = (TS(m.group(2)), TS(m.group(3)))
                hit = True
                break
        if hit:
            continue
        rest.append(s)
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    a, b = q["iv1"], q["iv2"]
    if a not in iv or b not in iv:
        raise ParseFail("interval_not_defined", "")
    for k, (s0, e0) in iv.items():
        if not s0.utc_minutes < e0.utc_minutes:
            raise Reject("empty_or_reversed_interval", k)
    r = relation(iv[a][0].utc_minutes, iv[a][1].utc_minutes, iv[b][0].utc_minutes, iv[b][1].utc_minutes)
    idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == r], r)
    pb = {"form": "TM-T3", "intervals": dict((k, {"start": v[0].canon(), "end": v[1].canon()}) for k, v in iv.items()), "asked": [a, b]}
    return {"answer_index": idx, "answer_text": r, "parse": pb, "info": {}}


# ---------------------------------------------------------------------------------------------------------------------
# TM-T4

DUR_TXT = r"(?:\d+ hours?(?: \d+ minutes?)?|\d+ minutes?)"
TASK_FRAMES = [
    (re.compile(r"^Task (%s) takes (%s) and can start at once$" % (NM, DUR_TXT)), None),
    (re.compile(r"^(%s) lasts (%s); it can start as soon as work begins$" % (NM, DUR_TXT)), None),
    (re.compile(r"^(%s) needs (%s) and has no prerequisite$" % (NM, DUR_TXT)), None),
    (re.compile(r"^Task (%s): (%s), no prerequisites$" % (NM, DUR_TXT)), None),
    (re.compile(r"^Task (%s) takes (%s) and starts only after (.+) are done$" % (NM, DUR_TXT)), 3),
    (re.compile(r"^Task (%s) takes (%s) and starts after (.+) are done$" % (NM, DUR_TXT)), 3),
    (re.compile(r"^(%s) needs (%s) and waits for (.+)$" % (NM, DUR_TXT)), 3),
    (re.compile(r"^(%s) lasts (%s); it cannot start before (.+) finish$" % (NM, DUR_TXT)), 3),
    (re.compile(r"^Task (%s): (%s), after (.+)$" % (NM, DUR_TXT)), 3),
]
PARALLEL_SENT = [re.compile(r"^Tasks that are ready may run at the same time, with no limit on how many$"),
                 re.compile(r"^There are enough workers for every task that is ready to run at once$")]
WINDOW_FRAMES = [
    re.compile(r"^Work begins at (%s) and everything must be finished by (%s)$" % (TSX, TSX)),
    re.compile(r"^The window opens at (%s) and closes at (%s); all work must end by then$" % (TSX, TSX)),
    re.compile(r"^(%s) to (%s)$" % (TSX, TSX)),
]
BOOK_FRAMES = [
    re.compile(r"^The booking (%s) starts (%s) and ends (%s)$" % (NM, TSX, TSX)),
    re.compile(r"^Booking (%s) is from (%s) to (%s)$" % (NM, TSX, TSX)),
    re.compile(r"^(%s) holds the slot from (%s) until (%s)$" % (NM, TSX, TSX)),
    re.compile(r"^(%s): (%s) to (%s)$" % (NM, TSX, TSX)),
]


def parse_dur(text):
    tot = 0
    seen = DUR_PART.findall(text)
    if not seen:
        raise ParseFail("bad_duration", text)
    for n, u in seen:
        tot += int(n) * (60 if u.startswith("hour") else 1)
    return tot


def solve_t4(stem, options):
    key, q4, remainder = read_question(["q.TM-T4", "q.TM-T4.overlap"], stem)
    stmts = _strip_common(statements(remainder), accept_half_open=True)
    # the question decides the variant
    plan_q = key == "q.TM-T4"
    ov_q = key != "q.TM-T4"
    body = stmts
    if plan_q:
        tasks, window, rest = [], None, []
        parallel = False
        for s in body:
            hit = False
            if any(r.match(s) for r in PARALLEL_SENT):
                parallel = True
                continue
            for rx, gi in TASK_FRAMES:
                m = rx.match(s)
                if m:
                    after = name_list(m.group(gi)) if gi else []
                    tasks.append({"name": m.group(1), "dur": parse_dur(m.group(2)), "after": after})
                    hit = True
                    break
            if hit:
                continue
            for rx in WINDOW_FRAMES:
                m = rx.match(s)
                if m:
                    if window is not None:
                        raise ParseFail("window_stated_twice", "")
                    window = (TS(m.group(1)), TS(m.group(2)))
                    hit = True
                    break
            if not hit:
                rest.append(s)
        if rest or window is None or not tasks:
            raise ParseFail("unread_sentences", str(rest))
        if not parallel:
            raise ParseFail("parallel_workers_not_stated", "")      # the answer depends on it, so the stem must say it
        names = [t["name"] for t in tasks]
        if len(set(names)) != len(names):
            raise ParseFail("duplicate_task", "")
        for t in tasks:
            for a in t["after"]:
                if a not in names:
                    raise ParseFail("unknown_prerequisite", a)
        span = window[1].utc_minutes - window[0].utc_minutes
        if span <= 0:
            raise Reject("window_not_positive", "")
        if span > 2000000:
            raise Reject("window_too_long_to_simulate", str(span))
        feasible = simulate(tasks, span)
        want = "yes" if feasible else "no"
        idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == want], want)
        pb = {"form": "TM-T4", "variant": "plan", "window": [window[0].canon(), window[1].canon()], "tasks": tasks}
        return {"answer_index": idx, "answer_text": "Yes" if feasible else "No", "parse": pb, "info": {}}
    a, b = q4["b1"], q4["b2"]
    bk, rest = {}, []
    for s in body:
        hit = False
        for rx in BOOK_FRAMES:
            mm = rx.match(s)
            if mm:
                if mm.group(1) in bk:
                    raise ParseFail("booking_defined_twice", mm.group(1))
                bk[mm.group(1)] = (TS(mm.group(2)), TS(mm.group(3)))
                hit = True
                break
        if not hit:
            rest.append(s)
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    if a not in bk or b not in bk:
        raise ParseFail("booking_not_defined", "")
    for k, (s0, e0) in bk.items():
        if not s0.utc_minutes < e0.utc_minutes:
            raise Reject("empty_or_reversed_interval", k)
    s1, e1 = bk[a][0].utc_minutes, bk[a][1].utc_minutes
    s2, e2 = bk[b][0].utc_minutes, bk[b][1].utc_minutes
    over = (s1 < e2) and (s2 < e1)
    want = "yes" if over else "no"
    idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == want], want)
    pb = {"form": "TM-T4", "variant": "overlap", "bookings": dict((k, {"start": v[0].canon(), "end": v[1].canon()}) for k, v in bk.items()),
          "asked": [a, b]}
    return {"answer_index": idx, "answer_text": "Yes" if over else "No", "parse": pb, "info": {}}


def simulate(tasks, span):
    """Minute-by-minute simulation. A task runs in every minute in which all its prerequisites are finished (at the START of that minute)."""
    remaining = dict((t["name"], t["dur"]) for t in tasks)
    after = dict((t["name"], t["after"]) for t in tasks)
    done = set()
    for minute in range(span):
        if len(done) == len(tasks):
            break
        active = [n for n in remaining if n not in done and all(a in done for a in after[n])]
        if not active:
            return False   # deadlock (a cycle)
        fin = []
        for n in active:
            remaining[n] -= 1
            if remaining[n] == 0:
                fin.append(n)
        for n in fin:
            done.add(n)
    return len(done) == len(tasks)


def solve(form, stem, options):
    return {"TM-T1": solve_t1, "TM-T2": solve_t2, "TM-T3": solve_t3, "TM-T4": solve_t4}[form](stem, options)
