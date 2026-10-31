"""Shared helpers for the relations_entities golden builders (v14, round 2). CPU-only, deterministic, no model calls.

Family goal: multi-way (choice) decisions about how two marked entities are related, or what type a marked entity
is. Every state carries the entity markers inline: <e1>...</e1> / <e2>...</e2> for relation rows, <e>...</e> for
entity-typing rows.

- fetch(): pinned URL download into golden_src/relations_entities/cache/<key>/ with a sha256 check.
- decon(): drops candidate records whose texts share an exact normalised text (>= 6 words) or a 10-word run with
  (a) every premise of tasksource/zero-shot-label-nli (forbidden: all 152 tasks incl. sem_eval_2010_task_8 and sciie;
  read only to drop overlaps), (b) every local *.jsonl under lean/ and ../data except held-out/eval files
  (ohs*, preds*, results*), caches and data/v14_parts, (c) the JevBench public splits, and (d) extra exclusion lists
  passed by the builder (OHS-3 sources FewRel + Few-NERD for Wikipedia text; the PubMed-based OHS-1/2 sources for
  PubMed text). OHS files are never opened. Verdicts are cached per text hash in cache/_decon/<key>.json.
- ohs3_wiki_texts(): all splits of FewRel (thunlp/FewRel data/*.json) and Few-NERD (DFKI-SLT/few-nerd supervised),
  both OHS-3 sources, pinned; used ONLY as exclusion lists.
- pubmed_ohs_texts(): PubMed 20k RCT (all splits), Medical Abstracts TC, PubMedQA pqa_labeled, SciFact corpus and the
  DDI 2013 corpus (OHS-1/2 sources), same pins as round 1 (crowdtruth_mre); exclusion lists only.
- cross_v14(): overlap check against the OTHER golden v14 raw parts already written (and earlier keys of this family).
- NearDup: exact + near-exact (word 5-gram MinHash, Jaccard >= thr) duplicate detector.
- detok(): joins a whitespace-tokenised sentence back into ordinary text (DocRED / CoNLL style tokens).
- write_outputs() / manifest_record() / append_manifest(): raw rows, defs and the MANIFEST record (file-locked,
  replaces an older record of the same key so reruns do not duplicate it).
"""
import collections
import fcntl
import hashlib
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # golden_src/relations_entities
GOLDEN = HERE.parent                               # golden_src
LEAN = GOLDEN.parent                               # lean
ROOT = LEAN.parent                                 # opendecide-data
JEV = ROOT.parent                                  # jev
CACHE = HERE / "cache"
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"
FAMILY = "relations_entities"
YN = ["yes", "no"]
SEED = 20261129
EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal",
             "numeric", "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit",
             "long_context", "table", "multi_hop", "ambiguous"}

HF_HUB = Path.home() / ".cache" / "huggingface" / "hub"
LABEL_NLI_REV = "ee693dba923b5d5484aa9232b7357c5e45dd39b8"
LABEL_NLI_DIR = HF_HUB / f"datasets--tasksource--zero-shot-label-nli/snapshots/{LABEL_NLI_REV}/data"
LABEL_NLI_URL = "https://huggingface.co/datasets/tasksource/zero-shot-label-nli/resolve/{rev}/data/{name}"
LABEL_NLI_FILES = {  # name -> sha256 (LFS oid)
    "test-00000-of-00001-c260d1ee78ad6397.parquet": "a7bc5319f8af2704adaba91a3aef8290913e2e3651f46225130e4bfd1cc0864d",
    "train-00000-of-00002-970172c89e89b5df.parquet": "aa0fe36796bc0ac46755738128dc101918303fed9c9a5c48aeced4d6060745b5",
    "train-00001-of-00002-509e762f01abeb95.parquet": "2d4ee59ed8c9d9e0e4cdd4b89aad0e8b4d00c68e7ef1c326f97bd2e55e1eb556",
    "validation-00000-of-00001-79d9ba1d8f02bef0.parquet": "f45c234013c9d994c39f9907403056564e120ef67b6492cc20faf5fac826e5ca",
}
JEVBENCH_PUBLIC = JEV / "bench" / "jevbench" / "datasets" / "public"
RUN = 10          # word-run length for overlap
MIN_EXACT = 6     # exact-match only for texts of at least this many words

# OHS-3 sources (forbidden; exclusion lists only)
FEWREL_COMMIT = "278a2315d2138810a379cd8d5718914dc56e2582"
FEWREL_FILES = {  # thunlp/FewRel data/<name> -> sha256
    "train_wiki.json": "8e9e58a05d559be773cbe18a8d4a16ba17e6d397663f9f05a056f894a94b92c1",
    "val_wiki.json": "76bb44c2485b6faed358a3ce040eadafcc8a8835245cd7e6afc1bef672d4a0bf",
    "val_pubmed.json": "fc0f13b534f6664fe0d8aec231d7590313bc6510d00dbc1b6746147f6a2b46e6",
    "val_nyt.json": "b519adc61a2bab0f05178e33a3cd8f284338b635629493e9e09616ba81bb428e",
    "val_semeval.json": "fd79cf35481f6596c23b92cd3ded3265481f3027a4b78d99921104f8fe632eb5",
    "pubmed_unsupervised.json": "fa3555941364024c2ac1b1857396515ecc65a515bc742e9da0502568fad5dd1f",
}
FEWNERD_REV = "205f3e9c9f3577ea2561d43f2f62dc249ab92d5b"
FEWNERD_FILES = {  # DFKI-SLT/few-nerd supervised/<name> -> sha256 (LFS oid)
    "train-00000-of-00001.parquet": "6ccb192b1accd3d1754db2244d18ddf64040357fb5b9076a338ec421a72d7d61",
    "validation-00000-of-00001.parquet": "d502de918f2a6510179e64bc8b7cfff4e28999188e308f8b0fe75bd71844da66",
    "test-00000-of-00001.parquet": "b7ad746fcbeb68fcc235ba7142d7c3723ea2dc39930089e947284defecf300c6",
}
# PubMed-based OHS-1/2 sources (exclusion lists only; same pins as round-1 crowdtruth_mre)
RCT_REV = "17ed2cb0590decfca0266add0c76f254f67232b4"
RCT_BASE = f"https://raw.githubusercontent.com/Franck-Dernoncourt/pubmed-rct/{RCT_REV}/PubMed_20k_RCT/"
RCT_FILES = {"train.txt": "8fda243202edd207fb61214e21f5629bba545522b921816d20d516e64d602d5b",
             "dev.txt": "8561119a162708a87e3138103470d10781c6b94ba390183d7d6df6297a738a25",
             "test.txt": "8511b832c1ee66b3df52df23c16ad81a69711ddd5b3a485421da3f8e9d5b44f4"}
OHS_BIO = {
    "medical_abstracts_train.parquet": ("https://huggingface.co/datasets/TimSchopf/medical_abstracts/resolve/"
                                        "d6afbd7ff4eb215db2470980023d7d7a3dfee7dc/data/train-00000-of-00001.parquet",
                                        "0c32fa436349619a2f95dd7338a57e896ff98e6537c71de89b053bcb24aef6b0"),
    "medical_abstracts_test.parquet": ("https://huggingface.co/datasets/TimSchopf/medical_abstracts/resolve/"
                                       "d6afbd7ff4eb215db2470980023d7d7a3dfee7dc/data/test-00000-of-00001.parquet",
                                       "c4f720ada4b69e5fc8f37f4965397839d45a061d5ebb663f3bf2cce2b1209f04"),
    "pubmedqa_pqa_labeled.parquet": ("https://huggingface.co/datasets/qiaojin/PubMedQA/resolve/"
                                     "9001f2853fb87cab8d220904e0de81ac6973b318/pqa_labeled/train-00000-of-00001.parquet",
                                     "3d56bd1abc11884579ecc3aab9dd3cdfce8b7cf54715daeca93b8022b7be231c"),
    "scifact_data.tar.gz": ("https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz",
                            "11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be"),
    "DDICorpus-2013.zip": ("https://raw.githubusercontent.com/isegura/DDICorpus/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/"
                           "DDICorpus-2013.zip", "87fc63e32ebce20d9841c372e0c594ec72d60882ab5621550ca73c3eaf80ab60"),
}


# ----------------------------------------------------------------------------------------------- download
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, path, sha):
    """Download once into cache/ and verify the pinned sha256 (sha=None only while pinning a new file)."""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        import requests
        tmp = path.with_suffix(path.suffix + ".part")
        with requests.get(url, headers={"User-Agent": "opendecide-golden-builder"}, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
        tmp.rename(path)
    got = sha256(path)
    if sha is None:
        print(f"PIN {path.name}: {got}")
    elif got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got} != {sha}")
    return path


# ----------------------------------------------------------------------------------------------- text utils
def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", str(t).lower()).strip()


def words(t):
    return re.findall(r"[a-z0-9]+", str(t).lower())


def clean(t):
    """Whitespace tidy only (no rewording)."""
    t = str(t).replace(" ", " ").replace("​", "").replace("\r", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def strip_markers(t):
    return re.sub(r"</?e[12]?>", "", t)


_NO_SPACE_BEFORE = {",", ".", ";", ":", "!", "?", ")", "]", "}", "%", "'s", "'S", "n't", "'re", "'ve", "'ll", "'d",
                    "'m", "''", "…"}
_NO_SPACE_AFTER = {"(", "[", "{", "``", "$", "#"}


def detok(tokens):
    """Join whitespace tokens (PTB/DocRED style) into readable text. Tokens may carry marker tags (<e1>...)."""
    out = ""
    prev = None
    quote_open = False
    for tok in tokens:
        core = strip_markers(tok)
        if prev is None:
            out = tok
        else:
            pc = strip_markers(prev)
            glue = False
            if core in _NO_SPACE_BEFORE or core.lower() in {"'s", "'re", "'ve", "'ll", "'d", "'m", "’s", "’re", "’ve",
                                                             "’ll", "’d", "’m", "n’t"}:
                glue = True
            elif core in {"'", "’"} and pc.endswith(("s", "S")):
                glue = True
            elif pc in _NO_SPACE_AFTER:
                glue = True
            elif core in {"-", "–", "/"} or pc in {"-", "–", "/"}:
                glue = True
            elif core == '"':
                glue = quote_open
            elif pc == '"' and quote_open:
                glue = True
            if tok.startswith("<e") and not tok.startswith("</") and core in _NO_SPACE_BEFORE:
                glue = False
            out += ("" if glue else " ") + tok
        if core == '"':
            quote_open = not quote_open
        prev = tok
    out = out.replace("``", '"').replace("''", '"')
    return out


NEG = re.compile(r"\b(not|no|never|none|nobody|nothing|neither|nor|without|cannot|fail(ed|s)? to)\b|n't\b", re.I)
HEDGE = re.compile(r"\b(may|might|could|possibly|potential(ly)?|putative|suggest(s|ed)?|whether|hypothes\w+)\b", re.I)
REPORTED = re.compile(r"\b(said|says|according to|claims?|claimed|told|reported|announced)\b", re.I)
NUMERIC = re.compile(r"\d")


def edge_join(tags):
    tags = [t for t in dict.fromkeys(tags) if t]
    for t in tags:
        assert t in EDGE_TAGS, t
    return ",".join(tags) if tags else None


# ----------------------------------------------------------------------------------------------- near-dup
def shingles(t, n=5):
    w = words(t)
    if len(w) < n:
        return {" ".join(w)}
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


class NearDup:
    """Exact (normalised) + near-exact (MinHash LSH over word 5-gram shingles, Jaccard >= thr) detector."""

    def __init__(self, thr=0.7, k=32, bands=8):
        self.thr, self.k, self.bands = thr, k, bands
        self.r = k // bands
        self.exact = set()
        self.buckets = collections.defaultdict(list)
        self.sh = []
        self.seeds = [int(hashlib.md5(str(i).encode()).hexdigest()[:8], 16) for i in range(k)]

    def _sig(self, sh):
        hs = [int(hashlib.md5(s.encode()).hexdigest()[:12], 16) for s in sh]
        return [min((h ^ sd) for h in hs) for sd in self.seeds]

    def seen(self, text, add=True):
        n = norm(text)
        if n in self.exact:
            return True
        sh = shingles(text)
        sig = self._sig(sh)
        keys = [(b, tuple(sig[b * self.r:(b + 1) * self.r])) for b in range(self.bands)]
        cands = set()
        for key in keys:
            cands.update(self.buckets.get(key, ()))
        for c in sorted(cands):
            o = self.sh[c]
            if len(sh & o) / max(1, len(sh | o)) >= self.thr:
                return True
        if add:
            self.exact.add(n)
            idx = len(self.sh)
            self.sh.append(sh)
            for key in keys:
                self.buckets[key].append(idx)
        return False


# ----------------------------------------------------------------------------------------------- exclusion lists
def ohs3_wiki_texts():
    """{'fewrel': [...], 'fewnerd': [...]}: every sentence of FewRel (all released files) and Few-NERD (supervised
    train/validation/test = all 188k sentences). OHS-3 sources; used only to DROP overlapping records."""
    import pandas as pd
    out = {"fewrel": [], "fewnerd": []}
    for name, sha in FEWREL_FILES.items():
        url = f"https://raw.githubusercontent.com/thunlp/FewRel/{FEWREL_COMMIT}/data/{name}"
        p = fetch(url, CACHE / "_excl" / "fewrel" / name, sha)
        d = json.loads(p.read_text())
        if isinstance(d, dict):
            items = [x for v in d.values() for x in v]
        else:
            items = d
        for x in items:
            toks = x.get("tokens") if isinstance(x, dict) else None
            if toks:
                out["fewrel"].append(" ".join(toks))
    for name, sha in FEWNERD_FILES.items():
        url = f"https://huggingface.co/datasets/DFKI-SLT/few-nerd/resolve/{FEWNERD_REV}/supervised/{name}"
        p = fetch(url, CACHE / "_excl" / "fewnerd" / name, sha)
        df = pd.read_parquet(p, columns=["tokens"])
        out["fewnerd"] += [" ".join(t) for t in df["tokens"]]
    return out


def pubmed_ohs_texts():
    """{source: [texts]} of the PubMed-based OHS sources (exclusion only)."""
    import tarfile
    import zipfile
    import xml.etree.ElementTree as ET
    import pandas as pd
    out = {"pubmed_rct": [], "medical_abstracts": [], "pubmedqa": [], "scifact": [], "ddi2013": []}
    for n, sha in RCT_FILES.items():
        p = fetch(RCT_BASE + n, CACHE / "_excl" / "pubmed_20k_rct" / n, sha)
        for line in open(p, encoding="utf-8"):
            if "\t" in line:
                out["pubmed_rct"].append(line.split("\t", 1)[1])
    f = {n: fetch(u, CACHE / "_excl" / n, h) for n, (u, h) in OHS_BIO.items()}
    for n in ("medical_abstracts_train.parquet", "medical_abstracts_test.parquet"):
        out["medical_abstracts"] += pd.read_parquet(f[n])["medical_abstract"].astype(str).tolist()
    d = pd.read_parquet(f["pubmedqa_pqa_labeled.parquet"])
    out["pubmedqa"] = [" ".join(c["contexts"]) for c in d["context"]] + d["long_answer"].astype(str).tolist()
    with tarfile.open(f["scifact_data.tar.gz"]) as tf:
        for line in tf.extractfile("data/corpus.jsonl").read().decode().splitlines():
            o = json.loads(line)
            out["scifact"] += [o["title"]] + o["abstract"]
    with zipfile.ZipFile(f["DDICorpus-2013.zip"]) as zf:
        for n in zf.namelist():
            if n.endswith(".xml"):
                out["ddi2013"] += [x.get("text") or "" for x in ET.fromstring(zf.read(n)).iter("sentence")]
    return out


# ----------------------------------------------------------------------------------------------- decontamination
def _is_skipped(rel_parts):
    parts = [x.lower() for x in rel_parts]
    if any(x.startswith(("ohs", "preds", "results")) for x in parts):
        return True
    if "cache" in parts or ".venv" in parts or "v14_parts" in parts or "node_modules" in parts:
        return True
    if parts and parts[-1] == "manifest.jsonl":
        return True
    return False


def scan_files():
    fs = set()
    for base in (LEAN, ROOT / "data"):
        if not base.exists():
            continue
        for p in base.rglob("*.jsonl"):
            rel = p.relative_to(base)
            if _is_skipped(rel.parts):
                continue
            fs.add(p)
    if JEVBENCH_PUBLIC.exists():
        fs |= set(JEVBENCH_PUBLIC.glob("*.jsonl"))
    return sorted(fs)


def label_nli_files():
    out = []
    for name, sha in LABEL_NLI_FILES.items():
        p = LABEL_NLI_DIR / name
        if not p.exists():
            p = fetch(LABEL_NLI_URL.format(rev=LABEL_NLI_REV, name=name), CACHE / "_label_nli" / name, sha)
        out.append(p)
    return out


def _thash(t):
    return hashlib.sha1(" ".join(words(t)).encode()).hexdigest()


def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


def decon(core, cache_name, verbose=True, extra_texts=None):
    """core: {rid: [text, ...]} -> {rid: reason} for records that overlap a forbidden / used / eval text.
    extra_texts: optional {reason: iterable of texts} also treated as forbidden (OHS source exclusion lists)."""
    import pandas as pd
    files = scan_files()
    sig = hashlib.sha1(json.dumps([[str(p), p.stat().st_size] for p in files] + [LABEL_NLI_REV]).encode()).hexdigest()
    cpath = CACHE / "_decon" / f"{cache_name}.json"
    cached = {}
    if cpath.exists():
        blob = json.loads(cpath.read_text())
        if blob.get("sig") == sig:
            cached = blob["verdicts"]
    text_by_h = {}
    for rid, texts in core.items():
        for t in texts:
            text_by_h[_thash(t)] = t
    todo = {h: t for h, t in text_by_h.items() if h not in cached}
    if todo:
        exact = collections.defaultdict(set)
        owner = collections.defaultdict(set)
        for h, t in todo.items():
            w = words(t)
            if len(w) >= MIN_EXACT:
                exact[" ".join(w)].add(h)
            for i in range(len(w) - RUN + 1):
                owner[hash(tuple(w[i:i + RUN]))].add(h)
        found = {}

        def check_words(w, reason):
            if not w:
                return
            for h in exact.get(" ".join(w), ()):
                found.setdefault(h, reason)
            for i in range(len(w) - RUN + 1):
                k = hash(tuple(w[i:i + RUN]))
                if k in owner:
                    for h in owner[k]:
                        found.setdefault(h, reason)

        for p in label_nli_files():
            df = pd.read_parquet(p, columns=["premise"])
            for t in set(df["premise"].astype(str)):
                check_words(words(t), "label_nli")
        for p in files:
            reason = "jevbench" if JEVBENCH_PUBLIC in p.parents else f"local:{p.name}"
            with open(p, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        check_words(words(line), reason)
                        continue
                    for s in _strings(obj):
                        if len(s) >= 20:
                            check_words(words(s), reason)
        for h in todo:
            cached[h] = found.get(h)
        cpath.parent.mkdir(parents=True, exist_ok=True)
        cpath.write_text(json.dumps({"sig": sig, "verdicts": cached}))
    hits = {}
    for rid, texts in core.items():
        for t in texts:
            v = cached.get(_thash(t))
            if v:
                hits.setdefault(rid, v)
                break
    if extra_texts:
        exact = collections.defaultdict(set)
        owner = collections.defaultdict(set)
        for rid, texts in core.items():
            for t in texts:
                w = words(t)
                if len(w) >= MIN_EXACT:
                    exact[" ".join(w)].add(rid)
                for i in range(len(w) - RUN + 1):
                    owner[hash(tuple(w[i:i + RUN]))].add(rid)
        for reason, texts in extra_texts.items():
            for t in texts:
                w = words(t)
                for rid in exact.get(" ".join(w), ()):
                    hits.setdefault(rid, reason)
                for i in range(len(w) - RUN + 1):
                    for rid in owner.get(hash(tuple(w[i:i + RUN])), ()):
                        hits.setdefault(rid, reason)
    if verbose:
        print(f"decon: {len(core)} records ({len(todo)} new texts scanned over {len(files)} files + label-NLI), "
              f"hits={len(hits)} {dict(collections.Counter(v.split(':')[0] for v in hits.values()))}")
    return hits


# A key is checked against every other family's parts and against the family keys EARLIER in this list.
FAMILY_ORDER = ["redocred", "webred", "drugprot", "biored", "ncbi_disease", "crossner", "wnut17"]


def cross_v14(core, own_keys, verbose=True, exact_min=MIN_EXACT):
    """{rid: [text, ...]} -> {rid: 'v14:<key>'} for records sharing an exact normalised text (>= 6 words) or a
    10-word run with a state in another golden v14 raw part (not our own keys, and not this family's keys that come
    later in FAMILY_ORDER)."""
    own_keys = set(own_keys)
    for k in list(own_keys & set(FAMILY_ORDER)):
        own_keys |= set(FAMILY_ORDER[FAMILY_ORDER.index(k) + 1:])
    exact = collections.defaultdict(set)
    owner = collections.defaultdict(set)
    for rid, texts in core.items():
        for t in texts:
            w = words(strip_markers(t))
            if len(w) >= exact_min:
                exact[" ".join(w)].add(rid)
            for i in range(len(w) - RUN + 1):
                owner[hash(tuple(w[i:i + RUN]))].add(rid)
    hits = {}
    for p in sorted(RAW_DIR.glob("*.jsonl")):
        k = p.stem
        if k in own_keys:
            continue
        with open(p) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                w = words(strip_markers(obj.get("state", "")))
                for rid in exact.get(" ".join(w), ()):
                    hits.setdefault(rid, f"v14:{k}")
                for i in range(len(w) - RUN + 1):
                    h = hash(tuple(w[i:i + RUN]))
                    if h in owner:
                        for rid in owner[h]:
                            hits.setdefault(rid, f"v14:{k}")
    if verbose:
        print(f"cross_v14: {len(core)} records, hits={len(hits)} {dict(collections.Counter(hits.values()))}")
    return hits


# ----------------------------------------------------------------------------------------------- balance
def capped_round_robin(pools, n, cap_share=0.5, rng=None):
    """pools: {label: [items]} (already shuffled). Takes items round-robin (rarest label first each pass) until n
    items or pools run dry; no label exceeds cap_share of the result."""
    labels = sorted(pools, key=lambda k: (len(pools[k]), k))
    out = []
    cnt = collections.Counter()
    idx = {k: 0 for k in labels}
    while len(out) < n:
        progressed = False
        for k in labels:
            if len(out) >= n:
                break
            if idx[k] < len(pools[k]):
                out.append((k, pools[k][idx[k]]))
                idx[k] += 1
                cnt[k] += 1
                progressed = True
        if not progressed:
            break
    # enforce the share cap
    while out:
        top, c = cnt.most_common(1)[0]
        if c <= cap_share * len(out):
            break
        for i in range(len(out) - 1, -1, -1):
            if out[i][0] == top:
                out.pop(i)
                cnt[top] -= 1
                break
    return [x for _, x in out]


# ----------------------------------------------------------------------------------------------- output
def check_rows(key, rows, defs_by_qid, soft_required=False):
    assert rows, "no rows"
    rids = [r["rid"] for r in rows]
    assert len(set(rids)) == len(rids), "duplicate rid"
    states = [norm(strip_markers(r["state"])) for r in rows]
    assert all(states), "empty state"
    assert len(set(states)) == len(states), "duplicate state"
    for r in rows:
        assert set(r) == {"key", "rid", "state", "instructions", "options", "gold", "soft", "meta"}, r.keys()
        assert r["key"] == key
        assert r["instructions"].strip() and r["gold"] in r["options"], r
        assert len(set(r["options"])) == len(r["options"]), r["options"]
        assert r["meta"]["split"] == "train"
        assert r["meta"]["family"] == FAMILY
        e = r["meta"].get("edge")
        assert e is None or all(x in EDGE_TAGS for x in e.split(",")), e
        qid = r["meta"].get("defs")
        d = defs_by_qid[qid] if qid else defs_by_qid[None]
        assert all(o in d for o in r["options"]), (qid, [o for o in r["options"] if o not in d])
        if r["options"] != YN:
            assert 3 <= len(r["options"]) <= 60, len(r["options"])
        if soft_required:
            assert r["soft"] is not None
        if r["soft"] is not None:
            assert set(r["soft"]) == set(r["options"]), (r["soft"], r["options"])
            assert abs(sum(r["soft"].values()) - 1) < 1e-6, r["soft"]
            assert r["soft"][r["gold"]] >= max(r["soft"].values()) - 1e-9, (r["gold"], r["soft"])
    yn = [r for r in rows if r["options"] == YN]
    if yn:
        share = sum(r["gold"] == "yes" for r in yn) / len(yn)
        assert 0.35 <= share <= 0.65, f"yes share {share:.3f}"
    ch = [r for r in rows if r["options"] != YN]
    if ch:
        top = max(collections.Counter(r["gold"] for r in ch).values()) / len(ch)
        assert top <= 0.5 + 1e-9, f"choice class share {top:.3f}"
    for qid, d in defs_by_qid.items():
        for k, v in d.items():
            assert v.strip(), (qid, k)
            assert len(v.split()) <= 48, (qid, k, len(v.split()))
    return True


def write_outputs(key, rows, defs_by_qid, soft_required=False):
    """defs_by_qid: {None: {...default...}, "<qid>": {...}}"""
    check_rows(key, rows, defs_by_qid, soft_required)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DEFS_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"{key}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    for qid, d in defs_by_qid.items():
        name = f"{key}.json" if qid is None else f"{key}__{qid}.json"
        with open(DEFS_DIR / name, "w") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return out


def summary(key, rows):
    yn = [r for r in rows if r["options"] == YN]
    ch = [r for r in rows if r["options"] != YN]
    edges = collections.Counter(t for r in rows for t in (r["meta"].get("edge") or "").split(",") if t)
    ys = (sum(r["gold"] == "yes" for r in yn) / len(yn)) if yn else None
    gold_ch = collections.Counter(r["gold"] for r in ch)
    lens = sorted(len(r["state"]) for r in rows)
    nopt = sorted(len(r["options"]) for r in rows)
    print(f"[{key}] rows={len(rows)} yesno={len(yn)} choice={len(ch)} yes_share={ys}")
    if ch:
        top = gold_ch.most_common(1)[0]
        print(f"  choice golds: {len(gold_ch)} distinct; top={top[0]!r} {top[1] / len(ch):.1%}")
        print(f"  gold dist: {dict(gold_ch.most_common())}")
    print(f"  options per row: min={nopt[0]} median={nopt[len(nopt) // 2]} max={nopt[-1]}")
    print(f"  edge tags: {dict(edges.most_common())} (untagged {sum(not r['meta'].get('edge') for r in rows)})")
    print(f"  state chars: min={lens[0]} median={lens[len(lens) // 2]} max={lens[-1]}")
    print(f"  soft coverage: {sum(r['soft'] is not None for r in rows)}/{len(rows)}")
    return {"yes_share": round(ys, 4) if ys is not None else None, "edges": edges, "n_yn": len(yn), "n_ch": len(ch)}


def show_samples(rows, n=5, seed=7):
    rng = random.Random(seed)
    for r in rng.sample(rows, min(n, len(rows))):
        print("-" * 100)
        print("RID:", r["rid"], "| edge:", r["meta"].get("edge"), "| defs:", r["meta"].get("defs"),
              "| orig:", json.dumps(r["meta"].get("orig_label"), ensure_ascii=False)[:300])
        print("STATE:\n" + r["state"][:2500])
        print("Q:", r["instructions"])
        print("OPTIONS:", r["options"], "| GOLD:", r["gold"], "| SOFT:", r["soft"])


def append_manifest(rec):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.touch(exist_ok=True)
    with open(MANIFEST, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            lines = [ln for ln in f.read().splitlines() if ln.strip()]
            keep = []
            for ln in lines:
                try:
                    o = json.loads(ln)
                    if o.get("key") == rec["key"]:
                        assert o.get("family") == FAMILY, "refusing to replace another family's record"
                        continue
                except json.JSONDecodeError:
                    pass
                keep.append(ln)
            keep.append(json.dumps(rec, ensure_ascii=False))
            f.seek(0)
            f.truncate()
            f.write("\n".join(keep) + "\n")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def manifest_record(key, dataset, licence, rows, qtype, notes, stats):
    return {"key": key, "family": FAMILY, "dataset": dataset, "licence": licence, "rows": len(rows), "qtype": qtype,
            "yesno_share": stats["yes_share"] if stats["yes_share"] is not None else 0.0,
            "edge_tags": sorted(stats["edges"]), "notes": notes}


# ----------------------------------------------------------------------------------------------- sentence split
_ABBREV = {"e.g", "i.e", "vs", "fig", "figs", "et al", "al", "approx", "ca", "cf", "dr", "mr", "mrs", "ms", "st",
           "no", "nos", "ref", "refs", "resp", "vol", "inc", "ltd", "co", "corp", "jr", "sr", "etc", "spp", "sp",
           "var", "subsp", "min", "max", "u.s", "p", "eq", "eqs", "dept", "univ", "viz"}
_BOUNDARY = re.compile(r"[.?!]['\")\]]?\s+(?=[A-Z0-9\[(\"'])")


def split_sentences(text, protected=()):
    """Character spans [(start, end)] of sentences in a biomedical abstract. A boundary is [.?!] + space + an
    upper-case letter / digit / bracket, except after a known abbreviation, a single capital initial, or inside a
    protected span (entity mentions)."""
    bounds = []
    for m in _BOUNDARY.finditer(text):
        end = m.start() + 1
        pre = text[max(0, m.start() - 12):m.start()]
        last = re.split(r"[\s(\[]", pre)[-1].lower().rstrip(".")
        if last in _ABBREV or re.fullmatch(r"[a-z]", last):
            continue
        # review fix: '13. 8%' / 'EC 1. 14. 16. 1' (a decimal point followed by a space in the source text) is not a
        # boundary; splitting there produced fragments such as '8% of northern Chinese ... (2.'
        if text[m.start() - 1:m.start()].isdigit() and text[m.end():m.end() + 1].isdigit():
            continue
        if any(a < end <= b or a <= m.end() - 1 < b for a, b in protected):
            continue
        bounds.append((end, m.end()))
    spans, start = [], 0
    for end, nxt in bounds:
        spans.append((start, end))
        start = nxt
    spans.append((start, len(text)))
    return [(a, b) for a, b in spans if text[a:b].strip()]


def sha256_text(t):
    return hashlib.sha256(str(t).encode("utf-8")).hexdigest()
