"""LR-05 LogChunks mapper (P1 realism, family T62 FLAKY-OR-REAL / CI-log triage; source L-R).

Own label: the manually labelled failure CHUNK of each Travis CI build log (validated with the original developers).
Recast (Opus approves): pick-one "which segment of this log excerpt explains why the build failed?". The excerpt is built by
PROGRAM span selection from the SAME log only (LR-B10): the gold chunk's lines + (k-1) distractor windows of the same line
count, k in {4, 8}; windows are shown as numbered segments in RANDOM order (so neither the original line numbers nor the
position among segments leaks the gold); distractor windows prefer lines that hit the example's own search keywords (the
dataset's `Keywords` field, human-chosen) so they look like failures. The `Category` field is a STRUCTURAL class of the chunk
(not a failure type; readme), so no category form is built (the plan's 'failure category' form has no label in this release).
A chunk that cannot be located in its log (after whitespace / ANSI normalisation) or whose windows do not fit the token
budget is dropped and logged (never cut). NEVER touched: the frozen 10% hold-out repos (quarantine).
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "logchunks"
FORM = "lr_logchunks_failure_segment"
FORMS = {FORM: "Which segment of this build log explains why the build failed?"}
BUDGET_TOKENS = 1000

RECAST_TABLE = {
    "dataset_id": "LogChunks (Zenodo 3632351) CC BY 4.0", "train_file": "logchunks_train.zip",
    "split_field": "none (own seeded 10% hold-out BY REPO, exactly ceil(10%) repos)",
    "source_label_set": ["<Chunk> text of each <Example> in build-failure-reason/<lang>/<owner>@<repo>.xml"],
    "recast_option_set": "Segment 1..k (display order); gold = the segment equal to the labelled chunk lines",
    "target_format": "Choice k, k in {4, 8}", "mapping": {"labelled chunk lines": "gold segment"},
    "distractor_policy": "same-log windows with the gold's line count; prefer windows hitting the example's own Keywords",
    "declared_balancing": "k alternates 4/8 (falls back to the smaller k when the budget is exceeded); segments in random order",
    "declared_drops": ["chunk not locatable in its log", "windows exceed the token budget", "gold chunk longer than 60 lines",
                       "R12 guards"],
    "question_form_ids": [FORM], "span_selection_rule": "gold lines + same-length windows from the same log, random order",
    "expected_token_mean": 650,
}
META = {"dataset": DATASET, "lr_id": "LR-05", "family": "T62", "tier": "A", "cap": 700, "share_alike": False,
        "p1_realism": True, "recast_table": RECAST_TABLE}

_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b-\x1f\x7f]")
_SGR_REMNANT = re.compile(r"\[[0-9;]*[mKGHJ]")        # the XML chunks keep '[31m' without the ESC byte


def norm_line(s):
    """Matching normaliser: ANSI sequences and their ESC-less remnants and whitespace differences are ignored."""
    return re.sub(r"\s+", " ", _SGR_REMNANT.sub("", _ANSI.sub("", s))).strip()


def display_line(s):
    """Display normaliser: real ANSI / control bytes removed (same function on gold and distractor lines)."""
    return _ANSI.sub("", s).rstrip()


def read_train(train_dir=None):
    """Yield {log_id, repo, language, keywords, category, chunk, log_text} for every labelled example in the train zip."""
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with zipfile.ZipFile(os.path.join(d, "logchunks_train.zip")) as z:
        names = set(z.namelist())
        for x in sorted(n for n in names if n.endswith(".xml") and "/build-failure-reason/" in n):
            root = ET.fromstring(z.read(x))
            for ex in root.findall("Example"):
                log = (ex.findtext("Log") or "").strip()
                lp = "LogChunks/logs/" + log
                if lp not in names:
                    continue
                parts = log.split("/")
                yield {"log_id": log, "language": parts[0], "repo": parts[1] if len(parts) > 1 else "",
                       "keywords": [k.strip() for k in (ex.findtext("Keywords") or "").split(",") if k.strip()],
                       "category": ex.findtext("Category"), "chunk": ex.findtext("Chunk") or "",
                       "log_text": z.read(lp).decode("utf-8", "replace"), "_src_line": log}


def locate_chunk(log_lines, chunk):
    """Return (start, end) line indexes (inclusive) of `chunk` inside `log_lines` after normalisation, else None.
    The authors trimmed chunk ends mid-line, so the FIRST and LAST chunk lines may be substrings of a log line; interior
    lines must be equal (or contained). Empty log lines between matched lines are skipped. Anchors shorter than 8 chars
    are refused (too ambiguous)."""
    cl = [norm_line(c) for c in chunk.replace("\r\n", "\n").split("\n")]
    cl = [c for c in cl if c]
    if not cl or len(cl[0]) < 8:
        return None
    nl = [norm_line(x) for x in log_lines]
    last = len(cl) - 1
    for i, line in enumerate(nl):
        if cl[0] not in line:
            continue
        j, k = i, 0
        while j < len(nl) and k <= last:
            if not nl[j] and k > 0:
                j += 1
                continue
            ok = (cl[k] in nl[j]) if k in (0, last) else (nl[j] == cl[k] or cl[k] in nl[j])
            if not ok:
                break
            j += 1
            k += 1
        if k > last:
            return i, j - 1
    return None


def _window_ok(nl, s, e):
    body = nl[s:e + 1]
    return sum(1 for x in body if x) >= max(1, (e - s + 1) // 2)


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        lines = src["log_text"].replace("\r\n", "\n").replace("\r", "\n").split("\n")
        loc = locate_chunk(lines, src["chunk"])
        if loc is None:
            self.drops.add("chunk_not_locatable", src["_src_line"])
            return []
        gs, ge = loc
        w = ge - gs + 1
        if w > 60:
            self.drops.add("gold_chunk_over_60_lines", src["_src_line"])
            return []
        nl = [norm_line(x) for x in lines]
        kws = [k.lower() for k in src["keywords"]]
        rng = lc.seeded_rng("logwin", self.seed, src["_src_line"])
        gold_tok = lc.approx_tokens("\n".join(display_line(x) for x in lines[gs:ge + 1]))
        starts = [s for s in range(0, len(lines) - w + 1) if (s + w - 1 < gs or s > ge) and _window_ok(nl, s, s + w - 1)]
        if len(starts) > 600:                       # seeded subsample keeps the token-length filter cheap on 10k-line logs
            starts = sorted(rng.sample(starts, 600))
        # length matching: distractor windows within 0.6x-1.6x of the gold's tokens (the relaxed band 0.3x-3x is the fallback)
        def tok(s):
            return lc.approx_tokens("\n".join(display_line(x) for x in lines[s:s + w]))
        near = [s for s in starts if 0.6 * gold_tok <= tok(s) <= 1.6 * gold_tok]
        if len(near) >= 12:
            starts = near
        else:
            starts = [s for s in starts if 0.3 * gold_tok <= tok(s) <= 3 * gold_tok]
        hard = [s for s in starts if kws and any(any(kw in nl[i].lower() for kw in kws) for i in range(s, s + w))]
        sid = "logchunks:%s" % src["_src_line"]
        k_first = self.ksched.next(9)         # 9 > LARGE_LABEL_SET: alternates 4 / 8
        for k in sorted({k_first, 4 if k_first == 8 else k_first}, reverse=True):
            chosen = self._pick(rng, starts, hard, w, k - 1)
            if chosen is None:
                continue
            segs = [(gs, ge)] + [(s, s + w - 1) for s in chosen]
            order = list(range(len(segs)))
            lc.seeded_rng("logorder", self.seed, sid).shuffle(order)
            texts = []
            for disp, idx in enumerate(order):
                a, b = segs[idx]
                body = "\n".join(display_line(x) for x in lines[a:b + 1]).strip("\n")
                texts.append("[Segment %d]\n%s" % (disp + 1, body))
            context = "\n\n".join(texts)
            if lc.approx_tokens(context) > BUDGET_TOKENS:
                continue
            gold_disp = order.index(0) + 1
            return [{"form": FORM, "kind": "choice", "context": context,
                     "options": ["Segment %d" % (i + 1) for i in range(len(segs))], "gold_text": "Segment %d" % gold_disp,
                     "source_row_id": sid,
                     "extra": {"segments": [segs[i] for i in order], "gold_seg_display": gold_disp, "window_lines": w,
                               "span_n": len(segs), "span_lens": [w] * len(segs), "language": src["language"],
                               "repo": src["repo"], "category": src["category"]}}]
        self.drops.add("windows_over_token_budget", src["_src_line"])
        return []

    @staticmethod
    def _pick(rng, starts, hard, w, n):
        """n non-overlapping windows; about half from the keyword-hitting pool (hard) when it has them."""
        chosen = []

        def free(s):
            return all(abs(s - c) >= w for c in chosen)
        pools = [list(hard), list(starts)]
        rng.shuffle(pools[0])
        rng.shuffle(pools[1])
        want_hard = (n + 1) // 2
        for s in pools[0]:
            if len(chosen) >= want_hard:
                break
            if free(s):
                chosen.append(s)
        for s in pools[1]:
            if len(chosen) >= n:
                break
            if free(s):
                chosen.append(s)
        return chosen if len(chosen) == n else None

    def independent_gold(self, src, cand):
        """Recompute the gold segment by TEXT: the displayed segment whose normalised text contains every chunk line in order."""
        cl = [norm_line(c) for c in src["chunk"].replace("\r\n", "\n").split("\n")]
        cl = [c for c in cl if c]
        segs = cand["context"].split("\n\n[Segment ")
        for i, blk in enumerate(segs):
            body = blk.split("\n", 1)[1] if "\n" in blk else ""
            text = "\n".join(x for x in (norm_line(y) for y in body.split("\n")) if x)
            pos = 0
            for c in cl:
                q = text.find(c, pos)
                if q < 0:
                    pos = -1
                    break
                pos = q + len(c)
            if pos >= 0:
                return "Segment %d" % (i + 1)
        return "?"
