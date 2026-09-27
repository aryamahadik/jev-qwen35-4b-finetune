"""OHS-3 part: few_nerd_fine (entity span typing, 20-way choice, track U).

Source: Few-NERD (Ding et al., ACL 2021), Hugging Face dataset DFKI-SLT/few-nerd, config "supervised", split "test",
pinned revision 205f3e9c9f3577ea2561d43f2f62dc249ab92d5b. Licence CC BY-SA 4.0.

Item = one test sentence with one entity span marked [[ ]]; question: which fine-grained Few-NERD type is the span?
Label set = the 20 most frequent fine types in the test split (counted as maximal same-tag token runs, since Few-NERD
uses IO tagging); ties broken with a seeded shuffle (none occur at this revision). 142 items, 7-8 per type, at most one
item per sentence, no entity surface string used twice. All 20 options shown in a seeded random order per row.

Determinism: the first run downloads the pinned parquet + README into ohs3/cache/few_nerd_fine/<rev>/; later runs read
only that snapshot (sha256 recorded). Seed 20261026.

No model predictions, results or LLM APIs are used.
"""
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.parquet as pq

LEAN = Path(__file__).resolve().parents[1]
REPO = "DFKI-SLT/few-nerd"
REV = "205f3e9c9f3577ea2561d43f2f62dc249ab92d5b"
CONFIG, SPLIT = "supervised", "test"
PARQUET_REL = "supervised/test-00000-of-00001.parquet"
CACHE = LEAN / "ohs3" / "cache" / "few_nerd_fine" / REV
OUT = LEAN / "data" / "ohs3_parts" / "few_nerd_fine.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "few_nerd_fine_summary.json"

TASK = "few_nerd_fine"
SEED = 20261026
N_ITEMS = 142
N_TYPES = 20
LICENCE = "CC BY-SA 4.0 (Few-NERD; text derived from English Wikipedia)"
ATTRIBUTION = ("Few-NERD: A Few-shot Named Entity Recognition Dataset. Ding, Xu, Chen, Wang, Hu, Xie, Zheng, Liu. "
               "ACL-IJCNLP 2021. https://aclanthology.org/2021.acl-long.248/ ; HF mirror DFKI-SLT/few-nerd.")

# Official Few-NERD fine-type names (ClassLabel names in the dataset card at REV). Index 0 = "O".
FINE_NAMES = [
    "O", "art-broadcastprogram", "art-film", "art-music", "art-other", "art-painting", "art-writtenart",
    "building-airport", "building-hospital", "building-hotel", "building-library", "building-other",
    "building-restaurant", "building-sportsfacility", "building-theater", "event-attack/battle/war/militaryconflict",
    "event-disaster", "event-election", "event-other", "event-protest", "event-sportsevent", "location-GPE",
    "location-bodiesofwater", "location-island", "location-mountain", "location-other", "location-park",
    "location-road/railway/highway/transit", "organization-company", "organization-education",
    "organization-government/governmentagency", "organization-media/newspaper", "organization-other",
    "organization-politicalparty", "organization-religion", "organization-showorganization",
    "organization-sportsleague", "organization-sportsteam", "other-astronomything", "other-award",
    "other-biologything", "other-chemicalthing", "other-currency", "other-disease", "other-educationaldegree",
    "other-god", "other-language", "other-law", "other-livingthing", "other-medical", "person-actor",
    "person-artist/author", "person-athlete", "person-director", "person-other", "person-politician",
    "person-scholar", "person-soldier", "product-airplane", "product-car", "product-food", "product-game",
    "product-other", "product-ship", "product-software", "product-train", "product-weapon",
]
COARSE_NAMES = ["O", "art", "building", "event", "location", "organization", "other", "person", "product"]

# Author-written definitions (one per label, written once and frozen before sampling; neutral; the "-other" types
# are defined relative to ALL official Few-NERD sibling subtypes, as in the source taxonomy).
DEFS = {
    "location-GPE": "A geopolitical entity: a country, state, province, region, city, town or other politically defined place.",
    "person-other": "A person who does not belong to the Few-NERD person subtypes actor, artist/author, athlete, director, politician, scholar or soldier.",
    "organization-other": "An organization that does not belong to the Few-NERD organization subtypes company, education, government/governmentagency, media/newspaper, politicalparty, religion, showorganization, sportsleague or sportsteam.",
    "organization-company": "A business or commercial company.",
    "person-artist/author": "A person known as a creator of artistic or written works, such as a musician, singer, painter or writer.",
    "person-athlete": "A person known as a sports player or athlete.",
    "person-politician": "A person known as a politician, head of state or government official.",
    "building-other": "A building or man-made structure that does not belong to the Few-NERD building subtypes airport, hospital, hotel, library, restaurant, sportsfacility or theater.",
    "organization-sportsteam": "A sports team or club.",
    "location-other": "A location that does not belong to the Few-NERD location subtypes GPE, bodiesofwater, island, mountain, park or road/railway/highway/transit.",
    "organization-education": "An educational institution, such as a school, college or university.",
    "other-biologything": "A biological entity or term, such as a gene, protein, cell, tissue or other biological substance or structure.",
    "location-road/railway/highway/transit": "A road, street, highway, railway line, route or other transit line.",
    "person-actor": "A person known as an actor or actress.",
    "product-other": "A product or man-made object that does not belong to the Few-NERD product subtypes airplane, car, food, game, ship, software, train or weapon.",
    "event-sportsevent": "A sports event, such as a match, race, tournament, championship or season.",
    "organization-government/governmentagency": "A government, government body or government agency.",
    "organization-media/newspaper": "A media organization, such as a newspaper, magazine, broadcaster or publisher.",
    "location-bodiesofwater": "A body of water, such as a sea, ocean, lake, river or bay.",
    "event-attack/battle/war/militaryconflict": "An attack, battle, war or other military conflict.",
}
INSTR_TMPL = "What type of entity is [[{span}]]?"

sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def ensure_snapshot():
    pq_path = CACHE / PARQUET_REL
    if not pq_path.exists():
        from huggingface_hub import hf_hub_download
        for f in (PARQUET_REL, "README.md"):
            hf_hub_download(REPO, f, repo_type="dataset", revision=REV, local_dir=str(CACHE))
    return pq_path


# ---------------- detokenisation (layout only; tokens are never changed except quote glyphs) ----------------
NO_SPACE_BEFORE = {",", ".", ";", ":", "!", "?", ")", "]", "}", "%", "...", "..", "]]", "”", "’", "»"}
NO_SPACE_AFTER = {"(", "[", "{", "$", "£", "€", "[[", "“", "‘", "«"}
CLITIC = re.compile(r"^(?:['’](?:s|S|re|ve|ll|d|m|t)|n['’]t)$")
DQUOTES = {"``", "''", '"'}


def detok(tokens):
    out, open_q = "", False
    attach_next = True  # no space before the first token
    for t in tokens:
        if t in DQUOTES:
            if not open_q:  # opening quote
                out += ("" if attach_next else " ") + '"'
                attach_next, open_q = True, True
            else:  # closing quote
                out += '"'
                attach_next, open_q = False, False
            continue
        sep = "" if (attach_next or t in NO_SPACE_BEFORE or CLITIC.match(t)) else " "
        out += sep + t
        attach_next = t in NO_SPACE_AFTER
    return out


def spans(fine):
    res, i = [], 0
    while i < len(fine):
        if fine[i]:
            j = i
            while j < len(fine) and fine[j] == fine[i]:
                j += 1
            res.append((i, j, int(fine[i])))
            i = j
        else:
            i += 1
    return res


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def main():
    pq_path = ensure_snapshot()
    pq_sha = hashlib.sha256(pq_path.read_bytes()).hexdigest()
    readme = CACHE / "README.md"
    readme_sha = hashlib.sha256(readme.read_bytes()).hexdigest() if readme.exists() else None
    tbl = pq.read_table(pq_path).to_pylist()

    # sanity: label names match the card's ClassLabel list
    card_txt = readme.read_text() if readme.exists() else ""
    for n in FINE_NAMES[1:]:
        assert f"': {n}\n" in card_txt, n

    # 1) type frequencies in the test split (span counts)
    freq = Counter()
    for r in tbl:
        for _, _, f in spans(r["fine_ner_tags"]):
            freq[f] += 1
    rng = random.Random(SEED)
    keys = sorted(freq)
    tb = {k: rng.random() for k in keys}  # seeded tie-break
    ranked = sorted(keys, key=lambda k: (-freq[k], tb[k]))
    top = ranked[:N_TYPES]
    boundary_tie = freq[ranked[N_TYPES - 1]] == freq[ranked[N_TYPES]]
    labels = [FINE_NAMES[k] for k in top]
    assert set(labels) == set(DEFS), set(labels) ^ set(DEFS)

    # 2) candidates
    drops = Counter()
    cands = defaultdict(list)
    seen_sent = set()
    for r in sorted(tbl, key=lambda x: int(x["id"])):
        toks, fine, coarse = r["tokens"], r["fine_ner_tags"], r["ner_tags"]
        plain = detok(toks)
        ns = norm(plain)
        if ns in seen_sent:
            drops["duplicate_sentence"] += 1
            continue
        seen_sent.add(ns)
        if any(toks[i] == "&" and i + 1 < len(toks) and toks[i + 1].lower() in ("amp", "quot", "lt", "gt", "nbsp")
               for i in range(len(toks))):
            drops["html_entity_artifact"] += 1
            continue
        if sum(t in DQUOTES for t in toks) % 2:
            drops["unbalanced_double_quotes"] += 1
            continue
        if "[[" in plain or "]]" in plain:
            drops["contains_marker"] += 1
            continue
        for (s, e, f) in spans(fine):
            if f not in top:
                continue
            state = detok(list(toks[:s]) + ["[["] + list(toks[s:e]) + ["]]"] + list(toks[e:]))
            span_txt = detok(list(toks[s:e]))
            if not (20 <= len(state) <= 6000):
                drops["state_length"] += 1
                continue
            if len(toks) < 5:
                drops["sentence_under_5_tokens"] += 1
                continue
            if not any(ch.isalnum() for ch in span_txt):
                drops["span_no_alnum"] += 1
                continue
            cands[f].append({"sid": r["id"], "start": s, "end": e, "fine": f, "coarse": int(coarse[s]),
                             "span": span_txt, "state": state, "n_tokens": len(toks)})

    # 3) stratified sampling: 7 per type, +1 for (N_ITEMS - 7*N_TYPES) seeded types
    base = N_ITEMS // N_TYPES
    extra = set(rng.sample(sorted(top), N_ITEMS - base * N_TYPES))
    quota = {k: base + (1 if k in extra else 0) for k in top}
    for k in sorted(top):
        rng.shuffle(cands[k])
    ptr = {k: 0 for k in top}
    used_sid, used_span = set(), set()
    picked = {k: [] for k in top}
    order = sorted(top)
    skip = Counter()
    while any(len(picked[k]) < quota[k] for k in order):
        progressed = False
        for k in order:
            if len(picked[k]) >= quota[k]:
                continue
            while ptr[k] < len(cands[k]):
                c = cands[k][ptr[k]]
                ptr[k] += 1
                if c["sid"] in used_sid:
                    skip["sentence_already_used"] += 1
                    continue
                if norm(c["span"]) in used_span:
                    skip["span_string_already_used"] += 1
                    continue
                used_sid.add(c["sid"])
                used_span.add(norm(c["span"]))
                picked[k].append(c)
                progressed = True
                break
        if not progressed:
            raise SystemExit("ran out of candidates")
    chosen = [c for k in order for c in picked[k]]
    rng.shuffle(chosen)

    card = "\n".join(f"- {l}: {DEFS[l]}" for l in labels)  # card in frequency order (fixed for all rows)
    rows = []
    for c in chosen:
        gold = FINE_NAMES[c["fine"]]
        opts = list(labels)
        rng.shuffle(opts)
        key = f"{c['sid']}:{c['start']}-{c['end']}"
        rows.append({
            "id": "r_" + sha(f"ohs3:{TASK}:row:{key}")[:12],
            "group_id": f"g:ohs3:{TASK}:sent{c['sid']}",
            "call_id": "c_" + sha(f"ohs3:{TASK}:call:{key}")[:12],
            "split": "ohs3",
            "track": "U",
            "source": TASK,
            "state": c["state"],
            "qtype": "choice",
            "instructions": INSTR_TMPL.format(span=c["span"]),
            "options": opts,
            "gold": gold,
            "role": "choice",
            "card": card,
            "meta": {
                "task": TASK,
                "dataset": REPO,
                "config": CONFIG,
                "split": SPLIT,
                "revision": REV,
                "sentence_id": c["sid"],
                "span_token_start": c["start"],
                "span_token_end_exclusive": c["end"],
                "span_text": c["span"],
                "fine_tag": gold,
                "fine_tag_id": c["fine"],
                "coarse_tag": COARSE_NAMES[c["coarse"]],
                "original_label": gold,
                "url": f"https://huggingface.co/datasets/{REPO}/blob/{REV}/{PARQUET_REL}",
                "record": f"{REPO}@{REV} {CONFIG}/{SPLIT} id={c['sid']}",
                "licence": LICENCE,
                "attribution": ATTRIBUTION,
            },
        })

    # checks
    assert len(rows) == N_ITEMS
    assert len({r["id"] for r in rows}) == len({r["group_id"] for r in rows}) == len({r["call_id"] for r in rows}) == N_ITEMS
    g = Counter(r["gold"] for r in rows)
    assert max(g.values()) / len(rows) <= 0.40 and set(g.values()) <= {base, base + 1}
    for r in rows:
        assert 20 <= len(r["state"]) <= 6000
        assert r["state"].count("[[") == 1 and r["state"].count("]]") == 1
        assert r["gold"] in r["options"] and sorted(r["options"]) == sorted(labels)
        inner = r["state"].split("[[")[1].split("]]")[0]
        assert inner == r["meta"]["span_text"], (inner, r["meta"]["span_text"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text)

    lens = sorted(len(r["state"]) for r in rows)
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "choice",
        "track": "U",
        "n_options": N_TYPES,
        "class_balance": dict(sorted(g.items(), key=lambda x: (-x[1], x[0]))),
        "max_class_share": round(max(g.values()) / len(rows), 4),
        "coarse_balance": dict(Counter(r["meta"]["coarse_tag"] for r in rows)),
        "types_with_8_items": sorted(FINE_NAMES[k] for k in extra),
        "label_set": [{"label": FINE_NAMES[k], "test_span_count": freq[k]} for k in top],
        "next_excluded_types": [{"label": FINE_NAMES[k], "test_span_count": freq[k]} for k in ranked[N_TYPES:N_TYPES + 3]],
        "boundary_tie_at_rank_20": boundary_tie,
        "instructions_template": INSTR_TMPL,
        "card": card,
        "label_definitions_source": "author-written (label names are the official Few-NERD fine-type names from the dataset card / paper); one neutral definition per label, written once and frozen",
        "author_written_definitions": DEFS,
        "source": f"Few-NERD (Ding et al. 2021), HF {REPO} config={CONFIG} split={SPLIT}",
        "revision": REV,
        "snapshot": {"cache_dir": str(CACHE.relative_to(LEAN)), "parquet": PARQUET_REL, "parquet_sha256": pq_sha,
                     "readme_sha256": readme_sha, "sentences_in_split": len(tbl)},
        "licence": LICENCE,
        "attribution": ATTRIBUTION,
        "date_range": "Few-NERD released 2021 (text from English Wikipedia, pre-2021); no per-item dates; track U",
        "pool": {"candidate_spans_per_type": {FINE_NAMES[k]: len(cands[k]) for k in top}, "dropped": dict(drops),
                 "sampling_skips": dict(skip)},
        "sampling": (f"type freq = span count in test split; top {N_TYPES} (seeded tie-break); candidates per type sorted by "
                     f"(sentence id, span start) then random.Random({SEED}).shuffle; round-robin over types in sorted-id "
                     "order taking the next candidate whose sentence and normalised span string are unused; quota 7 per "
                     "type, +1 for 2 seeded types; rows shuffled; options shuffled per row with the same RNG"),
        "state_format": "detokenised sentence (tokens joined; spacing fixed around punctuation/clitics; `` and '' shown as \"), target span wrapped in [[ ]]",
        "state_length": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "sentence_ids": sorted((r["meta"]["sentence_id"] for r in rows), key=int),
        "output_sha256": sha(text),
        "uncertain": [
            "Few-NERD uses IO tagging, so two adjacent entities with the same fine tag merge into one span; a marked span may occasionally cover two entities of the same type (gold type still correct).",
            "Few-NERD gold labels are crowd/expert annotated and have known noise, especially person-other vs person-artist/author/athlete and building-other vs location-other; gold is kept as the source label.",
            "Definitions are author-written; the '-other' definitions name all official sibling subtypes, including ones not among the 20 options (e.g. person-scholar), matching the source taxonomy.",
            "Detokenisation is heuristic (layout only); Few-NERD writes both opening and closing double quotes as ``, which are rendered as \" by alternation; sentences with an odd number of double-quote tokens are dropped. Source tokenisation artefacts such as `` s for a possessive after a quoted title (shown as \"Alicia\" s) and a lone ' for plural possessives are kept as-is.",
            "Few-NERD text is from Wikipedia and the dataset has been public since 2021, so contamination of pretraining data is likely (track U).",
            "Instructions differ per row only by the quoted span (as the spec asks).",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("sentence_ids", "card", "author_written_definitions")},
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
