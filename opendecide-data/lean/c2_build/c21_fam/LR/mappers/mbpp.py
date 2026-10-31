"""LR-12 MBPP (full config, train) mapper (P1 realism, family LR-code, outside T42c's 3,000; Opus LR-M7). Recast table below.

Form lr_mbpp_test_fails (T42c-Q-TFAIL2): "will this stated test fail when run against this function?" yes/no. The function is either
the HUMAN solution (crowd-written, verified to pass its tests) or a text MUTANT of it made by the deterministic mutator below (our own
code, no model). The gold is NEVER assumed: it is the result of EXECUTING the stated test against the shown code, through the
`exec_fn` hook, which production binds to the signed-off sandbox (od-sbx1); this module never executes dataset code itself. With no
`exec_fn` the form produces no rows (logged `tfail_hooks_missing`). A human solution that fails its own test, a timeout or an error
drops the candidate (logged). R4: the gold is recomputed by a second, separate execution call and must agree.
Balanced to 50% yes (= the test fails). NEVER touched: test (500), validation (90), prompt (10) (quarantine); problem-level G13 against
CodeMind sources and REval is applied by the stamp wrapper.
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

DATASET = "mbpp"
FORM = "lr_mbpp_test_fails"
FORMS = {FORM: "Will the stated test fail when it is run against this function?"}
MAX_MUTANTS = 4
CODE_TOKEN_BUDGET = 900
RECAST_TABLE = {
    "dataset_id": "MBPP full config (google-research-datasets/mbpp) train split, task ids 601-974", "train_file": "train.jsonl.gz",
    "split_field": "parquet file name (test, validation, prompt quarantined)", "source_label_set": ["execution result of (code, test statement)"],
    "recast_option_set": ["Yes", "No"], "target_format": "yes/no", "mapping": {"test statement fails": "Yes", "test statement passes": "No"},
    "distractor_policy": "n/a (mutants of the human solution are made by the deterministic text mutator in this file)",
    "declared_balancing": "50% yes; at most 2 rows per problem; round-robin over problems",
    "declared_drops": ["no exec_fn hook", "human solution fails its own test", "execution timeout or error", "code over 900 tokens",
                       "mutant text equal to the original", "second execution disagrees", "R12 guards"],
    "question_form_ids": [FORM], "span_selection_rule": "none", "expected_token_mean": 260,
}
META = {"dataset": DATASET, "lr_id": "LR-12", "family": "LR-code", "tier": "C", "cap": 300, "share_alike": False,
        "p1_realism": True, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with gzip.open(os.path.join(d, "train.jsonl.gz"), "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                r["_src_line"] = "mbpp:%s" % r["task_id"]
                yield r


_SWAPS = [(r"==", "!="), (r"!=", "=="), (r"<=", "<"), (r">=", ">"), (r"(?<![<=!>])<(?![<=])", "<="), (r"(?<![<=!>-])>(?![>=])", ">="),
          (r"\band\b", "or"), (r"\bor\b", "and"), (r"\bTrue\b", "False"), (r"\bFalse\b", "True"), (r"\+(?!=)", "-"), (r"(?<![-=])-(?![-=>])", "+"),
          (r"\bmin\(", "max("), (r"\bmax\(", "min("), (r"\+= 1", "-= 1"), (r"\bsorted\(", "list(")]


def normalise_code(code):
    return (code or "").replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ").rstrip()


def simple_mutants(code, limit=MAX_MUTANTS, seed=0):
    """Deterministic single-site text mutants of `code` (a changed copy per distinct site); no model, no execution."""
    sites = []
    for pat, rep in _SWAPS:
        for m in re.finditer(pat, code):
            sites.append((m.start(), m.end(), rep))
    # integer literal off-by-one
    for m in re.finditer(r"(?<![\w.])\d+(?![\w.])", code):
        sites.append((m.start(), m.end(), str(int(m.group(0)) + 1)))
    out, seen = [], {code}
    for s in sorted(sites, key=lambda t: lc.stable_hash("mbpp-mut", seed, t[0], t[1], t[2])):
        mutated = code[:s[0]] + s[2] + code[s[1]:]
        if mutated not in seen:
            seen.add(mutated)
            out.append(mutated)
        if len(out) >= limit:
            break
    return out


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def __init__(self, pools, seed=0, dry_run=True, mapper_file=None, stamp_fn=None, exec_fn=None, mutate_fn=None):
        super(Mapper, self).__init__(pools, seed=seed, dry_run=dry_run, mapper_file=mapper_file, stamp_fn=stamp_fn)
        self.exec_fn = exec_fn
        self.mutate_fn = mutate_fn or simple_mutants

    def _run(self, code, setup, test):
        """True = the stated test PASSES, False = it fails; None = error / timeout."""
        r = self.exec_fn(code, setup, test)
        return r if r in (True, False) else None

    def build(self, src, ctx):
        """ctx: {'variant': 'orig' | int mutant index, 'code': code shown, 'test': stated test statement}."""
        variant, code, test = ctx["variant"], ctx["code"], ctx["test"]
        sid = "%s:%s" % (src["_src_line"], "orig" if variant == "orig" else "mut%d" % variant)
        if self.exec_fn is None:
            self.drops.add("tfail_hooks_missing", sid)
            return []
        setup = src.get("test_setup_code") or ""
        if lc.approx_tokens(code) > CODE_TOKEN_BUDGET:
            self.drops.add("code_over_budget", sid)
            return []
        passes = self._run(code, setup, test)
        if passes is None:
            self.drops.add("exec_error_or_timeout", sid)
            return []
        if variant == "orig" and not passes:
            self.drops.add("human_solution_fails_own_test", sid)
            return []
        context = "Function:\n%s\n\nStated test: %s" % (code, test)
        if setup.strip():
            context = "Setup code:\n%s\n\n%s" % (normalise_code(setup), context)
        return [{"form": FORM, "kind": "yesno", "context": context, "options": ["Yes", "No"], "gold_text": "No" if passes else "Yes",
                 "source_row_id": sid, "extra": {"task_id": src["task_id"], "variant": "orig" if variant == "orig" else "mutant",
                                                  "test": test, "code": code, "setup": setup}}]

    def independent_gold(self, src, cand):
        x = cand["extra"]
        again = self._run(x["code"], x["setup"], x["test"])
        if again is None:
            raise RuntimeError("second execution failed")
        return "No" if again else "Yes"

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        recs = list(records)
        side = {"Yes": {}, "No": {}}
        made = {}
        for src in recs:
            tests = [t for t in (src.get("test_list") or []) if lc.normalise_ws(t)]
            code = normalise_code(src.get("code"))
            if not tests or not code:
                self.drops.add("no_tests_or_code", src["_src_line"])
                continue
            rng = lc.seeded_rng("mbpp-test", src["task_id"], self.seed)
            variants = [("orig", code)] + [(i, m) for i, m in enumerate(self.mutate_fn(code, MAX_MUTANTS, self.seed))]
            for var, c in variants:
                test = tests[rng.randrange(len(tests))]
                for cand in self.build(src, {"variant": var, "code": c, "test": test}):
                    row = self.finish_candidate(src, cand)
                    if row:
                        side[row["answer_text"]].setdefault(src["task_id"], []).append(row)
        out = []
        half = cap // 2
        for lab in ("Yes", "No"):
            groups = {k: list(v) for k, v in side[lab].items()}
            take = lc.round_robin_take({k: [(r,) for r in v] for k, v in groups.items()}, "mbpp%s%s" % (lab, self.seed), half,
                                       lambda it: [it[0]], unit_of=lambda it: it[0]["extra"]["task_id"], unit_limit=1)
            out.append([t for t in take])
        n = min(len(out[0]), len(out[1]))
        return out[0][:n] + out[1][:n]
