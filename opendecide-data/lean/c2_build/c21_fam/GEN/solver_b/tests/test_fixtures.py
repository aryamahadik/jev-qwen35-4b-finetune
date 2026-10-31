"""Hand-written fixtures for solver B (answers worked out by hand from the SCHEMA semantics, NOT taken from solver A).
Each fixture: (form, carrier, stem, options, expected option index)."""
import pytest

from b_main import solve_row

TXT = "TXT-PROSE"
FX = []


def fx(name, form, carrier, stem, options, want):
    FX.append(pytest.param(form, carrier, stem, options, want, id=name))


# ---- ARITH ----
fx("ar1_add_mul", "AR-F1", TXT,
   "Scene D01-0. aa equals 12 metres. bb equals 3 metres. Add aa and bb to get cc. Multiply cc by 4 to get dd. Find the final quantity dd.",
   ["48 metres", "60 metres", "75 metres", "15 metres"], 1)
fx("ar1_convert_pct_split", "AR-F1", TXT,
   "Scene D01-0. w is 2.5 kilograms. Convert w to gram; call it x. Take 20 percent of x; call it y. Split y in the ratio 1:4. z is the second share. "
   "Settle the final quantity z.",
   ["400 grams", "100 grams", "500 grams", "2000 grams"], 0)
fx("ar1_round_half_up", "AR-F1", TXT,
   "Scene D01-0. w stands at 2.5 litres. Round w to the nearest whole number (halves round up) to get r. Decide the final quantity r.",
   ["2 litres", "3 litres", "2.5 litres", "4 litres"], 1)
fx("ar1_count_noun", "AR-F1", TXT,
   "Scene D01-0. a equals 5 pidopos. b is 7 pidopos. c is the larger of a and b. Compute the final quantity c.",
   ["5 pidopos", "12 pidopos", "7 pidopos", "2 pidopos"], 2)
fx("ar2_below_threshold", "AR-F2", TXT,
   "Scene D01-0. a equals 7 litres. b equals 5 litres. Subtract b from a; the result is c. Work out whether c is at least 3 litres.",
   ["Yes", "No"], 1)
fx("ar2_unit_threshold_converted", "AR-F2", TXT,
   "Scene D01-0. a equals 2 hours. Compute whether a is more than 100 minutes.", ["Yes", "No"], 0)
fx("ar3_first_wrong_line", "AR-F3", TXT,
   "Scene D01-0. x equals 10 metres. y is x repeated 3 times. z equals y less x. w equals z and x added together. Worked solution: "
   "Line 1: y = x * 3 = 30 metres. Line 2: z = y - x = 30 metres. Line 3: w = z + x = 40 metres. "
   "A worked solution with 3 lines is shown. Find the first line that contains a mistake.",
   ["Line 1", "Line 2", "Line 3", "Line 4"], 1)
fx("ar3_wrong_expression_same_value", "AR-F3", TXT,
   "Scene D01-0. x equals 6 metres. y is x repeated 2 times. Worked solution: Line 1: y = x * 3 = 18 metres. "
   "A worked solution with 1 lines is shown. Find the first line that contains a mistake.",
   ["Line 1", "Line 2", "Line 3", "Line 4"], 0)
fx("ar3_follow_through_may_mix_units", "AR-F3", TXT,
   "Scene D01-0. x equals 2 kilometres. Convert x to metre; call it y. z equals 5 metres. Add y and z to get w. Worked solution: "
   "Line 1: y = x = 2 kilometres. Line 2: w = y + z = 7 metres. "
   "A worked solution with 2 lines is shown. Find the first line that contains a mistake.",
   ["Line 1", "Line 2", "Line 3", "Line 4"], 0)
# ---- LOGIC ----
fx("lg1_entailed", "LG-L1", TXT,
   "Scene D02-0. Use only the statements given. Aa is a pq. Anything that is a pq is a rs. Settle the status of the statement: Aa is a rs.",
   ["Contradicted", "Entailed", "Undetermined"], 1)
fx("lg1_undetermined", "LG-L1", TXT,
   "Scene D02-0. Use only the statements given. Aa is a pq. Anything that is a pq and is a tu is a rs. Settle the status of the statement: Aa is a rs.",
   ["Contradicted", "Entailed", "Undetermined"], 2)
fx("lg1_contradicted", "LG-L1", TXT,
   "Scene D02-0. Use only the statements given. Aa is a pq. None that is a pq is a rs. Settle the status of the statement: Aa is a rs.",
   ["Contradicted", "Entailed", "Undetermined"], 0)
fx("lg1_contrapositive", "LG-L1", TXT,   # needs the contrapositive: not rs, and pq -> rs, so not pq
   "Scene D02-0. Use only the statements given. Aa is not a rs. Anything that is a pq is a rs. Settle the status of the statement: Aa is a pq.",
   ["Contradicted", "Entailed", "Undetermined"], 0)
fx("lg1_relation_rule", "LG-L1", TXT,
   "Scene D02-0. Use only the statements given. Aa is a pq. Aa is rel to Bb. Whenever X is rel to Y and X is a pq, it follows that Y is a rs. "
   "Settle the status of the statement: Bb is a rs.",
   ["Contradicted", "Entailed", "Undetermined"], 1)
fx("lg2_must_be_true", "LG-L2", TXT,
   "Scene D02-0. Use only the statements given. Aa is a pq. Bb is not a pq. All that is a pq are a rs. Decide which statement must be true.",
   ["Aa is a rs", "Bb is a rs", "Aa is not a pq", "Bb is a pq"], 0)
fx("lg3_order", "LG-L3", TXT,
   "Scene D02-0. Arrange Ann, Bob and Cy in a row, one per position, positions counted from 1. Ann comes earlier than Bob. Cy takes position 1. "
   "Find which arrangement satisfies every constraint.",
   ["Ann, Bob, Cy", "Cy, Ann, Bob", "Cy, Bob, Ann", "Bob, Cy, Ann"], 1)
fx("lg4_follows", "LG-L4", TXT,
   "Scene D02-0. Use only the statements given. Aa is a pq. If something is a pq, it is a rs. Decide whether this conclusion follows: Aa is a rs.",
   ["No, it does not follow", "Yes, it follows"], 1)
fx("lg4_not_follows", "LG-L4", TXT,
   "Scene D02-0. Use only the statements given. Aa is a pq. If something is a rs, it is a pq. Decide whether this conclusion follows: Aa is a rs.",
   ["No, it does not follow", "Yes, it follows"], 0)
# ---- CAUSAL ----
fx("ca1_intervention", "CA-C1", TXT,
   "Scene D03-0. A system has the variables x, y and z. Each takes a whole value from 0 to 7. The outside input of x is 3. "
   "y = 2*x, limited to the range 0 to 7. z is the sum of x and y, mod 8. Establish z if y is set to 1 by intervention.",
   ["4", "1", "3", "5"], 0)
fx("ca2_counterfactual", "CA-C2", TXT,
   "Scene D03-0. A system has the variables x, y and z. Each takes a whole value from 0 to 7. "
   "y is (2*x, limited to the range 0 to 7) plus a hidden input of its own, mod 8. z is (the sum of x and y) plus a hidden input of its own, mod 8. "
   "x was seen to be 2. y was 5. z was 1. "
   "Settle what z would have been if x had been 3, everything else in the record being the same.",
   ["4", "2", "7", "0"], 0)
fx("ca3_confounder", "CA-C3", TXT,
   "Scene D03-0. A system has the variables p, q, r and s. Each takes a whole value from 0 to 7. r is a direct cause of p. "
   "r is a direct cause of q. s is a direct cause of q. Settle the role of r for the pair (p, q).",
   ["confounder", "mediator", "collider", "none"], 0)
fx("ca3_collider", "CA-C3", TXT,
   "Scene D03-0. A system has the variables p, q and r. Each takes a whole value from 0 to 7. There is a direct arrow from p to r. "
   "There is a direct arrow from q to r. Find the role of r for the pair (p, q).",
   ["confounder", "mediator", "collider", "none"], 2)
fx("ca4_adjustment", "CA-C4", TXT,
   "Scene D03-0. A system has the variables z, w, t and o. Each takes a whole value from 0 to 7. z is a direct cause of t. z is a direct cause of o. "
   "t is a direct cause of o. t is a direct cause of w. Every variable with no arrow into it is an independent random input; the question is about the stated arrows only. "
   "Compute which set is a valid adjustment set for the effect of t on o.",
   ["{}", "{z}", "{w}", "{z, w}"], 1)
fx("ca5_chain_blocked", "CA-C5", TXT,
   "Scene D03-0. A system has the variables a, b and c. Each takes a whole value from 0 to 7. a is a direct cause of b. b is a direct cause of c. "
   "Establish whether a and c must be independent given b.", ["Yes", "No"], 0)
fx("ca5_collider_opened", "CA-C5", TXT,
   "Scene D03-0. A system has the variables a, b and c. Each takes a whole value from 0 to 7. a is a direct cause of c. b is a direct cause of c. "
   "Establish whether a and b must be independent given c.", ["Yes", "No"], 1)
fx("ca5_collider_closed", "CA-C5", TXT,
   "Scene D03-0. A system has the variables a, b and c. Each takes a whole value from 0 to 7. a is a direct cause of c. b is a direct cause of c. "
   "Establish whether a and b must be independent given nothing.", ["Yes", "No"], 0)
# ---- TEMPORAL ----
CAL = "Use the proleptic Gregorian calendar and a 24-hour clock with no daylight-saving changes."
fx("tm1_leap_day", "TM-T1", TXT, "Scene D04-0. %s Find the date that is 2 days after 2024-02-28." % CAL,
   ["2024-03-01", "2024-02-29", "2024-03-02", "2024-03-03"], 0)
fx("tm1_business_days", "TM-T1", TXT,
   "Scene D04-0. %s Weekend days are Saturday and Sunday. There are no holidays. Find the date that is 1 business day after 2026-10-16." % CAL,
   ["2026-10-17", "2026-10-18", "2026-10-19", "2026-10-20"], 2)
fx("tm1_holiday_skipped", "TM-T1", TXT,
   "Scene D04-0. %s Weekend days are Saturday and Sunday. Holidays are 2026-10-19. Find the date that is 1 business day after 2026-10-16." % CAL,
   ["2026-10-17", "2026-10-19", "2026-10-20", "2026-10-21"], 2)
fx("tm1_clamp", "TM-T1", TXT,
   "Scene D04-0. %s Adding months keeps the day number, or uses the last day of the month if that day does not exist. "
   "Find the date that is 1 month after 2026-01-31." % CAL,
   ["2026-03-03", "2026-02-28", "2026-02-27", "2026-03-01"], 1)
fx("tm1_roll", "TM-T1", TXT,
   "Scene D04-0. %s A month step keeps the day of month, and any days beyond the month's end spill into the following month. "
   "Find the date that is 1 month after 2026-01-31." % CAL,
   ["2026-03-03", "2026-02-28", "2026-02-27", "2026-03-01"], 0)
fx("tm2_offsets", "TM-T2", TXT,
   "Scene D04-0. %s a happens at 2026-10-18 10:00 UTC+00:00. b happens at 2026-10-19 12:30 UTC+02:00. "
   "Find the time from a to b, written as days, hours and minutes." % CAL,
   ["1 day 0 hours 30 minutes", "2 days 0 hours 30 minutes", "1 day 1 hour 30 minutes", "0 days 24 hours 30 minutes"], 0)
fx("tm3_touching", "TM-T3", TXT,
   "Scene D04-0. %s An interval runs from its start up to but not including its end. p: 2026-01-01 00:00 UTC+00:00 until 2026-01-01 05:00 UTC+00:00. "
   "q: 2026-01-01 05:00 UTC+00:00 until 2026-01-01 08:00 UTC+00:00. Find how p and q relate." % CAL,
   ["disjoint with a gap", "touching end to start", "partial overlap", "one contains the other"], 1)
fx("tm3_contains", "TM-T3", TXT,
   "Scene D04-0. %s p: 2026-01-01 00:00 UTC+00:00 until 2026-01-01 05:00 UTC+00:00. q: 2026-01-01 01:00 UTC+00:00 until 2026-01-01 02:00 UTC+00:00. "
   "Find how p and q relate." % CAL,
   ["disjoint with a gap", "touching end to start", "partial overlap", "one contains the other"], 3)
fx("tm4_plan_on_the_boundary", "TM-T4", TXT,
   "Scene D04-0. %s There are enough workers for every task that is ready to run at once. Work begins at 2026-01-01 08:00 UTC+00:00 and everything must be finished by 2026-01-01 12:00 UTC+00:00. "
   "Task a takes 2 hours and can start at once. Task b takes 2 hours and starts only after a are done. Find whether the plan is feasible." % CAL,
   ["Yes", "No"], 0)
fx("tm4_plan_too_tight", "TM-T4", TXT,
   "Scene D04-0. %s There are enough workers for every task that is ready to run at once. Work begins at 2026-01-01 08:00 UTC+00:00 and everything must be finished by 2026-01-01 11:30 UTC+00:00. "
   "Task a takes 2 hours and can start at once. Task b takes 2 hours and starts only after a are done. Find whether the plan is feasible." % CAL,
   ["Yes", "No"], 1)
fx("tm4_overlap_half_open", "TM-T4", TXT,
   "Scene D04-0. %s Each interval includes its start and excludes its end. The booking p starts 2026-01-01 08:00 UTC+00:00 and ends 2026-01-01 09:00 UTC+00:00. "
   "The booking q starts 2026-01-01 09:00 UTC+00:00 and ends 2026-01-01 10:00 UTC+00:00. Establish whether p and q overlap." % CAL,
   ["Yes", "No"], 1)
# ---- TABLE (one table in five carriers) ----
ROWS = [("Aaa", "x", 10), ("Bbb", "y", 20), ("Ccc", "x", 30)]


def table_text(carrier):
    if carrier == "TBL-CSV":
        return "Table named tt:\nnm,grp,val\n" + "\n".join("%s,%s,%d" % r for r in ROWS)
    if carrier == "TBL-TSV":
        return "Table named tt:\nnm\tgrp\tval\n" + "\n".join("%s\t%s\t%d" % r for r in ROWS)
    if carrier == "TBL-PIPE":
        return "tt:\nnm | grp | val\n" + "\n".join("%s | %s | %d" % r for r in ROWS)
    if carrier == "TBL-KV":
        return "Table tt:\n" + "\n".join("row %d: nm=%s; grp=%s; val=%d" % (i + 1, r[0], r[1], r[2]) for i, r in enumerate(ROWS))
    return "tt:\n[" + ",".join('{"nm":"%s","grp":"%s","val":%d}' % r for r in ROWS) + "]"


for car in ("TBL-CSV", "TBL-TSV", "TBL-PIPE", "TBL-KV", "TBL-JSON"):
    fx("tb1_total_%s" % car, "TB-B1", car, "Scene D05-0.\nConsider the data below.\n%s\nSettle the total of val over the rows where grp is x." % table_text(car),
       ["40", "60", "30", "10"], 0)
fx("tb1_average_rounded", "TB-B1", "TBL-CSV",
   "Scene D05-0.\nTable data follows.\nTable named tt:\nnm,grp,val\nAaa,x,10\nBbb,x,11\nCcc,x,11\n"
   "Give the result to 2 decimal places, rounding half up.\nFind the average of val over the rows where grp is x.",
   ["10.67", "10.66", "11", "10"], 0)
fx("tb1_date_filter", "TB-B1", "TBL-CSV",
   "Scene D05-0.\nData:\nTable named tt:\nnm,when,val\nAaa,2026-01-01,1\nBbb,2026-02-01,2\nCcc,2026-03-01,4\n"
   "Compute the total of val over the rows where when is on or before 2026-02-01.",
   ["7", "3", "1", "6"], 1)
fx("tb2_group_rank", "TB-B2", "TBL-CSV",
   "Scene D05-0.\n%s\nFind which entry ranks first by highest total val per grp." % table_text("TBL-CSV"), ["x", "y", "Aaa", "Bbb"], 0)
fx("tb2_entry_rank_lowest", "TB-B2", "TBL-CSV",
   "Scene D05-0.\n%s\nFind which entry ranks first by lowest val." % table_text("TBL-CSV"), ["x", "y", "Aaa", "Bbb"], 2)
fx("tb3_join", "TB-B3", "TBL-CSV",
   "Scene D05-0.\nTable data follows.\nTable named p:\nnm,cat,amt\nAaa,u,5\nBbb,v,7\nTable named q:\nnm,score\nAaa,1.50\nAaa,2.50\nBbb,4.00\n"
   "Join the two tables on nm = nm.\n"
   "Establish the total of score over the joined rows where cat is u.", ["4", "5", "7", "2"], 0)
fx("tb3_join_count", "TB-B3", "TBL-CSV",
   "Scene D05-0.\nTable data follows.\nTable named p:\nnm,cat,amt\nAaa,u,5\nBbb,v,7\nTable named q:\nnm,score\nAaa,1.50\nAaa,2.50\nBbb,4.00\n"
   "Join the two tables on nm = nm.\n"
   "Establish the number of rows over the joined rows where cat is u.", ["1", "2", "3", "0"], 1)
fx("tb4_true", "TB-B4", "TBL-CSV",
   "Scene D05-0.\n%s\nDecide whether this claim is correct: the total of val over rows where grp is x is 40." % table_text("TBL-CSV"), ["True", "False"], 0)
fx("tb4_false_count", "TB-B4", "TBL-CSV",
   "Scene D05-0.\n%s\nDecide whether this claim is correct: exactly 3 rows satisfy: grp is x." % table_text("TBL-CSV"), ["True", "False"], 1)
fx("tb4_extreme_row", "TB-B4", "TBL-CSV",
   "Scene D05-0.\n%s\nDecide whether this claim is correct: the row with the highest val among rows where grp is x is Ccc." % table_text("TBL-CSV"), ["True", "False"], 0)


@pytest.mark.parametrize("form,carrier,stem,options,want", FX)
def test_hand_answers(form, carrier, stem, options, want):
    k = len(options)
    out = solve_row({"form": form, "k": k, "carrier": carrier, "stem": stem, "options": options})
    assert out["status"] == "ok", out
    assert out["answer_index"] == want, out


# ---- failure paths: a wording B does not know is a ParseFail, an ill-posed world state is a Reject; neither guesses ----
def test_unknown_wording_is_parse_fail_not_a_guess():
    out = solve_row({"form": "AR-F1", "k": 4, "carrier": TXT, "stem": "Scene D01-0. aa equals 12 metres. Wibble aa into bb. Find the final quantity bb.",
                     "options": ["1 metres", "2 metres", "3 metres", "4 metres"]})
    assert out["status"] == "parse_fail"


def test_non_terminating_division_is_rejected():
    out = solve_row({"form": "AR-F1", "k": 4, "carrier": TXT, "stem": "Scene D01-0. aa equals 10 metres. Divide aa by 3 to get bb. Find the final quantity bb.",
                     "options": ["3 metres", "4 metres", "3.33 metres", "5 metres"]})
    assert out["status"] == "reject" and out["code"] == "non_terminating"


def test_negative_intermediate_is_rejected():
    out = solve_row({"form": "AR-F1", "k": 4, "carrier": TXT,
                     "stem": "Scene D01-0. aa equals 1 metres. bb equals 5 metres. Subtract bb from aa; the result is cc. Find the final quantity cc.",
                     "options": ["4 metres", "-4 metres", "6 metres", "5 metres"]})
    assert out["status"] == "reject" and out["code"] == "negative_intermediate"


def test_inconsistent_knowledge_base_is_rejected():
    out = solve_row({"form": "LG-L1", "k": 3, "carrier": TXT,
                     "stem": "Scene D02-0. Use only the statements given. Aa is a pq. Aa is not a pq. Settle the status of the statement: Aa is a rs.",
                     "options": ["Contradicted", "Entailed", "Undetermined"]})
    assert out["status"] == "reject" and out["code"] == "inconsistent_knowledge_base"


def test_tie_for_first_place_is_rejected():
    out = solve_row({"form": "TB-B2", "k": 4, "carrier": "TBL-CSV",
                     "stem": "Scene D05-0.\nTable named tt:\nnm,grp,val\nAaa,x,10\nBbb,y,10\nFind which entry ranks first by highest total val per grp.",
                     "options": ["x", "y", "Aaa", "Bbb"]})
    assert out["status"] == "reject" and out["code"] == "tie_for_first_place"


def test_two_options_equal_in_value_is_not_picked_silently():
    out = solve_row({"form": "AR-F1", "k": 4, "carrier": TXT, "stem": "Scene D01-0. aa equals 12 metres. Find the final quantity aa.",
                     "options": ["12 metres", "12.0 metres", "13 metres", "14 metres"]})
    assert out["status"] == "reject" and out["code"] == "several_options_match_answer"


def test_cyclic_definition_is_parse_fail():
    out = solve_row({"form": "AR-F1", "k": 4, "carrier": TXT,
                     "stem": "Scene D01-0. aa equals 12 metres. Add bb and aa to get cc. Add cc and aa to get bb. Find the final quantity cc.",
                     "options": ["1 metres", "2 metres", "3 metres", "4 metres"]})
    assert out["status"] == "parse_fail"



def test_plan_stem_without_the_parallel_workers_sentence_is_refused():
    stem = ("Scene D04-0. %s Work begins at 2026-01-01 08:00 UTC+00:00 and everything must be finished by 2026-01-01 12:00 UTC+00:00. "
            "Task a takes 2 hours and can start at once. Task b takes 2 hours and starts only after a are done. Find whether the plan is feasible." % CAL)
    out = solve_row({"form": "TM-T4", "k": 2, "carrier": TXT, "stem": stem, "options": ["Yes", "No"]})
    assert out["status"] == "parse_fail" and out["code"] == "parallel_workers_not_stated"


def test_a_table_header_that_is_not_a_plain_identifier_is_refused_before_any_sql():
    stem = "Scene D05-0.\nTable named tt:\nnm,gr\"p; DROP TABLE t0;--,val\nAaa,x,10\nBbb,y,20\nFind the total of val over the rows where nm is Aaa."
    out = solve_row({"form": "TB-B1", "k": 4, "carrier": "TBL-CSV", "stem": stem, "options": ["10", "20", "30", "0"]})
    assert out["status"] == "parse_fail"
