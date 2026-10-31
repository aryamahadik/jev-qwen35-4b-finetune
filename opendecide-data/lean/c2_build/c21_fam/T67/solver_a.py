"""SOLVER A for T67: the forward rule engine (engine.py) over the SPEC. gold_a(rec) returns the label of the head the record asks:
GATE -> ALLOW / ASK / BLOCK; REASON -> reason class; TIER -> soft / hard / na. Solver B (a separate program) labels from the rendered side."""
from . import engine


def make_gold_a(lock_table):
    def gold_a(rec):
        g = engine.gold(rec["spec"], lock_table)
        head = rec["meta"]["head"]
        return g["label"] if head == "GATE" else (g["reason"] if head == "REASON" else g["tier"])
    return gold_a
