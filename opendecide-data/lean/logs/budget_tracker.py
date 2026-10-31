"""Budget tracker: live 4B progress + October Modal credit across all accounts -> projected spend and reserve.
Run: ../.venv/bin/python logs/budget_tracker.py   (from lean/). Reads logs and `modal billing summary` (free calls)."""
import glob, json, os, re, subprocess, sys
from datetime import datetime, timezone
LEAN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODAL = os.path.join(LEAN, "..", ".venv", "bin", "modal")
ACCTS = ["jaypatil-duke", "arya-mahadik-ai", "aryamhd", "atmosphor", "mahadikarya2", "mahadikarya3", "mahadikarya44"]
CREDIT = 30.0          # free credit per account per month
RATE = float(os.environ.get("RATE", "4.09"))  # measured all-in $/h: seg-1 app ap-o9PZiyo = H100 $19.11 + CPU $0.38 + RAM $0.19 over 4.82 h
STEPS = 30457
RELAY_OVERHEAD_H = 0.10  # per segment: start, model load, resume checks
SEG_H = 5.5              # usable hours per $30 account at RATE (leaves margin)

def last_step():
    best = None
    for f in sorted(glob.glob(os.path.join(LEAN, "logs", "main4b_seg*.log"))):
        for l in open(f):
            if l.startswith('{"step"'):
                d = json.loads(l)
                if best is None or d["step"] > best["step"]:
                    best = d
    return best

def rate_s_per_step():
    pts = []
    for f in sorted(glob.glob(os.path.join(LEAN, "logs", "main4b_seg*.log"))):
        for l in open(f):
            if l.startswith('{"step"'):
                d = json.loads(l); pts.append((d["step"], d["min"]))
    pts.sort(); a, b = pts[max(0, len(pts) - 41)], pts[-1]   # last ~2000 steps
    return (b[1] - a[1]) * 60 / max(1, b[0] - a[0])

def oct_used(acct):
    try:
        out = subprocess.run([MODAL, "billing", "summary", "--json"], capture_output=True, text=True, timeout=60,
                             env={**os.environ, "MODAL_PROFILE": acct}).stdout
        d = json.loads(out); return float(d["metered_cost"]) - float(d["adjustments"].get("free_storage", 0) or 0) * -1 * 0
    except Exception as e:
        return None

now = datetime.now(timezone.utc)
st = last_step(); sps = rate_s_per_step()
left_steps = STEPS - st["step"]; h4b = left_steps * sps / 3600
segs_left = max(1, -(-h4b // SEG_H))
cost_4b = (h4b + segs_left * RELAY_OVERHEAD_H) * RATE
plan = [("4B remaining (measured speed)", cost_4b, "essential"),
        ("2B main (1.99 s/step x 30,457 incl ckpt, +4% yn2b rows)", 17.3 * 1.04 * RATE, "essential"),
        ("Direct-hosting speed test + OHS-3 inference", 7.0, "essential"),
        ("Relabel with the new 4B (1 view + 2nd view on choice rows)", 5.6 * RATE, "optional"),
        ("4B + yn2b top-up (~2,000 steps + reads)", 2.0 * RATE, "optional")]
used = {a: oct_used(a) for a in ACCTS}
have = sum(CREDIT - (u or 0) for u in used.values())
ess = sum(c for _, c, k in plan if k == "essential"); opt = sum(c for _, c, k in plan if k == "optional")
print(f"== budget tracker {now:%Y-%m-%d %H:%M} UTC | rate ${RATE:.2f}/h (RATE env to change)")
print(f"4B: step {st['step']:,}/{STEPS:,} ({100*st['step']/STEPS:.1f}%), {sps:.2f} s/step (last ~2000 steps), "
      f"{h4b:.1f} h left -> ETA {datetime.fromtimestamp(now.timestamp()+h4b*3600+segs_left*360, timezone.utc):%a %H:%M} UTC, ~{int(segs_left)} more segment(s)")
print("October credit used / left per account:")
for a, u in used.items():
    print(f"  {a:16s} used {('%.2f' % u) if u is not None else '  n/a'}  left {('%.2f' % (CREDIT-u)) if u is not None else 'n/a'}")
print(f"TOTAL October credit left: ${have:.2f}")
for n, c, k in plan:
    print(f"  {k:9s} ${c:6.1f}  {n}")
print(f"Essentials ${ess:.1f} -> reserve ${have-ess:.1f} | + both optional ${ess+opt:.1f} -> reserve ${have-ess-opt:.1f} "
      f"| + relabel only -> ${have-ess-plan[3][1]:.1f} | + top-up only -> ${have-ess-plan[4][1]:.1f}")
print("Extra $30 account needed?", "NO for essentials" if have - ess >= 20 else "YES (reserve < $20)",
      "| for both optional steps:", "NO" if have - ess - opt >= 10 else "YES")
