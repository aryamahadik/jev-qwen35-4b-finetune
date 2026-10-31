# OWNER GOALS for C2.1 (NOT research; owner, 18 Oct 2026 ~01:15 UTC; binding targets for the planner)

Owner, paraphrased closely: C2 is the baseline. C2.1 must carry EVERY optimisation in one model and be the best we can
ever do. General accuracy: at most 2-3 points behind Jev 1.14 (4 is the maximum acceptable). On everything else C2.1
must beat Jev: agent / coding-agent tasks, latency, cost, security (injection, command safety, secrets, attack
robustness) and calibration. The owner will review the plan and approve the owner-reserved levers.

The planner MUST: (1) list every lever that moves general accuracy toward a <= 3-point gap with an honest estimated
gain range and evidence (from research_v3 files), including levers that need the owner's words (e.g. the A61 (b)
split-aware deny-list for public TRAIN splits, a selective-thinking tier, answer-changing serving dials such as
FP8 with a margin gate or one read per choice question) — mark those OWNER-RESERVED with a recommended default;
(2) give the projected gap with and without the owner-reserved levers; (3) give per-dimension targets vs Jev
(agent, latency, cost, security, calibration) with the measurement that proves each; (4) never propose breaking an
adopted rule silently (no LLM-generated datasets, no bigger teachers, no eval-set training, no sealed leakage).
