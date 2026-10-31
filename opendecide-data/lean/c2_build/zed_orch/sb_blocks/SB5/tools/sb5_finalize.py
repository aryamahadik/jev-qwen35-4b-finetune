"""SB5 QC finalize (A58 c; A66 a): the one writer of lean/data/c2_parts/SB5/qc/QC_REPORT.json after the A46 screen.

A66 (a) program fix. It re-derives EVERY binding non-G13 gate of SB5 from the files on disk at the unchanged A58 bars, writes
pass=true only when all of them pass (else pass=false with the reasons), records the sha256 of every input it read, lists the
gates it cannot evaluate as `gates_pending`, and writes only SB5's QC_REPORT.json (backup first).

Re-derived here (each is a check_* function; a failure appends a reason, an unreadable input or a crash also fails closed):
  files      MANIFEST vs disk (sha256 + rows, JSONL split on "\\n" only), screened work files == out/ and hold_owndev/, candidate rules
  gates      format gates (A58 c 5) RECOMPUTED with sb5_gates.run on the final files; the cached work/gates_*_screened.json must equal
             the recomputation (sha-bound, never trusted); tokens counted by the pinned tokenizer
  g1         G1 provenance + licence record (A58 a 1-4), the archive zip / rar shas on disk
  provenance every row (candidates and own dev) re-read against the archive on disk: text, label, gold, encoding, file sha
  a46        drop ids vs raw/screened files (exact set differences, byte-equal kept rows = nothing relabelled), the screen's
             inputs sha256, read completeness (SCORE.json, population), apply counts recomputed
  handoff    8.5 / deny-list / G-proxy handoff PASS records, the deny-list verdict bound to the query / list / program shas,
             the 8.5 binding input shas pinned by mix_c2.BINDING_INPUTS, C1-source-name and G-proxy-source checks recomputed
  crowd      C1 labels recomputed: coverage, bins vs the step-10 bars (easy <= 25%, hard <= 30%), p_g < 0.05 rows dropped
  selection  the official selection dry run recomputed (750, yes share 45-55%, bin bars, wordings), cached select_dry.json compared
  dev        own dev <= 150, disjoint from the candidates by id, source record (uci_rid) and normalised text, seeded hold-out re-drawn
  bench      step-4 exclusion recomputed: pins sha, self-test, 0 hits of every final candidate and dev row in the bench / pin / C2-dev
             indexes
Pending (not evaluated here): G13 incl. the OHS-AC path and A58 step 12, G9 official selection, the A61 final-mix 8.5 check, the
A58 step 11 joint pilot. a49c balance numbers are report-only for SB5 (not in mix_c2.A49C_BLOCKS) and are labelled so.

Usage: python -B sb5_finalize.py [--now ISO] [--write] [--dry-out SCRATCH.json]     (default is a DRY run: nothing is written; counts only on stdout)
--write backs the record on disk up to c2_build/_backup_a66/SB5/ first (verified by sha256) and refuses if it cannot."""
import datetime, functools, gzip, hashlib, json, os, random, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sb5_lib import *
import c2io

WRITER = Path(__file__).resolve()
ENC = "utf-8"
PINNED_TOKENIZER = "pinned Qwen3.5-4B tokenizer"
SB5_ID = "SB5_uci293"
DENY_KEY = "sb5_uci293_ar_twitter"
TARGET_ROWS, DEV_MAX = 750, 150
YES_LO, YES_HI = 0.45, 0.55
LOW_PG = 0.05
GENERIC_TERMS = {"tweet"}          # the builder's pre-check note: a bare generic word, not a key of this source
PENDING = [
    "G13 seed/candidates incl. the OHS-AC path (g13_c2.py over c2io.ALL_TARGETS, OHS-4 and OHS-AC exports counts-only, public anchors, G-proxy, C2 dev targets) "
    "and A58 step 12 (sob_text, sob_splits) on the final all-block mix: orchestrator batch; a hit drops the whole unit",
    "crowd selection, G9 official: c2_select.py select --fam SB5 (target 750; only the dry run is recomputed here)",
    "A61 final-mix 8.5 sealed-side source-name check for SB5_uci293 (A58 a 7 'again on the final mix'; mix_c2.py --final writes logs/a61_85_membership.json)",
    "A58 step 11 joint SB pilot (own-dev gain >= +2.0 pt, existing-dev drop <= 0.5 pt, G-proxy not rejected; orchestrator)",
]


# ------------------------------------------------------------------ context, small helpers

class Ctx:
    """Every path the writer reads or writes. Defaults are the real tree; tests point the mutable files at a copy."""
    def __init__(self, sb5=None, lean=None, part=None, c2=None, arch=None, bench=None, binding_inputs=None, backup_dir=None):
        self.sb5 = Path(sb5 or SB5); self.lean = Path(lean or LEAN); self.c2 = Path(c2 or C2)
        self.part = Path(part or self.lean / "data/c2_parts/SB5")
        self.arch = Path(arch or ARCH); self.bench = Path(bench or BENCH)
        self.work = self.sb5 / "work"; self.screen = self.sb5 / "screen"
        self.out = self.part / "out"; self.dev_path = self.part / "hold_owndev/mixdev_S5.jsonl"
        if not self.dev_path.exists() and (self.out / "mixdev_S5.jsonl").exists():
            self.dev_path = self.out / "mixdev_S5.jsonl"  # moved to out/ by the orchestrator at the batched G13 re-run (see the location note below)
        self.qc_path = self.part / "qc/QC_REPORT.json"
        self.backup_dir = Path(backup_dir or self.c2 / "_backup_a66/SB5")
        self.binding_inputs = binding_inputs          # None -> mix_c2.BINDING_INPUTS["SB5_uci293"] read when needed
        self.pins = self.sb5 / "bench_pins"
        self.denylist = self.lean / "data/c_parts/denylist.json"
        self.denylist_py = self.lean / "c_src/common/denylist.py"
        self.c1_names = self.c2 / "gblock/checks/c1_source_names.json"
        self.gproxy = self.c2 / "meta_src/gproxy/SOURCES.json"
        self.crowd_dir = self.lean / "data/c2_crowd_shards/SB5"
        self.labels_dir = self.crowd_dir / "labels_q35_4b_main500k"


class Rec:
    """Reasons (a non-empty list means pass=false) and the facts that go into the record."""
    def __init__(self):
        self.reasons, self.facts, self.shas = [], {}, {}
    def fail(self, msg): self.reasons.append(msg)
    def sha_of(self, ctx, path):
        """sha256 of a file the checks read, kept for the record's inputs_sha256 (key: path relative to lean/, else to the SB5 work dir)."""
        p = Path(path); s = sha(p.read_bytes())
        for base in (ctx.lean, ctx.sb5):
            try:
                self.shas[str(p.relative_to(base))] = s; break
            except ValueError:
                continue
        else:
            self.shas[str(p)] = s
        return s


def jl(b: bytes) -> list:
    """JSONL rows of a file's bytes: lines split on "\\n" ONLY (never str.splitlines: U+2028 / U+0085 / \\r are legal inside tweets)."""
    return [json.loads(l) for l in b.split(b"\n") if l.strip()]

def lines(b: bytes) -> list:
    return [l for l in b.split(b"\n") if l.strip()]

def J(p):
    return json.loads(Path(p).read_bytes().decode(ENC))

def wnorm(t):
    return " ".join(norm_tokens(t))


# ------------------------------------------------------------------ state

def load_state(ctx, R):
    """Read the final files and their raw / screened work files once."""
    S = {}
    S["man"] = J(ctx.out / "MANIFEST.json"); R.sha_of(ctx, ctx.out / "MANIFEST.json")
    S["cand_b"] = (ctx.out / c2io.CAND).read_bytes(); S["rel_b"] = (ctx.out / c2io.REL).read_bytes()
    S["dev_b"] = ctx.dev_path.read_bytes()
    S["cand"], S["dev"] = jl(S["cand_b"]), jl(S["dev_b"])
    S["raw_cand_b"] = (ctx.work / "candidates.jsonl").read_bytes(); S["raw_dev_b"] = (ctx.work / "owndev.jsonl").read_bytes()
    S["raw_cand"], S["raw_dev"] = jl(S["raw_cand_b"]), jl(S["raw_dev_b"])
    for p in (ctx.out / c2io.CAND, ctx.out / c2io.REL, ctx.dev_path, ctx.work / "candidates.jsonl", ctx.work / "owndev.jsonl"):
        R.sha_of(ctx, p)
    return S


# ------------------------------------------------------------------ check: files

def check_files(ctx, S, R):
    got, files = {}, {}
    for name, b in ((c2io.CAND, S["cand_b"]), (c2io.REL, S["rel_b"])):
        n = len(lines(b)); got[name] = (sha(b), n); files[name] = {"sha256": sha(b), "rows": n}
    for p in c2io.manifest_problems("SB5", S["man"], got):
        R.fail(p)
    if files[c2io.REL]["rows"] != 0:
        R.fail("relations file has rows: SB5 has no twins, it must be empty")
    dev_rows = len(S["dev"])
    mixdev = {"mixdev_S5.jsonl": {"sha256": sha(S["dev_b"]), "rows": dev_rows,
              "location": "data/c2_parts/SB5/hold_owndev/ (moved to out/ by the orchestrator at the batched G13 re-run)"}}
    if S["man"].get("own_dev", {}).get("mixdev_S5.jsonl", {}).get("sha256") != mixdev["mixdev_S5.jsonl"]["sha256"]:
        R.fail("own dev sha256 differs from the MANIFEST's")
    if S["man"].get("own_dev", {}).get("mixdev_S5.jsonl", {}).get("rows") != dev_rows:
        R.fail("own dev row count differs from the MANIFEST's")
    if S["cand_b"] != (ctx.work / "candidates_screened.jsonl").read_bytes():
        R.fail("out/candidates_c2.jsonl is not the A46-screened work file")
    if S["dev_b"] != (ctx.work / "owndev_screened.jsonl").read_bytes():
        R.fail("hold_owndev/mixdev_S5.jsonl is not the A46-screened own-dev work file")
    for p in c2io.candidate_problems("SB5", S["cand"]):
        R.fail(p)
    if len(S["cand"]) < TARGET_ROWS:
        R.fail(f"{len(S['cand'])} candidates < the {TARGET_ROWS}-row target")
    if {r["id"] for r in S["dev"]} & {r["id"] for r in S["cand"]}:
        R.fail("own dev ids overlap the candidates")
    if len({r["id"] for r in S["dev"]}) != dev_rows:
        R.fail("own dev has duplicate ids")
    S["files"], S["mixdev"] = files, mixdev
    R.facts["files"] = files


# ------------------------------------------------------------------ check: format gates (recomputed)

def check_gates(ctx, S, R):
    import sb5_gates
    out = {}
    for nm, path, b, rows, cached in (("candidates", ctx.out / c2io.CAND, S["cand_b"], S["cand"], ctx.work / "gates_candidates_screened.json"),
                                      ("owndev", ctx.dev_path, S["dev_b"], S["dev"], ctx.work / "gates_owndev_screened.json")):
        g = sb5_gates.run(str(path))                       # the format gates, recomputed from the final file
        if g["rows"] != len(rows) or g["rows"] != len(lines(b)):
            R.fail(f"format gates ({nm}): gate tool read {g['rows']} rows, the file has {len(lines(b))} \"\\n\"-split rows")
        if g.get("pass") is not True or any(g["failures"].values()):
            R.fail(f"format gates not 100% on the {nm} (recomputed): {[k for k, v in g['failures'].items() if v]}")
        if g["tokens"]["counted_by"] != PINNED_TOKENIZER:
            R.fail(f"format gates ({nm}): tokens were not counted by the pinned tokenizer ({g['tokens']['counted_by']!r})")
        g = dict(g, file=Path(path).name, input_sha256=sha(b))
        if Path(cached).exists():                          # a cached gate file is never trusted: it must equal the recomputation
            c = J(cached); R.sha_of(ctx, cached)
            same = {k: v for k, v in c.items() if k != "file"} == {k: v for k, v in g.items() if k not in ("file", "input_sha256")}
            if not same:
                R.fail(f"cached {Path(cached).name} differs from the recomputed gates (stale cache)")
            g["cached_gate_file"] = {"path": os.path.relpath(cached, ctx.lean), "sha256": sha(Path(cached).read_bytes()), "equals_recomputation": same}
        else:
            g["cached_gate_file"] = None
        out[nm] = g
    S["gates"] = out
    R.facts["gates_candidates_pass"], R.facts["gates_owndev_pass"] = out["candidates"]["pass"], out["owndev"]["pass"]
    # fix_iterations basis: the pre-screen gate files must show no failed gate round
    for nm, n in (("candidates", len(S["raw_cand"])), ("owndev", len(S["raw_dev"]))):
        p = ctx.work / f"gates_{nm}.json"
        c = J(p); R.sha_of(ctx, p)
        if c.get("pass") is not True or any(c["failures"].values()) or c["rows"] != n:
            R.fail(f"fix_iterations basis: the pre-screen gate file gates_{nm}.json shows a failed or stale gate round")


# ------------------------------------------------------------------ check: G1, archive, row provenance

def archive_by_rid(ctx):
    out = {}
    for lab, d in (("pos", "Positive"), ("neg", "Negative")):
        for p in sorted((ctx.arch / d).glob("*.txt")):
            b = p.read_bytes()
            try:
                s, enc = b.decode("utf-8-sig"), "utf-8"
            except UnicodeDecodeError:
                s, enc = b.decode("cp1256"), "cp1256"
            out[p.stem] = {"label": lab, "text": clean(s), "enc": enc, "file_sha": sha(b)[:16]}
    return out

def check_g1(ctx, S, R):
    g = J(ctx.sb5 / "G1_RECORD.json"); g1_sha = R.sha_of(ctx, ctx.sb5 / "G1_RECORD.json")
    S["g1"] = g
    if g.get("pass") is not True:
        R.fail("G1 record pass is not true")
    if g.get("block") != "SB5" or g.get("dataset", {}).get("uci_id") != 293:
        R.fail("G1 record is not the SB5 / UCI 293 record")
    lic = g.get("licence", {})
    if lic.get("spdx") != "CC-BY-4.0" or lic.get("page_check_passed") is not True or not str(lic.get("commercial_use_allowed", "")).lower().startswith("yes") \
            or "CC BY 4.0" not in str(lic.get("quote_uci_page", "")):
        R.fail("G1 licence: CC BY 4.0 / commercial use / official page check not all recorded")
    chk = g.get("A58_a_checks", {})
    for k in ("a1_allowed_licence_and_V", "a2_text_through_another_dataset", "a3_human_text_and_labels_only", "a4_train_split_only"):
        if not str(chk.get(k, "")).startswith("PASS"):
            R.fail(f"G1 record: A58 (a) check {k} is not PASS")
    if not g.get("label_method", {}).get("quote_uci_page_api_summary"):
        R.fail("G1 record has no label-method quote")
    if g.get("archive", {}).get("total_tweet_files") != 2000:
        R.fail("G1 record: archive is not the 2,000-file UCI 293 set")
    sh = g.get("sha256", {})
    zip_p, rar_p = ctx.sb5 / "src/uci293.zip", ctx.sb5 / "src/zip_out/Twitter.rar"
    for nm, p, key in (("zip", zip_p, "uci293.zip"), ("rar", rar_p, "Twitter.rar (inside the zip)")):
        if not p.exists():
            R.fail(f"{nm} not on disk: {p.name}")
        elif sha(p.read_bytes()) != sh.get(key):
            R.fail(f"{nm} sha256 on disk differs from the G1 record")
    S["zip_sha"], S["rar_sha"] = sh.get("uci293.zip"), sh.get("Twitter.rar (inside the zip)")
    R.facts["g1"] = {"zip_sha256": S["zip_sha"], "rar_sha256": S["rar_sha"], "licence": lic.get("spdx"), "record_sha256": g1_sha}

def check_provenance(ctx, S, R):
    """Every candidate and own-dev row against the archive on disk: nothing relabelled, nothing edited."""
    arch = archive_by_rid(ctx)
    if len(arch) != 2000:
        R.fail(f"archive on disk has {len(arch)} tweets, not 2,000")
    bad = Counter()
    lab = {"pos": "positive", "neg": "negative"}
    for part, rows in (("candidates", S["cand"]), ("owndev", S["dev"])):
        for r in rows:
            m = (r.get("meta") or {}).get("sb5") or {}
            x = arch.get(m.get("uci_rid"))
            if x is None:
                bad["rid_not_in_archive"] += 1; continue
            bad["state_differs_from_archive_text"] += r["state"] != x["text"]
            bad["file_sha_differs"] += m.get("file_sha256_16") != x["file_sha"]
            bad["label_differs_from_archive_dir"] += lab[x["label"]] != m.get("orig_label")
            bad["encoding_differs"] += m.get("encoding") != x["enc"]
            bad["gold_not_polarity_x_label"] += r["gold"] != int(str(m.get("orig_label"))[:3] == str(m.get("question_polarity")))
            bad["id_not_source_rid_polarity"] += r["id"] != f"c2_sb5:{m.get('uci_rid')}:{m.get('question_polarity')}"
            bad["source_not_c2_sb5"] += r.get("source") != "c2_sb5"
            bad["family_not_SB5"] += (r.get("meta") or {}).get("family") != "SB5"
            pv = m.get("provenance") or {}
            bad["row_zip_rar_sha_differs_from_G1"] += (pv.get("zip_sha256"), pv.get("rar_sha256")) != (S["zip_sha"], S["rar_sha"])
            bad["licence_not_cc_by_4"] += not str((r.get("meta") or {}).get("licence", "")).startswith("CC BY 4.0")
    for k, v in bad.items():
        if v:
            R.fail(f"row provenance: {v} row(s) with {k}")
    R.facts["provenance"] = {"rows_checked": len(S["cand"]) + len(S["dev"]), "problems": {k: v for k, v in bad.items() if v}}


# ------------------------------------------------------------------ check: A46 screen

def check_a46(ctx, S, R):
    deny = J(ctx.screen / "REPLAY_DENY_A46.json"); R.sha_of(ctx, ctx.screen / "REPLAY_DENY_A46.json")
    uns = J(ctx.screen / "REPLAY_UNSCREENED_A46.json"); R.sha_of(ctx, ctx.screen / "REPLAY_UNSCREENED_A46.json")
    drop_l = deny["drop_ids"]; drop = set(drop_l)
    if len(drop_l) != len(drop):
        R.fail("A46: duplicate ids in the drop list")
    if uns["drop_ids"]:
        R.fail("A46: unscreened rows remain")
    if not all(i.startswith("c2_sb5:") for i in drop):
        R.fail("A46: a drop id is not an SB5 row")
    inp_bad = []
    for rel, want in deny["inputs_sha256"].items():
        p = ctx.screen / rel
        if not p.exists() or sha(p.read_bytes()) != want:
            inp_bad.append(rel)
        else:
            R.sha_of(ctx, p)
    if inp_bad or not deny["inputs_sha256"]:
        R.fail(f"A46 inputs_sha256 differs from the files on disk (or is empty): {inp_bad}")
    rc, rd = S["raw_cand"], S["raw_dev"]
    rci, rdi = {r["id"] for r in rc}, {r["id"] for r in rd}
    fci, fdi = {r["id"] for r in S["cand"]}, {r["id"] for r in S["dev"]}
    if drop - (rci | rdi):
        R.fail(f"A46: {len(drop - (rci | rdi))} drop ids match no raw candidate or own-dev row")
    if rci - fci != drop & rci or rdi - fdi != drop & rdi:
        R.fail("A46: raw minus screened is not exactly the A46 drop ids (candidates or own dev)")
    if (fci | fdi) & drop:
        R.fail("A46: a drop id is still in the final candidates or own dev")
    # nothing relabelled or edited: the kept lines are the raw lines, in order, byte for byte
    for nm, rawb, finb, rows in (("candidates", S["raw_cand_b"], S["cand_b"], rc), ("own dev", S["raw_dev_b"], S["dev_b"], rd)):
        exp = [l for l, r in zip(lines(rawb), rows) if r["id"] not in drop]
        if exp != lines(finb):
            R.fail(f"A46: the kept {nm} rows are not byte-equal to the raw rows (relabelled or edited)")
    # screen completeness
    sc = J(ctx.screen / "reads/SCORE.json"); R.sha_of(ctx, ctx.screen / "reads/SCORE.json")
    n_all = len(rc) + len(rd)
    if sc.get("n_rows") != n_all or sc.get("n_incomplete") or sc.get("n_unread_refused") or sc.get("problems") or sc.get("incomplete"):
        R.fail("A46: the read score does not cover every raw row completely")
    bs = sc.get("by_source", {}).get("c2_sb5", {})
    if bs.get("rows") != n_all or bs.get("read_both") != n_all:
        R.fail("A46: not every row has both blind reads")
    pop = ctx.screen / "pool/population.jsonl.gz"
    pop_ids = {json.loads(l)["id"] for l in gzip.open(pop, "rt", encoding=ENC).read().split("\n") if l.strip()}
    R.sha_of(ctx, pop)
    if pop_ids != rci | rdi:
        R.fail("A46: the screened population is not the raw candidates + raw own dev")
    cnt = deny["counts"]
    if cnt["confirmed_rows"] != len(drop) or cnt["confirmed_wrong_gold"] + cnt["confirmed_ambiguous"] != cnt["confirmed_rows"] or cnt["opus_missing"]:
        R.fail("A46: the confirm counts do not match the drop list (or Opus verdicts are missing)")
    cg, dg = [r for r in rc if r["id"] in drop], [r for r in rd if r["id"] in drop]
    ap = {"deny_ids": len(drop), "candidates": [len(rc), len(S["cand"]), len(cg)], "owndev": [len(rd), len(S["dev"]), len(dg)],
          "ids_unmatched": len(drop - (rci | rdi)),
          "dropped_by_label": dict(Counter(r["meta"]["sb5"]["orig_label"] for r in cg + dg)),
          "dropped_by_answer": dict(Counter(r["gold"] for r in cg + dg)),
          "kept_cells": dict(Counter(f'{r["meta"]["sb5"]["orig_label"]}/{r["gold"]}' for r in S["cand"])),
          "deny_counts": cnt}
    cached = J(ctx.work / "apply_report.json"); R.sha_of(ctx, ctx.work / "apply_report.json")
    if cached != json.loads(json.dumps(ap)):       # JSON round trip: dict keys become strings, as in the cached file
        R.fail("A46: cached work/apply_report.json differs from the recomputed counts")
    S["drop"], S["apply"], S["a46_inputs"] = drop, ap, deny["inputs_sha256"]
    R.facts["a46"] = {"drop_ids": len(drop), "read_rows": n_all, "relabelled": 0}


# ------------------------------------------------------------------ check: handoff, deny-list, 8.5 inputs, C1 / G-proxy source names

def identifiers(ctx, S):
    h = J(ctx.sb5 / "HANDOFF_85_DENYLIST.json")
    ids = h["identifiers_for_the_8_5_sealed_side_source_name_check"]
    return h, ids

def binding_inputs(ctx):
    if ctx.binding_inputs is not None:
        return ctx.binding_inputs
    import mix_c2
    return mix_c2.BINDING_INPUTS[SB5_ID]

def check_handoff(ctx, S, R):
    h, ids = identifiers(ctx, S); R.sha_of(ctx, ctx.sb5 / "HANDOFF_85_DENYLIST.json")
    v = h.get("orchestrator_verdict", {})
    if v.get("8.5") != "PASS":
        R.fail("8.5 sealed-side source-name check (handoff orchestrator verdict) is not PASS")
    if not str(v.get("denylist", "")).startswith("PASS"):
        R.fail("deny-list handoff verdict is not PASS")
    if not str(v.get("gproxy_source", "")).startswith("PASS"):
        R.fail("G-proxy handoff verdict is not PASS")
    acts = {a["id"]: a for a in h.get("orchestrator_actions", [])}
    for k in ("8.5", "denylist", "g_proxy_source"):
        if not str(acts.get(k, {}).get("result", "")).startswith("PASS"):
            R.fail(f"handoff action {k} has no PASS result")
    # the deny-list verdict, bound to the query, list and program shas
    ver = J(ctx.sb5 / "denylist_verdict_sb5.json"); R.sha_of(ctx, ctx.sb5 / "denylist_verdict_sb5.json")
    qp = ctx.sb5 / "denylist_query_sb5.json"; q = J(qp); R.sha_of(ctx, qp)
    c = ver.get("counts", {})
    if any(c.get(k) for k in ("hit", "deny_taint", "no_new_rows", "ohs3_hit", "sealed_hit")) or c.get("datasets") != 1 or c.get("pass") != 1:
        R.fail(f"deny-list verdict counts are not a clean pass: {c}")
    vv = ver.get("verdicts", {}).get(DENY_KEY, {})
    if set(ver.get("verdicts", {})) != {DENY_KEY} or vv.get("verdict") != "pass" or vv.get("hit") or vv.get("taint_hits"):
        R.fail("deny-list verdict for the SB5 dataset is not pass / has hits")
    if set(q.get("datasets", {})) != {DENY_KEY} or q["datasets"][DENY_KEY].get("emits_rows") is not True:
        R.fail("deny-list query is not the single SB5 dataset query")
    if ver.get("query_sha256") != sha(qp.read_bytes()):
        R.fail("deny-list verdict query_sha256 differs from the query on disk")
    if ctx.denylist.exists() and ver.get("denylist_sha256") != sha(ctx.denylist.read_bytes()):
        R.fail("deny-list verdict was made against another deny-list than the one on disk")
    if ctx.denylist_py.exists() and ver.get("program_sha256") != sha(ctx.denylist_py.read_bytes()):
        R.fail("deny-list verdict was made by another denylist.py than the one on disk")
    if ver.get("canonical") is not True or ver.get("run") != "sb5":
        R.fail("deny-list verdict is not a canonical sb5 run")
    # 8.5 binding inputs (the pins mix_c2 uses), and that they carry this source
    for path, want in binding_inputs(ctx):
        p = Path(path)
        if not p.exists() or sha(p.read_bytes()) != want:
            R.fail(f"8.5 binding input {p.name} sha256 differs from the pin")
            continue
        R.sha_of(ctx, p)
        srcs = {s["id"]: s for s in J(p)["sources"]}
        s0 = srcs.get(SB5_ID)
        if s0 is None or s0.get("name") != ids["dataset_name"] or s0.get("host") != ids["host"]:
            R.fail(f"8.5 binding input {p.name} does not carry the SB5 source with the handoff identifiers")
    # C1 source names (recomputed against the cached C1 name list, sha-bound) and G-proxy sources
    terms = {t.casefold() for t in [ids["dataset_name"], ids["host"], ids["doi"], *ids["alt_names"], "uci", "arabic", "abdulla", "twitter", "jordanian", "aeect", "mahyoub"]}
    terms -= GENERIC_TERMS
    names = [n.casefold() for n in J(ctx.c1_names)["names"]]; R.sha_of(ctx, ctx.c1_names)
    hits = sorted(t for t in terms if any(re.search(r"(?<![0-9a-z])" + re.escape(t) + r"(?![0-9a-z])", n) for n in names))
    if hits:
        R.fail(f"C1 source names: SB5 identifiers appear in C1's sources: {hits}")
    gp = J(ctx.gproxy)["sources"]; R.sha_of(ctx, ctx.gproxy)
    gp_hosts = {x.casefold() for s in gp for x in [s.get("host", ""), *s.get("other_hosts", [])] if x}
    gp_names = {x.casefold() for s in gp for x in [s.get("id", ""), s.get("name", ""), s.get("upstream_id", "")] if x}
    mine_names = {x.casefold() for x in [ids["dataset_name"], *ids["alt_names"], ids["upstream_id"]]}
    if ids["host"].casefold() in gp_hosts or any(a in b or b in a for a in mine_names for b in gp_names):
        R.fail("G-proxy source check: an SB5 identifier matches a G-proxy source name or host")
    R.facts["handoff"] = {"8.5": v.get("8.5"), "denylist": "pass, 0 hit, 0 taint", "g_proxy_source": "PASS (recomputed against meta_src/gproxy/SOURCES.json: no host / name match)",
                          "c1_source_names": f"{len(names)} names, {len(terms)} terms, 0 hits (generic {sorted(GENERIC_TERMS)} excluded)",
                          "8.5_note": "PASS recorded by the orchestrator 17 Oct 03:36 UTC (sealed side, not re-derivable here); the A61 final-mix 8.5 check is pending"}


# ------------------------------------------------------------------ check: crowd labels, bins, p_g < 0.05

def check_crowd(ctx, S, R):
    sys.path.insert(0, str(LEAN))                      # code (shard_golden, c2_select) always from the real tree; ctx.lean holds data only
    import shard_golden as sg, c2_select as CS
    import crowd_select as cs
    probs, view = sg.load_labels(ctx.labels_dir, ctx.crowd_dir, return_view=True)
    why = CS.view_problem(view, CS.C1)
    if why:
        R.fail(f"crowd labels: {why}")
    sh = J(ctx.crowd_dir / "shards.json"); R.sha_of(ctx, ctx.crowd_dir / "shards.json")
    if sh.get("candidates_sha256") != sha(S["raw_cand_b"]):
        R.fail("crowd shards.json candidates_sha256 is not the raw (pre-A46) candidates file")
    if sh.get("rows") != len(S["raw_cand"]):
        R.fail("crowd shards.json row count is not the raw candidate count")
    rows, raw = S["cand"], S["raw_cand"]
    ids = {r["id"] for r in rows}; rawids = {r["id"] for r in raw}
    if sum(i in probs for i in ids) != len(ids):
        R.fail(f"crowd labels cover {sum(i in probs for i in ids)} of {len(ids)} candidates")
    if set(probs) != rawids:
        R.fail("crowd labels are not exactly the pre-A46 candidates")
    surplus = sorted(set(probs) - ids)
    if not set(surplus) <= S["drop"]:
        R.fail("surplus crowd labels include ids that A46 did not drop")
    pg_all = {r["id"]: cs.p_gold(r, probs[r["id"]]) for r in raw if r["id"] in probs}
    pg = {i: pg_all[i] for i in ids if i in pg_all}
    S["probs"], S["pg"] = probs, pg
    def shares(ps):
        c = Counter(cs.bin_of(x) for x in ps)
        return {b: c.get(b, 0) for b in ("easy", "medium", "hard")}, {b: round(c.get(b, 0) / max(1, len(ps)), 4) for b in ("easy", "medium", "hard")}
    bins_raw, sh_raw = shares(pg_all.values()); bins_fin, sh_fin = shares(pg.values())
    for nm, s in (("pre-A46 pool", sh_raw), ("final candidates", sh_fin)):
        if s["easy"] > cs.CAP["easy"] + 1e-12 or s["hard"] > cs.CAP["hard"] + 1e-12:
            R.fail(f"step-10 crowd bars on the {nm}: easy {s['easy']} (<= {cs.CAP['easy']}), hard {s['hard']} (<= {cs.CAP['hard']})")
    low_raw = sorted(i for i, x in pg_all.items() if x < LOW_PG)
    if set(low_raw) - S["drop"]:
        R.fail(f"p_g < {LOW_PG} rows were not dropped by A46: {len(set(low_raw) - S['drop'])}")
    low_fin = [i for i, x in pg.items() if x < LOW_PG]
    if low_fin:
        R.fail(f"{len(low_fin)} final candidates have p_g < {LOW_PG}")
    summ = J(ctx.work / "crowd_summary.json"); R.sha_of(ctx, ctx.work / "crowd_summary.json")
    if summ.get("rows") != len(raw) or summ.get("bins") != {b: n for b, n in bins_raw.items() if n} or summ.get("p_g_lt_0.05") != len(low_raw) \
            or sorted(summ.get("low_pg_ids", [])) != low_raw:
        R.fail("cached work/crowd_summary.json differs from the recomputed bins / low-p_g rows")
    S["crowd_summary"] = summ
    S["crowd"] = {"labels_dir": os.path.relpath(ctx.labels_dir, ctx.lean), "candidates_labelled": sum(i in probs for i in ids), "candidates": len(ids),
                  "labels_total": len(probs), "surplus_labels": len(surplus), "surplus_all_a46_dropped": set(surplus) <= S["drop"],
                  "read_on": f"the {len(raw)} pre-A46 candidates (shards.json candidates_sha256 {sh.get('candidates_sha256', '')[:8]}...); the surplus labels belong to the A46-dropped rows and are never used",
                  "bins_pre_a46": bins_raw, "bin_shares_pre_a46": sh_raw, "bins_final_candidates": bins_fin, "bin_shares_final": sh_fin,
                  "bars": dict(cs.CAP), "p_g_lt_0.05_pre_a46": len(low_raw), "p_g_lt_0.05_dropped_by_a46": len(set(low_raw) & S["drop"]),
                  "p_g_lt_0.05_final_candidates": len(low_fin), "summary": summ}
    R.facts["crowd"] = {"labelled": S["crowd"]["candidates_labelled"], "bins_final": bins_fin, "p_g_lt_0.05_final": len(low_fin)}


# ------------------------------------------------------------------ check: selection dry run (recomputed)

def a49c_blocks():
    import mix_c2
    return mix_c2.A49C_BLOCKS

def check_selection(ctx, S, R):
    sys.path.insert(0, str(LEAN))                      # code (shard_golden, c2_select) always from the real tree; ctx.lean holds data only
    import c2_select as CS, crowd_select as cs
    rows, pg = S["cand"], S["pg"]
    try:
        rec = CS.select_family("SB5", rows, [], pg, TARGET_ROWS)
    except SystemExit as e:
        R.fail(f"selection dry run refused: {e}"); return
    sel = set(rec["selected_ids"]); sr = [r for r in rows if r["id"] in sel]
    yes = sum(r["gold"] for r in sr) / len(sr)
    bins = Counter(rec["difficulty_bin"][i] for i in sel)
    wc = Counter(r["meta"]["wording_id"] for r in sr)
    out = {"rows": len(rows), "selected": len(sel), "yes_share": round(yes, 4),
           "labels": dict(Counter(r["meta"]["sb5"]["orig_label"] for r in sr)), "bins": dict(bins), "wordings": len(wc),
           "a49c_failing": rec["report"]["a49c"]["failing"],
           "g5": {k: (len(v) if hasattr(v, "__len__") else v) for k, v in rec["g5"].items()} if isinstance(rec["g5"], dict) else str(rec["g5"])[:200],
           "mean_pg_selected": round(sum(pg[i] for i in sel) / len(sel), 4)}
    if len(sel) != TARGET_ROWS:
        R.fail(f"selection dry run selects {len(sel)} rows, not {TARGET_ROWS}")
    if not YES_LO <= yes <= YES_HI:
        R.fail(f"selection dry run yes share {yes:.4f} is outside 45-55% (G10)")
    if bins.get("easy", 0) / len(sel) > cs.CAP["easy"] + 1e-12 or bins.get("hard", 0) / len(sel) > cs.CAP["hard"] + 1e-12:
        R.fail(f"selection dry run bins {dict(bins)} break the step-10 bars (easy <= 25%, hard <= 30%)")
    if len(wc) < 4 or max(wc.values()) / len(sel) > 0.35:
        R.fail("selection dry run: fewer than 4 wordings or one above 35% of the selected rows")
    if any(pg[i] < LOW_PG for i in sel):
        R.fail("selection dry run holds a p_g < 0.05 row")
    if any(r["gold"] not in (0, 1) for r in sr):
        R.fail("selection dry run holds a non yes/no gold")
    cached = J(ctx.work / "select_dry.json"); R.sha_of(ctx, ctx.work / "select_dry.json")
    if cached != json.loads(json.dumps(out)):
        R.fail("cached work/select_dry.json differs from the recomputed selection dry run")
    binding = "SB5" in a49c_blocks()
    if binding and out["a49c_failing"]:
        R.fail(f"A49 c checks fail on the selected rows and bind for SB5: {out['a49c_failing']}")
    out = dict(out, a49c_failing_is_binding_for_SB5=binding,
               a49c_note="report-only for SB5: SB5 is not in mix_c2.A49C_BLOCKS, so these numbers are reported (mix_c2 re-asserts only for binding blocks), not evaluated as a gate")
    S["sel"] = out
    R.facts["selection"] = {"selected": len(sel), "yes_share": out["yes_share"], "bins": out["bins"]}


# ------------------------------------------------------------------ check: own dev

def check_dev(ctx, S, R):
    dev, cand = S["dev"], S["cand"]
    if len(dev) > DEV_MAX:
        R.fail(f"own dev has {len(dev)} rows > {DEV_MAX}")
    rid = lambda r: r["meta"]["sb5"]["uci_rid"]
    if {rid(r) for r in dev} & {rid(r) for r in cand}:
        R.fail("own dev and candidates share a source record (uci_rid)")
    if {wnorm(r["state"]) for r in dev} & {wnorm(r["state"]) for r in cand}:
        R.fail("own dev and candidates share a normalised text")
    pool = J(ctx.work / "pool.json"); R.sha_of(ctx, ctx.work / "pool.json")
    dev_ids = list(pool["dev_ids"])
    kept = pool["kept"]
    redraw = []
    for lab in ("pos", "neg"):
        xs = sorted((r for r in kept if r["label"] == lab), key=lambda r: h("holdout", r["rid"]))
        redraw += [r["rid"] for r in xs[:75]]
    if dev_ids != redraw:
        R.fail("pool.json dev_ids are not the seeded (20261013) label-stratified 75+75 hold-out re-drawn from the kept pool")
    pool_dev, pool_cand = set(dev_ids), {r["rid"] for r in kept} - set(dev_ids)
    if {rid(r) for r in S["raw_dev"]} != pool_dev:
        R.fail("raw own dev is not the pool's hold-out")
    if {rid(r) for r in cand} - pool_cand or {rid(r) for r in dev} - pool_dev:
        R.fail("a candidate is outside the non-hold-out pool or an own-dev row outside the hold-out")
    R.facts["dev"] = {"rows": len(dev), "max": DEV_MAX, "shared_uci_rid": 0, "shared_text": 0}


# ------------------------------------------------------------------ check: bench exclusion (step 4), recomputed

@functools.lru_cache(maxsize=4)
def _targets(pins, bench, lean, own_part):
    import pyarrow.parquet as pq
    pins, bench = Path(pins), Path(bench)
    def build(items):
        ix = Index()
        for it in items:
            for s in segments(it):
                ix.add("t", s)
        return ix
    t = {}
    bi = []
    for p in [bench / "text_track/data/cases.jsonl"] + sorted((bench / "data").glob("*/cases.jsonl")):
        for l in open(p, encoding=ENC):
            o = json.loads(l); bi.append({"state": o.get("state"), "questions": o.get("questions")})
    t["bench_cases"] = build(bi)
    t["tweet_sentiment_ar_test_full"] = build(json.loads(l) for l in gzip.open(pins / "mteb__tweet_sentiment_multilingual/test/arabic.jsonl.gz", "rt", encoding=ENC))
    t["osact4_validation_full"] = build(pq.read_table(pins / "arbml__OSACT4_hatespeech/data/validation-00000-of-00001.parquet").to_pylist())
    mi = []
    for sub in ("SetFit__amazon_massive_scenario_ar-SA", "SetFit__amazon_massive_intent_ar-SA"):
        mi += [json.loads(l) for l in open(pins / sub / "test.jsonl", encoding=ENC)]
    t["massive_ar_test_full"] = build(mi)
    t["xnli_ar_test_full"] = build(pq.read_table(pins / "facebook__xnli/ar/test-00000-of-00001.parquet").to_pylist())
    import glob
    cx, paths = Index(), []
    for pat in ("data/c2_mixdev.jsonl", "data/c2_transfer_dev.jsonl", "data/c2_parts/*/out/mixdev_S5.jsonl", "data/*dev*.jsonl", "data/*eval*.jsonl"):
        for p in sorted(glob.glob(str(Path(lean) / pat))):
            if own_part in p or c2io.refusal(p) or c2io.refusal(os.path.realpath(p)) or p in paths:
                continue
            paths.append(p)
    for p in paths:
        with open(p, encoding=ENC) as f:
            for l in f:
                if AR.search(l):
                    for s in segments(json.loads(l)):
                        cx.add("c2_dev_eval", s)
    t["c2_dev_eval"] = cx
    return t, len(paths)

def check_bench(ctx, S, R):
    pins = J(ctx.pins / "SHA256.json"); R.sha_of(ctx, ctx.pins / "SHA256.json")
    pin_files = {"mteb/tweet_sentiment_multilingual:test/arabic.jsonl.gz": "mteb__tweet_sentiment_multilingual/test/arabic.jsonl.gz",
                 "arbml/OSACT4_hatespeech:data/validation-00000-of-00001.parquet": "arbml__OSACT4_hatespeech/data/validation-00000-of-00001.parquet",
                 "SetFit/amazon_massive_scenario_ar-SA:test.jsonl": "SetFit__amazon_massive_scenario_ar-SA/test.jsonl",
                 "SetFit/amazon_massive_intent_ar-SA:test.jsonl": "SetFit__amazon_massive_intent_ar-SA/test.jsonl"}
    for k, rel in pin_files.items():
        p = ctx.pins / rel
        if k not in pins or not p.exists() or sha(p.read_bytes()) != pins[k]:
            R.fail(f"bench pin {k} differs from SHA256.json (or is missing)")
    xn = ctx.pins / "facebook__xnli/ar/test-00000-of-00001.parquet"
    if not xn.exists():
        R.fail("bench pin xnli ar test is missing")
    targets, n_dev_files = _targets(str(ctx.pins), str(ctx.bench), str(ctx.lean), str(ctx.part))
    prep = J(ctx.work / "prep_report.json"); R.sha_of(ctx, ctx.work / "prep_report.json")
    if prep["bench_dev_exclusion_drops"]:
        R.fail("bench exclusion: the prep step dropped source rows (unexpected for SB5, recorded as found)")
    # self-test of the index on the pin it must catch
    segs = [json.loads(l)["text"] for l in gzip.open(ctx.pins / "mteb__tweet_sentiment_multilingual/test/arabic.jsonl.gz", "rt", encoding=ENC)]
    ix = Index()
    for s in segs:
        ix.add("t", s)
    rng = random.Random(1); pick = [s for s in segs if len(norm_tokens(s)) >= 8]; rng.shuffle(pick); pick = pick[:40]
    exact = sum(bool(ix.hit(s)) for s in pick); drop1 = sum(bool(ix.hit(" ".join(s.split()[1:]))) for s in pick)
    if not pick or exact != len(pick) or drop1 != len(pick):
        R.fail(f"bench exclusion self-test failed: exact {exact}/{len(pick)}, one-token-dropped {drop1}/{len(pick)}")
    hits = Counter()
    for part, rows in (("candidates", S["cand"]), ("owndev", S["dev"])):
        for r in rows:
            for name, tix in targets.items():
                if tix.hit(r["state"]):
                    hits[f"{part}:{name}"] += 1
    if hits:
        R.fail(f"bench exclusion: final rows hit a bench / pin / C2-dev index: {dict(hits)}")
    st = J(ctx.work / "exclusion_selftest.json"); R.sha_of(ctx, ctx.work / "exclusion_selftest.json")
    if st.get("uci_tweets_hit") or st.get("exact_hits") != st.get("probe") or st.get("drop_first_token_hits") != st.get("probe"):
        R.fail("cached exclusion_selftest.json shows hits or a failed self-test")
    seg_n = {name: tix.n_seg for name, tix in targets.items()}
    for k in ("bench_cases", "tweet_sentiment_ar_test_full", "osact4_validation_full", "massive_ar_test_full", "xnli_ar_test_full"):
        if seg_n[k] != prep["target_arabic_segments"].get(k):
            R.fail(f"bench exclusion: target {k} now has {seg_n[k]} segments, prep saw {prep['target_arabic_segments'].get(k)} (bench or pin changed)")
    S["bench"] = {"method": "program only (sb5_prep.py index; recomputed here by sb5_finalize.py): normalised segments, exact + near-exact (drop-first-token) index; no agent read bench text",
                  "targets_arabic_segments": seg_n, "pins": pins, "c2_dev_eval_files_now": n_dev_files,
                  "prep_c2_dev_eval_files": prep["c2_dev_eval_files"], "prep_c2_dev_eval_arabic_rows": prep["c2_dev_eval_arabic_rows"],
                  "source_rows_dropped_by_target": prep["bench_dev_exclusion_drops"], "source_rows_dropped_total": sum(prep["bench_dev_exclusion_drops"].values()),
                  "final_rows_hit": dict(hits), "final_rows_checked": len(S["cand"]) + len(S["dev"]),
                  "self_test": {"pins_segments": len(segs), "probe": len(pick), "exact_hits": exact, "drop_first_token_hits": drop1},
                  "scope_note": "Arabic-script segments only (every SB5 row has Arabic letters); the English-only full splits (sst5, sst2, boolq, xnli en/fr) are covered by the A58 step 12 G13 target sob_splits at the batched run"}
    R.facts["bench"] = {"final_rows_hit": sum(hits.values()), "self_test": f"{exact}/{len(pick)} + {drop1}/{len(pick)}"}


# ------------------------------------------------------------------ run, record, write

CHECKS = (check_files, check_gates, check_g1, check_provenance, check_a46, check_handoff, check_crowd, check_selection, check_dev, check_bench)

def parse_utc(s):
    try:
        t = datetime.datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None
    return t if t.tzinfo else None

def evaluate(ctx, now, checks=CHECKS, admission=True):
    """-> (qc record, Rec). Every check runs; an exception in one fails closed (a reason) and later checks that need its state fail too."""
    R = Rec(); S = {}
    try:
        S = load_state(ctx, R)
    except Exception as e:
        R.fail(f"inputs unreadable: {type(e).__name__}: {str(e)[:160]}")
        return build_record(ctx, S, R, now), R
    for fn in checks:
        try:
            fn(ctx, S, R)
        except (Exception, SystemExit) as e:
            R.fail(f"{fn.__name__} could not be completed: {type(e).__name__}: {str(e)[:160]}")
    qc = build_record(ctx, S, R, now)
    if qc["pass"] and admission:                       # the mixer's own admission test on the record about to be written
        try:
            adm = admission_check(ctx, qc)
        except Exception as e:
            adm = [f"admission self-check could not run: {type(e).__name__}: {str(e)[:160]}"]
        if adm:
            R.reasons += adm
            qc = build_record(ctx, S, R, now)
    return qc, R

def build_record(ctx, S, R, now):
    t = parse_utc(now)
    if t is None:
        R.fail("--now is not an ISO 8601 time with a UTC offset")
    ok = not R.reasons
    qc = {"pass": ok, "passed_utc": now if ok else None,
          "stage": "final (A46 screened; format gates recomputed at 100%; every non-G13 gate re-derived by the A66 writer; G13 deferred to the batched all-block run)",
          "family": "SB5", "ruling": "A58 (adopted 17 Oct 03:40 UTC; E1); record writer A66 (a)", "source": "UCI 293 Arabic tweets, train rows only (CC BY 4.0)",
          "fix_iterations": 0,
          "fix_iterations_basis": "no gate failed (the pre-screen gate files show 100% and are re-checked) and no regeneration or fix round took place; the A46 label-noise screen (A58 c 6) is a pre-registered step with drop-only outcomes, not a fix iteration",
          "reasons_not_passed": list(R.reasons)}
    qc["files"] = S.get("files"); qc["mixdev"] = S.get("mixdev")
    qc["bench_exclusion_step4"] = S.get("bench")
    qc["a46"] = ({"reads": "2 blind Haiku", "confirmed": S["apply"]["deny_counts"], "dropped_candidates": S["apply"]["candidates"][2], "dropped_owndev": S["apply"]["owndev"][2],
                  "relabelled": 0, "inputs_sha256": S.get("a46_inputs"), "kept_rows_byte_equal_to_raw": True} if "apply" in S else None)
    qc["apply"] = S.get("apply")
    g = S.get("gates") or {}
    qc["gates_candidates"], qc["gates_owndev"] = g.get("candidates"), g.get("owndev")
    qc["g1_provenance"] = R.facts.get("g1")
    qc["handoff_85_denylist_gproxy"] = R.facts.get("handoff")
    qc["row_provenance"] = R.facts.get("provenance")
    qc["own_dev_check"] = R.facts.get("dev")
    qc["crowd"] = S.get("crowd")
    qc["selection_dry_run"] = S.get("sel")
    gp = ctx.work / "probe_report.json"
    qc["g6_report_only"] = J(gp) if gp.exists() else None
    qc["rederived_checks"] = [fn.__name__.replace("check_", "") for fn in CHECKS]
    qc["inputs_sha256"] = dict(sorted(R.shas.items()))
    qc["writer"] = {"path": "c2_build/zed_orch/sb_blocks/SB5/tools/sb5_finalize.py", "sha256": sha(WRITER.read_bytes()), "ruling": "A66 (a, b)"}
    qc["gates_pending"] = list(PENDING)
    return qc

def admission_check(ctx, qc):
    """The mixer's own admission test on the record about to be written (only meaningful when every re-derivation passed)."""
    import mix_c2
    files = {c2io.CAND: ctx.out / c2io.CAND, c2io.REL: ctx.out / c2io.REL}
    binding = mix_c2.mx.qc_binding(qc, files)
    why = mix_c2.admission("SB5", qc, binding)
    return binding + why

class WriteRefused(Exception):
    pass

def write_record(ctx, qc, guard):
    """Backup first, verified by sha256; refuse if the backup cannot be made. Atomic replace, read-back check, out/ and hold_owndev/ untouched."""
    target = ctx.qc_path
    if target != ctx.part / "qc" / "QC_REPORT.json":
        raise WriteRefused("not SB5's QC_REPORT.json")
    if target.exists():
        cur = target.read_bytes()
        bp = ctx.backup_dir / f"QC_REPORT.before_write_{sha(cur)[:12]}.json"
        try:
            ctx.backup_dir.mkdir(parents=True, exist_ok=True)
            if bp.exists() and bp.read_bytes() != cur:
                raise WriteRefused(f"backup {bp.name} exists with other content")
            if not bp.exists():
                bp.write_bytes(cur)
            if not bp.exists() or sha(bp.read_bytes()) != sha(cur):
                raise WriteRefused("backup could not be verified")
        except OSError as e:
            raise WriteRefused(f"backup failed: {e}")
    new = (json.dumps(qc, indent=1, ensure_ascii=False) + "\n").encode(ENC)
    tmp = target.with_name(target.name + ".tmp")
    tmp.write_bytes(new); os.replace(tmp, target)
    if target.read_bytes() != new:
        raise WriteRefused("read-back differs")
    for p, s in guard.items():
        if sha(Path(p).read_bytes()) != s:
            raise WriteRefused(f"{p} changed during the write")
    return sha(new)

def main(argv):
    if "--write" in argv and "--dry" in argv:
        sys.exit("--write and --dry together: refused")
    write = "--write" in argv
    now = argv[argv.index("--now") + 1] if "--now" in argv else datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    ctx = Ctx()
    guard = {p: sha(Path(p).read_bytes()) for p in (ctx.out / c2io.CAND, ctx.out / c2io.REL, ctx.dev_path, ctx.out / "MANIFEST.json")}
    qc, R = evaluate(ctx, now)
    if "--dry-out" in argv:                              # the would-be record to a scratch file (never SB5's real record)
        dp = Path(argv[argv.index("--dry-out") + 1]).resolve()
        if dp == ctx.qc_path.resolve():
            sys.exit("--dry-out may not be the real record")
        dp.write_text(json.dumps(qc, indent=1, ensure_ascii=False) + "\n", encoding=ENC)
    wrote = None
    if write:
        wrote = write_record(ctx, qc, guard)
    print(json.dumps({"pass": qc["pass"], "passed_utc": qc["passed_utc"], "fix_iterations": qc["fix_iterations"], "reasons": qc["reasons_not_passed"],
                      "files": qc["files"], "facts": R.facts, "gates_pending": len(qc["gates_pending"]), "written": bool(wrote), "record_sha256": wrote,
                      "dry": not write, "writer_sha256": qc["writer"]["sha256"]}, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1:])
