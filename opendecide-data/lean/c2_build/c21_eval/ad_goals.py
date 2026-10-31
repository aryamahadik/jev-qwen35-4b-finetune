"""Run INSIDE the agentdojo==0.1.34 env (python -P -s ad_goals.py OUT.json): dump the GOAL text of every v1.2 injection task.
Used only for the label audit in h_agentdojo.py (a positive whose output lacks its injection goal)."""
import json
import sys

from agentdojo.task_suite import get_suite

goals = {s: {k: v.GOAL for k, v in get_suite("v1.2", s).injection_tasks.items()} for s in ["workspace", "travel", "banking", "slack"]}
json.dump(goals, open(sys.argv[1], "w"), indent=1, sort_keys=True)
