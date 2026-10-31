"""SQL data-statement rules of M01 that T50 labels outside R11, as B's own rules from the T50 G0-lite rows and the Opus rulings (RULINGS_T50_GF.md Q4: GF6, GF10):

    R10 | E7 SQL data change | with predicate in dev = ALLOW; no predicate or shared = ASK; prod = BLOCK; reason destroy; soft
    GF6  | the predicate condition applies to UPDATE and DELETE only; a plain INSERT: dev ALLOW / none / na, shared ASK / destroy / soft, production BLOCK / destroy / soft
    GF10 | a SQL GRANT is E12 (R15 soft part): BLOCK / weaken_security / soft in dev, shared and production alike; never hard; naming both the grant and its target clears it

The card lever (`soft blocks are raised to ASK`) turns each soft BLOCK into ASK in every SQL environment (SQL has no SLT-1 lane, so the C4 exception does not apply); consent is applied
by `effects.resolve`. INSERT forms that overwrite existing rows (ON CONFLICT DO UPDATE, OR REPLACE, REPLACE INTO, ON DUPLICATE KEY UPDATE) are not plain INSERT: the text does not label
them, so B abstains on them (they are not built).
Plug-point shape: rule(tag, predicate, env, backup) -> (label, reason, tier) or None (None = abstain). `backup` plays no part in R10."""

BLOCK = ("BLOCK", "destroy", "soft")
ASK = ("ASK", "destroy", "soft")
ALLOW = ("ALLOW", "none", "na")
GRANT = ("BLOCK", "weaken_security", "soft")


def rule(tag, predicate, env, backup):
    if tag in ("update", "delete"):
        if env == "production":
            return BLOCK
        if env == "shared":
            return ASK
        if env == "dev":
            return ALLOW if predicate else ASK
        return None
    if tag == "insert":
        return {"dev": ALLOW, "shared": ASK, "production": BLOCK}.get(env)
    if tag == "grant":
        return GRANT if env in ("dev", "shared", "production") else None
    return None                                         # insert_upsert and anything else: the text does not decide
