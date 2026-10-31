"""dx_lead_score: reviewer R's devx renderer + parse-back for F5 `gen3_lead_score` (yn2b/SPEC.md sections 5 F5, 6).

Latents: gen3_lead_score.sample_latents("devx", plan) (the held-out weighted-scorecard archetype and the two held-out
industry packs, devx seed stream and name pool). Labels: gen3_lead_score.decide only. Everything a reader sees (the
scorecard text, level names, statement and activity wording, the CRM layouts, questions, cards, options) was written
for devx from the scorer's semantics (evaluate / activity / latest_claim / dq_hits), not from the training renderers.

Views (one row per latent): score (options = this file's level names, ascending), yes/no "sales-ready" and its
inverse wording, judge yes/no on a recorded CRM result and its inverse wording, JB-letter.
Formats: crm (canonical JSON), packet (sectioned text), timeline (one merged, time-ordered feed).
"""
from __future__ import annotations

import copy
import json
import re
import sys
from collections import Counter
from datetime import date
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import dx_common as dx  # noqa: E402

KEY = "gen3_lead_score"
FMTS = ("crm", "packet", "timeline")
FMT_META = {"crm": "json", "packet": "markdown", "timeline": "log:chrono"}
PLAN = {"score": 230, "ready": 44, "judge": 44, "jb": 30}


def _g5():
    import gen3_lead_score as g5   # its latent sampler and decide() only
    return g5


def decide(f: dict, kind: str):
    g, _ = _g5().decide(f, {"kind": kind})
    return g


# ------------------------------------------------------------------------------------------------ wording
LEVELS = {3: ["Band C", "Band B", "Band A"], 4: ["Ladder step 1", "Ladder step 2", "Ladder step 3", "Ladder step 4"],
          5: ["Level I", "Level II", "Level III", "Level IV", "Level V"],
          6: ["Score band 1", "Score band 2", "Score band 3", "Score band 4", "Score band 5", "Score band 6"]}
ACT = {"demo": "asked for a live demo", "pricing": "looked at the pricing page", "webinar": "webinar",
       "guide": "downloaded a buyer's guide", "trial": "started a free trial", "roi": "used the savings calculator",
       "meeting": "trade-show meeting"}
FILLER_ACT = ("opened a product newsletter", "read a blog post", "visited the jobs page", "read a help-centre page",
              "opened an event reminder", "opened a release-notes email")
FILLER_MSG = ("Could you send the slides from our call?", "Thanks, that answered my question.",
              "Is there a customer we could speak to?", "I'll share this with the team.",
              "Can we move our next call to the afternoon?")
FILLER_NOTE = ("Called; no answer, left a message.", "Shared the product overview.", "Set up a follow-up call.",
               "Sent the reference list.", "Confirmed the contact's phone number.")
STATUS_PH = {"approved": "have an approved budget of", "requested": "have put in a request for a budget of",
             "hoped": "are hoping for a budget of", "hypothetical": "might be able to find a budget of"}
STATUS_FORM = {"approved": "approved", "requested": "requested", "hoped": "hoped for", "hypothetical": "not yet planned"}
DQ_TXT = {"competitor": "the lead's company is one of these competitors: {c}",
          "personal_email": "the primary contact writes from a personal email domain: {d}",
          "region": "the lead's region is outside the regions served: {r}",
          "customer": "the company is already a customer",
          "small": "the company size is below {m} employees"}


def money(n) -> str:
    return f"${int(n):,}"


def parse_money(s: str) -> int:
    m = re.fullmatch(r"\$([\d,]+)", s.strip())
    if not m:
        raise ValueError(f"money {s!r}")
    return int(m.group(1).replace(",", ""))


def band_lines(bands, unit: str) -> list:
    out = []
    for i, (lo, v) in enumerate(bands):
        hi = bands[i + 1][0] - 1 if i + 1 < len(bands) else None
        rng = f"{lo:,} or more {unit}" if hi is None else f"{lo:,} to {hi:,} {unit}"
        out.append(f"{rng}: {v}")
    return out


def parse_bands(lines: list, unit: str) -> list:
    out = []
    for ln in lines:
        m = re.fullmatch(r"([\d,]+) (?:to [\d,]+|or more) " + re.escape(unit) + r": (\d+)", ln)
        if not m:
            raise ValueError(f"band {ln!r}")
        out.append([int(m.group(1).replace(",", "")), int(m.group(2))])
    return out


SEN = ("S0", "S1", "S2", "S3", "S4")


# ------------------------------------------------------------------------------------------------ the scorecard
def rubric_lines(f: dict, levels: list) -> list:
    r = f["rub"]
    w = r["weights"]
    win = r["window"]
    lines = []
    lines.append(f"1. Scope. This scorecard gives every lead one level on the scoring date. The levels, lowest first: "
                 f"{'; '.join(levels)}.")
    rep = (" The one exception: a rep note that gives the prospect's target date counts as a target-date statement."
           if r["rep_timeline"] else "")
    lines.append("2. Evidence. Only the primary contact's own words count as statements: their web form and the "
                 "emails or chat messages they wrote themselves. Statements by any other contact, words the primary "
                 "contact attributes to someone else (such as 'my CFO says'), and rep notes do not count." + rep +
                 " When several counting statements of one kind exist, only the most recent one is used.")
    if r["size_source"] == "enrichment":
        lines.append("3. Company size. Use the headcount from the data-enrichment service, not the range the contact "
                     "gave on the web form.")
    else:
        lines.append("3. Company size. Use the size range the contact gave on the web form, taking its lower end; "
                     "ignore the headcount from the data-enrichment service.")
    lines.append("4. Fit points by company size: " + "; ".join(band_lines(r["fit_bands"], "employees")) + ".")
    tt = "; ".join(f"{t} = {SEN[s]}" for t, s in r["title_sen"].items())
    rm = "; ".join(f"{SEN[int(s)]}: {p}" for s, p in sorted(r["role_map"].items(), key=lambda kv: int(kv[0])))
    lines.append(f"5. Role points. The primary contact's job title gives a seniority grade: {tt}. Role points by "
                 f"grade: {rm}.")
    pts = "; ".join(f"{ACT[t]}: {p}" for t, p in r["acts"].items())
    span = (f"on the scoring date or up to {win['days']} days before it (an activity exactly {win['days']} days "
            f"before still counts)" if win["incl"] else
            f"on the scoring date or fewer than {win['days']} days before it (an activity exactly {win['days']} days "
            f"before does not count)")
    cap = f" Activity points are capped at {r['cap']} in total." if r.get("cap") is not None else ""
    lines.append(f"6. Activity points. Only activities logged under the lead's own id count, and only {span}. "
                 f"Points per activity type: {pts}. A webinar or trade-show meeting in this list earns its points only "
                 f"when attended (a registration alone earns nothing). The same activity type on the same day counts once. Other "
                 f"activity types earn nothing, and so does anything dated after the scoring date.{cap}")
    lines.append("7. Engagement points by activity points: " + "; ".join(band_lines(r["eng_bands"], "points")) + ".")
    b = r["budget"]
    lines.append(f"8. Budget points, from the most recent counting budget statement. First convert its amount to "
                 f"a {b['period']}ly figure (a monthly amount times 12 is yearly; a yearly amount divided by 12 is "
                 f"monthly). Approved and at least {money(b['amount'])} per {b['period']}: 3. Requested and at least "
                 f"that: 2. Approved or requested but below it: 1. Anything else (hoped for, not yet planned, or no "
                 f"statement): 0.")
    d3, d2, d1 = r["timeline"]["tiers"]
    lines.append(f"9. Timeline points, from the most recent counting target date: count the days from the scoring "
                 f"date to that date. 0 to {d3} days: 3. {d3 + 1} to {d2} days: 2. {d2 + 1} to {d1} days: 1. More "
                 f"than {d1} days, a date already passed, or no date: 0.")
    lines.append(f"10. Total = {w['fit']} x fit + {w['role']} x role + {w['eng']} x engagement + {w['budget']} x "
                 f"budget + {w['timeline']} x timeline.")
    th = "; ".join(f"{levels[i + 1]} from {t}" for i, t in enumerate(r["thresholds"]))
    lines.append(f"11. Levels by total: {levels[0]} below {r['thresholds'][0]}; {th}.")
    lines.append("12. Tie rule. When the total equals one of the level thresholds exactly and the budget points are "
                 "below 2, the lead gets the next lower level.")
    dq = []
    for d in r["dq"]:
        dq.append(DQ_TXT[d].format(c=", ".join(r["competitors"]), d=", ".join(r["personal_domains"]),
                                   r=", ".join(r["regions"]), m=r.get("min_size")))
    if dq:
        lines.append("13. Disqualifiers. The lead gets the lowest level, whatever its total (the total is still "
                     "worked out), when: " + "; or ".join(dq) + ".")
    else:
        lines.append("13. Disqualifiers. None.")
    lines.append(f"14. Sales-ready. A lead whose level is {levels[r['handoff']]} or higher is sales-ready.")
    return lines


def parse_rubric(lines: list) -> dict:
    """The scorecard text back to the rubric fields decide() reads."""
    body = {int(re.match(r"(\d+)\. ", ln).group(1)): re.sub(r"^\d+\. ", "", ln) for ln in lines}
    r = {"arch": "weighted"}
    m = re.search(r"The levels, lowest first: (.+)\.$", body[1])
    levels = m.group(1).split("; ")
    r["levels"] = levels
    r["rep_timeline"] = "a rep note that gives the prospect's target date counts" in body[2]
    r["size_source"] = "enrichment" if body[3].startswith("Company size. Use the headcount") else "form"
    r["fit_bands"] = parse_bands(re.search(r"by company size: (.+)\.$", body[4]).group(1).split("; "), "employees")
    m = re.search(r"seniority grade: (.+)\. Role points by grade: (.+)\.$", body[5])
    r["title_sen"] = {}
    for x in m.group(1).split("; "):
        t, s = x.rsplit(" = ", 1)
        r["title_sen"][t] = SEN.index(s)
    r["role_map"] = {}
    for x in m.group(2).split("; "):
        s, p = x.split(": ")
        r["role_map"][str(SEN.index(s))] = int(p)
    m6 = body[6]
    mm = re.search(r"up to (\d+) days before it \(an activity exactly \d+ days before still counts\)", m6)
    if mm:
        r["window"] = {"days": int(mm.group(1)), "incl": True}
    else:
        mm = re.search(r"fewer than (\d+) days before it \(an activity exactly \d+ days before does not count\)", m6)
        r["window"] = {"days": int(mm.group(1)), "incl": False}
    if "and so does anything dated after the scoring date." not in m6:
        raise ValueError("activity section incomplete")
    pts = re.search(r"Points per activity type: (.+?)\. A webinar or trade-show meeting", m6).group(1)
    inv = {v: k for k, v in ACT.items()}
    r["acts"] = {}
    for x in pts.split("; "):
        lab, p = x.rsplit(": ", 1)
        r["acts"][inv[lab]] = int(p)
    mc = re.search(r"Activity points are capped at (\d+) in total\.", m6)
    r["cap"] = int(mc.group(1)) if mc else None
    r["per_type_max"], r["unsub"] = None, None
    r["eng_bands"] = parse_bands(re.search(r"by activity points: (.+)\.$", body[7]).group(1).split("; "), "points")
    mb = re.search(r"Approved and at least \$([\d,]+) per (year|month): 3\.", body[8])
    r["budget"] = {"amount": int(mb.group(1).replace(",", "")), "period": mb.group(2)}
    mt = re.search(r"0 to (\d+) days: 3\. \d+ to (\d+) days: 2\. \d+ to (\d+) days: 1\.", body[9])
    r["timeline"] = {"tiers": [int(mt.group(1)), int(mt.group(2)), int(mt.group(3))]}
    mw = re.fullmatch(r"Total = (\d+) x fit \+ (\d+) x role \+ (\d+) x engagement \+ (\d+) x budget \+ (\d+) x "
                      r"timeline\.", body[10])
    r["weights"] = dict(zip(("fit", "role", "eng", "budget", "timeline"), map(int, mw.groups())))
    ml = re.fullmatch(r"Levels by total: .+? below (\d+); (.+)\.", body[11])
    th = [int(x.rsplit(" from ", 1)[1]) for x in ml.group(2).split("; ")]
    r["thresholds"] = th
    if int(ml.group(1)) != th[0]:
        raise ValueError("threshold text mismatch")
    r["dq"], r["competitors"], r["personal_domains"], r["regions"], r["min_size"] = [], [], [], [], None
    if body[13] != "Disqualifiers. None.":
        conds = re.search(r"when: (.+)\.$", body[13]).group(1).split("; or ")
        for c in conds:
            for k, t in DQ_TXT.items():
                pat = re.escape(t).replace(re.escape("{c}"), "(?P<x>.+)").replace(re.escape("{d}"), "(?P<x>.+)") \
                    .replace(re.escape("{r}"), "(?P<x>.+)").replace(re.escape("{m}"), "(?P<x>\\d+)")
                m = re.fullmatch(pat, c)
                if m:
                    r["dq"].append(k)
                    x = m.groupdict().get("x")
                    if k == "competitor":
                        r["competitors"] = x.split(", ")
                    elif k == "personal_email":
                        r["personal_domains"] = x.split(", ")
                    elif k == "region":
                        r["regions"] = x.split(", ")
                    elif k == "small":
                        r["min_size"] = int(x)
                    break
            else:
                raise ValueError(f"disqualifier {c!r}")
    mh = re.fullmatch(r"Sales-ready\. A lead whose level is (.+) or higher is sales-ready\.", body[14])
    r["handoff"] = levels.index(mh.group(1))
    r["amend"], r["override"] = None, None
    return r


# ------------------------------------------------------------------------------------------------ the lead file
def size_form_text(sf) -> str:
    lo, hi = sf
    return f"{lo:,} or more employees" if hi is None else f"{lo:,} to {hi:,} employees"


def parse_size_form(s: str) -> list:
    m = re.fullmatch(r"([\d,]+) or more employees", s)
    if m:
        return [int(m.group(1).replace(",", "")), None]
    m = re.fullmatch(r"([\d,]+) to ([\d,]+) employees", s)
    return [int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))]


def contact_name(f, who: str) -> str:
    L = f["lead"]
    return L["primary"]["name"] if who == "primary" else L["secondary"]["name"]


def claim_text(f: dict, c: dict) -> tuple[str, str]:
    """(channel label, text) of one statement."""
    L = f["lead"]
    k, sp, ch = c["kind"], c["speaker"], c["channel"]
    if k == "budget":
        amt = f"{money(c['amount'])} per {c['period']}"
        if ch == "form":
            return "web form", f"budget: {amt}; budget status: {STATUS_FORM[c['status']]}"
        if sp == "rep":
            return "rep note", f"prospect mentioned a budget of {amt} ({STATUS_FORM[c['status']]})"
        if sp == "boss":
            return f"message from {L['primary']['name']}", f"My {c['boss']} says we {STATUS_PH[c['status']]} {amt}."
        return f"message from {contact_name(f, sp)}", f"We {STATUS_PH[c['status']]} {amt}."
    if k == "timeline":
        d = c["date"]
        if ch == "form":
            return "web form", f"target go-live date: {d}"
        if sp == "rep":
            return "rep note", f"prospect is aiming to go live on {d}"
        if sp == "boss":
            return f"message from {L['primary']['name']}", f"My {c['boss']} wants this running by {d}."
        return f"message from {contact_name(f, sp)}", f"We would like to be up and running by {d}."
    if k == "need":
        if ch == "form":
            return "web form", f"main need: {c['need']}"
        if sp == "rep":
            return "rep note", f"prospect's main need is {c['need']}"
        if sp == "boss":
            return f"message from {L['primary']['name']}", f"My {c['boss']} says the main need is {c['need']}."
        return f"message from {contact_name(f, sp)}", f"Our main need is {c['need']}."
    raise ValueError(k)


ST_PH_R = {v: k for k, v in STATUS_PH.items()}
ST_FORM_R = {v: k for k, v in STATUS_FORM.items()}


def parse_claim(f_lead: dict, label: str, text: str) -> dict | None:
    """Inverse of claim_text: a statement dict (kind, speaker, channel, ...) or None for a filler line."""
    pn = f_lead["primary"]["name"]
    sn = (f_lead.get("secondary") or {}).get("name")
    am = r"\$[\d,]+ per (?:year|month)"

    def amt(s):
        a, p = s.split(" per ")
        return parse_money(a), p
    if label == "web form":
        m = re.fullmatch(rf"budget: ({am}); budget status: (.+)", text)
        if m:
            a, p = amt(m.group(1))
            return {"kind": "budget", "speaker": "primary", "channel": "form", "status": ST_FORM_R[m.group(2)],
                    "amount": a, "period": p}
        m = re.fullmatch(r"target go-live date: (\d{4}-\d{2}-\d{2})", text)
        if m:
            return {"kind": "timeline", "speaker": "primary", "channel": "form", "date": m.group(1)}
        m = re.fullmatch(r"main need: (.+)", text)
        if m:
            return {"kind": "need", "speaker": "primary", "channel": "form", "need": m.group(1)}
        raise ValueError(f"form line {text!r}")
    if label == "rep note":
        m = re.fullmatch(rf"prospect mentioned a budget of ({am}) \((.+)\)", text)
        if m:
            a, p = amt(m.group(1))
            return {"kind": "budget", "speaker": "rep", "channel": "note", "status": ST_FORM_R[m.group(2)],
                    "amount": a, "period": p}
        m = re.fullmatch(r"prospect is aiming to go live on (\d{4}-\d{2}-\d{2})", text)
        if m:
            return {"kind": "timeline", "speaker": "rep", "channel": "note", "date": m.group(1)}
        m = re.fullmatch(r"prospect's main need is (.+)", text)
        if m:
            return {"kind": "need", "speaker": "rep", "channel": "note", "need": m.group(1)}
        if text in FILLER_NOTE:
            return None
        raise ValueError(f"note line {text!r}")
    m = re.fullmatch(r"message from (.+)", label)
    if not m:
        raise ValueError(f"label {label!r}")
    who = m.group(1)
    sp = "primary" if who == pn else ("secondary" if who == sn else None)
    if sp is None:
        raise ValueError(f"unknown sender {who!r}")
    mb = re.fullmatch(rf"My (.+?) says we ({'|'.join(map(re.escape, STATUS_PH.values()))}) ({am})\.", text)
    if mb and sp == "primary":
        a, p = amt(mb.group(3))
        return {"kind": "budget", "speaker": "boss", "channel": "msg", "status": ST_PH_R[mb.group(2)], "amount": a,
                "period": p, "boss": mb.group(1)}
    mb = re.fullmatch(rf"We ({'|'.join(map(re.escape, STATUS_PH.values()))}) ({am})\.", text)
    if mb:
        a, p = amt(mb.group(2))
        return {"kind": "budget", "speaker": sp, "channel": "msg", "status": ST_PH_R[mb.group(1)], "amount": a,
                "period": p}
    mt = re.fullmatch(r"My (.+?) wants this running by (\d{4}-\d{2}-\d{2})\.", text)
    if mt and sp == "primary":
        return {"kind": "timeline", "speaker": "boss", "channel": "msg", "date": mt.group(2), "boss": mt.group(1)}
    mt = re.fullmatch(r"We would like to be up and running by (\d{4}-\d{2}-\d{2})\.", text)
    if mt:
        return {"kind": "timeline", "speaker": sp, "channel": "msg", "date": mt.group(1)}
    mn = re.fullmatch(r"My (.+?) says the main need is (.+)\.", text)
    if mn and sp == "primary":
        return {"kind": "need", "speaker": "boss", "channel": "msg", "need": mn.group(2), "boss": mn.group(1)}
    mn = re.fullmatch(r"Our main need is (.+)\.", text)
    if mn:
        return {"kind": "need", "speaker": sp, "channel": "msg", "need": mn.group(1)}
    if text in FILLER_MSG:
        return None
    raise ValueError(f"message {text!r}")


def act_text(f: dict, a: dict, rng_pick) -> str:
    if a["type"] == "filler":
        return rng_pick(FILLER_ACT)
    t = ACT[a["type"]]
    if a["type"] in ("webinar", "meeting"):
        return f"{t} ({a['status']})"
    return t


def parse_act(text: str) -> tuple:
    inv = {v: k for k, v in ACT.items()}
    m = re.fullmatch(r"(webinar|trade-show meeting) \((attended|registered)\)", text)
    if m:
        return inv[m.group(1)], m.group(2)
    if text in inv:
        return inv[text], None
    if text in FILLER_ACT:
        return "filler", None
    raise ValueError(f"activity {text!r}")


def ts_short(ts: str) -> str:
    """'2026-10-08T08:40:00Z' -> '2026-10-08 08:40 UTC'."""
    return ts[:10] + " " + ts[11:16] + " UTC"


def ts_long(s: str) -> str:
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC", s)
    return f"{m.group(1)}T{m.group(2)}:00Z"


def lead_lines(f: dict) -> list:
    L = f["lead"]
    out = [f"Lead id: {L['id']}", f"Company: {L['company']} ({L['domain']})", f"Region: {L['region']}",
           f"Existing customer: {'yes' if L['customer'] else 'no'}", f"Created: {L['created']}",
           f"Owner (sales rep): {L['owner']}", f"Stage: {L['stage']}",
           f"Primary contact: {L['primary']['name']}, {L['primary']['title']}, {L['primary']['email']}"]
    if L["secondary"]:
        s = L["secondary"]
        out.append(f"Other contact: {s['name']}, {s['title']}, {s['email']}")
    out += [f"Headcount (data-enrichment service): {L['size_enrich']:,}",
            f"Size range (web form): {size_form_text(L['size_form'])}"]
    return out


def parse_lead(lines: list) -> dict:
    d = {}
    for ln in lines:
        k, v = ln.split(": ", 1)
        d[k] = v
    L = {"id": d["Lead id"]}
    m = re.fullmatch(r"(.+) \((.+)\)", d["Company"])
    L["company"], L["domain"] = m.group(1), m.group(2)
    L["region"], L["customer"] = d["Region"], d["Existing customer"] == "yes"
    L["created"], L["owner"], L["stage"] = d["Created"], d["Owner (sales rep)"], d["Stage"]
    n, t, e = d["Primary contact"].rsplit(", ", 2)
    L["primary"] = {"name": n, "title": t, "email": e}
    if "Other contact" in d:
        n, t, e = d["Other contact"].rsplit(", ", 2)
        L["secondary"] = {"name": n, "title": t, "email": e}
    else:
        L["secondary"] = None
    L["size_enrich"] = int(d["Headcount (data-enrichment service)"].replace(",", ""))
    L["size_form"] = parse_size_form(d["Size range (web form)"])
    return L


def feed(f: dict, rng) -> list:
    """Every dated item: (ts, kind, label, text). kind: activity | statement | filler."""
    L = f["lead"]
    pick = lambda xs: xs[rng.randrange(len(xs))]  # noqa: E731
    out = []
    for a in f["acts"]:
        out.append((a["ts"], "activity", a["lead"], act_text(f, a, pick)))
    for c in f["claims"]:
        lab, txt = claim_text(f, c)
        out.append((c["ts"], "statement", lab, txt))
    for m in f["fillers"]["msgs"]:
        who = L["primary"]["name"] if m.get("speaker", "primary") == "primary" else \
            (L["secondary"] or L["primary"])["name"]
        out.append((m["ts"], "statement", f"message from {who}", pick(FILLER_MSG)))
    for n in f["fillers"]["notes"]:
        out.append((n["ts"], "statement", "rep note", pick(FILLER_NOTE)))
    out.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    return out


def record_line(f: dict, levels: list) -> str | None:
    rec = f.get("record")
    if not rec:
        return None
    lv = levels[f["rub"]["levels"].index(rec["level"])]
    n = re.fullmatch(r"(\d+) weighted points", rec["score"]).group(1)
    return f"Recorded result in the CRM: total {n} weighted points, level {lv}"


def vendor(f: dict) -> str:
    return re.sub(r" sales team$", "", f["surface"].get("to", "the vendor"))


def render_state(f: dict, fmt: str, rng, levels: list) -> str:
    r = f["rub"]
    head = f"Lead scorecard {r['rid']} (version {r['version']}, in force from {r['effective']}), {vendor(f)}"
    rl = rubric_lines(f, levels)
    ld = lead_lines(f)
    fd = feed(f, rng)
    rec = record_line(f, levels)
    today = f"Scoring date: {f['today']}"
    if fmt == "crm":
        obj = {"scorecard": {"title": head, "sections": rl}, "scoring_date": f["today"], "lead": ld,
               "activity_log": [{"time": ts_short(t), "lead_id": lab, "activity": txt} for t, k, lab, txt in fd
                                if k == "activity"],
               "correspondence": [{"time": ts_short(t), "source": lab, "text": txt} for t, k, lab, txt in fd
                                  if k == "statement"],
               "recorded_result": rec}
        return mv.render_json(obj)
    if fmt == "packet":
        lines = [f"## {head}"] + rl + ["", "## Lead record", today] + [f"- {x}" for x in ld]
        lines += ["", "## Activity log (lead id | activity)"]
        lines += [f"- {ts_short(t)} | {lab} | {txt}" for t, k, lab, txt in fd if k == "activity"]
        lines += ["", "## Correspondence and notes"]
        lines += [f"- {ts_short(t)} | {lab} | {txt}" for t, k, lab, txt in fd if k == "statement"]
        if rec:
            lines += ["", "## CRM", rec]
        return "\n".join(lines)
    # timeline: one merged feed
    lines = [head] + rl + ["", today, "LEAD"] + ld + ["", "FEED (oldest first)"]
    for t, k, lab, txt in fd:
        if k == "activity":
            lines.append(f"{ts_short(t)} | activity under {lab} | {txt}")
        else:
            lines.append(f"{ts_short(t)} | {lab} | {txt}")
    if rec:
        lines += ["", rec]
    return "\n".join(lines)


def parse_state(text: str) -> dict:
    out = {"record": None}
    if text.startswith("{"):
        o = json.loads(text)
        rl, today, ld = o["scorecard"]["sections"], o["scoring_date"], o["lead"]
        acts = [(ts_long(a["time"]), a["lead_id"], a["activity"]) for a in o["activity_log"]]
        stm = [(ts_long(c["time"]), c["source"], c["text"]) for c in o["correspondence"]]
        rec = o["recorded_result"]
    else:
        L = text.split("\n")
        if L[0].startswith("## "):
            i = 1
            rl = []
            while L[i]:
                rl.append(L[i])
                i += 1
            today = L[L.index("## Lead record") + 1][len("Scoring date: "):]
            j = L.index("## Lead record") + 2
            ld = []
            while j < len(L) and L[j].startswith("- "):
                ld.append(L[j][2:])
                j += 1
            acts, stm, rec = [], [], None
            sec = None
            for ln in L:
                if ln.startswith("## "):
                    sec = ln
                    continue
                if sec and sec.startswith("## Activity log") and ln.startswith("- "):
                    t, lab, txt = ln[2:].split(" | ", 2)
                    acts.append((ts_long(t), lab, txt))
                elif sec == "## Correspondence and notes" and ln.startswith("- "):
                    t, lab, txt = ln[2:].split(" | ", 2)
                    stm.append((ts_long(t), lab, txt))
                elif sec == "## CRM" and ln:
                    rec = ln
        else:
            i = 1
            rl = []
            while L[i]:
                rl.append(L[i])
                i += 1
            today = L[i + 1][len("Scoring date: "):]
            j = L.index("LEAD") + 1
            ld = []
            while L[j]:
                ld.append(L[j])
                j += 1
            acts, stm, rec = [], [], None
            k = L.index("FEED (oldest first)") + 1
            while k < len(L) and L[k]:
                t, lab, txt = L[k].split(" | ", 2)
                if lab.startswith("activity under "):
                    acts.append((ts_long(t), lab[len("activity under "):], txt))
                else:
                    stm.append((ts_long(t), lab, txt))
                k += 1
            rest = [x for x in L[k:] if x]
            rec = rest[0] if rest else None
    out["rub"] = parse_rubric(rl)
    out["today"] = today
    out["lead"] = parse_lead(ld)
    out["acts"] = []
    for n, (t, lid, txt) in enumerate(acts):
        typ, status = parse_act(txt)
        out["acts"].append({"eid": f"a{n + 1}", "ts": t, "lead": lid, "type": typ, "status": status})
    out["claims"] = []
    for t, lab, txt in stm:
        c = parse_claim(out["lead"], lab, txt)
        if c is not None:
            c["ts"] = t
            out["claims"].append(c)
    if rec:
        m = re.fullmatch(r"Recorded result in the CRM: total (\d+) weighted points, level (.+)", rec)
        out["record"] = {"score": f"{m.group(1)} weighted points", "level": m.group(2)}
    return out


# ------------------------------------------------------------------------------------------------ questions
def q_text(kind: str, f: dict, wording: str | None = None) -> str:
    lid, rid = f["lead"]["id"], f["rub"]["rid"]
    if kind == "score":
        return f"Applying scorecard {rid} on the scoring date, which level does lead {lid} get?"
    if kind == "ready":
        return f"Applying scorecard {rid} on the scoring date, is lead {lid} sales-ready?"
    if kind == "ready_n":
        return f"Applying scorecard {rid} on the scoring date, does lead {lid} fall short of sales-ready?"
    if kind == "judge":
        return f"Is the result recorded in the CRM for lead {lid} (total and level) supported by scorecard {rid}?"
    if kind == "judge_n":
        return f"Does the result recorded in the CRM for lead {lid} (total and level) depart from scorecard {rid}?"
    if kind == "jb":
        if wording == "fallback":
            return f"Statement: lead {lid} is sales-ready under scorecard {rid}. Which option fits the file?"
        return f"Under scorecard {rid} on the scoring date, which statement about lead {lid} holds?"
    raise ValueError(kind)


Q_PATTERNS = [(k, re.escape(q_text(k, {"lead": {"id": "LIDX"}, "rub": {"rid": "RIDX"}}, w))
               .replace("LIDX", r"(?P<lid>\S+)").replace("RIDX", r"(?P<rid>\S+)"))
              for k, w in (("score", None), ("ready", None), ("ready_n", None), ("judge", None), ("judge_n", None),
                           ("jb", "fallback"), ("jb", None))]


def parse_question(s: str):
    for k, pat in Q_PATTERNS:
        m = re.fullmatch(pat, s)
        if m:
            return k, m.groupdict()
    raise ValueError(f"question {s!r}")


def yn_defs(kind: str, f: dict) -> dict:
    rid = f["rub"]["rid"]
    ready = f"the level scorecard {rid} gives on the scoring date is at or above its sales-ready level"
    notr = f"the level scorecard {rid} gives is below its sales-ready level"
    same = f"working scorecard {rid} through gives exactly the recorded total and the recorded level"
    diff = f"working scorecard {rid} through gives a different total or a different level than the record"
    return {"ready": {"yes": ready, "no": notr}, "ready_n": {"yes": notr, "no": ready},
            "judge": {"yes": same, "no": diff}, "judge_n": {"yes": diff, "no": same}}[kind]


def jb_descs(f: dict) -> tuple:
    lid, rid = f["lead"]["id"], f["rub"]["rid"]
    return f"Lead {lid} is sales-ready under scorecard {rid}.", f"Lead {lid} is not sales-ready under scorecard {rid}."


# ------------------------------------------------------------------------------------------------ load + plan
def sample(plan_rows: dict) -> list:
    """gen3_lead_score.sample_latents("devx", plan) with each latent's tier kept (sample_latents itself drops it):
    the same steps (PLAN_ROWS / ATTACK_ROWS swapped in for the devx split, LeadScoreBuilder.build_split, base rows
    only), reading the tier from the base row's meta. Nothing is written."""
    g5 = _g5()
    saved = (dict(g5.PLAN_ROWS), dict(g5.ATTACK_ROWS))
    try:
        g5.PLAN_ROWS["devx"] = dict(plan_rows)
        g5.ATTACK_ROWS["devx"] = {k: 0 for k in plan_rows}
        fb = mv.FamilyBuilder(KEY, generator_file=g5.__file__, check_tz=True)
        b = g5.LeadScoreBuilder(fb)
        b.build_split("devx")
    finally:
        g5.PLAN_ROWS.clear()
        g5.PLAN_ROWS.update(saved[0])
        g5.ATTACK_ROWS.clear()
        g5.ATTACK_ROWS.update(saved[1])
    out = []
    for r in fb.rows:
        if r["meta"]["view"] != "base":
            continue
        kind = b.kind_of[r["rid"]]
        f = copy.deepcopy(b.facts[r["meta"]["latent_id"]])
        q = {"kind": g5.QUERY_OF_KIND[kind]}
        out.append({"latent_id": r["meta"]["latent_id"], "kind": kind, "query": q, "facts": f,
                    "gold": g5.decide(f, q)[0], "tier": r["meta"]["tier"]})
    return out


def load(plan_rows: dict | None = None) -> list:
    xs = sample(plan_rows or PLAN)
    items = []
    for x in xs:
        f = x["facts"]
        assert f["arch"] == "weighted" and not f["rub"].get("amend") and not f["rub"].get("override"), x["latent_id"]
        assert f["rub"].get("per_type_max") is None and f["rub"].get("unsub") is None, x["latent_id"]
        q = x["query"]["kind"]
        g = decide(f, q)
        assert g == x["gold"], (x["latent_id"], g, x["gold"])
        tier = _tier(x)
        items.append(dx.Item(x["latent_id"], tier, f["pack"], x["kind"], f, x["query"], g, {}))
    return items


def _tier(x) -> str:
    return x["tier"]


LAST_PLAN_REPORT: dict = {}
COUNTS = {"score": 75, "ready": 9, "judge": 9, "jb": 7}


def plan(items: list, rng) -> list:
    """75 score rows (gold levels as even as possible per K), 9 sales-ready, 9 judge, 7 JB rows, in sample order;
    yes/no gold balanced by the inverse wordings (dx.balance_assign)."""
    sc_pool = [it for it in items if it.kind in ("score", "score_rec")]
    by_k = Counter()
    score, cnt = [], Counter()
    # even levels: cap per (K, level), raised step by step until 75 rows are taken
    for cap in range(1, 40):
        for it in sc_pool:
            if len(score) >= COUNTS["score"]:
                break
            K = len(it.facts["rub"]["levels"])
            lv = it.facts["rub"]["levels"].index(it.gold0)
            if it not in score and cnt[(K, lv)] < cap:
                score.append(it)
                cnt[(K, lv)] += 1
                by_k[K] += 1
        if len(score) >= COUNTS["score"]:
            break
    yn_pool = {k: [it for it in items if it.kind == k] for k in ("ready", "judge", "jb")}
    picks = {}
    for k in ("ready", "judge", "jb"):
        ys = [it for it in yn_pool[k] if it.gold0 == "yes"]
        ns = [it for it in yn_pool[k] if it.gold0 == "no"]
        n = COUNTS[k]
        take = ys[: (n + 1) // 2] + ns[: n // 2]
        if len(take) < n:
            take += [it for it in yn_pool[k] if it not in take][: n - len(take)]
        picks[k] = take
    rot = dx.Rotor(rng)
    out = []
    for it in score:
        out.append((it, {"v": "score", "fmt": rot.pick("fmt", FMTS, ("score",))}))
    units, meta = [], []
    for it in picks["jb"]:
        t = it.gold0 == "yes"
        units.append([({"qk": "jb", "fmt": f, "tier": it.tier, "pack": it.pack, "pol": 0}, t) for f in FMTS])
        meta.append((it, [("jb", f) for f in FMTS]))
    for k in ("ready", "judge"):
        for it in picks[k]:
            t = it.gold0 == "yes"
            cands, cm = [], []
            for neg in (False, True):
                for f in FMTS:
                    cands.append(({"qk": "yn", "tpl": (k, neg), "fmt": f, "tier": it.tier, "pack": it.pack,
                                   "pol": int(neg)}, t != neg))
                    cm.append((k + ("_n" if neg else ""), f))
            units.append(cands)
            meta.append((it, cm))
    ch = dx.balance_assign(units, rng)
    for (it, cm), i in zip(meta, ch):
        v, f = cm[i]
        out.append((it, {"v": v, "fmt": f}))
    LAST_PLAN_REPORT.clear()
    LAST_PLAN_REPORT.update({"views": dict(Counter(v["v"] for _, v in out)),
                             "score_levels": {f"K{k}:L{l}": n for (k, l), n in sorted(cnt.items())}})
    out.sort(key=lambda x: x[0].lid)
    return out


# ------------------------------------------------------------------------------------------------ render
def levels_of(f: dict) -> list:
    return list(LEVELS[len(f["rub"]["levels"])])


def edges(f: dict) -> tuple:
    tags = set(t for t in f["surface"].get("sample_edges", ()) if t in mv.EDGE_TAGS)
    r = f["rub"]
    if any(c["speaker"] in ("rep", "boss") for c in f["claims"]):
        tags.add("hc:rep_note_ignored")
    if any(c["kind"] == "budget" and c["period"] != r["budget"]["period"] for c in f["claims"]):
        tags.add("hc:monthly_vs_annual")
    if any(r["title_sen"].get(f["lead"]["primary"]["title"]) == 0 for _ in [0]):
        tags.add("hc:assistant_title_zero")
    return tuple(sorted(tags))


def render(it: dx.Item, view: dict, fb, rng) -> mv.RowSpec:
    f, v, fmt = it.facts, view["v"], view["fmt"]
    lv = levels_of(f)
    state = render_state(f, fmt, rng, lv)
    e = edges(f)
    if v == "score":
        g = lv[f["rub"]["levels"].index(it.gold0)]
        opts = fb.score_options(lv)
        return mv.RowSpec("base", "score", state, q_text("score", f), g, FMT_META[fmt], "dx5_" + fmt, "dx5.score",
                          options=opts, levels=len(lv), edge=e)
    if v == "jb":
        y, n = jb_descs(f)
        opts, gold, wording = fb.jb(y, n, it.gold0 == "yes", rng, stratum=("dx5",))
        return mv.RowSpec("jb", "jb", state, q_text("jb", f, wording), gold, FMT_META[fmt], "dx5_" + fmt,
                          "dx5.jb" + ("f" if wording == "fallback" else ""), options=opts, polarity=0, edge=e)
    neg = v.endswith("_n")
    yes = (it.gold0 == "yes") != neg
    return mv.RowSpec("base", "yn", state, q_text(v, f), "yes" if yes else "no", FMT_META[fmt], "dx5_" + fmt,
                      "dx5." + v, defs=yn_defs(v, f), polarity=int(neg), role="neg" if neg else "aff",
                      judge=v.startswith("judge"), edge=e)


# ------------------------------------------------------------------------------------------------ parse-back
def parse(g: dict) -> dict:
    st = parse_state(g["state"])
    k, d = parse_question(g["instructions"])
    if d["lid"] != st["lead"]["id"]:
        raise ValueError("question names another lead")
    return {"st": st, "kind": k, "options": g["options"]}


def parsed_facts(p: dict) -> dict:
    st = p["st"]
    r = dict(st["rub"])
    rec = st["record"]
    return {"arch": "weighted", "today": st["today"], "rub": r, "lead": dict(st["lead"], decoy_id=None,
                                                                             lookalike=None),
            "acts": st["acts"], "claims": st["claims"], "record": rec}


def relabel(p: dict, g: dict):
    f = parsed_facts(p)
    k = p["kind"]
    if k == "score":
        return decide(f, "score")
    if k in ("ready", "ready_n"):
        v = decide(f, "ready")
        return v if k == "ready" else ("no" if v == "yes" else "yes")
    if k in ("judge", "judge_n"):
        v = decide(f, "judge")
        if mv.is_undefined(v):
            raise ValueError("judge undefined on the parsed file")
        return v if k == "judge" else ("no" if v == "yes" else "yes")
    v = decide(f, "jb")
    return p["options"][0] if v == "yes" else p["options"][1]


def _proj(f: dict, levels_map) -> dict:
    r = f["rub"]
    L = f["lead"]
    acts = tuple(sorted((a["ts"], a["lead"], a["type"], a["status"]) for a in f["acts"]))
    cl = tuple(sorted((c["ts"], c["kind"], c["speaker"], c["channel"], c.get("status"), c.get("amount"),
                       c.get("period"), c.get("date"), c.get("need")) for c in f["claims"]))
    rec = f.get("record")
    return {"today": f["today"], "levels": len(r["levels"]), "handoff": r["handoff"],
            "size_source": r["size_source"], "title_sen": tuple(sorted(r["title_sen"].items())),
            "role_map": tuple(sorted(r["role_map"].items())), "fit": json.dumps(r["fit_bands"]),
            "eng": json.dumps(r["eng_bands"]), "acts_pts": tuple(sorted(r["acts"].items())),
            "window": (r["window"]["days"], r["window"]["incl"]), "cap": r.get("cap"),
            "budget": (r["budget"]["amount"], r["budget"]["period"]), "tiers": tuple(r["timeline"]["tiers"]),
            "rep_tl": bool(r["rep_timeline"]), "weights": tuple(sorted(r["weights"].items())),
            "thresholds": tuple(r["thresholds"]), "dq": tuple(r["dq"]),
            "dq_lists": (tuple(r["competitors"]) if "competitor" in r["dq"] else (),
                         tuple(r["personal_domains"]) if "personal_email" in r["dq"] else (),
                         tuple(r["regions"]) if "region" in r["dq"] else (),
                         r.get("min_size") if "small" in r["dq"] else None),
            "lead": (L["id"], L["company"], L["region"], L["customer"], L["primary"]["name"], L["primary"]["title"],
                     L["primary"]["email"], L["size_enrich"], tuple(L["size_form"]),
                     (L["secondary"] or {}).get("name")),
            "acts": acts, "claims": cl,
            "record": (rec["score"], levels_map(rec["level"])) if rec else None}


def project(it: dx.Item) -> dict:
    f = it.facts
    lv = levels_of(f)
    return _proj(f, lambda x: lv[f["rub"]["levels"].index(x)])


def project_parsed(p: dict) -> dict:
    return _proj(parsed_facts(p), lambda x: x)
