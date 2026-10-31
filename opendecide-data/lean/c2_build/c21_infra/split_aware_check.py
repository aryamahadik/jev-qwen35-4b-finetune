"""A61(b) split-aware dataset check (C2.1 L-0 item (k); owner adopted R5 = A61(b), PREREG record A79; v2 brings the
code to rulings A82 1, 2, 7 and the v3.2 skeptic items 1, 2, 24 of plan section 16.1 step 0).

WHAT IT DECIDES
  Given a candidate public dataset (name, split names, licence, label provenance) it returns ONE record with
  decision ALLOW or DENY and a list of reasons. ALLOW is only ever given to human-labelled, permissively
  licensed TRAIN splits of a dataset that:
    - is not an A61(a) 8.5 HIT source under any id or form (gsm8k, hover, isarcasmeval, tydiqa, md_fdc, md_peps,
      DI-TS inputs, md_worldbank, md_usgs, md_cma; SB6 is added because the frozen names-only manifest lists it).
      The DI-TS inputs are barred BY NAME, every id and alias: CogComp/perspectrum,
      google-deepmind/logical-entailment-dataset, kunalkukreja21/temporal-expressions-evaluation-lm;
    - is not LLM-generated (labels or text), and does not derive from an LLM-generated or barred upstream;
    - is not an eval set, and has no test/dev split that is an eval target, in the G13 target registry
      (sections A, B, C, D, M), and is not a registry source bar (section E);
    - has no split-blind deny-list entry (a deny-list entry that names no splits taints the whole dataset).
  The ONE thing "split-aware" adds (A61(b)): a deny-list entry that names ONLY test/dev splits as tainted does
  not block the train split. A61(a) HITs and registry eval targets are never released by this rule.

LICENCES (A82 2, A82 7)
  Allowed: MIT, Apache-2.0, BSD, ISC, CC0, CC BY, CC BY-SA (share-alike: allowed AND disclosed; the record carries
  share_alike_disclosure: true and a note), CDLA-Permissive-1.0/2.0, ODC-By, US public domain / US Government
  work. Never allowed: any NC or ND term, GPL / LGPL / AGPL and other copyleft code licences, CDLA-Sharing, ODbL.

SPLIT-SCOPED RELEASE (A82 1; off unless --split-scoped-release; v3.2-r Sk 2, Sk 3)
  A dataset whose registry entry targets only named test/dev splits releases its TRAIN split ONLY when ALL of:
    1. only train-like splits are requested and none intersects the registry-scoped test/dev splits;
    2. the candidate carries g13_record = {"path": ..., "sha256": ...} (the G13 RESULT RECORD) and the file at path
       has exactly that sha256 (the "result sha"); a path with an ohs/sealed component is never opened;
    3. the record shows disjointness over the WHOLE train split, strictly: complete, not sampled, no row cap,
       rows_checked == rows_in_split == the candidate's declared train_split_rows (the full split from the card, never a
       capped subset), 0 hits outside R6 scaffolding, 0 rows dropped to reach disjointness (row-drop reading is not
       used in C2.1), against every registered target, for the CURRENT registry sha and a named method-set version.
  A released record carries train_split_seen: true and a g13_evidence block (path, sha256, registry sha, method-set
  version, per-split row counts). Without the flag, or with missing/stale/partial evidence, the dataset is denied.
  Result-record JSON the tool reads (all fields required):
    {"kind": "g13_result_record", "dataset": <name or hf_id>, "registry_sha256": <hex>, "method_set_version": <str>,
     "registry_entries": <int, = number of registry ids the run loaded>, "targets_all_registered": true,
     "complete": true, "rows_dropped_for_disjointness": 0,
     "splits": {<split>: {"rows_in_split": N, "rows_checked": N, "sampled": false, "row_cap": null,
                          "hits": H, "hits_outside_r6_scaffolding": 0}}}

SKEPTIC FIXES (v2.1, fresh Sonnet; S numbers are cited in the tests)
  S1 wrong-typed name / hf_id / aliases / derived_from entries never drop out of a bar check (a string is one entry, a
     dict upstream is read by name / hf_id / aliases, anything else is CANDIDATE_MALFORMED); S2 names are NFKD-folded and
     a name that still has non-ASCII characters is NON_ASCII_NAME (no homoglyph spelling); S3 only "dataset" and
     "catalogue" are kinds, and any members list makes a candidate a catalogue; S4 joined split names (trainval, holdout)
     are not train; S5 a slice is never a whole split; S7 a deny-list entry that taints only test/dev splits releases the
     train split only through the same flag + G13 result record (no evidence-free release anywhere); S8 more LLM names
     and AI-assist words; S9 evidence must be a regular file; S10 punctuation-only names never match a record; S11
     HotpotQA (named upstream of hover) is denied until an Opus ruling edits the table; S12 name bars for the A82 4 / 5
     EXCLUDED list and declared A82 9 violations (languages, modality); S13 wider DI-TS member aliases.
  Residuals no offline tool can close: the G13 result record is a file whose sha is pinned but whose maker is not
  authenticated, and train_split_rows is the candidate's own card number (the orchestrator checks both against the stamp
  service and the card at Opus sign-off); free-text provenance with an unlisted model name beside a human word still
  reads as human (use the enumerated values).

WHAT ALLOW DOES NOT MEAN
  ALLOW = "not barred by A61(b)". The source still needs its pre-mapper 8.5 PASS (orchestrator), the guards, the
  check-at-creation G13 stamp on every row, and a name on a re-frozen manifest before any mapper or row exists.
  This tool downloads nothing, reads no dataset and calls no model; it reads names and metadata only (plus, for a
  split-scoped release, the one G13 result record the candidate names).

FAIL-CLOSED
  Missing or unrecognised metadata is a DENY with deny_class INSUFFICIENT_EVIDENCE (not barred, just not
  shown to be safe); a barred fact is deny_class BAR. A catalogue (kind "catalogue") is never allowed as a
  whole: each member is a separate record and carries its own decision.

INPUT (JSON list of candidate objects; every field optional except name)
  name, aliases[], hf_id, kind ("dataset" | "catalogue"), splits_available[], splits_requested[]
  (default: every train-like split available), licence (string | list), label_provenance (string),
  text_provenance (string), derived_from[], eval_target_splits[] (splits of THIS dataset that we use as eval
  targets), members[] (child candidates of a catalogue).
  Prefer the enumerated label_provenance values: human, human_crowd, human_expert, llm_generated,
  mixed_human_llm, program, heuristic, model_labelled, unknown. Free text is scanned for LLM markers
  (any LLM marker denies, even in a negated sentence: fail-closed).

DENY-LIST FILE (optional, JSON list): {"name", "keys": [...], "tainted_splits": [...] | null, "reason", "ref"}
  tainted_splits null or ["*"] = split-blind (denies). Only test/dev-like tainted splits release the train
  split. Entries that match an A61(a) HIT are never released.

Only names, split names, licences and shas are read or printed. No path with ohs/sealed in any component is
ever opened (pathskip). Exit codes: 0 ok, 2 usage/input error.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathskip import is_skipped_path  # noqa: E402

TOOL_VERSION = "split_aware_check v2.1 (18 Oct 2026; A82 1, 2, 7; v3.2-r Sk 1, 2, 24; skeptic fixes S1-S14)"

# ----------------------------------------------------------------------------------------------------------
# Reason codes. BAR = a barred fact; INSUFFICIENT = metadata missing or unrecognised (fail-closed).
# ----------------------------------------------------------------------------------------------------------
BAR_CODES = {
    "A61A_HIT", "UPSTREAM_A61A_HIT", "REGISTRY_EVAL_TARGET", "REGISTRY_EVAL_TARGET_SPLIT_SCOPED",
    "REGISTRY_SOURCE_BAR", "UPSTREAM_BARRED", "DENYLIST_SPLIT_BLIND", "DENYLIST_TAINTED_TRAIN_SPLIT",
    "NO_TRAIN_SPLIT", "REQUESTED_SPLIT_NOT_TRAIN", "REQUESTED_SPLIT_NOT_AVAILABLE", "EVAL_TARGET_SPLIT_DECLARED",
    "LICENCE_NOT_PERMISSIVE", "LICENCE_ABSENT", "LABELS_LLM_GENERATED", "LABELS_NOT_HUMAN",
    "TEXT_LLM_GENERATED", "COMPETITOR_OUTPUT", "G13_HITS_OUTSIDE_SCAFFOLDING",
    "DENYLIST_TEST_ONLY_SPLIT_SCOPED", "A82_EXCLUDED", "NON_ENGLISH_DECLARED", "NON_TEXT_DECLARED",
}
INSUFFICIENT_CODES = {
    "NO_SPLIT_INFO", "LICENCE_UNKNOWN", "LICENCE_UNRECOGNISED", "LABELS_UNKNOWN", "CATALOGUE_PER_MEMBER_REQUIRED",
    "REGISTRY_UNMAPPED_ID", "G13_EVIDENCE_MISSING", "G13_EVIDENCE_INVALID",
    "CANDIDATE_MALFORMED", "NON_ASCII_NAME", "UPSTREAM_OF_A61A_NEEDS_RULING",
}

# ----------------------------------------------------------------------------------------------------------
# A61(a) 8.5 HIT list: barred under any id or form. Keys are matched on normalised tokens (see _match_key).
# The first ten are the A61(a) record named in the task; sb6 is on the frozen manifest's excluded list.
# Aliases for md_* sources are derived from the abbreviations (over-blocking is the safe error).
# ----------------------------------------------------------------------------------------------------------
A61A_HITS = {
    "gsm8k": ["gsm8k", "grade school math", "gsm hard", "gsm plus", "gsm symbolic", "mgsm"],
    "hover": ["hover", "di hover"],
    "isarcasmeval": ["isarcasmeval", "isarcasm", "semeval 2022 task 6"],
    "tydiqa": ["tydiqa", "tydi qa", "tydi"],
    "md_fdc": ["md fdc", "mdfdc", "fdc", "fooddata central", "food data central"],
    "md_peps": ["md peps", "mdpeps", "peps", "politically exposed persons"],
    "di_ts_inputs": ["di ts", "dits", "di ts inputs"],
    # v3.2-r Sk 1: the three DI-TS member sources, barred BY NAME with every id and alias (HF id, GitHub id, short
    # name, tasksource-style task name). Keys are matched on tokens, so "-", "_", "/" and case do not matter.
    "di_ts_perspectrum": ["perspectrum", "cogcomp perspectrum"],
    "di_ts_logical_entailment": ["logical entailment", "logical entailment dataset", "deepmind logical entailment",
                                 "google deepmind logical entailment dataset", "deepmind logical", "logical entail"],
    "di_ts_temporal_expressions": ["temporal expressions", "temporal expressions evaluation",
                                   "temporal expressions evaluation lm", "temporal expressions lm", "temporal expr",
                                   "kunalkukreja", "kunalkukreja21", "kunalkukreja21 temporal expressions"],
    "md_worldbank": ["md worldbank", "mdworldbank", "worldbank", "world bank"],
    "md_usgs": ["md usgs", "mdusgs", "usgs", "us geological survey"],
    "md_cma": ["md cma", "mdcma", "cma", "cleveland museum of art"],
    "sb6": ["sb6"],
}
A61A_TASK_NAMES = ["gsm8k", "hover", "isarcasmeval", "tydiqa", "md_fdc", "md_peps", "di_ts_inputs",
                   "md_worldbank", "md_usgs", "md_cma"]
# The DI-TS group is the union of its own short names and its three member sources.
DI_TS_MEMBERS = ["di_ts_perspectrum", "di_ts_logical_entailment", "di_ts_temporal_expressions"]
DI_TS_MEMBER_IDS = ["CogComp/perspectrum", "google-deepmind/logical-entailment-dataset",
                    "kunalkukreja21/temporal-expressions-evaluation-lm"]
# Sentinel names (name-only probe rows) = the ten task names + SB6 + the DI-TS members.
A61A_SENTINEL_NAMES = A61A_TASK_NAMES + ["sb6"] + DI_TS_MEMBER_IDS

# S11 (skeptic): plan section 2 "Any source that is an upstream of a barred A61(a) source (e.g. HotpotQA for hover) needs
# an Opus 8.5 ruling first plus a transitive full-row G13". The tool cannot see upstreams a candidate does not declare,
# so the one upstream the plan names is denied by name until an Opus ruling edits this table (a code change re-opens
# the section 16.1 step 0 conformance gate).
A61A_UPSTREAMS_NEED_RULING = {"hotpotqa": ["hotpotqa", "hotpot qa"]}

# S12 (skeptic): defence in depth for the datasets the plan lists as EXCLUDED by A82 4 (social-platform posts, contest and
# exam statements) and A82 5 (no-LLM-data rule). Name bars only; they never release anything. A82 9 (English only, no
# vision) is checked from the declared `languages` / `modality` fields when present.
A82_EXCLUDED = {
    "A82-4 civil_comments": ["civil comments"],
    "A82-4 social_chemistry_101": ["social chemistry"],
    "A82-4 goemotions": ["goemotions", "go emotions"],
    "A82-4 measuring_hate_speech": ["measuring hate speech"],
    "A82-4 hatexplain": ["hatexplain"],
    "A82-4 arc": ["=arc", "ai2 arc", "arc challenge", "arc easy"],
    "A82-4 medmcqa": ["medmcqa", "med mcqa"],
    "A82-4 math": ["=math", "competition math", "hendrycks math"],
    "A82-4 aqua_rat": ["aqua rat", "=aqua"],
    "A82-4 mathqa": ["mathqa", "math qa"],
    "A82-4 codecontests": ["codecontests", "code contests"],
    "A82-4 apps": ["=apps", "codeparrot apps"],
    "A82-4 project_codenet": ["codenet", "code net"],
    "A82-4 codeflaws": ["codeflaws"],
    "A82-4 new_yorker_caption_contest": ["new yorker", "newyorker", "caption contest"],
    "A82-5 when2call": ["when2call"],
    "A82-5 wildguardmix": ["wildguardmix", "wildguard mix", "wildguardtrain", "wildguard train"],
    "A82-5 wildjailbreak": ["wildjailbreak", "wild jailbreak"],
    "A82 e-snli (duplicate SNLI labels)": ["esnli", "e snli"],
}

# ----------------------------------------------------------------------------------------------------------
# G13 registry key table: registry id -> match keys. "=x" means the whole name must equal x. Every id parsed from
# sections A, B, C, D, E, M of the registry must be a key here (an unmapped id refuses the run: registry drift
# must be looked at by a person). E65-E71 come from A61A_HITS. An empty list = "no dataset-level key" (internal
# held-out sets, row-level exclusions, groups).
# ----------------------------------------------------------------------------------------------------------
REGISTRY_KEYS = {
    # A: Tier 1 eval sets
    "A1": ["when2call"],
    "A2": ["agentdojo", "ad clean", "ad matched", "ad shift"],
    "A3": ["injecagent", "tb matched"],
    "A4": ["notinject"],
    "A5": ["atbench codex"],
    "A6": ["atbench"],
    # B: Tier 2 and report-only
    "B1": ["bfcl", "berkeley function calling"],
    "B2": ["mcp atlas"],
    "B3": ["cruxeval"],
    "B4": ["equibench"],
    "B5": ["agentprocessbench"],
    "B6": ["steerbench"],
    "B7": ["msb", "mcp security bench"],
    "B8": ["impossible livecodebench", "impossible swebench", "impossible swe bench", "impossiblebench"],
    "B9": ["wildguardtest", "wildguard test", "wildguardmix"],  # wildguardmix carries the WildGuardTest split
    "B10": ["saber"],
    "B11": ["swe bench live", "swe rebench"],
    "B12": ["jevbench"],
    "B13": ["jev decision index", "decision index tools"],
    # C: not reported but registered
    "C1": ["ampermbench"],
    "C2": ["r judge"],
    "C3": ["tracesafe"],
    "C4": ["tau2", "tau bench", "tau2 bench"],
    "C5": ["terminal bench"],
    "C6": ["swe bench"],
    "C7": ["authgatebench"],
    "C8": ["=trace"],
    "C9": ["underspecbench"],
    "C10": ["overeager", "over eager"],
    "C11": ["=care", "care split"],
    "C12": ["=core"],
    "C13": ["librispeech"],
    # D: upstream eval-environment exclusions
    "D1": ["agentdojo"], "D2": ["tau bench"], "D3": ["bipia"], "D4": ["injecagent"], "D5": ["agentdyn"],
    "D6": ["msb"], "D7": ["mcptox"], "D8": ["llmail inject"], "D9": ["notinject"], "D10": ["pids bench"],
    "D11": ["tensortrust", "tensor trust"], "D12": ["codeipi"], "D13": ["logjack"],
    "D14": ["tau2", "tau bench"], "D15": ["mcp atlas"], "D16": ["mcp bench"], "D17": ["mcp universe"],
    "D18": ["toolhop"], "D19": ["car bench"], "D20": ["agentprocessbench"],
    "D21": ["cruxeval"], "D22": ["livecodebench", "live code bench"], "D23": ["reval", "humaneval", "classeval"],
    "D24": ["codemind"], "D25": ["=core"], "D26": ["swe flux"], "D27": ["equibench"], "D28": ["cruxeval x"],
    "D29": ["impossible livecodebench", "impossible swebench", "impossible swe bench", "impossiblebench"],
    "D30": ["evilgenie"], "D31": ["ampermbench", "underspecbench"], "D32": ["steerbench"], "D33": ["credleakbench"],
    # M: internal held-out sets (ours; no public dataset name except the conditional V2-lite set)
    "M1": [], "M2": [], "M3": [], "M4": ["v2 lite"],
    # E: source bars
    "E1": ["cvefixes"], "E2": ["primevul"], "E3": ["bigvul"], "E4": ["morefixes"],
    "E5": ["atomic red team"], "E6": ["gtfobins"], "E7": ["nl2bash"], "E8": ["tldr pages"],
    "E9": [],  # human-written MCP server schemas: a content class, no dataset name
    "E10": ["when2call"], "E10b": ["xlam", "apigen"], "E11": ["codereviewer"], "E12": ["codereviewqa"],
    "E13": ["toucan"], "E14": ["nemotron tool calling"], "E15": ["nemotron rl ipi"], "E16": ["toolace"],
    "E17": ["acecode"], "E18": ["codescaler"], "E19": ["swe smith"], "E19b": ["swe smith"],
    "E20": ["r2e gym"], "E21": ["notinject"], "E22": ["authgatebench"], "E23": ["agentabstain"],
    "E24": ["toolmaze"], "E25": ["toolbench x"], "E26": ["nestools"], "E27": ["toolhop"], "E28": ["car bench"],
    "E29": ["clarifybench"], "E30": ["agentdog", "atbench"], "E31": ["stepguard"], "E32": ["dynaguard"],
    "E33": ["terminal wrench"], "E34": ["hacktrace"], "E35": ["ih challenge"], "E36": ["pids bench"],
    "E37": ["issuetrojanbench"], "E38": ["=wasp", "wasp bench"], "E39": ["tensortrust", "tensor trust"],
    "E40": ["mcptox"], "E41": ["=trace"], "E42": ["impossiblebench"], "E43": ["authgatebench"], "E44": ["=core"],
    "E45": ["jev", "jevbench"], "E46": ["agentdog"], "E47": ["openhands critic"], "E48": ["strands decider"],
    "E49": ["=horizon", "horizon guard"], "E50": ["promptguard", "prompt guard"], "E51": ["piguard"],
    "E52": [],  # "every other detector": a class, no dataset name
    "E52b": ["celeris", "d1 ultra", "microsoft decision 1", "clm 8b"],
    "E53": ["bashlex"], "E54": ["care code"], "E55": ["agenttrust"], "E56": ["trufflehog"],
    "E57": ["=hypothesis"], "E58": ["swe smith js"],
    "E59": ["chatterbox"], "E60": ["=piper"], "E61": ["f5 tts"], "E62": ["xtts"], "E63": ["espeak ng"],
    "E64": [],  # SWE-smith-py GPL/LGPL repos: row-level exclusion, no dataset name
    # E65-E71 are the A61(a) HIT list (built in); mapped below.
}
for _i, _n in zip(range(65, 72), ["gsm8k", "hover", "isarcasmeval", "tydiqa", "md_fdc", "md_peps", "di_ts_inputs"]):
    REGISTRY_KEYS["E%d" % _i] = list(A61A_HITS[_n])
REGISTRY_KEYS["E71"] = list(A61A_HITS["di_ts_inputs"]) + [k for _m in DI_TS_MEMBERS for k in A61A_HITS[_m]]

# Registry entries whose scope is a SET OF SPLITS of a larger dataset (not the whole dataset).
REGISTRY_SPLIT_SCOPE = {"C13": ["test-clean", "test-other"]}


def e_subclass(rid):
    m = re.match(r"^E(\d+)([a-z]?)$", rid)
    if not m:
        return None
    n = int(m.group(1))
    if rid in ("E10", "E10b", "E19b") or 13 <= n <= 36:
        return "LLM_GENERATED"
    if 1 <= n <= 12:
        return "REMOVED_OR_OUT"
    if 37 <= n <= 44:
        return "LICENCE_NOT_USABLE"
    if 45 <= n <= 52:
        return "COMPETITOR_OUTPUT"
    if 53 <= n <= 58:
        return "TOOL_LICENCE_BAR"
    if 59 <= n <= 64:
        return "VOICE_BAR"
    if 65 <= n <= 71:
        return "A61A_HIT"
    return "OTHER"


# ----------------------------------------------------------------------------------------------------------
# Name matching
# ----------------------------------------------------------------------------------------------------------
def _fold(s):
    """NFKD-fold a name (full-width forms, accents) and drop combining marks, then lowercase. Anything still non-ASCII
    afterwards is reported by _nonascii (a homoglyph spelling must not pass as a different name)."""
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch)).lower()


def _nonascii(s):
    return any(ord(ch) > 127 for ch in _fold(s))


def tokens(s):
    return re.findall(r"[a-z0-9]+", _fold(s))


def _name_forms(c_names):
    """All name strings to match: each given name, plus the part after an org/ prefix."""
    out = []
    for n in c_names:
        if not isinstance(n, str) or not n.strip():
            continue
        out.append(n)
        if "/" in n:
            out.append(n.rsplit("/", 1)[1])
    return out


def match_key(key, names):
    """True if the key matches any name. Plain key: contiguous token run; or compact equality with a window of
    up to 4 adjacent tokens (gsm8k = gsm-8k); or, for keys of 7+ characters, a substring of the compact name.
    '=x': the whole name (org prefix removed) must equal x."""
    exact = key.startswith("=")
    kt = tokens(key[1:] if exact else key)
    if not kt:
        return False
    kc = "".join(kt)
    for n in names:
        nt = tokens(n)
        if not nt:
            continue
        if exact:
            if "".join(nt) == kc:
                return True
            continue
        L = len(kt)
        for i in range(0, len(nt) - L + 1):
            if nt[i:i + L] == kt:
                return True
        for w in range(1, 5):
            for i in range(0, len(nt) - w + 1):
                if "".join(nt[i:i + w]) == kc:
                    return True
        if len(kc) >= 7 and kc in "".join(nt):
            return True
    return False


def match_any(keys, names):
    return [k for k in keys if match_key(k, names)]


# ----------------------------------------------------------------------------------------------------------
# Splits, licences, label provenance
# ----------------------------------------------------------------------------------------------------------
_EVAL_PREFIXES = ("test", "dev", "val", "eval", "heldout", "hidden", "private", "tst")
# S4 (skeptic): a joined single token such as trainval, traintest, traindev or holdout must not read as 'train'. Any
# token that CONTAINS one of these words makes the split 'eval' (over-blocking is the safe error).
_EVAL_WORDS = ("test", "dev", "val", "eval", "held", "hold", "hidden", "private", "tst", "blind", "secret", "sealed",
               "unseen")


def split_class(name):
    """'train' | 'eval' | 'unknown'. Mixed names such as train_val are 'eval' (fail-closed)."""
    toks = tokens(re.sub(r"\[.*?\]", "", name or ""))
    if not toks:
        return "unknown"
    if any(t.startswith(_EVAL_PREFIXES) or any(w in t for w in _EVAL_WORDS) for t in toks):
        return "eval"
    if toks[0].startswith(("train", "trn")):
        return "train"
    return "unknown"


# "sa" (share-alike) is NOT a bad token any more (A82 2: CC BY-SA allowed, disclosed). NC, ND, and the copyleft code
# licences stay barred; a share-alike term next to NC/ND is still caught by those tokens.
_LIC_BAD_TOKENS = {"nc", "nd", "gpl", "lgpl", "agpl", "mpl", "eupl", "sspl", "cpal", "osl", "epl", "cddl",
                   "noncommercial", "research", "academic", "restricted", "proprietary", "custom", "openrail",
                   "gated", "internal", "odbl"}
# compact (tokens joined) strings that are barred outright although no bad token appears
_LIC_BAD_COMPACT_PREFIXES = ("cdlasharing", "communitydatalicenseagreementsharing", "opendatabaselicense",
                             "nodistribution", "noderiv")
_LIC_ALLOWED_PLAIN = {
    "mit", "mitlicense", "mit0", "apache20", "apache2", "apachelicense20", "apachelicenseversion20", "bsd", "bsd2",
    "bsd3", "bsd2clause", "bsd3clause", "bsdlicense", "isc", "cc0", "cc010", "cc0universal", "ccby", "ccby20",
    "ccby25", "ccby30", "ccby40", "unlicense", "zlib",
    # A82 7: CDLA-Permissive-2.0 (and 1.0)
    "cdlapermissive10", "cdlapermissive20", "cdlapermissive1", "cdlapermissive2",
    "communitydatalicenseagreementpermissive10", "communitydatalicenseagreementpermissive20",
    # ODC-By (A82: allowed)
    "odcby", "odcby10", "odcbyv10", "odcattributionlicense", "odcattributionlicense10",
    "opendatacommonsattributionlicense", "opendatacommonsattributionlicense10",
    # US public domain / US Government work (A82: allowed); plain public domain / PDDL kept from v1
    "publicdomain", "pd", "pddl", "uspublicdomain", "publicdomainus", "usgovernmentwork", "usgovernmentworks",
    "usfederalgovernmentwork", "usfederalgovernmentworks", "publicdomainusgovernment", "uspd", "usgovpublicdomain",
}
# CC BY-SA (A82 2): allowed, share-alike disclosed. Versions 1.0 to 4.0 and unversioned.
_LIC_ALLOWED_SHARE_ALIKE = {"ccbysa", "ccbysa10", "ccbysa20", "ccbysa25", "ccbysa30", "ccbysa40",
                            "creativecommonsattributionsharealike", "creativecommonsattributionsharealike10",
                            "creativecommonsattributionsharealike20", "creativecommonsattributionsharealike25",
                            "creativecommonsattributionsharealike30", "creativecommonsattributionsharealike40"}
_LIC_ALLOWED = _LIC_ALLOWED_PLAIN | _LIC_ALLOWED_SHARE_ALIKE
_LIC_ABSENT = {"none", "nolicense", "nolicence", "notstated", "notfound", "nonestated", "allrightsreserved",
               "nolicensestated", "nolicencestated"}
_LIC_UNKNOWN = {"", "unknown", "unspecified", "tbd", "na", "other", "mixed", "varies", "varied", "pertask",
                "perrow", "various"}


def licence_flags(lic):
    """Disclosure flags for licences that pass: ['SHARE_ALIKE'] for each CC BY-SA entry (A82 2). Pure function of the
    licence string(s); a licence that fails check_licence still gets its flag (harmless: the record is a DENY)."""
    items = lic if isinstance(lic, list) else [lic]
    out = []
    for it in items:
        if isinstance(it, str) and "".join(tokens(it)) in _LIC_ALLOWED_SHARE_ALIKE and "SHARE_ALIKE" not in out:
            out.append("SHARE_ALIKE")
    return out


def check_licence(lic):
    """Returns a list of (code, detail). All licences in a list must pass."""
    if lic is None:
        return [("LICENCE_UNKNOWN", "licence not provided")]
    items = lic if isinstance(lic, list) else [lic]
    if not items:
        return [("LICENCE_UNKNOWN", "licence list is empty")]
    out = []
    for it in items:
        if not isinstance(it, str):
            out.append(("LICENCE_UNRECOGNISED", "licence entry is not a string"))
            continue
        toks = tokens(it)
        comp = "".join(toks)
        bad = [t for t in toks if t in _LIC_BAD_TOKENS]
        bad += [pfx for pfx in _LIC_BAD_COMPACT_PREFIXES if comp.startswith(pfx)]
        if "non" in toks and any(t.startswith("commercial") for t in toks):
            bad.append("non-commercial")
        if "no" in toks and any(t.startswith("deriv") for t in toks):
            bad.append("no-derivatives")
        if bad:
            out.append(("LICENCE_NOT_PERMISSIVE", "%r has non-permissive term(s): %s" % (it, ",".join(sorted(set(bad))))))
        elif comp in _LIC_ABSENT:
            out.append(("LICENCE_ABSENT", "%r: no licence stated by the owner (all rights reserved)" % it))
        elif comp in _LIC_UNKNOWN:
            out.append(("LICENCE_UNKNOWN", "%r: not a licence" % it))
        elif comp not in _LIC_ALLOWED:
            out.append(("LICENCE_UNRECOGNISED", "%r is not on the permissive list" % it))
    return out


_LLM_TOKENS = {"llm", "llms", "gpt", "chatgpt", "claude", "gemini", "mixtral", "llama", "qwen", "deepseek",
               "mistral", "gemma", "palm", "synthetic", "distilled", "distillation", "bootstrapped", "codestral",
               # S8 (skeptic): more model families and AI-assist wording (a human token no longer hides them)
               "sonnet", "opus", "haiku", "grok", "kimi", "glm", "chatglm", "phi", "cohere", "openai", "anthropic",
               "bard", "copilot", "vicuna", "alpaca", "falcon", "davinci", "instructgpt", "o1", "o3", "o4", "ai",
               "assisted", "augmented", "paraphrased", "rewritten", "translated", "gpt4", "gpt3", "gpt35", "gpt4o"}
_LLM_PHRASES = re.compile(r"(language model|model[- ]generated|machine[- ]generated|ai[- ]generated|"
                          r"auto(matically)?[- ]generated|generated by|self[- ]instruct|gpt[- ]?\d|llm[- ]?(written|labell?ed))")
_NONHUMAN_TOKENS = {"program", "programmatic", "heuristic", "heuristics", "rule", "rules", "weak", "distant",
                    "pseudo", "silver", "automatic", "automatically", "scripted", "templated", "classifier"}
_HUMAN_TOKENS = {"human", "humans", "crowd", "crowdsourced", "crowdworkers", "expert", "experts", "manual",
                 "manually", "annotators", "annotator", "annotated", "adjudicated"}
_ENUM = {"human": "H", "human_crowd": "H", "human_expert": "H", "llm_generated": "L", "mixed_human_llm": "L",
         "program": "N", "heuristic": "N", "model_labelled": "N", "unknown": "U"}


def _provenance_class(s):
    """'H' human only | 'L' LLM marker | 'N' non-human process (or human mixed with a non-human process) |
    'U' unknown or unrecognised."""
    if s is None:
        return "U"
    if not isinstance(s, str):
        return "U"
    low = s.strip().lower()
    if low in _ENUM:
        return _ENUM[low]
    toks = set(tokens(low))
    if toks & _LLM_TOKENS or _LLM_PHRASES.search(low):
        return "L"
    nh = bool(toks & _NONHUMAN_TOKENS)
    hu = bool(toks & _HUMAN_TOKENS)
    if nh:
        return "N"
    if hu:
        return "H"
    return "U"


def check_provenance(label_prov, text_prov):
    out = []
    lc = _provenance_class(label_prov)
    if lc == "L":
        out.append(("LABELS_LLM_GENERATED", "label provenance %r has an LLM or synthetic marker" % (label_prov,)))
    elif lc == "N":
        out.append(("LABELS_NOT_HUMAN", "label provenance %r is not purely human" % (label_prov,)))
    elif lc == "U":
        out.append(("LABELS_UNKNOWN", "label provenance %r not shown to be human" % (label_prov,)))
    if text_prov is not None:
        tc = _provenance_class(text_prov)
        if tc == "L":
            out.append(("TEXT_LLM_GENERATED", "text provenance %r has an LLM or synthetic marker" % (text_prov,)))
    mark = re.search(r"\bjev\b", " ".join(str(x).lower() for x in (label_prov, text_prov) if x))
    if mark:
        out.append(("COMPETITOR_OUTPUT", "provenance mentions Jev: competitor outputs are never data or labels"))
    return out


# ----------------------------------------------------------------------------------------------------------
# Registry loading
# ----------------------------------------------------------------------------------------------------------
_ROW = re.compile(r"^\|\s*([A-Z]\d+[a-z]?)\s*\|(.*)\|\s*$")
_HEAD = re.compile(r"^##\s+([A-Z])\.\s")
_REGISTRY_SECTIONS = "ABCDEM"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_registry(path):
    """Parse the G13 registry draft. Returns {"sha256", "entries": {id: {...}}, "unmapped": [ids]}.
    Only the id and the first two cells (name) are kept; no other text is carried."""
    if is_skipped_path(path):
        raise ValueError("REGISTRY_PATH_BARRED: path has an ohs/sealed component")
    entries, unmapped, sec = {}, [], None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            h = _HEAD.match(line)
            if h:
                sec = h.group(1)
                continue
            m = _ROW.match(line.rstrip("\n"))
            if not m or sec not in _REGISTRY_SECTIONS:
                continue
            rid = m.group(1)
            if rid[0] != sec:
                continue
            cells = [c.strip() for c in m.group(2).split("|")]
            if rid in entries:
                raise ValueError("REGISTRY_DUPLICATE_ID: %s" % rid)
            if sec == "E":
                kind = "SOURCE_BAR:" + str(e_subclass(rid))
            else:
                kind = "EVAL_TARGET"
            entries[rid] = {"id": rid, "section": sec, "kind": kind, "name": cells[0] if cells else "",
                            "keys": REGISTRY_KEYS.get(rid), "split_scope": REGISTRY_SPLIT_SCOPE.get(rid)}
            if rid not in REGISTRY_KEYS:
                unmapped.append(rid)
    return {"sha256": sha256_file(path), "entries": entries, "unmapped": unmapped, "path_basename": os.path.basename(path)}


# ----------------------------------------------------------------------------------------------------------
# Core evaluation
# ----------------------------------------------------------------------------------------------------------
def _reason(code, detail, ref=None):
    return {"code": code, "detail": detail, "ref": ref}


def _as_list(x):
    """S1 (skeptic): a bare string is ONE entry (never iterated per character); None is empty."""
    if x is None:
        return []
    if isinstance(x, (list, tuple)):
        return list(x)
    return [x]


def _cand_names(c):
    names = [c.get("name"), c.get("hf_id")] + _as_list(c.get("aliases"))
    return _name_forms([n for n in names if isinstance(n, str) and n.strip()])


def _upstream_names(up):
    """Name strings of one derived_from entry: a string, or a dict with name / hf_id / aliases (S1)."""
    if isinstance(up, str):
        return _name_forms([up]) if up.strip() else []
    if isinstance(up, dict):
        return _cand_names(up)
    return []


def _malformed_reasons(c):
    """S1, S2: wrong-typed or non-ASCII identity fields never silently drop out of the bar checks. Returns reasons."""
    out = []
    if not isinstance(c.get("name"), str) or not c["name"].strip():
        out.append(("CANDIDATE_MALFORMED", "name must be a non-empty string"))
    if c.get("hf_id") is not None and not isinstance(c["hf_id"], str):
        out.append(("CANDIDATE_MALFORMED", "hf_id must be a string"))
    if c.get("aliases") is not None and not isinstance(c["aliases"], (str, list)):
        out.append(("CANDIDATE_MALFORMED", "aliases must be a list of strings"))
    if c.get("derived_from") is not None and not isinstance(c["derived_from"], (str, list)):
        out.append(("CANDIDATE_MALFORMED", "derived_from must be a list of names"))
    idents = [c.get("name"), c.get("hf_id")] + _as_list(c.get("aliases"))
    for al in _as_list(c.get("aliases")):
        if not isinstance(al, str):
            out.append(("CANDIDATE_MALFORMED", "every alias must be a string"))
    for up in _as_list(c.get("derived_from")):
        if isinstance(up, dict):
            idents += [up.get("name"), up.get("hf_id")] + _as_list(up.get("aliases"))
        elif isinstance(up, str):
            idents.append(up)
        else:
            out.append(("CANDIDATE_MALFORMED", "every derived_from entry must be a string or an object with a name"))
    if any(isinstance(i, str) and _nonascii(i) for i in idents):
        out.append(("NON_ASCII_NAME", "a name, alias, hf_id or upstream has characters that do not fold to ASCII "
                    "(a homoglyph spelling must not pass as a different name); give the ASCII form"))
    return out


def _a61a_matches(names):
    return [h for h, keys in A61A_HITS.items() if match_any(keys, names)]


def load_denylist(path):
    if is_skipped_path(path):
        raise ValueError("DENYLIST_PATH_BARRED: path has an ohs/sealed component")
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, list):
        raise ValueError("DENYLIST_BAD_SHAPE: must be a JSON list")
    for e in obj:
        if not isinstance(e, dict) or not isinstance(e.get("keys"), list) or not e["keys"]:
            raise ValueError("DENYLIST_BAD_ENTRY: each entry needs a non-empty keys list")
    return {"sha256": sha256_file(path), "entries": obj}


# ----------------------------------------------------------------------------------------------------------
# G13 disjointness evidence for a split-scoped release (A82 1; v3.2-r Sk 2, Sk 3)
# ----------------------------------------------------------------------------------------------------------
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_MAX_RECORD_BYTES = 16 * 1024 * 1024


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def check_g13_evidence(cand, registry, requested):
    """Validate the candidate's G13 result record for a split-scoped release of the splits in `requested`.
    Returns (ok, reasons, evidence). reasons = list of (code, detail). Nothing in the record is printed except
    numbers, the path and shas (hit rows and matched text never appear here)."""
    ref = cand.get("g13_record")
    if ref is None:
        return False, [("G13_EVIDENCE_MISSING", "split-scoped release needs g13_record {path, sha256}: a G13 result "
                        "record over the FULL train split with 0 hits outside R6 scaffolding")], None
    if not (isinstance(ref, dict) and isinstance(ref.get("path"), str) and ref["path"]
            and isinstance(ref.get("sha256"), str) and _HEX64.match(ref["sha256"].lower())):
        return False, [("G13_EVIDENCE_INVALID", "g13_record must be {path: str, sha256: 64 hex}")], None
    path, want_sha = ref["path"], ref["sha256"].lower()
    if is_skipped_path(path):
        return False, [("G13_EVIDENCE_INVALID", "g13_record path has an ohs/sealed component: never opened")], None
    try:
        if not os.path.isfile(path):  # S9: never hash a device, pipe or directory
            return False, [("G13_EVIDENCE_INVALID", "g13_record is not a regular file")], None
        if os.path.getsize(path) > _MAX_RECORD_BYTES:
            return False, [("G13_EVIDENCE_INVALID", "g13_record file is larger than 16 MB")], None
        got_sha = sha256_file(path)
    except OSError as e:
        return False, [("G13_EVIDENCE_INVALID", "g13_record unreadable: %s" % e.__class__.__name__)], None
    if got_sha != want_sha:
        return False, [("G13_EVIDENCE_INVALID", "g13_record sha256 mismatch (given %s..., file %s...)"
                        % (want_sha[:12], got_sha[:12]))], None
    try:
        with open(path, "r", encoding="utf-8") as f:
            rec = json.load(f)
    except (OSError, ValueError) as e:
        return False, [("G13_EVIDENCE_INVALID", "g13_record is not valid JSON: %s" % e.__class__.__name__)], None
    if not isinstance(rec, dict):
        return False, [("G13_EVIDENCE_INVALID", "g13_record must be a JSON object")], None

    bad, bar = [], []
    if rec.get("kind") != "g13_result_record":
        bad.append('kind must be "g13_result_record"')
    # the record must be about THIS dataset
    ds = rec.get("dataset")
    if not isinstance(ds, str) or not ds.strip():
        bad.append("dataset missing")
    else:
        mine = {"".join(tokens(n)) for n in _cand_names(cand)} - {""}
        theirs = {"".join(tokens(n)) for n in _name_forms([ds])} - {""}
        if not mine & theirs:
            bad.append("record is for a different dataset (%r)" % ds)
    # current registry only (a stamp is current for its registry sha)
    rs = rec.get("registry_sha256")
    if not (isinstance(rs, str) and rs.lower() == registry["sha256"]):
        bad.append("registry_sha256 is not the loaded registry sha (stale or missing evidence)")
    if not (isinstance(rec.get("method_set_version"), str) and rec["method_set_version"].strip()):
        bad.append("method_set_version missing")
    if not (_is_int(rec.get("registry_entries")) and rec["registry_entries"] == len(registry["entries"])):
        bad.append("registry_entries must equal the number of registry ids loaded (%d)" % len(registry["entries"]))
    if rec.get("targets_all_registered") is not True:
        bad.append("targets_all_registered must be true (every registered test/dev item)")
    if rec.get("complete") is not True:
        bad.append("complete must be true")
    if not (_is_int(rec.get("rows_dropped_for_disjointness")) and rec["rows_dropped_for_disjointness"] == 0):
        bad.append("rows_dropped_for_disjointness must be 0 (the row-drop reading is not used in C2.1)")

    splits = rec.get("splits")
    declared = cand.get("train_split_rows")
    ev_splits = {}
    if not isinstance(splits, dict) or not splits:
        bad.append("splits missing")
    else:
        for sp in requested:
            if "[" in sp or "]" in sp:  # S5: a slice such as train[:1200] is a subset, never "the whole train split"
                bad.append("split %r is a slice; the whole train split must be requested by its plain name" % sp)
                continue
            e = splits.get(sp)
            if not isinstance(e, dict):
                bad.append("split %r not covered by the record" % sp)
                continue
            n_in, n_chk = e.get("rows_in_split"), e.get("rows_checked")
            if not (_is_int(n_in) and _is_int(n_chk) and n_in > 0):
                bad.append("split %r: rows_in_split and rows_checked must be positive integers" % sp)
                continue
            if n_chk != n_in:
                bad.append("split %r: rows_checked %d != rows_in_split %d (whole split required, never a subset)" % (sp, n_chk, n_in))
            if e.get("sampled") is not False:
                bad.append("split %r: sampled must be false" % sp)
            if e.get("row_cap") is not None:
                bad.append("split %r: row_cap must be null (no cap)" % sp)
            h, ho = e.get("hits"), e.get("hits_outside_r6_scaffolding")
            if not (_is_int(h) and _is_int(ho) and 0 <= ho <= h):
                bad.append("split %r: hits and hits_outside_r6_scaffolding must be integers with outside <= hits" % sp)
            elif ho != 0:
                bar.append("split %r: %d G13 hit(s) outside R6 scaffolding" % (sp, ho))
            # full-split size must come from the dataset card, so a self-consistent capped record cannot pass
            if isinstance(declared, dict):
                dn = declared.get(sp)
            else:
                dn = declared if len(requested) == 1 else None
            if not (_is_int(dn) and dn > 0):
                bad.append("split %r: candidate must declare its full size in train_split_rows (from the card)" % sp)
            elif dn != n_in:
                bad.append("split %r: record rows_in_split %d != declared full train split %d" % (sp, n_in, dn))
            ev_splits[sp] = {"rows_in_split": n_in, "rows_checked": n_chk, "hits": h, "hits_outside_r6_scaffolding": ho}
    reasons = [("G13_EVIDENCE_INVALID", b) for b in bad] + [("G13_HITS_OUTSIDE_SCAFFOLDING", b) for b in bar]
    if reasons:
        return False, reasons, None
    return True, [], {"path": path, "sha256": got_sha, "registry_sha256": registry["sha256"],
                      "method_set_version": rec["method_set_version"], "splits": ev_splits}


def evaluate(cand, registry, denylist=None, split_scoped_release=False, _depth=0):
    """One record for one candidate. registry from load_registry (must have no unmapped ids)."""
    reasons, notes = [], []
    if not isinstance(cand, dict):
        return {"name": None, "kind": None, "decision": "DENY", "deny_class": "INSUFFICIENT_EVIDENCE",
                "reason_codes": ["CANDIDATE_MALFORMED"],
                "reasons": [_reason("CANDIDATE_MALFORMED", "candidate is not a JSON object")], "notes": [],
                "allowed_splits": [], "requested_splits_defaulted": False,
                "input": {"splits_available": [], "splits_requested": [], "licence": None, "label_provenance": None,
                          "text_provenance": None, "derived_from": []}}
    for code, detail in _malformed_reasons(cand):
        reasons.append(_reason(code, detail))
    names = _cand_names(cand)
    # S3: only "dataset" and "catalogue" are kinds. A spelling variant (catalog, collection, ...) or ANY members list is
    # treated as a catalogue, so members are never skipped; an unknown kind word is also a reason of its own.
    kind_raw = cand.get("kind")
    kind_norm = kind_raw.strip().lower() if isinstance(kind_raw, str) else kind_raw
    if kind_norm in (None, "", "dataset"):
        kind = "dataset"
    elif kind_norm in ("catalogue", "catalog"):
        kind = "catalogue"
    else:
        kind = "catalogue"
        reasons.append(_reason("CANDIDATE_MALFORMED", "kind %r is neither 'dataset' nor 'catalogue'" % (kind_raw,)))
    if kind == "dataset" and cand.get("members"):
        kind = "catalogue"
        notes.append("candidate lists members, so it is treated as a catalogue (never a source as a whole)")

    # --- A61(a) HITs, any id or form ------------------------------------------------------------------
    hits = _a61a_matches(names)
    for h in hits:
        reasons.append(_reason("A61A_HIT", "matches the recorded A61(a) 8.5 HIT source %s (barred under any id or form)" % h, h))
    for tag, keys in A61A_UPSTREAMS_NEED_RULING.items():
        if match_any(keys, names):
            reasons.append(_reason("UPSTREAM_OF_A61A_NEEDS_RULING",
                                   "%s is an upstream of a barred A61(a) source: needs an Opus 8.5 ruling plus a "
                                   "transitive full-row G13 first (plan section 2)" % tag, tag))
    for tag, keys in A82_EXCLUDED.items():
        if match_any(keys, names):
            reasons.append(_reason("A82_EXCLUDED", "%s: excluded by owner ruling A82 (plan 16.3 EXCLUDED list)" % tag, tag))
    langs = [str(x).strip().lower() for x in _as_list(cand.get("languages"))]
    if any(not (l == "en" or l.startswith("en-") or l.startswith("en_") or l in ("eng", "english")) for l in langs):
        reasons.append(_reason("NON_ENGLISH_DECLARED", "A82 9: English only; declared languages %s" % langs))
    mods = [str(x).strip().lower() for x in _as_list(cand.get("modality", cand.get("modalities")))]
    if any(m not in ("text", "txt") for m in mods):
        reasons.append(_reason("NON_TEXT_DECLARED", "A82 9: text only (no vision or audio); declared modality %s" % mods))

    # --- registry: eval targets and source bars --------------------------------------------------------
    def registry_hits(nms):
        out = []
        for rid, e in registry["entries"].items():
            ks = e["keys"] or []
            m = match_any(ks, nms)
            if m:
                out.append((rid, e, m))
        return out

    # split classes (needed for the split-scoped registry rule)
    avail = [s for s in (cand.get("splits_available") or []) if isinstance(s, str)]
    requested = cand.get("splits_requested")
    requested_defaulted = requested is None
    if requested is None:
        requested = [s for s in avail if split_class(s) == "train"]
    requested = [s for s in requested if isinstance(s, str)]

    released, evidence, evidence_cache = False, None, [None]
    for rid, e, m in registry_hits(names):
        if e["kind"] == "SOURCE_BAR:A61A_HIT":
            continue  # reported once as A61A_HIT
        if e["kind"].startswith("SOURCE_BAR"):
            sub = e["kind"].split(":", 1)[1]
            reasons.append(_reason("REGISTRY_SOURCE_BAR", "registry %s (%s): %s" % (rid, sub, e["name"]), rid))
            if sub == "COMPETITOR_OUTPUT":
                reasons.append(_reason("COMPETITOR_OUTPUT", "registry %s: competitor output is never data" % rid, rid))
        elif e["split_scope"]:
            scope = e["split_scope"]
            structural = bool(split_scoped_release and avail and requested
                              and all(split_class(s) == "train" for s in requested)
                              and not set(tokens_join(s) for s in requested) & set(tokens_join(s) for s in scope))
            ev_ok = False
            if structural:
                if evidence_cache[0] is None:
                    evidence_cache[0] = check_g13_evidence(cand, registry, requested)
                ev_ok, ev_reasons, ev_block = evidence_cache[0]
            if structural and ev_ok:
                released = True
                evidence = ev_block
                notes.append("registry %s is scoped to splits %s only; requested train splits do not intersect and the "
                             "G13 result record shows the FULL train split disjoint (released by --split-scoped-release)"
                             % (rid, scope))
            else:
                reasons.append(_reason("REGISTRY_EVAL_TARGET_SPLIT_SCOPED",
                                       "registry %s targets splits %s of this dataset (%s); %s"
                                       % (rid, scope, e["name"],
                                          "release needs valid G13 evidence over the full train split" if structural
                                          else "default strict mode denies the dataset"), rid))
                if structural:
                    for code, detail in ev_reasons:
                        if not any(r["code"] == code and r["detail"] == detail for r in reasons):
                            reasons.append(_reason(code, detail, rid))
        else:
            reasons.append(_reason("REGISTRY_EVAL_TARGET", "registry %s is this eval set or an upstream of it: %s" % (rid, e["name"]), rid))

    # --- derived_from upstreams ------------------------------------------------------------------------
    for up in _as_list(cand.get("derived_from")):
        un = _upstream_names(up)
        upl = up if isinstance(up, str) else (up.get("name") if isinstance(up, dict) else None)
        for h in _a61a_matches(un):
            reasons.append(_reason("UPSTREAM_A61A_HIT", "derived from %r, an A61(a) HIT source (%s)" % (upl, h), h))
        for tag, keys in A61A_UPSTREAMS_NEED_RULING.items():
            if match_any(keys, un):
                reasons.append(_reason("UPSTREAM_OF_A61A_NEEDS_RULING",
                                       "derived from %r = %s, an upstream of a barred A61(a) source: Opus 8.5 ruling + "
                                       "transitive full-row G13 first" % (upl, tag), tag))
        for tag, keys in A82_EXCLUDED.items():
            if match_any(keys, un):
                reasons.append(_reason("A82_EXCLUDED", "derived from %r = %s, excluded by owner ruling A82" % (upl, tag), tag))
        for rid, e, m in registry_hits(un):
            if e["kind"] == "SOURCE_BAR:A61A_HIT":
                continue
            reasons.append(_reason("UPSTREAM_BARRED", "derived from %r = registry %s (%s)" % (upl, rid, e["kind"]), rid))

    # --- split-aware deny-list --------------------------------------------------------------------------
    if denylist:
        for e in denylist["entries"]:
            if not match_any(e["keys"], names):
                continue
            ref = e.get("ref") or e.get("name") or "denylist"
            ts = e.get("tainted_splits")
            if hits:
                continue  # an A61(a) HIT is never released by split-awareness
            if ts is None or (isinstance(ts, list) and ("*" in ts or not ts)):
                reasons.append(_reason("DENYLIST_SPLIT_BLIND", "deny-list entry %s names no splits (taints the whole dataset)" % ref, ref))
            else:
                trainish = [s for s in ts if split_class(s) != "eval"]
                if trainish:
                    reasons.append(_reason("DENYLIST_TAINTED_TRAIN_SPLIT",
                                           "deny-list entry %s taints non-test/dev split(s) %s" % (ref, trainish), ref))
                else:
                    # S7: A82 1 releases a train split only on a G13 result record over the FULL train split. A deny-list
                    # entry for test/dev splits is a registered test/dev target, so it takes the same path (flag + record).
                    structural = bool(split_scoped_release and avail and requested
                                      and all(split_class(s) == "train" for s in requested)
                                      and not set(tokens_join(s) for s in requested) & set(tokens_join(s) for s in ts))
                    ev_ok = False
                    if structural:
                        if evidence_cache[0] is None:
                            evidence_cache[0] = check_g13_evidence(cand, registry, requested)
                        ev_ok, ev_reasons, ev_block = evidence_cache[0]
                    if structural and ev_ok:
                        released = True
                        evidence = ev_block
                        notes.append("SPLIT_AWARE_RELEASE: deny-list entry %s taints only test/dev split(s) %s; the G13 "
                                     "result record shows the FULL train split disjoint" % (ref, ts))
                    else:
                        reasons.append(_reason("DENYLIST_TEST_ONLY_SPLIT_SCOPED",
                                               "deny-list entry %s taints test/dev split(s) %s; %s" % (ref, ts,
                                               "release needs valid G13 evidence over the full train split" if structural
                                               else "release needs --split-scoped-release, train-only requested splits and "
                                                    "a G13 result record"), ref))
                        if structural:
                            for code, detail in ev_reasons:
                                if not any(r["code"] == code and r["detail"] == detail for r in reasons):
                                    reasons.append(_reason(code, detail, ref))

    # --- splits ------------------------------------------------------------------------------------------
    if not avail:
        reasons.append(_reason("NO_SPLIT_INFO", "splits_available not provided"))
    else:
        if not any(split_class(s) == "train" for s in avail):
            reasons.append(_reason("NO_TRAIN_SPLIT", "no train-like split among %s" % avail))
        for s in requested:
            if s not in avail:
                reasons.append(_reason("REQUESTED_SPLIT_NOT_AVAILABLE", "requested split %r not in splits_available" % s))
            if split_class(s) != "train":
                reasons.append(_reason("REQUESTED_SPLIT_NOT_TRAIN", "requested split %r is not a train split" % s))
        if not requested and any(split_class(s) == "train" for s in avail):
            reasons.append(_reason("REQUESTED_SPLIT_NOT_TRAIN", "no splits requested"))
    ets = [s for s in (cand.get("eval_target_splits") or []) if isinstance(s, str)]
    if ets:
        reasons.append(_reason("EVAL_TARGET_SPLIT_DECLARED", "candidate declares eval-target split(s) %s" % ets))

    # --- licence and provenance ---------------------------------------------------------------------------
    for code, detail in check_licence(cand.get("licence")):
        reasons.append(_reason(code, detail))
    for code, detail in check_provenance(cand.get("label_provenance"), cand.get("text_provenance")):
        reasons.append(_reason(code, detail))

    # --- catalogue / members --------------------------------------------------------------------------------
    members = []
    if kind == "catalogue":
        reasons.append(_reason("CATALOGUE_PER_MEMBER_REQUIRED",
                               "a catalogue is never a source as a whole; each member needs its own record and name"))
        if _depth < 3:
            for m in _as_list(cand.get("members")):
                members.append(evaluate(m, registry, denylist, split_scoped_release, _depth + 1))

    codes = {r["code"] for r in reasons}
    decision = "DENY" if reasons else "ALLOW"
    deny_class = None
    if reasons:
        deny_class = "BAR" if codes & BAR_CODES else "INSUFFICIENT_EVIDENCE"
    allowed_splits = [s for s in requested if split_class(s) == "train"] if decision == "ALLOW" else []
    rec = {
        "name": cand.get("name"),
        "kind": kind,
        "decision": decision,
        "deny_class": deny_class,
        "reason_codes": sorted(codes),
        "reasons": reasons,
        "notes": notes,
        "allowed_splits": allowed_splits,
        "requested_splits_defaulted": requested_defaulted,
        "input": {"splits_available": avail, "splits_requested": requested, "licence": cand.get("licence"),
                  "label_provenance": cand.get("label_provenance"), "text_provenance": cand.get("text_provenance"),
                  "derived_from": cand.get("derived_from") or []},
    }
    sa = licence_flags(cand.get("licence"))
    if sa:
        rec["share_alike_disclosure"] = True
        notes.append("SHARE_ALIKE: CC BY-SA licence is allowed (A82 2) and must be disclosed; rows from this dataset "
                     "carry the share-alike flag")
    if decision == "ALLOW" and released:
        rec["train_split_seen"] = True
        rec["g13_evidence"] = evidence
    if decision == "ALLOW":
        rec["allow_means"] = ("not barred by A61(b) only; still needs the pre-mapper 8.5 PASS, the guards, the "
                              "check-at-creation G13 stamp on every row and a name on a re-frozen manifest before any "
                              "mapper or row")
    if members:
        rec["members"] = members
    return rec


def tokens_join(s):
    return "".join(tokens(s))


def evaluate_all(cands, registry, denylist=None, split_scoped_release=False):
    if registry["unmapped"]:
        raise ValueError("REGISTRY_UNMAPPED_ID: registry ids with no key entry: %s" % ",".join(registry["unmapped"]))
    return [evaluate(c, registry, denylist, split_scoped_release) for c in cands]


def counts(records):
    c = {"total": len(records), "ALLOW": 0, "DENY": 0, "BAR": 0, "INSUFFICIENT_EVIDENCE": 0, "by_reason": {}}
    for r in records:
        c[r["decision"]] += 1
        if r["deny_class"]:
            c[r["deny_class"]] += 1
        for code in r["reason_codes"]:
            c["by_reason"][code] = c["by_reason"].get(code, 0) + 1
    return c


# ----------------------------------------------------------------------------------------------------------
# R5 manifest adapter (names-only manifest v1)
# ----------------------------------------------------------------------------------------------------------
def r5_candidates_from_manifest(manifest_path):
    """Read r5_candidate_datasets from the frozen names-only manifest. Names and the manifest's own 'use' text
    are the only inputs: no licence, no label provenance and no splits exist there, so those stay None."""
    if is_skipped_path(manifest_path):
        raise ValueError("MANIFEST_PATH_BARRED: path has an ohs/sealed component")
    with open(manifest_path, "r", encoding="utf-8") as f:
        man = json.load(f)
    r5 = man.get("r5_candidate_datasets")
    if not isinstance(r5, dict):
        raise ValueError("MANIFEST_NO_R5: r5_candidate_datasets missing")
    cands, excluded = [], []
    for c in r5.get("candidates", []):
        d = {"name": c["name"], "kind": "catalogue" if "catalogue" in str(c.get("kind", "")) or "group" in str(c.get("kind", "")) else "dataset",
             "source": "manifest.r5_candidate_datasets.candidates", "manifest_status": c.get("status"),
             "manifest_kind": c.get("kind"), "manifest_use": c.get("use")}
        if "TRAIN" in str(c.get("use", "")) + c["name"]:
            d["splits_requested"] = ["train"]
        cands.append(d)
    for n in (r5.get("excluded_even_if_R5_adopted") or {}).get("names", []):
        excluded.append({"name": n, "kind": "dataset", "source": "manifest.r5_candidate_datasets.excluded_even_if_R5_adopted.names"})
    return {"manifest_sha256": sha256_file(manifest_path), "manifest_frozen": man.get("frozen"),
            "manifest_version": man.get("version"), "candidates": cands, "excluded": excluded}


def a61a_sentinels(covered_records):
    """One name-only sentinel per A61(a) task name that no manifest-excluded entry already covers."""
    out = []
    for h in A61A_SENTINEL_NAMES:
        want = set(_a61a_matches(_name_forms([h])))
        if not any(want <= set(_a61a_matches(_name_forms([r["name"]]))) for r in covered_records):
            out.append({"name": h, "kind": "dataset", "source": "A61(a) record named in the task (sentinel; not in the manifest excluded list)"})
    return out


# ----------------------------------------------------------------------------------------------------------
# Markdown rendering
# ----------------------------------------------------------------------------------------------------------
def render_markdown(result):
    L = []
    L.append("| # | Name | Source | Decision | Class | Reason codes |")
    L.append("|---|---|---|---|---|---|")
    for i, r in enumerate(result["records"], 1):
        L.append("| %d | %s | %s | %s | %s | %s |" % (i, str(r["name"]).replace("|", "/"), r.get("source_label", ""), r["decision"],
                                                      r["deny_class"] or "-", ", ".join(r["reason_codes"]) or "-"))
    L.append("")
    for i, r in enumerate(result["records"], 1):
        L.append("### %d. %s: %s" % (i, r["name"], r["decision"]))
        for x in r["reasons"]:
            L.append("- %s: %s" % (x["code"], x["detail"]))
        for n in r["notes"]:
            L.append("- note: %s" % n)
        if r["decision"] == "ALLOW":
            L.append("- allowed splits: %s. %s" % (r["allowed_splits"], r["allow_means"]))
        L.append("")
    return "\n".join(L)


# ----------------------------------------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--registry", required=True, help="G13 target registry markdown")
    ap.add_argument("--denylist", help="optional split-aware deny-list JSON")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--candidates", help="JSON list of candidate objects")
    g.add_argument("--r5-manifest", help="names-only manifest; checks r5_candidate_datasets (+ excluded names)")
    ap.add_argument("--a61a-sentinels", action="store_true", help="with --r5-manifest: add name-only sentinels for A61(a) names the manifest does not list")
    ap.add_argument("--split-scoped-release", action="store_true",
                    help="NOT the default: release the train split of a dataset whose registry entry targets only named test splits")
    ap.add_argument("--out", required=True, help="records JSON to write")
    a = ap.parse_args(argv)
    for p in (a.registry, a.denylist, a.candidates, a.r5_manifest, a.out):
        if p and is_skipped_path(p):
            print("REFUSED: path has an ohs/sealed component", file=sys.stderr)
            return 2
    try:
        registry = load_registry(a.registry)
        denylist = load_denylist(a.denylist) if a.denylist else None
        meta = {}
        if a.r5_manifest:
            m = r5_candidates_from_manifest(a.r5_manifest)
            cands = [dict(c, source_label="R5 candidate") for c in m["candidates"]]
            ex = [dict(c, source_label="manifest excluded name") for c in m["excluded"]]
            cands += ex
            if a.a61a_sentinels:
                cands += [dict(c, source_label="A61(a) sentinel") for c in a61a_sentinels(ex)]
            meta = {"manifest_sha256": m["manifest_sha256"], "manifest_frozen": m["manifest_frozen"], "manifest_version": m["manifest_version"]}
        else:
            with open(a.candidates, "r", encoding="utf-8") as f:
                cands = json.load(f)
            if not isinstance(cands, list):
                raise ValueError("CANDIDATES_BAD_SHAPE: must be a JSON list")
            meta = {"candidates_sha256": sha256_file(a.candidates)}
        recs = evaluate_all(cands, registry, denylist, a.split_scoped_release)
        for r, c in zip(recs, cands):
            r["source_label"] = c.get("source_label", "") if isinstance(c, dict) else ""
    except (ValueError, OSError, KeyError, AttributeError, TypeError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    result = {"tool": TOOL_VERSION, "tool_sha256": sha256_file(os.path.abspath(__file__)),
              "registry_sha256": registry["sha256"], "registry_ids": len(registry["entries"]),
              "denylist_sha256": denylist["sha256"] if denylist else None,
              "split_scoped_release": a.split_scoped_release, "inputs": meta, "counts": counts(recs), "records": recs}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, sort_keys=True)
    c = result["counts"]
    print("records=%d ALLOW=%d DENY=%d (BAR=%d INSUFFICIENT_EVIDENCE=%d) registry_sha=%s" % (
        c["total"], c["ALLOW"], c["DENY"], c["BAR"], c["INSUFFICIENT_EVIDENCE"], registry["sha256"][:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
