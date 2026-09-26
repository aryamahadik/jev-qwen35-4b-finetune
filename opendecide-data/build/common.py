"""OpenDecide v1.0-rc build: shared helpers.

Everything a build step needs that is not step-specific lives here:
  * paths (all relative to the opendecide-data root; never write outside it except the HF cache)
  * config and lock access (build/config.yaml, build/sources.lock.json)
  * seed derivation (DESIGN 13 step 0) and stable hashing
  * id helpers (row id, call_id, group_id, key; DESIGN 1.1)
  * dedup text normalisation (DESIGN 9.1 step 1)
  * deterministic JSON / JSONL IO (sorted keys, sorted rows, atomic writes, sha256)
  * the normalised-record contract {source, split, source_id, text, label, soft, meta} and its validator
  * source hygiene helpers used by loaders (PII masking, HTML unescape)
  * GitHub file fetch at a pinned commit (into the HF cache, never into the repo)
  * logging and step checkpoints (data/interim/checkpoints/)

Import it from a step with ``sys.path.insert(0, <build dir>)`` then ``import common``.
Only the standard library, PyYAML and (lazily) numpy / requests are imported here.

authored_by: llm:claude:foundation-engineer-1
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import logging
import math
import os
import re
import sys
import tempfile
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

AUTHORED_BY = "llm:claude:foundation-engineer-1"

# ------------------------------------------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------------------------------------------
BUILD_DIR = Path(__file__).resolve().parent
ROOT = BUILD_DIR.parent                                  # opendecide-data/
DESIGN_MD = ROOT / "DESIGN.md"
ASSETS = ROOT / "assets"
DATA = ROOT / "data"
INTERIM = DATA / "interim"
NORMALISED = INTERIM / "normalised"
CHECKPOINTS = INTERIM / "checkpoints"
LOG_DIR = INTERIM / "logs"
REPORTS = DATA / "reports"
STEPS_DIR = BUILD_DIR / "steps"
LOADERS_DIR = BUILD_DIR / "loaders"
SCHEMA_DIR = BUILD_DIR / "schema"
CONFIG_PATH = BUILD_DIR / "config.yaml"
LOCK_PATH = BUILD_DIR / "sources.lock.json"
BUILD_DECISIONS = ROOT / "design" / "build_decisions.md"
VENV_PYTHON = ROOT / ".venv" / "bin" / "python"
HF_HOME = Path(os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface")))
GITHUB_CACHE = HF_HOME / "opendecide" / "github"        # raw GitHub files at pinned commits (DESIGN 3: never in repo)

SEED_ENV = "OPENDECIDE_SEED"


def rel(path: Path | str) -> str:
    """Path relative to the opendecide-data root, POSIX style (for logs, checkpoints, reports)."""
    p = Path(path).resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def ensure_dirs() -> None:
    for d in (INTERIM, NORMALISED, CHECKPOINTS, LOG_DIR, REPORTS):
        d.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------------------------------------------------------
# Config and lock
# ------------------------------------------------------------------------------------------------------------------
@lru_cache(maxsize=1)
def load_config() -> dict:
    import yaml
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def cfg(*keys: str, default: Any = KeyError) -> Any:
    """Nested config lookup: cfg("caps", "jev_calls"). Raises KeyError unless a default is given."""
    node: Any = load_config()
    for k in keys:
        if isinstance(node, Mapping) and k in node:
            node = node[k]
        else:
            if default is KeyError:
                raise KeyError("config.yaml has no " + ".".join(keys))
            return default
    return node


def file_sha256(path: Path | str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def config_sha256() -> str:
    return file_sha256(CONFIG_PATH)


def load_lock() -> dict:
    """build/sources.lock.json, or {} before s01_lock has run."""
    if not LOCK_PATH.exists():
        return {}
    with open(LOCK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def pinned_revision(lock_key: str, *, kind: str = "sources") -> str:
    """Full commit sha for a source (or model) pin: the lock's resolved sha, else a full sha written in config.

    Raises RuntimeError when only a prefix is known (run s01_lock first).
    """
    entry = load_lock().get(kind, {}).get(lock_key)
    if entry and entry.get("status") == "resolved" and entry.get("resolved_sha"):
        return entry["resolved_sha"]
    pin = cfg(kind, lock_key, "revision", default=None)
    if isinstance(pin, str) and FULL_SHA.match(pin):
        return pin
    raise RuntimeError(f"{kind}.{lock_key}: no full revision (config pin {pin!r}); run build/steps/s01_lock.py")


# ------------------------------------------------------------------------------------------------------------------
# Seeds (DESIGN 13 step 0) and stable hashing
# ------------------------------------------------------------------------------------------------------------------
def master_seed() -> int:
    """The master seed: $OPENDECIDE_SEED (set by build.py --seed) or config master_seed (20260925)."""
    env = os.environ.get(SEED_ENV)
    if env:
        return int(env)
    try:
        return int(cfg("master_seed"))
    except Exception:  # config unreadable: fall back to the spec value
        return 20260925


def sub_seed(step: str, source: str = "", group: str = "", *, seed: int | None = None) -> int:
    """int(sha256(f"{seed}:{step}:{source}:{group}").hexdigest()[:16], 16)  (DESIGN 13 step 0)."""
    s = master_seed() if seed is None else int(seed)
    return int(hashlib.sha256(f"{s}:{step}:{source}:{group}".encode("utf-8")).hexdigest()[:16], 16)


def rng(step: str, source: str = "", group: str = "", *, seed: int | None = None):
    """numpy.random.Generator(PCG64(sub_seed(...))). The only sanctioned source of randomness in the build."""
    import numpy as np
    return np.random.Generator(np.random.PCG64(sub_seed(step, source, group, seed=seed)))


def stable_hash(*parts: Any, bits: int = 64) -> int:
    """Seed-independent stable integer hash of the joined parts (e.g. option_order_seed = stable_hash(group_id))."""
    s = "|".join(str(p) for p in parts)
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[: bits // 4], 16)


def seeded_rank_key(step: str, source: str, item_id: Any, *, seed: int | None = None) -> str:
    """Deterministic, seed-dependent sort key for "seeded rank order" sampling (sort ascending, take first k)."""
    s = master_seed() if seed is None else int(seed)
    return hashlib.sha256(f"{s}:{step}:{source}:rank:{item_id}".encode("utf-8")).hexdigest()


# ------------------------------------------------------------------------------------------------------------------
# Ids (DESIGN 1.1)
# ------------------------------------------------------------------------------------------------------------------
SPLITS = ("train", "dev", "dev_zs", "eval")
SPLIT_CODES = {"train": "T", "dev": "D", "dev_zs": "Z", "eval": "E"}


def sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def canonical_json(obj: Any) -> str:
    """Canonical JSON used for hashing object-valued states (CMP) and for every file we write."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def row_id(key: str, *, seed: int | None = None) -> str:
    """"r_" + sha1(f"{seed}|{key}")[:12]; opaque, never encodes role or gold."""
    s = master_seed() if seed is None else int(seed)
    return "r_" + sha1_hex(f"{s}|{key}")[:12]


def call_id(split: str, state: Any, *, seed: int | None = None) -> str:
    """"c_" + sha1(f"{seed}|{split}|{state}")[:12]; byte-identical state => one Jev call. Object states are hashed
    as canonical JSON (only CMP-B77 has one)."""
    s = master_seed() if seed is None else int(seed)
    state_s = state if isinstance(state, str) else canonical_json(state)
    return "c_" + sha1_hex(f"{s}|{split}|{state_s}")[:12]


def group_id(source: str, source_split: str, source_id: str) -> str:
    return f"g:{source}:{source_split}:{source_id}"


def fresh_group_id(family: str, n: int) -> str:
    return f"g:fresh:{family}:{int(n):03d}"


def row_key(split: str, source: str, source_split: str, source_id: str, state_variant: str, slot: str) -> str:
    """Readable key {split_code}:{source}:{source_split}:{source_id}#{state_variant}/{slot}, e.g.
    "E:banking77:test:1742#s0/q3"."""
    if split not in SPLIT_CODES:
        raise ValueError(f"unknown split {split!r}")
    return f"{SPLIT_CODES[split]}:{source}:{source_split}:{source_id}#{state_variant}/{slot}"


def relation_id(n: int) -> str:
    return f"rel_{int(n):06d}"


# ------------------------------------------------------------------------------------------------------------------
# Dedup normalisation (DESIGN 9.1 step 1): NFKC, lower-case, non-alphanumeric runs -> one space
# ------------------------------------------------------------------------------------------------------------------
_NON_ALNUM = re.compile(r"[\W_]+", re.UNICODE)


def norm_text(text: str) -> str:
    return _NON_ALNUM.sub(" ", unicodedata.normalize("NFKC", text).lower()).strip()


def norm_hash(text: str) -> str:
    """sha1 of norm_text (exact-duplicate detector key)."""
    return sha1_hex(norm_text(text))


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------------------------------------------------------
# Deterministic JSON / JSONL IO
# ------------------------------------------------------------------------------------------------------------------
def dumps(obj: Any) -> str:
    return canonical_json(obj)


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="." + path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.chmod(tmp, 0o644)                                     # mkstemp creates 0600
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def natural_key(value: Any) -> tuple:
    """Sort key that orders "2" before "10" and numbers before strings (stable across runs)."""
    s = str(value)
    return (0, int(s), "") if s.isdigit() else (1, 0, s)


def write_jsonl(path: Path | str, records: Iterable[Mapping], *,
                sort_key: str | Callable[[Mapping], Any] | None = "id") -> dict:
    """Write records as canonical JSONL (one object per line, "\\n" endings, UTF-8), sorted deterministically.

    sort_key: a field name (natural order), a callable, or None to keep the given order (only when the caller has
    already produced a deterministic order). Returns {"path", "n", "sha256"}.
    """
    path = Path(path)
    recs = list(records)
    if sort_key is not None:
        if callable(sort_key):
            recs.sort(key=sort_key)
        else:
            recs.sort(key=lambda r: natural_key(r[sort_key]))
    data = "".join(dumps(r) + "\n" for r in recs).encode("utf-8")
    _atomic_write_bytes(path, data)
    return {"path": rel(path), "n": len(recs), "sha256": hashlib.sha256(data).hexdigest()}


def read_jsonl(path: Path | str) -> Iterator[dict]:
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{i}: bad JSON: {exc}") from None


def write_json(path: Path | str, obj: Any, *, indent: int | None = 1) -> dict:
    """Pretty but deterministic JSON (sorted keys, trailing newline). Returns {"path", "sha256"}."""
    path = Path(path)
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=indent, allow_nan=False)
    data = (text + "\n").encode("utf-8")
    _atomic_write_bytes(path, data)
    return {"path": rel(path), "sha256": hashlib.sha256(data).hexdigest()}


def read_json(path: Path | str) -> Any:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_text(path: Path | str, text: str) -> dict:
    path = Path(path)
    data = text.encode("utf-8")
    _atomic_write_bytes(path, data)
    return {"path": rel(path), "sha256": hashlib.sha256(data).hexdigest()}


# ------------------------------------------------------------------------------------------------------------------
# Normalised-record contract (DESIGN 13 step 2)
#   {source, split, source_id, text, label, soft, meta}
# ------------------------------------------------------------------------------------------------------------------
RECORD_FIELDS = ("source", "split", "source_id", "text", "label", "soft", "meta")
_SOURCE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_SPLIT_RE = re.compile(r"^[a-z][a-z0-9_.-]*$")
_SOURCE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")   # no ':', '#', '/', whitespace (they delimit keys)
RESERVED_META = ("text_sha256",)                                 # added by s02_normalise
SOFT_TOL = 1e-6


def _is_unit(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and 0.0 <= float(x) <= 1.0


def validate_record(rec: Any, *, sources: Mapping[str, Sequence[str]] | None = None) -> list[str]:
    """Return a list of contract violations (empty list = valid).

    * source: registered loader name ([a-z][a-z0-9_]*); split: the loader's split name (native or regrouped).
    * source_id: string, stable across runs, unique within (source, split); [A-Za-z0-9][A-Za-z0-9_.-]*.
    * text: non-empty string (the base text that becomes the state body; wrappers are applied at render).
    * label: the source's own gold: str (class name / id), int (ordinal rating / level), a sorted list of unique str
      (multi-label), or None (no gold: filler, injection pools, unlabeled rows).
    * soft: None; a float in [0, 1]; a list of floats in [0, 1] summing to 1 (distribution over ordered levels);
      or a dict {label: float in [0, 1]} (per-label vote fractions; if meta.soft_kind == "distribution" it must sum
      to 1).
    * meta: dict with str keys, JSON-serialisable without NaN/inf.
    """
    errs: list[str] = []
    if not isinstance(rec, Mapping):
        return ["record is not an object"]
    keys = set(rec.keys())
    missing = [f for f in RECORD_FIELDS if f not in keys]
    extra = sorted(keys - set(RECORD_FIELDS))
    if missing:
        errs.append(f"missing fields {missing}")
    if extra:
        errs.append(f"unexpected fields {extra} (put them in meta)")
    if missing:
        return errs
    src, split, sid = rec["source"], rec["split"], rec["source_id"]
    if not isinstance(src, str) or not _SOURCE_RE.match(src):
        errs.append(f"bad source {src!r}")
    if not isinstance(split, str) or not _SPLIT_RE.match(split):
        errs.append(f"bad split {split!r}")
    if sources is not None and isinstance(src, str):
        if src not in sources:
            errs.append(f"source {src!r} is not registered")
        elif isinstance(split, str) and split not in sources[src]:
            errs.append(f"split {split!r} not declared for {src!r} {list(sources[src])}")
    if not isinstance(sid, str) or not _SOURCE_ID_RE.match(sid):
        errs.append(f"bad source_id {sid!r} (string of [A-Za-z0-9_.-], no ':', '#', '/')")
    text = rec["text"]
    if not isinstance(text, str) or not text.strip():
        errs.append("text must be a non-empty string")
    elif "\x00" in text:
        errs.append("text contains NUL")
    label = rec["label"]
    if label is not None:
        if isinstance(label, bool):
            errs.append("label must not be a bool")
        elif isinstance(label, list):
            if not all(isinstance(x, str) and x for x in label):
                errs.append("multi-label must be a list of non-empty strings")
            elif label != sorted(set(label)):
                errs.append("multi-label list must be sorted and unique")
        elif isinstance(label, str):
            if not label:
                errs.append("label is an empty string")
        elif not isinstance(label, int):
            errs.append(f"label has type {type(label).__name__} (str | int | list[str] | None)")
    soft = rec["soft"]
    meta = rec["meta"]
    if soft is not None:
        if isinstance(soft, bool):
            errs.append("soft must not be a bool")
        elif isinstance(soft, (int, float)):
            if not _is_unit(soft):
                errs.append(f"soft {soft!r} not in [0, 1]")
        elif isinstance(soft, list):
            if not soft or not all(_is_unit(x) for x in soft):
                errs.append("soft list values must be in [0, 1]")
            elif abs(sum(float(x) for x in soft) - 1.0) > SOFT_TOL:
                errs.append(f"soft distribution sums to {sum(soft)!r}, not 1")
        elif isinstance(soft, Mapping):
            if not soft or not all(isinstance(k, str) and _is_unit(v) for k, v in soft.items()):
                errs.append("soft dict must map str -> [0, 1]")
            elif isinstance(meta, Mapping) and meta.get("soft_kind") == "distribution" \
                    and abs(sum(float(v) for v in soft.values()) - 1.0) > SOFT_TOL:
                errs.append("soft distribution (dict) does not sum to 1")
        else:
            errs.append(f"soft has type {type(soft).__name__}")
    if not isinstance(meta, Mapping):
        errs.append("meta must be an object")
    else:
        if not all(isinstance(k, str) for k in meta):
            errs.append("meta keys must be strings")
        try:
            json.dumps(meta, allow_nan=False)
        except (TypeError, ValueError) as exc:
            errs.append(f"meta not JSON-serialisable: {exc}")
    return errs


def check_record(rec: Any, **kw: Any) -> None:
    errs = validate_record(rec, **kw)
    if errs:
        sid = rec.get("source_id") if isinstance(rec, Mapping) else None
        src = rec.get("source") if isinstance(rec, Mapping) else None
        raise ValueError(f"invalid normalised record {src}:{sid}: " + "; ".join(errs))


def make_record(source: str, split: str, source_id: Any, text: str, label: Any = None,
                soft: Any = None, meta: Mapping | None = None) -> dict:
    """Convenience constructor (stringifies source_id)."""
    return {"source": source, "split": split, "source_id": str(source_id), "text": text,
            "label": label, "soft": soft, "meta": dict(meta or {})}


def normalised_path(source: str, split: str) -> Path:
    return NORMALISED / f"{source}__{split}.jsonl"


def read_normalised(source: str, split: str) -> Iterator[dict]:
    return read_jsonl(normalised_path(source, split))


def record_sort_key(rec: Mapping) -> tuple:
    return (rec["source"], rec["split"], natural_key(rec["source_id"]))


# ------------------------------------------------------------------------------------------------------------------
# Source hygiene (DESIGN 8.1, 13 step 2) — called by loaders
# ------------------------------------------------------------------------------------------------------------------
EMAIL_RE = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])")
_PHONE_PATTERNS = (
    re.compile(r"(?<![\w+])\+\d{1,3}[\s.-]?(?:\(\d{1,4}\)[\s.-]?)?\d{2,4}(?:[\s.-]?\d{2,4}){2,4}(?!\w)"),   # +44 20 7946 0958
    re.compile(r"(?<![\w(])\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\w)"),                                     # (555) 010-4477
)
MASK_EMAIL = "<EMAIL>"
MASK_PHONE = "<PHONE>"


def mask_pii(text: str, *, digit_run_min: int | None = None) -> tuple[str, int]:
    """Mask e-mail addresses and phone numbers; optionally every run of >= digit_run_min digits (HINT3: 7).

    Returns (masked_text, n_masks). Runs of >= verification.pii.general_digit_run_min (10) digits are always
    masked as phone numbers. Deterministic and idempotent.
    """
    n = 0

    def _sub(pattern: re.Pattern, repl: str, s: str) -> str:
        nonlocal n
        out, k = pattern.subn(repl, s)
        n += k
        return out

    text = _sub(EMAIL_RE, MASK_EMAIL, text)
    for pat in _PHONE_PATTERNS:
        text = _sub(pat, MASK_PHONE, text)
    general = int(cfg("verification", "pii", "general_digit_run_min", default=10))
    run_min = general if digit_run_min is None else min(int(digit_run_min), general)
    text = _sub(re.compile(r"(?<!\d)\d{%d,}(?!\d)" % run_min), MASK_PHONE, text)
    return text, n


def unescape_html(text: str, max_rounds: int = 3) -> str:
    """html.unescape until stable (drug reviews carry double-escaped entities such as &amp;#039;)."""
    for _ in range(max_rounds):
        new = html.unescape(text)
        if new == text:
            break
        text = new
    return text


def clean_text(text: str, *, html_entities: bool = False, digit_run_min: int | None = None) -> tuple[str, int]:
    """Standard loader hygiene: optional HTML unescape, CRLF -> LF, strip, PII masking. Returns (text, n_pii)."""
    if html_entities:
        text = unescape_html(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    return mask_pii(text, digit_run_min=digit_run_min)


def pii_residual(text: str) -> int:
    """Count e-mail / phone patterns still present (s02 reports it; should be 0)."""
    return len(EMAIL_RE.findall(text)) + sum(len(p.findall(text)) for p in _PHONE_PATTERNS)


# ------------------------------------------------------------------------------------------------------------------
# GitHub files at a pinned commit (DESIGN 3: requests at the pinned commit; stored in the HF cache)
# ------------------------------------------------------------------------------------------------------------------
def github_cache_path(repo: str, sha: str, path: str) -> Path:
    return GITHUB_CACHE / repo.replace("/", "__") / sha / path


def github_file(repo: str, sha: str, path: str, *, expect_sha256: str | None = None, timeout: int = 60) -> Path:
    """Download raw.githubusercontent.com/{repo}/{sha}/{path} once into the HF cache and return the local path.

    If expect_sha256 is None, the sha256 recorded in build/sources.lock.json (if any) is checked.
    """
    if not FULL_SHA.match(sha):
        raise ValueError(f"github_file needs a full commit sha, got {sha!r}")
    local = github_cache_path(repo, sha, path)
    if expect_sha256 is None:
        for entry in load_lock().get("sources", {}).values():
            if entry.get("kind") == "github" and entry.get("repo") == repo and entry.get("resolved_sha") == sha:
                for f in entry.get("files", []):
                    if f.get("path") == path and f.get("sha256"):
                        expect_sha256 = f["sha256"]
    if not local.exists():
        import requests
        url = f"https://raw.githubusercontent.com/{repo}/{sha}/{path}"
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        _atomic_write_bytes(local, resp.content)
    if expect_sha256 is not None:
        got = file_sha256(local)
        if got != expect_sha256:
            raise RuntimeError(f"sha256 mismatch for {repo}@{sha}:{path}: {got} != {expect_sha256}")
    return local


# ------------------------------------------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------------------------------------------
def get_logger(name: str, *, log_file: Path | str | None = None, level: int = logging.INFO) -> logging.Logger:
    """Logger that writes to stderr and to data/interim/logs/<name>.log (appending)."""
    logger = logging.getLogger(f"opendecide.{name}")
    if logger.handlers:
        return logger
    logger.setLevel(level)
    logger.propagate = False
    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(Path(log_file) if log_file else LOG_DIR / f"{name}.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger


# ------------------------------------------------------------------------------------------------------------------
# Checkpoints (data/interim/checkpoints/<step>.json). Content is deterministic (no timestamps); timings go to logs.
# ------------------------------------------------------------------------------------------------------------------
def checkpoint_path(step: str) -> Path:
    return CHECKPOINTS / f"{step}.json"


def step_code_sha256(step_file: Path | str) -> str:
    return file_sha256(step_file)


def _hash_paths(paths: Iterable[Path | str]) -> dict:
    out = {}
    for p in paths:
        p = Path(p)
        if not p.is_absolute():
            p = ROOT / p
        out[rel(p)] = file_sha256(p) if p.is_file() else None
    return dict(sorted(out.items()))


def write_checkpoint(step: str, *, step_file: Path | str, seed: int, outputs: Iterable[Path | str] = (),
                     inputs: Iterable[Path | str] = (), info: Mapping | None = None, args: Mapping | None = None,
                     partial: bool = False) -> dict:
    """Record a finished step. `inputs` are extra files the result depends on (common.py is always included);
    a `partial` run (e.g. s02 --sources banking77) is never treated as current by `build.py --stage all`."""
    ck = {"step": step, "seed": int(seed), "step_sha256": step_code_sha256(step_file),
          "config_sha256": config_sha256(), "inputs": _hash_paths([Path(__file__), *inputs]),
          "outputs": _hash_paths(outputs), "args": dict(args or {}), "info": dict(info or {}),
          "status": "partial" if partial else "done"}
    write_json(checkpoint_path(step), ck)
    return ck


def read_checkpoint(step: str) -> dict | None:
    p = checkpoint_path(step)
    if not p.exists():
        return None
    try:
        return read_json(p)
    except (OSError, json.JSONDecodeError):
        return None


def checkpoint_is_current(step: str, *, step_file: Path | str, seed: int, args: Mapping | None = None) -> tuple[bool, str]:
    """(True, "") if the step's checkpoint matches this code, config, seed and args and its outputs are unchanged."""
    ck = read_checkpoint(step)
    if not ck:
        return False, "no checkpoint"
    if ck.get("status") != "done":
        return False, f"checkpoint status {ck.get('status')!r}"
    if ck.get("seed") != int(seed):
        return False, "seed changed"
    if ck.get("step_sha256") != step_code_sha256(step_file):
        return False, "step code changed"
    if ck.get("config_sha256") != config_sha256():
        return False, "config changed"
    if args is not None and ck.get("args") != dict(args):
        return False, "args changed"
    for p, sha in (ck.get("inputs") or {}).items():
        fp = ROOT / p
        if (file_sha256(fp) if fp.is_file() else None) != sha:
            return False, f"input changed: {p}"
    for p, sha in (ck.get("outputs") or {}).items():
        fp = ROOT / p
        if sha is None:
            if not fp.exists():
                return False, f"output missing: {p}"
        elif not fp.is_file() or file_sha256(fp) != sha:
            return False, f"output changed: {p}"
    return True, ""


# ------------------------------------------------------------------------------------------------------------------
# Step CLI (every build/steps/sNN_*.py uses this)
# ------------------------------------------------------------------------------------------------------------------
def step_argparser(description: str) -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--seed", type=int, default=None, help="master seed (default: config master_seed)")
    ap.add_argument("--lofo", choices=["A", "B", "E", "G"], default=None, help="leave-one-family-out train variant")
    ap.add_argument("--rehydrate", action="store_true", help="restore idonly text where the step needs it")
    return ap


def step_main(step: str, step_file: str | Path, run: Callable[[argparse.Namespace, logging.Logger], Mapping | None],
              *, description: str = "", parser: argparse.ArgumentParser | None = None,
              argv: Sequence[str] | None = None) -> int:
    """Parse args, set the seed, run the step, write its checkpoint. `run` returns {"outputs": [...], "info": {...}}.

    `run` may also return "inputs" (files the result depends on, re-hashed by the driver) and "partial": True
    (a restricted run that `--stage all` must redo). Exit code: 0 on success, 1 when run() raises or returns
    {"ok": False}.
    """
    ap = parser or step_argparser(description or step)
    args = ap.parse_args(argv)
    if args.seed is not None:
        os.environ[SEED_ENV] = str(args.seed)
    seed = master_seed()
    ensure_dirs()
    log = get_logger(step)
    if seed != int(cfg("master_seed")):
        log.warning("seed %d differs from the master seed %d: outputs are not the canonical build", seed, cfg("master_seed"))
    log.info("start %s (seed %d)", step, seed)
    try:
        result = dict(run(args, log) or {})
    except Exception:
        log.exception("step %s failed", step)
        return 1
    if result.get("ok", True) is False:
        log.error("step %s reported failure: %s", step, result.get("error", ""))
        return 1
    ck_args = {k: v for k, v in sorted(vars(args).items()) if k != "seed"}
    write_checkpoint(step, step_file=step_file, seed=seed, outputs=result.get("outputs", []),
                     inputs=result.get("inputs", []), info=result.get("info", {}), args=ck_args,
                     partial=bool(result.get("partial", False)))
    log.info("done %s", step)
    return 0


def append_build_decision(role: str, text: str, date: str = "2026-09-25") -> None:
    """Append one dated bullet to design/build_decisions.md (never overwrites)."""
    with open(BUILD_DECISIONS, "a", encoding="utf-8") as fh:
        fh.write(f"- {date} ({role}) {text}\n")
