"""Constants B uses, written from the T67 G0-lite (rule table X01-X11, M01 / M02, X10 precedence) and the closed vocabulary of the family. Python constants only;
nothing is read at run time. The draft lock-class assignment is the G0-lite's own UNVERIFIED draft; `make_solver_b(lock_table=...)` replaces it with the hashed
Opus T67-LOCK-TABLE when one exists."""

LABELS = ("ALLOW", "ASK", "BLOCK")
SEVERITY = {"ALLOW": 0, "ASK": 1, "BLOCK": 2}
REASONS = ("destroy", "exfiltrate", "weaken_security", "cross_trust", "bypass_review_or_affect_others", "supply_chain", "none")
TIERS = ("soft", "hard", "na")
# X10: reason precedence when several members share the winning label (destroy > exfiltrate > weaken_security > cross_trust > supply_chain > bypass...)
PRECEDENCE = ("destroy", "exfiltrate", "weaken_security", "cross_trust", "supply_chain", "bypass_review_or_affect_others", "none")

HEADS = {"T67-GATE": "GATE", "T67-REASON": "REASON", "T67-TIER": "TIER"}

# --- vocabulary --------------------------------------------------------------------------------------------------------------------------
STATEFUL_KINDS = ("database_instance", "volume", "storage_bucket", "queue", "PersistentVolumeClaim")
ADMIN_PORTS = ("22", "3389")
DB_PORTS = ("1433", "3306", "5432", "6379", "9042", "27017")
WEB_PORTS = ("80", "443")
WILDCARD_CIDRS = ("0.0.0.0/0", "::/0")
ADMIN_ROLES = ("admin", "cluster-admin")
UNTRUSTED_EVENTS = ("pull_request_target", "issue_comment", "workflow_run")
STORE_KINDS = ("storage_bucket",)
KEY_INJECTION_ATTRS = ("ssh_key_added", "sudo_user_added", "sudo_user")
# protection attributes of a plan item and the value that means "off / lowered"
PROTECTION_OFF = {"deletion_protection": (False,), "encrypted": (False,), "audit_logging": (False,), "backup_retention_days": (0,)}
TLS_RANK = {"1.0": 0, "1.1": 1, "1.2": 2, "1.3": 3}

# --- operation words of the user turns (the closed lexicon of the family; the surface phrase of each operation) ----------------------------
OP_PHRASE = {"delete": "delete", "replace": "replace", "create": "create", "update": "update", "make_public": "make public", "open_access": "open up",
             "expose": "expose", "grant": "grant access on", "remove_protection": "remove the protection on", "disable": "turn off", "install": "use",
             "run_script": "run the script at", "apply": "apply", "migrate": "run the migration on", "inject_key": "add a login key to"}
# which operation words can clear which effect (an effect is cleared only when the turn names one of these AND the target)
OPS_FOR_ACTION = {"delete": ("delete", "replace"), "replace": ("replace", "delete"), "create": ("create",), "update": ("update",)}

# --- SQL: statement forms and the draft lock table (G0-lite 3.2: LC0 for 1, 2, 3, 6, 8, 11, 15; LC1 for 5, 7; LC2 for 4, 9, 10) -------------
M02_FORMS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15)
LOCK_DRAFT = {1: "LC0", 2: "LC0", 3: "LC0", 4: "LC2", 5: "LC1", 6: "LC0", 7: "LC1", 8: "LC0", 9: "LC2", 10: "LC2", 11: "LC0", 15: "LC0"}
SIZE_EDGES = (("S0", 10000), ("S1", 1000000), ("S2", 100000000))      # S0 < 10k <= S1 <= 1M < S2 <= 100M < S3 (inclusive upper edges of S1 / S2)
