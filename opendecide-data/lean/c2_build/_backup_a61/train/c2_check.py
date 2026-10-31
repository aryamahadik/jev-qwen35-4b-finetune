"""c2_check.py: the C2 training chain's money and stop-rule checks (PREREG A37 j/k, A42-D 2.1-2.4; spec 5.5, 10.4).

A port of c_build/endgame/r1_check.py (read only, never edited) with the C2 numbers:
  * C2 Modal cap $40 over EVERY C2 Modal line on any account (A42-D 2.1); training <= T_max (2.3), fixed ONCE at the
    training GO:  T_max = min($34, $32 - C2 Modal spend to date), spend to date = logs/c2_spend.jsonl (the non-training
    lines: pilots, reads, OHS-AC, ...; `spend` adds one).  $32 = $40 - $4 evaluation - $2 SPEED-3 - $2 reserve.
  * A37 (k) as changed by A42-D 2.3: STOP and ask when the steps-100-300 projection is above T_max (was $17).
  * Accounts: free credit first, mahadikarya2 then (relay) mahadikarya3; no card (aryamhd) is ever accepted here.
    Each segment is capped by min(training budget left under T_max, free credit left on the account, 540 min); when the
    credit is the binding cap the verdict is RELAY (exit 3): copy the run to the next account (c2_chain.sh copy).
  Every command prints its fields and ends with one verdict line; EXIT CODE 0 only on GO, 3 RELAY, 1 everything else.

  cd lean && ../.venv/bin/python -B c2_build/train/c2_check.py tmax [--fix]
                                                      first100 | proj | seg --profile P | spend --usd X --what W --profile P
                                                      status [--profile P] | ledger "text" --profile P
Segments are recorded by c2_chain.sh in logs/c2_segments.jsonl (open line, then closed line, as r1_segments.jsonl).
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
LOGS = HERE / "logs"
NAME = "q35_4b_c2"
PROFILES = ("mahadikarya2", "mahadikarya3")     # A42-D 2.4; the card account is never accepted here
USD_H = 4.09                                    # spec 5.5 / A28 (Modal lists 3.95; the higher one is used)
ALLOW = 2.0                                     # spec 9.2: smoke and overhead on top of training time
CAP_TOTAL, TMAX_CAP, TMAX_BASE = 40.0, 34.0, 32.0
FN_TIMEOUT_MIN, SEG_MARGIN_MIN, LOAD_SAVE_MIN = 600, 60, 8
SEG_MAX_MIN = FN_TIMEOUT_MIN - SEG_MARGIN_MIN   # 540
MIN_SEG_MIN = 10
CREDIT_RESERVE = 1.0                            # dollars of free credit never planned
BILL_LAG_S = 75 * 60
DEFAULT_REF_SPS = 3.716                         # round 1's measured pessimistic s/step (spec 9.2)
LOSS_KEYS = ("loss", "task", "cons", "cons_comp", "cons_equiv", "inv", "perm", "kl", "ord")


def _bill(profile: str) -> dict:
    sys.path.insert(0, str(LEAN / "c_build/endgame"))
    import spend_guard
    return spend_guard.bill(profile)


BILL = _bill            # tests replace this
NOW = time.time         # tests replace this


def j(p: Path):
    try:
        return json.loads(Path(p).read_text())
    except Exception:  # noqa: BLE001
        return None


def read_jsonl(p: Path) -> list:
    out = []
    for line in (Path(p).read_text().splitlines() if Path(p).exists() else []):
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


class Verdict(Exception):
    def __init__(self, kind: str, rec: dict, verdict: str, code: int):
        super().__init__(verdict)
        self.kind, self.rec, self.verdict, self.code = kind, rec, verdict, code


def done(kind: str, rec: dict, verdict: str, code: int | None = None):
    code = (0 if verdict == "GO" else 3 if verdict.startswith("RELAY") else 1) if code is None else code
    raise Verdict(kind, rec, verdict, code)


# ----------------------------------------------------------------------------------------------- money
def spend_other(logs: Path | None = None) -> float:
    return round(sum(float(r.get("usd", 0)) for r in read_jsonl((logs or LOGS) / "c2_spend.jsonl")), 4)


def tmax_value(other: float) -> float:
    return round(min(TMAX_CAP, TMAX_BASE - other), 2)


def tmax(fix: bool = False, logs: Path | None = None) -> float:
    """T_max (A42-D 2.3): fixed once at the training GO (logs/c2_tmax.json), then read back unchanged."""
    logs = logs or LOGS
    rec = j(logs / "c2_tmax.json")
    if rec:
        return float(rec["t_max"])
    other = spend_other(logs)
    t = tmax_value(other)
    if fix:
        if t <= 0:
            done("tmax", {"spent_other": other, "t_max": t}, "STOP: no training budget left under the $40 cap")
        logs.mkdir(parents=True, exist_ok=True)
        (logs / "c2_tmax.json").write_text(json.dumps(
            {"t_max": t, "spent_other_usd": other, "cap_total": CAP_TOTAL, "formula": "min(34, 32 - spend to date)",
             "fixed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW()))}, indent=1))
    return t


def _launches(logs: Path):
    """(profile, start, end|None, ok, cap_s) from c2_segments.jsonl: an open line, then a closed line (rc)."""
    opened, out = {}, []
    for r in read_jsonl(logs / "c2_segments.jsonl"):
        try:
            s = float(r["start"])
        except (KeyError, TypeError, ValueError):
            continue
        m = re.search(r"--stop-after-min\s+(\d+(?:\.\d+)?)", str(r.get("args") or ""))
        cap_s = float(m.group(1)) * 60 if m else None
        key = (str(r.get("seg")), s)
        if r.get("open") is True:
            opened[key] = (str(r.get("profile")), cap_s)
            continue
        prof = str(r.get("profile") or (opened.get(key) or ("",))[0])
        opened.pop(key, None)
        try:
            e = float(r["end"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append((prof, s, e, r.get("rc") == 0, cap_s))
    out += [(p, s, None, False, c) for (_, s), (p, c) in opened.items()]
    return out


def unbilled_usd(profile: str, logs: Path | None = None, now: float | None = None) -> float:
    """Upper bound of this account's segment spend not yet in billing (billing lags up to about 75 min)."""
    now, tot = now or NOW(), 0.0
    for p, s, e, ok, cap_s in _launches(logs or LOGS):
        if p != profile:
            continue
        hi = e if e is not None else (s + cap_s if cap_s else now)
        lo = max(s, now - BILL_LAG_S)
        if hi > lo:
            tot += (hi - lo) / 3600 * USD_H
    return round(tot, 2)


def spent_training(logs: Path | None = None) -> tuple:
    """(usd, how): per account max(wall of closed rc=0 segments, billing delta since preflight), a launch that did not
    close with rc 0 counted to its cap but never above billing delta + the last 75 min (r1_check.spent_so_far)."""
    logs, now = logs or LOGS, NOW()
    base = (j(logs / "c2_baseline.json") or {}).get("profiles") or {}
    launches = _launches(logs)
    profs = sorted({p for p, *_ in launches} | set(base))
    if not profs:
        return None, "no c2_baseline.json and no c2_segments.jsonl: spend so far unknown"
    tot, notes = 0.0, []
    for p in profs:
        wall_ok = sum(e - s for q, s, e, ok, _ in launches if q == p and ok and e is not None) / 3600 * USD_H
        bill_usd, known = 0.0, False
        if p in base:
            try:
                bill_usd, known = float(BILL(p)["metered"]) - float(base[p]), True
            except Exception:  # noqa: BLE001
                pass
        unsure = [x for x in launches if x[0] == p and not x[3]]
        ub_wall = wall_ok
        lag = 0.0
        for q, s, e, ok, cap_s in unsure:
            hi = (min(now, s + cap_s) if cap_s else now)
            hi = max(hi, e if e is not None else s)
            ub_wall += max(0.0, hi - s) / 3600 * USD_H
            lag += max(0.0, hi - max(s, now - BILL_LAG_S)) / 3600 * USD_H
        ub_bill = bill_usd + lag if known else math.inf
        usd = max(wall_ok, bill_usd, min(ub_wall, ub_bill) if unsure else 0.0)
        tot += usd
        notes.append(f"{p}: wall {wall_ok:.2f}, billing delta {bill_usd:.2f}" + (f", {len(unsure)} unclosed" if unsure else ""))
    return round(tot, 2), "; ".join(notes)


def credit_minutes(profile: str, logs: Path | None = None) -> tuple:
    """Minutes of H100 the account's free credit can still pay (credit left - unbilled - reserve)."""
    b = BILL(profile)
    unb = unbilled_usd(profile, logs)
    afford = float(b["credit_left"]) - unb - CREDIT_RESERVE
    return max(0, math.floor(afford / USD_H * 60)), {"credit_left": b["credit_left"], "unbilled": unb,
                                                      "reserve": CREDIT_RESERVE}


# ----------------------------------------------------------------------------------------------- stop rules
def steps_of(meta: dict) -> list:
    return [r for r in (meta or {}).get("log", []) if isinstance(r, dict) and "step" in r]


def first100_verdict(meta, ref_sps: float | None = None) -> tuple:
    """A37 (k) first segment (steps 0-100, log_every 1): non-finite loss term -> ABORT; plus chain guards: <95 records,
    a loss above 3x the mean of steps 0-4, s/step (steps 10-99) above 2x the reference. Returns (record, verdict)."""
    if meta is None:
        return {"problems": ["no logs/relay_q35_4b_c2_stopped_at_100.json (segment 1 not done or crashed)"]}, "ABORT"
    recs = [r for r in steps_of(meta) if r["step"] < 100]
    p, ref = [], ref_sps or DEFAULT_REF_SPS
    bad = [r["step"] for r in recs for k in LOSS_KEYS if k in r and (r[k] is None or not math.isfinite(float(r[k])))]
    if bad:
        p.append(f"non-finite loss term at steps {sorted(set(bad))[:5]} (A37 k: abort at once)")
    fin = [float(r["loss"]) for r in recs if r.get("loss") is not None and math.isfinite(float(r["loss"]))]
    head = fin[:5]
    if head and max(fin) > 3 * (sum(head) / len(head)):
        p.append(f"loss {max(fin):.3f} > 3 x the mean of steps 0-4 ({sum(head) / len(head):.3f})")
    if len(recs) < 95:
        p.append(f"only {len(recs)} step records (log_every 1 expects 100)")
    t = {r["step"]: r.get("min") for r in recs}
    sps = None
    if t.get(10) is not None and t.get(99) is not None:
        sps = (t[99] - t[10]) * 60 / 89
        if sps > 2 * ref:
            p.append(f"s/step {sps:.2f} > 2 x reference {ref}")
    else:
        p.append("cannot time steps 10-99")
    n = recs[0].get("of") if recs else None
    rec = {"records": len(recs), "loss_first5_mean": round(sum(head) / len(head), 4) if head else None,
           "loss_max": max(fin) if fin else None, "s_per_step_10_99": round(sps, 3) if sps else None, "n_steps": n,
           "reference_s_per_step": ref, "problems": p}
    return rec, "ABORT" if p else "GO"


def rate_after_restarts(recs: list) -> float | None:
    """s/step over the records after the last restart of the trainer clock (`min` falls on a restart)."""
    run, last = [], None
    for r in recs:
        if r.get("min") is None:
            continue
        if last is not None and r["min"] < last:
            run = []
        run.append(r)
        last = r["min"]
    if len(run) >= 2 and run[-1]["step"] > run[0]["step"]:
        return (run[-1]["min"] - run[0]["min"]) * 60 / (run[-1]["step"] - run[0]["step"])
    return None


def rest_verdict(kind, head, n, at, sps, spent, other, t_max, credit_min, profile, credit_info=None):
    """A37 (k) / A42-D 2.3 on the rest of the run from step `at`. Pure: returns by raising Verdict (done)."""
    rest_usd = (n - at) * sps * USD_H / 3600
    projected = max(n * sps * USD_H / 3600 + ALLOW, spent + rest_usd + ALLOW)
    budget_min = math.floor((t_max - spent - ALLOW) / USD_H * 60)
    need_min = (n - at) * sps / 60
    k = max(1, math.ceil(need_min / (SEG_MAX_MIN - LOAD_SAVE_MIN)))
    seg_min, limit = min(budget_min, SEG_MAX_MIN), "budget"
    if credit_min < seg_min:
        seg_min, limit = credit_min, "credit"
    rec = {**head, "n_steps": n, "from_step": at, "s_per_step_used": round(sps, 3), "spent_training_usd": round(spent, 2),
           "spent_other_usd": round(other, 2), "projected_training_usd": round(projected, 1), "T_max": t_max,
           "cap_total": CAP_TOTAL, "budget_min": budget_min, "credit_min": credit_min, "stop_after_min": seg_min,
           "limit": limit, "need_min_for_rest": round(need_min, 1), "segments_left": k, "profile": profile,
           "credit": credit_info}
    if projected > t_max:
        done(kind, rec, f"STOP: projection ${projected:.1f} is above T_max ${t_max} (A37 k, A42-D 2.3): ask the owner")
    if other + projected > CAP_TOTAL:
        done(kind, rec, f"STOP: other spend ${other:.1f} + projection ${projected:.1f} is above the ${CAP_TOTAL:g} C2 cap")
    if budget_min < need_min + k * LOAD_SAVE_MIN:
        done(kind, rec, f"STOP: the rest needs {need_min + k * LOAD_SAVE_MIN:.0f} min but T_max leaves {budget_min} min; "
                        "ask the owner")
    if seg_min < MIN_SEG_MIN:
        if profile == PROFILES[0]:
            done(kind, rec, f"RELAY: free credit on {profile} leaves {credit_min} min; copy the run to {PROFILES[1]} "
                            "(c2_chain.sh copy) and resume there")
        done(kind, rec, f"STOP: free credit on {profile} leaves {credit_min} min and no free account is left; a card "
                        "needs the owner's named GO (A42-D 2.4)")
    return rec, seg_min


# ----------------------------------------------------------------------------------------------- commands
def stopped_files() -> dict:
    return {int(m.group(1)): q for q in (LEAN / "logs").glob(f"relay_{NAME}_stopped_at_*.json")
            if (m := re.fullmatch(rf"relay_{NAME}_stopped_at_(\d+)\.json", q.name))}


def cmd_proj(profile: str):
    meta = j(LEAN / f"logs/relay_{NAME}_stopped_at_300.json")
    if meta is None:
        done("proj", {"problems": ["no logs/relay_q35_4b_c2_stopped_at_300.json"]}, "STOP")
    recs = [r for r in steps_of(meta) if 100 <= r["step"] <= 300 and r.get("min") is not None]
    sps = rate_after_restarts(recs)
    n = (meta.get("steps") or (recs[-1].get("of") if recs else None))
    if sps is None:
        done("proj", {"problems": ["fewer than 2 timed records in steps 100-300"]}, "STOP")
    if not isinstance(n, int) or n <= 300:
        done("proj", {"problems": [f"n_steps unknown ({n!r})"]}, "STOP")
    spent, how = spent_training()
    if spent is None:
        done("proj", {"problems": [how]}, "STOP")
    t_max, other = tmax(), spend_other()
    cm, ci = credit_minutes(profile)
    rec, seg_min = rest_verdict("proj", {"s_per_step_100_300": round(sps, 3), "spent_how": how}, n, 300, sps, spent,
                                other, t_max, cm, profile, ci)
    (LOGS / "c2_stop_after_min.txt").write_text(f"{seg_min}\n{rec['limit']}\n")
    done("proj", rec, "GO")


def cmd_seg(profile: str):
    if (LEAN / f"logs/relay_{NAME}_final.json").exists():
        done("seg", {"problems": ["relay_q35_4b_c2_final.json exists: nothing left to run"]}, "STOP")
    pr = j(LOGS / "c2_check_proj.json") or {}
    if pr.get("decision") != "GO":
        done("seg", {"problems": ["no GO record of c2_check.py proj (steps 100-300)"]}, "STOP")
    prev = max([300] + [int((j(LOGS / f"c2_check_{k}.json") or {}).get("next_from") or 0) for k in ("seg", "resume")])
    got = stopped_files()
    at = max(got) if got else None
    if at is None or at <= prev:
        # a new segment on a fresh profile after a copy: the progress reference is the last known stop
        done("seg", {"problems": [f"no progress: latest stopped_at {at} <= {prev}"], "from_step": prev}, "STOP")
    meta = j(got[at]) or {}
    recs = [r for r in steps_of(meta) if r["step"] >= 300 and r.get("min") is not None]
    sps_post = rate_after_restarts(recs)
    sps = max(x for x in (float(pr["s_per_step_100_300"]), sps_post) if x is not None)
    n = meta.get("steps") or (recs[-1].get("of") if recs else None)
    if not isinstance(n, int) or n <= at:
        done("seg", {"problems": [f"n_steps unknown ({n!r}) or not above the stop {at}"]}, "STOP")
    spent, how = spent_training()
    if spent is None:
        done("seg", {"problems": [how]}, "STOP")
    cm, ci = credit_minutes(profile)
    head = {"s_per_step_after_300": round(sps_post, 3) if sps_post else None, "spent_how": how, "next_from": at}
    rec, seg_min = rest_verdict("seg", head, n, at, sps, spent, spend_other(), tmax(), cm, profile, ci)
    (LOGS / "c2_stop_after_min.txt").write_text(f"{seg_min}\n{rec['limit']}\n")
    done("seg", rec, "GO")


def cmd_resume(profile: str):
    """First segment on a new account after `c2_chain.sh copy` (or a crash relaunch): the same budget, from the
    latest stop in logs/relay_q35_4b_c2_stopped_at_*.json, without the 'progress since the last segment' rule."""
    if (LEAN / f"logs/relay_{NAME}_final.json").exists():
        done("resume", {"problems": ["relay_q35_4b_c2_final.json exists: nothing left to run"]}, "STOP")
    pr = j(LOGS / "c2_check_proj.json") or {}
    if pr.get("decision") != "GO":
        done("resume", {"problems": ["no GO record of c2_check.py proj (steps 100-300)"]}, "STOP")
    got = stopped_files()
    at = max(got) if got else None
    if at is None:
        done("resume", {"problems": ["no relay_q35_4b_c2_stopped_at_*.json"]}, "STOP")
    meta = j(got[at]) or {}
    recs = [r for r in steps_of(meta) if r["step"] >= 300 and r.get("min") is not None]
    sps = max(x for x in (float(pr["s_per_step_100_300"]), rate_after_restarts(recs)) if x is not None)
    n = meta.get("steps") or (recs[-1].get("of") if recs else None) or pr.get("n_steps")
    spent, how = spent_training()
    if spent is None or not isinstance(n, int) or n <= at:
        done("resume", {"problems": [how if spent is None else f"n_steps unknown ({n!r})"]}, "STOP")
    cm, ci = credit_minutes(profile)
    rec, seg_min = rest_verdict("resume", {"spent_how": how, "next_from": at}, n, at, sps, spent, spend_other(), tmax(),
                                cm, profile, ci)
    (LOGS / "c2_stop_after_min.txt").write_text(f"{seg_min}\n{rec['limit']}\n")
    done("resume", rec, "GO")


def ledger_line(text: str, profile: str) -> str:
    spent, _ = spent_training()
    other, t = spend_other(), tmax()
    try:
        cl = BILL(profile)["credit_left"]
    except Exception:  # noqa: BLE001
        cl = "?"
    tot = (spent or 0) + other
    return (f"| {text} | {time.strftime('%d %b %H:%M', time.gmtime(NOW()))} UTC, {profile} | training ${spent if spent is not None else '?'}"
            f" of T_max ${t}, other ${other:.2f}, C2 total ${tot:.2f} of ${CAP_TOTAL:g}, credit left ${cl} | free credit |")


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    if not a:
        print(__doc__)
        return 2

    def opt(name, default=None):
        return a[a.index(name) + 1] if name in a else default
    cmd, profile = a[0], opt("--profile", PROFILES[0])
    LOGS.mkdir(parents=True, exist_ok=True)
    if profile not in PROFILES:
        print(f"REFUSED: profile {profile!r} (C2 uses {PROFILES}; no card without the owner's named GO)")
        return 1
    try:
        if cmd == "other":     # the number for mix_c2.py --spend-to-date
            print(spend_other())
            return 0
        if cmd == "tmax":
            t = tmax(fix="--fix" in a)
            print(json.dumps({"t_max": t, "spent_other_usd": spend_other(), "fixed": (LOGS / "c2_tmax.json").exists()}))
            return 0
        if cmd == "first100":
            rec, v = first100_verdict(j(LEAN / f"logs/relay_{NAME}_stopped_at_100.json"), float(opt("--ref-sps", 0)) or None)
            done("first100", rec, v)
        if cmd == "proj":
            cmd_proj(profile)
        if cmd == "seg":
            cmd_seg(profile)
        if cmd == "resume":
            cmd_resume(profile)
        if cmd == "verify-copy":   # c2_chain.sh copy: the downloaded run folder, before it is put on the next account
            d = Path(a[1])
            man = j(d / "_ckpt/manifest.json")
            if not man or not (d / "_ckpt/state.pt").exists():
                done("verify-copy", {"dir": str(d)}, "STOP: no _ckpt/manifest.json or state.pt in the copy")
            import hashlib
            bad = [f for f, h in man["files"].items() if not (d / "_ckpt" / f).exists()
                   or hashlib.sha256((d / "_ckpt" / f).read_bytes()).hexdigest() != h]
            snaps = sorted(q.name for q in (d / "snaps").glob("s[0-9]*")) if (d / "snaps").exists() else []
            done("verify-copy", {"files": len(man["files"]), "bad": bad[:5], "snaps": snaps}, "STOP: bad files" if bad else "GO")
        if cmd == "cap":     # before seg1 / seg2: a fixed-length segment must fit the credit and T_max
            mins = float(opt("--min"))
            spent, how = spent_training()
            cm, ci = credit_minutes(profile)
            t_max = tmax()
            bm = math.floor((t_max - (spent or 0) - ALLOW) / USD_H * 60)
            rec = {"segment_min": mins, "credit_min": cm, "budget_min": bm, "T_max": t_max, "spent_how": how, "credit": ci}
            if spent is None:
                done("cap", rec, "STOP: spend so far unknown")
            if bm < mins:
                done("cap", rec, f"STOP: T_max leaves {bm} min, segment needs {mins:.0f}")
            if cm < mins:
                done("cap", rec, f"RELAY: free credit on {profile} leaves {cm} min, segment needs {mins:.0f}"
                     if profile == PROFILES[0] else f"STOP: free credit on {profile} leaves {cm} min")
            done("cap", rec, "GO")
        if cmd == "spend":
            usd = float(opt("--usd"))
            rec = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW())), "usd": usd, "what": opt("--what"),
                   "profile": profile}
            with (LOGS / "c2_spend.jsonl").open("a") as f:
                f.write(json.dumps(rec) + "\n")
            print(json.dumps({**rec, "spent_other_usd": spend_other(), "t_max_if_fixed_now": tmax_value(spend_other())}))
            return 0
        if cmd == "status":
            sp, how = spent_training()
            print(json.dumps({"t_max": tmax(), "spent_other": spend_other(), "spent_training": sp, "how": how,
                              "cap_total": CAP_TOTAL}))
            return 0
        if cmd == "ledger":
            line = ledger_line(a[1], profile)
            with (LOGS / "c2_ledger.md").open("a") as f:
                f.write(line + "\n")
            print(line)
            return 0
    except Verdict as v:
        LOGS.mkdir(parents=True, exist_ok=True)
        (LOGS / f"c2_check_{v.kind}.json").write_text(json.dumps({**v.rec, "decision": v.verdict}, indent=1))
        for k, val in v.rec.items():
            print(f"{k}: {json.dumps(val)[:160]}")
        print(v.verdict)
        return v.code
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
