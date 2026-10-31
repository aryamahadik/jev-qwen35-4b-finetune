"""gen_numeric_dates: policy excerpt + realistic scenario decisions that hinge on numbers, units, dates and time
(yes/no and choice, labels by construction, fact-flip twins).

Each item shows a short policy excerpt from a real-world setting (HR, refunds, insurance, shipping, pharmacy, travel,
grants, school rules, sports, finance, utilities, clubs) and a scenario; a small decision function applies the rule
exactly. Every schema has TWO independent implementations of its decision (for example a day loop and numpy's
busday_count, Fraction and Decimal arithmetic, zoneinfo and the stated UTC offsets); they are asserted equal for every
row, and the written file is re-checked from meta.orig_label["facts"] (the facts re-render to the exact state text).

Question types (meta.defs = qid):
  pos     direct yes/no question about the condition ('Is X eligible ...?')
  neg     the complementary / negated outcome ('Is X too old ...?', 'Was the request made too late?')
  claim   a named person states a conclusion (reported speech); 'Is <speaker> right?'
  est     'Do the stated facts establish that ...?'  (a hidden decisive fact -> no; its twin reveals it -> yes)
  letter  (A)-(D) choice of an exact value (date, amount, dose, duration); wrong options are typical mistakes
          (calendar vs business days, forgot the leap day, wrong rounding, wrong UTC offset, percent of the wrong base)
  cat_<schema>  categorical outcome with fixed options (e.g. on time / late with penalty / rejected)
Every base item gets a twin (meta.twin_of) that changes ONE decisive fact so the gold answer changes; yes/no pairs
therefore hold one yes and one no. Deterministic (seed 20261215), CPU only.
"""
import collections
import hashlib
import json
import os
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "moral_social_norms"))
from common import EDGE_TAGS, check_rows, norm, summary, write_defs  # noqa: E402
from nd_common import NEG_RE, Sty  # noqa: E402
import nd_time  # noqa: E402
import nd_time2  # noqa: E402
import nd_money  # noqa: E402
import nd_units  # noqa: E402

KEY = "gen_numeric_dates"
SEED = 20261215
FAMILY = "numeric_temporal"
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
LETTERS = ["A", "B", "C", "D"]
TARGET_PAIRS = 12500  # -> about 25,000 rows (base + fact-flip twin)

SCHEMAS = [
    nd_time.AgeCutoff(), nd_time.AgeBand("rental"), nd_time.AgeBand("youth"), nd_time.SubmissionDeadline(),
    nd_time.BusinessDays(), nd_time.DayWindow(),
    nd_time2.MonthAdd(), nd_time2.DateValidity(), nd_time2.TzDeadline(), nd_time2.FlightDuration(), nd_time2.GapDuration(),
    nd_time2.PaydaySchedule(), nd_time2.Schengen(), nd_time2.ShippingDispatch(), nd_time2.MedExpiry(),
    nd_money.Discounts(), nd_money.VatExpense(), nd_money.IncomeTax(), nd_money.InsurancePayout(), nd_money.CurrencyExpense(),
    nd_money.GpaHonors(), nd_money.PassMark(), nd_money.TimeclockOvertime(), nd_money.CashRounding(), nd_money.Attendance(),
    nd_money.PercentChange(), nd_money.Quorum(), nd_money.TieredBill(), nd_money.ParkingFee(), nd_money.LatePenalty(),
    nd_units.DosePerKg(), nd_units.DoseTiming(), nd_units.Baggage(), nd_units.ColdChain(), nd_units.SpeedTicket(),
    nd_units.RideHeight(), nd_units.MarathonQualify(), nd_units.WinPct(), nd_units.FmlaEligibility(), nd_units.BenefitsStart(),
    nd_units.OvertimeWeekly(), nd_units.GrantBudget(), nd_units.RefundCategory(), nd_units.LibraryFine(), nd_units.InterestDays(),
    nd_units.DtiLtv(), nd_units.AvgDailyBalance(),
]

QDEFS = {
    "pos": {"yes": "Applying the policy's numbers, dates, times, units and stated counting, rounding and conversion rules exactly to the facts, what the question asks is true; a value exactly on an inclusive limit ('at least', 'by', 'no later than') counts as meeting it.",
            "no": "Applied exactly, what the question asks is false: the computed value falls on the wrong side of the limit, lands exactly on an exclusive limit ('before', 'under', 'more than'), or another stated condition fails."},
    "neg": {"yes": "The unfavourable or negated outcome the question names (for example too old, late, over the limit, refused) really follows when the policy's numbers, dates and stated counting and rounding rules are applied exactly to the facts.",
            "no": "Applied exactly, that unfavourable outcome does not follow: the requirement or limit is actually met, including a value exactly on an inclusive limit, or an exception in the policy covers the case."},
    "claim": {"yes": "The person's statement matches what the policy gives when its numbers, dates, units and counting or rounding rules are applied exactly to the stated facts.",
              "no": "The person's statement is wrong once the policy is applied exactly (for example an off-by-one day, a missed holiday, leap day, time-zone offset, unit conversion or rounding step)."},
    "est": {"yes": "The facts as stated are enough to show, by exact calculation under the policy, that the condition in the question holds.",
            "no": "Either the exact calculation shows the condition does not hold, or a fact needed to decide (such as a time, date, weight or amount) is not stated, so it is not established."},
    "letter": {x: (f"Option ({x}) gives the exact value that results from applying the policy's rules (dates, business days, "
                   f"time zones, units, rounding, caps and exceptions) to the facts; the other options reflect calculation errors.")
               for x in LETTERS},
}


def edge_join(tags):
    tags = [t for t in dict.fromkeys(tags) if t]
    for t in tags:
        assert t in EDGE_TAGS, t
    return ",".join(sorted(tags)) if tags else None


EST_Q = ["Do the stated facts establish that {c}?", "Based only on the information given, can one conclude that {c}?",
         "Is it established by the facts above that {c}?"]
CLAIM_Q = ["Is {s} right?", "Under the policy, is {s} correct?", "Given the policy and the facts, is what {s} said accurate?"]


def pronominal(f, intro, clause):
    """'X told him that Ravi is ...' -> 'X told him that he is ...' when the addressee is the person named first."""
    who = f.get("who")
    if not who or who[1] == "they" or not intro.endswith(f" told {who[2]} that"):
        return clause
    name = who[0]
    if clause.startswith(name + "'s "):
        return who[3] + clause[len(name) + 2:]
    if clause.startswith(name + " "):
        return who[1] + clause[len(name):]
    return clause


def cap1(s):
    return s[:1].upper() + s[1:]


class Builder:
    def __init__(self):
        self.rng = random.Random(SEED)
        self.seen = set()
        self.pairs = []
        self.stats = collections.Counter()

    # ------------------------------------------------------------------ checks shared with the file re-check
    @staticmethod
    def agree(s, f):
        if s.preds_list:
            a, b = s.preds(f), s.preds2(f)
            assert a == b, (s.name, "preds", a, b, f)
        if s.cat:
            a, b = s.catv(f), s.catv2(f)
            assert a == b, (s.name, "cat", a, b, f)
        if s.letter:
            a, b = s.val(f), s.val2(f)
            if a is not None or b is not None:
                assert a == b, (s.name, "val", a, b, f)

    @staticmethod
    def diff_keys(s, f, g):
        ign = set(getattr(s, "derived_keys", ())) | {"sty"}
        return [k for k in set(f) | set(g) if k not in ign and f.get(k) != g.get(k)]

    # ------------------------------------------------------------------ one pair
    def make_pair(self, s, idx):
        rng = self.rng
        modes = []
        if s.preds_list:
            modes = list(s.yn_modes.items())
            if any(s.can_hide(q) for q in s.preds_list):
                modes = [("pos", 0.36), ("neg", 0.2), ("claim", 0.16), ("est", 0.28)]
        choice_kinds = [k for k, on in (("cat", bool(s.cat)), ("letter", s.letter)) if on]
        if choice_kinds and (not modes or rng.random() < s.choice_share):
            mode = rng.choice(choice_kinds)
        else:
            r, acc = rng.random() * sum(w for _, w in modes), 0
            mode = modes[-1][0]
            for m, w in modes:
                acc += w
                if r < acc:
                    mode = m
                    break
        p = rng.choice(s.preds_list) if mode not in ("cat", "letter") else None
        if mode in ("pos", "neg", "claim", "est"):
            q = None
            hidden = False
            if mode == "est" and s.can_hide(p) and rng.random() < 0.65:
                for _ in range(80):
                    f = s.sample(rng)
                    if s.valid(f) and s.preds(f)[p] is True:
                        break
                else:
                    return None
                base = s.hide(f, p, rng)
                if base is None or s.preds(base)[p] is not None:
                    return None
                twin, hidden = f, True
            else:
                for _ in range(80):
                    f = s.sample(rng)
                    if s.valid(f) and s.preds(f)[p] is not None:
                        break
                else:
                    return None
                v = s.preds(f)[p]
                twin = s.flip(f, rng, lambda g: s.preds(g)[p] is (not v))
                if twin is None:
                    return None
                base = f
            self.agree(s, base)
            self.agree(s, twin)
            vb, vt = s.preds(base)[p], s.preds(twin)[p]
            pq = s.pq(base, p)
            if mode == "neg" and not pq["neg"]:
                mode = "pos"
            qi = rng.randrange(10 ** 6)
            pol = rng.random() < 0.5
            out = []
            for fx, v in ((base, vb), (twin, vt)):
                st = s.render(fx)
                pqx = s.pq(fx, p)
                if mode == "pos":
                    q = pqx["pos"][qi % len(pqx["pos"])]
                    gold = "yes" if v is True else "no"
                elif mode == "neg":
                    q = pqx["neg"][qi % len(pqx["neg"])]
                    gold = "yes" if v is False else "no"
                elif mode == "est":
                    q = EST_Q[qi % len(EST_Q)].format(c=pqx["cpos"])
                    gold = "yes" if v is True else "no"
                else:
                    intro, short = pqx["speakers"][qi % len(pqx["speakers"])]
                    st = st + "\n\n" + f"{intro} {pronominal(fx, intro, pqx['cpos'] if pol else pqx['cneg'])}."
                    q = CLAIM_Q[(qi // 7) % len(CLAIM_Q)].format(s=short)
                    gold = "yes" if (v is pol) else "no"
                out.append((st, q, gold, fx, v))
            if out[0][2] == out[1][2]:
                return None
            ans = {"mode": mode, "pred": p, "claim_pol": pol if mode == "claim" else None}
        elif mode == "cat":
            target = rng.choice(s.cat)
            for _ in range(200):
                f = s.sample(rng)
                if s.valid(f) and s.catv(f) == target:
                    break
            else:
                return None
            others = [c for c in s.cat if c != target]
            t2 = rng.choice(others)
            twin = s.flip(f, rng, lambda g: s.catv(g) == t2)
            if twin is None:
                twin = s.flip(f, rng, lambda g: s.catv(g) is not None and s.catv(g) != target)
            if twin is None:
                return None
            base = f
            self.agree(s, base)
            self.agree(s, twin)
            qs = s.cat_q(base)
            q = qs[rng.randrange(len(qs))]
            out = [(s.render(fx), q, s.catv(fx), fx, s.catv(fx)) for fx in (base, twin)]
            ans = {"mode": "cat"}
            hidden = False
        else:  # letter
            for _ in range(80):
                f = s.sample(rng)
                if s.valid(f) and s.val(f) is not None:
                    break
            else:
                return None
            v0 = s.fmtv(f, s.val(f))
            twin = s.flip(f, rng, lambda g: s.val(g) is not None and s.fmtv(g, s.val(g)) != v0)
            if twin is None:
                return None
            base = f
            self.agree(s, base)
            self.agree(s, twin)
            vb, vt = s.fmtv(base, s.val(base)), s.fmtv(twin, s.val(twin))
            opts = [vb, vt]
            for w in list(s.wrongs(base)) + list(s.wrongs(twin)):
                try:
                    t = s.fmtv(base, w)
                except (ValueError, AssertionError):
                    continue
                if t not in opts:
                    opts.append(t)
            if len(opts) < 4:
                return None
            opts = opts[:2] + rng.sample(opts[2:], 2)
            rng.shuffle(opts)
            qs = s.letter_q(base)
            q = qs[rng.randrange(len(qs))]
            otxt = "\n\nOptions:\n" + "\n".join(f"({L}) {o}" for L, o in zip(LETTERS, opts))
            out = [(s.render(fx) + otxt, q, LETTERS[opts.index(v)], fx, v) for fx, v in ((base, vb), (twin, vt))]
            ans = {"mode": "letter", "options": opts}
            hidden = False
        d = self.diff_keys(s, out[0][3], out[1][3])
        assert len(d) == 1, (s.name, d)
        (sb, qb, gb, fb, vb), (st_, qt, gt, ft_, vt) = out
        nb, nt = norm(sb), norm(st_)
        if gb == gt or nb == nt or nb in self.seen or nt in self.seen:
            return None
        self.seen.update({nb, nt})
        qid = mode if mode in ("pos", "neg", "claim", "est", "letter") else f"cat_{s.name}"
        rows = []
        rid = f"{KEY}-{s.name}-{idx:05d}"
        for j, (stx, qx, gx, fx, vx) in enumerate(out):
            tags = list(s.edges(fx, p))
            negr = getattr(s, "neg_rule", lambda _f: False)(fx)
            if mode == "neg" and NEG_RE.search(qx):
                tags.append("negation")
                if negr:
                    tags.append("double_negation")
            if mode == "claim":
                tags.append("reported_speech")
                cl = stx.rsplit("\n\n", 1)[-1]
                if NEG_RE.search(cl):
                    tags.append("negation")
                    if negr:
                        tags.append("double_negation")
            if mode == "est" and hidden and j == 0:
                tags.append("missing_info")
            if mode == "est" and hidden and j == 1:
                tags = [t for t in tags if t != "missing_info"]
            if getattr(s, "multi_hop", False):
                tags.append("multi_hop")
            if getattr(s, "table", False):
                tags.append("table")
            if getattr(s, "units", False):
                tags.append("units")
            orig = {"schema": s.name, "qid": qid, **{k: v for k, v in ans.items() if v is not None},
                    "value": vx if not isinstance(vx, bool) else ("true" if vx else "false") if vx is not None else "undetermined",
                    "facts": fx}
            if vx is None:
                orig["value"] = "undetermined"
            meta = {"dataset": f"program generator golden_src/gen/{KEY}.py", "config": f"{s.name}:{qid}",
                    "revision": "", "licence": "Generated by Claude-written program in this repo (no third-party text)",
                    "split": "train", "orig_label": orig, "family": FAMILY, "edge": edge_join(tags), "defs": qid}
            if j == 1:
                meta["twin_of"] = rid
            rows.append({"key": KEY, "rid": rid if j == 0 else rid + "-twin", "state": stx, "instructions": qx,
                         "options": (["yes", "no"] if mode in ("pos", "neg", "claim", "est") else
                                     (LETTERS if mode == "letter" else list(s.cat))),
                         "gold": gx, "soft": None, "meta": meta})
        self.stats[(s.name, qid)] += 1
        return rows

    def run(self, scale=1.0):
        for s in SCHEMAS:
            quota = max(1, int(round(s.quota * scale)))
            made = tries = 0
            while made < quota and tries < quota * 60:
                tries += 1
                r = self.make_pair(s, made)
                if r is None:
                    continue
                self.pairs.append(r)
                made += 1
            print(f"{s.name:28s} pairs={made:5d} tries={tries}", flush=True)
            if made < quota:
                print(f"   WARNING: {s.name} under quota ({made}/{quota})")
        return self.pairs


SCHEMA_BY_NAME = {s.name: s for s in SCHEMAS}


def recheck(path):
    """Independent pass over the written file: every gold is recomputed from meta.orig_label.facts."""
    n = 0
    by_rid = {}
    for line in open(path):
        r = json.loads(line)
        o = r["meta"]["orig_label"]
        s = SCHEMA_BY_NAME[o["schema"]]
        f = o["facts"]
        Builder.agree(s, f)
        base_state = s.render(f)
        assert r["state"].startswith(base_state), (r["rid"], "render mismatch")
        q = o["qid"]
        if q in ("pos", "neg", "est", "claim"):
            v, v2 = s.preds(f)[o["pred"]], s.preds2(f)[o["pred"]]
            assert v == v2
            exp = {"pos": v is True, "neg": v is False, "est": v is True,
                   "claim": v is not None and v == o.get("claim_pol")}[q]
            assert r["gold"] == ("yes" if exp else "no"), (r["rid"], q, v, r["gold"])
            assert r["options"] == ["yes", "no"]
        elif q == "letter":
            opts = o["options"]
            want = s.fmtv(f, s.val(f))
            assert want == s.fmtv(f, s.val2(f))
            assert opts.count(want) == 1
            assert r["gold"] == LETTERS[opts.index(want)], r["rid"]
            assert r["state"].endswith("\n".join(f"({L}) {x}" for L, x in zip(LETTERS, opts)))
        else:
            assert r["gold"] == s.catv(f) == s.catv2(f), r["rid"]
        by_rid[r["rid"]] = r
        n += 1
    for rid, r in by_rid.items():
        t = r["meta"].get("twin_of")
        if t:
            b = by_rid[t]
            assert b["gold"] != r["gold"] and b["meta"]["defs"] == r["meta"]["defs"], rid
    print(f"recheck OK: {n} rows, every gold recomputed from facts with both implementations")


def yesno_share(rows):
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    return round(sum(r["gold"] == "yes" for r in yn) / len(yn), 4) if yn else None


def upsert_manifest(rec):
    line = json.dumps(rec, ensure_ascii=False)
    for _ in range(20):
        text = MANIFEST.read_text() if MANIFEST.exists() else ""
        lines = text.splitlines()
        mine = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("key") == rec["key"]]
        if not mine:
            with open(MANIFEST, "a") as fh:
                fh.write(line + "\n")
            return
        for i in mine:
            assert json.loads(lines[i]).get("family") == FAMILY
        new = [ln for i, ln in enumerate(lines) if i not in set(mine)] + [line]
        tmp = MANIFEST.with_suffix(".jsonl.tmp_nd")
        tmp.write_text("\n".join(new) + "\n")
        if (MANIFEST.read_text() if MANIFEST.exists() else "") == text:
            os.replace(tmp, MANIFEST)
            return
        tmp.unlink()
        time.sleep(0.2)
    raise RuntimeError("manifest kept changing")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=float, default=None, help="default: TARGET_PAIRS / sum of schema quotas")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    b = Builder()
    scale = a.scale if a.scale is not None else TARGET_PAIRS / sum(s.quota for s in SCHEMAS)
    pairs = b.run(scale)
    rng = random.Random(SEED + 1)
    rng.shuffle(pairs)
    rows = [r for pr in pairs for r in pr]
    rev = "gen-v1+sha256:" + hashlib.sha256(b"".join(p.read_bytes() for p in sorted(HERE.glob("nd_*.py")) +
                                                   [Path(__file__).resolve()])).hexdigest()[:16]
    for r in rows:
        r["meta"]["revision"] = rev
    check_rows(rows)
    summary(rows)
    if a.dry:
        out = Path(os.environ.get("ND_DRY_OUT", "/tmp/nd_dry.jsonl"))
    else:
        RAW.mkdir(parents=True, exist_ok=True)
        out = RAW / f"{KEY}.jsonl"
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    recheck(out)
    if a.dry:
        return
    defs = dict(QDEFS)
    for s in SCHEMAS:
        if s.cat:
            defs[f"cat_{s.name}"] = s.cat_defs
    for qid, d in defs.items():
        write_defs(f"{KEY}__{qid}", d)
    et = sorted({t for r in rows for t in (r["meta"]["edge"] or "").split(",") if t})
    nsch = len(SCHEMAS)
    upsert_manifest({"key": KEY, "family": FAMILY, "dataset": f"{KEY} (program generator, golden_src/gen/{KEY}.py + nd_*.py)",
                     "licence": "n/a (program-generated; Claude-written templates and rules, labels by construction)",
                     "rows": len(rows), "qtype": "yesno+choice", "yesno_share": yesno_share(rows), "edge_tags": et,
                     "notes": NOTES.format(nsch=nsch, rows=len(rows))})


NOTES = ("program-generated policy excerpt + scenario decisions hinging on numbers, units, dates and time ({nsch} schemas: "
         "age on a date incl. 29 Feb births, deadlines with inclusive/exclusive wording + grace + extensions, business days "
         "with listed holidays, day-0/day-1 windows across leap days, month-end clamping, calendar validity (1900/2000/2100), "
         "time zones with stated UTC offsets (DST, half-hour zones, date line), flight times, rest/fasting gaps across "
         "midnight, paydays, Schengen 90/180, dispatch cut-offs, expiry vs in-use periods, discounts, VAT, tax bands, "
         "deductible/coinsurance/OOP, FX tables, GPA/percent rounding rules, 7-minute punch rounding, cash rounding, "
         "attendance, percent vs percentage points, quorum/majority, tiered bills, parking, late penalties, dose per kg, "
         "dose timing, baggage lb/in, Fahrenheit logs, speed thresholds km/h vs mph, ride height in vs cm, marathon "
         "standards, win percentage, leave eligibility, benefits start, overtime, grant indirect caps, refunds, library "
         "fines, day-count interest, DTI/LTV, average daily balance); every item has a fact-flip twin (meta.twin_of) whose "
         "one changed fact flips the answer (yes/no share exactly 0.5 per schema); two independent implementations per "
         "schema asserted equal and the written file re-checked from meta.orig_label.facts; qids pos/neg/claim/est "
         "(yes/no; est includes hidden-fact -> no) + letter (A-D exact value, distractors = typical errors) + "
         "cat_<schema>. Deterministic (seed 20261215). NOTE: {rows} rows exceed build_v14_golden.py CAP=12000 per key "
         "(the assembler keeps whole twin groups).")

if __name__ == "__main__":
    main()
