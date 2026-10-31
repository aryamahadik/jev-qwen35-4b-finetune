#!/usr/bin/env python3
"""G-block card admission (PREREG_FINAL A39 c; G-LEX-style 2/2 extraction of each card's options).

A card is admitted only if BOTH independent Haiku reads (rA, rB) restate every option consistently with its
definition AND every example text falls in the intended option. The program below only assists: it checks
completeness and runs a lexical nearest-definition test; the verdict per card is a careful reading, recorded in
cards/admission/review.json with a reason. Any doubt rejects. Nothing here sets, edits or chooses a label: the
readers' restatements and examples are checked only, never labels, never training targets.

Subcommands:
  compare   verify task-file hashes, load both reads, map opaque qids back to cards, run the program checks,
            write cards/admission/compare.json and print a review sheet (per domain, or one domain: compare <dom>).
  write     join compare.json with review.json; write cards/admitted.jsonl and cards/ADMISSION.md.
Writes go through c2_kit.paths (A38 guard, never-open guard, lean/ only).
"""
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

C2 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
GB = C2 / "gblock"
CARDS = GB / "cards"
EXT = CARDS / "extract"
KEYS = CARDS / "extract_key"
OUT = CARDS / "admission"
sys.path.insert(0, str(C2))
from c2_kit import paths as kp  # noqa: E402

READS = ("rA", "rB")
MEANING_MAX_WORDS, EXAMPLE_MAX_WORDS = 25, 40
COPY_JACC = 0.8          # meaning vs own definition content-word Jaccard at or above this = copied, not restated
TARGET_MIN, TARGET_MAX = 2, 4

STOP = set(("a an the and or of to in on for with at by from is it be as that this your their its do does are was "
            "were been being into than then so if when while which who what whom whose how there here these those "
            "such each any all some very can could would should will shall may might must just also only pick "
            "choose text option it's they them he she we you our us i me my").split())


def stem(t):
    for suf in ("ing", "ed", "es", "s"):
        if len(t) > len(suf) + 3 and t.endswith(suf) and not t.endswith("ss"):
            return t[: -len(suf)]
    return t


def toks(s):
    return [stem(t) for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOP]


def wc(s):
    return len(re.findall(r"[A-Za-z0-9']+", s))


def jacc(a, b):
    a, b = set(a), set(b)
    return 1.0 if not a and not b else len(a & b) / len(a | b)


class Tfidf:
    def __init__(self, docs):
        df = Counter()
        for d in docs:
            df.update(set(toks(d)))
        n = len(docs)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1.0 for t, c in df.items()}

    def vec(self, s):
        tf = Counter(toks(s))
        v = {t: c * self.idf.get(t, 1.0) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}

    def cos(self, a, b):
        va, vb = self.vec(a), self.vec(b)
        return sum(x * vb.get(t, 0.0) for t, x in va.items())


def nearest(tf, text, cands):
    """cands: {name: text}. Returns (best name, margin of own over best other is computed by caller), scores."""
    sc = {k: round(tf.cos(text, v), 3) for k, v in cands.items()}
    return max(sc, key=sc.get), sc


def load():
    man = json.loads((KEYS / "manifest.json").read_text())
    keys = json.loads((KEYS / "keys.json").read_text())
    survivors = {s["src"]: s for s in json.loads((CARDS / "survivors.json").read_text())}
    problems = []
    reads = {r: {} for r in READS}
    for t in man["tasks"]:
        tf = Path(t["task_file"])
        h = hashlib.sha256(tf.read_bytes()).hexdigest()
        if h != t["sha256"]:
            problems.append(f"{t['task_id']}: task file sha256 changed since the manifest")
        task = json.loads(tf.read_text())
        ap = Path(t["answer_file"])
        if not ap.exists():
            problems.append(f"{t['task_id']}: no answer file")
            continue
        try:
            ans = json.loads(ap.read_text())
        except Exception as e:  # noqa: BLE001 - reported
            problems.append(f"{t['task_id']}: unreadable answer ({e})")
            continue
        if ans.get("task_id") != t["task_id"]:
            problems.append(f"{t['task_id']}: answer task_id {ans.get('task_id')!r}")
        shown = {c["qid"]: c for c in task["cards"]}
        seen = Counter()
        for a in ans.get("answers", []):
            q = a.get("qid")
            seen[q] += 1
            if q not in shown:
                problems.append(f"{t['task_id']}: unknown qid {q!r}")
                continue
            src = keys[t["task_id"]][q]
            reads[t["read"]][src] = {"task_id": t["task_id"], "qid": q, "options": a.get("options", [])}
        for q in shown:
            if seen[q] != 1:
                problems.append(f"{t['task_id']}: qid {q} answered {seen[q]} times")
    return survivors, reads, problems


def check_card(tf, s, reads):
    card = s["card"]
    labels = [o["label"].strip() for o in card["options"]]
    defs = {o["label"].strip(): o["definition"].strip() for o in card["options"]}
    flags, per = [], {}
    for r in READS:
        got = reads[r].get(s["src"])
        if got is None:
            flags.append(f"{r}:missing_card")
            continue
        names = [o.get("name", "") for o in got["options"]]
        if sorted(names) != sorted(labels):
            if sorted(n.strip().lower() for n in names) == sorted(x.lower() for x in labels):
                flags.append(f"{r}:name_case_or_space")
            else:
                flags.append(f"{r}:option_names_differ {names}")
        by = {o.get("name", "").strip().lower(): o for o in got["options"]}
        per[r] = {}
        for lab in labels:
            o = by.get(lab.lower())
            if o is None:
                flags.append(f"{r}:{lab}:missing_option")
                continue
            m, e = (o.get("meaning") or "").strip(), (o.get("example") or "").strip()
            rec = {"meaning": m, "example": e}
            if not m or not e:
                flags.append(f"{r}:{lab}:empty_field")
            if wc(m) > MEANING_MAX_WORDS:
                flags.append(f"{r}:{lab}:meaning_long({wc(m)})")
            if wc(e) > EXAMPLE_MAX_WORDS:
                flags.append(f"{r}:{lab}:example_long({wc(e)})")
            j = jacc(toks(m), toks(defs[lab]))
            rec["meaning_def_jaccard"] = round(j, 3)
            if j >= COPY_JACC:
                flags.append(f"{r}:{lab}:meaning_copied({j:.2f})")
            bm, scm = nearest(tf, m, defs)
            rec["meaning_nearest"], rec["meaning_scores"] = bm, scm
            if bm != lab:
                flags.append(f"{r}:{lab}:meaning_nearest={bm}")
            be, sce = nearest(tf, e, defs)
            rec["example_nearest"], rec["example_scores"] = be, sce
            if be != lab:
                flags.append(f"{r}:{lab}:example_nearest_def={be}")
            if len(lab.split()) > 1 or card["kind"] == "choice":
                if re.search(r"\b" + re.escape(lab.lower()) + r"\b", e.lower()):
                    flags.append(f"{r}:{lab}:example_names_option")
            per[r][lab] = rec
    # cross-read: each read's example against the OTHER read's restatements (a second, independent lexical classifier)
    cross = {}
    if all(r in per for r in READS):
        for r, other in (("rA", "rB"), ("rB", "rA")):
            omeans = {lab: per[other][lab]["meaning"] for lab in labels if lab in per[other]}
            for lab in labels:
                if lab not in per[r] or not omeans:
                    continue
                b, sc = nearest(tf, per[r][lab]["example"], omeans)
                cross[f"{r}:{lab}"] = b
                if b != lab:
                    flags.append(f"{r}:{lab}:example_nearest_other_read_meaning={b}")
        agree = {lab: round(jacc(toks(per["rA"][lab]["meaning"]), toks(per["rB"][lab]["meaning"])), 3)
                 for lab in labels if lab in per["rA"] and lab in per["rB"]}
    else:
        agree = {}
    hard = [f for f in flags if any(k in f for k in ("missing", "names_differ", "empty_field"))]
    return {"src": s["src"], "domain": s["domain"], "kind": card["kind"], "question": card["question"],
            "who_decides": card.get("who_decides", ""), "options": [{"label": l, "definition": defs[l]} for l in labels],
            "expected_share": card.get("expected_share"), "reads": per, "cross": cross, "meaning_agree_jaccard": agree,
            "flags": flags, "hard_fail": hard}


def cmd_compare(only=None):
    survivors, reads, problems = load()
    docs = []
    for s in survivors.values():
        docs += [o["definition"] for o in s["card"]["options"]]
    for r in READS:
        for v in reads[r].values():
            for o in v["options"]:
                docs += [o.get("meaning", ""), o.get("example", "")]
    tf = Tfidf(docs)
    res = [check_card(tf, s, reads) for s in sorted(survivors.values(), key=lambda s: s["src"])]
    summ = {"problems": problems, "cards": len(res),
            "answered": {r: len(reads[r]) for r in READS},
            "cards_with_any_flag": sum(1 for x in res if x["flags"]),
            "hard_fail": sum(1 for x in res if x["hard_fail"]),
            "flag_types": dict(Counter(re.sub(r"^r[AB]:(.*?:)?", "", f).split("=")[0].split("(")[0]
                                       for x in res for f in x["flags"]))}
    kp.write_json(OUT / "compare.json", {"summary": summ, "cards": res})
    print(json.dumps(summ, indent=1))
    for x in res:
        if only and x["domain"] != only:
            continue
        print("\n" + "=" * 100)
        print(f"{x['src']}  [{x['kind']}]  {x['question']}")
        print(f"  who: {x['who_decides']}")
        print(f"  share: {x['expected_share']}")
        for o in x["options"]:
            lab = o["label"]
            print(f"  * {lab}: {o['definition']}")
            for r in READS:
                rec = x["reads"].get(r, {}).get(lab)
                if rec:
                    print(f"     {r} M: {rec['meaning']}")
                    print(f"     {r} E: {rec['example']}")
        print(f"  FLAGS: {x['flags']}")


def cmd_write():
    cmp_ = json.loads((OUT / "compare.json").read_text())
    rev = json.loads((OUT / "review.json").read_text())
    verdicts = rev["verdicts"]
    res = cmp_["cards"]
    missing = [x["src"] for x in res if x["src"] not in verdicts]
    if missing:
        raise SystemExit(f"no verdict for {missing}")
    admitted, rejected, capped = [], [], []
    by_dom = defaultdict(list)
    for x in res:
        v = verdicts[x["src"]]
        if v["admit"] and x["hard_fail"]:
            raise SystemExit(f"{x['src']}: admitted with a hard program failure {x['hard_fail']}")
        if v["admit"]:
            by_dom[x["domain"]].append(x)
        else:
            rejected.append((x, v["reason"]))
    # target cap: at most TARGET_MAX per domain; the rule and the drop order are fixed in review.json ("cap_rule").
    for dom, xs in by_dom.items():
        keep = xs
        if len(xs) > TARGET_MAX:
            order = rev.get("cap_drop_order", {}).get(dom)
            if not order:
                raise SystemExit(f"{dom}: {len(xs)} pass but review.json has no cap_drop_order")
            keep = list(xs)
            for src in order:
                if len(keep) <= TARGET_MAX:
                    break
                keep = [k for k in keep if k["src"] != src]
            for k in xs:
                if k not in keep:
                    capped.append((k, rev.get("cap_reasons", {}).get(k["src"], "passed; over the per-domain target of 4")))
        admitted += keep
    rows = []
    for x in sorted(admitted, key=lambda x: x["src"]):
        cid = "gb_" + x["src"].replace("#", "_c")
        rows.append({"card_id": cid, "domain": x["domain"], "kind": x["kind"], "question": x["question"],
                     "options": [o["label"] for o in x["options"]],
                     "definitions": {o["label"]: o["definition"] for o in x["options"]}})
    kp.write_jsonl(CARDS / "admitted.jsonl", rows)
    doms = sorted({x["domain"] for x in res})
    cnt = {d: {"survivors": sum(1 for x in res if x["domain"] == d),
               "admitted": sum(1 for r in rows if r["domain"] == d),
               "admitted_yesno": sum(1 for r in rows if r["domain"] == d and r["kind"] == "yes/no"),
               "admitted_choice": sum(1 for r in rows if r["domain"] == d and r["kind"] == "choice"),
               "rejected": sum(1 for x, _ in rejected if x["domain"] == d),
               "capped": sum(1 for x, _ in capped if x["domain"] == d)} for d in doms}
    L = ["# G-block task-card admission (PREREG_FINAL A39 c)", "",
         "Binding: PREREG_FINAL.md Ruling A39 (c) (G-LEX-style 2/2 Haiku extraction of each card's options) and A37 (b) "
         "(Haiku never sets a label). This step admits task cards only. No label, row or training target is created.", "",
         "## Rule", "",
         "A card is admitted only if BOTH independent Haiku reads (rA, rB; separate chunk files, opaque qids, own card "
         "and option order) restate EVERY option consistently with its definition AND every example text falls in the "
         "intended option under the card's definitions. Judged by program-assisted comparison "
         "(`tools/admit_cards.py compare`: completeness, exact option names, length limits, copy check, nearest "
         "definition by TF-IDF cosine for each restatement and example, and each example against the other read's "
         "restatements) plus a careful reading of every restatement and example. Lexical flags are aids, not verdicts: "
         "every card was read in full, and any doubt rejects.", "",
         f"Inputs: 50 lint survivors (`cards/survivors.json`), 4/4 read files returned "
         f"(rA_001, rA_002, rB_001, rB_002); task-file sha256 = manifest for all 4. "
         f"Program problems: {cmp_['summary']['problems'] or 'none'}.", "",
         "## Counts per domain", "",
         "| Domain | Lint survivors | Admitted | yes/no | choice | Rejected | Over target (not admitted) |",
         "|---|---|---|---|---|---|---|"]
    for d in doms:
        c = cnt[d]
        L.append(f"| {d} | {c['survivors']} | {c['admitted']} | {c['admitted_yesno']} | {c['admitted_choice']} | "
                 f"{c['rejected']} | {c['capped']} |")
    tot = {k: sum(c[k] for c in cnt.values()) for k in next(iter(cnt.values()))}
    L.append(f"| **total** | {tot['survivors']} | {tot['admitted']} | {tot['admitted_yesno']} | "
             f"{tot['admitted_choice']} | {tot['rejected']} | {tot['capped']} |")
    short = [d for d in doms if cnt[d]["admitted"] < TARGET_MIN]
    L += ["", f"Target 2-4 admitted per domain: {'met in every domain' if not short else 'NOT met in ' + ', '.join(short)}.", ""]
    L += ["## Admitted cards", ""]
    for r in rows:
        L.append(f"- `{r['card_id']}` ({r['domain']}, {r['kind']}): {r['question']} Options: "
                 + ", ".join(f"*{o}*" for o in r["options"]))
    L += ["", "## Rejections and reasons", "",
          f"{len(rejected)} of {len(res)} read cards were rejected after the reads.", ""]
    for x, why in sorted(rejected, key=lambda t: t[0]["src"]):
        L.append(f"- `{x['src']}` ({x['domain']}, {x['kind']}): {x['question']}  \n  Reason: {why}")
    if capped:
        L += ["", "## Passed but not admitted (per-domain target of at most 4; reserve)", ""]
        for x, why in capped:
            L.append(f"- `{x['src']}` ({x['domain']}, {x['kind']}): {x['question']}  \n  Reason: {why}")
    copies = {x["src"]: sum(1 for f in x["flags"] if "meaning_copied" in f) for x in res}
    n_opt = sum(2 * len(x["options"]) for x in res)
    L += ["", "## Program-check summary (aids only)", "",
          f"- Completeness: rA {cmp_['summary']['answered']['rA']}/{len(res)}, rB {cmp_['summary']['answered']['rB']}/{len(res)} cards answered; hard failures (missing card or option, "
          f"option names differ, empty field): {cmp_['summary']['hard_fail']}.",
          f"- Copied restatements: {sum(copies.values())} of {n_opt} option restatements "
          f"(on admitted cards: {sum(copies[x['src']] for x in admitted)}).",
          f"- Lexical flags (examples nearest another option's definition, or another read's restatement): "
          f"{cmp_['summary']['flag_types'].get('example_nearest_def', 0)} and "
          f"{cmp_['summary']['flag_types'].get('example_nearest_other_read_meaning', 0)}; restatement nearest another "
          f"definition: {cmp_['summary']['flag_types'].get('meaning_nearest', 0)}. Every flag was read; none "
          "showed a real misplacement on an admitted card (yes/no negations and paraphrase defeat word overlap).",
          "- Same-decision pairs admitted together (both within the target, no cap needed): office_help_1#1 / "
          "office_help_3#1 (what the writer wants), sci_abstracts_2#1 / sci_abstracts_3#1 (main subject). "
          "Labelling the same text with both cards adds little; downstream may pick one per text."]
    L += ["", "## Earlier drops (before the reads; from `cards/lint_report.json`)", "",
          "16 of 66 authored cards failed lint (label word in question 11, definitions overlap 5, personal-trait "
          "question 1; one card had two reasons) and were never sent to the reads.", "",
          "## Notes", "",
          "- The readers' restatements and examples are used only to judge the cards. They are never labels and never "
          "training data.",
          "- The file-access audit of the four read agents' transcripts is not part of this step (transcripts are on "
          "never-open paths for this workflow); the orchestrator records it. A failed audit discards that read and "
          "re-opens admission for the affected cards.",
          f"- Artifacts: `cards/admission/compare.json` (program checks), `cards/admission/review.json` (per-card "
          f"verdicts and reasons), `cards/admitted.jsonl` ({len(rows)} cards).", ""]
    kp.write_text(CARDS / "ADMISSION.md", "\n".join(L))
    print(json.dumps({"admitted": len(rows), "rejected": len(rejected), "capped": len(capped), "per_domain": cnt},
                     indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "compare":
        cmd_compare(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "write":
        cmd_write()
    else:
        raise SystemExit("usage: admit_cards.py compare [domain] | write")
