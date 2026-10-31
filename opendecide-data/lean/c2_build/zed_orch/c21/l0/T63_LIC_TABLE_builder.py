"""T63-LIC-TABLE builder (T63-B6). Rules first, then explicit per-cell overrides from the block review. Identifiers only, no licence text.
Usage: python lic_build.py review   -> print non-permissive blocks (rules + overrides applied)
       python lic_build.py write    -> write T63_LIC_TABLE.json + T63_LIC_TABLE_RECORD.json
"""
import collections
import datetime
import hashlib
import itertools
import json
import os
import sys

C2 = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build"
sys.path.insert(0, os.path.join(C2, "c21_fam"))
from LP_COMMON import util  # noqa: E402
from T63 import lic, config as CFG  # noqa: E402

L0 = os.path.join(C2, "zed_orch", "c21", "l0")
DEP = list(lic.DEP_IDS)
PROJ = list(lic.PROJECT_IDS)
USE = list(lic.USE_IDS)
DIST = list(lic.DIST_IDS)
UN = CFG.LIC_USE
DN = CFG.LIC_DIST

FAM = {"MIT": "permissive", "Apache-2.0": "permissive", "BSD-2-Clause": "permissive", "BSD-3-Clause": "permissive", "ISC": "permissive",
       "CC0-1.0": "permissive", "Unlicense": "permissive", "MPL-2.0": "weak_file", "LGPL-2.1-only": "weak_lib", "LGPL-3.0-only": "weak_lib",
       "GPL-2.0-only": "strong", "GPL-3.0-only": "strong", "AGPL-3.0-only": "network", "CC-BY-4.0": "cc_by", "CC-BY-NC-4.0": "cc_nc",
       "NOASSERTION": "marker"}
PERMP = ("MIT", "Apache-2.0", "BSD-3-Clause")
GPL3FAM = ("GPL-3.0-only", "AGPL-3.0-only")              # project licences that can carry GPL-3.0-family code in a combined work
LGPL_CARRY = ("LGPL-3.0-only", "GPL-3.0-only", "AGPL-3.0-only")
MARK = "NOASSERTION"
U1, U2, U3, U4, U5 = USE
D1, D2, D3 = DIST

DECISION_RULES = {
    "label_semantics": {
        "COMPATIBLE": "the project can keep its stated licence for the work in this usage and distribution mode, with the dependency's routine duties "
                      "(notice, attribution, per-file source offer) met; clearly fine",
        "INCOMPATIBLE": "meeting the dependency's terms in this mode needs the combined work under terms the project licence id cannot give; clear, widely "
                        "agreed conflict",
        "REVIEW": "contested or condition-dependent (linking theory, relink material, network-use reach, commercial-use facts, unknown terms); a human "
                  "must decide",
        "scope": "policy gold for a coding agent over SPDX identifiers only; NOT legal advice; no licence text is quoted",
    },
    "trigger_rules": [
        "T1 LC-USE-5 dev-time tool only: nothing of the dependency ships or is combined with the product -> COMPATIBLE unless the dependency is "
        "CC-BY-NC-4.0 (commercial-use facts) or the marker (unknown terms) -> REVIEW",
        "T2 LC-USE-4 separate process: separate program across a process boundary is not one combined work; the dependency's duties stay with that "
        "program -> COMPATIBLE unless CC-BY-NC-4.0 or the marker -> REVIEW",
        "T3 LC-DIST-2 internal only and LC-DIST-3 network service: distribution-triggered copyleft (GPL, LGPL, MPL) is not triggered -> COMPATIBLE; "
        "the AGPL-3.0-only network-use clause is the exception (rule F5)",
        "T4 LC-DIST-1 distributed to others with LC-USE-1/2/3: copyleft scope decides; LC-USE-1 vendored and LC-USE-2 static form one combined work "
        "(widely agreed); LC-USE-3 dynamic link combined-work status is contested -> never INCOMPATIBLE on the dynamic-link theory alone",
        "T5 consistency: internal only and dev-time tool only are never stricter than distributed to others for the same pair",
    ],
    "family_rules": [
        "F1 permissive (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, CC0-1.0, Unlicense): notice/attribution only -> COMPATIBLE in every cell, "
        "every project id including the marker",
        "F2 weak copyleft, file-level (MPL-2.0): per-file copyleft; larger work may keep the project licence; GPL-family projects reach it through "
        "the MPL-2.0 secondary-licence path -> COMPATIBLE, except LC-USE-1 vendored + LC-DIST-1 into MIT / Apache-2.0 / BSD-3-Clause / marker "
        "projects -> REVIEW (copied files keep MPL-2.0 and edits to them must be offered in source)",
        "F3 weak copyleft, library (LGPL-2.1-only, LGPL-3.0-only): projects LGPL-3.0-only / GPL-3.0-only / AGPL-3.0-only can carry the code "
        "-> COMPATIBLE; otherwise LC-DIST-1 + LC-USE-1/2 -> REVIEW (relink material and library-stays-LGPL conditions), LC-USE-3 -> COMPATIBLE "
        "(designed case), but REVIEW for the marker project (project terms must allow modification and reverse engineering)",
        "F4 strong copyleft (GPL-2.0-only, GPL-3.0-only): GPL-3.0-only / AGPL-3.0-only projects carry it -> COMPATIBLE; marker project + "
        "LC-DIST-1 + LC-USE-1/2/3 -> REVIEW (project terms not asserted); other projects + LC-DIST-1: LC-USE-1/2 -> INCOMPATIBLE, LC-USE-3 -> REVIEW",
        "F5 network copyleft (AGPL-3.0-only): LC-DIST-1 as F4; LC-DIST-2/3 + LC-USE-1/2/3 -> REVIEW (network-use source duty for a combined "
        "program; reach without modification and for internal remote users contested) except an AGPL-3.0-only project -> COMPATIBLE; "
        "LC-USE-4/5 -> COMPATIBLE",
        "F6 CC-BY-4.0: attribution only, no copyleft -> COMPATIBLE, except marker project + LC-DIST-1 + LC-USE-1/2/3 -> REVIEW (the licence bars "
        "downstream restrictions on the material; unknown project terms may add them)",
        "F7 CC-BY-NC-4.0: non-commercial limit -> REVIEW everywhere (commercial-use facts), except GPL-3.0-only / AGPL-3.0-only projects + "
        "LC-DIST-1 + LC-USE-1/2 -> INCOMPATIBLE (those projects forbid added restrictions on a distributed combined work)",
        "F8 proprietary / no-assertion marker as dependency (NOASSERTION): grant terms unknown -> REVIEW in every cell",
        "F9 marker as project: copyleft-triggered cells -> REVIEW (whether the unasserted project terms can meet the copyleft is unknown); "
        "untriggered cells follow the dependency rule",
    ],
}


def rule(dep, proj, use, dist):
    """-> (label, rule_id, rationale). Family + trigger rules only (no overrides)."""
    f = FAM[dep]
    un, dn = UN[use], DN[dist]
    if f == "permissive":
        return "COMPATIBLE", "F1", "%s is permissive: notice/attribution duties only; no copyleft reaches a %s work (%s, %s)" % (dep, proj, un, dn)
    if f == "marker":
        return "REVIEW", "F8", "dependency carries the proprietary / no-assertion marker: grant terms unknown, a human must confirm rights (%s, %s)" % (un, dn)
    if f == "cc_nc":
        if proj in GPL3FAM and use in (U1, U2) and dist == D1:
            return ("INCOMPATIBLE", "F7",
                    "CC-BY-NC-4.0 adds a non-commercial limit; %s forbids added restrictions on a distributed combined work (%s)" % (proj, un))
        return "REVIEW", "F7", "CC-BY-NC-4.0 non-commercial limit: whether this use (%s, %s) is commercial is fact-dependent" % (un, dn)
    if use == U5:
        return "COMPATIBLE", "T1", "dev-time tool only: %s is neither shipped nor combined with the product, so its terms do not reach %s code" % (dep, proj)
    if use == U4:
        return ("COMPATIBLE", "T2",
                "separate process: %s runs as its own program across a process boundary, not one combined work with %s code (%s)" % (dep, proj, dn))
    if f == "cc_by":
        if proj == MARK and dist == D1:
            return ("REVIEW", "F6",
                    "CC-BY-4.0 bars downstream restrictions on the material; unasserted project terms may add them in a distributed %s build" % un)
        return "COMPATIBLE", "F6", "CC-BY-4.0 needs attribution only, no copyleft; fits a %s work with attribution kept (%s, %s)" % (proj, un, dn)
    if f == "network" and dist in (D2, D3):
        if proj == "AGPL-3.0-only":
            return "COMPATIBLE", "F5", "AGPL-3.0-only dependency in an AGPL-3.0-only project: same licence, network-use source duty already the project's (%s, %s)" % (un, dn)
        if dist == D2:
            return ("REVIEW", "F5",
                    "AGPL-3.0-only network-use clause: whether internal remote users of a combined program (%s) trigger a source offer is condition-dependent; %s" % (un, proj))
        return ("REVIEW", "F5",
                "AGPL-3.0-only network-use clause on a combined program (%s) offered as a service; reach without modification is contested and %s does not carry AGPL terms" % (un, proj))
    if dist in (D2, D3):
        return "COMPATIBLE", "T3", "%s: nothing is conveyed, so the distribution-triggered copyleft of %s is not triggered (%s, %s)" % (dn, dep, un, proj)
    # dist == D1, use in U1..U3
    if f == "weak_file":
        if use == U1 and (proj in PERMP or proj == MARK):
            return ("REVIEW", "F2",
                    "vendored MPL-2.0 files keep MPL-2.0 inside a %s tree and edits to them must be offered in source: per-file conditions to check" % proj)
        if proj in LGPL_CARRY and use == U1:
            return "COMPATIBLE", "F2", "MPL-2.0 files may sit in a %s larger work through the MPL-2.0 secondary-licence path; distributed vendored copy" % proj
        return "COMPATIBLE", "F2", "MPL-2.0 copyleft is per file: MPL files keep MPL-2.0 with source offered, the larger work may stay %s (%s, distributed)" % (proj, un)
    if f == "weak_lib":
        if proj in LGPL_CARRY:
            why = "LGPL-3.0-only is GPL-3.0 terms plus permissions" if dep == "LGPL-3.0-only" else "LGPL-2.1-only may be converted to GPL terms"
            return "COMPATIBLE", "F3", "%s code can be carried in a %s work (%s); %s, distributed" % (dep, proj, why, un)
        if use == U3:
            if proj == MARK:
                return ("REVIEW", "F3",
                        "%s dynamic link needs project terms that allow modification and reverse engineering; the marker project's terms are unknown" % dep)
            return "COMPATIBLE", "F3", "%s dynamic link is the designed case: replaceable library plus notice leave the %s work under %s" % (dep, proj, proj)
        return ("REVIEW", "F3",
                "%s %s into a %s work: allowed only if the library stays %s and relink material is supplied; condition-dependent" % (dep, un, proj, dep))
    if f in ("strong", "network"):
        if proj in GPL3FAM:
            return "COMPATIBLE", "F4", "%s code can be carried in a %s work (same licence or GPL-3.0/AGPL-3.0 combination permission); %s, distributed" % (dep, proj, un)
        if proj == MARK:
            return ("REVIEW", "F9",
                    "%s copyleft triggers on distributing the combined work (%s); the project licence is not asserted, so whether it can meet that is unknown" % (dep, un))
        if use in (U1, U2):
            return ("INCOMPATIBLE", "F4",
                    "%s copyleft triggers on distribution of the combined work (%s); %s cannot meet it without relicensing the whole" % (dep, un, proj))
        return ("REVIEW", "F4",
                "%s dynamic link: whether it forms one combined work is contested; if it does, %s cannot meet the copyleft on distribution" % (dep, proj))
    raise AssertionError((dep, proj, use, dist))


def k(dep, proj, use, dist):
    return lic.key(dep, proj, use, dist)


# ---- overrides from the block review (cell -> (label, reason)); filled after reading every non-permissive block -------------------
OVERRIDES = {}


def _ov(dep, proj, uses, dists, label, reason):
    for u in uses:
        for d in dists:
            OVERRIDES[k(dep, proj, u, d)] = (label, reason)


_ov("GPL-2.0-only", "GPL-3.0-only", (U1, U2), (D1,), "INCOMPATIBLE",
    "rule F4 treats GPL-3.0-only as able to carry GPL code, but GPL-2.0-only has no later-version option and GPL-3.0-only adds terms: "
    "the distributed combined work cannot meet both")
_ov("GPL-2.0-only", "GPL-3.0-only", (U3,), (D1,), "REVIEW",
    "same GPL-2.0-only / GPL-3.0-only conflict, but dynamic-link combined-work status is contested (T4)")
_ov("GPL-2.0-only", "AGPL-3.0-only", (U1, U2), (D1,), "INCOMPATIBLE",
    "rule F4 treats AGPL-3.0-only as able to carry GPL code, but GPL-2.0-only cannot join a GPL-3.0-family combined work: distributed "
    "combination cannot meet both")
_ov("GPL-2.0-only", "AGPL-3.0-only", (U3,), (D1,), "REVIEW",
    "same GPL-2.0-only / AGPL-3.0-only conflict, dynamic-link combined-work status contested (T4)")
_ov("GPL-2.0-only", "AGPL-3.0-only", (U1, U2, U3), (D3,), "REVIEW",
    "rule T3 says nothing is conveyed, but the AGPL-3.0-only project's network-use source duty would cover a combined program that "
    "GPL-2.0-only code cannot join on AGPL-3.0-only terms; contested network-use reach")
_ov("AGPL-3.0-only", "GPL-3.0-only", (U1, U2, U3), (D2, D3), "COMPATIBLE",
    "rule F5 gives REVIEW for non-AGPL projects, but GPL-3.0-only expressly permits combination with AGPL-3.0-only; the network-use duty "
    "then covers the combination and a GPL-3.0-only project can meet it (same as its LC-DIST-1 cells)")
_ov("LGPL-2.1-only", "LGPL-3.0-only", (U1, U2), (D1,), "REVIEW",
    "rule F3 lets LGPL-3.0-only carry LGPL code, but LGPL-2.1-only converts only to GPL terms, not to LGPL-3.0-only; keeping it a "
    "separate relinkable library or moving the project to GPL is condition-dependent")
_ov("CC-BY-NC-4.0", "LGPL-3.0-only", (U1, U2), (D1,), "INCOMPATIBLE",
    "rule F7 only names GPL-3.0-only / AGPL-3.0-only, but LGPL-3.0-only builds on GPL-3.0 terms that forbid added restrictions on the "
    "distributed library work; the non-commercial limit is one")



def override_rationale(dep, proj, use, dist, label):
    un, dn = UN[use], DN[dist]
    if dep == "GPL-2.0-only" and dist == D1 and label == "INCOMPATIBLE":
        return "GPL-2.0-only has no later-version option and %s adds terms: the distributed combined work (%s) cannot meet both" % (proj, un)
    if dep == "GPL-2.0-only" and dist == D1:
        return "GPL-2.0-only vs %s conflict if dynamic linking forms one combined work; that status is contested" % proj
    if dep == "GPL-2.0-only" and dist == D3:
        return ("AGPL-3.0-only project offered as a service: its network-use source duty would cover a combined program (%s) that GPL-2.0-only code "
                "cannot join; contested" % un)
    if dep == "AGPL-3.0-only":
        return ("GPL-3.0-only permits combination with AGPL-3.0-only; the network-use duty covers the combination (%s, %s) and a GPL-3.0-only "
                "project can meet it" % (un, dn))
    if dep == "LGPL-2.1-only":
        return ("LGPL-2.1-only converts only to GPL terms, not to LGPL-3.0-only; %s keeps the project LGPL-3.0-only only under library/relink "
                "conditions" % un)
    if dep == "CC-BY-NC-4.0":
        return ("CC-BY-NC-4.0 adds a non-commercial limit; LGPL-3.0-only builds on GPL-3.0 terms that forbid added restrictions on the distributed "
                "library work (%s)" % un)
    raise AssertionError((dep, proj, use, dist))


def build():
    cells, rule_out, overrides = {}, {}, []
    for dep, proj, use, dist in itertools.product(DEP, PROJ, USE, DIST):
        lab, rid, why = rule(dep, proj, use, dist)
        key = k(dep, proj, use, dist)
        rule_out[key] = lab
        if key in OVERRIDES:
            nlab, reason = OVERRIDES[key]
            if nlab != lab:
                overrides.append({"cell": key, "rule": rid, "rule_label": lab, "final_label": nlab, "reason": reason})
            lab, rid, why = nlab, rid + "+override", override_rationale(dep, proj, use, dist, nlab)
        cells[key] = {"label": lab, "rationale": why, "rule": rid}
    return cells, rule_out, overrides


RANK = {"COMPATIBLE": 0, "REVIEW": 1, "INCOMPATIBLE": 2}


def self_checks(cells, overrides):
    out = {}
    want = {k(*c) for c in itertools.product(DEP, PROJ, USE, DIST)}
    out["cells_expected"] = len(want)
    out["cells_present"] = len(cells)
    out["every_cell_exactly_once"] = (set(cells) == want and len(cells) == len(want))
    cnt = collections.Counter(v["label"] for v in cells.values())
    out["label_counts"] = {lab: cnt.get(lab, 0) for lab in CFG.LIC_LABELS}
    out["label_shares"] = {lab: round(cnt.get(lab, 0) / float(len(cells)), 4) for lab in CFG.LIC_LABELS}
    fams = collections.OrderedDict()
    for dep in DEP:
        f = FAM[dep]
        fams.setdefault(f, collections.Counter())
        for key, v in cells.items():
            if key.split("|")[0] == dep:
                fams[f][v["label"]] += 1
    out["label_counts_per_family"] = {f: {lab: c.get(lab, 0) for lab in CFG.LIC_LABELS} for f, c in fams.items()}
    per_dep = {}
    for dep in DEP:
        c = collections.Counter(v["label"] for key, v in cells.items() if key.split("|")[0] == dep)
        per_dep[dep] = {lab: c.get(lab, 0) for lab in CFG.LIC_LABELS}
    out["label_counts_per_dependency"] = per_dep
    mixed, mixed_cells = [], collections.Counter()
    for dep, proj in itertools.product(DEP, PROJ):
        labs = {cells[k(dep, proj, u, d)]["label"] for u in USE for d in DIST}
        if len(labs) >= 2:
            mixed.append("%s|%s" % (dep, proj))
            for u in USE:
                for d in DIST:
                    mixed_cells[cells[k(dep, proj, u, d)]["label"]] += 1
    npairs = len(DEP) * len(PROJ)
    out["mixed_pairs"] = {"count": len(mixed), "of": npairs, "share": round(len(mixed) / float(npairs), 4),
                          "cells_in_mixed_pairs_by_label": {lab: mixed_cells.get(lab, 0) for lab in CFG.LIC_LABELS},
                          "pairs": mixed}
    viol = []
    for dep, proj in itertools.product(DEP, PROJ):
        for u in USE:
            if RANK[cells[k(dep, proj, u, D2)]["label"]] > RANK[cells[k(dep, proj, u, D1)]["label"]]:
                viol.append("D2>D1 %s" % k(dep, proj, u, D2))
        for d in DIST:
            for u in USE:
                if RANK[cells[k(dep, proj, U5, d)]["label"]] > RANK[cells[k(dep, proj, u, d)]["label"]]:
                    viol.append("U5>%s %s" % (u, k(dep, proj, U5, d)))
        for u in USE:   # dev-time tool vs distributed (any use)
            if RANK[cells[k(dep, proj, U5, D1)]["label"]] > RANK[cells[k(dep, proj, u, D1)]["label"]]:
                viol.append("U5D1>%sD1 %s" % (u, k(dep, proj, u, D1)))
    d3 = []
    for dep, proj in itertools.product(DEP, PROJ):
        for u in USE:
            if RANK[cells[k(dep, proj, u, D3)]["label"]] > RANK[cells[k(dep, proj, u, D1)]["label"]]:
                d3.append(k(dep, proj, u, D3))
    out["consistency"] = {"internal_or_devtool_stricter_than_distributed": viol, "violations": len(viol), "justified_exceptions": [],
                          "report_only_network_stricter_than_distributed": d3}
    out["overrides_count"] = len(overrides)
    return out


def review():
    cells, _, overrides = build()
    for dep in DEP:
        if FAM[dep] == "permissive":
            continue
        for proj in PROJ:
            print("== %s -> %s" % (dep, proj))
            for u in USE:
                row = []
                for d in DIST:
                    c = cells[k(dep, proj, u, d)]
                    row.append("%-12s%s" % (c["label"][:4] + ("*" if "override" in c["rule"] else ""), c["rule"].split("+")[0]))
                print("   %-9s %s" % (u, " | ".join(row)))
    print("overrides:", len(overrides))
    print(json.dumps({x: y for x, y in self_checks(cells, overrides).items() if x not in ("label_counts_per_dependency",)}, indent=1)[:3000])


def write():
    cells, _, overrides = build()
    checks = self_checks(cells, overrides)
    checks["k10_mixed_pair_support"] = (
        "K10 needs >= 40%% of LIC ROWS from mixed pairs; %d of 128 pairs (%.1f%%) are mixed but they hold %d cells including all %d INCOMPATIBLE "
        "cells, so a label-stratified draw can reach >= 40%% mixed-pair rows" % (checks["mixed_pairs"]["count"], 100 * checks["mixed_pairs"]["share"],
        sum(checks["mixed_pairs"]["cells_in_mixed_pairs_by_label"].values()), checks["label_counts"]["INCOMPATIBLE"]))
    data = {"table_id": "T63-LIC-TABLE", "fixture": False,
            "note": "Policy gold for a coding agent over SPDX identifiers only; NOT legal advice. No licence text is quoted. NOASSERTION is the "
                    "proprietary / no-assertion marker.",
            "author": "Opus 5.5 high, separate session (T63-B6)",
            "dep_ids": DEP, "project_ids": PROJ, "use": USE, "dist": DIST,
            "use_names": UN, "dist_names": DN,
            "decision_rules": DECISION_RULES, "cells": cells, "overrides": overrides, "self_checks": checks}
    tb = lic.LicTable(data)                     # computes the canonical content sha exactly as the loader does
    data["sha256"] = tb.sha
    lic.LicTable(data)                          # re-validate with the declared sha
    tpath = os.path.join(L0, "T63_LIC_TABLE.json")
    rpath = os.path.join(L0, "T63_LIC_TABLE_RECORD.json")
    for pth in (tpath, rpath):
        if os.path.exists(pth):
            raise SystemExit("refusing to overwrite " + pth)
    with open(tpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, sort_keys=False, ensure_ascii=True)
        f.write("\n")
    file_sha = util.sha256_file(tpath)
    rec = {"table_id": "T63-LIC-TABLE", "sha256": tb.sha,
           "sha256_kind": "canonical content sha (LP_COMMON.util.sha_obj over cells labels + id lists), the value lic.LicTable and "
                          "pool_writer.check_table_binding compare",
           "file_sha256": file_sha, "file": "zed_orch/c21/l0/T63_LIC_TABLE.json",
           "cell_count": len(cells), "label_counts": checks["label_counts"], "overrides_count": len(overrides),
           "author": "Opus 5.5 high, separate session (T63-B6)",
           "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "note": "policy gold for a coding agent, not legal advice; identifiers only; hashed before any LIC row"}
    with open(rpath, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=True)
        f.write("\n")
    print(json.dumps(rec, indent=1))
    print("record file sha256", util.sha256_file(rpath))


if __name__ == "__main__":
    if sys.argv[1] == "review":
        review()
    elif sys.argv[1] == "write":
        write()
