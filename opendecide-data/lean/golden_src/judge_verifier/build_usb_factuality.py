"""Build raw rows for usb_factuality: is a summary sentence fully supported by its evidence? (USB, Krishna et al.,
Findings of EMNLP 2023, "USB: A Unified Summarization Benchmark Across Tasks and Domains").

Source : HF kundank/usb (the authors' release) pinned to revision beba6462df4d38afbb7fb569022c5f19524b41b3,
         processed_data.tar.gz -> factuality_classification/train.jsonl and unsupported_span_prediction/train.jsonl
         ONLY (validation/test members are never extracted). Code/licence: GitHub kukrishna/usb @ 99f42d70.
Licence: Apache-2.0 (LICENSE in github.com/kukrishna/usb at the pinned commit; HF card 'license: apache-2.0'). The texts
         are Wikipedia (CC BY-SA).
Texts  : Wikipedia articles (biographies, companies, schools, disasters). The summary sentences are the human-written
         Wikipedia lead sentences and the annotators' corrected versions of them.
Labels : HUMAN. Annotators aligned every lead ('summary') sentence to evidence sentences in the article body and deleted
         or rewrote every part the evidence does not support. FAC label 1 = the original sentence (contains
         unsupported content), label 0 = the corrected sentence (fully supported). Pairs share the same evidence and
         differ only in the unsupported content -> fact-flip twins (meta.twin_of), kept together under one question.
Checks : a pair is kept only if the edit really removed content: the original sentence has content words (not in a
         stopword list) that are absent from both the corrected sentence and the evidence, or the authors' unsupported-
         span file marks a non-empty span in the original (drops pure grammar/typo fixes that FAC also labels 1).
         Pairs whose only removed content is a birth date / middle name ('born ...') are capped at 30% of pairs.
         Review fix: the corrected sentence must be lexically covered by the evidence (<= 2 content words whose
         5-letter prefix is absent from the evidence), because about 1 in 6 corrected sentences kept content the
         listed evidence does not state (annotator leniency), which would make the 'supported' gold wrong.
Filters: decontamination (evidence + sentence) against label-NLI, local train/dev/eval (incl. WikiText filler) and
         JevBench; cross-check with other v14 parts; exact/near-duplicate states removed only among rows with the same
         label (a twin pair is never collapsed).
Deterministic (seed 20261205). CPU only.
"""
import collections
import json
import random
import re
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "usb_factuality"
SEED = 20261205
REV = "beba6462df4d38afbb7fb569022c5f19524b41b3"
GIT = "99f42d702e37e6e8e50cc8c5cdca32de72059f10"
FILES = {
    "processed_data.tar.gz": (f"https://huggingface.co/datasets/kundank/usb/resolve/{REV}/processed_data.tar.gz",
                              "2d043d940120558b9d9e4f2d0a379fc95b18ad6953837828af1b725c5c15ea05"),
    "LICENSE": (f"https://raw.githubusercontent.com/kukrishna/usb/{GIT}/LICENSE", "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"),
}
MEMBERS = ["factuality_classification/train.jsonl", "unsupported_span_prediction/train.jsonl"]
LICENCE = (f"Apache-2.0 (https://github.com/kukrishna/usb/blob/{GIT}/LICENSE; HF card huggingface.co/datasets/kundank/usb "
           f"@ {REV[:8]} 'license: apache-2.0'); texts from Wikipedia (CC BY-SA)")
DATASET = "kundank/usb (USB factuality_classification, train)"
BIRTH_CAP = 0.30
MAX_UNCOVERED = 2  # corrected sentence: max content words (5-letter prefix) missing from the evidence
STOP = set("""a an the and or but of in on at to for from by with as is are was were be been being it its this that
these those he she they his her their them who whom which what when where while also has have had not no s
""".split())

Q = {
    "sup": "Is every piece of information in the summary sentence supported by the evidence sentences?",
    "unsup": "Does the summary sentence contain any information that the evidence sentences do not support?",
}
DEFS = {
    "sup": {
        "yes": "Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated "
               "in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not "
               "count as support.",
        "no": "Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or "
              "qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.",
    },
    "unsup": {
        "yes": "At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or "
               "qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.",
        "no": "Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly "
              "implied by the evidence sentences; nothing is added beyond them.",
    },
}


def content_words(t):
    return [w for w in C.words(t) if w not in STOP]


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "usb"
    tar = C.fetch(FILES["processed_data.tar.gz"][0], cache / "processed_data.tar.gz", FILES["processed_data.tar.gz"][1])
    C.fetch(FILES["LICENSE"][0], cache / "LICENSE", FILES["LICENSE"][1])
    data = {}
    with tarfile.open(tar) as tf:
        for m in MEMBERS:  # train members only
            f = tf.extractfile(m)
            data[m] = [json.loads(l) for l in f.read().decode("utf-8").splitlines() if l.strip()]
    fac, spans = data[MEMBERS[0]], data[MEMBERS[1]]
    span_idx = {}
    for s in spans:
        marked = re.findall(r"\[\](.*?)\[/\]", s["annotated_summary"])
        span_idx[(s["id"], C.norm(s["summary"]))] = [x.strip() for x in marked if re.search(r"[A-Za-z0-9]", x)]
    stats = collections.Counter()
    groups = collections.defaultdict(list)
    for f in fac:
        groups[(f["id"], f["summ_idx"])].append(f)
    pairs = []
    for (doc, si), v in sorted(groups.items()):
        if sorted(x["label"] for x in v) != [0, 1]:
            stats["bad_group"] += 1
            continue
        sup = next(x for x in v if x["label"] == 0)
        uns = next(x for x in v if x["label"] == 1)
        if sup["input_lines"] != uns["input_lines"]:
            stats["evidence_mismatch"] += 1
            continue
        ev = [C.clean(x) for x in sup["input_lines"] if C.clean(x)]
        s0, s1 = C.clean(sup["summary_sent"]), C.clean(uns["summary_sent"])
        if not ev or not s0 or not s1 or C.norm(s0) == C.norm(s1):
            stats["empty_or_same"] += 1
            continue
        ev_words = set(C.words(" ".join(ev)))
        extra = [w for w in content_words(s1) if w not in set(C.words(s0)) and w not in ev_words]
        marked = span_idx.get((doc, C.norm(s1)), [])
        if not extra and not marked:
            stats["drop_no_real_removal"] += 1
            continue
        # reviewer fix (v14 review): USB's corrected sentences sometimes keep content that the listed evidence does
        # not state (e.g. 'Siege operations were supervised by Vauban' against 'against Vauban's advice'), which
        # contradicts the strict 'fully supported' definition. Keep a pair only if the corrected sentence is covered
        # by the evidence: at most MAX_UNCOVERED content words (5-letter prefix match) absent from the evidence.
        ev_stems = {w[:5] for w in ev_words}
        uncovered = [w for w in content_words(s0) if w[:5] not in ev_stems]
        if len(uncovered) > MAX_UNCOVERED:
            stats["drop_corrected_not_covered"] += 1
            continue
        diff_text = " ".join(extra) + " " + " ".join(marked)
        birth = bool(re.search(r"\bborn\b", s1) and not re.search(r"\bborn\b", s0)) and len(extra) <= 6
        pairs.append({"pid": f"{doc.replace('/', '-').replace('.json', '')}-{si}", "domain": doc.split("/")[0],
                      "ev": ev, "s0": s0, "s1": s1, "extra": extra, "marked": marked, "birth": birth,
                      "diff": diff_text})
    stats["pairs"] = len(pairs)
    core = {p["pid"]: [" ".join(p["ev"]), p["s1"]] for p in pairs}
    hits = C.decon(core, cache_name=KEY)
    xhits = C.cross_v14({p["pid"]: [" ".join(p["ev"])] for p in pairs}, own_keys={KEY})
    pairs = [p for p in pairs if p["pid"] not in hits and p["pid"] not in xhits]
    stats["after_decon"] = len(pairs)

    pairs.sort(key=lambda p: p["pid"])
    rng.shuffle(pairs)
    birth = [p for p in pairs if p["birth"]]
    other = [p for p in pairs if not p["birth"]]
    n_birth = min(len(birth), int(BIRTH_CAP / (1 - BIRTH_CAP) * len(other)))
    pairs = other + birth[:n_birth]
    stats["birth_pairs_kept"] = n_birth
    rng.shuffle(pairs)

    rows = []
    for i, p in enumerate(pairs):
        qid = "sup" if i % 2 == 0 else "unsup"
        ev_txt = "\n".join(f"- {x}" for x in p["ev"])
        rid0, rid1 = f"{p['pid']}-corrected", f"{p['pid']}-original"
        if re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b|\bborn\b|\bdied\b", p["diff"]):
            e = "temporal"
        elif re.search(r"\d", p["diff"]):
            e = "numeric"
        elif len(p["ev"]) >= 3:
            e = "multi_hop"
        else:
            e = C.edge(p["s1"], order=("double_negation", "negation", "quantifier"), default=None)
        for rid, sent, supported, twin in ((rid0, p["s0"], True, rid1), (rid1, p["s1"], False, rid0)):
            gold = ("yes" if supported else "no") if qid == "sup" else ("no" if supported else "yes")
            rows.append({
                "key": KEY, "rid": rid,
                "state": f"Evidence sentences (from the article):\n{ev_txt}\n\nSummary sentence:\n{sent}",
                "instructions": Q[qid], "options": C.YN, "gold": gold, "soft": None,
                "meta": {"dataset": DATASET, "config": f"factuality_classification/train.jsonl; domain={p['domain']}",
                         "revision": f"hf:{REV}; sha256:{FILES['processed_data.tar.gz'][1]}", "licence": LICENCE,
                         "split": "train",
                         "orig_label": {"fac_label": 0 if supported else 1, "role": "corrected" if supported else
                                        "original", "removed_content": p["marked"] or p["extra"][:12]},
                         "family": C.FAMILY, "edge": e, "defs": qid, "twin_of": twin},
            })
    # exact / near-duplicate states only among rows with the same label (twins are near-identical by design)
    kept = []
    for lab in (0, 1):
        sub = [r for r in rows if r["meta"]["orig_label"]["fac_label"] == lab]
        kept += C.near_dup_filter(sub, lambda r: r["state"], thresh=0.9)
    keep_rids = {r["rid"] for r in kept}
    rows = [r for r in rows if r["rid"] in keep_rids]
    for r in rows:
        if r["meta"]["twin_of"] not in keep_rids:
            r["meta"]["twin_of"] = None
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits), "| cross_v14:", len(xhits))
    print("domains:", dict(collections.Counter(r["meta"]["config"].split("domain=")[1] for r in rows)))
    C.show_samples(rows, n=5, seed=15)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Summary-sentence factual consistency against evidence sentences, HUMAN labels: Wikipedia lead sentences vs "
        "the annotators' corrected versions (unsupported content removed) = fact-flip twins with the same evidence "
        "(meta.twin_of), both under one question (supported? / contains unsupported info?); pairs kept only when the "
        "edit removed real content (grammar-only fixes dropped); birth-date-only pairs capped at 30%.", st))


if __name__ == "__main__":
    main()
