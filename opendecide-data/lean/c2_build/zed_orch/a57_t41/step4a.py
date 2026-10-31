"""A57 step 4a for T41 (quarantine answers only; drops only, nothing admitted):
format check, family checkers (check_skin / check_wording / check_deleg / check_attack, which hold G-SL, negation profile, fact-lock
placeholders and the lexicon unit test), label-word / question leak (the chunker's forbid rule), exact duplicates, lexicon registry
unit tests, hash compare vs the OHS-AC freeze export. Then writes the G-LEX 2-read task files for the survivors.
Counts / ids only. Run from c2_build:  ../../.venv/bin/python -B zed_orch/a57_t41/step4a.py [glex]"""
import hashlib, json, re, sys, time
from collections import Counter, defaultdict
from pathlib import Path
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
import ac_hash as A
from c2_kit import chunker as CH
from c2_kit.lexicon import LexiconRegistry, question_sem
from families.T41 import haiku_author as H, pools as P, fixtures as FX

AUTH = H.ROOT
Q = C2 / "a57_pool_quarantine" / "T41"
OUT = Path(__file__).parent
(Q / "_work").mkdir(exist_ok=True)
STATE = Q / "_work" / "step4a_state.json"
tasks = json.loads((AUTH / "TASKS.json").read_text())["tasks"]
keys, plans = {}, {}
for p in (AUTH / "key").glob("*.json"):
    keys.update(json.loads(p.read_text())["key"])
for p in (AUTH / "plan").glob("*.json"):
    plans.update(json.loads(p.read_text())["plan"])


def forbid_hit(text, forbid):
    low = text.lower()
    return [f for f in forbid if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low)]


def load():
    items, probs = {}, []
    for t in tasks:
        f = Path(t["answer_file"])
        if not f.exists():
            probs.append(f"{t['task_id']}: no answer file"); continue
        try:
            arr = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            probs.append(f"{t['task_id']}: not JSON"); continue
        chunk = json.loads((AUTH / "chunks" / f"{t['task_id']}.json").read_text())
        want = [it["qid"] for it in chunk["items"]]
        got = {}
        for a in arr if isinstance(arr, list) else []:
            if isinstance(a, dict) and isinstance(a.get("qid"), str) and isinstance(a.get("text"), str) \
                    and set(a) <= {"qid", "text"}:
                got.setdefault(a["qid"], a["text"])
        if set(got) != set(want) or len(arr) != len(want):
            probs.append(f"{t['task_id']}: qids differ ({len(got)} vs {len(want)}; {len(arr)} entries)")
        for q in want:
            if q in got:
                iid = keys[q]
                items[iid] = {"iid": iid, "qid": q, "task": t["task_id"], "text": got[q], "plan": plans[iid]}
    return items, probs


def main():
    log = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
    items, probs = load()
    log["answers_loaded"] = len(items)
    log["format_problems"] = probs
    log["expected_items"] = sum(t["n_items"] for t in tasks)
    drops = {}   # iid -> reason

    FORBID = tuple(H.TP.T41Plugin.LABEL_WORDS) + tuple(t for _, _, t in FX.WORDINGS)
    for iid, it in sorted(items.items()):
        pl, text = it["plan"], it["text"]
        role = pl["role"]
        if pl.get("held_out"):
            drops[iid] = "held_out_role"; continue
        if role == "skin":
            if "register" in pl and iid.startswith("t41a.attack"):
                pass
            pr = H.check_skin(text, pl["register"])
            rule = "check_skin"
        elif role == "wording":
            pr, rule = H.check_wording(pl["qform"], text), "check_wording"
        elif role == "lexicon":
            pr, rule = H.check_deleg(pl["sem"], text), "check_deleg"
        else:
            pr, rule = H.check_attack(text), "check_attack"
        if pr:
            drops[iid] = f"{rule}"; it["problem"] = re.sub(r"'[^']*'", "'..'", pr[0])[:50]; continue
        if role in ("skin", "attack") and forbid_hit(text, FORBID):
            drops[iid] = "label_word_or_question_leak"
    # exact duplicates (normalised) inside a role: keep the first by item id
    seen = {}
    for iid, it in sorted(items.items()):
        if iid in drops:
            continue
        k = (it["plan"]["role"], it["plan"].get("sem") or it["plan"].get("qform"), re.sub(r"\W+", " ", it["text"].lower()).strip())
        if k in seen:
            drops[iid] = "duplicate"
        else:
            seen[k] = iid
    # lexicon registry unit tests (wordings + deleg forms together; duplicates / parse ambiguity drop)
    reg = LexiconRegistry("T41")
    for sem, meaning in P.DELEG_MEANING.items():
        reg.declare(sem, "deontic" if sem == "deleg.direct" else "confirmation", meaning)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem("T41", qf), "question", meaning)
    fid_of = {}
    for iid, it in sorted(items.items()):
        if iid in drops or it["plan"]["role"] not in ("wording", "lexicon"):
            continue
        pl = it["plan"]
        try:
            if pl["role"] == "wording":
                f = reg.add(it["text"], question_sem("T41", pl["qform"]), family="T41")
            else:
                f = reg.add(it["text"].replace("{ARG}", "{ARG:s0}").replace("{SRC}", "{SRC:s0}"), pl["sem"],
                            slots={"ARG": "category", "SRC": "category"}, family="T41")
            fid_of[iid] = f.form_id
        except Exception:
            drops[iid] = "lexicon_add"
    ut = reg.unit_test_all()
    for iid, fid in fid_of.items():
        if not ut[fid]:
            drops[iid] = "lexicon_unit_test"
    # hash compare vs OHS-AC freeze export (per item, template cut)
    ex = A.ACExports()
    assert A.selftest(ex)
    texts = {iid: [it["text"]] for iid, it in items.items() if iid not in drops}
    hits, rep = A.check_texts(ex, texts, cut=True)
    hit_ids = {k for m in hits.values() for k in m}
    by_m = {m: len(v) for m, v in hits.items()}
    for k in hit_ids:
        drops[k] = "ac_hash:" + "+".join(sorted(m for m, v in hits.items() if k in v))
    log["ac_hash"] = {"manifest_sha256": ex.manifest_sha, "final_suite_sha256": ex.manifest.get("final_suite_sha256"),
                      "stage": ex.manifest.get("stage"), "checked": len(texts), "hit_items": len(hit_ids), "by_method": by_m}
    surv = sorted(i for i in items if i not in drops)
    def tally(sub):
        return {"authored": sum(1 for i in items if sub(items[i])), "survive": sum(1 for i in surv if sub(items[i])),
                "dropped_by_reason": dict(Counter(drops[i].split(":")[0] for i in items if i in drops and sub(items[i])))}
    log["by_role"] = {
        "skin": tally(lambda it: it["plan"]["role"] == "skin" and it["iid"].startswith("t41a.skin")),
        "attack": tally(lambda it: it["iid"].startswith("t41a.attack")),
        "wording": tally(lambda it: it["plan"]["role"] == "wording"),
        "deleg": tally(lambda it: it["plan"]["role"] == "lexicon")}
    log["per_register_survivors"] = dict(Counter(items[i]["plan"]["register"] for i in surv if i.startswith("t41a.skin")))
    log["per_qform_survivors"] = dict(Counter(items[i]["plan"]["qform"] for i in surv if items[i]["plan"]["role"] == "wording"))
    log["per_meaning_survivors"] = dict(Counter(items[i]["plan"]["sem"] for i in surv if items[i]["plan"]["role"] == "lexicon"))
    log["check_problem_kinds"] = dict(Counter(f"{it['plan'].get('qform') or it['plan']['role']}: {it['problem']}" for it in items.values() if it.get("problem")))
    log["drop_reasons_all"] = dict(Counter(v.split(":")[0] for v in drops.values()))
    STATE.write_text(json.dumps({"drops": drops, "survivors": surv, "fid_of": fid_of,
                                 "texts": {i: items[i]["text"] for i in items}}, indent=1, sort_keys=True))
    (OUT / "step4a_log.json").write_text(json.dumps(log, indent=1) + "\n")
    print(json.dumps(log, indent=1))


if __name__ == "__main__":
    main()
