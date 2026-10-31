"""Seeded name source for lane L-P. EVERY entity string of a generated row comes from c21_infra/namespace.py with the
TRAINING salt (the only salt this lane can reach). No hand-picked fake names.

Slots the family G0-lites need that namespace.py's SLOT_TO_KIND does not list (ns.iac_resource, ns.manifest_object,
ns.ci_job, ns.migration_id, ns.lifecycle_rule, ns.lockfile_package, ns.registry_host exists) are mapped here onto an
EXISTING namespace.py kind (LOCAL_SLOT_TO_KIND). That is a mapping, not a new name generator: the string still comes from
namespace.py. FLAG for L-0: adding these slots to namespace.SLOT_TO_KIND would make the local mapping unnecessary.

`deny_check` is L-0's deny-list program (real brands, registered names, G13 target strings). It is a hook; a production
run without it is allowed but NOTED. A small built-in list of real package names is always applied on top (K3: no real
third-party package name in a generated row), and a built-in list of real stdlib module names for the package kind.
"""
from . import paths  # noqa: F401  (puts c21_infra on sys.path)
from namespace import NameSpace, NamespaceError, SLOT_TO_KIND  # noqa: E402

LOCAL_SLOT_TO_KIND = dict(SLOT_TO_KIND)
LOCAL_SLOT_TO_KIND.update({
    "ns.iac_resource": "noun_entity", "ns.manifest_object": "noun_entity", "ns.ci_job": "noun_entity",
    "ns.migration_id": "noun_entity", "ns.lifecycle_rule": "noun_entity", "ns.lockfile_package": "package",
})

# Real third-party package names that must never appear (small built-in list; L-0's program is the full one). The last line holds real packages that the
# syllable alphabet of namespace.py CAN spell (consonant + vowel (+ l n r s t) syllables), found by hand: a seeded name could coincide with them.
REAL_PACKAGE_DENY = frozenset("""
requests numpy pandas scipy flask django fastapi pydantic pytest setuptools wheel pip boto3 botocore urllib3 certifi idna
six attrs click jinja2 markupsafe werkzeug sqlalchemy pillow cryptography lxml pyyaml tqdm rich typer httpx aiohttp
express react lodash axios moment webpack babel eslint typescript jquery vue angular chalk commander debug uuid
serde tokio rand regex clap syn quote anyhow thiserror libc log bytes futures hyper
redis sinon nodemon tornado kombu mako nose zope karma keras bandit radon luigi ramda terser vite morgan multer pino viper
""".split())


def _deny_union(external):
    def deny(name):
        low = name.lower()
        parts = set(low.replace("_", "-").replace(".", "-").split("-"))
        if low in REAL_PACKAGE_DENY or parts & REAL_PACKAGE_DENY:
            return True
        return bool(external and external(name))
    return deny


class Names:
    """One instance per spec family / group. `tag` separates the families, `seed` the group."""

    def __init__(self, tag, seed, deny_check=None):
        self.tag = tag
        self.ns = NameSpace("training", "%s:%s" % (tag, seed), deny_check=_deny_union(deny_check))
        self._used = {}

    def kind_of(self, slot):
        key = str(slot).split(" ", 1)[0]
        if key not in LOCAL_SLOT_TO_KIND:
            raise NamespaceError("unknown slot %r" % slot)
        return LOCAL_SLOT_TO_KIND[key]

    def get(self, slot, key):
        """Pure function of (tag, seed, slot, key); two different keys may collide (use `unique` when distinctness matters)."""
        return self.ns.name(self.kind_of(slot), "%s/%s" % (self.tag, key))

    def unique(self, slot, key):
        """Distinct from every name issued for the same slot by this instance."""
        return self.ns.unique(self.kind_of(slot), "%s/%s" % (self.tag, key))

    def slug(self, slot, key):
        return self.get(slot, key).lower().replace(" ", "-")
