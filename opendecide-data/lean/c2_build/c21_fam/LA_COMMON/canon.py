"""Canonical JSON, hashing, deterministic RNG and frozen tables (no I/O except sha_file)."""
import hashlib
import json
import random


def canon(obj):
    """Canonical JSON text: sorted keys, no spaces, ASCII only."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_obj(obj):
    return sha_text(canon(obj))


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rng_for(*parts):
    """Deterministic random.Random from any JSON-able parts. Used for STRUCTURE decisions only;
    every NAME comes from namespace.py (see names.py)."""
    seed = int(sha_text(canon(list(parts)))[:16], 16)
    return random.Random(seed)


def stable_fraction(*parts):
    """Deterministic number in [0, 1) from parts (for split assignment and hashing buckets)."""
    return int(sha_text(canon(list(parts)))[:12], 16) / float(16 ** 12)


class FrozenTable:
    """A named, versioned, hashed table (rule table, resolver list, payload registry).

    The sha is over the canonical JSON of the entries. A table that is exported for a pilot records its sha;
    any later edit changes the sha (a gate edit, needs Opus)."""

    def __init__(self, name, version, entries):
        self.name = name
        self.version = version
        self.entries = entries
        self.sha = sha_obj({"name": name, "version": version, "entries": entries})

    def to_dict(self):
        return {"name": self.name, "version": self.version, "sha256": self.sha, "entries": self.entries}

    def assert_sha(self, expected):
        if self.sha != expected:
            raise ValueError("frozen table %s sha %s != expected %s" % (self.name, self.sha[:12], expected[:12]))


def assign_split(spec_family_id, dev_fraction=0.10):
    """dev = 10% of spec FAMILIES; every rendering/contrast row of a spec family lands in one split (K13)."""
    return "dev" if stable_fraction("split", spec_family_id) < dev_fraction else "train"
