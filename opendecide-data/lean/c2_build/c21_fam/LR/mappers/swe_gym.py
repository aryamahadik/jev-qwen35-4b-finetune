"""LR-09 SWE-Gym mapper (P1 realism, family T57r transfer slice; source L-R). Recast table below (Opus approves, G-R2 batch).

Own labels (human artefacts only): the file the HUMAN gold patch changes, and the test file the HUMAN test patch changes.
Recast: two localisation pick-ones. (1) lr_swegym_fix_file: repository + the failing test ids (+ the test patch when it fits) ->
which source file does the fix change? (2) lr_swegym_test_file: the gold patch -> which test file does the accompanying test patch
change? Options: the gold path plus program-chosen paths of single-file patches of OTHER instances of the SAME repository (path-token
overlap, k alternating 4 / 8). Only instances whose patch (or test patch) touches exactly ONE file get a row. NO issue text
(problem_statement, hints_text), no execution list is used; the four-gate patch-verdict rows with mutated negatives belong to the
T57r family on the signed-off sandbox, not here. Only whitelisted-repo rows exist in train/ (downloader). Instance-level G13 against
SWE-bench / SWE-bench-Live / SWE-rebench (plan K9) is applied by the stamp wrapper. NEVER touched: n/a (single train split).
"""
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "swe_gym"
F_FIX, F_TEST = "lr_swegym_fix_file", "lr_swegym_test_file"
FORMS = {F_FIX: "Which file does the fix change?", F_TEST: "Which test file does the test patch change?"}
PATCH_BUDGET = 900          # tokens: gold patch shown in F_TEST (never cut; over budget = drop)
TESTPATCH_OPTIONAL_BUDGET = 500   # tokens: test patch shown in F_FIX only when it fits
MAX_F2P = 6
RECAST_TABLE = {
    "dataset_id": "SWE-Gym/SWE-Gym train (whitelisted repos), fields instance_id, repo, patch, test_patch, FAIL_TO_PASS", "train_file": "train.jsonl.gz",
    "split_field": "none (single train split)", "source_label_set": ["the single file in the gold patch", "the single file in the test patch"],
    "recast_option_set": "gold path + program-chosen paths of other instances of the same repo, k in {4, 8}",
    "target_format": "Choice k (k alternating 4 / 8)", "mapping": {"gold patch file": "gold option", "test patch file": "gold option (F_TEST)"},
    "distractor_policy": "same-repo single-file patch paths of other instances, ranked by path-token overlap with the gold path",
    "declared_balancing": "round-robin over (repo, form); gold position balanced by the row finisher; k alternates 4 / 8",
    "declared_drops": ["patch touches != 1 file", "test patch touches != 1 file", "fewer than 3 distractor paths in the repo pool",
                       "gold patch over 900 tokens (F_TEST)", "R12 guards (CVE ids, emails, credentials in diff text)"],
    "question_form_ids": [F_FIX, F_TEST], "span_selection_rule": "none (patches are shown whole or the row is dropped)", "expected_token_mean": 420,
}
META = {"dataset": DATASET, "lr_id": "LR-09", "family": "T57r", "tier": "C", "cap": 1000, "share_alike": False,
        "p1_realism": True, "recast_table": RECAST_TABLE}
_DIFF_GIT = re.compile(r"^diff --git a/(.+?) b/(.+)$", re.M)
_PLUS_FILE = re.compile(r"^\+\+\+ b/(.+)$", re.M)


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with gzip.open(os.path.join(d, "train.jsonl.gz"), "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                r["_src_line"] = "swegym:" + r["instance_id"]
                yield r


def diff_files(patch):
    return [m.group(2) for m in _DIFF_GIT.finditer(patch or "")]


def single_file(patch):
    fs = diff_files(patch)
    return fs[0] if len(fs) == 1 else None


def f2p_list(v):
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except ValueError:
            v = [v]
    return [lc.normalise_ws(x) for x in (v or []) if lc.normalise_ws(x)]


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def _options(self, gold, pool, sid, form):
        cands = sorted(p for p in pool if p != gold)
        if len(cands) < 3:
            return None
        k = self.ksched.next(len(cands) + 1)
        ranked = sorted(cands, key=lambda p: (-lc.name_overlap(gold, p), lc.stable_hash("swegym-dist", sid, form, p)))
        return [gold] + ranked[:k - 1]

    def build(self, src, ctx):
        sid = src["_src_line"]
        form = ctx["form"]
        pools = ctx["pools"][src["repo"]]
        if form == F_FIX:
            gold = single_file(src["patch"])
            if gold is None:
                self.drops.add("patch_not_single_file", sid)
                return []
            opts = self._options(gold, pools["fix"], sid, form)
            if opts is None:
                self.drops.add("pool_too_small", sid)
                return []
            tests = f2p_list(src.get("FAIL_TO_PASS"))[:MAX_F2P]
            context = "Repository: %s\nFailing tests that the fix must make pass:\n%s" % (src["repo"], "\n".join("- " + t for t in tests) if tests else "- (none listed)")
            tp = (src.get("test_patch") or "").strip()
            if tp and lc.approx_tokens(tp) <= TESTPATCH_OPTIONAL_BUDGET:
                context += "\n\nTest patch:\n" + tp
        else:
            gold = single_file(src["test_patch"])
            if gold is None:
                self.drops.add("test_patch_not_single_file", sid)
                return []
            opts = self._options(gold, pools["test"], sid, form)
            if opts is None:
                self.drops.add("pool_too_small", sid)
                return []
            patch = (src.get("patch") or "").strip()
            if lc.approx_tokens(patch) > PATCH_BUDGET:
                self.drops.add("patch_over_budget", sid)
                return []
            context = "Repository: %s\nFix patch:\n%s" % (src["repo"], patch)
        return [{"form": form, "kind": "choice", "context": context, "options": opts, "gold_text": gold, "source_row_id": sid,
                 "k_full": len(pools["fix" if form == F_FIX else "test"]), "extra": {"repo": src["repo"], "instance": src["instance_id"]}}]

    def independent_gold(self, src, cand):
        text = src["patch"] if cand["form"] == F_FIX else src["test_patch"]
        fs = _PLUS_FILE.findall(text or "")
        return fs[0] if len(fs) == 1 else None

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        recs = list(records)
        pools = {}
        for r in recs:
            p = pools.setdefault(r["repo"], {"fix": set(), "test": set()})
            a, b = single_file(r["patch"]), single_file(r["test_patch"])
            if a:
                p["fix"].add(a)
            if b:
                p["test"].add(b)
        groups = {}
        for r in recs:
            for form in (F_FIX, F_TEST):
                groups.setdefault((r["repo"], form), []).append((r, form))

        def make(item):
            src, form = item
            out = []
            for cand in self.build(src, {"form": form, "pools": pools}):
                row = self.finish_candidate(src, cand)
                if row:
                    out.append(row)
            return out
        gk = {"%s|%s" % k: v for k, v in groups.items()}
        return lc.round_robin_take(gk, "swegym%s" % self.seed, cap, make)
