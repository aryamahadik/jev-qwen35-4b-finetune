"""T53 FAKE-CREDENTIAL REGISTRY (G0-lite T53 section 3; Round 2: OFFLINE ONLY, FIX-3 / K21).

Every credential-like or personal-data-like token in a T53 row is a registered fake: record
{shape id, generation seed, checksum status, frequency counters}. Checksummed formats (the 6-character CRC32 base62
tail of a GitHub-style token) are generated with a deliberately WRONG checksum in 100% of rows, ALLOW and BLOCK
alike, so the checksum carries no label signal. Documented example keys (list kept by L-0, not reproduced here;
UNVERIFIED) are capped at <= 1% of credential-like values and spread equally over labels.

OFFLINE ONLY: this module, destination.py and the verifiers import no network-capable module and call no
subprocess; no row value, or part of one, is ever sent to any service or API (pure local functions; CPU test K21).
gitleaks (MIT) is only a catalogue of SHAPES; TruffleHog (AGPL) is barred and not used.
"""
import base64
import hashlib
import json
import re
import zlib

from LA_COMMON.canon import rng_for, sha_text

B62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

CRED_SHAPES = ("cloud_key_id", "ckt_token", "signed3", "pem_block", "hex_key", "db_url", "bearer", "passphrase")
PII_SHAPES = ("pii_email", "pii_phone", "pii_name", "pii_id")
BENIGN_SHAPES = ("digest64", "uuid", "rand_id", "long_blob")           # key-shaped but benign (block f)
SHAPES = CRED_SHAPES + PII_SHAPES + BENIGN_SHAPES
CHECKSUMMED = ("ckt_token",)


def b62(n, width):
    s = ""
    while n:
        n, r = divmod(n, 62)
        s = B62[r] + s
    return s.rjust(width, "0")[-width:]


def crc_tail(body):
    """GitHub-style tail: base62 of CRC32(body), 6 chars (the format named in the excerpt)."""
    return b62(zlib.crc32(body.encode("ascii")) & 0xFFFFFFFF, 6)


# ------------------------------------------------------------------------------------------------ OFFLINE verifiers
def verify_ckt(value):
    m = re.fullmatch(r"([a-z]{2,4})_([A-Za-z0-9]{30})([A-Za-z0-9]{6})", value)
    return bool(m) and crc_tail(m.group(2)) == m.group(3)


def verify_pem(value):
    m = re.fullmatch(r"-----BEGIN ([A-Z ]+)-----\n([A-Za-z0-9+/=\n]+)\n-----END \1-----", value)
    if not m:
        return False
    try:
        der = base64.b64decode(m.group(2).replace("\n", ""), validate=True)
    except Exception:
        return False
    if len(der) < 4 or der[0] != 0x30:
        return False
    if der[1] < 0x80:
        return der[1] == len(der) - 2
    n = der[1] & 0x7F
    return len(der) >= 2 + n and int.from_bytes(der[2:2 + n], "big") == len(der) - 2 - n


def verify_jwt(value):
    parts = value.split(".")
    if len(parts) != 3:
        return False
    try:
        pad = lambda s: s + "=" * (-len(s) % 4)
        hdr = json.loads(base64.urlsafe_b64decode(pad(parts[0])))
        json.loads(base64.urlsafe_b64decode(pad(parts[1])))
        return isinstance(hdr, dict) and "alg" in hdr
    except Exception:
        return False


REAL_PREFIX = re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA|ANPA|ANVA|AIPA)[A-Z2-7]{16}\b|\bgh[pousr]_[A-Za-z0-9]{36}\b|"
                         r"\bsk_live_[0-9a-zA-Z]{24}\b|\bxox[baprs]-[0-9A-Za-z-]{10,}\b|\bAIza[0-9A-Za-z_-]{35}\b")


def is_live_looking(value):
    """Any OFFLINE checksum or format verifier passes -> the value could be a live credential. Must be False."""
    return bool(verify_ckt(value) or verify_pem(value) or verify_jwt(value) or REAL_PREFIX.search(value))


# ------------------------------------------------------------------------------------------------ generation
def _pick(rng, alphabet, n):
    return "".join(rng.choice(alphabet) for _ in range(n))


class FakeFactory:
    """Generates fake values for one spec family. `syllables` supplies namespace-derived words (stems), `host`/`user`
    namespace names for the db_url / email shapes. Everything else is random characters, not names."""

    def __init__(self, seed, names):
        self.rng = rng_for("t53-fake", seed)
        self.names = names

    def make(self, shape, key="k"):
        rng = self.rng
        if shape == "cloud_key_id":
            pfx = self.names.get("ns.path_stem", key + ".pfx")[:4].upper().ljust(4, "Z")
            if pfx in ("AKIA", "ASIA", "AGPA", "AIDA", "AROA", "ANPA", "ANVA", "AIPA"):
                pfx = "ZZZZ"
            return pfx + _pick(rng, B32, 16), {"checksum": "n/a"}
        if shape == "ckt_token":
            pfx = self.names.get("ns.path_stem", key + ".ckt")[:3].lower().ljust(3, "z")
            if pfx.startswith("gh"):
                pfx = "zk" + pfx[2:]
            body = _pick(rng, B62, 30)
            good = crc_tail(body)
            tail = good
            while tail == good:
                tail = _pick(rng, B62, 6)
            return "%s_%s%s" % (pfx, body, tail), {"checksum": "wrong"}
        if shape == "signed3":
            parts = [base64.urlsafe_b64encode(bytes(rng.randrange(256) for _ in range(n))).decode().rstrip("=") for n in (18, 33, 32)]
            if parts[0].startswith("ey"):
                parts[0] = "zz" + parts[0][2:]
            return ".".join(parts), {"checksum": "n/a"}
        if shape == "pem_block":
            body = bytes(rng.randrange(256) for _ in range(96))
            if body[0] == 0x30:
                body = bytes([0x31]) + body[1:]
            b = base64.b64encode(body).decode()
            lines = "\n".join(b[i:i + 64] for i in range(0, len(b), 64))
            return "-----BEGIN PRIVATE KEY-----\n%s\n-----END PRIVATE KEY-----" % lines, {"checksum": "n/a"}
        if shape == "hex_key":
            return _pick(rng, "0123456789abcdef", rng.choice((32, 40))), {"checksum": "n/a"}
        if shape == "db_url":
            scheme = rng.choice(("postgresql", "mysql"))
            return "%s://%s:%s@%s:%d/%s" % (scheme, self.names.get("ns.handle", key + ".u"), _pick(rng, B62, 14),
                                           self.names.get("ns.host", key + ".dbh"), rng.choice((5432, 3306, 6543)),
                                           self.names.get("ns.database", key + ".db")), {"checksum": "n/a"}
        if shape == "bearer":
            return _pick(rng, B62, 40), {"checksum": "n/a"}
        if shape == "passphrase":
            return "-".join(self.names.get("ns.noun.symbol", "%s.w%d" % (key, i)) for i in range(4)), {"checksum": "n/a"}
        if shape == "digest64":
            return _pick(rng, "0123456789abcdef", 64), {"checksum": "n/a"}
        if shape == "uuid":
            h = _pick(rng, "0123456789abcdef", 32)
            return "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:]), {"checksum": "n/a"}
        if shape == "rand_id":
            return _pick(rng, B62, 24), {"checksum": "n/a"}
        if shape == "long_blob":
            return base64.b64encode(bytes(rng.randrange(256) for _ in range(60))).decode(), {"checksum": "n/a"}
        if shape == "pii_email":
            return "%s@%s" % (self.names.get("ns.handle", key + ".em"), self.names.get("ns.host", key + ".emh")), {"checksum": "n/a"}
        if shape == "pii_phone":
            return "+1-555-01%02d" % rng.randrange(100), {"checksum": "n/a"}
        if shape == "pii_name":
            return "%s %s" % (self.names.get("ns.handle", key + ".fn").capitalize(), self.names.get("ns.handle", key + ".ln").capitalize()), {"checksum": "n/a"}
        if shape == "pii_id":
            return "000-%02d-%04d" % (rng.randrange(1, 99), rng.randrange(1, 9999)), {"checksum": "n/a"}
        raise ValueError(shape)


class Registry:
    """Registered-fake registry. Stores sha256 of values (never the value itself) plus counters."""

    def __init__(self):
        self.recs = {}
        self.parts = set()                     # hashes of the long alphanumeric runs inside registered values (multi-part shapes)
        self.by_shape = {}

    def register(self, value, shape, seed, checksum="n/a", example=False, label=None):
        h = sha_text(value)
        if h not in self.recs:                 # a quad shares its values: count each distinct value once
            self.by_shape[shape] = self.by_shape.get(shape, 0) + 1
        self.recs[h] = {"shape": shape, "seed": str(seed), "checksum": checksum, "example": bool(example), "label": label}
        for run in re.findall(r"[A-Za-z0-9]{16,}", value):
            self.parts.add(sha_text(run))
        return h

    def contains(self, value):
        h = sha_text(value)
        return h in self.recs or h in self.parts

    def stats(self):
        n = len(self.recs)
        return {"values": n, "by_shape": dict(self.by_shape), "examples": sum(r["example"] for r in self.recs.values()),
                "checksum_wrong": sum(r["checksum"] == "wrong" for r in self.recs.values())}


class ExampleKeys:
    """Documented example keys (vendor docs; list kept by L-0, NOT reproduced here, UNVERIFIED). Empty until L-0 supplies it."""

    def __init__(self, values=()):
        self.values = set(values)

    @staticmethod
    def load(path=None):
        if not path:
            return ExampleKeys()
        with open(path, "r", encoding="utf-8") as f:
            return ExampleKeys(json.load(f))

    def is_example(self, v):
        return v in self.values


# ------------------------------------------------------------------------------------------------ scanner (K1)
_TOKEN_PATTERNS = [
    ("ckt_token", re.compile(r"\b[a-z]{2,4}_[A-Za-z0-9]{36}\b")),
    ("cloud_key_id", re.compile(r"\b[A-Z]{4}[A-Z2-7]{16}\b")),
    ("pem_block", re.compile(r"-----BEGIN [A-Z ]+-----\n[A-Za-z0-9+/=\n]+\n-----END [A-Z ]+-----")),
    ("signed3", re.compile(r"\b[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{30,}\b")),
    ("db_url", re.compile(r"\b(?:postgresql|mysql)://[^\s:/@]+:[^\s@]+@[^\s/]+/[^\s'\"]+")),
    ("hex_key", re.compile(r"\b[0-9a-f]{32}\b|\b[0-9a-f]{40}\b")),
    ("pii_email", re.compile(r"(?<![\w.-])[A-Za-z0-9._]+@[A-Za-z0-9.-]+\.[a-z]+\b")),
    ("pii_phone", re.compile(r"\+1-555-01\d\d")),
    ("pii_id", re.compile(r"\b000-\d\d-\d{4}\b")),
    ("bearer", re.compile(r"\b[A-Za-z0-9]{36,64}\b")),
    ("passphrase", re.compile(r"\b[a-z]{3,}(?:-[a-z]{3,}){3}\b")),
]


def find_tokens(text):
    """Credential-like / PII-like tokens in a rendered row (Guard-10-style scrub, own patterns). -> [(shape, value)].
    A match lying inside a longer match (an email-shaped span inside a database URL) is dropped."""
    spans = []
    for shape, rx in _TOKEN_PATTERNS:
        for m in rx.finditer(text):
            spans.append((m.start(), m.end(), shape, m.group(0)))
    spans += [(m.start(), m.end(), "real_prefix", m.group(0)) for m in REAL_PREFIX.finditer(text)]
    keep = []
    for a, b, shape, v in spans:
        if any((a2 <= a and b <= b2 and (a2, b2) != (a, b)) for a2, b2, _, _ in spans):
            continue
        keep.append((shape, v))
    return keep
