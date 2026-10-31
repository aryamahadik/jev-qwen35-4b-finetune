"""LR-03 Juliet Test Suite 1.3 (C/C++, Java, C#) mapper, P1 realism (T65 VULN-SYNTH; family T65, source L-R).

Own label: PROGRAM labels. Juliet ships synthetic testcases whose vulnerable function is `<base>_bad` (C/C++), `bad` (Java) or `Bad`
(C#) and whose fixed variants are `goodG2B*`, `goodB2G*`, `good<N>` (any case of the first letter) inside the same file (NSA CAS);
the CWE class is the testcase directory. Recast (Opus approves): (1) yes/no "is this function the vulnerable variant?" on bad/good
TWINS from the same file (yes rate 50% by construction: one bad + one good per chosen file); (2) pick-one "which CWE class is the
flaw?" on bad functions with k in {4, 8} program-chosen hard distractor CWE names (the suite has > 8 classes). Row shares by
language: C/C++ 50%, Java 25%, C# 25% of each form (a language that cannot fill its share is reported, not back-filled).

What the mapper does to the code (so the label cannot be read off names, comments or literals; T65-M2 scrub): comments are stripped
(the FLAW / FIX comments and the @description header carry the answer); every identifier containing bad / good / cwe / flaw / benign /
vuln (any case) is renamed to a neutral item_N name; every STRING LITERAL containing a marker word (bad, good, flaw, fix, benign, safe,
vuln, secure, cwe) is replaced by a neutral string; the method is renamed `handle_item` and its modifiers / throws clause / static
qualifier are dropped (bad is public, goodX private or static). For the CWE-class form the class-name words (>= 4 letters) of the
GOLD class are also scrubbed from string literals and from ALL-CAPS macro/constant names. Include / import / using lines and
preprocessor lines lie outside the function and are not part of the row. Only single-file testcases (no a/b/c multi-file flow
variants, no C++ namespaces) are used; one file per base name, round-robin over CWE directories; a candidate whose rendering is a
near-duplicate (5-gram Jaccard >= 0.8) of an already chosen function is skipped. Guard F2: no CVE ids (R12).

NEVER touched: the frozen 10% hold-out CWE directories (quarantine zips), any CVE-labelled data.
"""
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "juliet_1_3"
F_YN = "lr_juliet_is_vulnerable"
F_CWE = "lr_juliet_cwe_class"
FORMS = {F_YN: "Is this function the vulnerable variant?", F_CWE: "Which CWE class is the flaw in this function?"}
LANG_SHARE = {"c": 0.5, "java": 0.25, "csharp": 0.25}
LANG_LABEL = {"c": "C", "java": "Java", "csharp": "C#"}

RECAST_TABLE = {
    "dataset_id": "NIST SARD Juliet Test Suite v1.3: C/C++ (SARD 112), Java (SARD 111), C# (SARD 110)",
    "train_file": "juliet_{c,java,csharp}_train.zip",
    "split_field": "none (own seeded 10% hold-out BY CWE DIRECTORY, frozen in the downloader; same CWE ids in every language)",
    "source_label_set": ["method name bad / Bad / <base>_bad (vulnerable)", "method names good* / Good* / goodG2B* / goodB2G* (fixed)",
                         "testcase directory CWE<id>_<name> (class)"],
    "recast_option_set": {"yes_no": ["Yes", "No"], "cwe": "gold CWE name + k-1 program-chosen distractor CWE names, k in {4,8}"},
    "target_format": "yes/no and Choice k", "mapping": {"bad method": "Yes", "good variant": "No"},
    "distractor_policy": "label-name token overlap + TF-IDF logistic confusion fitted on the train functions",
    "declared_balancing": "yes/no: one bad + one good per file (50%); cwe: round-robin over CWE directories; k alternates; "
                          "language shares C/C++ 50% / Java 25% / C# 25%",
    "declared_drops": ["multi-file flow variants (a/b/c suffix)", "C++ namespace files", "more than one file per base name",
                       "near-duplicate rendering of a chosen function", "R12 guards", "functions over the token cap"],
    "scrub": "comments; identifiers with bad/good/cwe/flaw/benign/vuln; string literals with marker words; (CWE form) class-name words "
             "in strings and ALL-CAPS macros",
    "question_form_ids": [F_YN, F_CWE], "span_selection_rule": "the whole method (short)", "expected_token_mean": 190,
    "caps": {F_YN: 350, F_CWE: 350},
}
META = {"dataset": DATASET, "lr_id": "LR-03", "family": "T65", "tier": "A", "cap": 700, "share_alike": False,
        "p1_realism": True, "recast_table": RECAST_TABLE}

_CWE_DIR = re.compile(r"^CWE(?P<num>\d+)_(?P<name>.+)$")
_LEAK = re.compile(r"\w*(?:bad|good|cwe|flaw|benign|vuln)\w*", re.I)
_MARK = re.compile(r"bad|good|flaw|fix|benign|safe|vuln|secure|cwe", re.I)
_STRLIT = re.compile(r'"(?:\\.|[^"\\\n])*"')
_CAPS = re.compile(r"\b[A-Z][A-Z0-9_]{3,}\b")
_STOP = {"with", "from", "that", "this", "than", "into", "over", "after", "before", "when", "without", "used", "using"}
KEEP_ONE_PER_BASE = True

LANGS = {
    "c": {"zip": "juliet_c_train.zip", "single": re.compile(r"^(?P<base>.+)_(?P<flow>\d{2})\.(?P<ext>c|cpp)$"),
          "good": re.compile(r"^good(?:G2B|B2G)\d*$|^good\d+$"), "depth": None},
    "java": {"zip": "juliet_java_train.zip", "single": re.compile(r"^(?P<base>.+)_(?P<flow>\d{2})\.(?P<ext>java)$"),
             "good": re.compile(r"^good(?:G2B|B2G)\d*$|^good\d+$"), "depth": 1},
    "csharp": {"zip": "juliet_csharp_train.zip", "single": re.compile(r"^(?P<base>.+)_(?P<flow>\d{2})\.(?P<ext>cs)$"),
               "good": re.compile(r"^Good(?:G2B|B2G)\d*$|^Good\d+$"), "depth": 2},
}


# ----------------------------------------------------------------------------------------------------------
# reader (train zips only)
# ----------------------------------------------------------------------------------------------------------
def read_train(train_dir=None, langs=("c", "java", "csharp")):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for lang in langs:
        cfg = LANGS[lang]
        zp = os.path.join(d, cfg["zip"])
        if not os.path.isfile(zp):
            continue
        with zipfile.ZipFile(zp) as z:
            for name in z.namelist():
                if "/testcases/" not in "/" + name:
                    continue
                parts = name.split("/")
                if len(parts) < 3:
                    continue
                m = cfg["single"].match(parts[-1])
                if not m:
                    continue                                  # multi-file flow variants (a/b/..) and others are not used
                cdir = [p for p in parts if _CWE_DIR.match(p)]
                if not cdir:
                    continue
                raw = z.read(name).decode("latin-1").replace("\r\n", "\n").replace("\r", "\n")
                if m.group("ext") == "cpp" and "namespace" in raw:
                    continue
                yield {"lang": lang, "path": name, "cwe_dir": cdir[0], "base": m.group("base"), "flow": m.group("flow"),
                       "text": raw, "_src_line": name}


# ----------------------------------------------------------------------------------------------------------
# parsing helpers
# ----------------------------------------------------------------------------------------------------------
def strip_comments(src):
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        nx = src[i + 1] if i + 1 < n else ""
        if c == "/" and nx == "*":
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            out.append(" ")
        elif c == "/" and nx == "/":
            j = src.find("\n", i)
            i = n if j < 0 else j
        elif c in "\"'":
            q = c
            k = i + 1
            while k < n and src[k] != q:
                k += 2 if src[k] == "\\" else 1
            out.append(src[i:k + 1])
            i = k + 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


_HDR = re.compile(r"(?m)^[ \t]*(?P<static>static[ \t]+)?(?P<ret>(?:(?:const|unsigned|struct)[ \t]+)*[A-Za-z_]\w*(?:[ \t]*\*+[ \t]*|[ \t]+))"
                  r"(?P<name>[A-Za-z_]\w*)[ \t]*\((?P<params>[^;{}]*)\)[ \t]*\n?[ \t]*\{")
_HDR_OO = re.compile(r"(?m)^[ \t]*(?P<mods>(?:(?:public|private|protected|internal|static|override|virtual|final|sealed|abstract)[ \t]+)*)"
                     r"(?P<ret>[A-Za-z_][\w<>,\.\?]*(?:\[\])?)[ \t]+(?P<name>[A-Za-z_]\w*)[ \t]*\((?P<params>[^;{}]*)\)"
                     r"(?P<throws>[ \t]*(?:throws[ \t]+[\w\., \t]+)?)[ \t]*\n?[ \t]*\{")
_KEYWORDS = {"if", "while", "for", "switch", "return", "sizeof", "else", "foreach", "catch", "using", "lock", "new", "do", "try"}


def _match_brace(text, open_idx):
    depth = 0
    i, n = open_idx, len(text)
    while i < n:
        c = text[i]
        if c in "\"'":
            q = c
            i += 1
            while i < n and text[i] != q:
                i += 2 if text[i] == "\\" else 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _depth_before(text, idx):
    depth, i = 0, 0
    while i < idx:
        c = text[i]
        if c in "\"'":
            q = c
            i += 1
            while i < idx and text[i] != q:
                i += 2 if text[i] == "\\" else 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return depth


def find_functions(clean, lang="c"):
    """Function / method definitions in comment-stripped source: C at top level; Java at class level (depth 1); C# at depth 2
    (namespace + class). Returns list of dict(name, ret, params, body, static)."""
    fns = []
    oo = lang != "c"
    for m in (_HDR_OO if oo else _HDR).finditer(clean):
        name = m.group("name")
        if name in _KEYWORDS or m.group("ret").strip() in _KEYWORDS:
            continue
        depth = _depth_before(clean, m.start())
        if (oo and depth != LANGS[lang]["depth"]) or (not oo and depth != 0):
            continue
        ob = clean.index("{", m.end() - 1)
        cb = _match_brace(clean, ob)
        if cb < 0:
            continue
        static = bool(m.group("static")) if not oo else ("static" in m.group("mods"))
        fns.append({"name": name, "ret": m.group("ret").strip(), "params": m.group("params").strip(), "body": clean[ob:cb + 1],
                    "static": static, "start": m.start()})
    return fns


def classify_functions(clean, lang, base_flow):
    """-> (bad_fn or None, [good fns]). C: bad = '<base>_NN_bad'; Java 'bad'; C# 'Bad'. good = good*/Good* variants with a body."""
    bad_name = {"c": base_flow + "_bad", "java": "bad", "csharp": "Bad"}[lang]
    bad, goods = None, []
    for f in find_functions(clean, lang):
        if f["name"] == bad_name:
            bad = f
        elif LANGS[lang]["good"].match(f["name"]):
            goods.append(f)
    return bad, goods


def class_words(label):
    """Words (>= 4 letters) of a class label such as 'CWE-190 Integer Overflow' (scrubbed from strings / macros in CWE rows)."""
    name = label.split(" ", 1)[1] if " " in label else label
    return sorted({w.lower() for w in re.findall(r"[A-Za-z]{4,}", name)} - _STOP)


def neutralise(code, extra_words=()):
    """Rename identifiers with marker words, replace marker string literals, scrub class-name words from strings and macros."""
    names, strs = {}, {}

    def ident(m):
        w = m.group(0)
        if w not in names:
            names[w] = "item_%d" % (len(names) + 1)
        return names[w]

    def strlit(m):
        s = m.group(0)
        low = s.lower()
        if _MARK.search(low) or any(w in low for w in extra_words):
            if s not in strs:
                strs[s] = '"str_%d"' % (len(strs) + 1)
            return strs[s]
        return s

    # string literals first (their text must not be touched by the identifier pass), then identifiers outside literals
    parts, last = [], 0
    for m in _STRLIT.finditer(code):
        parts.append(("code", code[last:m.start()]))
        parts.append(("str", strlit(m)))
        last = m.end()
    parts.append(("code", code[last:]))
    out = []
    for kind, text in parts:
        if kind == "str":
            out.append(text)
            continue
        text = _LEAK.sub(ident, text)
        if extra_words:
            text = _CAPS.sub(lambda m: ident(m) if any(w in m.group(0).lower() for w in extra_words) else m.group(0), text)
        out.append(text)
    return "".join(out)


def render_function(fn, extra_words=()):
    code = "%s handle_item(%s)\n%s" % (fn["ret"], re.sub(r"\s+", " ", fn["params"]), fn["body"])
    code = neutralise(code, extra_words)
    lines = [ln.rstrip() for ln in code.split("\n")]
    out, blank = [], 0
    for ln in lines:
        if not ln.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(ln)
    return "\n".join(out).strip()


def cwe_label(cwe_dir):
    m = _CWE_DIR.match(cwe_dir)
    return "CWE-%s %s" % (m.group("num"), m.group("name").replace("_", " "))


def is_bad_name(lang, name):
    return name.endswith("_bad") if lang == "c" else (name == "bad" if lang == "java" else name == "Bad")


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def __init__(self, pools, seed=0, dry_run=True, mapper_file=None, chooser=None, stamp_fn=None):
        super().__init__(pools, seed=seed, dry_run=dry_run, mapper_file=mapper_file, stamp_fn=stamp_fn)
        self.chooser = chooser

    # -- selection of files: one per base, round-robin over CWE directories, near-duplicate filtered -------------
    def _usable(self, records):
        out = []
        for src in records:
            lang = src.get("lang", "c")
            clean = strip_comments(src["text"])
            bad, goods = classify_functions(clean, lang, src["base"] + "_" + src["flow"])
            if bad is None or not goods:
                self.drops.add("no_bad_or_no_good_function", src["path"])
                continue
            out.append((src, bad, goods))
        return out

    def _pick_files(self, usable, n, tag):
        by_dir = {}
        seen_base = set()
        order = sorted(usable, key=lambda t: lc.stable_hash("jfile", self.seed, tag, t[0]["path"]))
        for src, bad, goods in order:
            if KEEP_ONE_PER_BASE and src["base"] in seen_base:
                continue
            seen_base.add(src["base"])
            by_dir.setdefault(src["cwe_dir"], []).append((src, bad, goods))
        dirs = sorted(by_dir, key=lambda d: lc.stable_hash("jdir", self.seed, tag, d))
        picked, shingles = [], []
        while len(picked) < n and any(by_dir.values()):
            for d in dirs:
                if by_dir[d] and len(picked) < n:
                    cand = by_dir[d].pop()
                    sh = lc._shingles(render_function(cand[1]))
                    # near-duplicate filter (R8): a sibling flow variant that renders like an already chosen function is skipped
                    if any(a and sh and len(a & sh) / float(len(a | sh)) >= 0.8 for a in shingles):
                        self.drops.add("near_duplicate_function", cand[0]["path"])
                        continue
                    shingles.append(sh)
                    picked.append(cand)
        return picked

    def build(self, src, ctx):
        """Candidates for one usable file: ctx['form'] selects the form (the file picker runs in map_records)."""
        lang = src.get("lang", "c")
        clean = strip_comments(src["text"])
        bad, goods = classify_functions(clean, lang, src["base"] + "_" + src["flow"])
        if bad is None or not goods:
            return []
        form = ctx.get("form", F_YN)
        sid = "juliet:%s" % src["path"]
        slots = {"lang": LANG_LABEL[lang]}
        if form == F_YN:
            good = goods[lc.stable_hash("jgood", self.seed, sid) % len(goods)]
            out = []
            for fn, gold in ((bad, "Yes"), (good, "No")):
                out.append({"form": F_YN, "kind": "yesno", "context": render_function(fn), "options": ["Yes", "No"],
                            "gold_text": gold, "source_row_id": "%s#%s" % (sid, "bad" if gold == "Yes" else "good"),
                            "slots": slots, "extra": {"orig_fn": fn["name"], "lang": lang, "cwe_dir": src["cwe_dir"], "pair": sid}})
            return out
        label = cwe_label(src["cwe_dir"])
        all_labels = ctx["labels"]
        k = self.ksched.next(len(all_labels))
        words = tuple(class_words(label))
        code = render_function(bad, words)
        dist = ctx["chooser"].choose(label, k, key=sid, text=code)
        return [{"form": F_CWE, "kind": "choice", "context": code, "options": [label] + dist,
                 "gold_text": label, "source_row_id": sid, "k_full": len(all_labels), "slots": slots,
                 "extra": {"orig_fn": bad["name"], "lang": lang, "cwe_dir": src["cwe_dir"]}}]

    def independent_gold(self, src, cand):
        lang = src.get("lang", "c")
        if cand["form"] == F_YN:
            name = cand["extra"]["orig_fn"]
            # Juliet convention: the vulnerable method is the bad one (C suffix _bad, Java bad, C# Bad); the other methods are fixed
            if name not in src["text"]:
                return "?"
            return "Yes" if is_bad_name(lang, name) else "No"
        # class label: the directory component 'CWE<num>_<Name>' of the file path
        comp = [p for p in src["path"].split("/") if re.match(r"CWE\d+_", p)][0]
        num, name = comp[3:].split("_", 1)
        return "CWE-%s %s" % (num, name.replace("_", " "))

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        records = list(records)
        usable = self._usable(records)
        caps = RECAST_TABLE["caps"]
        rows = []
        langs = sorted({u[0].get("lang", "c") for u in usable}, key=lambda l: list(LANG_SHARE).index(l) if l in LANG_SHARE else 9)
        share_total = sum(LANG_SHARE.get(l, 0.25) for l in langs) or 1.0

        def n_for(total, lang):
            """Largest-remainder allocation of `total` rows over the languages, so the shares sum exactly to the cap."""
            raw = {l: total * LANG_SHARE.get(l, 0.25) / share_total for l in langs}
            base = {l: int(v) for l, v in raw.items()}
            left = total - sum(base.values())
            for l in sorted(langs, key=lambda l: (-(raw[l] - base[l]), l))[:left]:
                base[l] += 1
            return base[lang]
        # yes/no twins
        used_paths, used_bases = set(), set()
        for lang in langs:
            sub = [u for u in usable if u[0].get("lang", "c") == lang]
            for src, bad, goods in self._pick_files(sub, n_for(caps[F_YN] // 2, lang), "yn" + lang):
                used_paths.add(src["path"])
                used_bases.add((lang, src["base"]))
                for cand in self.build(src, {"form": F_YN}):
                    r = self.finish_candidate(src, cand)
                    if r:
                        rows.append(r)
        # CWE class
        labels = sorted({cwe_label(s["cwe_dir"]) for s, _, _ in usable})
        if len(labels) >= 2:
            chooser = self.chooser or lc.DistractorChooser(labels)
            if self.chooser is None:
                chooser.fit([render_function(b, tuple(class_words(cwe_label(s["cwe_dir"])))) for s, b, g in usable],
                            [cwe_label(s["cwe_dir"]) for s, b, g in usable], seed=self.seed)
            for lang in langs:
                # T65-M1: JUL-CWE is drawn from test cases NOT used by JUL-VULN (neither the file nor a flow variant of its base)
                sub = [u for u in usable if u[0].get("lang", "c") == lang and u[0]["path"] not in used_paths
                       and (lang, u[0]["base"]) not in used_bases]
                for src, bad, goods in self._pick_files(sub, n_for(caps[F_CWE], lang), "cwe" + lang):
                    for cand in self.build(src, {"form": F_CWE, "labels": labels, "chooser": chooser}):
                        r = self.finish_candidate(src, cand)
                        if r:
                            rows.append(r)
        return rows
