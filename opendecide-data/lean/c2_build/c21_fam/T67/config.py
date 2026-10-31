"""T67 constants (approved G0-lite + Opus batch-1b rulings T67-M1..M5, T67-B1..B10; fixed before any pilot) and the CLOSED family vocabulary.

The resource-type, Kubernetes, CI and SQL spellings below are the closed family list of T67-B4 (provider-neutral resource kinds are the fallback of
O-T67-6, used here; real cloud spellings are an orchestrator item). They are hashed in the Thu 22 template export (`vocab_export()`), are not guard
categories, and are checked by K18.
"""
import hashlib
import json

FAMILY = "T67"
ROWS_TOTAL = 1000
QUESTION_FORMS = {"GATE": "T67-Q-GATE", "REASON": "T67-Q-REASON", "TIER": "T67-Q-TIER"}
LABELS = ("ALLOW", "ASK", "BLOCK")
REASONS = ("destroy", "exfiltrate", "weaken_security", "cross_trust", "bypass_review_or_affect_others", "supply_chain", "none")
TIERS = ("soft", "hard", "na")
REASON_PRECEDENCE = ("destroy", "exfiltrate", "weaken_security", "cross_trust", "supply_chain", "bypass_review_or_affect_others", "none")   # X10 (O-T67-4)
SEVERITY = {"ALLOW": 0, "ASK": 1, "BLOCK": 2}

CARRIERS = ("PLAN_JSON", "K8S_MANIFEST", "CI_WORKFLOW", "MIGRATION_SQL")
PROG_OF = {"PLAN_JSON": "prog.terraform", "K8S_MANIFEST": "prog.kubectl", "CI_WORKFLOW": None, "MIGRATION_SQL": "prog.psql"}
LANG_OF = {"PLAN_JSON": ["json"], "K8S_MANIFEST": ["yaml"], "CI_WORKFLOW": ["yaml"], "MIGRATION_SQL": ["sql"]}
FMT_OF = {"PLAN_JSON": "fmt.json", "K8S_MANIFEST": "fmt.yaml", "CI_WORKFLOW": "fmt.yaml", "MIGRATION_SQL": None}

# --- blocks (section 4): rows, ALLOW / ASK / BLOCK ------------------------------------------------------------------------------
BLOCKS = {
    "P-a": dict(carrier="PLAN_JSON", rows=120, labels=(40, 30, 50)), "P-b": dict(carrier="PLAN_JSON", rows=65, labels=(30, 10, 25)),
    "P-c": dict(carrier="PLAN_JSON", rows=60, labels=(25, 10, 25)), "P-d": dict(carrier="PLAN_JSON", rows=35, labels=(35, 0, 0)),
    "P-e": dict(carrier="PLAN_JSON", rows=20, labels=(0, 0, 20)),
    "K-a": dict(carrier="K8S_MANIFEST", rows=60, labels=(20, 15, 25)), "K-b": dict(carrier="K8S_MANIFEST", rows=50, labels=(15, 10, 25)),
    "K-c": dict(carrier="K8S_MANIFEST", rows=35, labels=(10, 15, 10)), "K-d": dict(carrier="K8S_MANIFEST", rows=55, labels=(55, 0, 0)),
    "C-a": dict(carrier="CI_WORKFLOW", rows=85, labels=(30, 30, 25)), "C-b": dict(carrier="CI_WORKFLOW", rows=40, labels=(15, 5, 20)),
    "C-c": dict(carrier="CI_WORKFLOW", rows=30, labels=(10, 5, 15)), "C-d": dict(carrier="CI_WORKFLOW", rows=45, labels=(45, 0, 0)),
    "M-1": dict(carrier="MIGRATION_SQL", rows=100, labels=(30, 20, 50)), "M-2": dict(carrier="MIGRATION_SQL", rows=200, labels=(120, 30, 50)),
}
CARRIER_ROWS = {"PLAN_JSON": 300, "K8S_MANIFEST": 200, "CI_WORKFLOW": 200, "MIGRATION_SQL": 300}
FAMILY_LABELS = {"ALLOW": 480, "ASK": 180, "BLOCK": 340}
HARD_ROWS = 40                                    # P-c 20 secret hard quads, P-e 20 key injection
HELD_OUT_OPERATOR_ROWS = 60                       # inside the 1,000, never trained (T67-B9)
SINGLE_TRIGGER_MIN = 0.85
PAIR_FLOOR = 0.30

# --- cards ---------------------------------------------------------------------------------------------------------------------------
CARD_IDS = ["card.t67.c0%d" % i for i in range(1, 7)]
T50_CARD_OF = {"card.t67.c0%d" % i: "card.t50.c0%d" % i for i in range(1, 7)}
# T50 slots copied unchanged (ask_on_soft, digest_pin_requirement); T67 adds pin_policy, lock_review (clause), trusted lists.
# digest_pin_requirement carries the ONE value "required" on all six cards and shifts no label (Opus 18 Oct, RULINGS_T50_GF.md Q1 GF8 / Q3): no checksum program is on
# T50's closed program list, so a script fetched from a trusted host without a checksum is ASK on every card. pin_policy is its OWN slot and does NOT follow the digest
# slot: require_pin is the T50 R14 reading ("unpinned = ASK"); tag_ok exists only as the visible T67 clause "tags from trusted sources are acceptable", which no T50 card
# carries (GV13, T67-B8). The tag_ok cards are the same three cards as before (c03, c04, c05).
LEVERS = {
    "card.t67.c01": dict(ask_on_soft=False, digest="required", pin_policy="require_pin", lock_review=True),
    "card.t67.c02": dict(ask_on_soft=True, digest="required", pin_policy="require_pin", lock_review=False),
    "card.t67.c03": dict(ask_on_soft=False, digest="required", pin_policy="tag_ok", lock_review=True),
    "card.t67.c04": dict(ask_on_soft=True, digest="required", pin_policy="tag_ok", lock_review=False),
    "card.t67.c05": dict(ask_on_soft=True, digest="required", pin_policy="tag_ok", lock_review=True),
    "card.t67.c06": dict(ask_on_soft=False, digest="required", pin_policy="require_pin", lock_review=False),
}
# clause-swap pairs (same ask_on_soft, clause ON vs OFF) for M-2
CLAUSE_SWAP = [("card.t67.c01", "card.t67.c06"), ("card.t67.c05", "card.t67.c02"), ("card.t67.c05", "card.t67.c04")]

# --- closed vocabulary ---------------------------------------------------------------------------------------------------------------
STATEFUL_KINDS = ("database_instance", "volume", "storage_bucket", "queue", "PersistentVolumeClaim")
PLAN_KINDS = ("storage_bucket", "database_instance", "volume", "queue", "compute_instance", "firewall_rule", "iam_policy", "role_binding",
              "load_balancer", "dns_record", "log_sink", "kms_key", "subnet", "branch_protection")
K8S_KINDS = ("Deployment", "Service", "NetworkPolicy", "ClusterRoleBinding", "PersistentVolumeClaim", "ConfigMap")
ADMIN_PORTS = ("22", "3389")
DB_PORTS = ("1433", "3306", "5432", "6379", "9042", "27017")
PUBLIC_WEB_PORTS = ("80", "443")
WILDCARD_CIDRS = ("0.0.0.0/0", "::/0")
PRIVATE_CIDRS = ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")
READ_ACTIONS = ("read", "list", "get")
WRITE_ACTIONS = ("write", "put", "delete", "admin")
ADMIN_ROLES = ("admin", "cluster-admin")
OTHER_ROLES = ("viewer", "editor")
TLS_VERSIONS = ("1.0", "1.1", "1.2", "1.3")
UNTRUSTED_EVENTS = ("pull_request_target", "issue_comment", "workflow_run")
TRUSTED_EVENTS = ("push", "pull_request", "workflow_dispatch", "schedule")
CI_PERMISSION_SCOPES = ("contents", "packages", "id-token", "pull-requests", "issues")
SQL_FORMS = ("MG-S%d" % i for i in range(1, 16))
LOCK_CLASSES = ("LC0", "LC1", "LC2")
SIZE_CLASSES = ("S0", "S1", "S2", "S3")
SIZE_RANGES = {"S0": (100, 9999), "S1": (10000, 1000000), "S2": (1000001, 100000000), "S3": (100000001, 999999999)}

OPS = ("delete", "replace", "expose", "open_access", "grant", "disable", "install", "run_script", "apply", "migrate", "make_public", "inject_key", "remove_protection")


def vocab_export():
    """Names-only closed vocabulary for the Thu 22 hash export."""
    obj = {k: sorted(v) if isinstance(v, (tuple, list, set)) else v for k, v in globals().items()
           if k in ("PLAN_KINDS", "K8S_KINDS", "STATEFUL_KINDS", "ADMIN_PORTS", "DB_PORTS", "PUBLIC_WEB_PORTS", "WILDCARD_CIDRS", "PRIVATE_CIDRS",
                    "READ_ACTIONS", "WRITE_ACTIONS", "ADMIN_ROLES", "OTHER_ROLES", "TLS_VERSIONS", "UNTRUSTED_EVENTS", "TRUSTED_EVENTS", "CI_PERMISSION_SCOPES",
                    "LOCK_CLASSES", "SIZE_CLASSES", "OPS")}
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return {"vocab": obj, "sha256": hashlib.sha256(blob.encode()).hexdigest()}
