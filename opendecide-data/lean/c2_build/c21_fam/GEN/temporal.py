"""GEN / TEMPORAL sub-block. SOLVER A = calendar-library arithmetic (datetime, calendar) and critical-path computation.
Solver B (civil-day-number integer arithmetic, weekday by modular arithmetic, time-stepped feasibility simulation) is NOT here.

Forms: TM-T1 date after an offset, TM-T2 duration between two timestamps, TM-T3 how two intervals relate,
TM-T4 is the plan feasible / do two bookings overlap.
Every row states the calendar rule it needs (month rule, weekend set, holiday list, half-open intervals). Proleptic Gregorian,
24-hour clock, fixed UTC offsets, no daylight saving, no time-zone names.
"""
import calendar
import datetime as dt

from gen_common import Doc, date_jitter, end_block, item_sep, join_names, minutes_jitter, pick_options_ranked, unit_text

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKENDS = [(5, 6), (5, 6), (5, 6), (4, 5), (6,), (5,)]
REL = ["disjoint with a gap", "touching end to start", "partial overlap", "one contains the other"]
MONTH_RULES = ["clamp", "roll"]


# ------------------------------------------------------------------------------------------------
# Dates
# ------------------------------------------------------------------------------------------------
def d_of(s):
    return dt.date.fromisoformat(s)


def rand_date(rng, special=0.1):
    if rng.random() < special:
        y = rng.choice([1899, 1900, 1901, 1999, 2000, 2001, 2099, 2100, 2101, 2023, 2024, 2027, 2028])
    else:
        y = rng.randint(1996, 2052)
    return dt.date(y, rng.randint(1, 12), rng.randint(1, 28))


def add_months(d, n, rule):
    total = d.year * 12 + (d.month - 1) + n
    y, m = divmod(total, 12)
    m += 1
    dim = calendar.monthrange(y, m)[1]
    if d.day <= dim:
        return dt.date(y, m, d.day)
    if rule == "clamp":
        return dt.date(y, m, dim)
    return dt.date(y, m, dim) + dt.timedelta(days=d.day - dim)


def add_business(d, n, weekend, holidays):
    cur, k = d, 0
    hol = set(holidays)
    while k < n:
        cur += dt.timedelta(days=1)
        if cur.weekday() not in weekend and cur not in hol:
            k += 1
    return cur


def apply_ops(start, ops, rule, weekend, holidays):
    cur = start
    for op in ops:
        u, n = op["unit"], op["n"]
        if u == "day":
            cur += dt.timedelta(days=n)
        elif u == "week":
            cur += dt.timedelta(weeks=n)
        elif u == "month":
            cur = add_months(cur, n, rule)
        else:
            cur = add_business(cur, n, weekend, [d_of(h) for h in holidays])
    return cur


def solve_t1(spec):
    """SOLVER A for TM-T1."""
    return apply_ops(d_of(spec["start"]), spec["ops"], spec["month_rule"], tuple(spec["weekend"]), spec["holidays"]).isoformat()


# ---- flawed calendars --------------------------------------------------------------------------
def _dim_noleap(y, m):
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]


def add_days_noleap(ymd, n):
    y, m, d = ymd
    for _ in range(n):
        d += 1
        if d > _dim_noleap(y, m):
            d = 1
            m += 1
            if m > 12:
                m = 1
                y += 1
    return (y, m, d)


def flawed_t1(spec):
    """{flaw: iso date string} for the flawed solvers that apply to this spec."""
    start = d_of(spec["start"])
    ops, rule, weekend, hol = spec["ops"], spec["month_rule"], tuple(spec["weekend"]), spec["holidays"]
    correct = solve_t1(spec)
    out = {}
    # off by one day
    c = d_of(correct)
    out["off_by_one_day"] = (c + dt.timedelta(days=rng_sign(spec))).isoformat()
    # other month rule
    if rule:
        other = "roll" if rule == "clamp" else "clamp"
        out["wrong_clamp"] = apply_ops(start, ops, other, weekend, hol).isoformat()
    # inclusive start
    ops2 = [dict(o, n=o["n"] - 1) if o["unit"] != "month" and o["n"] > 1 else dict(o) for o in ops]
    out["inclusive_start"] = apply_ops(start, ops2, rule, weekend, hol).isoformat()
    if any(o["unit"] == "business_day" for o in ops):
        out["business_as_calendar"] = apply_ops(start, [dict(o, unit="day") if o["unit"] == "business_day" else o for o in ops], rule, weekend, hol).isoformat()
        out["holiday_ignored"] = apply_ops(start, ops, rule, weekend, []).isoformat()
        out["weekend_default"] = apply_ops(start, ops, rule, (5, 6), hol).isoformat()
    # leap day forgotten: only for pure day/week chains
    if all(o["unit"] in ("day", "week") for o in ops):
        total = sum(o["n"] * (7 if o["unit"] == "week" else 1) for o in ops)
        if total > 0:
            y, m, d = add_days_noleap((start.year, start.month, start.day), total)
            try:
                out["leap_forgotten"] = dt.date(y, m, d).isoformat()
            except ValueError:
                pass
    # --- symmetry (skeptic fix 18 Oct): every error model above lands at a fixed side of the correct date, and "off_by_one_day" is the only option
    # within a day of another one, so the correct option was the one with a neighbour (option-only probe 80 percent). Real solvers combine
    # slips, so each base slip also comes in a one-day-off compound and "later" counterparts exist. Nothing here changes a label.
    base = dict(out)
    plus = {"inclusive_start": "exclusive_start_plus", "business_as_calendar": "business_as_calendar_plus", "holiday_ignored": "holiday_double_counted",
            "weekend_default": "weekend_default_plus", "wrong_clamp": "wrong_clamp_plus", "leap_forgotten": "leap_forgotten_plus",
            "off_by_one_day": "off_by_two_days"}
    for name, v in base.items():
        d = d_of(v)
        sign = (1 if d > c else -1) if name == "off_by_one_day" else (1 if hash_str(spec["start"] + name) % 2 else -1)
        out[plus[name]] = (d + dt.timedelta(days=sign)).isoformat()
    # unit / order slips: far from the correct date, on either side
    if any(o["unit"] == "month" for o in ops):
        out["month_as_30_days"] = apply_ops(start, [dict(o, unit="day", n=30 * o["n"]) if o["unit"] == "month" else o for o in ops], rule, weekend, hol).isoformat()
    if any(o["unit"] == "week" for o in ops):
        out["week_as_5_days"] = apply_ops(start, [dict(o, unit="day", n=5 * o["n"]) if o["unit"] == "week" else o for o in ops], rule, weekend, hol).isoformat()
        out["week_as_8_days"] = apply_ops(start, [dict(o, unit="day", n=8 * o["n"]) if o["unit"] == "week" else o for o in ops], rule, weekend, hol).isoformat()
    if len(ops) > 1:
        out["only_first_step"] = apply_ops(start, ops[:1], rule, weekend, hol).isoformat()
        out["steps_reversed"] = apply_ops(start, list(reversed(ops)), rule, weekend, hol).isoformat()
    if any(o["unit"] == "business_day" for o in ops):
        out["business_as_calendar_plus_week"] = (d_of(out["business_as_calendar"]) + dt.timedelta(days=7)).isoformat() if "business_as_calendar" in out else correct
    # "later" counterparts of the inclusive / exclusive slip (n + 1 instead of n - 1) for day / week chains
    ops3 = [dict(o, n=o["n"] + 1) if o["unit"] != "month" else dict(o) for o in ops]
    out["exclusive_start_plus_one"] = apply_ops(start, ops3, rule, weekend, hol).isoformat()
    return {k: v for k, v in out.items() if v != correct}


def rng_sign(spec):
    return 1 if (hash_str(spec["start"]) % 2) else -1


def hash_str(s):
    h = 0
    for ch in s:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return h


def offset_text(ops):
    parts = []
    for o in ops:
        u = {"day": "day", "week": "week", "month": "month", "business_day": "business day"}[o["unit"]]
        parts.append("%d %s%s" % (o["n"], u, "" if o["n"] == 1 else "s"))
    return ", then ".join(parts)


def make_t1(rng, namer, bin_name, balancer, scope):
    for _ in range(400):
        start = rand_date(rng)
        if bin_name == "easy":
            ops = [rng.choice([{"unit": "day", "n": rng.randint(5, 400)}, {"unit": "week", "n": rng.randint(1, 60)}])]
        elif bin_name == "mid":
            c = rng.choice(["month", "business", "two"])
            if c == "month":
                ops = [{"unit": "month", "n": rng.randint(1, 20)}]
            elif c == "business":
                ops = [{"unit": "business_day", "n": rng.randint(3, 40)}]
            else:
                ops = [{"unit": rng.choice(["week", "month"]), "n": rng.randint(1, 10)}, {"unit": "day", "n": rng.randint(2, 60)}]
        else:
            order = rng.choice([["month", "business_day"], ["business_day", "month"], ["month", "week", "business_day"], ["month", "day", "business_day"]])
            ops = [{"unit": u, "n": rng.randint(1, 14) if u in ("month", "week") else rng.randint(3, 40)} for u in order]
        has_month = any(o["unit"] == "month" for o in ops)
        has_bus = any(o["unit"] == "business_day" for o in ops)
        if has_month and ops[0]["unit"] == "month" and rng.random() < 0.55:
            # make the month rule matter: start on the 31st and land in a month with 30 days or fewer
            for _k in range(30):
                st0 = dt.date(rng.randint(1996, 2052), rng.choice([1, 3, 5, 7, 8, 10, 12]), 31)
                nn = rng.randint(1, 20)
                land = add_months(dt.date(st0.year, st0.month, 28), nn, "clamp")
                if calendar.monthrange(land.year, land.month)[1] < 31:
                    start = st0
                    ops[0]["n"] = nn
                    break
        if has_month and ops[0]["unit"] == "month" and rng.random() < 0.6:
            dim = calendar.monthrange(start.year, start.month)[1]
            start = dt.date(start.year, start.month, rng.randint(min(29, dim), dim))
        rule = rng.choice(MONTH_RULES) if has_month else None
        weekend = rng.choice(WEEKENDS) if has_bus else (5, 6)
        spec = {"version": 1, "form": "TM-T1", "start": start.isoformat(), "ops": ops, "month_rule": rule, "weekend": list(weekend), "holidays": []}
        if has_bus:
            # holidays on business days between the business op's start and its no-holiday end
            d0 = d_of(spec["start"])
            for o in ops:
                if o["unit"] == "business_day":
                    break
                d0 = apply_ops(d0, [o], rule, weekend, [])
            d1 = apply_ops(d0, [o], rule, weekend, [])
            span = (d1 - d0).days
            nh = rng.randint(0, 3)
            hols = set()
            for _h in range(nh * 3):
                if len(hols) == nh or span < 2:
                    break
                cand = d0 + dt.timedelta(days=rng.randint(1, span))
                if cand.weekday() not in weekend:
                    hols.add(cand.isoformat())
            spec["holidays"] = sorted(hols)
        correct = solve_t1(spec)
        fl = flawed_t1(spec)
        # distinct values, distinct types
        chosen = pick_options_ranked(correct, {t: [v] for t, v in fl.items()}, 4, rng, balancer, scope, jitter=date_jitter)
        if chosen is None:
            continue
        score = len(ops) + (1 if has_month else 0) + (2 if has_bus else 0) + len(spec["holidays"])
        return {"spec": spec, "answer": correct, "options": [{"text": correct, "trap": None, "correct": True}] +
                [{"text": v, "trap": t, "correct": False} for v, t in chosen], "score": score}
    return None


def perturb_t1(item, rng, balancer, scope):
    spec = item["spec"]
    old = solve_t1(spec)
    edits = []
    for i, o in enumerate(spec["ops"]):
        for d in (-3, -2, -1, 1, 2, 3):
            if o["n"] + d >= 1:
                edits.append(("n", i, o["n"] + d))
    if spec["month_rule"]:
        edits.append(("rule", None, "roll" if spec["month_rule"] == "clamp" else "clamp"))
    for i in range(len(spec["holidays"])):
        edits.append(("drop_hol", i, None))
    edits.append(("start", None, 1))
    rng.shuffle(edits)
    for kind, i, v in edits:
        s2 = {k: (list(x) if isinstance(x, list) else x) for k, x in spec.items()}
        s2["ops"] = [dict(o) for o in spec["ops"]]
        if kind == "n":
            s2["ops"][i]["n"] = v
        elif kind == "rule":
            s2["month_rule"] = v
        elif kind == "drop_hol":
            s2["holidays"] = [h for j, h in enumerate(spec["holidays"]) if j != i]
        else:
            s2["start"] = (d_of(spec["start"]) + dt.timedelta(days=v)).isoformat()
        new = solve_t1(s2)
        if new == old:
            continue
        fl = flawed_t1(s2)
        chosen = pick_options_ranked(new, {t: [v] for t, v in fl.items()}, 4, rng, balancer, scope, jitter=date_jitter)
        if chosen is None:
            continue
        return {"spec": s2, "answer": new, "options": [{"text": new, "trap": None, "correct": True}] +
                [{"text": v2, "trap": t, "correct": False} for v2, t in chosen], "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# Timestamps with fixed UTC offsets
# ------------------------------------------------------------------------------------------------
def ts_obj(ts):
    """ts = {'date': 'YYYY-MM-DD', 'hm': 'HH:MM', 'off': minutes}"""
    h, m = ts["hm"].split(":")
    tz = dt.timezone(dt.timedelta(minutes=ts["off"]))
    return dt.datetime.fromisoformat(ts["date"]).replace(hour=int(h), minute=int(m), tzinfo=tz)


def off_text(off):
    sign = "+" if off >= 0 else "-"
    a = abs(off)
    return "UTC%s%02d:%02d" % (sign, a // 60, a % 60)


def ts_text(ts):
    return "%s %s %s" % (ts["date"], ts["hm"], off_text(ts["off"]))


def make_ts(d, minute_of_day, off):
    return {"date": d.isoformat(), "hm": "%02d:%02d" % (minute_of_day // 60, minute_of_day % 60), "off": off}


def from_utc(utc_dt, off):
    loc = utc_dt.astimezone(dt.timezone(dt.timedelta(minutes=off)))
    return {"date": loc.date().isoformat(), "hm": "%02d:%02d" % (loc.hour, loc.minute), "off": off}


OFFSETS = [-480, -420, -360, -300, -240, -180, -60, 0, 60, 120, 180, 240, 330, 345, 480, 540, 600]


def local_naive(ts):
    return ts_obj(ts).replace(tzinfo=None)


def fmt_duration(minutes, fmt):
    if fmt == "min":
        return "%d minutes" % minutes if minutes != 1 else "1 minute"
    if fmt == "hm":
        h, m = divmod(minutes, 60)
        return "%d %s %d %s" % (h, "hour" if h == 1 else "hours", m, "minute" if m == 1 else "minutes")
    d, rem = divmod(minutes, 1440)
    h, m = divmod(rem, 60)
    return "%d %s %d %s %d %s" % (d, "day" if d == 1 else "days", h, "hour" if h == 1 else "hours", m, "minute" if m == 1 else "minutes")


FMT_PHRASE = {"dhm": "days, hours and minutes", "hm": "hours and minutes", "min": "minutes"}


def duration_minutes(spec):
    """SOLVER A for TM-T2."""
    return int((ts_obj(spec["t2"]) - ts_obj(spec["t1"])).total_seconds() // 60)


def feb29_between(a, b):
    n = 0
    for y in range(a.year, b.year + 1):
        if calendar.isleap(y):
            d = dt.date(y, 2, 29)
            if a.date() <= d <= b.date():
                n += 1
    return n


def flawed_t2(spec):
    t1, t2 = spec["t1"], spec["t2"]
    correct = duration_minutes(spec)
    out = {}
    out["offset_ignored"] = int((local_naive(t2) - local_naive(t1)).total_seconds() // 60)
    out["offset_sign_flipped"] = correct + 2 * (t2["off"] - t1["off"])
    out["off_by_one_day"] = correct + 1440
    out["inclusive_day"] = correct - 1440
    out["dst_shift"] = correct + 60
    nf = feb29_between(ts_obj(t1), ts_obj(t2))
    if nf:
        out["leap_forgotten"] = correct - 1440 * nf
    # compound readings (two slips at once) keep the correct duration from being the one every wrong option differs from in one place only
    out["offset_ignored_plus_day"] = out["offset_ignored"] + 1440
    out["dst_minus_day"] = correct + 60 - 1440
    out["minute_misread"] = correct + (30 if (t1["off"] + t2["off"]) % 90 == 0 else -30)
    if t1["off"] != t2["off"]:
        out["sign_flipped_plus_dst"] = out["offset_sign_flipped"] + 60
    if nf:
        out["leap_and_dst"] = correct - 1440 * nf + 60
    out = {k: v for k, v in out.items() if v != correct and v > 0}
    return out


def make_t2(rng, namer, bin_name, balancer, scope):
    for _ in range(400):
        d1 = rand_date(rng, 0.15)
        off1 = rng.choice(OFFSETS) if bin_name != "easy" else 0
        off2 = off1 if bin_name == "easy" else rng.choice(OFFSETS)
        if bin_name == "easy":
            span = rng.randint(60, 3 * 1440)
        elif bin_name == "mid":
            span = rng.randint(1440, 60 * 1440)
        else:
            span = rng.randint(30 * 1440, 800 * 1440)
        if bin_name == "hard" and rng.random() < 0.5:
            # make the span cross a 29 Feb of a leap year
            y = rng.choice([2024, 2028, 2000, 2020, 2032, 2040])
            d1 = dt.date(y, 2, 29) - dt.timedelta(days=rng.randint(10, 300))
            span = rng.randint(320, 700) * 1440
        t1 = make_ts(d1, rng.randrange(0, 1440, 5), off1)
        utc2 = ts_obj(t1) + dt.timedelta(minutes=span + rng.randrange(0, 1440, 5))
        t2 = from_utc(utc2, off2)
        if abs(ts_obj(t2).year - 2000) > 60:
            continue
        fmt = rng.choice(["dhm", "dhm", "hm", "min"] if bin_name != "easy" else ["hm", "min", "dhm"])
        names = [namer.lower("event", "a"), namer.lower("event", "b")]
        spec = {"version": 1, "form": "TM-T2", "t1": t1, "t2": t2, "fmt": fmt, "names": names}
        correct = duration_minutes(spec)
        if correct <= 0:
            continue
        fl = flawed_t2(spec)
        chosen = pick_options_ranked(correct, {t: [v] for t, v in fl.items()}, 4, rng, balancer, scope, jitter=minutes_jitter)
        if chosen is None:
            continue
        score = 1 + (off1 != off2) * 2 + (span > 30 * 1440) + (fmt == "dhm")
        txt = lambda m: fmt_duration(m, fmt)
        return {"spec": spec, "answer": txt(correct), "options": [{"text": txt(correct), "trap": None, "correct": True}] +
                [{"text": txt(v), "trap": t, "correct": False} for v, t in chosen], "score": score}
    return None


def perturb_t2(item, rng, balancer, scope):
    spec = item["spec"]
    old = duration_minutes(spec)
    cands = [("t2_min", d) for d in (-90, -45, -30, -15, 15, 30, 45, 90)] + [("t2_day", d) for d in (-1, 1)] + [("off2", d) for d in (-60, 60)]
    rng.shuffle(cands)
    for kind, d in cands:
        s2 = dict(spec)
        if kind == "off2":
            s2["t2"] = dict(spec["t2"], off=spec["t2"]["off"] + d)
        else:
            delta = dt.timedelta(minutes=d) if kind == "t2_min" else dt.timedelta(days=d)
            s2["t2"] = from_utc(ts_obj(spec["t2"]) + delta, spec["t2"]["off"])
        new = duration_minutes(s2)
        if new == old or new <= 0:
            continue
        fl = flawed_t2(s2)
        chosen = pick_options_ranked(new, {t: [v] for t, v in fl.items()}, 4, rng, balancer, scope, jitter=minutes_jitter)
        if chosen is None:
            continue
        f = spec["fmt"]
        return {"spec": s2, "answer": fmt_duration(new, f), "options": [{"text": fmt_duration(new, f), "trap": None, "correct": True}] +
                [{"text": fmt_duration(v, f), "trap": t, "correct": False} for v, t in chosen], "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# T3 interval relations (half-open intervals, absolute time)
# ------------------------------------------------------------------------------------------------
def relation(s1, e1, s2, e2):
    """SOLVER A for TM-T3 on absolute minutes."""
    if e1 < s2 or e2 < s1:
        return "disjoint with a gap"
    if e1 == s2 or e2 == s1:
        return "touching end to start"
    if (s1 <= s2 and e2 <= e1) or (s2 <= s1 and e1 <= e2):
        return "one contains the other"
    return "partial overlap"


def iv_minutes(spec):
    out = []
    for iv in (spec["iv1"], spec["iv2"]):
        out.append((int(ts_obj(iv["start"]).timestamp() // 60), int(ts_obj(iv["end"]).timestamp() // 60)))
    return out


def solve_t3(spec):
    (s1, e1), (s2, e2) = iv_minutes(spec)
    return relation(s1, e1, s2, e2)


def flawed_t3(spec):
    (s1, e1), (s2, e2) = iv_minutes(spec)
    truth = relation(s1, e1, s2, e2)
    out = {}
    # inclusive end: closed intervals share the boundary instant
    if e1 < s2 or e2 < s1:
        out["inclusive_end"] = truth
    else:
        r = relation(s1, e1 + 1, s2, e2 + 1) if False else None
        closed_touch = (e1 == s2 or e2 == s1)
        if closed_touch:
            out["inclusive_end"] = "partial overlap"
        else:
            out["inclusive_end"] = truth
    # local clock readings instead of absolute time
    a = [(local_naive(spec["iv1"]["start"]), local_naive(spec["iv1"]["end"])), (local_naive(spec["iv2"]["start"]), local_naive(spec["iv2"]["end"]))]
    m = lambda x: int(x.replace(tzinfo=dt.timezone.utc).timestamp() // 60)
    out["ignore_offsets"] = relation(m(a[0][0]), m(a[0][1]), m(a[1][0]), m(a[1][1]))
    out["nested_as_overlap"] = "partial overlap" if truth == "one contains the other" else truth
    gap = min(abs(s2 - e1), abs(s1 - e2))
    out["near_gap_as_touching"] = "touching end to start" if (truth == "disjoint with a gap" and gap <= 120) else truth
    out["touch_as_gap"] = "disjoint with a gap" if truth == "touching end to start" else truth
    out["overlap_as_nested"] = "one contains the other" if truth == "partial overlap" else truth
    ovl = min(e1, e2) - max(s1, s2)
    out["tiny_overlap_as_touching"] = "touching end to start" if (truth == "partial overlap" and ovl <= 30) else truth
    same_day = ts_obj(spec["iv1"]["start"]).date() == ts_obj(spec["iv2"]["start"]).date()
    out["same_day_as_overlap"] = "partial overlap" if (truth == "disjoint with a gap" and same_day) else truth
    # one endpoint misread: the set of relations that can result, split by what was misread
    mis = {"start_misread_hour": set(), "end_misread_hour": set(), "endpoint_day_misread": set()}
    for k in (0, 1):
        for j in (0, 1):
            for d in (-1440, -120, -60, 60, 120, 1440):
                vals = [[s1, e1], [s2, e2]]
                vals[k][j] += d
                if vals[k][1] > vals[k][0]:
                    r = relation(vals[0][0], vals[0][1], vals[1][0], vals[1][1])
                    if r != truth:
                        key = "endpoint_day_misread" if abs(d) == 1440 else ("start_misread_hour" if j == 0 else "end_misread_hour")
                        mis[key].add(r)
    out.update(mis)
    return out


def make_t3(rng, namer, bin_name, want, balancer, scope):
    for _ in range(400):
        base = rand_date(rng, 0.05)
        off1 = rng.choice(OFFSETS) if bin_name != "easy" else 0
        off2 = off1 if bin_name == "easy" else rng.choice(OFFSETS)
        t0 = dt.datetime(base.year, base.month, base.day, 6, 0, tzinfo=dt.timezone.utc)
        L1 = rng.randrange(60, 8 * 60, 15)
        s1 = 0
        e1 = L1
        if want == "disjoint with a gap":
            gap = rng.choice([5, 15, 30, 45, 60, 90, 240]) if bin_name != "easy" else rng.choice([60, 120, 240])
            s2 = e1 + gap
            e2 = s2 + rng.randrange(30, 6 * 60, 15)
        elif want == "touching end to start":
            s2 = e1
            e2 = s2 + rng.randrange(30, 6 * 60, 15)
        elif want == "partial overlap":
            s2 = s1 + rng.randrange(15, L1, 15)
            e2 = e1 + rng.randrange(15, 4 * 60, 15)
        else:
            s2 = s1 + rng.randrange(15, max(30, L1 - 14), 15)
            e2 = s2 + rng.randrange(15, max(30, L1 - (s2 - s1)), 15)
            e2 = min(e2, e1)
            if e2 <= s2:
                continue
        if rng.random() < 0.5:
            (s1, e1), (s2, e2) = (s2, e2), (s1, e1)
        mk = lambda s, e, off: {"start": from_utc(t0 + dt.timedelta(minutes=s), off), "end": from_utc(t0 + dt.timedelta(minutes=e), off)}
        spec = {"version": 1, "form": "TM-T3", "iv1": mk(s1, e1, off1), "iv2": mk(s2, e2, off2),
                "names": [namer.lower("event", "a"), namer.lower("event", "b")]}
        if solve_t3(spec) != want:
            continue
        fl = flawed_t3(spec)
        wrong = [r for r in REL if r != want]
        traps = []
        for w in wrong:
            ft = [f for f, o in fl.items() if w in (o if isinstance(o, set) else {o})]
            traps.append(balancer.pick(scope, ft) if ft else "unmodelled")
        if any(t == "unmodelled" for t in traps) and rng.random() < 0.9:
            continue
        return {"spec": spec, "answer": want, "options": [{"text": want, "trap": None, "correct": True}] +
                [{"text": w, "trap": tr, "correct": False} for w, tr in zip(wrong, traps)], "score": 2 + (off1 != off2) * 2 + (bin_name == "hard")}
    return None


def perturb_t3(item, rng, balancer, scope):
    spec = item["spec"]
    old = solve_t3(spec)
    cands = [(iv, which, d) for iv in ("iv1", "iv2") for which in ("start", "end") for d in (-60, -30, -15, -1, 1, 15, 30, 60)]
    rng.shuffle(cands)
    for iv, which, d in cands:
        s2 = dict(spec)
        s2[iv] = dict(spec[iv])
        s2[iv][which] = from_utc(ts_obj(spec[iv][which]) + dt.timedelta(minutes=d), spec[iv][which]["off"])
        (a, b), (c, e) = iv_minutes(s2)
        if b <= a or e <= c:
            continue
        new = solve_t3(s2)
        if new == old:
            continue
        fl = flawed_t3(s2)
        wrong = [r for r in REL if r != new]
        traps = []
        for w in wrong:
            ft = [f for f, o in fl.items() if w in (o if isinstance(o, set) else {o})]
            traps.append(balancer.pick(scope, ft) if ft else "unmodelled")
        return {"spec": s2, "answer": new, "options": [{"text": new, "trap": None, "correct": True}] +
                [{"text": w, "trap": tr, "correct": False} for w, tr in zip(wrong, traps)], "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# T4 feasibility of a plan / overlap of two bookings
# ------------------------------------------------------------------------------------------------
def critical_path(tasks):
    """tasks: [{'name','dur','after':[names]}] in topological order. Returns minimum makespan (minutes)."""
    fin = {}
    for t in tasks:
        start = max([fin[a] for a in t["after"]] or [0])
        fin[t["name"]] = start + t["dur"]
    return max(fin.values())


def critical_path_flawed(tasks, flaw):
    if flaw == "serial_sum":
        return sum(t["dur"] for t in tasks)
    if flaw == "longest_task":
        return max(t["dur"] for t in tasks)
    if flaw == "sequential_prereqs":
        fin = {}
        for x in tasks:
            fin[x["name"]] = x["dur"] + sum(fin[a] for a in x["after"])
        return max(fin.values())
    if flaw == "drop_dependency":
        best = None
        for i, t in enumerate(tasks):
            for a in t["after"]:
                t2 = [dict(x) for x in tasks]
                t2[i]["after"] = [x for x in t["after"] if x != a]
                v = critical_path(t2)
                best = v if best is None else min(best, v)
        return best if best is not None else critical_path(tasks)
    raise ValueError(flaw)


def dur_text(minutes):
    h, m = divmod(minutes, 60)
    if h and m:
        return "%d %s %d %s" % (h, "hour" if h == 1 else "hours", m, "minute" if m == 1 else "minutes")
    if h:
        return "%d %s" % (h, "hour" if h == 1 else "hours")
    return "%d %s" % (m, "minute" if m == 1 else "minutes")


def solve_t4(spec):
    """SOLVER A for TM-T4."""
    if spec["variant"] == "plan":
        w = int((ts_obj(spec["win_end"]) - ts_obj(spec["win_start"])).total_seconds() // 60)
        return "yes" if critical_path(spec["tasks"]) <= w else "no"
    (s1, e1), (s2, e2) = [(int(ts_obj(b["start"]).timestamp() // 60), int(ts_obj(b["end"]).timestamp() // 60)) for b in (spec["b1"], spec["b2"])]
    return "yes" if max(s1, s2) < min(e1, e2) else "no"


def flawed_t4(spec):
    out = {}
    if spec["variant"] == "plan":
        w = int((ts_obj(spec["win_end"]) - ts_obj(spec["win_start"])).total_seconds() // 60)
        for f in ("serial_sum", "longest_task", "drop_dependency", "sequential_prereqs"):
            out[f] = "yes" if critical_path_flawed(spec["tasks"], f) <= w else "no"
        return out
    (s1, e1), (s2, e2) = [(int(ts_obj(b["start"]).timestamp() // 60), int(ts_obj(b["end"]).timestamp() // 60)) for b in (spec["b1"], spec["b2"])]
    out["inclusive_end"] = "yes" if max(s1, s2) <= min(e1, e2) else "no"
    a = [(local_naive(b["start"]), local_naive(b["end"])) for b in (spec["b1"], spec["b2"])]
    m = lambda x: int(x.replace(tzinfo=dt.timezone.utc).timestamp() // 60)
    out["ignore_offsets"] = "yes" if max(m(a[0][0]), m(a[1][0])) < min(m(a[0][1]), m(a[1][1])) else "no"
    out["same_day_means_overlap"] = "yes" if (a[0][0].date() == a[1][0].date() or a[0][1].date() == a[1][1].date()) else "no"
    ovl = min(e1, e2) - max(s1, s2)
    out["tiny_overlap_ignored"] = "yes" if ovl >= 30 else "no"
    nested = (s1 <= s2 and e2 <= e1) or (s2 <= s1 and e1 <= e2)
    out["nested_not_overlap"] = "no" if nested else ("yes" if max(s1, s2) < min(e1, e2) else "no")
    return out


def make_t4(rng, namer, bin_name, want_yes, balancer, scope, variant=None):
    variant = variant or ("plan" if rng.random() < 0.7 else "overlap")
    for _ in range(400):
        base = rand_date(rng, 0.05)
        t0 = dt.datetime(base.year, base.month, base.day, 8, 0, tzinfo=dt.timezone.utc)
        if variant == "plan":
            off = rng.choice(OFFSETS) if bin_name != "easy" else 0
            nt = {"easy": 3, "mid": rng.choice([4, 5]), "hard": rng.choice([5, 6])}[bin_name]
            names = [namer.lower("event", "t%d" % i) for i in range(nt)]
            tasks = []
            for i in range(nt):
                k = rng.randint(0, min(2, i)) if i else 0
                after = sorted(rng.sample(names[:i], k)) if k else []
                tasks.append({"name": names[i], "dur": rng.randrange(30, 4 * 60 + 1, 15), "after": after})
            cp = critical_path(tasks)
            fls = [f for f in ("serial_sum", "longest_task", "drop_dependency", "sequential_prereqs")]
            rng.shuffle(fls)
            ok = False
            for f in fls:
                fv = critical_path_flawed(tasks, f)
                if want_yes and fv > cp:
                    lo, hi = cp, fv - 1
                elif (not want_yes) and fv < cp:
                    lo, hi = fv, cp - 1
                else:
                    continue
                if hi < lo:
                    continue
                cands = [x for x in range(lo - lo % 5 + 5, hi + 1, 5) if lo <= x <= hi] or [lo, hi]
                W = rng.choice(cands)
                if W <= 0:
                    continue
                ok = True
                break
            if not ok:
                # no flawed reading falls on the other side of any window: use a near-miss margin window (class independent of structure)
                if want_yes:
                    W = cp + rng.choice([5, 10, 15, 30])
                elif cp > 20:
                    W = cp - rng.choice([5, 10, 15])
                else:
                    continue
                if W <= 0:
                    continue
                margin_only = True
            else:
                margin_only = False
            start = from_utc(t0, off)
            end = from_utc(t0 + dt.timedelta(minutes=W), off)
            spec = {"version": 1, "form": "TM-T4", "variant": "plan", "tasks": tasks, "win_start": start, "win_end": end}
            score = nt + sum(len(t["after"]) for t in tasks)
        else:
            off1 = rng.choice(OFFSETS)
            off2 = rng.choice(OFFSETS) if bin_name != "easy" else off1
            L1 = rng.randrange(60, 6 * 60, 15)
            if want_yes:
                s2 = rng.randrange(15, L1, 15)
                e2 = s2 + rng.randrange(30, 5 * 60, 15)
            else:
                s2 = L1 + rng.choice([0, 0, 15, 30, 60, 120])
                e2 = s2 + rng.randrange(30, 5 * 60, 15)
            if rng.random() < 0.5:
                s1, e1, s2, e2 = s2, e2, 0, L1
            else:
                s1, e1 = 0, L1
            mk = lambda s, e, off: {"start": from_utc(t0 + dt.timedelta(minutes=s), off), "end": from_utc(t0 + dt.timedelta(minutes=e), off)}
            spec = {"version": 1, "form": "TM-T4", "variant": "overlap", "b1": mk(s1, e1, off1), "b2": mk(s2, e2, off2),
                    "names": [namer.lower("event", "a"), namer.lower("event", "b")]}
            score = 3 + (off1 != off2) * 2 + (bin_name == "hard")
        if (solve_t4(spec) == "yes") != want_yes:
            continue
        fl = flawed_t4(spec)
        correct, wrong = ("yes", "no") if want_yes else ("no", "yes")
        ft = [f for f, o in fl.items() if o == wrong]
        trap = balancer.pick(scope, ft) if ft else "unmodelled"
        if trap == "unmodelled" and rng.random() < 0.95:
            continue
        T = {"yes": "Yes", "no": "No"}
        return {"spec": spec, "answer": correct, "options": [{"text": T[correct], "trap": None, "correct": True}, {"text": T[wrong], "trap": trap, "correct": False}],
                "score": score}
    return None


def perturb_t4(item, rng, balancer, scope):
    spec = item["spec"]
    old = solve_t4(spec)
    if spec["variant"] == "plan":
        cands = [("win_end", d) for d in (-120, -60, -30, -15, -5, 5, 15, 30, 60, 120)] + [("dur", (i, d)) for i in range(len(spec["tasks"])) for d in (-30, -15, 15, 30)]
    else:
        cands = [(b, (w, d)) for b in ("b1", "b2") for w in ("start", "end") for d in (-30, -15, -5, 5, 15, 30, 60)]
    rng.shuffle(cands)
    for kind, arg in cands:
        s2 = {k: v for k, v in spec.items()}
        if spec["variant"] == "plan":
            if kind == "win_end":
                s2["win_end"] = from_utc(ts_obj(spec["win_end"]) + dt.timedelta(minutes=arg), spec["win_end"]["off"])
                if ts_obj(s2["win_end"]) <= ts_obj(spec["win_start"]):
                    continue
            else:
                i, d = arg
                s2["tasks"] = [dict(t) for t in spec["tasks"]]
                s2["tasks"][i]["dur"] = spec["tasks"][i]["dur"] + d
                if s2["tasks"][i]["dur"] < 15:
                    continue
        else:
            w, d = arg
            s2[kind] = dict(spec[kind])
            s2[kind][w] = from_utc(ts_obj(spec[kind][w]) + dt.timedelta(minutes=d), spec[kind][w]["off"])
            if ts_obj(s2[kind]["end"]) <= ts_obj(s2[kind]["start"]):
                continue
        new = solve_t4(s2)
        if new == old:
            continue
        fl = flawed_t4(s2)
        correct, wrong = ("yes", "no") if new == "yes" else ("no", "yes")
        ft = [f for f, o in fl.items() if o == wrong]
        trap = balancer.pick(scope, ft) if ft else "unmodelled"
        T = {"yes": "Yes", "no": "No"}
        return {"spec": s2, "answer": new, "options": [{"text": T[correct], "trap": None, "correct": True}, {"text": T[wrong], "trap": trap, "correct": False}],
                "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------------------------------------
def _ts_vals(ts):
    return (ts_text(ts), "number", "datetime")        # a full timestamp with a UTC offset: the voice lane has no spoken form for it yet


def render(item, pool, widx, rng, domain, carrier="TXT-PROSE"):
    spec = item["spec"]
    form = spec["form"]
    doc = Doc()
    doc.sentence(pool.get("scene." + domain, rng.randrange(1 << 20)), {})
    idx = 0

    def whole(key):
        nonlocal idx
        item_sep(doc, carrier, idx)
        idx += 1
        doc.sentence(pool.get(key, rng.randrange(1 << 20)), {}, whole=("entity", "rule"))

    if form == "TM-T1":
        whole("tm.calendar_rule")
        if spec["month_rule"]:
            whole("tm.rule.clamp" if spec["month_rule"] == "clamp" else "tm.rule.roll")
        if any(o["unit"] == "business_day" for o in spec["ops"]):
            item_sep(doc, carrier, idx)
            idx += 1
            doc.sentence(pool.get("tm.weekend", rng.randrange(1 << 20)), {"days": (join_names([WEEKDAY_NAMES[w] for w in spec["weekend"]]), "entity", "rule")})
            item_sep(doc, carrier, idx)
            idx += 1
            if spec["holidays"]:
                doc.sentence(pool.get("tm.holidays", rng.randrange(1 << 20)), {"dates": (join_names(spec["holidays"]), "number", "date")})
            else:
                doc.sentence(pool.get("tm.no_holidays", rng.randrange(1 << 20)), {}, whole=("entity", "rule"))
        end_block(doc, carrier)
        doc.sentence(pool.get("q.TM-T1", widx), {"start": (spec["start"], "number", "date"), "offset": (offset_text(spec["ops"]), "number", "quantity")})
        return doc.text(), doc.spans
    if form == "TM-T2":
        whole("tm.calendar_rule")
        evs = sorted([(ts_obj(spec["t1"]), 0), (ts_obj(spec["t2"]), 1)]) if carrier == "TXT-TIMELINE" else [(None, 0), (None, 1)]
        for _, i in evs:
            item_sep(doc, carrier, idx)
            idx += 1
            doc.sentence(pool.get("tm.ts", rng.randrange(1 << 20)), {"name": (spec["names"][i], "entity", "name"), "ts": _ts_vals(spec["t%d" % (i + 1)])})
        end_block(doc, carrier)
        doc.sentence(pool.get("q.TM-T2", widx), {"t1": (spec["names"][0], "entity", "name"), "t2": (spec["names"][1], "entity", "name"),
                                                "fmt": (FMT_PHRASE[spec["fmt"]], "entity", "rule")})
        return doc.text(), doc.spans
    if form == "TM-T3":
        whole("tm.calendar_rule")
        whole("tm.iv.def")
        order = [0, 1]
        if carrier == "TXT-TIMELINE" and ts_obj(spec["iv2"]["start"]) < ts_obj(spec["iv1"]["start"]):
            order = [1, 0]
        for i in order:
            iv = spec["iv%d" % (i + 1)]
            item_sep(doc, carrier, idx)
            idx += 1
            doc.sentence(pool.get("tm.interval", rng.randrange(1 << 20)), {"name": (spec["names"][i], "entity", "name"), "start": _ts_vals(iv["start"]), "end": _ts_vals(iv["end"])})
        end_block(doc, carrier)
        doc.sentence(pool.get("q.TM-T3", widx), {"iv1": (spec["names"][0], "entity", "name"), "iv2": (spec["names"][1], "entity", "name")})
        return doc.text(), doc.spans
    # TM-T4
    whole("tm.calendar_rule")
    if spec["variant"] == "plan":
        whole("tm.parallel")      # skeptic fix 18 Oct: feasibility assumes unlimited parallel workers, which the stem never said
        item_sep(doc, carrier, idx)
        idx += 1
        doc.sentence(pool.get("tm.window", rng.randrange(1 << 20)), {"start": _ts_vals(spec["win_start"]), "end": _ts_vals(spec["win_end"])})
        for t in spec["tasks"]:
            item_sep(doc, carrier, idx)
            idx += 1
            if t["after"]:
                doc.sentence(pool.get("tm.task", rng.randrange(1 << 20)), {"name": (t["name"], "entity", "name"), "dur": (dur_text(t["dur"]), "number", "quantity"),
                                                                     "after": (join_names(t["after"]), "entity", "name")})
            else:
                doc.sentence(pool.get("tm.task.noafter", rng.randrange(1 << 20)), {"name": (t["name"], "entity", "name"), "dur": (dur_text(t["dur"]), "number", "quantity")})
        end_block(doc, carrier)
        doc.sentence(pool.get("q.TM-T4", widx), {})
    else:
        whole("tm.iv.def")
        for i, b in enumerate((spec["b1"], spec["b2"])):
            item_sep(doc, carrier, idx)
            idx += 1
            doc.sentence(pool.get("tm.booking", rng.randrange(1 << 20)), {"name": (spec["names"][i], "entity", "name"), "start": _ts_vals(b["start"]), "end": _ts_vals(b["end"])})
        end_block(doc, carrier)
        doc.sentence(pool.get("q.TM-T4.overlap", widx), {"b1": (spec["names"][0], "entity", "name"), "b2": (spec["names"][1], "entity", "name")})
    return doc.text(), doc.spans


def item_bin(item):
    s = item["score"]
    spec = item["spec"]
    f = spec["form"]
    if f == "TM-T1":
        ops = spec["ops"]
        simple = all(o["unit"] in ("day", "week") for o in ops)
        if len(ops) == 1 and simple:
            return "easy"
        if (len(ops) == 1 and (ops[0]["unit"] == "month" or len(spec["holidays"]) <= 1)) or (len(ops) == 2 and not any(o["unit"] == "business_day" for o in ops)):
            return "mid"
        return "hard"
    if f in ("TM-T2", "TM-T3"):
        return "easy" if s <= 2 else ("mid" if s <= 4 else "hard")
    if spec["variant"] == "plan":
        return "easy" if s <= 5 else ("mid" if s <= 9 else "hard")
    return "easy" if s <= 3 else ("mid" if s <= 5 else "hard")
