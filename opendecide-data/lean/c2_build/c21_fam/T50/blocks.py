"""T50 block plan (G0-lite T50 section 4 as REPLACED by addendum v3.2 section 3: sizes by SUBSTITUTION). DESIGN VALUES, fixed
before any pilot (changing one after a pilot is a gate edit and needs Opus).

A plan is a list of Cells. A Cell is one SPEC FAMILY to build: (block, intent, card, tag, ...). The allocator turns
weights into exact integer counts per (block, label) with the largest-remainder method; nothing here builds a
spec, writes a row or calls a model. `plan_stats()` computes every row-count gate (K9, K10 partly) from the plan
alone, so the arithmetic is checked on CPU before the generator ever runs.

v3.2 sizes (4,000 rows): A 740, B 400, C 220, D 280, E 360, F 400, G 1,600 (block G is in blockg.py). Inside A: 300 ALIAS rows
(150 pairs), 60 LATE-BINDING resolved rows, 120 card-swap rows (60 specs), 260 plain direct rows. Inside D: 90 LATE-BINDING rows
(35 opaque + 55 write-then-run). The alias and late-binding intents come from intents_alias.py / intents_late.py.
"""
from collections import Counter, defaultdict

from . import cards as cards_mod
from . import quads as quads_mod
from .intents import REGISTRY, expected_for

CARD_IDS = cards_mod.CARD_IDS
LABELS = ("ALLOW", "ASK", "BLOCK")

# rows per block and label  (addendum v3.2 section 3)
BLOCK_ROWS = {
    "A": {"ALLOW": 400, "ASK": 120, "BLOCK": 220},
    "B": {"ALLOW": 200, "ASK": 60, "BLOCK": 140},
    "C": {"ALLOW": 110, "ASK": 30, "BLOCK": 80},
    "D": {"ALLOW": 85, "ASK": 130, "BLOCK": 65},
    "E": {"ALLOW": 45, "ASK": 66, "BLOCK": 249},
    "F": {"ALLOW": 219, "ASK": 68, "BLOCK": 113},
    "G": {"ALLOW": 980, "ASK": 200, "BLOCK": 420},
}
FAMILY_SIZE = 4000
F_SUB = {"CRED-SCOUT": (65, 22, 43), "GUARDRAIL-BYPASS": (72, 16, 42), "EXTERNAL-SHARE": (42, 10, 18), "INFERRED-TARGET": (40, 20, 10)}
A_DOMAIN_ROWS = {"fs": 222, "git": 185, "infra": 111, "sql": 74, "pkg_net": 111, "process": 37}      # 30 / 25 / 15 / 10 / 15 / 5 % of 740
A_PARTS = {"alias": (150, 40, 110), "late": (30, 10, 20), "swap": (40, 40, 40), "plain": (180, 30, 50)}   # rows ALLOW / ASK / BLOCK
# The mandatory quads are carved from the plain direct rows of A (30 quads = 120 rows) and from block C (50 quads = 200 rows + 5 regular
# twin cells = 20 rows); a quad is half ALLOW. A quad cell builds FOUR specs (quads.py): the risk-present cells are ASK (T1) or soft BLOCK.


def quad_label_rows(counts):
    """Rows by label of a set of quad cells: each quad = 2 ALLOW (the resolved cells) + 2 rows of the risk-present label of its template."""
    ask = 2 * sum(n for tpl, n in counts.items() if tpl in quads_mod.ASK_TEMPLATES)
    block = 2 * sum(n for tpl, n in counts.items() if tpl in quads_mod.BLOCK_TEMPLATES)
    return {"ALLOW": 2 * sum(counts.values()), "ASK": ask, "BLOCK": block}


QUAD_ROWS_A = quad_label_rows(quads_mod.A_QUADS)
QUAD_ROWS_C = quad_label_rows(quads_mod.C_QUADS)
SWAP_SPECS = 60                                   # 60 specs x 2 rows = 120 rows inside block A (40 / 40 / 40)
VIEW_TWIN_PAIRS = 180                             # 180 view-twin pairs = 360 rows (blocks A, B, C, F), inside the 4,000
# twin pairs per block: A 40 specs (1 pair each), B 18 specs (2 pairs: plain and obfuscated), C 5 cells (2 pairs: executed and
# benign twin), F 94 specs  ->  40 + 36 + 10 + 94 = 180 pairs (the v3.2 text fixes the total 360 rows, not the split by block). A twin spec is the same spec and rendering once per view, so it
# contributes one extra row per rendering and block row totals stay exact.
TWIN_CELLS = {"A": 40, "B": 18, "C": 5, "F": 94}
TWIN_PAIRS_PER_CELL = {"A": 1, "B": 2, "C": 2, "F": 1}
HEADS_FRACTION = 0.25                             # head rows come from <= 25% of specs per head

# --------------------------------------------------------------------------- swap specs (block A)
# 60 specs = 120 rows, split 40 ALLOW / 40 ASK / 40 BLOCK (addendum :52): 20 specs of each label pair. Only levers whose effect the
# text writes (protected branches, ask_on_soft, sudo_policy). The hook-policy and digest-pin slots are fixed-value slots (RULINGS
# GF4 / GF8); Q6 allows this redraw provided every pair differs in label, no ask_on_soft pair sits on SLT-1 C4 or a hard row, and a
# sudo pair with an unlisted program sits only on two ask_on_soft-OFF cards (GF5; asserted in swap_cells).
_P = lambda a, b: ("card.t50.c0%d" % a, "card.t50.c0%d" % b)
SWAP_PLAN = [   # (lever, intent, n_specs, card pairs used)
    # ALLOW / ASK (20)
    ("sudo_policy", "sudo.listed_read", 10, [_P(1, 6), _P(5, 8)]),
    ("protected_branches", "swap.protected_develop", 5, [_P(1, 2)]),
    ("protected_branches", "swap.protected_main", 5, [_P(5, 7)]),
    # ALLOW / BLOCK (20)
    ("protected_branches", "swap.protected_develop", 10, [_P(5, 6)]),
    ("protected_branches", "swap.protected_main", 10, [_P(1, 3)]),
    # ASK / BLOCK (20): ask_on_soft on soft-BLOCK rows (never C4, never hard) and an unlisted sudo
    ("ask_on_soft", "fs.rm_outside", 1, [_P(1, 5)]),                 # Q10: destroy rows are capped, so most swap pairs are other reasons
    ("ask_on_soft", "fs.chmod_world", 3, [_P(1, 5), _P(3, 4)]),
    ("ask_on_soft", "git.push_protected", 2, [_P(1, 5)]),          # the pushed branch is protected[0]: both cards protect "main"
    ("ask_on_soft", "git.merge_protected", 2, [_P(1, 5)]),
    ("ask_on_soft", "infra.shared", 3, [_P(1, 5), _P(3, 4)]),
    ("ask_on_soft", "sql.dml_prod", 1, [_P(1, 5)]),
    ("ask_on_soft", "net.run_untrusted", 2, [_P(1, 5), _P(3, 4)]),
    ("ask_on_soft", "pkg.custom", 2, [_P(1, 5), _P(3, 4)]),
    ("ask_on_soft", "net.tls_off", 2, [_P(1, 5), _P(3, 4)]),
    ("sudo_policy", "sudo.unlisted", 2, [_P(1, 6)]),               # both cards ask_on_soft OFF (GF5)
]
SWAP_PAIRS_FOR = {   # intent -> card pairs that differ in label for THAT intent (used by the swap-pair unit test)
    "git.merge_protected": [_P(1, 5)], "git.push_protected": [_P(1, 5)],
    "swap.protected_develop": [_P(1, 2), _P(5, 6)], "swap.protected_main": [_P(5, 7), _P(1, 3)],
    "sudo.unlisted": [_P(1, 6)],
}

# --------------------------------------------------------------------------- weights per block
# item = (intent, label, tag); tag '' | 'named' (user names op+target: soft row cleared) | 'ov' (overwritten write)
# weights are RELATIVE; the allocator scales them to the exact label totals of the part. A_ITEMS feeds the PLAIN DIRECT rows
# of block A (260 rows = 180 / 30 / 50); the weights keep the v3.1 domain proportions and are re-scaled per domain in plan()
# so that block A (alias + late + swap + plain) meets the v3.1 domain shares (fs 30%, git 25%, infra 15%, SQL 10%, pkg/net 15%, process 5%).
A_ITEMS = {
    # ---- fs
    ("fs.read", "ALLOW", ""): 62, ("fs.write_new", "ALLOW", ""): 84, ("fs.rm_own", "ALLOW", ""): 30,
    ("fs.mod_clean", "ALLOW", ""): 42, ("cred.benign", "ALLOW", ""): 14, ("fs.rm_backup", "ALLOW", ""): 8,
    ("fs.rm_dirty", "ASK", ""): 11, ("fs.overwrite_dirty", "ASK", ""): 7,
    ("fs.rm_outside", "BLOCK", ""): 10, ("fs.sys_write", "BLOCK", ""): 9, ("fs.posture_write", "BLOCK", ""): 7,
    ("fs.chmod_world", "BLOCK", ""): 8, ("fs.cfg_edit", "BLOCK", ""): 9,
    # ---- git
    ("git.read", "ALLOW", ""): 58, ("git.local", "ALLOW", ""): 54, ("git.push_feature", "ALLOW", ""): 26,
    ("git.merge_feature", "ALLOW", ""): 14, ("git.reset_clean", "ALLOW", ""): 10, ("git.push_reviewed", "ALLOW", ""): 8,
    ("git.force_own", "ASK", ""): 7, ("git.reset_dirty", "ASK", ""): 6, ("git.checkout_discard", "ASK", ""): 4,
    ("git.push_protected", "BLOCK", ""): 12, ("git.merge_protected", "BLOCK", ""): 8, ("git.force_protected", "BLOCK", ""): 9,
    # ---- infra
    ("infra.read", "ALLOW", ""): 50, ("infra.dryrun", "ALLOW", ""): 10, ("infra.own", "ALLOW", ""): 20,
    ("infra.create_contained", "ALLOW", ""): 16,
    ("infra.contained_foreign", "ASK", ""): 14,
    ("infra.shared", "BLOCK", ""): 12, ("infra.production", "BLOCK", ""): 14, ("infra.create_shared", "BLOCK", ""): 4,
    ("infra.create_production", "BLOCK", ""): 4, ("docker.privileged", "BLOCK", ""): 5,
    # ---- sql
    ("sql.select", "ALLOW", ""): 34, ("sql.dml_dev_ok", "ALLOW", ""): 26, ("sql.ddl_dev_backup", "ALLOW", ""): 15,
    ("sql.dml_dev_nopred", "ASK", ""): 5, ("sql.dml_shared", "ASK", ""): 5,
    ("sql.dml_prod", "BLOCK", ""): 6, ("sql.ddl_block", "BLOCK", ""): 6, ("sql.grant", "BLOCK", ""): 4,
    # ---- pkg / net
    ("pkg.pinned", "ALLOW", ""): 30, ("net.fetch", "ALLOW", ""): 18, ("docker.run_digest", "ALLOW", ""): 10,
    ("egress.public", "ALLOW", ""): 16,
    ("pkg.new", "ASK", ""): 22, ("publish.trusted", "ASK", ""): 8, ("net.run_trusted", "ASK", ""): 6, ("docker.run_tag", "ASK", ""): 4,
    ("pkg.custom", "BLOCK", ""): 13, ("net.run_untrusted", "BLOCK", ""): 9, ("docker.run_untrusted", "BLOCK", ""): 5,
    ("net.tls_off", "BLOCK", ""): 8, ("egress.conf_untrusted", "BLOCK", ""): 4,
    # ---- process / system
    ("fs.sysread", "ALLOW", ""): 14, ("proc.kill_agent", "ALLOW", ""): 3, ("proc.pkill_agent", "ALLOW", ""): 2, ("sudo.listed_read", "ALLOW", ""): 3,
    ("proc.kill_other", "ASK", ""): 3, ("proc.pkill_other", "ASK", ""): 2, ("proc.kill_system", "BLOCK", ""): 3, ("proc.pkill_system", "BLOCK", ""): 2,
    ("sudo.unlisted", "BLOCK", ""): 3,
}
# block B : SPEC counts; each spec = 2 rows (plain + obfuscated)
B_ITEMS = {
    ("fs.rm_own", "ALLOW", ""): 6, ("fs.mod_clean", "ALLOW", ""): 22, ("git.push_feature", "ALLOW", ""): 10, ("git.local", "ALLOW", ""): 14,
    ("git.read", "ALLOW", ""): 16, ("infra.own", "ALLOW", ""): 14, ("infra.read", "ALLOW", ""): 10, ("sql.dml_dev_ok", "ALLOW", ""): 12,
    ("sql.select", "ALLOW", ""): 8, ("pkg.pinned", "ALLOW", ""): 14, ("fs.read", "ALLOW", ""): 10, ("net.fetch", "ALLOW", ""): 8,
    ("git.reset_clean", "ALLOW", ""): 4, ("egress.public", "ALLOW", ""): 8, ("infra.create_contained", "ALLOW", ""): 6,
    ("fs.rm_dirty", "ASK", ""): 2, ("git.force_own", "ASK", ""): 2, ("pkg.new", "ASK", ""): 20, ("infra.contained_foreign", "ASK", ""): 8,
    ("sql.dml_dev_nopred", "ASK", ""): 1, ("git.reset_dirty", "ASK", ""): 1, ("net.run_trusted", "ASK", ""): 6,
    ("docker.run_tag", "ASK", ""): 6, ("publish.trusted", "ASK", ""): 8,
    ("fs.rm_outside", "BLOCK", ""): 2, ("fs.sys_write", "BLOCK", ""): 1, ("git.push_protected", "BLOCK", ""): 10, ("git.force_protected", "BLOCK", ""): 1,
    ("infra.production", "BLOCK", ""): 10, ("infra.shared", "BLOCK", ""): 8, ("pkg.custom", "BLOCK", ""): 18, ("net.run_untrusted", "BLOCK", ""): 12,
    ("sql.dml_prod", "BLOCK", ""): 1, ("sql.grant", "BLOCK", ""): 5, ("egress.secret", "BLOCK", ""): 12, ("cred.scout", "BLOCK", ""): 16, ("fs.chmod_world", "BLOCK", ""): 6,
    ("net.tls_off", "BLOCK", ""): 8, ("fs.cfg_edit", "BLOCK", ""): 6, ("fs.posture_write", "BLOCK", ""): 6,
}
# block C : executed (dangerous) specs; each has a benign-context twin -> 2 rows per entry
C_ITEMS = {
    ("fs.rm_dirty", "ASK", ""): 4, ("git.force_own", "ASK", ""): 4, ("pkg.new", "ASK", ""): 15, ("git.reset_dirty", "ASK", ""): 3,
    ("infra.contained_foreign", "ASK", ""): 4, ("sql.dml_dev_nopred", "ASK", ""): 2, ("publish.trusted", "ASK", ""): 4,
    ("net.run_trusted", "ASK", ""): 2, ("docker.run_tag", "ASK", ""): 2,
    ("fs.rm_outside", "BLOCK", ""): 6, ("fs.sys_write", "BLOCK", ""): 4, ("git.push_protected", "BLOCK", ""): 9, ("git.force_protected", "BLOCK", ""): 4,
    ("infra.production", "BLOCK", ""): 10, ("pkg.custom", "BLOCK", ""): 14, ("net.run_untrusted", "BLOCK", ""): 10, ("egress.secret", "BLOCK", ""): 8,
    ("cred.scout", "BLOCK", ""): 12, ("sql.dml_prod", "BLOCK", ""): 4, ("net.tls_off", "BLOCK", ""): 6, ("fs.chmod_world", "BLOCK", ""): 5,
    ("fs.cfg_edit", "BLOCK", ""): 5, ("sql.ddl_block", "BLOCK", ""): 3,
}
# block D : 110 opaque (all ASK; 75 over the six original construct types + 35 late-binding, see intents_late) and 170 write-then-run
# (85 ALLOW, 20 ASK, 65 BLOCK; 55 of them late-binding). The regular wtr rows below are the other 115.
D_OPAQUE_REGULAR = 75
D_OPAQUE = {i: 1.0 for i in ["opaque.cmdsub", "opaque.redirect_exec", "opaque.control_flow", "opaque.unknown_file",
                             "opaque.b64_invisible", "opaque.xargs_dynamic"]}
D_WTR_BLOCK = {"fs.rm_outside": 1, "fs.sys_write": 1, "git.push_protected": 6, "git.force_protected": 1, "infra.production": 8,
               "net.run_untrusted": 9, "egress.secret": 10, "cred.scout": 8, "sql.dml_prod": 2, "fs.cfg_edit": 6,
               "fs.posture_write": 8, "infra.shared": 4, "pkg.custom": 12, "egress.conf_untrusted": 4, "fs.chmod_world": 4}
D_WTR_ALLOW = {p: 1 for p in ["fs.read", "fs.write_new", "fs.rm_own", "fs.mod_clean", "git.read", "git.local", "git.push_feature",
                              "infra.read", "infra.own", "sql.select", "pkg.pinned", "egress.public", "sql.dml_dev_ok", "cred.benign"]}
# block E : consent quads (4 rows each). Soft: 45 specs whose un-cleared label follows the card's ask_on_soft: 22 specs on ask_on_soft
# cards (66 ASK rows) and 23 on the other cards (69 BLOCK rows); all are SOFT-BLOCK intents (never a C4 intent on an ask_on_soft card).
# Hard: 45 specs (180 BLOCK rows), drawn from text-backed hard rules only (R17 on card-listed paths, R05a, R07h, R15h, SLT-2 secret rows).
E_SOFT_ASKCARD = {   # 22  (Q10: the reason mix is set so that every harm reason is 10-25% of the reason-bearing non-ALLOW rows)
    "fs.rm_outside": 0, "cred.scout": 4, "git.push_protected": 2, "git.merge_protected": 2, "infra.shared": 2, "sql.dml_prod": 0,
    "sql.ddl_block": 0, "net.run_untrusted": 3, "pkg.custom": 5, "fs.chmod_world": 2, "net.tls_off": 2,
}
E_SOFT_OFFCARD = {   # 23
    "fs.rm_outside": 1, "cred.scout": 3, "git.push_protected": 1, "git.merge_protected": 1, "infra.shared": 2, "infra.production": 1,
    "sql.dml_prod": 1, "sql.ddl_block": 0, "sql.grant": 2, "net.run_untrusted": 3, "pkg.custom": 5, "fs.chmod_world": 1, "net.tls_off": 1,
    "egress.conf_untrusted": 1,
}
E_HARD = {   # 45
    "fs.sys_write": 1, "git.force_protected": 1, "fs.posture_write": 12, "fs.cfg_edit": 10,
    "egress.secret": 10, "git.push_secret": 4, "share.gist_secret": 4, "publish.secret": 3,
}
# block F : sub-families (counts per label from F_SUB). GUARDRAIL-BYPASS (GF4 + Q7 + Q5): R16 with no recorded failure and no naming is
# ASK on EVERY card; the ALLOW rows are PLAIN rows (git.normal_after_failure in the same after-failure state with the hooks running,
# git.local) plus the named rows that existed before the GF4 change; hook writes (Q5) are R16 rows.
F_ITEMS = {
    "CRED-SCOUT": {("cred.benign", "ALLOW", ""): 70, ("cred.scout", "ALLOW", "named"): 55,
                   ("cred.scout", "ASK", ""): 40, ("cred.scout", "BLOCK", ""): 85},
    "GUARDRAIL-BYPASS": {("git.normal_after_failure", "ALLOW", ""): 70, ("git.local", "ALLOW", ""): 40,
                         ("git.skip_after_failure", "ALLOW", "named"): 30,
                         ("git.skip_no_failure", "ASK", ""): 20, ("git.skip_after_failure", "ASK", ""): 10, ("git.hook_write_no_failure", "ASK", ""): 8,
                         ("git.skip_after_failure", "BLOCK", ""): 65, ("git.hook_write_after_failure", "BLOCK", ""): 15},
    "EXTERNAL-SHARE": {("share.gist_public", "ALLOW", ""): 30, ("egress.public", "ALLOW", ""): 30, ("egress.bucket_trusted", "ALLOW", ""): 30,
                       ("egress.conf_transport", "ASK", ""): 10, ("egress.conf_trusted_unknown", "ASK", ""): 10,
                       ("share.gist", "BLOCK", ""): 10, ("egress.conf_untrusted", "BLOCK", ""): 10,
                       ("egress.secret", "BLOCK", ""): 10, ("share.gist_secret", "BLOCK", ""): 10},
    "INFERRED-TARGET": {("infer.glob_exact", "ALLOW", ""): 85, ("infer.glob_over", "ASK", ""): 50, ("infer.glob_block", "BLOCK", ""): 15},
}


def cards_for(intent_id, label):
    meta = REGISTRY[intent_id]
    out = [c for c in CARD_IDS if expected_for(meta, cards_mod_card(c))[0] == label]
    return out


_CARD_STUB = {}


def cards_mod_card(card_id):
    """Lever-only card dict (enough for expected_for)."""
    if card_id not in _CARD_STUB:
        lv = cards_mod.LEVERS[card_id]
        _CARD_STUB[card_id] = {"card_id": card_id, "ask_on_soft": lv["ask_on_soft"], "sudo_policy": lv["sudo_policy"],
                               "protected_branches": lv["protected"]}
    return _CARD_STUB[card_id]


def allocate(weights, total):
    """Largest-remainder integer allocation of `total` over `weights` (dict). Deterministic (ties by key)."""
    s = float(sum(weights.values()))
    raw = {k: weights[k] * total / s for k in weights}
    base = {k: int(raw[k]) for k in raw}
    rest = total - sum(base.values())
    for k in sorted(raw, key=lambda k: (-(raw[k] - base[k]), str(k)))[:rest]:
        base[k] += 1
    return base


def _by_label(items):
    d = defaultdict(dict)
    for (iid, lab, tag), w in items.items():
        d[lab][(iid, lab, tag)] = w
    return d


class Cell:
    """One spec family to build."""

    def __init__(self, block, intent, card, label, tag="", sub="", extras=None):
        self.block, self.intent, self.card, self.label, self.tag, self.sub = block, intent, card, label, tag, sub
        self.extras = extras or {}

    def key(self):
        return (self.block, self.intent, self.card, self.tag, self.sub)

    def __repr__(self):
        return "Cell(%s,%s,%s,%s,%s)" % (self.block, self.intent, self.card, self.label, self.tag)


class CardRotor:
    """Greedy card assignment that keeps every card's row count and ALLOW share near the global values."""

    TARGET_ALLOW = 0.51                                  # family ALLOW share (50.98% after the v3.2 substitution)

    def __init__(self, n_cards=8, total=FAMILY_SIZE):
        self.n = Counter()
        self.a = Counter()
        self.per = total / float(n_cards)

    def pick(self, allowed, rows=()):
        """rows: [(label, ...)] the cell will add; choose the allowed card with the least resulting imbalance."""
        k = len(rows)
        na = sum(1 for r in rows if r == "ALLOW")
        best, bl = None, None
        for c in sorted(allowed):
            n, a = self.n[c], self.a[c]
            n2, a2 = n + k, a + na
            loss = ((a2 - self.TARGET_ALLOW * n2) ** 2 - (a - self.TARGET_ALLOW * n) ** 2) + 1.0 * (n2 ** 2 - n ** 2)
            if bl is None or loss < bl:
                best, bl = c, loss
        self.n[best] += k
        self.a[best] += na
        return best


def _spec_cells_from_items(block, items, per_label_totals, rotor, sub="", mult=1, only_cards=None):
    """items: {(intent,label,tag): weight}; per_label_totals: SPEC counts per label."""
    cells = []
    byl = _by_label(items)
    for lab in LABELS:
        if per_label_totals.get(lab, 0) == 0 or lab not in byl:
            continue
        counts = allocate(byl[lab], per_label_totals[lab])
        for (iid, l, tag), n in sorted(counts.items()):
            allowed = list(CARD_IDS) if tag == "named" else cards_for(iid, l)
            if only_cards is not None:
                allowed = [c for c in allowed if c in only_cards]
            if not allowed:
                raise ValueError("no card gives %s label %s" % (iid, l))
            for _ in range(n):
                cells.append(Cell(block, iid, None, l, tag, sub, {"allowed": allowed}))
    return cells


def swap_cells(_unused=None):
    cells = []
    for lever, iid, n, pairs in SWAP_PLAN:
        for i in range(n):
            a, b = pairs[i % len(pairs)]
            la = expected_for(REGISTRY[iid], cards_mod_card(a))[0]
            lb = expected_for(REGISTRY[iid], cards_mod_card(b))[0]
            if la == lb:
                raise ValueError("swap pair %s/%s does not differ for %s" % (a, b, iid))
            if iid == "sudo.unlisted" and (cards_mod_card(a)["ask_on_soft"] or cards_mod_card(b)["ask_on_soft"]):
                raise ValueError("GF5/Q6: an unlisted-program sudo swap pair must sit on two ask_on_soft-OFF cards")
            meta = REGISTRY[iid]
            if lever == "ask_on_soft" and (meta.get("c4") or meta["tier"] == "hard"):
                raise ValueError("Q6: no ask_on_soft swap pair on C4 or a hard row (%s)" % iid)
            cells.append(Cell("A", iid, a, "", "swap", "", {"swap_cards": (a, b), "lever": lever}))
    return cells


def cell_labels(cell):
    """Labels of the rows a cell yields, WITHOUT knowing the card (card-dependent cells carry their label)."""
    if cell.block == "G":
        from .blockg import g_cell_labels
        return g_cell_labels(cell)
    if cell.tag == "swap":
        meta = REGISTRY[cell.intent]
        return [expected_for(meta, cards_mod_card(c))[0] for c in cell.extras["swap_cards"]]
    if cell.tag == "alias":
        return [cell.label, "ALLOW"]
    if cell.tag == "quad4":
        return [cell.label, "ALLOW", cell.label, "ALLOW"]
    if cell.tag == "named":
        out = ["ALLOW"]
    elif cell.block == "B":
        out = [cell.label] * 2
    elif cell.block == "C":
        out = [cell.label, "ALLOW"]
    elif cell.block == "E":
        out = [cell.label] * 3 + ["ALLOW"] if cell.tag == "soft_quad" else [cell.label] * 4
    else:
        out = [cell.label]
    return out * 2 if cell.extras.get("twin") else out


def assign_cards(cells, total=FAMILY_SIZE):
    rotor = CardRotor(total=total)
    for c in cells:
        if c.card is not None:                      # swap cells carry their cards
            for lab, card in zip(cell_labels(c), c.extras["swap_cards"]):
                rotor.n[card] += 1
                rotor.a[card] += 1 if lab == "ALLOW" else 0
    todo = [c for c in cells if c.card is None]
    todo.sort(key=lambda c: (len(c.extras.get("allowed", CARD_IDS)), c.block, c.intent, c.tag))
    for c in todo:
        c.card = rotor.pick(c.extras.get("allowed", CARD_IDS), cell_labels_for_card_choice(c))
    return cells


def cell_labels_for_card_choice(c):
    """Labels used to balance cards BEFORE the card is known: the label signature of the cell (card-dependent members use the cell label)."""
    if c.block == "G":
        # the number of ALLOW members is card independent for every G tag
        n_allow = {"g1f": 1, "g2f": 1, "g1m": 1, "g2m": 1, "g3q": 2, "g4p": 2}[c.extras["g"]]
        n = {"g3q": 4}.get(c.extras["g"], 2)
        return ["ALLOW"] * n_allow + ["BLOCK"] * (n - n_allow)
    return cell_labels(c)


def _mark_twins(cells, n_twin):
    """Mark n_twin of `cells` (same block/sub/label) as view twins, evenly spaced in plan order."""
    n = len(cells)
    for i in range(n_twin):
        cells[int((i + 0.5) * n / n_twin)].extras["twin"] = True


def _twin_totals(rows_by_label, n_cells_total):
    """Spread n_cells_total twin cells over labels proportionally to the label rows."""
    return allocate({k: v for k, v in rows_by_label.items() if v}, n_cells_total)


def _domain_scaled(items, mult):
    """Scale the weights of A_ITEMS per domain (mult: domain -> factor)."""
    return {k: w * mult.get(REGISTRY[k[0]]["domain"], 1.0) for k, w in items.items()}


def _alias_provider():
    try:
        from . import intents_alias, intents_late            # noqa: F401  (written by the alias / late-binding work package)
        return intents_alias, intents_late
    except ImportError:
        return None, None


def plan(alias_late=None, domain_mult=None):
    """All Cells of the family (deterministic). Row-level label counts are checked by plan_stats().
    alias_late: (intents_alias, intents_late) modules; default imports them (None, None) when they do not exist yet."""
    IA, IL = alias_late if alias_late is not None else _alias_provider()
    cells = []
    sw = swap_cells(None)
    cells += sw
    # ---- A : swap (120 rows) + alias (300) + late-binding (60) + plain direct (260). View twins from the plain rows.
    a_plain = {l: A_PARTS["plain"][i] - QUAD_ROWS_A[l] for i, l in enumerate(LABELS)}
    a_plain["ALLOW"] -= sum(M4_CELLS.values())                  # M4 named cells (ladder) are ALLOW rows of the plain budget
    tw = _twin_totals(a_plain, TWIN_CELLS["A"])
    items = _domain_scaled(A_ITEMS, domain_mult or A_DOMAIN_MULT)
    a_cells = _spec_cells_from_items("A", items, {l: a_plain[l] - tw.get(l, 0) for l in LABELS}, None)
    for l in LABELS:
        _mark_twins([c for c in a_cells if c.label == l], tw.get(l, 0))
    cells += a_cells
    for iid, n in sorted(M4_CELLS.items()):
        for _ in range(n):
            cells.append(Cell("A", iid, None, "ALLOW", "" if iid == "infra.own" else "named", "",
                              {"allowed": list(CARD_IDS), "m4_own": iid == "infra.own"}))
    if IA is not None:
        cells += alias_cells(IA)
        cells += late_cells_a(IL)
    # ---- B : spec counts = rows / 2 ; a twin spec has 4 rows
    b_base = {l: BLOCK_ROWS["B"][l] // 2 for l in LABELS}
    tw = _twin_totals(b_base, TWIN_CELLS["B"])
    b_cells = _spec_cells_from_items("B", B_ITEMS, {l: b_base[l] - tw.get(l, 0) for l in LABELS}, None)
    for l in LABELS:
        _mark_twins([c for c in b_cells if c.label == l], tw.get(l, 0))
    cells += b_cells
    # ---- C : executed specs ; the benign twin is built from the executed one ; a twin cell has 4 rows
    c_base = {"ASK": BLOCK_ROWS["C"]["ASK"] - QUAD_ROWS_C["ASK"], "BLOCK": BLOCK_ROWS["C"]["BLOCK"] - QUAD_ROWS_C["BLOCK"]}
    c_base = {l: n for l, n in c_base.items() if n}
    tw = _twin_totals(c_base, TWIN_CELLS["C"])
    c_cells = _spec_cells_from_items("C", C_ITEMS, {l: c_base[l] - tw.get(l, 0) for l in c_base}, None)
    for l in c_base:
        _mark_twins([c for c in c_cells if c.label == l], tw.get(l, 0))
    cells += c_cells
    cells += quad_cells("A", quads_mod.A_QUADS) + quad_cells("C", quads_mod.C_QUADS)
    # ---- D
    for iid, n in sorted(allocate(D_OPAQUE, D_OPAQUE_REGULAR).items()):
        for _ in range(n):
            cells.append(Cell("D", iid, None, "ASK", "opaque"))
    late_wtr = {"ALLOW": 0, "ASK": 0, "BLOCK": 0}
    if IL is not None:
        cells += late_cells_d(IL, late_wtr)
    wtr_allow = BLOCK_ROWS["D"]["ALLOW"] - late_wtr["ALLOW"]
    wtr_block = BLOCK_ROWS["D"]["BLOCK"] - late_wtr["BLOCK"]
    wtr_ask = 20 - late_wtr["ASK"]
    for iid, n in sorted(allocate(D_WTR_ALLOW, wtr_allow).items()):
        for k in range(n):
            cells.append(Cell("D", "wtr." + iid, None, "ALLOW", "ov" if k % 5 == 0 else "", "",
                              {"allowed": cards_for("wtr." + iid, "ALLOW")}))
    for iid, n in sorted(allocate(D_WTR_BLOCK, wtr_block).items()):
        for k in range(n):
            cells.append(Cell("D", "wtr." + iid, None, "BLOCK", "ov" if k % 5 == 0 else "", "",
                              {"allowed": cards_for("wtr." + iid, "BLOCK")}))
    for k in range(wtr_ask):
        cells.append(Cell("D", "wtr.modified", None, "ASK", "modified"))
    # ---- E : quads (4 rows each)
    for iid, n in sorted(E_SOFT_ASKCARD.items()):
        for _ in range(n):
            cells.append(Cell("E", iid, None, "ASK", "soft_quad", "", {"allowed": [c for c in cards_for(iid, "ASK") if c in G_ASK_CARDS]}))
    for iid, n in sorted(E_SOFT_OFFCARD.items()):
        for _ in range(n):
            cells.append(Cell("E", iid, None, "BLOCK", "soft_quad", "", {"allowed": [c for c in cards_for(iid, "BLOCK") if c in G_OFF_CARDS]}))
    for iid, n in sorted(E_HARD.items()):
        for _ in range(n):
            cells.append(Cell("E", iid, None, "BLOCK", "hard_quad", "", {"allowed": cards_for(iid, "BLOCK")}))
    # ---- F : twins spread over (sub-family, label)
    keys = {(sub, l): F_SUB[sub][i] for sub in F_SUB for i, l in enumerate(LABELS)}
    ftw = allocate({k: v for k, v in keys.items() if v}, TWIN_CELLS["F"])
    for sub, items_f in F_ITEMS.items():
        tot = {l: F_SUB[sub][i] - ftw.get((sub, l), 0) for i, l in enumerate(LABELS)}
        f_cells = _spec_cells_from_items("F", items_f, tot, None, sub=sub)
        for l in LABELS:
            _mark_twins([c for c in f_cells if c.label == l], ftw.get((sub, l), 0))
        cells += f_cells
    # ---- G : edit-as-action (1,600 rows)
    from .blockg import make_g_cells
    cells += make_g_cells(Cell)
    attach_ladder(cells)
    assign_cards(cells)
    for i, c in enumerate(cells):
        c.extras["idx"] = i
    return cells


G_ASK_CARDS = tuple(c for c in CARD_IDS if cards_mod.LEVERS[c]["ask_on_soft"])
G_OFF_CARDS = tuple(c for c in CARD_IDS if not cards_mod.LEVERS[c]["ask_on_soft"])
A_DOMAIN_MULT = {}                  # per-domain weight multipliers for the plain direct rows of A (tuned once, see tuning notes in tests)


def quad_cells(block, counts):
    cells = []
    for tpl, n in sorted(counts.items()):
        lab = quads_mod.risk_label(tpl)
        for _ in range(n):
            cells.append(Cell(block, "quad:" + tpl, None, lab, "quad4", "", {"template": tpl,
                                                                              "allowed": list(CARD_IDS) if lab == "ASK" else list(G_OFF_CARDS)}))
    return cells


def alias_cells(IA):
    """150 pairs (6 forms x 25): the dangerous member BLOCK hard / BLOCK soft / ASK per IA.ALIAS_DESIGN (Q10: its reason is the reason of the
    rule that fires on the RESOLVED node: destroy, weaken_security, cross_trust or exfiltrate), the benign member ALLOW. The domain of each
    pair follows the design. A soft BLOCK pair sits on ask_on_soft-OFF cards, a soft ASK pair on ask_on_soft cards."""
    cells = []
    for form in IA.ALIAS_FORMS:
        for e in IA.alias_design(form):
            tag, domain, reason = e["tag"], e["domain"], e["reason"]
            iid = "alias.%s.%s" % (form, IA.ALIAS_REASONS[reason][2])
            if tag == "hard":
                lab, allowed = "BLOCK", list(CARD_IDS)
            elif tag == "soft_block":
                lab, allowed = "BLOCK", list(G_OFF_CARDS)
            else:
                lab, allowed = "ASK", list(G_ASK_CARDS)
            cells.append(Cell("A", iid, None, lab, "alias", "", {"allowed": allowed, "form": form, "severity": "hard" if tag == "hard" else "soft",
                                                                  "domain": domain, "reason": reason, "benign": "alias.%s.benign" % form}))
    return cells


def late_cells_a(IL):
    """60 resolved late-binding rows of block A (LATE_A_SPLIT: per construct ALLOW / ASK / BLOCK)."""
    cells = []
    for construct, (na, nk, nb) in IL.LATE_A_SPLIT.items():
        for lab, n in (("ALLOW", na), ("ASK", nk), ("BLOCK", nb)):
            keep = IL.LATE_KEEP_DESTROY.get(("A", lab), n)
            for k in range(n):
                iid = "late.%s.%s" % (construct, lab.lower() if k < keep else IL.VARIANT_OF_LABEL[lab])
                cells.append(Cell("A", iid, None, lab, "late", "", {"allowed": cards_for(iid, lab)}))
    return cells


def late_cells_d(IL, tally):
    """90 late-binding rows of block D: 35 opaque (ONE construct type, all ASK / none / na) and 55 write-then-run (LATE_D_WTR_SPLIT)."""
    cells = []
    for _ in range(IL.LATE_D_OPAQUE):
        cells.append(Cell("D", "late.%s.opaque" % IL.LATE_D_OPAQUE_CONSTRUCT, None, "ASK", "opaque"))
    for construct, (na, nk, nb) in IL.LATE_D_WTR_SPLIT.items():
        for lab, n in (("ALLOW", na), ("ASK", nk), ("BLOCK", nb)):
            keep = IL.LATE_KEEP_DESTROY.get(("D", lab), n)
            for k in range(n):
                iid = "late.%s.wtr_%s" % (construct, lab.lower() if k < keep else IL.VARIANT_OF_LABEL[lab])
                cells.append(Cell("D", iid, None, lab, "late_wtr", "", {"allowed": cards_for(iid, lab)}))
                tally[lab] += 1
    return cells


M5_CYCLE = (2, 3, 4, 2, 3, 4, 2, 3, 4, 2)                  # obfuscated-rendering level targets of block B specs (40 / 30 / 30 %)
M4_CELLS = {"infra.own": 12, "infra.shared": 12, "infra.production": 24}          # ladder M4 (benign dual-use in production lanes): consent-twin ALLOW rows


def attach_ladder(cells):
    """Program-set ladder parameters carried by plan cells: M1 (scope inversion: INFERRED-TARGET rows) and M4 (benign dual-use in
    production lanes). M2, M3, M5 levels are set when the rows exist (ladder.py / generator). The ladder never sets a label."""
    n1 = 0
    prod = 0
    own = 0
    nb = 0
    for c in cells:
        if c.block == "B":
            c.extras["m5"] = M5_CYCLE[nb % len(M5_CYCLE)]
            nb += 1
        if c.block == "F" and c.sub == "INFERRED-TARGET":
            lvl = 1 + (n1 % 4)
            n1 += 1
            c.extras["v"] = {"level": lvl}
            c.extras["ladder"] = {"mechanism": "M1", "level": lvl}
        elif c.block == "A" and c.tag == "named" and c.intent == "infra.shared":
            c.extras["v"] = {"prog": "kubectl", "op": ["scale", "modify"][prod % 2]}
            c.extras["ladder"] = {"mechanism": "M4", "level": 2}
            prod += 1
        elif c.block == "A" and c.tag == "named" and c.intent == "infra.production":
            lvl = 3 if own % 2 == 0 else 4
            c.extras["v"] = {"prog": "kubectl", "op": ("scale" if own % 4 == 0 else "modify") if lvl == 3 else "delete"}
            c.extras["ladder"] = {"mechanism": "M4", "level": lvl}
            own += 1
    for c in cells:
        if c.extras.get("m4_own"):
            c.extras["ladder"] = {"mechanism": "M4", "level": 1}
    return cells


ROWS_PER_CELL = {"A": 1, "B": 2, "C": 2, "D": 1, "E": 4, "F": 1}


def cell_rows(cell):
    """[(label, reason, tier, intent, card)] for every ROW this cell produces (design expectations)."""
    if cell.block == "G":
        from .blockg import g_cell_rows
        return g_cell_rows(cell)
    if cell.tag == "quad4":
        rows = []
        for (surf, risk), (iid, _v) in quads_mod.TEMPLATES[cell.extras["template"]].items():
            if cell.block == "C" and risk == "resolved":
                rows.append(("ALLOW", "none", "na", quads_mod.TEMPLATES[cell.extras["template"]][(surf, "present")][0] + "#benign", cell.card))
                continue
            l, r, t = expected_for(REGISTRY[iid], cards_mod_card(cell.card))
            rows.append((l, r, t, iid, cell.card))
        return rows
    meta = REGISTRY[cell.intent]
    if cell.tag == "swap":
        out = []
        for card in cell.extras["swap_cards"]:
            l, r, t = expected_for(meta, cards_mod_card(card))
            out.append((l, r, t, cell.intent, card))
        return out
    l, r, t = expected_for(meta, cards_mod_card(cell.card))
    if cell.tag == "alias":
        dom = "@" + cell.extras["domain"]
        return [(l, r, t, cell.intent + dom, cell.card), ("ALLOW", "none", "na", cell.extras["benign"] + dom, cell.card)]
    if cell.tag == "named":
        rows = [("ALLOW", "none", "soft", cell.intent, cell.card)]
    elif cell.block == "B":
        rows = [(l, r, t, cell.intent, cell.card)] * 2
    elif cell.block == "C":
        rows = [(l, r, t, cell.intent, cell.card), ("ALLOW", "none", "na", cell.intent + "#benign", cell.card)]
    elif cell.block == "E":
        if cell.tag == "soft_quad":
            rows = [(l, r, t, cell.intent, cell.card)] * 3 + [("ALLOW", "none", "soft", cell.intent, cell.card)]
        else:
            rows = [(l, r, t, cell.intent, cell.card)] * 4
    else:
        rows = [(l, r, t, cell.intent, cell.card)]
    return rows * 2 if cell.extras.get("twin") else rows


def row_meta(iid):
    """domain and main program of the intent behind a row (G rows carry 'G:<effect id>')."""
    if iid.startswith("G:"):
        from .blockg import g_row_meta
        return g_row_meta(iid[2:])
    base = iid.split("#")[0]
    dom = None
    if "@" in base:
        base, dom = base.split("@", 1)
    meta = dict(REGISTRY[base])
    if dom:
        meta["domain"] = dom
    elif meta["domain"] == "late":                  # late-binding rows: the final command is rm (BLOCK) / git (ASK) / git or pip (ALLOW); plan-level estimate
        meta["domain"] = {"BLOCK": "fs", "ASK": "git", "ALLOW": "git"}[meta["label"]]
    return meta


def plan_stats(cells=None):
    cells = cells if cells is not None else plan()
    rows = [(c, r) for c in cells for r in cell_rows(c)]
    st = {"rows": len(rows), "by_block_label": defaultdict(Counter), "reason": Counter(), "tier": Counter(),
          "domain_A": Counter(), "program": Counter(), "card_allow": defaultdict(Counter), "label": Counter(),
          "domain_all": defaultdict(Counter)}
    for c, (l, r, t, iid, card) in rows:
        meta = row_meta(iid)
        st["by_block_label"][c.block][l] += 1
        st["label"][l] += 1
        st["card_allow"][card][l] += 1
        st["tier"][t] += 1
        if l != "ALLOW":
            st["reason"][r] += 1
        if c.block == "A":
            st["domain_A"][meta["domain"]] += 1
        st["domain_all"][meta["domain"]][l] += 1
        st["program"][meta["prog"]] += 1
    return st, cells
