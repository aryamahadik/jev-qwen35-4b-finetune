"""SOLVER A for T63: the forward label functions over the SPEC (never the rendered text).

  NEAR   near.gold_label            policy function of the snapshot record (T8 first-match clause, then NM-T1..T7 rule)
  EX-A1  exists.gold_a1             membership in the spec's registry listing
  EX-A2  exists.gold_a2             membership in the spec's complete library export list
  EX-B   exists.gold_b              membership in the hashed stdlib export file (bound by sha; EX-B1 and EX-B2 alike; the L-0 image-record export only)
  LIC    lic.gold_label             lookup in the hashed Opus table
Solver B is a separate program (ROW_SCHEMA.md); it reads the RENDERED row only.
"""
from . import exists, lic, near


def make_gold_a(exports=None, table=None):
    def gold_a(rec):
        spec = rec["spec"]
        head = spec["head"]
        if head == "NEAR":
            return near.gold_label(spec)
        if head == "LIC":
            if table is None:
                raise ValueError("LIC rows need the hashed Opus licence table; none bound")
            if not (spec.get("table_sha") == rec["witness_inputs"].get("table_sha") == table.sha):
                raise ValueError("licence table sha differs from the bound table")
            return lic.gold_label(spec, table)
        sub = spec["sub"]
        if sub == "EX-A1":
            return exists.gold_a1(spec)
        if sub == "EX-A2":
            return exists.gold_a2(spec)
        if exports is None:
            raise ValueError("EX-B rows need the sha-bound L-0 image-record export; none bound")
        if not (spec["export_sha"] == rec["witness_inputs"].get("export_sha") == exports.sha):
            raise ValueError("export sha differs from the bound export file")
        return exists.gold_b(spec, exports)
    return gold_a
