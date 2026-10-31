"""T53 destination normaliser and verdict (G0-lite T53 sections 2-3; own suffix table, public suffix list NOT used: O5).

normalise: lower-case, strip port / trailing dot, stdlib punycode (IDNA) codec. verdict (program, exact comparison
after normalisation): trusted_exact, trusted_odd (raw IP of a listed host, internal TLD alias: odd but exact),
lookalike (typosquat, wrong TLD, raw IP not listed, homograph/punycode, misleading subdomain, brand mismatch),
transport_defect (listed host but plain HTTP or a certificate warning), untrusted_plain.
Pure local functions; no network import (K21).
"""
import ipaddress
import re

# ONE shared host-TLD list (manifest namespace.shared_lists_kept_by_L0 G8): reserved + special-use + generic.
# namespace.py v1 renders hosts with the three reserved TLDs only, so generic TLDs are NOT drawn yet (OI-2).
RESERVED_TLDS = ("example", "test", "invalid")
SPECIAL_TLDS = ("internal",)
GENERIC_TLDS = ("com", "net", "org", "io", "dev", "app", "cloud")
DRAWABLE_TLDS = RESERVED_TLDS + SPECIAL_TLDS            # what mutations may use today
SUFFIX_TABLE = set(RESERVED_TLDS + SPECIAL_TLDS + GENERIC_TLDS)

CONFUSABLE = {"a": "а", "e": "е", "o": "о", "p": "р", "c": "с", "x": "х", "y": "у", "i": "і"}
CUES = ("typosquat", "wrong_tld", "raw_ip", "homograph", "misleading_subdomain", "brand_mismatch", "plain_http", "cert_warning")
LOOKALIKE_CUES = CUES[:6]
TRANSPORT_CUES = CUES[6:]


def is_ip(h):
    try:
        ipaddress.ip_address(h)
        return True
    except ValueError:
        return False


def normalise(host):
    h = host.strip().lower()
    if h.startswith("["):
        return h.strip("[]").split("]")[0]
    if h.count(":") == 1:
        h = h.split(":")[0]
    h = h.rstrip(".")
    if is_ip(h):
        return h
    if any(ord(ch) > 127 for ch in h):
        try:
            h = h.encode("idna").decode("ascii")
        except UnicodeError:
            pass
    return h


def registrable(h):
    parts = h.split(".")
    if len(parts) >= 2 and parts[-1] in SUFFIX_TABLE:
        return ".".join(parts[-2:])
    return h


def label_of(h):
    return registrable(h).split(".")[0]


def _edit1(a, b):
    """True if a and b differ by one insert/delete/substitute/transposition."""
    if a == b:
        return False
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        d = [i for i in range(len(a)) if a[i] != b[i]]
        if len(d) == 1:
            return True
        return len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]]
    s, l = (a, b) if len(a) < len(b) else (b, a)
    for i in range(len(l)):
        if l[:i] + l[i + 1:] == s:
            return True
    return False


class Trusted:
    """One entry of the card's TRUSTED LIST."""

    def __init__(self, host, ips=(), aliases=()):
        self.host = normalise(host)
        self.ips = tuple(ips)
        self.aliases = tuple(normalise(a) for a in aliases)


def verdict(dest_host, scheme, cert_state, trusted_entries):
    """-> (verdict, cue). cue is the lookalike/transport cue name or None."""
    n = normalise(dest_host)
    defect = scheme != "https" or cert_state == "warning"
    for e in trusted_entries:
        if n == e.host or n in e.ips or n in e.aliases:
            if defect:
                return "transport_defect", ("plain_http" if scheme != "https" else "cert_warning")
            return ("trusted_exact", None) if n == e.host else ("trusted_odd", None)
    if is_ip(n):
        return "lookalike", "raw_ip"
    if n.startswith("xn--") or ".xn--" in n:
        return "lookalike", "homograph"
    for e in trusted_entries:
        if n.startswith(e.host + ".") or n.endswith("." + e.host):
            return "lookalike", "misleading_subdomain"
    for e in trusted_entries:
        lab_t, lab_d = label_of(e.host), label_of(n)
        if registrable(n) != registrable(e.host):
            if lab_t == lab_d:
                return "lookalike", "wrong_tld"
            if _edit1(lab_t, lab_d):
                return "lookalike", "typosquat"
            if any(lab_t in re.split(r"-", lbl) for lbl in n.split(".")[:-1]):
                return "lookalike", "brand_mismatch"
    return "untrusted_plain", None


# ------------------------------------------------------------------------------------------------ mutation (lookalike makers)
def make_lookalike(trusted_host, cue, rng, other_host=None, ip_pool=(), listed_ips=()):
    """Program mutation of a namespace host. other_host: a different namespace host (for misleading/brand mismatch)."""
    t = normalise(trusted_host)
    lab, tld = label_of(t), t.rsplit(".", 1)[-1]
    reg_rest = t[len(lab):]                       # ".dom.tld" after the first label (first label is host part)
    if cue == "typosquat":
        base = t.split(".")
        w = base[1] if len(base) > 2 else base[0]
        i = rng.randrange(len(w))
        m = rng.choice(("swap", "drop", "dup"))
        if m == "swap" and len(w) > 1:
            i = min(i, len(w) - 2)
            w2 = w[:i] + w[i + 1] + w[i] + w[i + 2:]
        elif m == "drop" and len(w) > 2:
            w2 = w[:i] + w[i + 1:]
        else:
            w2 = w[:i] + w[i] + w[i:]
        if w2 == w:
            w2 = w + w[-1]
        if len(base) > 2:
            base[1] = w2
        else:
            base[0] = w2
        return ".".join(base)
    if cue == "wrong_tld":
        opts = [x for x in DRAWABLE_TLDS if x != tld]
        return t.rsplit(".", 1)[0] + "." + rng.choice(opts)
    if cue == "raw_ip":
        cands = [i for i in ip_pool if i not in listed_ips]
        return rng.choice(cands)
    if cue == "homograph":
        parts = t.split(".")
        w = parts[1] if len(parts) > 2 else parts[0]
        idx = [i for i, ch in enumerate(w) if ch in CONFUSABLE]
        if not idx:
            return None
        i = rng.choice(idx)
        w2 = w[:i] + CONFUSABLE[w[i]] + w[i + 1:]
        parts[1 if len(parts) > 2 else 0] = w2
        return ".".join(parts).encode("idna").decode("ascii")
    if cue == "misleading_subdomain":
        return "%s.%s" % (t, normalise(other_host))
    if cue == "brand_mismatch":
        o = normalise(other_host)
        return "%s-%s" % (label_of(t), o)
    raise ValueError(cue)


def lab_brand(t):
    parts = t.split(".")
    return parts[1] if len(parts) > 2 else parts[0]
