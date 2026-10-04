"""Build the replay-source table of LICENCE_REGISTER.md from replay_licence_scan.json (CPU, no network).
Usage: python3 make_replay_register.py   (rewrites the block between the REPLAY_TABLE markers in LICENCE_REGISTER.md)"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.dirname(HERE)
scan = json.load(open(os.path.join(SPEC, "replay_licence_scan.json")))
cnt, lic = scan["cnt"], scan["lic"]

DROP = {
    "yelp": "Yelp agreement non-commercial; read from a test split",
    "yelp5": "Yelp agreement non-commercial; read from a test split",
    "logiqa2": "CC BY-NC-SA 4.0 upstream (github.com/csitfun/LogiQA2.0)",
    "yahoo": "Licence unknown (Webscope); forbidden list; read from a test split",
    "amazon_polarity": "Forbidden list; terms unclear; read from a test split",
    "musr_murder_mysteries": "DI test items (MuSR has no train split)",
    "musr_object_placements": "DI test items (MuSR has no train split)",
    "musr_team_allocation": "DI test items (MuSR has no train split)",
    "mrpc": "GLUE licence unknown; glue/mrpc forbidden",
    "rte": "GLUE licence unknown",
    "tb_label_nli": "Forbidden label-NLI set; licence 'other'",
    "gd_bbh_mistake": "Reuses BBH inputs (DI test)",
    "civil_comments": "Jigsaw-derived (MBIB 040_Jigsaw in forbidden mbib-base); not grandfatherable",
    "toxic_conv": "Jigsaw-derived (SetFit/toxic_conversations_50k); no licence; not grandfatherable",
    "br_newsmtsc": "Source text POLUSA is non-commercial (zenodo.org/records/3946057); C1 trained on it: disclose",
    "wiki_stance_afd": "No licence on the card; AfD is a JevBench jagged source",
}
DEFAULT_DROP = {
    "boolq": "Forbidden list (super_glue/boolq). Owner may grandfather",
    "condaqa": "Forbidden list (CONDAQA). Owner may grandfather",
    "dbpedia": "Forbidden list (dbpedia_14). Owner may grandfather",
    "banking77": "Forbidden list (banking77); also a dev source and DI test. Owner may grandfather",
}
CLAUDE_GOLD = ("binj_", "std_", "hard_", "planted_", "proc_")
PROGRAM = {"judge_mathderiv": "procedural (build_judge.py)"}
MAP = {
    "judge_prm800k": "map to MIT, github.com/openai/prm800k (as gd_prm800k_steps); judged-object exception",
}
# Verifier 3 Oct: decision 6 (a creator's own HF card is not an official licence record) and decision 12 (unverified
# = out, new AND replay) also apply to replay. These sources cite only the creator's HF card in meta.licence.
_HF = "creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop"
HF_ONLY = {
    "br_congress_policy": _HF, "br_steam_aspect": _HF + "; 3.G also excludes Steam for new rows",
    "gd_aegis_prompts": _HF + "; prompts only", "gd_climate_targets": _HF, "gd_edgar_10k_item": _HF,
    "gd_faithdial": _HF, "gd_helpsteer2_attr": _HF + "; judged-object exception",
    "gd_helpsteer3_pref": _HF + "; minus 1 OHS-3 overlap unit (A10); judged-object exception",
    "gd_mfrc": _HF, "gd_mtbench_human": _HF + "; judged-object exception", "gd_qasc": _HF, "gd_quartz": _HF,
    "gd_ropes_sci": _HF, "gd_spiced": _HF,
    "judge_helpsteer2": _HF + " (same record as gd_helpsteer2_attr); judged-object exception",
}
VERIFY = {
    "clinc150": "candidate CC BY 3.0 (github.com/clinc/oos-eval); train split only; dev source + DI test",
    "massive": "candidate CC BY 4.0 (github.com/alexa/massive)",
    "mnli3": "MultiNLI: mixed licences by genre (OANC, CC BY-SA 3.0 fiction, other); check the official MultiNLI page",
    "mnli": "MultiNLI: mixed licences by genre; check the official MultiNLI page",
    "mnli_neutral": "MultiNLI: mixed licences by genre; check the official MultiNLI page",
    "qnli": "GLUE QNLI (from SQuAD 1.1, CC BY-SA 4.0); GLUE terms to check",
    "proofwriter": "candidate CC BY 4.0 at the AllenAI original (not the tasksource mirror)",
    "fld": "unknown (hitachi-nlp FLD release); check the repo LICENSE",
    "csqa": "candidate MIT (CommonsenseQA original release)",
    "arc": "candidate CC BY-SA 4.0 (AI2 ARC); train split only (DI uses the test split)",
    "copa": "candidate BSD-2 (COPA original release)",
    "clothing": "candidate CC0 at the original Kaggle page (Women's E-Commerce Clothing Reviews); the mirror does not count",
    "gd_finqa": "FinQA annotations MIT (V); report text = FinTabNet, CDLA-Permissive-1.0 per papers only, IBM record unverified and not on the allowed list (merge 3 Oct); same rule as MultiHiertt/ConvFinQA",
}
ZENODO = {"br_claimbuster", "br_mnds", "gd_clickbait16", "gd_clickbait17", "gd_crowdtruth_mre", "gd_drugprot",
          "gd_east_asian_prejudice"}
JUDGED = {"gd_helpsteer2_attr", "gd_helpsteer3_pref", "gd_prm800k_steps", "gd_ragtruth_summary", "gd_mtbench_human"}
NOTES = {
    "gd_redocred": "minus 6 OHS-3 overlap units (A10)",
    "gd_helpsteer3_pref": "minus 1 OHS-3 overlap unit (A10); judged-object exception",
    "gd_ragtruth_summary": "judged-object exception; DI RAGTruth-adjacent (disclose); CNN/DM text, MIT covers annotations",
    "gd_casehold_yn": "CaseHOLD is not OHS-1's legal part (LegalBench + LEDGAR)",
    "gd_winogrande": "train split only (DI uses validation)",
    "gd_storm_ef": "weather events: makes weather-heavy sealed domains 'adjacent'",
    "gd_aegis_prompts": "prompts only (Aegis responses are LLM-written and excluded)",
}


def short(s):
    s = s.replace("|", "/")
    m = re.match(r"^\s*([^()]{0,60}?)\s*(\(|$)", s)
    head = (m.group(1) if m else s[:60]).strip().rstrip(";,")
    return head or s[:60]


rows, tot = [], {"KEEP": 0, "KEEP (program)": 0, "KEEP (mapped)": 0, "VERIFY or drop": 0, "DROP": 0,
                 "DROP (default)": 0}
for s in sorted(cnt):
    n = cnt[s]
    L = max(lic[s].items(), key=lambda x: x[1])[0]
    sa = "SA" if re.search(r"BY-SA|BY SA|GFDL", L) else ""
    if s in DROP:
        st, note = "DROP", DROP[s]
    elif s in DEFAULT_DROP:
        st, note = "DROP (default)", DEFAULT_DROP[s]
    elif s.startswith(CLAUDE_GOLD):
        st, note = "DROP (default)", "Claude-written golds, blind-solved. Owner may grandfather"
    elif s.startswith("pg_") or s in PROGRAM:
        st, note = "KEEP (program)", PROGRAM.get(s, "procedural generator (build_pg.py)") + "; stamp CC0 1.0 (program-generated)"
    elif s in MAP:
        st, note = "KEEP (mapped)", MAP[s]
    elif s in VERIFY:
        st, note = "VERIFY or drop", VERIFY[s]
    elif s in HF_ONLY:
        st, note = "VERIFY or drop", HF_ONLY[s]
    elif s.startswith("gd_gen"):
        st, note = "KEEP (program)", "program-generated in this repo"
    else:
        st, note = "KEEP", ""
        if s in ZENODO:
            note = "Zenodo-hosted (owner decision 7)"
        if s in JUDGED and s not in NOTES:
            note = "judged-object exception (LLM outputs judged by humans)"
        if s in NOTES:
            note = NOTES[s]
    tot[st] += n
    shown = short(L) if L else "(none in meta)"
    rows.append(f"| `{s}` | {n:,} | {shown} | {sa} | {st} | {note} |")

out = ["| Source | Rows | Licence (from meta; full string with URL in replay_licence_scan.json) | SA | Status | Note |",
       "|---|---|---|---|---|---|"] + rows
out += ["", "**Totals by status:** " + "; ".join(f"{k} {v:,}" for k, v in tot.items())
        + f"; all {sum(cnt.values()):,} rows in {len(cnt)} sources."]
block = "\n".join(out)
path = os.path.join(SPEC, "LICENCE_REGISTER.md")
doc = open(path).read()
a, b = "<!-- REPLAY_TABLE_START -->", "<!-- REPLAY_TABLE_END -->"
i, j = doc.index(a) + len(a), doc.index(b)
open(path, "w").write(doc[:i] + "\n" + block + "\n" + doc[j:])
print(block.splitlines()[-1])
