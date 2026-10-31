"""STEP 4 (G9 re-read) scoring. CPU only; no model is called. Counts and ids only on stdout. Never relabels, never changes data.

  g9_score.py check                    task-file sha vs manifest, answer files present / valid JSON (counts)
  g9_score.py score FAM [FAM ...]      two blind reads vs gold (c2_kit.g5h.score), Sonnet adjudication tasks (queue + 30 controls)
  g9_score.py adjudicate FAM [...]     Sonnet verdicts -> Opus confirmation tasks for wrong_gold flags only
  g9_score.py final FAM [...]          Opus verdicts -> per-family result (G9_RESULT.json); confirmed wrong gold = generator bug (report)
  options: --skip TASK_ID ...  (reader task ids whose file-access audit failed: treated as unanswered)

Layout under c2_build/crowd_c2/g9_reread/: tasks/ answers/ key/ manifest.json (made by make_tasks.py), fam/<FAM>/{score.json,
adjudication/,confirm/,G9_RESULT.json}. Ambiguous flags come from the Sonnet pass (bar: ambiguous <= 1% of the seeded 300 rows,
unchanged); the quarantine rule (a template with > 3% disagreement over its read rows) is reported, nothing is dropped here."""
import sys, json, hashlib, argparse
from pathlib import Path
HERE = Path(__file__).resolve().parent
CB = HERE.parent.parent
sys.path.insert(0, str(CB))
sys.dont_write_bytecode = True
import c2_select as S
import qc_full_c2 as Q
from c2_kit import g5h, chunker
import pilot

OUT = CB / "crowd_c2" / "g9_reread"
CHAR_BUDGET = 90000


def _templates(r):
    if r["meta"].get("c2"):
        return [str(x) for x in g5h._templates(r)]
    m = r["meta"]
    return ["pack:" + str(m.get("domain_pack")), "style:" + str(m.get("defs_style"))]


def _manifest():
    return json.load(open(OUT / "manifest.json"))


def _read(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return None


def cmd_check(skip):
    bad_sha, missing, invalid = [], [], []
    for t in _manifest():
        tf = Path(t["task_file"])
        if hashlib.sha256(tf.read_bytes()).hexdigest() != t["sha256"]:
            bad_sha.append(t["task_id"])
        a = Path(t["answer_file"])
        if not a.is_file() or t["task_id"] in skip:
            missing.append(t["task_id"])
        elif not isinstance(_read(a), list):
            invalid.append(t["task_id"])
    print(json.dumps({"tasks": len(_manifest()), "task_sha_mismatch": bad_sha, "missing_or_skipped": missing, "invalid_json": invalid}))


def family_rows(fam):
    rows, _, _ = S.family_inputs(S.LinkGuardedInputLog(), fam)
    return {r["id"]: r for r in rows}


def write_tasks(kind, fam, d, items, key, prompt):
    sub = d / kind
    tag = "ADJ" if kind == "adjudication" else "CONF"
    title = "G9 re-read adjudication (flag only)" if kind == "adjudication" else "G9 re-read confirmation (Opus, wrong_gold flags)"
    tasks, part, size, n = [], [], 0, 0
    (sub / "tasks").mkdir(parents=True, exist_ok=True)
    (sub / "answers").mkdir(parents=True, exist_ok=True)

    def emit():
        nonlocal part, size, n
        if not part:
            return
        tid = f"{fam}-{tag}-{n:03d}"
        ans, tf = sub / "answers" / f"{tid}.json", sub / "tasks" / f"{tid}.md"
        text = pilot._task_text(title, fam, tid, ans, len(part), prompt, Q.ADJ_CONTRACT, part)
        tf.write_text(text)
        tasks.append({"stage": kind, "task_id": tid, "task_file": str(tf), "answer_file": str(ans), "n_items": len(part),
                      "aids": [it["aid"] for it in part], "sha256": hashlib.sha256(text.encode()).hexdigest()})
        part, size, n = [], 0, n + 1

    for it in items:
        s = len(json.dumps(it, ensure_ascii=False))
        if part and (len(part) >= Q.ADJ_CHUNK or size + s > CHAR_BUDGET):
            emit()
        part.append(it)
        size += s
    emit()
    Q._w(sub / "key.json", {"family": fam, "stage": kind, "key": key, "note": "orchestrator only"})
    Q._w(sub / "manifest.json", {"family": fam, "stage": kind, "tasks": tasks})
    return tasks


def cmd_score(fams, skip):
    man = _manifest()
    for fam in fams:
        key = json.load(open(OUT / "key" / f"{fam}.json"))
        tasks = [t for t in man if t["family"] == fam]
        miss = [t["task_id"] for t in tasks if t["task_id"] in skip or not Path(t["answer_file"]).is_file()]
        if miss:
            print(json.dumps({"family": fam, "pending": miss}))
            continue
        by = family_rows(fam)
        ans, probs = {}, {}
        for rd in ("A", "B"):
            raw = {}
            for t in tasks:
                if t["reader"] != rd:
                    continue
                a = _read(t["answer_file"])
                if isinstance(a, list):
                    raw[t["chunk_task_id"]] = a
            got, pr = chunker.load_answers(Q._KeyBatch(key["readers"][rd]), raw)
            ans[rd], probs[rd] = got, pr
        rows = [by[i] for i in key["row_ids"]]
        res = g5h.score(rows, key["items"], ans["A"], ans["B"], seed=f"{fam}|g9-reread-control", template_of=_templates)
        n_samp = len(set(key["sample_ids"]) & set(key["row_ids"]))
        res["n_sample_rows"] = n_samp
        res["quarantined"] = sorted(t for t, d in res["templates"].items() if d["rate"] > g5h.QUARANTINE_ABOVE)
        res["quarantined_n_ge_20"] = sorted(t for t, d in res["templates"].items()
                                            if d["rate"] > g5h.QUARANTINE_ABOVE and d["n"] >= 20)
        d = OUT / "fam" / fam
        Q._w(d / "score.json", res)
        adj, akey = g5h.adjudication_items(by, res, seed=f"{fam}|g9-reread-adj")
        items = [{"aid": a, **it} for a, it in adj]
        tasks_adj = write_tasks("adjudication", fam, d, items, akey, Q.ADJ_PROMPT)
        print(json.dumps({"family": fam, "n_read": res["n_read"], "sample_rows": n_samp,
                          "load_problems": {r: len(p) for r, p in probs.items()}, "queue": len(res["queue"]),
                          "controls": len(res["control"]), "quarantined": len(res["quarantined"]),
                          "quarantined_n_ge_20": len(res["quarantined_n_ge_20"]),
                          "adjudication_tasks": [t["task_file"] for t in tasks_adj]}))


def cmd_adjudicate(fams, skip):
    for fam in fams:
        d = OUT / "fam" / fam
        got, probs, missing, unanswered = Q._cascade_verdicts(d, "adjudication", skip)
        Q._w(d / "adjudication" / "first_pass.json", {"verdicts": {a: {"verdict": v, "reason": r} for a, (v, r) in got.items()},
                                                      "problems": probs, "unanswered": unanswered})
        if missing or unanswered or probs:
            print(json.dumps({"family": fam, "incomplete": True, "missing_tasks": missing, "unanswered": len(unanswered),
                              "problems": len(probs)}))
            continue
        akey = json.load(open(d / "adjudication" / "key.json"))["key"]
        score = json.load(open(d / "score.json"))
        adj_items = {}
        for t in json.load(open(d / "adjudication" / "manifest.json"))["tasks"]:
            body = Path(t["task_file"]).read_text().split("## Items (JSON; answer every item exactly once, keyed by its qid)\n\n", 1)[1]
            for it in json.loads(body):
                adj_items[it["aid"]] = it
        wrong = sorted(a for a, (v, _) in got.items() if v == "wrong_gold")
        amb = sorted(a for a, (v, _) in got.items() if v == "ambiguous")
        control = set(score["control"])
        items, ckey = [], {}
        for a in wrong:
            it = dict(adj_items[a])
            it["first_flag"], it["first_reason"] = got[a]
            items.append(it)
            ckey[a] = akey[a]
        tasks = write_tasks("confirm", fam, d, items, ckey, Q.CONFIRM_PROMPT) if items else []
        if not items:
            Q._w(d / "confirm" / "manifest.json", {"family": fam, "stage": "confirm", "tasks": []})
            Q._w(d / "confirm" / "key.json", {"family": fam, "stage": "confirm", "key": {}})
        Q._w(d / "sonnet_flags.json", {"wrong_gold_rows": sorted(akey[a] for a in wrong),
                                       "ambiguous_rows": sorted(akey[a] for a in amb)})
        print(json.dumps({"family": fam, "answered": len(got), "sonnet_wrong_gold": len(wrong), "sonnet_ambiguous": len(amb),
                          "controls_flagged": sum(1 for a in wrong + amb if akey[a] in control),
                          "confirm_tasks": [t["task_file"] for t in tasks]}))


def cmd_final(fams, skip):
    for fam in fams:
        d = OUT / "fam" / fam
        score = json.load(open(d / "score.json"))
        flags = json.load(open(d / "sonnet_flags.json"))
        cm = json.load(open(d / "confirm" / "manifest.json"))
        conf = {}
        if cm["tasks"]:
            conf, probs, missing, unanswered = Q._cascade_verdicts(d, "confirm", skip)
            if probs or missing or unanswered:
                print(json.dumps({"family": fam, "confirm_incomplete": True, "problems": len(probs), "missing": missing,
                                  "unanswered": len(unanswered)}))
                continue
        ckey = json.load(open(d / "confirm" / "key.json"))["key"]
        confirmed = sorted(ckey[a] for a, (v, _) in conf.items() if v == "wrong_gold")
        opus_ok = sum(1 for _, (v, _) in conf.items() if v == "gold_ok")
        opus_amb = sum(1 for _, (v, _) in conf.items() if v == "ambiguous")
        n_samp = score["n_sample_rows"]
        amb_all = sorted(set(flags["ambiguous_rows"]) | {ckey[a] for a, (v, _) in conf.items() if v == "ambiguous"})
        res = {"family": fam, "gate": "G9-reread", "n_read": score["n_read"], "n_sample_rows": n_samp,
               "queue": len(score["queue"]), "sonnet_wrong_gold": len(flags["wrong_gold_rows"]), "opus_gold_ok": opus_ok,
               "opus_ambiguous": opus_amb, "confirmed_wrong_gold": len(confirmed), "confirmed_wrong_gold_ids": confirmed,
               "generator_bug": bool(confirmed), "ambiguous_rows": len(amb_all),
               "ambiguous_rate_of_sample": (len(amb_all) / n_samp if n_samp else None), "bar_ambiguous": g5h.AMBIGUOUS_MAX,
               "quarantined_templates": len(score["quarantined"]), "quarantined_n_ge_20": len(score["quarantined_n_ge_20"]),
               "note": "report only: no data changed, nothing relabelled or dropped here"}
        Q._w(d / "G9_RESULT.json", res)
        print(json.dumps({k: v for k, v in res.items() if k != "confirmed_wrong_gold_ids"}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("check", "score", "adjudicate", "final"))
    ap.add_argument("fams", nargs="*")
    ap.add_argument("--skip", nargs="*", default=[])
    a = ap.parse_args()
    skip = set(a.skip)
    if a.cmd == "check":
        cmd_check(skip)
    else:
        {"score": cmd_score, "adjudicate": cmd_adjudicate, "final": cmd_final}[a.cmd](a.fams, skip)


if __name__ == "__main__":
    main()
