"""LR-11 CommitPackFT mapper (P1 realism, family T66 REVIEW-GATE head; source L-R). Recast table below (Opus approves, G-R2 batch).

Own label: the pairing a human made when committing: this subject line was written for THIS change. Recast: yes/no "does the
commit message describe the change in this diff?". YES rows show a commit's own diff with its own subject. NO rows show a commit's
diff with the subject of ANOTHER commit of the SAME repository (both parts are dataset text; nothing is written by a model). LR-B3:
a swap pair is dropped when either subject has < 4 word tokens or the two subjects' token Jaccard >= 0.5. Only rows whose repo licence
is in the ONE code whitelist (mit, apache-2.0, bsd-2-clause, bsd-3-clause, cc0-1.0) are read (the downloader already wrote only those;
the reader and the mapper check again). Data / markup / prose languages are not selected for this code-review head (declared;
their files stay in train/). The diff is a unified diff of old_contents vs new_contents (3 context lines) of the one changed file.
NEVER touched: n/a (the release has no test split).
"""
import difflib
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "commitpackft"
FORM = "lr_cpft_message_matches_diff"
FORMS = {FORM: "Does the commit message describe the change shown in the diff?"}
WHITELIST = tc.CODE_WHITELIST_CPFT
EXCLUDED_LANGS = frozenset(["markdown", "text", "json", "yaml", "xml", "csv", "restructuredtext", "rdoc", "textile", "org", "creole",
                            "asciidoc", "gettext catalog", "bibtex", "apacheconf", "ini", "toml", "json5", "jsonld", "tsv", "rmarkdown",
                            "html", "html+erb", "html+django", "html+php", "css", "scss", "sass", "less", "svg", "pod", "mediawiki",
                            "plain text", "diff", "robotframework", "robots.txt"])
MAX_FILE_CHARS = 24000
DIFF_TOKEN_BUDGET = 1000
MIN_SUBJECT_TOKENS = 4
JACCARD_MAX = 0.5
RECAST_TABLE = {
    "dataset_id": "bigcode/commitpackft (revision in the download log), licence-whitelisted rows", "train_file": "data/<lang>.jsonl.gz",
    "split_field": "none (no test split in the release)", "source_label_set": ["own (diff, subject) pair"],
    "recast_option_set": ["Yes", "No"], "target_format": "yes/no",
    "mapping": {"own subject": "Yes", "subject of another same-repo commit (token Jaccard < 0.5, >= 4 tokens)": "No"},
    "distractor_policy": "same-repo message swap (LR-B3); every commit is used once, as a YES or as the diff donor of a NO",
    "declared_balancing": "50% yes (equal counts); round-robin over languages; at most 3 rows per repo",
    "declared_drops": ["duplicate (language, commit, file) row", "licence not in whitelist", "excluded data/markup language", "subject < 4 tokens", "file > 24000 chars", "diff over 1000 tokens",
                       "empty diff", "no same-repo partner for a NO", "R12 guards (CVE ids, emails, credentials in diff text)"],
    "question_form_ids": [FORM], "span_selection_rule": "none (whole diff must fit the budget; never cut)", "expected_token_mean": 520,
}
META = {"dataset": DATASET, "lr_id": "LR-11", "family": "T66", "tier": "C", "cap": 800, "share_alike": False,
        "p1_realism": True, "recast_table": RECAST_TABLE}
_WORD = re.compile(r"[a-z0-9]+")


def read_train(train_dir=None, langs=None, max_rows_per_lang=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    dd = os.path.join(d, "data")
    for fn in sorted(os.listdir(dd)):
        if not fn.endswith(".jsonl.gz"):
            continue
        lang = fn[:-len(".jsonl.gz")]
        if (langs and lang not in langs) or lang.lower() in EXCLUDED_LANGS:
            continue
        n = 0
        with gzip.open(os.path.join(dd, fn), "rt", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                if r.get("license") not in WHITELIST:
                    continue
                r["_src_line"] = "cpft:%s:%s:%s" % (lang, r["commit"], r.get("new_file", ""))
                yield r
                n += 1
                if max_rows_per_lang and n >= max_rows_per_lang:
                    break


def subject_tokens(s):
    return _WORD.findall((s or "").lower())


def jaccard(a, b):
    ta, tb = set(subject_tokens(a)), set(subject_tokens(b))
    return len(ta & tb) / float(len(ta | tb)) if (ta or tb) else 1.0


def make_diff(src):
    old, new = src.get("old_contents") or "", src.get("new_contents") or ""
    if len(old) > MAX_FILE_CHARS or len(new) > MAX_FILE_CHARS:
        return None, "file_too_long"
    ol, nl = old.splitlines(), new.splitlines()
    diff = list(difflib.unified_diff(ol, nl, fromfile="a/" + str(src.get("old_file") or src.get("new_file")),
                                     tofile="b/" + str(src.get("new_file")), n=3, lineterm=""))
    if not diff:
        return None, "empty_diff"
    return "\n".join(diff), None


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        """src carries '_shown' (the subject to display) and '_role' ('yes' | 'no')."""
        sid = src["_src_line"] + ("::swap" if src["_role"] == "no" else "")
        if src.get("license") not in WHITELIST:
            self.drops.add("licence_not_whitelisted", sid)
            return []
        own = lc.normalise_ws(src.get("subject"))
        shown = lc.normalise_ws(src["_shown"])
        if len(subject_tokens(own)) < MIN_SUBJECT_TOKENS or len(subject_tokens(shown)) < MIN_SUBJECT_TOKENS:
            self.drops.add("subject_under_4_tokens", sid)
            return []
        if src["_role"] == "no" and (jaccard(own, shown) >= JACCARD_MAX or own.lower() == shown.lower()):
            self.drops.add("swap_subjects_too_similar", sid)
            return []
        diff, why = make_diff(src)
        if diff is None:
            self.drops.add(why, sid)
            return []
        if lc.approx_tokens(diff) > DIFF_TOKEN_BUDGET:
            self.drops.add("diff_over_budget", sid)
            return []
        context = "Repository language: %s\nFile: %s\nDiff:\n%s\n\nCommit message: %s" % (src.get("lang"), src.get("new_file"), diff, shown)
        return [{"form": FORM, "kind": "yesno", "context": context, "options": ["Yes", "No"],
                 "gold_text": "Yes" if src["_role"] == "yes" else "No", "source_row_id": sid,
                 "extra": {"repo": src.get("repos"), "lang": src.get("lang"), "license": src.get("license"), "pair": src["_src_line"],
                           "role": src["_role"], "shown_subject": shown}}]

    def independent_gold(self, src, cand):
        # recomputed from the raw subject and what is actually displayed in the row: the label is Yes iff the shown subject IS the commit's own
        return "Yes" if lc.normalise_ws(cand["context"].rsplit("Commit message: ", 1)[1]) == lc.normalise_ws(src["subject"]) else "No"

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        eligible, seen_ids = [], set()
        for r in records:
            if r.get("_src_line") in seen_ids:
                self.drops.add("duplicate_item", r.get("_src_line"))
                continue
            seen_ids.add(r.get("_src_line"))
            if r.get("license") not in WHITELIST:
                self.drops.add("licence_not_whitelisted", r.get("_src_line"))
                continue
            if str(r.get("lang", "")).lower() in EXCLUDED_LANGS:
                self.drops.add("excluded_language", r.get("_src_line"))
                continue
            if len(subject_tokens(r.get("subject"))) < MIN_SUBJECT_TOKENS:
                self.drops.add("subject_under_4_tokens", r.get("_src_line"))
                continue
            eligible.append(r)
        by_repo = {}
        for r in eligible:
            by_repo.setdefault(r.get("repos"), []).append(r)
        yes_items, no_items = [], []
        for repo, items in by_repo.items():
            items.sort(key=lambda r: lc.stable_hash("cpft-order", self.seed, r["_src_line"]))
            for r in items:
                coin = lc.stable_hash("cpft-coin", self.seed, r["_src_line"]) & 1
                partner = None
                if coin:
                    for p in items:
                        if p is not r and p["commit"] != r["commit"] and jaccard(r["subject"], p["subject"]) < JACCARD_MAX \
                                and len(subject_tokens(p["subject"])) >= MIN_SUBJECT_TOKENS:
                            partner = p
                            break
                if partner is not None:
                    no_items.append((dict(r, _role="no", _shown=partner["subject"]), repo))
                else:
                    yes_items.append((dict(r, _role="yes", _shown=r["subject"]), repo))
        half = cap // 2
        out = []
        for side in (yes_items, no_items):
            groups = {}
            for it in side:
                groups.setdefault(str(it[0].get("lang")).lower(), []).append(it)

            def make(item):
                src = item[0]
                rr = []
                for cand in self.build(src, {}):
                    r = self.finish_candidate(src, cand)
                    if r:
                        rr.append(r)
                return rr
            out.append(lc.round_robin_take(groups, "cpft%s" % self.seed, half, make, unit_of=lambda it: it[1], unit_limit=3))
        n = min(len(out[0]), len(out[1]))
        return out[0][:n] + out[1][:n]
