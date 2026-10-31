#!/usr/bin/env python3
"""formats-1 QC: previews, lints, sealed id-only check on every output, deny-list run, path check, manifest.

Run from the formats-1 folder:  ../../../../.venv/bin/python qc/run_qc.py [--skip-sealed]
Prints counts only. The sealed checker is run as a program (never read, never edited); only its id-level output files
for OUR inputs are read back (hit ids and kinds), never its exports.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT.parents[2]
PY = str(LEAN.parent / ".venv" / "bin" / "python")
SEALED = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
DENY = LEAN / "c_src" / "common" / "denylist.py"
QC = ROOT / "qc"
TMP = ROOT / "tmp"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(LEAN))

from fixtures import NOTE, QUESTION, WORDING, card_for, choice_case, defs_block, doc_for  # noqa: E402
from fmt1 import card, labels, pool  # noqa: E402

INPUT_PATHS = [
    "c_spec/C_DATA_SPEC.md", "c_spec/C_TRAIN_RECIPE.md", "PREREG_FINAL.md",
    "c_src/common/MARKERS.md", "c_src/common/denylist.py", "c_src/common/negcount.py",
    "decoder_io.py",  # v1.1: the A16 readout (cygnet_msg, card_defs, user_msg) that loader_check runs
] + [f"c_src/{f}/G0_SPEC.md" for f in ["COMMIT"] + [f"F{i}" for i in range(1, 14)]]
VERSION = "formats-1 v1.1"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_previews() -> Path:
    """Rendered placeholder previews (not rows): every style, every defs variant x card style, few-shot, inverted,
    masked IDs and swapped names, so the sealed check also sees the composed chrome."""
    out = []
    for i, st in enumerate(pool.styles(held_out=None)):
        r = card.render_row_text(st, doc=doc_for(st["skin"]), question=QUESTION, qtype="noul", card=card_for(i),
                                 wording=WORDING, note=NOTE)
        out.append({"id": f"PV-{st['id']}", "kind": "preview_not_a_row", "qtype": "noul", **r})
        c = choice_case(i)
        r = card.render_row_text(st, doc=doc_for(st["skin"]), question=c["question"], qtype="choice", card=c["card"],
                                 options=c["options"], wording=c["wording"], note=c["note"])
        out.append({"id": f"PV-{st['id']}-choice", "kind": "preview_not_a_row", "qtype": "choice",
                    "options": c["options"], **r})
    for cs in pool._load("card_styles.jsonl"):
        st = {**pool.styles(held_out=None)[0], "card_style": cs["id"], "instr_position": "IP1"}
        for v in [o for o in pool._load("defs_styles.jsonl") if o.get("kind") == "defs_variant"]:
            if v["style"] == "none":
                continue
            ents = [{"name": "Label one", "text": "text one"}, {"name": "Label two", "text": "text two"}]
            blk = {"type": "defs", "variant": v["id"], "heading": "Definitions", "entries": ents}
            if v["style"] == "one_line_examples" or v.get("ex_mode") == "after_table":
                ents[0]["examples"] = ["example one"]
            if v["style"] == "rubric_table":
                blk["columns"] = ["Label", "Meaning"]
            if v["style"] == "decision_list" and not v.get("named"):
                for e in ents:
                    e.pop("name")
            if v["style"] == "short":
                for e in ents:
                    e.pop("text")
            out.append({"id": f"PV-{cs['id']}-{v['id']}", "kind": "preview_not_a_row",
                        "card": card.render_card({"title": "Card", "blocks": [blk]}, st)})
    st0 = pool.styles(held_out=None)[0]
    for t in pool._load("fewshot_templates.jsonl"):
        ex = [{"case": "Case text one", "answer": "Label one"}, {"case": "Case text two", "answer": "Label two"}]
        if t.get("needs_note"):
            for e in ex:
                e["note"] = "Reason text."
        out.append({"id": f"PV-{t['id']}", "kind": "preview_not_a_row", "card": card.render_card(
            {"blocks": [{"type": "fewshot", "template": t["id"], "heading": None, "examples": ex}]}, st0)})
    for q in pool.inverted_all("inverted_question"):
        out.append({"id": f"PV-{q['id']}", "kind": "preview_not_a_row",
                    "instructions": card.inverted_question(q["id"], "rule 4")})
    for r in pool.inverted_all("inverted_case_ref"):
        out.append({"id": f"PV-{r['id']}", "kind": "preview_not_a_row",
                    "options": card.case_refs(r["id"], 6, "preview")})
    for m in pool._load("label_masks.jsonl"):
        out.append({"id": f"PV-{m['id']}", "kind": "preview_not_a_row",
                    "options": labels.masked_ids(m["id"], 12, "preview")})
    for k in range(20):
        out.append({"id": f"PV-SWAP-{k:02d}", "kind": "preview_not_a_row",
                    "options": labels.swapped_names("mixed" if k % 2 else "group", 6, f"preview{k}")})
    p = QC / "previews.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False, sort_keys=True) + "\n")
    return p


def loader_stats() -> dict:
    """card.loader_check (decoder_io cygnet, schema_branch_mark, random option order) over every style x {choice,
    yes/no} and every card style x definition variant x {choice, yes/no}; plus the v1.0 path measured the same way
    (render_card text in a choice row's card field), which the review found hidden."""
    styles = pool.styles(held_out=None)
    res = {"decoder_io_sha256": card.DECODER_IO_SHA256, "layout": card.SERVE_LAYOUT, "style": card.SERVE_STYLE}
    ok = {"choice": 0, "noul": 0}
    old = {"full": 0, "part": 0, "none": 0}
    forms, routes = {}, {}
    for i, st in enumerate(styles):
        c = choice_case(i)
        ms = card.must_show(c["card"], question=c["question"], wording=c["wording"], note=c["note"])
        r = card.render_row_text(st, doc=doc_for(st["skin"]), question=c["question"], qtype="choice", card=c["card"],
                                 options=c["options"], wording=c["wording"], note=c["note"])
        row = {"id": f"q-{st['id']}", "qtype": "choice", "options": c["options"], "gold": c["gold"], **r}
        ok["choice"] += card.loader_check(row, must_show=ms)["ok"]
        forms[c["form"]] = forms.get(c["form"], 0) + 1
        rt = pool.defs_variant(c["variant"])["choice_route"]
        routes[rt] = routes.get(rt, 0) + 1
        # v1.0 path: the whole render_card text of the fixture card (tests/fixtures.card_for) in a choice row's card
        # field; count its non-empty card lines that decoder_io hides (the review's measurement, by card line)
        rv = card.render_row_text(st, doc=doc_for(st["skin"]), question=QUESTION, qtype="noul", card=card_for(i))
        row_old = {"id": f"o-{st['id']}", "qtype": "choice", "options": ["Label one", "Label two", "Label three"],
                   "gold": "Label two", **rv}
        n_lines = sum(1 for ln in rv["card"].split("\n") if ln.strip())
        hidden = sum(p.startswith("card line") for p in card.loader_check(row_old)["problems"])
        old["full" if hidden == 0 else "none" if hidden == n_lines else "part"] += 1
        rn = card.render_row_text(st, doc=doc_for(st["skin"]), question=QUESTION, qtype="noul", card=card_for(i),
                                  wording=WORDING, note=NOTE)
        rown = {"id": f"n-{st['id']}", "qtype": "noul", "options": None, "gold": i % 2, **rn}
        ok["noul"] += card.loader_check(rown, must_show=card.must_show(card_for(i), question=QUESTION,
                                                                        wording=WORDING, note=NOTE))["ok"]
    pairs = {"choice": 0, "noul": 0}
    n_pairs = 0
    names = ["Label one", "Label two", "Label three"]
    for cs in pool._load("card_styles.jsonl"):
        for k, v in enumerate(o for o in pool._load("defs_styles.jsonl") if o.get("kind") == "defs_variant"):
            if v["style"] == "none":
                continue
            n_pairs += 1
            st = {**styles[0], "card_style": cs["id"], "instr_position": f"IP{k % 5 + 1}"}
            cd = {"title": "Card", "blocks": [{"type": "task", "text": "Task line."},
                                              {"type": "para", "text": "Rule paragraph sentence."},
                                              defs_block(v["id"], names)]}
            for qt in ("choice", "noul"):
                f = card.render_row_text(st, doc=doc_for(st["skin"]), question=QUESTION, qtype=qt, card=cd,
                                         options=names if qt == "choice" else None)
                row = {"id": f"p-{cs['id']}-{v['id']}", "qtype": qt, "options": names if qt == "choice" else None,
                       "gold": "Label two" if qt == "choice" else 1, **f}
                pairs[qt] += card.loader_check(row, must_show=card.must_show(cd, question=QUESTION))["ok"]
    res.update({"styles": len(styles), "styles_choice_pass": ok["choice"], "styles_yesno_pass": ok["noul"],
                "choice_fixture_label_forms": forms, "choice_fixture_defs_routes": routes,
                "card_style_x_variant_pairs": n_pairs, "pairs_choice_pass": pairs["choice"],
                "pairs_yesno_pass": pairs["noul"],
                "v1_0_path_render_card_on_choice_rows": {**old, "note": "styles whose fixture card lines the v1.0 path "
                                                         "(render_card text in a choice row) showed fully / partly "
                                                         "/ not at all"}})
    return res


def lints() -> dict:
    """Counts for the chrome lints (the same checks as tests/, recorded for the manifest)."""
    from c_src.common.negcount import LEXICON_SHA256, count
    import re
    sys.path.insert(0, str(ROOT / "tests"))
    from test_fmt1 import RECORD_WORDS, _chrome_strings
    ch = _chrome_strings()
    neg = sum(1 for s in ch if count(re.sub(r"\{[^}]*\}", "x", s)).k_all)
    rec = sum(1 for s in ch if RECORD_WORDS.search(s))
    return {"chrome_strings": len(ch), "negation_cue_hits": neg, "record_status_word_hits": rec,
            "negcount_lexicon_sha256": LEXICON_SHA256}


def sealed(files: list[Path]) -> dict:
    res = {}
    outdir = QC / "sealed"
    outdir.mkdir(exist_ok=True)
    for f in files:
        out = outdir / (f.stem + ".sealedqc.jsonl")
        summ = outdir / (f.stem + ".summary.json")
        cmd = [PY, str(SEALED), str(f), "--id-field", "id", "--out", str(out), "--summary", str(summ)]
        if f.name == "previews.jsonl":
            cmd += ["--structure-fields", "state,card,instructions,options"]
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=230)
        hits = []
        if out.exists():
            for line in out.read_text().splitlines():
                o = json.loads(line)
                if o.get("hit"):
                    hits.append(o.get("id"))
        sm = json.loads(summ.read_text()) if summ.exists() else {}
        res[f.name] = {"exit": cp.returncode, "hit_ids": hits, "rows": sm.get("rows"), "rows_hit": sm.get("rows_hit"),
                       "rows_report_only": sm.get("rows_report_only"), "parse_errors": sm.get("parse_errors"),
                       "kinds_nonzero": {k: v["rows"] for k, v in sm.get("kinds", {}).items() if v.get("rows")},
                       "p_vocab_loaded": sm.get("settings", {}).get("p_vocab_loaded"),
                       "checker_sha256": sm.get("checker_sha256"), "suite_sha256": sm.get("suite_sha256"),
                       "input_sha256": sm.get("input_sha256")}
    return res


def denylist() -> dict:
    q = {"datasets": {"c_formats1_pool": {
        "names": ["formats-1 format style pool", "formats-1 label-name lexicons"],
        "datasets": [], "domains": ["format styles", "definition styles", "label names"], "parents": [],
        "emits_rows": False}}, "parents_registry": {}}
    qp = QC / "denylist_query.json"
    qp.write_text(json.dumps(q, indent=1) + "\n")
    vp = QC / "denylist_verdicts.json"
    dl = TMP / "denylist_formats1.json"
    cp = subprocess.run([PY, str(DENY), "check", "--query", str(qp), "--out", str(vp), "--run", "formats1",
                         "--denylist", str(dl), "--fail-on-taint"], capture_output=True, text=True, cwd=str(LEAN),
                        timeout=230)
    pp = subprocess.run([PY, str(DENY), "paths"] + INPUT_PATHS, capture_output=True, text=True, cwd=str(LEAN),
                        timeout=60)
    v = json.loads(vp.read_text()) if vp.exists() else None
    dl_sha = sha(dl) if dl.exists() else None
    if dl.exists():
        dl.unlink()  # keyed-hash deny-list copy: not kept in this folder
    return {"check_exit": cp.returncode, "check_stdout_tail": cp.stdout.strip().splitlines()[-3:],
            "verdict_file": str(vp.relative_to(ROOT)), "verdicts": (v or {}).get("verdicts") if v else None,
            "denylist_sha256": dl_sha, "paths_exit": pp.returncode,
            "paths_refused": [ln for ln in pp.stdout.splitlines() if ln.startswith("REFUSED")]}


def tests() -> dict:
    cp = subprocess.run([PY, "-m", "pytest", "-q", "tests", "-p", "no:cacheprovider"], capture_output=True, text=True,
                        cwd=str(ROOT), timeout=230)
    return {"exit": cp.returncode, "tail": cp.stdout.strip().splitlines()[-1]}


def manifest(qc: dict) -> None:
    files = []
    for f in sorted((ROOT / "data").glob("*.jsonl")):
        objs = [json.loads(x) for x in f.read_text().splitlines()]
        files.append({"path": f"data/{f.name}", "objects": len(objs), "sha256": sha(f),
                      "kinds": sorted({o.get("kind", "") for o in objs})})
    for rel in ["build_pool.py", "fmt1/__init__.py", "fmt1/pool.py", "fmt1/render.py", "fmt1/card.py",
                "fmt1/labels.py", "fmt1/guard.py", "tests/fixtures.py", "tests/test_fmt1.py", "qc/run_qc.py",
                "qc/previews.jsonl", "qc/cross_issue_choice_rows.json"]:
        files.append({"path": rel, "sha256": sha(ROOT / rel)})
    styles = pool.styles(held_out=None)
    m = {
        "builder": "formats-1", "version": VERSION,
        "written_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "binding": {"C_DATA_SPEC.md": sha(LEAN / "c_spec/C_DATA_SPEC.md"),
                    "C_TRAIN_RECIPE.md": sha(LEAN / "c_spec/C_TRAIN_RECIPE.md"),
                    "PREREG_FINAL.md": sha(LEAN / "PREREG_FINAL.md"),
                    "sealed_suite_sha256_A15": "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"},
        "what": "Spec section 6 format style pool (step 4, format agent 1): styles + renderers, definition styles, "
                "few-shot card templates, inverted cards, masked / swapped label-name rules. No rows.",
        "licence": "CC0 1.0 (Claude-authored chrome, closed lexicons and program code; no third-party text)",
        "public_datasets": [], "parents": [], "rows": 0, "seed": 20261003,
        "counts": {
            "styles": len(styles), "styles_training": sum(not s["held_out"] for s in styles),
            "styles_held_out_dev_only": sum(s["held_out"] for s in styles),
            "containers": len(pool._load("containers.jsonl")), "skins": len(pool._load("skins.jsonl")),
            "skins_held_out_only": sum(s["held_out_only"] for s in pool._load("skins.jsonl")),
            "card_styles": len(pool._load("card_styles.jsonl")),
            "card_styles_held_out_only": sum(c["held_out_only"] for c in pool._load("card_styles.jsonl")),
            "registers": 4, "instr_positions": 5, "fences": 4,
            "defs_styles": sum(o.get("kind") != "defs_variant" for o in pool._load("defs_styles.jsonl")),
            "defs_variants": sum(o.get("kind") == "defs_variant" for o in pool._load("defs_styles.jsonl")),
            "fewshot_templates": len(pool._load("fewshot_templates.jsonl")),
            "inverted_card_frames": len(pool.inverted_all("inverted_card_frame")),
            "inverted_case_refs": len(pool.inverted_all("inverted_case_ref")),
            "inverted_questions": len(pool.inverted_all("inverted_question")),
            "mask_schemes": len(pool._load("label_masks.jsonl")), "swap_words": len(pool.swap_words()),
            "label_notices": len(pool.label_notices()), "label_rules": len(pool.label_rules()),
            "previews_not_rows": sum(1 for _ in open(QC / "previews.jsonl")),
        },
        "held_out_style_ids": [s["id"] for s in styles if s["held_out"]],
        "held_out_only_skins": [s["id"] for s in pool._load("skins.jsonl") if s["held_out_only"]],
        "held_out_only_card_styles": [c["id"] for c in pool._load("card_styles.jsonl") if c["held_out_only"]],
        "files": files,
        "qc": qc,
        "input_paths": [{"path": p, "sha256": sha(LEAN / p)} for p in INPUT_PATHS],
        "interface": {
            "import": "sys.path.insert(0, 'c_src/formats/formats-1'); from fmt1 import pool, render, card, labels",
            "row_meta": "meta.format_style = FS id; meta.defs_style = DS name (one_line, one_line_examples, "
                        "rubric_table, decision_list, short, none; none = DS-none, a row with no card or no "
                        "definitions block); DV / FT / IVQ / MS ids go to the family side manifest or edge tags per "
                        "its G0 spec",
            "rows": "card.render_row_text(style, doc=, question=, qtype='choice'|'noul', card=, options= (choice), "
                    "wording=, note=) -> state, instructions, card. qtype is required. Yes/no: the card is shown "
                    "whole. Choice: option definitions become '- {option}: {definition}' card lines "
                    "(card.render_choice_defs; examples inline; same for every card style; the name is the exact "
                    "option text); every other block (term definitions, rubric tables, decision lists, short "
                    "lists, paragraphs, items, steps, tables, few-shot, inverted frames, notices) moves into "
                    "instructions in the card style's layout, before wording and question; IP4 / IP5 put the task "
                    "line first / last. choice_card='refuse' raises instead of moving. Moved text is printed "
                    "twice by schema_branch_mark: count it twice against the token cap.",
            "loader_check": "card.loader_check(row, must_show=card.must_show(card_ir, question=, wording=, note=)) "
                            "renders the row with lean/decoder_io.py (sha256 pinned 908c08d7) user_msg in cygnet / "
                            "schema_branch_mark under a seeded random option order; ok only if every non-empty "
                            "card line, definition, example and rule sentence is in the prompt and the gold letter "
                            "maps back. card.render_and_check does both and raises. Every family row passes it "
                            "(LR04, LR07, LR14, LR15).",
            "held_out_rule": "pool.styles() = training styles only; pool.styles(held_out=True) = the 50 dev-only "
                             "styles (S5, mix-tuning dev); pool.styles(held_out=None) = all 400 (previews and tests "
                             "only). A training row takes its style through pool.training_style(sid), which raises "
                             "HeldOutStyleError on a held-out id (pool.dev_style is the reverse). The mixer refuses "
                             "any training row whose meta.format_style is in held_out_style_ids (or whose "
                             "meta.sampler is S5) with pool.refuse_held_out(rows) or `python -m fmt1.guard "
                             "shard.jsonl ...` (exit 1 on refusal). A held-out skin or card style never appears in "
                             "training.",
            "not_here": "instruction wording pools, locales (spelling, dates, currencies, units) and real-text "
                        "codebooks are formats-2's",
        },
        "changes": {
            "v1.1": [
                "Choice rows (review formats-1, blocking): decoder_io prints no card text on choice rows except "
                "'- {option}: {definition}' lines. Added card.render_choice_defs, qtype-aware card.render_row_text "
                "(option definitions -> option lines, every other block -> instructions in the instruction "
                "position's order), card.must_show and card.loader_check / render_and_check (decoder_io pinned).",
                "choice_visible / on_choice_rows on all 12 card styles; choice_visible / choice_route / "
                "on_choice_rows on all 27 definition variants; row_qtype / on_choice_rows on the 10 inverted "
                "frames. All true, proven by loader_check through render_row_text (qc.loader).",
                "LR04 and LR07 require loader_check on choice rows; LR14 (every row passes loader_check; no "
                "'- Yes: ' / '- No: ' yes/no card lines) and LR15 (inverted rows) added: 15 label rules.",
                "render_defs refuses entry keys a variant cannot show (cells on one_line, examples on one_line), "
                "so nothing is dropped silently.",
                "Held-out guard: pool.training_style, pool.dev_style, pool.held_out_style_ids, "
                "pool.refuse_held_out and the fmt1.guard program.",
                "Interface lists defs_style 'none' (DS-none).",
                "COMMIT G0 re-read at fac29b7b (input_notes).",
                "Previews: every style as a yes/no row and as a choice row (800) plus the card-style x variant, "
                "few-shot, inverted, masked and swapped previews.",
                "Style ids and combinations unchanged from v1.0; object sha256 values change with the version "
                "field and the new fields.",
            ],
        },
        "input_notes": [
            "c_src/COMMIT/G0_SPEC.md changed after v1.0 read it (aa2ed123 -> fac29b7b, COMMIT third resolution "
            "round). Re-read for formats-1: the A59 container rule is unchanged (compat_hints "
            "COMMIT_route_or_message_only still holds). The new R4-06 route folder-name filter on swapped-name "
            "twins is a COMMIT-side program filter over its own message and hunk text (1.4 word parts); it uses "
            "no formats-1 lexicon. COMMIT swapped-name twins keep the card's own option names and swap two "
            "definitions, so on choice rows they write the swapped definitions with card.render_choice_defs (exact "
            "option text) and pass loader_check; SEM-47's sentences are card text and move to instructions on "
            "choice rows.",
            "decoder_io.py read for the loader check only (cygnet_msg, cygnet_parts, card_defs, as_letter_row, "
            "user_msg, label); sha256 908c08d7 equals the A16 readout.",
        ],
        "open_items": [
            "Orchestrator (cross-family G0, blocking for families): decoder_io shows card text on yes/no rows only. "
            "Every family's G0 spec must put what a choice row needs into instructions, state or '- {option}: "
            "{definition}' lines, and pass card.loader_check on every row (F4's clauses and masked-ID definitions "
            "are in its card). Proposed entry for G0_CROSS_ISSUES.json: qc/cross_issue_choice_rows.json. Changing "
            "the layout instead would need an amendment and would break the C1 bit-for-bit rule.",
            "Mixer: run pool.refuse_held_out (or python -m fmt1.guard) on every training shard before each freeze.",
            "Orchestrator: counts-only template/style compare against the sealed styles (spec 9) and the 7.2 "
            "Claude-seed decontamination of data/*.jsonl and qc/previews.jsonl (not run here).",
            "Families with own marker or container rules (F3 rule 20, F4 section 4, F8 record words, F9 fences, "
            "F10 ST5 omission marker, COMMIT A59) filter styles by flags / compat_hints; the renderers refuse "
            "anything they cannot show.",
            "Instruction position IP4 / IP5 move the family's card-level task line; a family with per-row "
            "instruction text in the card (F11-R2-11) keeps it in instructions and uses the task block only for a "
            "card-level line.",
        ],
    }
    (ROOT / "MANIFEST.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-sealed", action="store_true")
    a = ap.parse_args()
    prev = write_previews()
    qc = {"lints": lints(), "loader": loader_stats(), "tests": tests()}
    if not a.skip_sealed:
        qc["sealed_check"] = sealed(sorted((ROOT / "data").glob("*.jsonl")) + [prev])
    qc["denylist"] = denylist()
    manifest(qc)
    hits = {k: len(v["hit_ids"]) for k, v in qc.get("sealed_check", {}).items()}
    print(json.dumps({"lints": qc["lints"], "loader": qc["loader"], "tests": qc["tests"], "sealed_hits": hits,
                      "sealed_exits": {k: v["exit"] for k, v in qc.get("sealed_check", {}).items()},
                      "denylist": {k: qc["denylist"][k] for k in ("check_exit", "paths_exit", "paths_refused",
                                                                   "verdicts")}}, indent=1))


if __name__ == "__main__":
    main()
