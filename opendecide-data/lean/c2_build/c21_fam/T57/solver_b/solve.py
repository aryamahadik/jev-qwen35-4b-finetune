"""T57 Solver B. Input: schema.b_view(row, packages) (carriers + b_inputs + task package, no label / class / kind / tags).

Method: for every shown candidate tree B loads the rendered files into its own evaluator for the row's language (LC_SOLVER_B),
runs the package's structured cases (one fresh instance per case) and the differential points against the REFERENCE tree, and
derives NOFIX / REGRESSION / PARTIAL / CORRECT with the ROW_SCHEMA rule (TARGET / PASS-TO-PASS come from running the buggy tree).
`raises` steps carry abstract ids (ERR_VALUE, ERR_STATE): B resolves each id to the language-visible name by running the step on the
reference tree. LOCALISE gold = the enclosing function of the lines that differ between reference and buggy files (own per-language
function-span finder). status is 'ok' or 'unsupported' / 'timeout' / 'ambiguous'; those are never labels.
"""
import difflib
import re

from LC_SOLVER_B import langs
from LC_SOLVER_B.common import Budget, Timeout, Unsupported
from LC_SOLVER_B.diffapply import apply_diff

LETTERS = "ABCD"


def _tree(pkg, files):
    d = dict(files)
    for k, v in pkg.get("go_files", {}).items():
        d.setdefault(k, v)
    return d


class Runner:
    def __init__(self, lang, pkg):
        self.lang = lang
        self.pkg = pkg
        self.errmap = {}

    def _prog(self, files):
        return langs.program(self.lang, _tree(self.pkg, files), Budget(8_000_000))

    @staticmethod
    def _plain_eq(got, expect):
        return got == expect

    def run_case(self, files, case, learn=False):
        """Return (passed: bool, detail). With learn=True record ERR id -> observed exception name."""
        prog = self._prog(files)
        inst = None
        for st in case["steps"]:
            fn = st["fn"]
            if inst is None:
                inst = prog.fresh(fn)
            r = prog.invoke(inst, fn, st["args"])
            op = st["op"]
            if op == "eq":
                if r[0] != "ok":
                    return False, "eq-raised"
                got = r[1]
                if self.lang == "bash":
                    ok = str(got) == str(st["expect"])
                else:
                    ok = got == st["expect"] and type(got) is type(st["expect"])
                if not ok:
                    return False, "eq-mismatch"
            elif op == "raises":
                if r[0] != "exc":
                    return False, "no-raise"
                if learn:
                    self.errmap.setdefault(st["err"], r[1])
                else:
                    want = self.errmap.get(st["err"])
                    if want is None:
                        raise Unsupported("unlearned error id " + st["err"])
                    if r[1] != want:
                        return False, "wrong-exception"
            elif op == "do":
                if r[0] != "ok":
                    return False, "do-raised"
            else:
                raise Unsupported("step op " + op)
        return True, ""

    def point_obs(self, prog, point, snapshot):
        inst = None
        outs = []
        touched = False
        for c in point:
            if inst is None:
                inst = prog.fresh(c["fn"])
            if inst is not None:
                touched = True
            outs.append(prog.invoke(inst, c["fn"], c["args"]))
        if snapshot and touched:
            outs.append(prog.invoke(inst, snapshot, []))
        return outs


def classify(runner, pkg, cand_files, buggy_pass):
    """Execution class of one candidate tree."""
    vis = pkg["visible_case"]
    ok, _ = runner.run_case(cand_files, vis)
    if not ok:
        return "NOFIX"
    for case in pkg["hidden_cases"]:
        if buggy_pass[case["name"]]:
            ok, _ = runner.run_case(cand_files, case)
            if not ok:
                return "REGRESSION"
    for case in pkg["hidden_cases"]:
        if not buggy_pass[case["name"]]:
            ok, _ = runner.run_case(cand_files, case)
            if not ok:
                return "PARTIAL"
    # differential against the reference
    ref_prog = runner._prog(pkg["reference_files"])
    cand_prog = runner._prog(cand_files)
    snap = pkg.get("snapshot")
    for pt in pkg["differential_points"]:
        if runner.point_obs(ref_prog, pt, snap) != runner.point_obs(cand_prog, pt, snap):
            return "PARTIAL"
    return "CORRECT"


# ------------------------------------------------------------------------------------------------ LOCALISE
_HDR = {
    "python": re.compile(r"^(\s*)def\s+([A-Za-z_]\w*)\s*\("),
    "javascript": re.compile(r"^(\s*)(?:export\s+)?(?:function\s+([A-Za-z_$][\w$]*)\s*\(|([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*(?::\s*[^{]+)?\{)"),
    "go": re.compile(r"^()func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)\s*\("),
    "bash": re.compile(r"^()([A-Za-z_]\w*)\(\)\s*\{"),
}
_HDR["typescript"] = _HDR["javascript"]
_NOT_FN = {"if", "for", "while", "switch", "catch", "constructor", "return"}


def _enclosing(lang, lines, idx):
    """Name of the function enclosing line idx (0-based), else None."""
    rx = _HDR[lang]
    for j in range(idx, -1, -1):
        m = rx.match(lines[j])
        if m:
            name = m.group(2) or (m.group(3) if m.lastindex and m.lastindex >= 3 else None)
            if name in _NOT_FN or name is None:
                continue
            ind = len(m.group(1))
            if lang in ("go", "bash"):
                return name
            if j == idx or (len(lines[idx]) - len(lines[idx].lstrip())) > ind:
                return name
            if lang == "python":
                continue
            return name
    return None


def _regions(lang, pkg):
    """Textual differences between the reference and the buggy files, grouped by the enclosing function (own span finder).
    -> {fn: {path: [opcode index, ...]}} and the per-file opcode lists."""
    ops = {}
    groups = {}
    for path in sorted(set(pkg["reference_files"]) | set(pkg["buggy_files"])):
        a = pkg["reference_files"].get(path, "")
        b = pkg["buggy_files"].get(path, "")
        if a == b:
            continue
        al, bl = a.split("\n"), b.split("\n")
        sm = difflib.SequenceMatcher(a=al, b=bl, autojunk=False)
        ops[path] = (al, bl, sm.get_opcodes())
        for k, (tag, i1, i2, j1, j2) in enumerate(ops[path][2]):
            if tag == "equal":
                continue
            jj = min(j1, len(bl) - 1)
            fn = _enclosing(lang, bl, jj)
            if fn is None and tag == "delete":
                fn = _enclosing(lang, bl, max(j1 - 1, 0))
            if fn is not None:
                groups.setdefault(fn, {}).setdefault(path, []).append(k)
    return groups, ops


def _tree_with(pkg, ops, selected):
    """Reference files with only the selected opcodes of the buggy version applied."""
    tree = dict(pkg["reference_files"])
    for path, idxs in selected.items():
        al, bl, codes = ops[path]
        out = []
        for k, (tag, i1, i2, j1, j2) in enumerate(codes):
            out.extend(bl[j1:j2] if k in idxs else al[i1:i2])
        tree[path] = "\n".join(out)
    return tree


def localise(lang, pkg):
    """Functions whose text differs between the reference and the buggy files (textual view)."""
    groups, _ = _regions(lang, pkg)
    return set(groups)


def localise_behavioural(lang, pkg, runner):
    """Functions whose buggy text changes BEHAVIOUR: each textual region is applied alone to the reference tree and the visible case,
    the hidden cases and the differential points are re-run (a behaviour-preserving edit, e.g. a local rename, is not the bug)."""
    groups, ops = _regions(lang, pkg)
    ref_prog = runner._prog(pkg["reference_files"])
    snap = pkg.get("snapshot")
    changed = set()
    for fn, sel in groups.items():
        tree = _tree_with(pkg, ops, sel)
        bad = False
        for case in [pkg["visible_case"]] + pkg["hidden_cases"]:
            if not runner.run_case(tree, case)[0]:
                bad = True
                break
        if not bad:
            prog = runner._prog(tree)
            for pt in pkg["differential_points"]:
                if runner.point_obs(ref_prog, pt, snap) != runner.point_obs(prog, pt, snap):
                    bad = True
                    break
        if bad:
            changed.add(fn)
    return changed, set(groups)


def shown_trees(view, pkg):
    """Candidate trees derived from the SHOWN patches (PATCH_DIFF applied to the buggy tree): this is what a model sees, so it is
    the order B uses. Returns (trees, letters) or (None, None) for heads without shown patches."""
    pd = view["carriers"].get("PATCH_DIFF")
    if pd is None:
        return None, None
    items = pd if isinstance(pd, list) else [{"option": None, "diff": pd}]
    trees, letters = [], []
    for it in items:
        try:
            t, _ = apply_diff(pkg["buggy_files"], it["diff"])
        except ValueError as e:
            raise Unsupported("shown diff does not apply: %s" % e)
        trees.append({p: t[p] for p in pkg["buggy_files"] if p in t})
        letters.append(it["option"])
    return trees, letters


def _test_name_of(text, lang):
    for rx in (r"def test_(\w+)\(", r"test\('([^']+)'", r"func Test(\w+)\(", r"^test_(\w+)\(\)"):
        m = re.search(rx, text, re.M)
        if m:
            return m.group(1)
    return None


def _opt_letter_index(options, name):
    for i, o in enumerate(options):
        if o == name:
            return i
    return None


def solve(view):
    rid = view["row_id"]
    try:
        return _solve(view)
    except Unsupported as e:
        return {"row_id": rid, "status": "unsupported", "label": None, "evidence": {"why": str(e)[:200]}}
    except Timeout as e:
        return {"row_id": rid, "status": "timeout", "label": None, "evidence": {"why": str(e)[:200]}}


def _solve(view):
    head = view["head"]
    lang = view["lang"]
    pkg = view["package"]
    bi = view["b_inputs"]
    rid = view["row_id"]
    runner = Runner(lang, pkg)
    res = {"row_id": rid, "status": "ok", "label": None, "classes": [], "evidence": {}}
    car_opts = view["carriers"].get("OPTIONS")
    if head == "LOCALISE":
        for case in [pkg["visible_case"]] + pkg["hidden_cases"]:
            runner.run_case(pkg["reference_files"], case, learn=True)
        fns, textual = localise_behavioural(lang, pkg, runner)
        opts = [o.partition(". ")[2] for o in car_opts]
        res["evidence"]["b_inputs_options_consistent"] = opts == list(bi["options"])
        res["evidence"]["textually_changed_fns"] = len(textual)
        hit = [i for i, o in enumerate(opts) if o in fns]
        res["evidence"]["behaviourally_changed_fns"] = len(fns)
        if len(hit) != 1:
            res["status"] = "ambiguous"
            res["evidence"]["hits"] = len(hit)
            return res
        res["label"] = LETTERS[hit[0]]
        return res
    # learn the abstract error ids on the reference tree (also checks the reference passes everything it should)
    for case in [pkg["visible_case"]] + pkg["hidden_cases"]:
        ok, why = runner.run_case(pkg["reference_files"], case, learn=True)
        if not ok:
            res["evidence"].setdefault("ref_fail", []).append(why)
    # PASS-TO-PASS / TARGET from the buggy tree
    buggy_pass = {}
    for case in pkg["hidden_cases"]:
        buggy_pass[case["name"]] = runner.run_case(pkg["buggy_files"], case)[0]
    trees, letters = shown_trees(view, pkg)
    if trees is not None:
        res["evidence"]["shown_trees_match_b_inputs"] = [t == c for t, c in zip(trees, bi["candidate_files"])] if len(trees) == len(bi["candidate_files"]) else False
    if head == "TESTSEL":
        patched = trees[0] if trees else bi["candidate_files"][0]
        names = [_test_name_of(o, lang) for o in car_opts]
        by = {c["name"].lower(): c for c in pkg["hidden_cases"]}
        sel = []
        states = []
        res["evidence"]["b_inputs_options_consistent"] = [n.lower() if n else n for n in names] == [x.lower() for x in bi["options"]]
        for i, nm in enumerate(names):
            case = by.get((nm or "").lower())
            if case is None:
                raise Unsupported("option case not in package")
            before = runner.run_case(pkg["buggy_files"], case)[0]
            after = runner.run_case(patched, case)[0]
            states.append((before, after))
            if (not before) and after:
                sel.append(i)
        res["evidence"]["other_options_pass_before_and_after"] = all(st == (True, True) for i, st in enumerate(states) if i not in sel)
        if len(sel) != 1:
            res["status"] = "ambiguous"
            res["evidence"]["fail_to_pass_options"] = len(sel)
            return res
        res["label"] = LETTERS[sel[0]]
        return res
    classes = [classify(runner, pkg, cf, buggy_pass) for cf in (trees if trees is not None else bi["candidate_files"])]
    res["classes"] = classes
    if head == "VERDICT":
        res["label"] = "CORRECT" if classes[0] == "CORRECT" else "INCORRECT"
        res["reason_class"] = classes[0]
    elif head == "BEST4":
        good = [i for i, c in enumerate(classes) if c == "CORRECT"]
        if len(good) != 1:
            res["status"] = "ambiguous"
            res["evidence"]["correct_candidates"] = len(good)
            return res
        res["label"] = LETTERS[good[0]]
    elif head == "REASON":
        letter = None
        for o in view["carriers"]["OPTIONS"]:
            l, _, t = o.partition(". ")
            if t == classes[0]:
                letter = l
        res["label"] = letter
        if letter is None:
            res["status"] = "ambiguous"
    else:
        raise Unsupported("head " + head)
    return res
