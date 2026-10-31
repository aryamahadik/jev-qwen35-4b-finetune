"""Rebuild the scoped input files from C2_1_PLAN_v3.md + C2_1_BUILD_ORDER.md (orchestrator tool; run from lean/).
Sealed side gets plan sections 3, 4, the section 10 OWNER-RESERVED table, 11 and the L-S block (ohs5_sealed/inputs/DECISION_SPEC.md);
training side gets sections 1, 2, 5, 6, 7, 8 + section 3's PRE-REGISTERED RULES block (training_inputs/PLAN_TRAINING_SIDE.md) and
one LANE_<X>.md per lane (build-order header + lane block). Usage: ../.venv/bin/python -B c2_build/zed_orch/c21/make_scoped_inputs.py [--no-sealed]"""
import re, os, sys, hashlib
P = "c2_build/zed_orch/c21/C2_1_PLAN_v3.md"; B = "c2_build/zed_orch/c21/C2_1_BUILD_ORDER.md"
plan = open(P).read().split("\n"); bo = open(B).read().split("\n")
heads = [(i, int(m.group(1))) for i, l in enumerate(plan) for m in [re.match(r"^## (\d+)\. ", l)] if m]
def sec(n):
    for k, (i, s) in enumerate(heads):
        if s == n:
            j = heads[k + 1][0] if k + 1 < len(heads) else len(plan)
            return "\n".join(plan[i:j]).rstrip("\n").rstrip("-").rstrip()
    raise SystemExit(f"no section {n}")
s3, s10 = sec(3), sec(10)
pr = s3[s3.index("PRE-REGISTERED RULES (one look"):]
own = s10[s10.index("OWNER-RESERVED (rules reserve"):]
hdr = "\n".join(plan[0:9])
bh = [i for i, l in enumerate(bo) if l.startswith("## ")]
def blk(tag):
    """The lane's '## <tag> ' block plus every '### <tag> ' subsection (v3.2 lane additions), each up to the next heading of
    the same or a higher level."""
    out = []
    for i, l in enumerate(bo):
        lvl = 2 if l.startswith("## " + tag + " ") else 3 if l.startswith("### " + tag + " ") else 0
        if not lvl:
            continue
        j = i + 1
        while j < len(bo) and not any(bo[j].startswith("#" * h + " ") for h in range(1, lvl + 1)):
            j += 1
        out.append("\n".join(bo[i:j]).rstrip().rstrip("-").rstrip())
    return "\n\n".join(out)
glob_hdr = "\n".join(bo[0:56])
os.makedirs("c2_build/zed_orch/c21/training_inputs", exist_ok=True)
def w(p, t):
    open(p, "w").write(t + "\n"); print(p, len(t), hashlib.sha256((t + "\n").encode()).hexdigest()[:16])
if "--no-sealed" not in sys.argv:
    os.makedirs("ohs5_sealed/inputs", exist_ok=True)
    w("ohs5_sealed/inputs/DECISION_SPEC.md", "# OHS-5 decision-level spec for the SEALED side (from C2_1_PLAN_v3.md sections 3, 4, the section 10 OWNER-RESERVED table, 11)\n\n" + hdr + "\n\n" + s3 + "\n\n" + sec(4) + "\n\n## 10 (OWNER-RESERVED table only)\n" + own + "\n\n" + sec(11) + "\n\n" + blk("L-S"))
w("c2_build/zed_orch/c21/training_inputs/PLAN_TRAINING_SIDE.md", "# C2.1 plan, TRAINING-SIDE scope (sections 1, 2, 5, 6, 7, 8 + section 3's PRE-REGISTERED RULES block)\n\n" + hdr + "\n\n" + sec(1) + "\n\n" + sec(2) + "\n\n## 3 (PRE-REGISTERED RULES block only)\n" + pr + "\n\n" + sec(5) + "\n\n" + sec(6) + "\n\n" + sec(7) + "\n\n" + sec(8) + (("\n\n" + sec(16)) if any(n == 16 for _, n in heads) else ""))
for tag in ("L-0", "L-A", "L-I", "L-T", "L-C", "L-G", "L-R", "L-K", "L-P"):
    b = blk(tag)
    if b:
        w(f"c2_build/zed_orch/c21/training_inputs/LANE_{tag}.md", glob_hdr + "\n\n" + b)
w("c2_build/zed_orch/c21/training_inputs/LANE_L-E.md", "# Eval-harness lane scope: plan section 4 + the L-E block\n\n" + hdr + "\n\n" + sec(4) + "\n\n" + glob_hdr + "\n\n" + blk("L-E"))
w("c2_build/zed_orch/c21/training_inputs/LANE_L-D.md", "# Deployment lane scope: plan sections 6, 8 + the L-D block\n\n" + hdr + "\n\n" + sec(6) + "\n\n" + sec(8) + "\n\n" + glob_hdr + "\n\n" + blk("L-D"))
