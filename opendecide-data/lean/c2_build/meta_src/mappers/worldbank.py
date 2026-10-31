"""worldbank.py: metadata mapper for md_worldbank (World Bank Projects and Operations; CC BY 4.0; development finance).

Upstream fields used as targets: status, lendinginstr, totalcommamt, ibrd / ida commitments, boardapprovaldate,
closingdate, regionname, countryshortname, projectfinancialtype, envassesmentcategorycode, supplementprojectflg, approvalfy,
major sector / theme lists, project_name (word presence only). Abstracts are never used.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from _common_a import (CHOICE_Q, COUNT_NEG, COUNT_POS, YEAR_NEG, YEAR_POS, Task, bool_task, bucket_task, concept_task, eq_task, ge_task, yn_card)

NAME = "worldbank"
DOMAIN = "development_finance"
LICENCE = "CC BY 4.0 (World Bank Projects and Operations metadata; attribution to the World Bank Group)"
HEADERS = ["Development project record", "Project register entry", "Lending operation record from a development-bank register", "Project and operations register row"]
RAW = Path(__file__).resolve().parent.parent / "raw_a" / "worldbank" / "projects.json"
REF_YEAR = 2026
GROUPS = {"board_approval_date": "date", "approval_fy": "date", "ibrd_usd_m": "amt", "ida_usd_m": "amt", "total_usd_m": "amt", "closing_date": "close", "reference_year": "date"}
USD_POS = ["Is the total commitment {n} million USD or more?", "Does the project commit at least {n} million USD in total?", "Is the total commitment at least {n} million USD?"]
USD_NEG = ["Is the total commitment below {n} million USD?", "Does the project commit less than {n} million USD in total?"]


def num(s):
    try:
        return int(str(s).replace(",", ""))
    except (ValueError, TypeError):
        return None


def load():
    out = []
    for x in json.loads(RAW.read_text()):
        tot = num(x.get("totalcommamt"))
        bd = (x.get("boardapprovaldate") or "")[:10]
        cd = None
        if x.get("closingdate"):
            try:
                cd = datetime.strptime(x["closingdate"].split(" ")[0], "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                cd = None
        fy = x.get("approvalfy")
        fy_ok = bool(bd and fy and str(fy).isdigit() and (int(bd[:4]) + (1 if int(bd[5:7]) >= 7 else 0)) == int(fy))
        out.append({"id": x["id"], "name": x.get("project_name") or "", "status": x.get("status"), "region": x.get("regionname"),
                    "country": x.get("countryshortname"), "instr": x.get("lendinginstr"), "tot": tot, "ibrd": num(x.get("ibrdcommamt")),
                    "ida": num(x.get("idacommamt")), "approval": bd or None, "closing": cd, "fy": int(fy) if fy_ok else None,
                    "env": x.get("envassesmentcategorycode"), "supp": x.get("supplementprojectflg"),
                    "fin": [t for t in (x.get("projectfinancialtype") or []) if t in ("IBRD", "IDA", "Grants", "Other")],
                    "n_sec": len({s["name"] for s in (x.get("mjsector_namecode") or []) if s.get("name")}),
                    "n_theme": len({s["name"] for s in (x.get("mjtheme_namecode") or []) if s.get("name")})})
    return [r for r in out if r["tot"] is not None and r["tot"] > 0 and r["name"]]


def rid_of(r):
    return r["id"]


def group_of(k):
    return GROUPS.get(k, k)


def yr(r, k):
    return int(r[k][:4]) if r.get(k) else None


def fields_of(r):
    fin = "+".join(r["fin"]) if r["fin"] else None
    return {
        "project_id": ("Project ID", r["id"]), "project_name": ("Project name", r["name"]), "status": ("Status", r["status"]),
        "region": ("Region", r["region"]), "country": ("Country", r["country"]), "instrument": ("Lending instrument", r["instr"]),
        "total_usd_m": ("Total commitment (USD million)", f"{r['tot'] / 1e6:.2f}"),
        "ibrd_usd_m": ("IBRD commitment (USD million)", f"{r['ibrd'] / 1e6:.2f}" if r["ibrd"] is not None else None),
        "ida_usd_m": ("IDA commitment (USD million)", f"{r['ida'] / 1e6:.2f}" if r["ida"] is not None else None),
        "board_approval_date": ("Board approval date", r["approval"]), "closing_date": ("Closing date", r["closing"]),
        "approval_fy": ("Approval fiscal year", str(r["fy"]) if r["fy"] else None), "reference_year": ("Reference year", str(REF_YEAR)),
        "env_category": ("Environmental category", r["env"]), "supplemental": ("Supplemental flag", r["supp"]), "finance_type": ("Financing type", fin),
        "major_sectors": ("Major sectors listed", str(r["n_sec"])), "themes": ("Major themes listed", str(r["n_theme"])),
    }


def words(r, w):
    return re.search(r"\b" + re.escape(w) + r"\b", r["name"], re.I) is not None


def gap(r):
    return yr(r, "closing") - yr(r, "approval")


def tasks():
    T = []
    add = T.append
    for thr in (10, 25, 50, 100, 200, 500):
        add(ge_task(f"wb_commit_ge_{thr}", ["total_usd_m"], lambda r: r["tot"] / 1e6, thr, pos=USD_POS, neg=USD_NEG, why=f"totalcommamt >= {thr} million"))
    add(bool_task("wb_ida_gt_ibrd", ["ibrd_usd_m", "ida_usd_m"], lambda r: r["ida"] > r["ibrd"], "", ["Is the IDA commitment larger than the IBRD commitment?", "Does the project have more IDA than IBRD money?"],
                  ["Is the IDA commitment smaller than the IBRD commitment?", "Does the project have less IDA than IBRD money?"],
                  elig=lambda r: r["ibrd"] is not None and r["ida"] is not None and r["ida"] != r["ibrd"], why="idacommamt > ibrdcommamt"))
    add(bool_task("wb_ibrd_positive", ["ibrd_usd_m"], lambda r: r["ibrd"] > 0, "", ["Is the IBRD commitment above zero?", "Does the project carry any IBRD money?"],
                  ["Is it true that the IBRD commitment is not above zero?", "Is it true that the project carries no IBRD money?"], elig=lambda r: r["ibrd"] is not None, why="ibrdcommamt > 0"))
    for y in (2000, 2005, 2010, 2015, 2020):
        add(ge_task(f"wb_approved_ge_{y}", ["board_approval_date"], lambda r: yr(r, "approval"), y, pos=YEAR_POS, neg=YEAR_NEG, elig=lambda r: bool(r["approval"]),
                    fmt={"verb": "approved by the board", "what": "board approval"}, why=f"approval year >= {y}"))
    for v in ("Active", "Closed", "Dropped", "Pipeline"):
        add(eq_task(f"wb_status_is_{v.lower()}", ["status"], lambda r: r["status"], v, "project status", why=f"status == {v}"))
    for v in ("East Asia and Pacific", "Europe and Central Asia", "Latin America and Caribbean", "Middle East and North Africa", "South Asia", "Eastern and Southern Africa"):
        add(eq_task(f"wb_region_is_{re.sub('[^a-z]+', '_', v.lower())}", ["region"], lambda r: r["region"], v, "region", why=f"regionname == {v}"))
    for v in ("Investment Project Financing", "Development Policy Lending", "Specific Investment Loan", "Technical Assistance Loan", "Program-for-Results Financing"):
        add(eq_task(f"wb_instr_is_{re.sub('[^a-z]+', '_', v.lower())}", ["instrument"], lambda r: r["instr"], v, "lending instrument", why=f"lendinginstr == {v}"))
    for n in (3, 5, 7):
        add(Task(f"wb_span_ge_{n}", "yn", ["board_approval_date", "closing_date"], pred=lambda r, n=n: gap(r) >= n, elig=lambda r: bool(r["approval"] and r["closing"]),
                 pos=["Is the closing year at least {n} years after the board approval year?", "Does the closing date fall {n} or more calendar years after the approval date?"],
                 neg=["Is the closing year fewer than {n} years after the board approval year?", "Does the closing date fall fewer than {n} calendar years after the approval date?"],
                 fmt={"n": n}, why=f"closing year - approval year >= {n}"))
    for w in ("Water", "Health", "Education", "Energy", "Climate"):
        add(Task(f"wb_name_has_{w.lower()}", "yn", ["project_name"], pred=lambda r, w=w: words(r, w),
                 pos=["Does the project name contain the word '{v}'?", "Is the word '{v}' part of the project name?"],
                 neg=["Is it true that the project name does not contain the word '{v}'?", "Is it true that the word '{v}' is not part of the project name?"], fmt={"v": w},
                 why=f"word {w} in project_name"))
    add(eq_task("wb_supplemental", ["supplemental"], lambda r: r["supp"], "Y", "supplemental flag", elig=lambda r: r["supp"] in ("Y", "N"), why="supplementprojectflg == Y"))
    for v in ("IDA", "IBRD"):
        add(Task(f"wb_fin_has_{v.lower()}", "yn", ["finance_type"], pred=lambda r, v=v: v in r["fin"], elig=lambda r: bool(r["fin"]),
                 pos=["Does the financing type list include {v}?", "Is {v} one of the financing types?"],
                 neg=["Is it true that the financing type list does not include {v}?", "Is it true that {v} is not one of the financing types?"], fmt={"v": v}, why=f"{v} in projectfinancialtype"))
    add(bool_task("wb_second_half", ["board_approval_date"], lambda r: int(r["approval"][5:7]) >= 7, "", ["Was the board approval in July to December?", "Is the approval month between July and December?"],
                  ["Is it true that the board approval was not in July to December?", "Is it true that the approval month is not between July and December?"], elig=lambda r: bool(r["approval"]), why="approval month >= 7"))
    add(eq_task("wb_country_is_india", ["country"], lambda r: r["country"], "India", "country", why="countryshortname == India"))
    add(ge_task("wb_sectors_ge_2", ["major_sectors"], lambda r: r["n_sec"], 2, elig=lambda r: r["n_sec"] > 0, fmt={"things": "major sectors", "thing": "major-sector"}, why="distinct mjsector >= 2"))
    add(ge_task("wb_themes_ge_2", ["themes"], lambda r: r["n_theme"], 2, elig=lambda r: r["n_theme"] > 0, fmt={"things": "major themes", "thing": "major-theme"}, why="distinct mjtheme >= 2"))
    # carded concepts
    add(concept_task("wb_c_large", ["total_usd_m"], lambda r: r["tot"] >= 100e6, "a large operation", yn_card("the total commitment is 100 million USD or more", "the total commitment is below 100 million USD"), why=">= 100m"))
    add(concept_task("wb_c_mega", ["total_usd_m"], lambda r: r["tot"] >= 300e6, "a mega operation", yn_card("the total commitment is 300 million USD or more", "the total commitment is below 300 million USD"), why=">= 300m"))
    add(concept_task("wb_c_long_running", ["board_approval_date", "closing_date"], lambda r: gap(r) >= 6, "long-running", yn_card("the closing year is 6 or more calendar years after the approval year", "the gap between the years is under 6"),
                     elig=lambda r: bool(r["approval"] and r["closing"]), why="gap >= 6"))
    add(concept_task("wb_c_open", ["status"], lambda r: r["status"] in ("Active", "Pipeline"), "an open project", yn_card("the status is Active or Pipeline", "the status is Closed or Dropped"), elig=lambda r: r["status"] in ("Active", "Pipeline", "Closed", "Dropped"), why="status in open"))
    add(concept_task("wb_c_needs_assessment", ["env_category"], lambda r: r["env"] in ("A", "B"), "an operation needing an environmental assessment", yn_card("the environmental category is A or B", "the category is C"),
                     elig=lambda r: r["env"] in ("A", "B", "C"), why="env in A,B"))
    add(concept_task("wb_c_recent", ["board_approval_date", "reference_year"], lambda r: REF_YEAR - yr(r, "approval") <= 5, "recently approved",
                     yn_card("the reference year minus the approval year is 5 or less", "the reference year minus the approval year is more than 5"), elig=lambda r: bool(r["approval"]), why=f"{REF_YEAR} - approval year <= 5"))
    add(concept_task("wb_c_fy_end", ["board_approval_date"], lambda r: r["approval"][5:7] == "06", "approved in the last month of the fiscal year", yn_card("the approval month is June", "the approval month is any other month"),
                     elig=lambda r: bool(r["approval"]), why="approval month == 06"))
    add(concept_task("wb_c_blend", ["ibrd_usd_m", "ida_usd_m"], lambda r: r["ibrd"] > 0 and r["ida"] > 0, "a blend operation", yn_card("both the IBRD and the IDA commitments are above zero", "one of them is zero"),
                     elig=lambda r: r["ibrd"] is not None and r["ida"] is not None, why="ibrd > 0 and ida > 0"))
    # choice heads
    add(bucket_task("wb_ch_amount_class", ["total_usd_m"], lambda r: "small" if r["tot"] < 25e6 else "medium" if r["tot"] < 100e6 else "large" if r["tot"] < 500e6 else "very large",
                    ["small", "medium", "large", "very large"], "size class", defs=[("small", "Pick this when the total commitment is under 25 million USD."), ("medium", "Pick this for 25 million up to under 100 million."),
                    ("large", "Pick this for 100 million up to under 500 million."), ("very large", "Pick this for 500 million or more.")], why="tot bins"))
    add(bucket_task("wb_ch_period", ["board_approval_date"], lambda r: "before 2000" if yr(r, "approval") < 2000 else "2000-2009" if yr(r, "approval") < 2010 else "2010-2019" if yr(r, "approval") < 2020 else "2020 or later",
                    ["before 2000", "2000-2009", "2010-2019", "2020 or later"], "approval period", elig=lambda r: bool(r["approval"]), why="approval year bins"))
    add(bucket_task("wb_ch_fiscal_year", ["board_approval_date"], lambda r: str(r["fy"]), [str(y) for y in (2014, 2015, 2016, 2017)], "fiscal year of the board approval", ordered=False, k=4,
                    elig=lambda r: r["fy"] in (2014, 2015, 2016, 2017), card="The World Bank fiscal year runs from 1 July to 30 June and is named after the calendar year in which it ends. Approval on or after 1 July of year Y falls in fiscal year Y+1; approval before 1 July falls in fiscal year Y.",
                    why="approval date -> FY (rows kept only where the upstream approvalfy equals the rule)"))
    grp = {"Active": "open", "Pipeline": "open", "Closed": "closed", "Dropped": "dropped"}
    add(bucket_task("wb_ch_status_group", ["status"], lambda r: grp[r["status"]], ["open", "closed", "dropped"], "status group", ordered=False, k=3, elig=lambda r: r["status"] in grp,
                    defs=[("open", "Pick this when the status is Active or Pipeline."), ("closed", "Pick this when the status is Closed."), ("dropped", "Pick this when the status is Dropped.")], why="status -> group"))
    rg = {"Eastern and Southern Africa": "Africa", "Western and Central Africa": "Africa", "East Asia and Pacific": "Asia-Pacific", "South Asia": "Asia-Pacific",
          "Europe and Central Asia": "Europe and Central Asia", "Latin America and Caribbean": "Americas", "Middle East and North Africa": "Middle East and North Africa"}
    add(bucket_task("wb_ch_region_group", ["region"], lambda r: rg[r["region"]], ["Africa", "Asia-Pacific", "Europe and Central Asia", "Americas", "Middle East and North Africa"], "region group", ordered=False, k=4,
                    elig=lambda r: r["region"] in rg, defs=[("Africa", "Pick this for Eastern and Southern Africa or Western and Central Africa."), ("Asia-Pacific", "Pick this for East Asia and Pacific or South Asia."),
                    ("Europe and Central Asia", "Pick this for Europe and Central Asia."), ("Americas", "Pick this for Latin America and Caribbean."), ("Middle East and North Africa", "Pick this for Middle East and North Africa.")], why="region -> group"))
    fam = {"Investment Project Financing": "investment", "Specific Investment Loan": "investment", "Sector Investment and Maintenance Loan": "investment", "Development Policy Lending": "policy-based",
           "Structural Adjustment Loan": "policy-based", "Technical Assistance Loan": "technical or other", "Program-for-Results Financing": "results-based", "Financial Intermediary Loan": "technical or other", "Emergency Recovery Loan": "technical or other"}
    add(bucket_task("wb_ch_instr_family", ["instrument"], lambda r: fam[r["instr"]], ["investment", "policy-based", "results-based", "technical or other"], "instrument family", ordered=False, k=4, elig=lambda r: r["instr"] in fam,
                    defs=[("investment", "Pick this for Investment Project Financing, Specific Investment Loan or Sector Investment and Maintenance Loan."), ("policy-based", "Pick this for Development Policy Lending or Structural Adjustment Loan."),
                    ("results-based", "Pick this for Program-for-Results Financing."), ("technical or other", "Pick this for Technical Assistance Loan, Financial Intermediary Loan or Emergency Recovery Loan.")], why="instr -> family"))
    add(bucket_task("wb_ch_env_level", ["env_category"], lambda r: {"A": "full assessment", "B": "partial assessment", "C": "little or no assessment"}[r["env"]], ["full assessment", "partial assessment", "little or no assessment"],
                    "assessment level", elig=lambda r: r["env"] in ("A", "B", "C"), defs=[("full assessment", "Pick this when the environmental category is A."), ("partial assessment", "Pick this when the category is B."),
                    ("little or no assessment", "Pick this when the category is C.")], why="env -> level"))
    add(bucket_task("wb_ch_span_class", ["board_approval_date", "closing_date"], lambda r: "short" if gap(r) <= 3 else "medium" if gap(r) <= 6 else "long", ["short", "medium", "long"], "duration class",
                    elig=lambda r: bool(r["approval"] and r["closing"]) and gap(r) >= 0, defs=[("short", "Pick this when the closing year is 0 to 3 calendar years after the approval year."),
                    ("medium", "Pick this for 4 to 6 years."), ("long", "Pick this for 7 or more years.")], why="gap bins"))
    add(bucket_task("wb_ch_finance_mix", ["ibrd_usd_m", "ida_usd_m"], lambda r: "IBRD only" if r["ida"] == 0 and r["ibrd"] > 0 else "IDA only" if r["ibrd"] == 0 and r["ida"] > 0 else "blend",
                    ["IBRD only", "IDA only", "blend"], "financing mix", ordered=False, k=3, elig=lambda r: r["ibrd"] is not None and r["ida"] is not None and (r["ibrd"] > 0 or r["ida"] > 0),
                    defs=[("IBRD only", "Pick this when the IBRD commitment is above zero and the IDA commitment is zero."), ("IDA only", "Pick this when the IDA commitment is above zero and the IBRD commitment is zero."),
                    ("blend", "Pick this when both are above zero.")], why="ibrd/ida zero pattern"))
    add(bucket_task("wb_ch_fiscal_quarter", ["board_approval_date"], lambda r: {7: "FQ1", 8: "FQ1", 9: "FQ1", 10: "FQ2", 11: "FQ2", 12: "FQ2", 1: "FQ3", 2: "FQ3", 3: "FQ3", 4: "FQ4", 5: "FQ4", 6: "FQ4"}[int(r["approval"][5:7])],
                    ["FQ1", "FQ2", "FQ3", "FQ4"], "fiscal quarter of the approval", elig=lambda r: bool(r["approval"]),
                    defs=[("FQ1", "Pick this for approval in July, August or September."), ("FQ2", "Pick this for October to December."), ("FQ3", "Pick this for January to March."), ("FQ4", "Pick this for April to June.")],
                    why="approval month -> fiscal quarter"))
    return T
