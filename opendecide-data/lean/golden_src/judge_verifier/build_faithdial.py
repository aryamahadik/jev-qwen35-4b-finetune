"""Build raw rows for faithdial: is a knowledge-grounded dialogue response faithful to its knowledge snippet?
(FaithDial; Dziri et al., TACL 2022, "FaithDial: A Faithful Benchmark for Information-Seeking Dialogue").

Source : HF McGill-NLP/FaithDial (the authors' release) pinned to revision 7a414e80725eac766f2602676dc8b39f80b061e4,
         data/train.json ONLY (valid/test files never downloaded).
Licence: MIT (dataset card README.md at the pinned revision: 'license: mit' and 'Licensing Information: MIT').
Texts  : Wizard of Wikipedia dialogues (crowd-written): a knowledge sentence from Wikipedia, the dialogue history, the
         original WoW wizard response (human-written) and, for unfaithful turns, a FaithDial rewrite written by trained
         crowd editors to be faithful to the knowledge.
Labels : HUMAN BEGIN-taxonomy labels of the ORIGINAL response (Hallucination / Entailment / Generic / Uncooperative,
         multi-label; 'Hallucination'+'Entailment' = partly grounded, partly unsupported). Rows:
           no  : an original response labelled Hallucination (pure or partial) - it states something the knowledge does
                 not support (made-up facts, or personal experiences/opinions/feelings claimed by the bot);
           yes : an original response labelled Entailment only (faithful WoW turn), or the FaithDial editor's rewrite of
                 a hallucinated turn (faithful by the editing protocol).
         Generic and Uncooperative turns are not used. One row per dialogue turn (an original and its rewrite are never
         both used). Two framings (qids): 'sup' (fully supported?) and 'hal' (contains unsupported information?).
Filters: decontamination (knowledge + response) against label-NLI, local train/dev/eval and JevBench; cross-check
         with other v14 parts; exact/near-duplicate states removed.
Deterministic (seed 20261207). CPU only.
"""
import collections
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "faithdial"
SEED = 20261207
REV = "7a414e80725eac766f2602676dc8b39f80b061e4"
BASE = f"https://huggingface.co/datasets/McGill-NLP/FaithDial/resolve/{REV}/"
FILES = {"data/train.json": "51eff8212d804b1954b7eefa8987265750f0412b0b18b534ed2dbe636e524512", "README.md": "b95c31b515df1a45e0e19a9d9fde6e2c470353c8ae4b800d092c7650d19866ac"}
LICENCE = (f"MIT (https://huggingface.co/datasets/McGill-NLP/FaithDial/blob/{REV}/README.md, 'license: mit'; "
           "'Licensing Information: MIT'); knowledge sentences from Wikipedia (CC BY-SA)")
DATASET = "McGill-NLP/FaithDial (train; BEGIN labels of Wizard-of-Wikipedia responses + FaithDial rewrites)"
TARGET = 4400
MIX = {"hal_partial": 0.30, "hal_pure": 0.20, "faith_natural": 0.25, "faith_edited": 0.25}

Q = {
    "sup": "Is everything the wizard's response asserts supported by the knowledge snippet?",
    "hal": "Does the wizard's response assert anything that the knowledge snippet does not support?",
}
_SUP = ("Faithful: every factual claim in the response is stated in or directly entailed by the knowledge snippet; "
        "questions, greetings, acknowledgements and hedges ('I'm not sure, but...') are fine, as long as nothing "
        "unsupported is asserted.")
_HAL = ("Unfaithful: the response asserts something the knowledge snippet does not support, e.g. a fact or detail not "
        "in the snippet, a contradiction, or the bot's own personal experiences, feelings, opinions or preferences "
        "presented as its own ('I love hiking', 'my daughter wants one'), even if most of the response is grounded.")
DEFS = {"sup": {"yes": _SUP, "no": _HAL}, "hal": {"yes": _HAL, "no": _SUP}}


def render(u, resp):
    hist = u["history"]
    lines = [f"Knowledge snippet:\n{C.clean(u['knowledge'])}", "", "Conversation so far:"]
    n = len(hist)
    for i, h in enumerate(hist):
        role = "Seeker" if (n - 1 - i) % 2 == 0 else "Wizard"
        lines.append(f"{role}: {C.clean(h)}")
    lines += ["", "Wizard's response:", C.clean(resp)]
    return "\n".join(lines)


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "faithdial"
    paths = {rel: C.fetch(BASE + rel, cache / Path(rel).name, sha) for rel, sha in FILES.items()}
    D = json.load(open(paths["data/train.json"]))
    stats = collections.Counter()
    turns = []
    for di, d in enumerate(D):
        for ui, u in enumerate(d["utterances"]):
            b = tuple(u["BEGIN"])
            orig, resp = u.get("original_response"), u.get("response")
            rid = f"fd-train-{di}-{ui}"
            if not u.get("knowledge") or not u.get("history"):
                stats["drop_no_k_or_hist"] += 1
                continue
            if "Hallucination" in b:
                if not orig or not resp:
                    stats["drop_missing"] += 1
                    continue
                kind = "hal_partial" if "Entailment" in b else "hal_pure"
                turns.append({"rid": rid, "u": u, "kind": kind, "b": b})
            elif b == ("Entailment",):
                text = resp if resp else orig
                if not text:
                    continue
                turns.append({"rid": rid, "u": u, "kind": "faith_natural", "b": b, "text": text})
            else:
                stats[f"drop_{'+'.join(b)}"] += 1
    stats["turns"] = len(turns)
    core = {}
    for t in turns:
        u = t["u"]
        core[t["rid"]] = [u["knowledge"], u.get("original_response") or "", u.get("response") or ""]
    hits = C.decon(core, cache_name=KEY)
    xhits = C.cross_v14({t["rid"]: [t["u"]["knowledge"]] for t in turns if len(t["u"]["knowledge"].split()) >= 8},
                        own_keys={KEY})
    turns = [t for t in turns if t["rid"] not in hits and t["rid"] not in xhits]
    stats["after_decon"] = len(turns)
    turns.sort(key=lambda t: t["rid"])
    rng.shuffle(turns)
    quota = {k: int(round(v * TARGET)) for k, v in MIX.items()}
    got = collections.Counter()
    sel = []
    hal_pool = [t for t in turns if t["kind"].startswith("hal")]
    # hallucinated turns are split: some give the unfaithful original (no), the others give the faithful rewrite (yes)
    for t in hal_pool:
        if got[t["kind"]] < quota[t["kind"]]:
            sel.append((t, t["kind"], t["u"]["original_response"]))
            got[t["kind"]] += 1
        elif got["faith_edited"] < quota["faith_edited"]:
            sel.append((t, "faith_edited", t["u"]["response"]))
            got["faith_edited"] += 1
    for t in turns:
        if t["kind"] == "faith_natural" and got["faith_natural"] < quota["faith_natural"]:
            sel.append((t, "faith_natural", t["text"]))
            got["faith_natural"] += 1
    stats.update({f"sel_{k}": v for k, v in got.items()})

    rows = []
    for i, (t, kind, text) in enumerate(sel):
        qid = "sup" if rng.random() < 0.5 else "hal"
        faithful = kind.startswith("faith")
        gold = ("yes" if faithful else "no") if qid == "sup" else ("no" if faithful else "yes")
        state = render(t["u"], text)
        e = C.edge(text, order=("double_negation", "negation", "hypothetical", "numeric", "quantifier"), default=None)
        if kind == "hal_partial" and e is None:
            e = "implicit"
        rows.append({
            "key": KEY, "rid": f"{t['rid']}-{'rewrite' if kind == 'faith_edited' else 'orig'}", "state": state,
            "instructions": Q[qid], "options": C.YN, "gold": gold, "soft": None,
            "meta": {"dataset": DATASET, "config": "data/train.json", "revision": f"hf:{REV}; sha256:{FILES['data/train.json']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"BEGIN_of_original": list(t["b"]), "judged_text": "faithdial_rewrite" if kind ==
                                    "faith_edited" else "original_wow_response", "kind": kind},
                     "family": C.FAMILY, "edge": e, "defs": qid},
        })
    rows = C.near_dup_filter(rows, lambda r: r["state"], thresh=0.92)
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits), "| cross_v14:", len(xhits))
    print("kinds:", dict(collections.Counter(r["meta"]["orig_label"]["kind"] for r in rows)))
    C.show_samples(rows, n=6, seed=17)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Knowledge-grounded dialogue faithfulness with HUMAN BEGIN labels: unfaithful = WoW wizard turns labelled "
        "Hallucination (pure or partial: grounded content plus an unsupported claim or the bot's own personal "
        "experience/opinion); faithful = Entailment-only WoW turns or FaithDial editors' rewrites; Generic/"
        "Uncooperative dropped; one row per turn; two framings (supported? / asserts unsupported?).", st))


if __name__ == "__main__":
    main()
