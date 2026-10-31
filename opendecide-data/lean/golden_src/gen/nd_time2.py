"""gen_numeric_dates schemas, part 2: month arithmetic, calendar validity, time zones, durations, pay schedules,
Schengen 90/180, dispatch cut-offs, medicine expiry."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

from nd_common import (V, MONTHS, PLACES, WEEKDAYS, D, Schema, Sty, add_days, add_months, add_months2, cap, dur_hm,
                       dur_words, fd, fdm, ft, iso, isleap, month_end, ordn, person, plural)

LAB = ["Situation: ", "Case: ", "", "Facts: "]

# =============================================================================================================
class MonthAdd(Schema):
    """'N months after' with end-of-month clamping (passport validity, probation, loan instalments, notice) and
    'end of the Nth month after the month earned' (points expiry)."""
    name = "month_add"
    quota = 700
    letter = True
    DOMS = ["passport", "probation", "loan", "points", "tenancy"]

    def sample(self, rng):
        dom = rng.choice(self.DOMS)
        yr = rng.choice([2025, 2026, 2027, 2028, 2029])
        n = {"passport": rng.choice([3, 6, 6]), "probation": rng.choice([3, 6]), "loan": rng.randint(1, 11),
             "points": rng.choice([12, 18, 24, 6]), "tenancy": rng.choice([1, 2, 3])}[dom]
        day = rng.choice([28, 29, 30, 31, 31, 30, 29]) if rng.random() < 0.7 else rng.randint(1, 27)
        m = rng.randint(1, 12)
        while True:
            try:
                s = dt.date(yr, m, day)
                break
            except ValueError:
                day -= 1
        f = {"dom": dom, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "n": n,
             "start": iso(s)}
        key = D(self._key(f))
        f["act"] = iso(key + dt.timedelta(days=rng.choice([0, 0, 1, -1, 2, -2, 3, -3])))
        return f

    def _key(self, f):
        if f["dom"] == "points":
            s = D(f["start"])
            y, m = divmod(s.month - 1 + f["n"], 12)
            return month_end(s.year + y, m + 1)
        return add_months(f["start"], f["n"])

    def _key2(self, f):
        if f["dom"] == "points":
            first = D(add_months2(f["start"][:8] + "01", f["n"] + 1))
            return iso(first - dt.timedelta(days=1))
        return add_months2(f["start"], f["n"])

    def preds(self, f):
        k = self._key(f)
        if f["dom"] in ("passport", "tenancy"):
            return {"ok": f["act"] >= k}  # expiry / move-out date on or after the threshold
        return {"ok": f["act"] <= k}

    def preds2(self, f):
        k = D(self._key2(f))
        a = D(f["act"])
        if f["dom"] in ("passport", "tenancy"):
            return {"ok": not (a < k)}
        return {"ok": not (a > k)}

    def val(self, f):
        return self._key(f)

    def val2(self, f):
        return self._key2(f)

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 3))

    def wrongs(self, f):
        s = D(f["start"])
        k = D(self._key(f))
        out = [iso(k + dt.timedelta(days=1)), iso(k - dt.timedelta(days=1)), iso(s + dt.timedelta(days=30 * f["n"]))]
        # overflow instead of clamping (e.g. 31 Aug + 6 months -> 3 March)
        y, m = divmod(s.month - 1 + f["n"], 12)
        try:
            out.append(iso(dt.date(s.year + y, m + 1, 1) + dt.timedelta(days=s.day - 1)))
        except ValueError:
            pass
        if f["dom"] == "points":
            out.append(add_months(f["start"], f["n"]))
            out.append(month_end(*(lambda d: (d.year, d.month))(D(add_months(f["start"][:8] + "01", f["n"] - 1)))))
        return out

    def alts(self, f):
        return {"act": [add_days(f["act"], d) for d in (-2, -1, 1, 2, 3, -3)],
                "start": [add_days(f["start"], d) for d in (-1, 1, -2, 2)], "n": [f["n"] - 1, f["n"] + 1]}

    def valid(self, f):
        return f["n"] >= 1 and D(f["act"]) > D(f["start"])

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        s = D(f["start"])
        if f["dom"] != "points" and s.day > 28 and D(self._key(f)).day != s.day:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        n, who, dom = f["n"], f["who"][0], f["dom"]
        clamp = st.c("cl", ["If that month has no such day, the last day of that month is used.",
                            "Where the month is too short to have that day (for example 31 June), use the last day of the month instead."])
        mo = f"{n} {plural(n, 'month')}"
        start, act = fd(f["start"], ds), fd(f["act"], ds)
        if dom == "passport":
            dest = st.c("dest", ["Kenya", "Thailand", "Peru", "Vietnam", "Morocco", "Indonesia", "Egypt", "Jordan"])
            pol = (f"Entry requirements for {dest} (as published by the {f['org']} Travel Agency)\n- Your passport must be valid for at least {mo} after the date you arrive: "
                   f"its expiry date must be on or after the date {mo} after your arrival date. {clamp}\n- At least two blank pages are required.\n- Proof of onward travel may be requested.")
            scen = f"{who} will arrive in {dest} on {start}. {cap(f['who'][3])} passport expires on {act}."
        elif dom == "probation":
            pol = (f"{f['org']} Housing Association - staff handbook\n- Probation lasts {mo}. It ends on the same day of the month {mo} after the start date, and the employee is on probation up to and including that day. {clamp}\n"
                   f"- During probation the notice period is one week.")
            scen = f"{who} started work on {start}. On {act}, {f['who'][1]} handed in one week's notice."
        elif dom == "loan":
            pol = (f"{f['org']} Credit Union - instalment schedule\n- Instalment number k is due k months after the loan date, on the same day of the month as the loan date. {clamp}\n"
                   f"- A payment made on or before its due date is on time.\n- Late payments incur a $15 fee.")
            scen = f"{who}'s loan was taken out on {start}. {cap(f['who'][1])} paid instalment number {n} on {act}."
        elif dom == "points":
            pol = (f"{f['org']} Rewards - points expiry\n- Points expire at the end of the {ordn(n)} month after the month in which they were earned. For example, with a 12-month life, "
                   f"points earned on any day in March expire at the end of March the following year.\n- Points cannot be transferred.")
            pol = pol.replace("with a 12-month life", "with a 12-month life" if n == 12 else "under a 12-month rule")
            scen = f"{who} earned 4,000 points on {start} and wants to redeem them on {act}."
        else:  # tenancy
            pol = (f"{f['org']} Lettings - ending a periodic tenancy\n- A tenant must give at least {mo}' notice in writing. The earliest date the tenancy can end is the same day of the month {mo} after the landlord receives the notice. {clamp}\n"
                   f"- Rent is payable up to the day the tenancy ends.")
            pol = pol.replace("1 month' notice", "one month's notice")
            scen = f"The landlord received {who}'s written notice on {start}. {cap(f['who'][1])} {V(f['who'], 'wants')} the tenancy to end on {act}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who, dom = f["who"][0], f["dom"]
        m = {"passport": ([f"Does {who}'s passport meet the validity requirement?", f"Is {who}'s passport valid for long enough for this trip?"],
                          [f"Will {who}'s passport fail the validity requirement?", f"Does {who}'s passport expire too soon for this trip?"],
                          f"{who}'s passport meets the validity rule", f"{who}'s passport expires too soon"),
             "probation": ([f"Was {who} still on probation when {f['who'][1]} handed in notice?"], [f"Had {who}'s probation already ended when {f['who'][1]} handed in notice?"],
                           f"{who} was still on probation that day", f"{who}'s probation had already ended that day"),
             "loan": ([f"Was instalment number {f['n']} paid on time?"], [f"Was instalment number {f['n']} paid late?"],
                      "the instalment was paid on time", "the instalment was paid late"),
             "points": ([f"Can {who} still redeem those points on that date?"], [f"Will those points have expired by that date?"],
                        "the points can still be redeemed that day", "the points will have expired by then"),
             "tenancy": ([f"Can the tenancy end on the date {who} wants?"], [f"Is the date {who} wants too early for the tenancy to end?"],
                         "the tenancy can end on that date", "that date is too early for the tenancy to end")}[dom]
        return dict(pos=m[0], neg=m[1], cpos=m[2], cneg=m[3],
                    speakers=[("A colleague told " + f["who"][2] + " that", "the colleague"), ("An online forum post claimed that", "the forum post")])

    def letter_q(self, f):
        return {"passport": ["What is the earliest expiry date the passport may have?"], "probation": ["On what date does the probation period end?"],
                "loan": [f"On what date is instalment number {f['n']} due?"], "points": ["On what date do the points earned that day expire?"],
                "tenancy": ["What is the earliest date on which the tenancy can end?"]}[f["dom"]]


# =============================================================================================================
class DateValidity(Schema):
    """Does a written calendar date exist? (Gregorian leap-year rule: 1900 and 2100 are not leap years, 2000 is.)"""
    name = "date_validity"
    quota = 350
    DOMS = ["birth", "archive", "lease", "form"]

    def sample(self, rng):
        dom = rng.choice(self.DOMS)
        r = rng.random()
        if r < 0.55:
            m, d = 2, 29
            y = rng.choice([1900, 2000, 2100, 1896, 1904, 1996, 2023, 2024, 2025, 2028, 1800, 2096, 2104, 1700, 1600])
        elif r < 0.8:
            m = rng.choice([4, 6, 9, 11])
            d = 31
            y = rng.randint(1920, 2030)
        else:
            m, d = rng.choice([(2, 30), (2, 28), (4, 30), (1, 31), (6, 30), (9, 31), (11, 31), (12, 31)])
            y = rng.randint(1920, 2030)
        if dom == "lease" and y < 2025:
            y = rng.choice([2096, 2100, 2104, 2099, 2112])
        if dom == "birth" and y > 2025:
            y = rng.choice([1900, 1904, 1896, 2000])
        if dom == "form":
            y = rng.choice([2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
        return {"dom": dom, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
                "y": y, "m": m, "d": d, "rule": rng.random() < 0.6}

    def valid(self, f):
        if f["dom"] == "birth" and not (1850 <= f["y"] <= 2025):
            return False
        if f["dom"] == "lease" and f["y"] < 2025:
            return False
        if f["dom"] == "form" and not (2020 <= f["y"] <= 2035):
            return False
        return 1 <= f["d"] <= 31 and 1 <= f["m"] <= 12

    def preds(self, f):
        try:
            dt.date(f["y"], f["m"], f["d"])
            return {"ok": True}
        except ValueError:
            return {"ok": False}

    def preds2(self, f):
        L = [31, 29 if isleap(f["y"]) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][f["m"] - 1]
        return {"ok": f["d"] <= L}

    def alts(self, f):
        return {"y": [f["y"] + k for k in (-4, 4, -1, 1, -100, 100, 400, -400)], "d": [f["d"] - 1, f["d"] - 2],
                "m": [x for x in (1, 3, 5, 7, 8, 10, 12) if x != f["m"]][:3]}

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        if f["m"] == 2 and f["d"] == 29 and f["y"] % 100 == 0:
            t.append("exception")
        if not f["rule"]:
            t.append("implicit")
        return t

    def _datetxt(self, f, st):
        y, m, d = f["y"], f["m"], f["d"]
        return st.c("dt", [f"{d} {MONTHS[m - 1]} {y}", f"{MONTHS[m - 1]} {d}, {y}", f"{y}-{m:02d}-{d:02d}"])

    def render(self, f):
        st = Sty(f)
        rule = (" " + st.c("rl", ["Leap years are years divisible by 4, except century years (such as 1800 or 1900), which are leap years only if divisible by 400.",
                                  "February has 29 days in a leap year. A year is a leap year if it is divisible by 4 but not by 100, or if it is divisible by 400."])
                if f["rule"] else "")
        date = self._datetxt(f, st)
        who = f["who"][0]
        if f["dom"] == "birth":
            pol = f"{f['org']} Civil Registry - data-entry rules\n- A date of birth must be a real calendar date; entries such as 31 April must be sent back for correction.{rule}\n- Names are entered exactly as written on the source document."
            scen = f"A digitised baptism record lists the date of birth of {who} as {date}."
        elif f["dom"] == "archive":
            pol = f"{f['org']} City Archive - cataloguing guidelines\n- Record the date of a document only if it is a date that exists in the Gregorian calendar; otherwise flag the entry as 'date doubtful'.{rule}\n- Undated documents are catalogued by decade."
            scen = f"An archivist, {who}, is cataloguing a letter dated {date}."
        elif f["dom"] == "lease":
            pol = f"{f['org']} Land Registry - lease registration\n- The end date of a lease must be a real calendar date; a lease whose end date does not exist cannot be registered until corrected.{rule}\n- Lease terms longer than 125 years need special approval."
            scen = f"{who} is registering a long lease whose stated end date is {date}."
        else:
            pol = f"{f['org']} Insurance - application checks\n- The policy start date entered on the form must be a date that exists on the calendar; impossible dates are returned to the applicant.{rule}\n- The form must be signed by the applicant."
            scen = f"{who}'s signed form gives a policy start date of {date}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        return dict(pos=["Is the date as written a real calendar date that can be accepted?", "Does the date given actually exist in the calendar?"],
                    neg=["Must the date be rejected because no such date exists?", "Is the date as written an impossible calendar date?"],
                    cpos="the date is a valid calendar date", cneg="no such date exists",
                    speakers=[("A trainee remarked that", "the trainee"), ("A supervisor noted that", "the supervisor")])


# =============================================================================================================
ZONES = [("New York", "America/New_York"), ("Chicago", "America/Chicago"), ("Denver", "America/Denver"),
         ("Phoenix", "America/Phoenix"), ("Los Angeles", "America/Los_Angeles"), ("Anchorage", "America/Anchorage"),
         ("Honolulu", "Pacific/Honolulu"), ("St. John's", "America/St_Johns"), ("São Paulo", "America/Sao_Paulo"),
         ("London", "Europe/London"), ("Paris", "Europe/Paris"), ("Berlin", "Europe/Berlin"), ("Lagos", "Africa/Lagos"),
         ("Nairobi", "Africa/Nairobi"), ("Dubai", "Asia/Dubai"), ("Mumbai", "Asia/Kolkata"), ("Kathmandu", "Asia/Kathmandu"),
         ("Singapore", "Asia/Singapore"), ("Tokyo", "Asia/Tokyo"), ("Brisbane", "Australia/Brisbane"),
         ("Sydney", "Australia/Sydney"), ("Adelaide", "Australia/Adelaide"), ("Auckland", "Pacific/Auckland"),
         ("Reykjavik", "Atlantic/Reykjavik")]
ZN = dict((b, a) for a, b in ZONES)

# independent DST table: (standard offset minutes, dst offset minutes or None, rule)
MAN = {"America/New_York": (-300, -240, "us"), "America/Chicago": (-360, -300, "us"), "America/Denver": (-420, -360, "us"),
       "America/Phoenix": (-420, None, None), "America/Los_Angeles": (-480, -420, "us"), "America/Anchorage": (-540, -480, "us"),
       "Pacific/Honolulu": (-600, None, None), "America/St_Johns": (-210, -150, "us"), "America/Sao_Paulo": (-180, None, None),
       "Europe/London": (0, 60, "eu"), "Europe/Paris": (60, 120, "eu"), "Europe/Berlin": (60, 120, "eu"),
       "Africa/Lagos": (60, None, None), "Africa/Nairobi": (180, None, None), "Asia/Dubai": (240, None, None),
       "Asia/Kolkata": (330, None, None), "Asia/Kathmandu": (345, None, None), "Asia/Singapore": (480, None, None),
       "Asia/Tokyo": (540, None, None), "Australia/Brisbane": (600, None, None), "Australia/Sydney": (600, 660, "au"),
       "Australia/Adelaide": (570, 630, "au"), "Pacific/Auckland": (720, 780, "nz"), "Atlantic/Reykjavik": (0, None, None)}


def nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - 6) % 7)


def transition_days(tz, y):
    r = MAN[tz][2]
    if r == "us":
        return {nth_sunday(y, 3, 2), nth_sunday(y, 11, 1)}
    if r == "eu":
        return {last_sunday(y, 3), last_sunday(y, 10)}
    if r == "au":
        return {nth_sunday(y, 4, 1), nth_sunday(y, 10, 1)}
    if r == "nz":
        return {nth_sunday(y, 4, 1), last_sunday(y, 9)}
    return set()


def man_offset(tz, d):
    """Independent offset (minutes) for a LOCAL date that is not a transition day."""
    std, dst, r = MAN[tz]
    if r is None:
        return std
    y = d.year
    if r == "us":
        on = nth_sunday(y, 3, 2) < d < nth_sunday(y, 11, 1)
    elif r == "eu":
        on = last_sunday(y, 3) < d < last_sunday(y, 10)
    elif r == "au":
        on = d > nth_sunday(y, 10, 1) or d < nth_sunday(y, 4, 1)
    else:
        on = d > last_sunday(y, 9) or d < nth_sunday(y, 4, 1)
    return dst if on else std


def zi_offset(tz, d, m):
    """Primary: zoneinfo offset (minutes) at local date d, minute m."""
    x = dt.datetime.combine(D(d), dt.time(m // 60, m % 60), tzinfo=ZoneInfo(tz))
    return int(x.utcoffset().total_seconds() // 60)


def off_s(mins, st=0):
    sign = "+" if mins >= 0 else "-"
    a = abs(mins)
    h, m = divmod(a, 60)
    s = f"{h}:{m:02d}" if m else f"{h}"
    return ("UTC" if st == 0 else "GMT") + (f"{sign}{s}" if mins else "+0")


def to_local(tz, utc_min):
    """UTC minutes since epoch-ordinal -> (local date iso, minute) via zoneinfo."""
    day, m = divmod(utc_min, 1440)
    u = dt.datetime.combine(dt.date.fromordinal(day), dt.time(m // 60, m % 60), tzinfo=dt.timezone.utc)
    x = u.astimezone(ZoneInfo(tz))
    return iso(x.date()), x.hour * 60 + x.minute


def utc_min(tz, d, m):
    x = dt.datetime.combine(D(d), dt.time(m // 60, m % 60), tzinfo=ZoneInfo(tz))
    u = x.astimezone(dt.timezone.utc)
    return u.date().toordinal() * 1440 + u.hour * 60 + u.minute


def utc_min2(tz, d, m):
    return D(d).toordinal() * 1440 + m - man_offset(tz, D(d))


def safe_local(tz, d):
    dd = D(d)
    return dd not in transition_days(tz, dd.year) and dd - dt.timedelta(days=1) not in transition_days(tz, dd.year) \
        and dd + dt.timedelta(days=1) not in transition_days(tz, dd.year)


class TzDeadline(Schema):
    """Deadline stated in one city's local time, action stated in another city's local time (offsets given)."""
    name = "tz_deadline"
    quota = 750
    letter = True
    hide_keys = {"ok": ["zB"]}
    DOMS = ["bid", "exam", "presale", "grant", "trade", "hackathon"]
    OFFS = list(range(-720, 841, 15))

    def sample(self, rng):
        zA, zB = rng.sample([z for _, z in ZONES], 2)
        yr = rng.choice([2025, 2026, 2027, 2028])
        d = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        t = rng.choice([1020, 1439, 720, 1080, 540, 1200, 0 + 600, 960])
        incl = rng.random() < 0.7 or t == 1439
        f = {"dom": rng.choice(self.DOMS), "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
             "zA": zA, "zB": zB, "dl_d": iso(d), "dl_t": t, "incl": incl}
        U = utc_min(zA, iso(d), t)
        off = rng.choice([0, 0, 1, -1, 60, -60, 59, -59, 61, -61, 30, -30]) if rng.random() < 0.85 else rng.randint(-900, 900)
        f["ac_d"], f["ac_t"] = to_local(zB, U + off)
        return f

    def valid(self, f):
        if f["zB"] is None:
            return safe_local(f["zA"], f["dl_d"])
        return (f["zA"] != f["zB"] and safe_local(f["zA"], f["dl_d"]) and safe_local(f["zB"], f["ac_d"])
                and 0 <= f["ac_t"] < 1440 and (f["incl"] or f["dl_t"] != 1439) and safe_local(f["zB"], self.val(f)[0]))

    def preds(self, f):
        b = utc_min(f["zA"], f["dl_d"], f["dl_t"])
        if f["zB"] is None:
            loc = D(f["ac_d"]).toordinal() * 1440 + f["ac_t"]
            outs = {(loc - o <= b) if f["incl"] else (loc - o < b) for o in self.OFFS}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        a = utc_min(f["zB"], f["ac_d"], f["ac_t"])
        return {"ok": a <= b if f["incl"] else a < b}

    def preds2(self, f):
        b = utc_min2(f["zA"], f["dl_d"], f["dl_t"])
        if f["zB"] is None:
            outs = set()
            for o in (self.OFFS[0], self.OFFS[-1]):
                x = dt.datetime.combine(D(f["ac_d"]), dt.time(f["ac_t"] // 60, f["ac_t"] % 60), tzinfo=dt.timezone(dt.timedelta(minutes=o)))
                u = x.astimezone(dt.timezone.utc)
                a = u.date().toordinal() * 1440 + u.hour * 60 + u.minute
                outs.add(not (a > b) if f["incl"] else not (a >= b))
            return {"ok": outs.pop() if len(outs) == 1 else None}
        a = utc_min2(f["zB"], f["ac_d"], f["ac_t"])
        return {"ok": not (a > b) if f["incl"] else not (a >= b)}

    def val(self, f):
        if f["zB"] is None:
            return None
        return list(to_local(f["zB"], utc_min(f["zA"], f["dl_d"], f["dl_t"])))

    def val2(self, f):
        if f["zB"] is None:
            return None
        u = utc_min2(f["zA"], f["dl_d"], f["dl_t"])
        # local B = u + offset(B); iterate: offset depends on the local date (safe dates only)
        day, m = divmod(u + MAN[f["zB"]][0], 1440)
        off = man_offset(f["zB"], dt.date.fromordinal(day))
        day, m = divmod(u + off, 1440)
        return [iso(dt.date.fromordinal(day)), m]

    def fmtv(self, f, v):
        st = Sty(f)
        return f"{ft(v[1], st.i('ts', 3))} on {fdm(v[0], st.i('ds', 2), wd=True)}"

    def wrongs(self, f):
        d, m = self.val(f)
        base = D(d).toordinal() * 1440 + m
        out = []
        for k in (60, -60, 120, -120, 1440, -1440):
            day, mm = divmod(base + k, 1440)
            out.append([iso(dt.date.fromordinal(day)), mm])
        # sign error: local B = deadline local A - (offB - offA) instead of +
        oA = zi_offset(f["zA"], f["dl_d"], f["dl_t"])
        oB = zi_offset(f["zB"], d, m)
        day, mm = divmod(D(f["dl_d"]).toordinal() * 1440 + f["dl_t"] - (oB - oA), 1440)
        out.insert(0, [iso(dt.date.fromordinal(day)), mm])
        return out

    def alts(self, f):
        if f["zB"] is None:
            return {}
        t = f["ac_t"]
        return {"ac_t": [x for x in (t - 1, t + 1, t - 60, t + 60, t - 30, t + 30, t - 2, t + 2) if 0 <= x < 1440],
                "zB": [z for _, z in ZONES if z not in (f["zA"], f["zB"])],
                "incl": [not f["incl"]] if f["dl_t"] != 1439 else [],
                "ac_d": [add_days(f["ac_d"], k) for k in (-1, 1)]}

    def edges(self, f, p):
        t = ["temporal", "numeric", "units"]
        if f["zB"] is None:
            return t + ["missing_info"]
        if f["dl_d"] != self.val(f)[0]:
            t.append("implicit")
        return t

    def _offtxt(self, tz, d, m, st, k):
        o = zi_offset(tz, d, m)
        return off_s(o, st.i("os" + k, 2))

    def render(self, f):
        st = Sty(f)
        ds, ts = st.i("ds", 2), st.i("ts", 3)
        cA, cB = ZN[f["zA"]], ZN.get(f["zB"])
        oA = self._offtxt(f["zA"], f["dl_d"], f["dl_t"], st, "a")
        oB = self._offtxt(f["zB"], f["ac_d"], f["ac_t"], st, "b") if f["zB"] else None
        tm = ft(f["dl_t"], ts)
        date = fd(f["dl_d"], ds, wd=True)
        when = (st.c("inc", [f"no later than {tm} {cA} time ({oA}) on {date}", f"by {tm} {cA} time ({oA}) on {date}"]) if f["incl"]
                else st.c("exc", [f"before {tm} {cA} time ({oA}) on {date}", f"strictly before {tm} {cA} time ({oA}) on {date}"]))
        who = f["who"][0]
        dom = f["dom"]
        head, rule, act = {
            "bid": (f"{f['org']} Port Authority - request for proposals", f"Proposals must be uploaded {when}. The upload time recorded by the portal decides.", "uploaded the proposal"),
            "exam": (f"{f['org']} Institute - online certification exam", f"Answer sheets must be submitted {when}. Late sheets are not marked.", "submitted the answer sheet"),
            "presale": (f"{f['org']} Arena - member presale", f"Presale codes can be used {when}; after that, tickets go on general sale.", "used the presale code"),
            "grant": (f"{f['org']} Research Council - full proposals", f"Full proposals are due {when}. There is no grace period.", "submitted the full proposal"),
            "trade": (f"{f['org']} Securities - order cut-off", f"Orders for the fund must be placed {when} to receive that day's price.", "placed the order"),
            "hackathon": (f"{f['org']} Global Hackathon - final submissions", f"Projects must be submitted {when}.", "submitted the project"),
        }[dom]
        pol = f"{head}\n- {rule}\n- Participants in other time zones must convert the deadline themselves.\n- Technical problems must be reported before the deadline."
        if f["zB"] is None:
            scen = (f"{who} {act} at {ft(f['ac_t'], st.i('ts2', 3))} on {fd(f['ac_d'], ds, wd=True)}, according to the clock on {f['who'][3]} laptop. "
                    f"{cap(f['who'][1])} {V(f['who'], 'was')} travelling that week, and the time zone the laptop was set to is not known.")
        else:
            scen = st.c("sc", [f"{who}, who lives in {cB} ({oB} on that date), {act} at {ft(f['ac_t'], st.i('ts2', 3))} local time on {fd(f['ac_d'], ds, wd=True)}.",
                               f"Working from {cB}, where clocks were at {oB}, {who} {act} at {ft(f['ac_t'], st.i('ts2', 3))} local time on {fd(f['ac_d'], ds, wd=True)}."])
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        thing = {"bid": "the proposal", "exam": "the answer sheet", "presale": "the presale purchase", "grant": "the proposal",
                 "trade": "the order", "hackathon": "the project"}[f["dom"]]
        return dict(pos=[f"Did {who} meet the deadline?", f"Was {thing} in time under the rules?"],
                    neg=[f"Did {who} miss the deadline?", f"Was {thing} too late under the rules?"],
                    cpos=f"{who} met the deadline", cneg=f"{who} missed the deadline",
                    speakers=[("A teammate told " + f["who"][2] + " that", "the teammate"), ("The organisers' chatbot replied that", "the chatbot")])

    def letter_q(self, f):
        return [f"What was the local time in {ZN[f['zB']]} at the moment of the deadline?"]


# =============================================================================================================
class FlightDuration(Schema):
    """Scheduled flight time from local departure/arrival times in different zones (corporate travel policy)."""
    name = "flight_duration"
    quota = 550
    letter = True
    ROUTES = [("New York", "London", 7), ("London", "Singapore", 13), ("Tokyo", "Los Angeles", 10), ("Dubai", "Sydney", 14),
              ("Paris", "Mumbai", 9), ("Chicago", "Berlin", 9), ("São Paulo", "Paris", 11), ("Los Angeles", "Honolulu", 6),
              ("Auckland", "Los Angeles", 12), ("Singapore", "Tokyo", 7), ("Nairobi", "London", 9), ("Denver", "Anchorage", 5),
              ("Mumbai", "Singapore", 6), ("London", "New York", 8), ("Kathmandu", "Dubai", 4), ("Adelaide", "Singapore", 7),
              ("Phoenix", "Chicago", 3), ("Reykjavik", "New York", 6), ("Lagos", "Dubai", 8), ("Sydney", "Auckland", 3),
              ("St. John's", "London", 5), ("Brisbane", "Tokyo", 9), ("Berlin", "Nairobi", 8), ("Honolulu", "Tokyo", 9),
              ("Singapore", "Sydney", 8), ("Dubai", "London", 7), ("Los Angeles", "Sydney", 15), ("New York", "Tokyo", 14)]

    def sample(self, rng):
        a, b, typ = rng.choice(self.ROUTES)
        if rng.random() < 0.5:
            a, b = b, a
        zA, zB = ZN_INV[a], ZN_INV[b]
        yr = rng.choice([2025, 2026, 2027, 2028])
        d = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        t = rng.randrange(0, 1440, 5)
        H = max(2, typ + rng.choice([0, 0, -1, 1]))
        dur = H * 60 + rng.choice([0, 0, 5, -5, 10, -10, 60, -60, 25, -25, 90, -90])
        dur = max(60, dur)
        U = utc_min(zA, iso(d), t)
        ad, at = to_local(zB, U + dur)
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "zA": zA, "zB": zB,
                "dep_d": iso(d), "dep_t": t, "arr_d": ad, "arr_t": at, "H": H, "rule": rng.choice(["gt", "ge"]),
                "dom": rng.choice(["business", "rest", "perdiem"])}

    def dur(self, f):
        return utc_min(f["zB"], f["arr_d"], f["arr_t"]) - utc_min(f["zA"], f["dep_d"], f["dep_t"])

    def dur2(self, f):
        return utc_min2(f["zB"], f["arr_d"], f["arr_t"]) - utc_min2(f["zA"], f["dep_d"], f["dep_t"])

    def valid(self, f):
        if not (safe_local(f["zA"], f["dep_d"]) and safe_local(f["zB"], f["arr_d"]) and 0 <= f["arr_t"] < 1440):
            return False
        return 45 <= self.dur(f) <= 20 * 60

    def preds(self, f):
        d = self.dur(f)
        return {"ok": d > f["H"] * 60 if f["rule"] == "gt" else d >= f["H"] * 60}

    def preds2(self, f):
        d = self.dur2(f)
        return {"ok": d > f["H"] * 60 if f["rule"] == "gt" else not (d < f["H"] * 60)}

    def val(self, f):
        return self.dur(f)

    def val2(self, f):
        return self.dur2(f)

    def fmtv(self, f, v):
        return dur_words(v) if Sty(f).p("dw", 0.5) else dur_hm(v)

    def wrongs(self, f):
        local = (D(f["arr_d"]).toordinal() * 1440 + f["arr_t"]) - (D(f["dep_d"]).toordinal() * 1440 + f["dep_t"])
        d = self.dur(f)
        oA = zi_offset(f["zA"], f["dep_d"], f["dep_t"])
        oB = zi_offset(f["zB"], f["arr_d"], f["arr_t"])
        return [x for x in (local, local + (oB - oA), d + 60, d - 60, d + 30, 2 * local - d) if 0 < x < 30 * 60]

    def alts(self, f):
        t = f["arr_t"]
        return {"arr_t": [x for x in (t - 5, t + 5, t - 10, t + 10, t - 60, t + 60, t - 30, t + 30) if 0 <= x < 1440],
                "H": [f["H"] - 1, f["H"] + 1], "rule": ["ge" if f["rule"] == "gt" else "gt"],
                "dep_t": [x for x in (f["dep_t"] - 10, f["dep_t"] + 10, f["dep_t"] - 60, f["dep_t"] + 60) if 0 <= x < 1440]}

    def edges(self, f, p):
        t = ["temporal", "numeric", "units"]
        if f["dep_d"] != f["arr_d"]:
            t.append("implicit")
        return t

    def render(self, f):
        st = Sty(f)
        ds, ts = st.i("ds", 2), st.i("ts", 3)
        H = f["H"]
        hh = f"{H} {plural(H, 'hour')}"
        cmp_ = f"more than {hh}" if f["rule"] == "gt" else f"{hh} or more"
        head = {"business": (f"{f['org']} Consulting - travel policy", f"Business class may be booked only when the scheduled flight time is {cmp_}; otherwise book economy."),
                "rest": (f"{f['org']} Engineering - travel and rest", f"Staff who take a flight whose scheduled flight time is {cmp_} may start work at noon the next day."),
                "perdiem": (f"{f['org']} University - travel allowances", f"A long-haul meal allowance of $60 is paid for any flight whose scheduled flight time is {cmp_}.")}[f["dom"]]
        pol = f"{head[0]}\n- {head[1]}\n- Flight time is measured from scheduled departure to scheduled arrival; all schedule times are local times.\n- Connections are treated as separate flights."
        cA, cB = ZN[f["zA"]], ZN[f["zB"]]
        oA = off_s(zi_offset(f["zA"], f["dep_d"], f["dep_t"]), st.i("os", 2))
        oB = off_s(zi_offset(f["zB"], f["arr_d"], f["arr_t"]), st.i("os", 2))
        flt = st.c("fl", ["QX", "NB", "TR", "AV", "LK"]) + str(100 + st.i("fn", 899))
        scen = st.c("sc", [
            f"{f['who'][0]} is booked on flight {flt}, departing {cA} at {ft(f['dep_t'], ts)} on {fd(f['dep_d'], ds)} (local time, {oA}) and arriving in {cB} at {ft(f['arr_t'], ts)} on {fd(f['arr_d'], ds)} (local time, {oB}).",
            f"Flight {flt} for {f['who'][0]}: departs {cA} {ft(f['dep_t'], ts)} local time ({oA}), {fd(f['dep_d'], ds)}; arrives {cB} {ft(f['arr_t'], ts)} local time ({oB}), {fd(f['arr_d'], ds)}."])
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        m = {"business": ([f"May {who} book business class for this flight?"], [f"Must {who} fly economy on this flight?"],
                          "business class is allowed on this flight", "this flight must be booked in economy"),
             "rest": ([f"May {who} start work at noon the day after this flight?"], [f"Is {who} required to start work at the normal time after this flight, without the late start?"],
                      f"{who} qualifies for the late start", f"{who} does not qualify for the late start"),
             "perdiem": ([f"Is {who} entitled to the long-haul meal allowance for this flight?"], [f"Is {who} ineligible for the long-haul meal allowance for this flight?"],
                         "the meal allowance applies", "the meal allowance does not apply")}[f["dom"]]
        return dict(pos=m[0], neg=m[1], cpos=m[2], cneg=m[3],
                    speakers=[("The travel desk told " + f["who"][2] + " that", "the travel desk"), ("A colleague said", "the colleague")])

    def letter_q(self, f):
        return ["What is the scheduled flight time of this flight?"]


ZN_INV = {a: b for a, b in ZONES}


# =============================================================================================================
class GapDuration(Schema):
    """Time between two clock times that may cross midnight: connections, rest, fasting, incubation windows."""
    name = "gap_duration"
    quota = 650
    letter = True
    DOMS = ["mct", "rest", "fasting", "incubation", "babysit"]

    def sample(self, rng):
        dom = rng.choice(self.DOMS)
        yr = rng.choice([2025, 2026, 2027, 2028])
        d = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        req = {"mct": rng.choice([45, 50, 60, 75, 90]), "rest": rng.choice([8, 10, 11, 12]) * 60,
               "fasting": rng.choice([6, 8, 12]) * 60, "incubation": rng.choice([18, 16, 20]) * 60,
               "babysit": rng.choice([3, 4, 5]) * 60}[dom]
        hi = {"incubation": req + rng.choice([6, 8]) * 60}.get(dom)
        t1 = {"mct": rng.randrange(0, 1440, 5), "rest": rng.choice(range(1080, 1440, 5)), "fasting": rng.choice(range(1140, 1440, 5)),
              "incubation": rng.randrange(480, 1200, 5), "babysit": rng.randrange(1020, 1320, 5)}[dom]
        bound = rng.choice([req] + ([hi] if hi else []))
        gap = bound + rng.choice([0, 0, 1, -1, 5, -5, 15, -15, 60, -60, 0])
        if dom == "babysit":
            gap = rng.randint(req // 60 - 1, req // 60 + 3) * 60 + rng.choice([0, 15, 30, 45, 1, 59])
        a = d.toordinal() * 1440 + t1
        b = a + gap
        f = {"dom": dom, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "req": req, "hi": hi,
             "d1": iso(d), "t1": t1, "d2": iso(dt.date.fromordinal(b // 1440)), "t2": b % 1440}
        if dom == "babysit":
            f["rate"] = rng.choice([15, 18, 20, 22])
        return f

    def gap(self, f):
        return (D(f["d2"]).toordinal() - D(f["d1"]).toordinal()) * 1440 + f["t2"] - f["t1"]

    def gap2(self, f):
        a = dt.datetime.combine(D(f["d1"]), dt.time(f["t1"] // 60, f["t1"] % 60))
        b = dt.datetime.combine(D(f["d2"]), dt.time(f["t2"] // 60, f["t2"] % 60))
        return int((b - a).total_seconds() // 60)

    def valid(self, f):
        g = self.gap(f)
        return 0 <= f["t2"] < 1440 and 0 <= f["t1"] < 1440 and 10 <= g <= 40 * 60

    def _ok(self, f, g):
        if f["dom"] == "incubation":
            return f["req"] <= g <= f["hi"]
        if f["dom"] == "babysit":
            return None
        return g >= f["req"]

    def preds(self, f):
        if f["dom"] == "babysit":
            return {"ok": self._fee(f, self.gap(f)) > f["rate"] * (f["req"] // 60)}
        return {"ok": self._ok(f, self.gap(f))}

    def preds2(self, f):
        g = self.gap2(f)
        if f["dom"] == "babysit":
            hrs = -(-g // 60)
            return {"ok": hrs * f["rate"] > f["rate"] * (f["req"] // 60)}
        if f["dom"] == "incubation":
            return {"ok": not (g < f["req"] or g > f["hi"])}
        return {"ok": not (g < f["req"])}

    def _fee(self, f, g):
        return ((g + 59) // 60) * f["rate"]

    def val(self, f):
        return self.gap(f)

    def val2(self, f):
        return self.gap2(f)

    def fmtv(self, f, v):
        return dur_words(v)

    def wrongs(self, f):
        g = self.gap(f)
        return [x for x in (g + 60, g - 60, g + 720, g - 720, g + 10, g - 10, 1440 - g) if 0 < x < 48 * 60]

    def alts(self, f):
        t = f["t2"]
        a = {"t2": [x for x in (t - 1, t + 1, t - 5, t + 5, t - 15, t + 15, t - 60, t + 60) if 0 <= x < 1440],
             "req": [f["req"] + k for k in (-60, 60, -15, 15) if f["req"] + k > 0 and f["dom"] != "babysit"]}
        if f["dom"] == "incubation":
            a["hi"] = [f["hi"] - 60, f["hi"] + 60]
        return a

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        if f["d1"] != f["d2"]:
            t.append("implicit")
        return t

    def _when(self, d, t, st, k, ref):
        tm = ft(t, st.i("ts", 3))
        if d == ref:
            return f"{tm} on {fdm(d, st.i('ds', 2))}"
        return f"{tm} on {fdm(d, st.i('ds', 2))}" if st.p(k, 0.6) else f"{tm} the next day" if (D(d) - D(ref)).days == 1 else f"{tm} on {fdm(d, st.i('ds', 2))}"

    def render(self, f):
        st = Sty(f)
        who, dom = f["who"][0], f["dom"]
        w1 = f"{ft(f['t1'], st.i('ts', 3))} on {fdm(f['d1'], st.i('ds', 2), wd=True)}"
        w2 = self._when(f["d2"], f["t2"], st, "nx", f["d1"])
        yr = D(f["d1"]).year
        if dom == "mct":
            ap = st.c("ap", ["Harbor International", "Summit Regional", "Northfield International", "Lakeside Central"])
            pol = f"{ap} Airport ({yr} connection rules)\n- Minimum connecting time for international-to-domestic transfers: {f['req']} minutes between the scheduled arrival of the first flight and the scheduled departure of the second.\n- Connections shorter than the minimum cannot be sold on one ticket."
            scen = f"{who}'s itinerary has an international flight scheduled to arrive at {w1} and a domestic flight scheduled to depart at {w2}, both on one ticket."
        elif dom == "rest":
            pol = f"{f['org']} Freight - driver hours\n- Drivers must have at least {dur_words(f['req'])} of consecutive rest between the end of one shift and the start of the next.\n- Shifts may not exceed 13 hours."
            scen = f"{who}'s shift ended at {w1}. {cap(f['who'][3])} next shift is scheduled to start at {w2}."
        elif dom == "fasting":
            pol = f"{f['org']} Day Surgery - patient instructions\n- Do not eat for at least {dur_words(f['req'])} before your scheduled procedure time. Clear water is allowed until two hours before.\n- Bring a list of your medicines."
            scen = f"{who} finished {f['who'][3]} last meal at {w1}. The procedure is scheduled for {w2}."
        elif dom == "incubation":
            pol = f"{f['org']} Microbiology Lab - protocol\n- Plates must be incubated for at least {dur_words(f['req'])} and no more than {dur_words(f['hi'])} before they are read.\n- Record the incubator temperature at the start."
            scen = f"{who} placed the plates in the incubator at {w1} and read them at {w2}."
        else:
            pol = f"{f['org']} Sitters - rates\n- Babysitting is charged at ${f['rate']} per hour; every started hour is charged as a full hour.\n- The minimum booking is {f['req'] // 60} hours."
            scen = f"{who} started babysitting at {w1} and the parents came home at {w2}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who, dom = f["who"][0], f["dom"]
        sp = [("A colleague told " + f["who"][2] + " that", "the colleague"), ("A friend said", "the friend")]
        m = {"mct": ([f"Does {who}'s connection meet the minimum connecting time?"], [f"Is {who}'s connection shorter than the minimum connecting time?"],
                     "the connection meets the minimum", "the connection is too short"),
             "rest": ([f"Does {who} get enough rest between the two shifts?"], [f"Is {who}'s rest between shifts shorter than required?"],
                      f"{who} gets enough rest between the shifts", f"{who}'s rest is shorter than required"),
             "fasting": ([f"Did {who} fast for long enough before the procedure?"], [f"Is {who}'s fast shorter than required?"],
                         f"{who} fasted long enough", f"{who}'s fast is too short"),
             "incubation": ([f"Were the plates incubated for a permitted length of time?"], [f"Was the incubation time outside the permitted range?"],
                            "the incubation time was within the permitted range", "the incubation time was outside the permitted range"),
             "babysit": ([f"Is the charge for this evening more than the charge for the minimum booking?"], [f"Is the charge for this evening no more than the charge for the minimum booking?"],
                         "the evening costs more than the minimum booking", "the evening costs no more than the minimum booking")}[dom]
        return dict(pos=m[0], neg=m[1], cpos=m[2], cneg=m[3], speakers=sp)

    def letter_q(self, f):
        return {"mct": ["How long is the scheduled connection?"], "rest": ["How long is the rest period between the two shifts?"],
                "fasting": ["How long is the fasting period before the procedure?"], "incubation": ["How long were the plates incubated?"],
                "babysit": ["How long did the babysitting last?"]}[f["dom"]]


# =============================================================================================================
class PaydaySchedule(Schema):
    """Semi-monthly paydays moved to the preceding/following business day; biweekly paydays."""
    name = "payday"
    quota = 550
    letter = True

    def sample(self, rng):
        yr = rng.choice([2025, 2026, 2027, 2028])
        kind = rng.choice(["semi", "semi", "biweekly"])
        f = {"kind": kind, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
             "dir": rng.choice(["prev", "next"]), "y": yr, "m": rng.randint(1, 12), "half": rng.choice([1, 2])}
        if kind == "biweekly":
            a = dt.date(yr, 1, 2) + dt.timedelta(days=rng.randint(0, 13))
            while a.weekday() != 4:
                a += dt.timedelta(days=1)
            f["anchor"] = iso(a)
        nom = D(self._nominal(f))
        hol = []
        if rng.random() < 0.5:
            cands = [nom + dt.timedelta(days=k) for k in range(-4, 5)]
            cands = [c for c in cands if c.weekday() < 5]
            if cands:
                hol.append(iso(rng.choice(cands)))
        f["hol"] = hol
        pay = D(self._pay(f))
        f["exp"] = iso(rng.choice([pay, pay, nom, pay + dt.timedelta(days=rng.choice([-1, 1, -3, 3]))]))
        return f

    def _nominal(self, f):
        if f["kind"] == "semi":
            return iso(dt.date(f["y"], f["m"], 15)) if f["half"] == 1 else month_end(f["y"], f["m"])
        # the biweekly payday in (y, m) number `half` (1st or 2nd in the month)
        d = D(f["anchor"])
        out = []
        while d.year <= f["y"]:
            if d.year == f["y"] and d.month == f["m"]:
                out.append(d)
            d += dt.timedelta(days=14)
        return iso(out[min(f["half"], len(out)) - 1])

    def _pay(self, f):
        d = D(self._nominal(f))
        step = -1 if f["dir"] == "prev" else 1
        while d.weekday() >= 5 or iso(d) in f["hol"]:
            d += dt.timedelta(days=step)
        return iso(d)

    def _pay2(self, f):
        H = np.array(f["hol"], dtype="datetime64[D]")
        nom = np.datetime64(self._nominal(f))
        return str(np.busday_offset(nom, 0, roll="backward" if f["dir"] == "prev" else "forward", holidays=H))

    def valid(self, f):
        return True

    def preds(self, f):
        return {"ok": f["exp"] == self._pay(f)}

    def preds2(self, f):
        return {"ok": f["exp"] == self._pay2(f)}

    def val(self, f):
        return self._pay(f)

    def val2(self, f):
        return self._pay2(f)

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 3), wd=True)

    def wrongs(self, f):
        nom = D(self._nominal(f))
        g = dict(f, dir="next" if f["dir"] == "prev" else "prev")
        g2 = dict(f, hol=[])
        return [self._nominal(f), self._pay(g), self._pay(g2), iso(D(self._pay(f)) + dt.timedelta(days=-1)),
                iso(nom + dt.timedelta(days=1))]

    def alts(self, f):
        a = {"dir": ["next" if f["dir"] == "prev" else "prev"], "exp": [add_days(f["exp"], k) for k in (-1, 1, -2, 2, -3, 3)]}
        if f["hol"]:
            a["hol"] = [[]]
        else:
            nom = D(self._nominal(f))
            if nom.weekday() < 5:
                a["hol"] = [[iso(nom)]]
        return a

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        if D(self._nominal(f)).weekday() >= 5 or self._nominal(f) in f["hol"]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        mv = "the business day before" if f["dir"] == "prev" else "the next business day after it"
        mv2 = "brought forward to the last business day before it" if f["dir"] == "prev" else "moved to the first business day after it"
        hol = ("; ".join(fd(h, ds, wd=True) for h in f["hol"]))
        hl = f" Bank holidays this year that fall near paydays: {hol}." if f["hol"] else st.c("nh", [" No bank holiday falls near the paydays in question.", ""])
        if f["kind"] == "semi":
            rule = st.c("r", [f"Salaries are paid twice a month: on the 15th and on the last day of the month. If a payday falls on a Saturday, Sunday or bank holiday, payment is {mv2}.",
                              f"Pay dates: the 15th and the last calendar day of each month. A pay date that is not a business day (weekend or bank holiday) is replaced by {mv}."])
            period = f"the {'first' if f['half'] == 1 else 'second'} half of {MONTHS[f['m'] - 1]} {f['y']}"
            which = f"payment for {period}"
        else:
            rule = f"Employees are paid every other Friday, starting on {fd(f['anchor'], ds, wd=True)}. If a payday is a bank holiday, payment is {mv2}."
            which = f"the {'first' if f['half'] == 1 else 'second'} payday in {MONTHS[f['m'] - 1]} {f['y']}"
        pol = f"{f['org']} Manufacturing - payroll calendar\n- {rule}{hl}\n- Payslips are available in the portal two days before payment."
        scen = st.c("sc", [f"{f['who'][0]} is planning {f['who'][3]} rent payment and has marked {fd(f['exp'], ds, wd=True)} as the date of {which}.",
                           f"{f['who'][0]} expects {which} to arrive on {fd(f['exp'], ds, wd=True)}."])
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is {who} right about the date of that payment?", f"Will that payment be made on the date {who} expects?"],
                    neg=[f"Will that payment be made on a different date from the one {who} expects?", f"Has {who} got the payment date wrong?"],
                    cpos=f"the payment will be made on the date {who} expects", cneg=f"the payment will not be made on the date {who} expects",
                    speakers=[("A payroll clerk told " + f["who"][2] + " that", "the payroll clerk")])

    def letter_q(self, f):
        return ["On which date will that payment be made?"]


# =============================================================================================================
class Schengen(Schema):
    """90 days in any rolling 180-day period; entry and exit days both count."""
    name = "schengen"
    quota = 450
    letter = True
    multi_hop = True

    def sample(self, rng):
        yr = rng.choice([2025, 2026, 2027, 2028])
        base = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        trips = []
        cur = base
        for _ in range(rng.choice([1, 2, 2, 3])):
            ln = rng.randint(8, 40)
            trips.append([iso(cur), iso(cur + dt.timedelta(days=ln - 1))])
            cur = cur + dt.timedelta(days=ln - 1 + rng.randint(10, 60))
        pe = cur + dt.timedelta(days=rng.randint(5, 40))
        f = {"who": person(rng), "sty": rng.randrange(10 ** 9), "trips": trips, "pin": iso(pe)}
        # latest allowed exit, then probe around it
        L = self.latest(f)
        if L is None:
            return self.sample(rng)
        off = rng.choice([0, 0, 1, 1, -1, 2, -3, 5, -6])
        f["pout"] = iso(D(L) + dt.timedelta(days=off))
        return f

    @staticmethod
    def _prev(f):
        s = set()
        for a, b in f["trips"]:
            d = D(a)
            while d <= D(b):
                s.add(d)
                d += dt.timedelta(days=1)
        return s

    def ok_for(self, f, pout):
        """Primary: on day d of the planned trip the window holds the earlier days in [d-179, d] plus the
        (d - entry + 1) planned days so far (the planned trip is shorter than 180 days)."""
        P = self._prev(f)
        pin = D(f["pin"])
        d = pin
        while d <= D(pout):
            prev = sum(1 for k in range(180) if d - dt.timedelta(days=k) in P)
            if prev + (d - pin).days + 1 > 90:
                return False
            d += dt.timedelta(days=1)
        return True

    def latest(self, f):
        P = self._prev(f)
        pin = D(f["pin"])
        d = pin
        last = None
        while (d - pin).days < 150:
            prev = sum(1 for k in range(180) if d - dt.timedelta(days=k) in P)
            if prev + (d - pin).days + 1 > 90:
                break
            last = d
            d += dt.timedelta(days=1)
        return iso(last) if last else None

    def valid(self, f):
        if D(f["pout"]) < D(f["pin"]):
            return False
        prev_end = max(D(b) for _, b in f["trips"])
        for (a, b) in f["trips"]:
            if D(b) < D(a):
                return False
        return prev_end < D(f["pin"])

    def preds(self, f):
        return {"ok": self.ok_for(f, f["pout"])}

    def preds2(self, f):
        # prefix sums over an ordinal array
        lo = min(D(a) for a, _ in f["trips"]).toordinal() - 200
        hi = D(f["pout"]).toordinal() + 1
        pres = [0] * (hi - lo + 1)
        for a, b in f["trips"] + [[f["pin"], f["pout"]]]:
            for o in range(D(a).toordinal(), D(b).toordinal() + 1):
                pres[o - lo] = 1
        cum = [0]
        for x in pres:
            cum.append(cum[-1] + x)
        for o in range(D(f["pin"]).toordinal(), D(f["pout"]).toordinal() + 1):
            i = o - lo
            if cum[i + 1] - cum[max(0, i - 179)] > 90:
                return {"ok": False}
        return {"ok": True}

    def val(self, f):
        return self.latest(f)

    def val2(self, f):
        # independent: scan exits with preds2 until it fails
        o = D(f["pin"])
        best = None
        for k in range(0, 121):
            g = dict(f, pout=iso(o + dt.timedelta(days=k)))
            if self.preds2(g)["ok"]:
                best = g["pout"]
            else:
                break
        return best

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 2), wd=False)

    def wrongs(self, f):
        L = D(self.latest(f))
        used = sum((D(b) - D(a)).days + 1 for a, b in f["trips"])
        naive = D(f["pin"]) + dt.timedelta(days=90 - used - 1)
        return [iso(L + dt.timedelta(days=1)), iso(L - dt.timedelta(days=1)), iso(naive), iso(L + dt.timedelta(days=2)),
                iso(naive + dt.timedelta(days=2))]

    def alts(self, f):
        a = {"pout": [add_days(f["pout"], k) for k in (-1, 1, -2, 2, -5, 5)]}
        t0 = f["trips"][0]
        a["trips"] = [[[t0[0], add_days(t0[1], k)]] + f["trips"][1:] for k in (-3, -1, 1, 3)]
        return a

    def edges(self, f, p):
        return ["temporal", "numeric", "long_context"] if len(f["trips"]) >= 3 else ["temporal", "numeric"]

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 2)
        pol = st.c("pol", [
            "Short-stay rule for the Schengen area (visa-free visitors)\n- A visitor may stay at most 90 days in any 180-day period.\n- The period is rolling: on each day of a stay, count the days spent in the area on that day and during the 179 days before it; the total may never exceed 90.\n- The day of entry and the day of exit both count as full days of stay.",
            "Schengen 90/180 rule - summary for travellers\n- On any day you are in the area, the number of days you have spent there in the 180-day window ending on that day (that day included) must be 90 or fewer.\n- Entry and exit days count as days of stay, even if you arrive late at night.\n- Days in other countries outside the area do not count.",
        ])
        trips = "\n".join(f"- {fd(a, ds)} to {fd(b, ds)}" for a, b in f["trips"])
        who = f["who"][0]
        scen = (f"{who}, who does not need a visa, has made these earlier stays in the Schengen area (dates of entry and exit):\n{trips}\n"
                f"{cap(f['who'][1])} now {V(f['who'], 'plans')} to enter on {fd(f['pin'], ds)} and leave on {fd(f['pout'], ds)}, with no other travel in between.")
        return f"{pol}\n\n{st.c('lab', ['Situation: ', 'Case: ', ''])}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Does {who}'s planned trip comply with the 90/180 rule?", f"Can {who} make the planned trip without overstaying?"],
                    neg=[f"Would {who} overstay under the 90/180 rule on the planned trip?", f"Does {who}'s planned trip break the 90/180 rule?"],
                    cpos=f"the planned trip complies with the 90/180 rule", cneg=f"the planned trip would break the 90/180 rule",
                    speakers=[("A travel blogger told " + f["who"][2] + " that", "the blogger"), ("A consulate phone line said", "the phone line")])

    def letter_q(self, f):
        return [f"If {f['who'][0]} enters on the planned date, what is the latest exit date that keeps the trip within the rule?"]


# =============================================================================================================
class ShippingDispatch(Schema):
    """Order cut-off in the warehouse's time zone + business-day dispatch and transit."""
    name = "shipping_dispatch"
    quota = 550
    letter = True
    multi_hop = True
    derived_keys = ()

    def sample(self, rng):
        zS = rng.choice(["America/New_York", "America/Chicago", "America/Los_Angeles", "Europe/London", "Europe/Berlin",
                         "Australia/Sydney", "Asia/Singapore"])
        zC = rng.choice([z for _, z in ZONES if z != zS and MAN[z][2] in (MAN[zS][2], None)])
        yr = rng.choice([2025, 2026, 2027, 2028])
        d = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        cut = rng.choice([720, 840, 900, 960, 1020])
        k = rng.choice([1, 2, 3, 5])
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "zS": zS, "zC": zC, "cut": cut,
             "k": k, "hol": []}
        # order near the cut-off (in store time), expressed in customer local time
        U = utc_min(zS, iso(d), cut) + rng.choice([0, -1, 1, -30, 30, -61, 59, -200, 200])
        f["od"], f["ot"] = to_local(zC, U)
        if rng.random() < 0.35:
            h = D(self._dispatch(f)) + dt.timedelta(days=rng.randint(0, k + 2))
            if h.weekday() < 5:
                f["hol"] = [iso(h)]
        f["need"] = iso(D(self._deliver(f)) + dt.timedelta(days=rng.choice([0, 0, -1, 1, 2, -2])))
        return f

    def _store_local(self, f):
        return to_local(f["zS"], utc_min(f["zC"], f["od"], f["ot"]))

    def _dispatch(self, f):
        sd, sm = self._store_local(f)
        d = D(sd)
        isb = lambda x: x.weekday() < 5 and iso(x) not in f["hol"]
        if isb(d) and sm < f["cut"]:
            return iso(d)
        d += dt.timedelta(days=1)
        while not isb(d):
            d += dt.timedelta(days=1)
        return iso(d)

    def _deliver(self, f):
        d = D(self._dispatch(f))
        n = 0
        while n < f["k"]:
            d += dt.timedelta(days=1)
            if d.weekday() < 5 and iso(d) not in f["hol"]:
                n += 1
        return iso(d)

    def _deliver2(self, f):
        u = utc_min2(f["zC"], f["od"], f["ot"])
        # store-local via the manual offset table
        day, m = divmod(u + MAN[f["zS"]][0], 1440)
        off = man_offset(f["zS"], dt.date.fromordinal(day))
        day, m = divmod(u + off, 1440)
        sd = np.datetime64(iso(dt.date.fromordinal(day)))
        H = np.array(f["hol"], dtype="datetime64[D]")
        if np.is_busday(sd, holidays=H) and m < f["cut"]:
            disp = sd
        else:
            disp = np.busday_offset(sd + 1, 0, roll="forward", holidays=H)
        return str(np.busday_offset(disp, f["k"], roll="forward", holidays=H))

    def valid(self, f):
        sd, _ = self._store_local(f)
        return safe_local(f["zC"], f["od"]) and safe_local(f["zS"], sd) and 0 <= f["ot"] < 1440

    def preds(self, f):
        return {"ok": self._deliver(f) <= f["need"]}

    def preds2(self, f):
        return {"ok": not (self._deliver2(f) > f["need"])}

    def val(self, f):
        return self._deliver(f)

    def val2(self, f):
        return self._deliver2(f)

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 3), wd=True)

    def wrongs(self, f):
        v = D(self._deliver(f))
        g = dict(f, zC=f["zS"])  # forgot the time-zone conversion
        out = [self._deliver(g), iso(v + dt.timedelta(days=1)), iso(v - dt.timedelta(days=1)), self._deliver(dict(f, hol=[]))]
        # calendar days instead of business days
        out.append(iso(D(self._dispatch(f)) + dt.timedelta(days=f["k"])))
        return out

    def alts(self, f):
        t = f["ot"]
        return {"ot": [x for x in (t - 1, t + 1, t - 30, t + 30, t - 60, t + 60, t - 120, t + 120) if 0 <= x < 1440],
                "need": [add_days(f["need"], k) for k in (-1, 1, -2, 2)], "k": [f["k"] - 1, f["k"] + 1] if f["k"] > 1 else [f["k"] + 1],
                "hol": [[]] if f["hol"] else [], "cut": [f["cut"] - 60, f["cut"] + 60]}

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        if f["hol"]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        ds, ts = st.i("ds", 3), st.i("ts", 3)
        cS, cC = ZN[f["zS"]], ZN[f["zC"]]
        sd, sm = self._store_local(f)
        oS = off_s(zi_offset(f["zS"], sd, sm), st.i("os", 2))
        oC = off_s(zi_offset(f["zC"], f["od"], f["ot"]), st.i("os", 2))
        k = f["k"]
        hol = (f" The warehouse is closed on {fd(f['hol'][0], ds, wd=True)} (public holiday), which is not a business day." if f["hol"] else "")
        pol = (f"{f['org']} Supplies - shipping information\n- Orders placed before {ft(f['cut'], ts)} {cS} time ({oS}) on a business day are dispatched the same day. Orders placed at or after that time, or on a weekend or holiday, are dispatched on the next business day.\n"
               f"- Standard delivery arrives {k} business {plural(k, 'day')} after the dispatch day.\n- Business days are Monday to Friday.{hol}")
        scen = (f"{f['who'][0]}, who lives in {cC} ({oC}), placed an order at {ft(f['ot'], st.i('ts2', 3))} local time on {fd(f['od'], ds, wd=True)} with standard delivery. "
                f"{cap(f['who'][1])} {V(f['who'], 'needs')} the parcel by {fd(f['need'], ds, wd=True)}.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Will the parcel arrive by the date {who} needs it?", f"Is the order expected to be delivered in time for {who}?"],
                    neg=[f"Will the parcel arrive too late for {who}?", f"Will standard delivery miss the date {who} needs?"],
                    cpos="the parcel will arrive in time", cneg="the parcel will arrive too late",
                    speakers=[("A customer service chat told " + f["who"][2] + " that", "the chat agent"), ("A friend told " + f["who"][2] + " that", "the friend")])

    def letter_q(self, f):
        return ["On which date should the standard delivery arrive?"]


# =============================================================================================================
class MedExpiry(Schema):
    """Month/year expiry (usable through the month's last day) combined with a beyond-use period after opening."""
    name = "med_expiry"
    quota = 450
    letter = True
    multi_hop = True

    def sample(self, rng):
        yr = rng.choice([2025, 2026, 2027, 2028])
        em, ey = rng.randint(1, 12), yr + rng.choice([0, 1])
        n = rng.choice([28, 28, 30, 42, 56, 90, 14])
        eo = D(month_end(ey, em))
        o = eo - dt.timedelta(days=rng.randint(-5, n + 25))
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "em": em, "ey": ey, "n": n,
             "open": iso(o), "count": rng.choice(["day1", "day0"]), "prod": rng.choice(["insulin pen", "eye drops", "oral suspension", "inhaler", "vaccine vial"])}
        last = D(self._last(f))
        f["use"] = iso(last + dt.timedelta(days=rng.choice([0, 0, 1, -1, 2, -2])))
        return f

    def _last(self, f):
        exp = D(month_end(f["ey"], f["em"]))
        bud = D(f["open"]) + dt.timedelta(days=f["n"] - 1 if f["count"] == "day1" else f["n"])
        return iso(min(exp, bud))

    def _last2(self, f):
        first_next = dt.date(f["ey"] + (f["em"] == 12), f["em"] % 12 + 1, 1)
        exp = first_next.toordinal() - 1
        bud = D(f["open"]).toordinal() + f["n"] - (1 if f["count"] == "day1" else 0)
        return dt.date.fromordinal(exp if exp < bud else bud).isoformat()

    def valid(self, f):
        return D(f["use"]) >= D(f["open"]) and D(f["open"]) <= D(month_end(f["ey"], f["em"]))

    def preds(self, f):
        return {"ok": f["use"] <= self._last(f)}

    def preds2(self, f):
        return {"ok": not (D(f["use"]) > D(self._last2(f)))}

    def val(self, f):
        return self._last(f)

    def val2(self, f):
        return self._last2(f)

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 3))

    def wrongs(self, f):
        exp_first = iso(dt.date(f["ey"], f["em"], 1))
        bud = D(f["open"]) + dt.timedelta(days=f["n"] - 1 if f["count"] == "day1" else f["n"])
        return [exp_first, month_end(f["ey"], f["em"]), iso(bud), iso(bud + dt.timedelta(days=1)), iso(bud - dt.timedelta(days=1)),
                iso(D(self._last(f)) + dt.timedelta(days=1))]

    def alts(self, f):
        return {"use": [add_days(f["use"], k) for k in (-1, 1, -2, 2)], "open": [add_days(f["open"], k) for k in (-1, 1, -3, 3)],
                "count": ["day0" if f["count"] == "day1" else "day1"], "em": [f["em"] - 1, f["em"] + 1] if 1 < f["em"] < 12 else []}

    def edges(self, f, p):
        return ["temporal", "numeric"]

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        n = f["n"]
        cnt = ("The day it is first opened counts as day 1." if f["count"] == "day1" else "The day it is opened is day 0; the count starts the next day.")
        pol = st.c("pol", [
            f"{f['org']} Pharmacy - storage and expiry\n- An expiry date printed as month/year (for example 03/2027) means the product may be used up to and including the last day of that month.\n- Once opened, the {f['prod']} may be used for {n} days. {cnt} After that, discard it.\n- Whichever limit comes first applies.",
            f"{f['org']} Community Clinic - medicine handling\n- Month/year expiry dates run to the end of the stated month.\n- In-use period after opening: {n} days. {cnt}\n- A product must not be used once either the expiry date or the in-use period has passed.",
        ])
        scen = (f"{f['who'][0]}'s {f['prod']} is printed 'EXP {f['em']:02d}/{f['ey']}'. {cap(f['who'][1])} opened it on {fd(f['open'], ds)} "
                f"and {V(f['who'], 'wants')} to use it on {fd(f['use'], ds)}.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"May {who} still use the {f['prod']} on that date?", f"Is the {f['prod']} still usable on that date under the rules?"],
                    neg=[f"Should the {f['prod']} already have been discarded by that date?", f"Is it too late to use the {f['prod']} on that date?"],
                    cpos=f"the {f['prod']} can still be used on that date", cneg=f"the {f['prod']} must not be used on that date",
                    speakers=[("A pharmacist told " + f["who"][2] + " that", "the pharmacist"), ("A family member said", "the family member")])

    def letter_q(self, f):
        return [f"What is the last day on which the opened {f['prod']} may be used?"]
