#!/usr/bin/env python3
"""A75 (a): build data/c2_never_train_manifest.json, the never-train manifest that A42-D 13.1 / 13.3 requires and that
mix_c2 --final refuses without (--never-train-manifest). CPU only, no network, no model.

SOURCE OF THE LISTS (ONLY these; PREREG_FINAL.md line numbers at the time of A75):
  * A40 (a) never-train additions, lines 2132-2139: 22 entries (20 Hugging Face ids, plus the angular/angular and vitejs/vite
    commit histories on line 2138).
  * A42-D 13.3 public anchors, lines 2738-2747: 13 entries (gating: BFCL V4 selection + irrelevance, InjecAgent, NotInject,
    R-Judge, CRUXEval-O MCQ, EquiBench Python, When2Call; exploratory: AgentProcessBench, ATBench-Codex, ACPBench,
    CodeJudgeBench, LiveCodeBench, SWE-bench Verified).
Nothing else is added. Before writing, the tool re-reads PREREG_FINAL.md and refuses (exit 2, nothing written) unless each
entry's quoted PREREG text is on its stated line(s). Names = the PREREG name, its separator/case variants, and (for a few) the
aliases the deny-list uses (data/c_parts/denylist.json, checked present at build time) plus the shorthand forms the A75 task
quotes. Every alias must contain its entry's core token (so a name that PREREG does not list cannot slip in).

ANCHOR FILES: path + sha256 only for an anchor file that exists outside never-open paths. The candidates are listed below
(found by a name search of the jev tree that skips every never-open path); a candidate whose path has any never-open part is
refused, a missing one is skipped. bench/external_quarantine (the DI quarantine) is never touched here: g13_di/di_never_train.json
already carries it and mix_c2.merge_di_never_train merges it in on top.

OUTPUT FORMAT (mix_c2.load_never_train): a json with "names" (strings, lower case) and "anchors" (dicts with "name", "path",
"sha256"); the other keys (entries, spec, counts) are information only. No timestamps: the same inputs give the same bytes.

Usage (from lean/c2_build):  ../../.venv/bin/python -B meta_src/build_never_train.py [--dry] [--force] [--out FILE]
Prints counts and shas only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
LEAN = BUILD.parent
PREREG = LEAN / "PREREG_FINAL.md"
DENYLIST = LEAN / "data" / "c_parts" / "denylist.json"
OUT = LEAN / "data" / "c2_never_train_manifest.json"

NEVER_OPEN_PARTS = ("ohs", "sealed", "external_quarantine", "longbench_v2", "preread", "sealed_brief", ".claude", "kwfind", "kwruns")

# ------------------------------------------------------------------------------------------------ the adopted lists
# (id, list, (first line, last line) in PREREG_FINAL.md, quoted text, hf id or None, cores, extra aliases, deny-list aliases)
# `extra` = shorthand/variant forms beyond the generated separator variants; `dl` = aliases the deny-list uses for the entry
# (verified in data/c_parts/denylist.json at build time).
A40, D133 = "A40 (a)", "A42-D 13.3"
E = []


def add(id_, lst, lines, text, hf, cores, extra=(), dl=()):
    E.append(dict(id=id_, list=lst, lines=lines, text=text, hf=hf, cores=tuple(cores), extra=tuple(extra), dl=tuple(dl)))


add("A40a-01", A40, (2132, 2132), "deepset/prompt-injections", "deepset/prompt-injections", ["promptinjections"])
add("A40a-02", A40, (2132, 2132), "jackhhao/jailbreak-classification", "jackhhao/jailbreak-classification", ["jailbreakclassification"])
add("A40a-03", A40, (2132, 2132), "reshabhs/SPML_Chatbot_Prompt_Injection", "reshabhs/SPML_Chatbot_Prompt_Injection", ["spml"],
    dl=["spml"])
add("A40a-04", A40, (2133, 2133), "djapp18/JailbreaksOverTime", "djapp18/JailbreaksOverTime", ["jailbreaksovertime"],
    extra=["jailbreaks over time", "jailbreaks-over-time", "jailbreaks_over_time"])
add("A40a-05", A40, (2134, 2134), "mmathys/openai-moderation-api-evaluation", "mmathys/openai-moderation-api-evaluation", ["openaimoderation"],
    extra=["openai-moderation", "openai_moderation", "openai moderation"])
add("A40a-06", A40, (2134, 2134), "nvidia/Aegis-AI-Content-Safety-Dataset-2.0", "nvidia/Aegis-AI-Content-Safety-Dataset-2.0", ["aegis"],
    extra=["aegis2", "aegis2.0", "aegis-2.0", "aegis_2.0", "aegis 2.0", "aegis-2", "aegis_2", "aegis 2"], dl=["aegis 2.0 responses"])
add("A40a-07", A40, (2135, 2135), "gretelai/gretel-pii-masking-en-v1", "gretelai/gretel-pii-masking-en-v1", ["gretel"],
    extra=["gretel-pii", "gretel_pii", "gretel pii"])
add("A40a-08", A40, (2135, 2135), "beki/privy", "beki/privy", ["privy"])
add("A40a-09", A40, (2135, 2135), "nvidia/Nemotron-PII", "nvidia/Nemotron-PII", ["nemotronpii"])
add("A40a-10", A40, (2136, 2136), "pminervini/HaluEval", "pminervini/HaluEval", ["halueval"], extra=["halu-eval", "halu_eval", "halu eval"],
    dl=["halueval"])
add("A40a-11", A40, (2136, 2136), "clinc/clinc_oos", "clinc/clinc_oos", ["clinc"],
    extra=["clinc150", "clinc 150", "clinc_150", "clinc-150", "clinc oos"], dl=["clinc150", "clinc 150", "clinc oos", "clinc_oos"])
add("A40a-12", A40, (2136, 2136), "mteb/amazon_massive_intent", "mteb/amazon_massive_intent", ["massive"],
    extra=["massive", "amazon massive", "amazon_massive", "amazon-massive", "amazonscience/massive"],
    dl=["massive", "amazon massive", "amazonscience/massive"])
add("A40a-13", A40, (2136, 2136), "benayas/snips", "benayas/snips", ["snips"],
    extra=["snips built in intents", "snips_built_in_intents"], dl=["snips", "snips built in intents", "snips_built_in_intents"])
add("A40a-14", A40, (2136, 2136), "legacy-datasets/banking77", "legacy-datasets/banking77", ["banking77"],
    extra=["banking 77", "banking_77", "banking-77"], dl=["banking77", "banking 77"])
add("A40a-15", A40, (2137, 2137), "gorilla-llm/Berkeley-Function-Calling-Leaderboard", "gorilla-llm/Berkeley-Function-Calling-Leaderboard",
    ["bfcl", "berkeleyfunctioncalling"], extra=["bfcl"], dl=["bfcl", "berkeley function calling leaderboard"])
add("A40a-16", A40, (2137, 2137), "BEE-spoke-data/consumer-finance-complaints", "BEE-spoke-data/consumer-finance-complaints",
    ["consumerfinancecomplaints"], dl=["consumer finance complaints"])
add("A40a-17", A40, (2138, 2138), "angular/angular", None, ["angularangular"],
    extra=["angular/angular", "angular_angular", "angular-angular"])
add("A40a-18", A40, (2138, 2138), "vitejs/vite", None, ["vitejsvite"], extra=["vitejs/vite", "vitejs_vite", "vitejs-vite"])
add("A40a-19", A40, (2138, 2138), "tasksource/esci", "tasksource/esci", ["esci"],
    extra=["esci", "amazon esci", "amazon_esci", "amazon-esci"], dl=["esci", "amazon esci"])
add("A40a-20", A40, (2139, 2139), "LocalLLaMA/typed-decisions", "LocalLLaMA/typed-decisions", ["typeddecisions"])
add("A40a-21", A40, (2139, 2139), "AndeyTait/JevForge-Mind2Web", "AndeyTait/JevForge-Mind2Web", ["jevforgemind2web"])
add("A40a-22", A40, (2139, 2139), "Praveenrajus/jev-bench", "Praveenrajus/jev-bench", ["jevbench"], extra=["jevbench", "jev bench"],
    dl=["jevbench", "jev bench"])

add("D133-01", D133, (2738, 2739), "BFCL V4 selection + irrelevance", None, ["bfcl", "berkeleyfunctioncalling"],
    extra=["bfcl", "bfcl v4", "bfcl_v4", "bfcl-v4", "bfcl-eval", "bfcl_eval", "bfcl v4 selection", "bfcl_v4_selection", "bfcl-v4-selection",
           "bfcl v4 irrelevance", "bfcl_v4_irrelevance", "bfcl-v4-irrelevance", "berkeley function calling leaderboard",
           "berkeley-function-calling-leaderboard", "gorilla-llm/berkeley-function-calling-leaderboard"],
    dl=["bfcl", "berkeley function calling leaderboard"])
add("D133-02", D133, (2740, 2740), "InjecAgent", None, ["injecagent"], extra=["injecagent", "injec agent", "injec_agent", "injec-agent"])
add("D133-03", D133, (2740, 2740), "NotInject", None, ["notinject"], extra=["notinject", "not inject", "not_inject", "not-inject"])
add("D133-04", D133, (2741, 2741), "R-Judge", None, ["rjudge"], extra=["r-judge", "r_judge", "rjudge", "r judge"])
add("D133-05", D133, (2742, 2742), "CRUXEval-O as MCQ", None, ["cruxeval"],
    extra=["cruxeval", "cruxeval-o", "cruxeval_o", "cruxeval o", "cruxeval-o mcq", "cruxeval_o_mcq", "cruxeval-o as mcq"], dl=["cruxeval"])
add("D133-06", D133, (2743, 2743), "EquiBench Python", None, ["equibench"],
    extra=["equibench", "equibench python", "equibench_python", "equibench-python"])
add("D133-07", D133, (2744, 2745), "When2Call test", None, ["when2call"],
    extra=["when2call", "when2call test", "when2call_test", "when2call-test"], dl=["when2call"])
add("D133-08", D133, (2746, 2746), "AgentProcessBench", None, ["agentprocessbench"],
    extra=["agentprocessbench", "agent process bench", "agent_process_bench", "agent-process-bench"])
add("D133-09", D133, (2746, 2746), "ATBench-Codex", None, ["atbench"],
    extra=["atbench", "atbench-codex", "atbench_codex", "atbench codex"])
add("D133-10", D133, (2746, 2746), "ACPBench", None, ["acpbench"], extra=["acpbench", "acp bench", "acp_bench", "acp-bench"])
add("D133-11", D133, (2747, 2747), "CodeJudgeBench", None, ["codejudgebench"],
    extra=["codejudgebench", "code judge bench", "code_judge_bench", "code-judge-bench"])
add("D133-12", D133, (2747, 2747), "LiveCodeBench post-cutoff execution", None, ["livecodebench"],
    extra=["livecodebench", "live code bench", "live_code_bench", "live-code-bench", "livecodebench execution", "livecodebench_execution",
           "livecodebench-execution"])
add("D133-13", D133, (2747, 2747), "SWE-bench Verified", None, ["swebench"],
    extra=["swe-bench", "swe_bench", "swebench", "swe bench", "swe-bench verified", "swe_bench_verified", "swebench_verified",
           "swebench-verified", "swe bench verified", "swe-bench-verified"])

# anchor files that exist outside never-open paths (LEAN-relative); entry id -> candidates
ANCHOR_CANDIDATES = {
    "D133-05": [("cruxeval", "think/data/public_refs/cruxeval/test.jsonl",
                 "raw CRUXEval test set (the 800 problems the CRUXEval-O MCQ anchor is built from)")],
}


# ------------------------------------------------------------------------------------------------ helpers
def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tokens(s: str) -> list[str]:
    return [t for t in re.split(r"[-_\s/]+", s.lower()) if t]


def variants(hf: str) -> set[str]:
    """The id itself, its repo part and org+repo with the separators - _ and space (lower case)."""
    org, _, repo = hf.partition("/")
    out = {hf.lower()}
    rt = tokens(repo)
    for sep in ("-", "_", " "):
        out.add(sep.join(rt))
    for sep in ("-", "_"):
        out.add(sep.join(tokens(org) + rt))
    return out


def names_of(e: dict) -> list[str]:
    s = {e["text"].lower()}
    if e["hf"]:
        s |= variants(e["hf"])
    s |= {x.lower() for x in e["extra"]} | {x.lower() for x in e["dl"]}
    return sorted(s)


def never_open(path) -> str | None:
    parts = [x.lower() for x in Path(str(path)).parts]
    for p in parts:
        for bad in NEVER_OPEN_PARTS:
            if bad in p:
                return bad
    return None


def prereg_problems(lines: list[str]) -> list[str]:
    out = []
    for e in E:
        a, b = e["lines"]
        blob = " ".join(re.sub(r"^\s*>\s?", "", x).strip() for x in lines[a - 1:b])
        blob = re.sub(r"\s+", " ", blob)
        if e["text"] not in blob:
            out.append(f"{e['id']}: '{e['text']}' is not on PREREG_FINAL.md line(s) {a}-{b}")
    return out


def denylist_problems() -> list[str]:
    if not DENYLIST.is_file():
        return [f"deny-list missing: {DENYLIST}"]
    have = set()
    for ent in json.loads(DENYLIST.read_text(encoding="utf-8"))["entries"]:
        for a in [ent.get("name") or ""] + list(ent.get("aliases", [])):
            have.add(a.split(":", 1)[-1].lower() if ":" in a and a.split(":", 1)[0] in ("span", "name", "dev") else a.lower())
    return [f"{e['id']}: deny-list alias '{a}' is not in {DENYLIST.name}" for e in E for a in e["dl"] if a.lower() not in have]


def core_problems() -> list[str]:
    out = []
    for e in E:
        for n in names_of(e):
            if not any(c in norm(n) for c in e["cores"]):
                out.append(f"{e['id']}: name '{n}' does not contain its core token {e['cores']}")
    return out


def build() -> dict:
    lines = PREREG.read_text(encoding="utf-8").splitlines()
    probs = prereg_problems(lines) + denylist_problems() + core_problems()
    ids = [e["id"] for e in E]
    if len(set(ids)) != len(ids):
        probs.append("duplicate entry ids")
    if probs:
        raise SystemExit("refused (nothing written):\n  " + "\n  ".join(probs))
    entries, names, anchors = [], set(), []
    for e in E:
        nm = names_of(e)
        names |= set(nm)
        entries.append({"id": e["id"], "list": e["list"], "prereg_lines": list(e["lines"]), "prereg_text": e["text"],
                        "names": nm, "denylist_aliases": sorted({a.lower() for a in e["dl"]})})
        for name, rel, note in ANCHOR_CANDIDATES.get(e["id"], []):
            p = (LEAN / rel)
            bad = never_open(p)
            if bad:
                raise SystemExit(f"refused: anchor candidate {rel} is on a never-open path ({bad})")
            if not p.is_file():
                continue
            anchors.append({"name": name, "path": str(p.resolve()), "sha256": sha256_file(p), "entry": e["id"], "note": note})
    return {
        "what": "C2 never-train manifest (A75 a): the A42-D 13.3 public anchors and the A40 (a) never-train datasets, from the adopted lists only",
        "spec": "PREREG_FINAL.md A42-D 13.1 / 13.3, A40 (a), A75 (a); g13_di/di_never_train.json merges in on top (mix_c2.merge_di_never_train)",
        "counts": {"entries": len(entries), "a40a": sum(e["list"] == A40 for e in E), "d133": sum(e["list"] == D133 for e in E),
                   "names": len(names), "anchors": len(anchors)},
        "names": sorted(names),
        "anchors": anchors,
        "entries": entries,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="build and check, write nothing")
    ap.add_argument("--force", action="store_true", help="overwrite an existing different manifest")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)
    doc = build()
    blob = (json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    out = Path(a.out)
    print("counts", json.dumps(doc["counts"], sort_keys=True))
    print("manifest sha256", hashlib.sha256(blob).hexdigest(), f"({len(blob)} bytes)")
    if a.dry:
        print("dry: nothing written")
        return 0
    if out.exists() and out.read_bytes() != blob and not a.force:
        print(f"refused: {out} exists and differs (use --force)")
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(blob)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
