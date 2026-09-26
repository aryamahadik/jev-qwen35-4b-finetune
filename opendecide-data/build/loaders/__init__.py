"""OpenDecide source-loader registry (DESIGN 13 step 2). See build/loaders/README.md for the contract.

Add a source by dropping a new module into build/loaders/ that decorates a generator with ``@register``:

    from loaders import register, LoaderContext
    import common

    @register("banking77", splits=("train", "test"), lock_key="banking77")
    def load(split: str, ctx: LoaderContext):
        ds = ctx.load_hf(split=split)
        ...
        yield common.make_record("banking77", split, i, text, label=..., meta={...})

Every module in this package is imported automatically (sorted by name) the first time the package is imported, so
no shared file has to be edited. A module that fails to import is recorded in IMPORT_ERRORS (and reported by
s02_normalise) instead of breaking every other loader.

authored_by: llm:claude:foundation-engineer-1
"""
from __future__ import annotations

import collections
import importlib
import logging
import pkgutil
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping

_BUILD_DIR = Path(__file__).resolve().parent.parent
if str(_BUILD_DIR) not in sys.path:
    sys.path.insert(0, str(_BUILD_DIR))

import common  # noqa: E402

LoaderFn = Callable[[str, "LoaderContext"], Iterable[dict]]


@dataclass(frozen=True)
class LoaderSpec:
    source: str                    # registered source name (normalised files: <source>__<split>.jsonl)
    splits: tuple[str, ...]        # split names this loader emits (native or regrouped)
    fn: LoaderFn
    module: str
    lock_key: str                  # key into config.yaml `sources` / build/sources.lock.json
    info: Mapping[str, Any] = field(default_factory=dict)


REGISTRY: dict[str, LoaderSpec] = {}
IMPORT_ERRORS: dict[str, str] = {}
_DISCOVERED = False


def register(source: str, splits: Iterable[str], *, lock_key: str | None = None, **info: Any):
    """Decorator: register `fn(split, ctx) -> Iterable[record]` as the loader for `source`.

    source    lower-case name used in file names and records (e.g. "banking77", "hint3_curekart").
    splits    the splits the loader can emit; s02 calls fn once per split.
    lock_key  config.yaml `sources` entry holding the pin (defaults to `source`).
    info      free-form metadata recorded in the normalise summary (e.g. wrapper="banking77", note="...").
    """
    splits_t = tuple(splits)
    if not splits_t:
        raise ValueError(f"loader {source!r} declares no splits")

    def deco(fn: LoaderFn) -> LoaderFn:
        if source in REGISTRY and REGISTRY[source].fn is not fn:
            raise ValueError(f"source {source!r} registered twice ({REGISTRY[source].module} and {fn.__module__})")
        REGISTRY[source] = LoaderSpec(source=source, splits=splits_t, fn=fn, module=fn.__module__,
                                      lock_key=lock_key or source, info=dict(info))
        return fn

    return deco


def discover(*, force: bool = False) -> dict[str, LoaderSpec]:
    """Import every module in build/loaders/ (sorted, skipping names that start with "_")."""
    global _DISCOVERED
    if _DISCOVERED and not force:
        return REGISTRY
    _DISCOVERED = True
    for mod in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if mod.name.startswith("_"):
            continue
        name = f"{__name__}.{mod.name}"
        try:
            if name in sys.modules and force:
                importlib.reload(sys.modules[name])
            else:
                importlib.import_module(name)
        except Exception:  # keep other loaders usable; s02 reports this
            IMPORT_ERRORS[mod.name] = traceback.format_exc(limit=5)
    return REGISTRY


def get(source: str) -> LoaderSpec:
    discover()
    if source not in REGISTRY:
        raise KeyError(f"no loader registered for {source!r} (have: {sorted(REGISTRY)})")
    return REGISTRY[source]


def sources() -> dict[str, tuple[str, ...]]:
    """{source: splits} for every registered loader."""
    discover()
    return {s: spec.splits for s, spec in sorted(REGISTRY.items())}


class LoaderContext:
    """What a loader gets besides the split name: pins, config, logging, hygiene helpers and drop accounting."""

    def __init__(self, spec: LoaderSpec, split: str, *, log: logging.Logger | None = None):
        self.spec = spec
        self.source = spec.source
        self.split = split
        self.lock_key = spec.lock_key
        self.log = log or common.get_logger(f"loader.{spec.source}")
        self.drops: collections.Counter[str] = collections.Counter()
        self.notes: dict[str, Any] = {}

    # --- pins -------------------------------------------------------------------------------------------------------
    @property
    def pin(self) -> dict:
        """The config.yaml `sources` entry for this loader's lock_key."""
        return dict(common.cfg("sources", self.lock_key))

    @property
    def lock(self) -> dict:
        """The build/sources.lock.json entry (empty before s01_lock has run)."""
        return dict(common.load_lock().get("sources", {}).get(self.lock_key, {}))

    @property
    def revision(self) -> str:
        """Full commit sha to load (from the lock; a full sha in config also works)."""
        return common.pinned_revision(self.lock_key)

    # --- loading helpers ---------------------------------------------------------------------------------------------
    def load_hf(self, *, split: str | None = None, config: str | None = None, streaming: bool | None = None,
                **kwargs: Any):
        """datasets.load_dataset(repo, config, revision=<pinned sha>, data_dir/data_files from config, ...)."""
        from datasets import load_dataset
        pin = self.pin
        if pin.get("kind") != "hf_dataset":
            raise ValueError(f"{self.lock_key} is not an hf_dataset source")
        args: dict[str, Any] = {"revision": self.revision}
        if pin.get("data_dir"):
            args["data_dir"] = pin["data_dir"]
        if pin.get("data_files"):
            args["data_files"] = pin["data_files"]
        stream = pin.get("streaming", False) if streaming is None else streaming
        if stream:
            args["streaming"] = True
        if split is not None:
            args["split"] = split
        args.update(kwargs)
        name = config if config is not None else pin.get("config")
        self.log.info("load_dataset(%r, %r, %s)", pin["repo"], name, {k: v for k, v in args.items()})
        return load_dataset(pin["repo"], name, **args) if name else load_dataset(pin["repo"], **args)

    def github_file(self, path: str) -> Path:
        """Local copy of `path` from this loader's pinned GitHub repo (downloaded once into the HF cache)."""
        pin = self.pin
        if pin.get("kind") != "github":
            raise ValueError(f"{self.lock_key} is not a github source")
        return common.github_file(pin["repo"], self.revision, path)

    # --- hygiene and accounting --------------------------------------------------------------------------------------
    def clean(self, text: str, *, html_entities: bool = False, digit_run_min: int | None = None) -> tuple[str, int]:
        """common.clean_text: optional HTML unescape, CRLF -> LF, strip, PII masking. Returns (text, n_pii)."""
        return common.clean_text(text, html_entities=html_entities, digit_run_min=digit_run_min)

    def drop(self, reason: str, n: int = 1) -> None:
        """Count a dropped source row (reported per reason in the normalise summary)."""
        self.drops[reason] += n

    def note(self, key: str, value: Any) -> None:
        """Record a loader-level fact (e.g. a regrouping count) in the normalise summary."""
        self.notes[key] = value


def iter_records(source: str, split: str, *, log: logging.Logger | None = None) -> tuple[LoaderContext, Iterator[dict]]:
    spec = get(source)
    if split not in spec.splits:
        raise ValueError(f"{source!r} has no split {split!r} (declared: {spec.splits})")
    ctx = LoaderContext(spec, split, log=log)
    return ctx, iter(spec.fn(split, ctx))


discover()
