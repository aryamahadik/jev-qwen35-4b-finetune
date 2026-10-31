"""Name provider: every identifier in a T41c row comes from c21_infra/namespace.py with the TRAINING salt.

- NameSpace is always built with side="training" (the built-in training salt). There is no salt argument here.
- Slots with a native kind in namespace.py (org, repo, host, service, handle, mcp_tool) use it.
- Slots whose kind L-0 has not added yet (package, path_stem, branch, envvar, ticket, project, endpoint,
  mcp_server) are REFUSED in strict mode (`SlotUnavailable`), because NAMES_MANIFEST_V1 says no row job may fill a
  null-kind slot. `proxy=True` derives them from existing kinds so unit tests and the 20-example dry run can run;
  every example built that way carries `proxy_names=True` and a row job must refuse it.
- Hosts use namespace.py's host renderer (reserved TLDs, a subset of the shared L-0 host-TLD list). Raw IPs come
  only from the shared raw-IP pool ranges, drawn by a seeded program from a namespace-derived digest.
- A caller-supplied deny_check (the L-0 deny-list program) makes the namespace redraw.
"""
import hashlib
import re
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_INFRA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(_HERE))), "c21_infra")
if _INFRA not in sys.path:
    sys.path.insert(0, _INFRA)
import namespace as _ns  # noqa: E402

NATIVE = {"ns.org": "company", "ns.repo": "repo", "ns.host": "host", "ns.service": "service",
          "ns.handle": "user", "ns.mcp_tool": "tool"}
# L-0 will add these kinds (named after the slot suffix); until then they are null in v1
PENDING = {"ns.package": "package", "ns.path_stem": "path_stem", "ns.branch": "branch", "ns.envvar": "envvar",
           "ns.ticket": "ticket", "ns.project": "project", "ns.endpoint": "endpoint", "ns.mcp_server": "mcp_server"}
_PROXY_BASE = {"ns.package": "repo", "ns.path_stem": "user", "ns.branch": "tool", "ns.envvar": "tool",
               "ns.ticket": "bucket", "ns.project": "repo", "ns.endpoint": "tool", "ns.mcp_server": "service"}

# shared L-0 raw-IP pool (documentation + private ranges); the fixed metadata literal is never drawn
RAW_IP_POOL = (("192", "0", "2"), ("198", "51", "100"), ("203", "0", "113"), ("10",), ("172", "16"), ("192", "168"))


class SlotUnavailable(Exception):
    pass


class NameProvider:
    def __init__(self, seed, proxy=False, deny_check=None):
        self.ns = _ns.NameSpace("training", seed, deny_check=deny_check)
        self.proxy = bool(proxy)
        self.used_proxy = False

    def fingerprint(self):
        return self.ns.fingerprint()

    def get(self, slot, key):
        """One distinct name per (slot, key) within this provider."""
        if slot in NATIVE:
            return self.ns.unique(NATIVE[slot], "%s|%s" % (slot, key))
        if slot in PENDING:
            kind = PENDING[slot]
            if kind in _ns.KINDS:                     # L-0 added the native kind
                return self.ns.unique(kind, "%s|%s" % (slot, key))
            if not self.proxy:
                raise SlotUnavailable("%s has no namespace kind yet (L-0 must add %r); rows are blocked" % (slot, kind))
            self.used_proxy = True
            base = self.ns.unique(_PROXY_BASE[slot], "%s|%s" % (slot, key))
            return self._shape(slot, base)
        raise SlotUnavailable("unknown slot %r" % slot)

    @staticmethod
    def _shape(slot, base):
        stem = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
        if slot == "ns.envvar":
            return re.sub(r"[^A-Z0-9]+", "_", base.upper()).strip("_")
        if slot == "ns.branch":
            return "feat/" + stem
        if slot == "ns.ticket":                       # prefix from the name, digits from its hex part
            hexpart = re.findall(r"[0-9a-f]{4}$", stem)
            digits = "".join(str(int(c, 16) % 10) for c in (hexpart[0] if hexpart else "0000"))
            return stem.split("-")[0][:4].upper() + "-" + digits
        if slot == "ns.endpoint":
            return "/" + stem.replace("_", "/")
        return stem

    def host(self, key):
        return self.get("ns.host", key)

    def raw_ip(self, key):
        """Raw IP drawn from the shared pool only (seeded, from a namespace-derived digest)."""
        h = hashlib.sha256(("rawip|" + self.ns.unique("host", "rawip|" + str(key))).encode()).digest()
        base = RAW_IP_POOL[h[0] % len(RAW_IP_POOL)]
        rest = [str(h[i + 1] % 254 + 1) for i in range(4 - len(base))]
        return ".".join(list(base) + rest)

    def path_in(self, workspace, key, depth=2):
        parts = [self.get("ns.path_stem", "%s|%d" % (key, i)) for i in range(depth)]
        return workspace.rstrip("/") + "/" + "/".join(parts)
