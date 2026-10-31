# LANE LOCK (F4), 6 Oct 2026 01:20 UTC, orchestrator
OWNER: workflow "c-lanes-v3" (one lane per family; all older lanes, including the lean build, c-repair-rounds and
c-family-lanes, are STOPPED). Only c-lanes-v3 agents may change F4. Any other agent must stop and change nothing.
Earlier agents may have left background jobs or partial work. Check tmp/HANDOFF_*.md, tmp/repair/ notes, running
processes (pgrep -fl "F4") and logs before starting anything new.
