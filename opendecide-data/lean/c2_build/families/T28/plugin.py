"""families/T28/plugin.py: T28 permission verdicts from precedence rules (allow / ask / deny), a C2 family plugin.

Semantics: G0_SPEC.md (frozen; sha in T28Plugin.G0_SHA256). The card lists 3-8 permission rules (effect, tool pattern,
0-2 argument conditions), states the glob semantics, the precedence policy (P1-P5, a lexicon clause of kind
"precedence"), the default verdict for no match and the closed-world sentence. The state shows one proposed tool call;
on inverted rows the state lists the candidate calls ("Calls to review:") and the options are the labels "Call i".

  solver A   rule AST (c2_kit.rules: Rule / RuleSet over Glob / Cmp / And nodes; glob_a token matcher) run by
             rules.resolve under the card's policy                                           paradigm ast_interpreter
  solver B   solver_b.py: its own parser of the RENDERED row (regexes, json, yaml), a match table built with compiled
             regular expressions (glob_b) and integer-cents sign tests, precedence by sort keys  paradigm regex_compile
  plan       _plan_call / _predict below: a third, direct matcher (glob_a + plain comparisons + a separately written
             precedence loop). It never sets a gold: it drives the error-model distractors, the inverted candidates,
             the minimal-edit twin predictions (G-TW checks them against solver A) and the trap tags
  samplers   S1 forward (rule list); S2 label-first (decisive rule + 1-2 near-miss rules); S3 settings-file-first
             (YAML / JSON); S4 admin memo + agent transcript; S5 held out (statement JSON + IT chat thread)
  questions  ch_verdict (3-way, 16/40), yes/no on allow / deny / ask (18/40; complements: syntactic, option framing,
             antonym; yn_mustnot carries the double negation), ch_rule (which rule decides, 4/40), ch_inverted (which
             call runs without asking, 2/40, deep)
  relations  complement (yes/no), minimal-edit twin (one slot; prediction from the plan), equiv (another policy
             format + another skin), inv (one attack line), G4 metamorphic (rename people / namespace / domain,
             shuffle under order-free policies, add an inert rule, move the amount across a threshold)
Built-in packs (PACKS) are Claude-written stand-ins for the Haiku pack pool (A37 f: no pool before A38). They live
in memory only; the real pool replaces them through T28Plugin(packs=...).

Stage B fix iteration 1 (14 Oct 2026; G0 v1.2 section 10, PILOT_REPORT of pilot/ and pilot_i1/):
  cards      the rules print once: row.card on a yes/no row, the head of the instructions on a choice row (kit cards:
             place_rules); two styles, full 85% / short 15% (card_style, _card_tpl); solver B reads both
  balance    yes/no targets by the g index (consecutive yes/no slots have opposite targets); overlay partners, twin
             targets and the mask draw hashed per slot group (_group_key), so the yes rate and the verdict thirds are exact
  plans      ch_rule: n and the default option's gold outcome drawn from the row key (_rule_plan, 1/k); ch_inverted: k
             drawn from the key, the candidate calls listed in the state and the options "Call i" (no option text
             carries the call: the Stage B / 5,000-row G6 finding, section 10); twin targets (_twin_want)
  deals      cards = (sampler, pack) over circular pack windows (_pack_pool); registers and skins dealt (_deal_skin)
  polarity   wording polarity rule R2 (POLARITY_*; ctx_for screens the pool; quarantined_wordings)
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path

from c2_kit import cards as CARDS
from c2_kit import glob_a
from c2_kit import polarity as POL
from c2_kit import rules as RL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import plan_choice
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.globsem import GlobSem
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "T28"

# ------------------------------------------------------------------------------------------------ closed sets
EFFECTS = ("allow", "ask", "deny")                       # card and option order
EFFECT_ORDER = ("deny", "ask", "allow")                  # P1, and the P3 tie-break: strongest first
RANK = {e: i for i, e in enumerate(EFFECT_ORDER)}
EFFECT_SET = {e: [e] for e in EFFECTS}
ENV_SET = {"prod": ["production"], "staging": ["staging"], "dev": ["development"]}
OWNER_SET = {"self": ["self", "the requesting user"], "other": ["other", "someone else"]}
ROLE_SET = {"maintainer": ["maintainer"], "analyst": ["analyst"], "contractor": ["contractor"],
            "auditor": ["auditor"]}
CAT_SETS = {"env": ENV_SET, "owner": OWNER_SET, "role": ROLE_SET}
ARG_KINDS = ("recipient", "path", "amount", "owner", "env")        # call argument order
ARG_NAME = {"recipient": "to", "path": "path", "amount": "amount", "owner": "owner", "env": "env"}
SUFFIX = {"recipient": "TO", "path": "PATH", "amount": "AMT", "owner": "OWNER", "env": "ENV", "role": "ROLE"}
PIN = {"recipient": ":raw", "path": ":raw", "amount": "", "owner": ":s0", "env": "", "role": ""}
POLICY_IDS = ("P1", "P2", "P3", "P4", "P5")
POLICIES = {"P1": "effect_order", "P2": "first_match", "P3": "most_specific", "P4": "last_match",
            "P5": "priority_list"}
PREC_SEM = {p: f"prec.{p}" for p in POLICY_IDS}
CMPS = ("cmp.le", "cmp.lt", "cmp.ge", "cmp.gt")
CMP_OP = {"cmp.le": "<=", "cmp.lt": "<", "cmp.ge": ">=", "cmp.gt": ">"}
DROP_INCL = {"cmp.le": "cmp.lt", "cmp.ge": "cmp.gt"}
ADD_EXCL = {"cmp.lt": "cmp.le", "cmp.gt": "cmp.ge"}
GLOB_SEMS = {"noslash": GlobSem(star_crosses_slash=False, question_mark=False),
             "slash": GlobSem(star_crosses_slash=True, question_mark=False),
             "dstar": GlobSem(star_crosses_slash=False, question_mark=False, double_star=True)}
GLOB_DRAW = ("noslash", "noslash", "slash", "dstar")
THRESHOLDS = (2500, 5000, 10000, 20000, 25000, 50000, 100000, 150000, 250000)
USERS = ("Dana Okafor", "Lee Park", "Mira Castell", "Tomas Ferreira", "Aiko Brandt", "Ravi Anand", "Noor Haddad",
         "Sam Whitlock")
AGENTS = ("Relay", "Juniper", "Beacon", "Courier", "Atlas Desk", "Harbor Assistant")
SPARE_NS = ("zephyr", "orchard", "quarry", "lantern")
CODE_WORDS = ("Kestrel", "Marlin", "Quokka", "Heron", "Lynx", "Otter")
VERDICT_TEXT = {"allow": "Allow", "ask": "Ask the user first", "deny": "Deny"}
DEFAULT_OPTION = "No rule applies (the default verdict is used)"

# ------------------------------------------------------------------------------------------------ question forms
QFORM_SLOTS = (("ch_verdict",) * 16 + ("yn_allow",) * 8 + ("yn_allow_syn",) + ("yn_deny",) * 3 + ("yn_deny_syn",)
               + ("yn_ask",) * 3 + ("yn_mustnot",) * 2 + ("ch_rule",) * 4 + ("ch_inverted",) * 2)
YN = {"yn_allow": ("allow", 1), "yn_allow_syn": ("allow", -1), "yn_allow_opt": ("allow", -1),
      "yn_deny": ("deny", 1), "yn_deny_syn": ("deny", -1), "yn_deny_ant": ("deny", -1),
      "yn_ask": ("ask", 1), "yn_ask_opt": ("ask", -1),
      "yn_mustnot": ("deny", 1), "yn_mustnot_syn": ("deny", -1)}
# G0 v1.2 section 2 (balance by seed arithmetic): j = the slot's index among the block's slots of its form (verdict
# rows); g = its index among ALL the block's yes/no slots (yes/no rows), so consecutive yes/no slots (2m, 2m + 1) have
# opposite targets and a block holds exactly 9 yes and 9 no targets. Overlay partners (complement, twin, equiv, inv)
# are drawn per GROUP of slots (pairs of yes/no slots, triples of verdict slots; _group_key), so each group's
# partners cancel: the family's yes rate and verdict thirds are exact before drops.
SLOT_J = tuple(QFORM_SLOTS[:i].count(q) for i, q in enumerate(QFORM_SLOTS))
SLOT_G = tuple(sum(1 for x in QFORM_SLOTS[:i] if x in YN) for i in range(len(QFORM_SLOTS)))
COMPLEMENT_PARTNERS = {"yn_allow": ("yn_allow_syn", "yn_allow_opt"), "yn_allow_syn": ("yn_allow",),
                       "yn_deny": ("yn_deny_syn", "yn_deny_ant"), "yn_deny_syn": ("yn_deny",),
                       "yn_ask": ("yn_ask_opt",), "yn_mustnot": ("yn_mustnot_syn",)}
P_COMPLEMENT = 0.45
P_EQUIV = 0.13
P_INV = 0.10
P_TWIN = 0.42
P_DEFAULT = 0.15
P_MASKED = 0.16
INVERTED_K = (3, 4, 4, 5)                  # ch_inverted candidate counts (drawn from the row key, never from the structure)
CALLS_HEAD = "Calls to review:"            # G0 v1.2 S20: the state lists the candidate calls; the options are "Call i"

# ------------------------------------------------------------------------------------------------ program text
MATCH_LINE = ("How to read the policy: a rule applies to a call when its tool pattern matches the tool name and every "
              "condition listed with the rule holds for the call. A condition about an argument or a session role "
              "that the call does not include does not hold.")
SPEC_LINE = {
    "tool_first": ("Specificity: compare the tool patterns first (an exact tool name is more specific than a "
                   "namespace pattern such as ns.*, which is more specific than *); if they tie, the rule with more "
                   "conditions is more specific. If two applicable rules are equally specific, deny beats ask and "
                   "ask beats allow."),
    "conds_first": ("Specificity: compare the number of conditions first (more conditions is more specific); if they "
                    "tie, an exact tool name is more specific than a namespace pattern such as ns.*, which is more "
                    "specific than *. If two applicable rules are equally specific, deny beats ask and ask beats "
                    "allow."),
}
VERDICT_LINE = ("Verdicts: allow = the agent makes the call without asking; ask = the agent asks the user and makes "
                "the call only after the user confirms; deny = the agent does not make the call.")
CLOSED_WORLD = "The listed permission rules are complete: no other rule, exception or standing permission applies."
OWNER_LINE = ('Owner values: an owner argument names who owns the item the call acts on; "self" (the requesting '
              'user) is the user the agent works for, and "other" (someone else) is anyone else.')
LITERAL_LINE = "Every other character in a pattern matches only itself."      # G0 S4 (Haiku pass H3)
PRIORITY_HEAD = "Priority list, highest priority first: "                      # G0 S12 (Haiku pass H25)
# The short definition style (G0 v1.2 section 4, spec 3.0 "a short or no card on about 15% of rows"): the same rules in
# fewer words. Lines that carry the glob semantics, the precedence clause, the default, the codes and the closed-world
# sentence stay verbatim; c2_kit.cards.variant_problems checks every pair (slots, quoted literals, numbers, operator
# words and the negation count k_all are the same; test_fix_i1.py::test_short_card_lines_keep_the_rules).
MATCH_SHORT = ("A rule applies when its tool pattern matches the tool name and every condition listed with it holds; "
               "a condition about an argument or session role that the call does not include does not hold.")
SPEC_SHORT = {
    "tool_first": ("Specificity: compare tool patterns first (an exact tool name beats a namespace pattern such as "
                   "ns.*, which beats *); if they tie, more conditions is more specific. If two applicable rules are "
                   "equally specific, deny beats ask and ask beats allow."),
    "conds_first": ("Specificity: compare the number of conditions first (more is more specific); if they tie, an "
                    "exact tool name beats a namespace pattern such as ns.*, which beats *. If two applicable rules "
                    "are equally specific, deny beats ask and ask beats allow."),
}
VERDICT_SHORT = ("Verdicts: allow = make the call without asking; ask = ask the user, then make the call only after "
                 "the user confirms; deny = do not make the call.")
OWNER_SHORT = ('Owner values: an owner argument names who owns the item the call acts on; "self" is the requesting '
               'user, the user the agent works for; "other" is someone else.')
CARD_STYLES = ("full", "short")
CARD_SHARES = {"full": 0.85, "short": 0.15}          # cards.draw_style from the row's seed and sampler (label-blind)
CHAT_PREFIX = "[agent] proposes "                                              # G0 section 4 (Haiku pass H11)
NOTE_PREFIX = "Tool output note: "
LAYOUT = {"S1": ("narrative", "policy", "call"), "S2": ("narrative", "call", "policy"),
          "S3": ("policy", "narrative", "call"), "S4": ("policy", "narrative", "call"),
          "S5": ("narrative", "policy", "call")}
SAMPLER_CFG = {
    "S1": dict(n=(3, 8), policy=("list",), call=("json", "func", "cli"), near=(0, 1, 1, 2)),
    "S2": dict(n=(3, 6), policy=("list",), call=("json", "func", "cli"), near=(1, 2)),
    "S3": dict(n=(4, 8), policy=("yaml", "json"), call=("json", "func", "cli"), near=(0, 1, 1, 2)),
    "S4": dict(n=(3, 6), policy=("memo",), call=("transcript",), near=(0, 1, 1, 2)),
    "S5": dict(n=(3, 8), policy=("statements",), call=("chat",), near=(0, 1, 1, 2)),
}
EQUIV_POLICY_STYLES = ("list", "yaml", "json", "memo")
PLAIN_CALL_STYLES = ("json", "func", "cli")

# ------------------------------------------------------------------------------------------------ built-in packs
# Claude-written stand-ins for the Haiku pack pool (40+ packs after A38). A pack: org label (domains are
# <org>.example, eu.<org>.example; near misses <org>.test and <org>-mail.example), a partner and an outside label,
# recipient local parts, path roots with their near-miss roots, sub-folders, file names, and namespaces of tools,
# each tool with its argument kinds (closed set ARG_KINDS). A pack marked held_out feeds S5 (mixdev) only.
PACKS = (
    {"id": "pk-northwind", "org": "northwind", "partner": "brightpath", "outside": "mailhub",
     "locals": ("dana", "ops", "billing", "lee"),
     "roots": {"/data/prod": "/data/production", "/srv/reports": "/srv/reports-old",
               "/home/shared": "/home/shared-archive"},
     "subdirs": ("2026", "archive"), "files": ("q3.csv", "summary.txt", "ledger.db"),
     "ns": {"mail": {"send": ("recipient",), "draft": ("recipient",), "read": ()},
            "payments": {"transfer": ("recipient", "amount"), "refund": ("amount",),
                         "invoice": ("recipient", "amount")},
            "files": {"read": ("path", "owner"), "write": ("path", "owner"), "delete": ("path", "owner"),
                      "share": ("path", "recipient")},
            "db": {"query": ("env",), "migrate": ("env",), "drop_table": ("env", "owner")}}},
    {"id": "pk-harborline", "org": "harborline", "partner": "keelstone", "outside": "postbox",
     "locals": ("sam", "accounts", "support", "noor"),
     "roots": {"/srv/exports": "/srv/exports-old", "/data/live": "/data/lively", "/var/backups": "/var/backups2"},
     "subdirs": ("2025", "tmp"), "files": ("orders.csv", "notes.md", "dump.sql"),
     "ns": {"inbox": {"send": ("recipient",), "reply": ("recipient",), "archive": ()},
            "billing": {"charge": ("amount",), "payout": ("recipient", "amount"), "credit": ("amount",)},
            "storage": {"get": ("path", "owner"), "put": ("path", "owner"), "purge": ("path", "owner")},
            "deploy": {"release": ("env",), "rollback": ("env",), "scale": ("env",)}}},
    {"id": "pk-quillstone", "org": "quillstone", "partner": "fernbank", "outside": "relaymail",
     "locals": ("ravi", "team", "finance", "mira"),
     "roots": {"/docs/legal": "/docs/legal-drafts", "/data/crm": "/data/crm2", "/home/projects": "/home/projects-old"},
     "subdirs": ("drafts", "2026"), "files": ("contract.pdf", "contacts.csv", "plan.md"),
     "ns": {"crm": {"export": ("recipient",), "update": ("owner", "env"), "merge": ("owner",)},
            "ledger": {"post": ("amount",), "transfer": ("recipient", "amount"), "reverse": ("amount",)},
            "docs": {"open": ("path",), "edit": ("path", "owner"), "publish": ("path", "recipient")}}},
    {"id": "pk-tidewater", "org": "tidewater", "partner": "saltmarsh", "outside": "outbound",
     "locals": ("aiko", "oncall", "treasury", "tomas"),
     "roots": {"/vault/keys": "/vault/keys-backup", "/srv/payroll": "/srv/payroll-test",
               "/data/ops": "/data/operations"},
     "subdirs": ("archive", "current"), "files": ("batch.csv", "keys.json", "roster.txt"),
     "ns": {"notify": {"email": ("recipient",), "page": ("recipient",)},
            "treasury": {"wire": ("recipient", "amount"), "sweep": ("amount",)},
            "vault": {"read": ("path", "owner"), "shred": ("path", "owner")},
            "cluster": {"restart": ("env",), "drain": ("env",)}}},
    {"id": "pk-alderbank", "org": "alderbank", "partner": "millrace", "outside": "fastpost",
     "locals": ("lee", "claims", "helpdesk", "ana"),
     "roots": {"/backups/db": "/backups/db-old", "/srv/claims": "/srv/claims2", "/home/team": "/home/teams"},
     "subdirs": ("weekly", "2026"), "files": ("claims.csv", "snapshot.tar", "readme.md"),
     "ns": {"chat": {"post": ("recipient",), "dm": ("recipient",)},
            "expenses": {"reimburse": ("recipient", "amount"), "file_claim": ("amount",)},
            "backups": {"restore": ("path", "env"), "prune": ("path", "env")},
            "warehouse": {"query": ("env",), "truncate": ("env", "owner")}}},
    {"id": "pk-fernlake", "org": "fernlake", "partner": "copperleaf", "outside": "mailgate", "held_out": True,
     "locals": ("jo", "events", "shop", "kim"),
     "roots": {"/repo/main": "/repo/mainline", "/data/shop": "/data/shop-staging", "/srv/media": "/srv/media-old"},
     "subdirs": ("assets", "2026"), "files": ("index.html", "prices.csv", "logo.png"),
     "ns": {"calendar": {"invite": ("recipient",), "cancel": ("owner",)},
            "shop": {"order": ("amount",), "refund": ("recipient", "amount")},
            "repo": {"push": ("path", "env"), "delete_branch": ("path", "owner")},
            "secrets": {"rotate": ("env",), "export": ("recipient", "env")}}},
)

# ------------------------------------------------------------------------------------------------ error-model names
T28_MODELS = {
    "t28_ask_as_allow": "collapses the ask tier into allow (reads 'ask the user' as permission)",
    "t28_ask_as_deny": "collapses the ask tier into deny",
    "t28_default_deny": "falls back to refusing the call when no rule is read as applying",
    "t28_star_slash_flip": "reads '*' as crossing '/' when the card says it does not, or the reverse",
    "t28_near_miss_match": ("treats a near-miss string as a match: a folder pattern as a plain text prefix "
                            "(/data/prod/* covering /data/production/...), *@<org>.example as covering <org>.test, "
                            "<org>-mail.example or a sub-domain"),
    "t28_lowest_rule_number": "reads 'listed first / last' as the lowest / highest rule number",
    "t28_specificity_order_swap": "compares the two specificity components in the other order",
    "t28_priority_reversed": "reads the priority list from the bottom up",
}
for _n, _d in T28_MODELS.items():
    register_name(_n, _d)

MODEL_VARIANTS = (
    ("first_match", dict(policy="P2")),
    ("last_match", dict(policy="P4")),
    ("effect_order", dict(policy="P1")),
    ("most_specific", dict(policy="P3", spec_order="tool_first")),
    ("ignore_arguments", dict(ignore_conds=True)),
    ("default_allow", dict(default="allow")),
    ("drop_inclusive_endpoint", dict(cmp_map=DROP_INCL)),
    ("add_exclusive_endpoint", dict(cmp_map=ADD_EXCL)),
    ("t28_ask_as_allow", dict(post=("ask", "allow"))),
    ("t28_ask_as_deny", dict(post=("ask", "deny"))),
    ("t28_default_deny", dict(default="deny")),
    ("t28_star_slash_flip", dict(flip_slash=True)),
    ("t28_near_miss_match", dict(loose=True)),
    ("t28_lowest_rule_number", dict(lowest_id=True)),
    ("t28_specificity_order_swap", dict(swap_order=True)),
    ("t28_priority_reversed", dict(reverse_priority=True)),
)


# ------------------------------------------------------------------------------------------------ helpers
@dataclass
class _Call:
    tool: str
    args: dict
    role: str | None = None

    def as_dict(self) -> dict:
        return {"tool": self.tool, "args": dict(self.args), "role": self.role}


@dataclass
class _Cond:
    kind: str
    value: object               # pattern | category key | (cmp sem, threshold cents)


@dataclass
class _Rule:
    effect: str
    tool: str
    conds: list = field(default_factory=list)


def call_key(call: dict) -> str:
    """Canonical key of a call (choice key of inverted options)."""
    return json.dumps({"tool": call["tool"], "args": call["args"], "role": call["role"]}, sort_keys=True)


def _policy(env: dict) -> str:
    return env["PREC"].split(".", 1)[1]


def _tool_rank(pat: str) -> int:
    if pat == "*":
        return 0
    if pat.endswith(".*") and pat.count("*") == 1:
        return 1
    if "*" not in pat:
        return 2
    raise ContractError(f"tool pattern {pat!r} is not exact, ns.* or *")


def _cmp_holds(sem: str, amount: int, bound: int) -> bool:
    return {"cmp.le": amount <= bound, "cmp.lt": amount < bound, "cmp.ge": amount >= bound,
            "cmp.gt": amount > bound}[sem]


def _answer(qform: str, effect: str):
    if qform == "ch_verdict":
        return effect
    pred, pol = YN[qform]
    return int((effect == pred) == (pol == 1))


def _domains(pack: dict) -> dict:
    o = pack["org"]
    return {"internal": f"{o}.example", "sub": f"eu.{o}.example", "partner": f"{pack['partner']}.example",
            "outside": f"{pack['outside']}.test", "nm_tld": f"{o}.test", "nm_hyphen": f"{o}-mail.example"}


def _org_label(domain: str) -> str | None:
    labels = domain.split(".")
    return labels[-2].split("-")[0] if len(labels) >= 2 else None


def _loose_rcpt(pat: str, addr: str) -> bool:
    """The near_miss_match reading of a recipient pattern."""
    if "@" not in pat or "@" not in addr:
        return False
    pl, pd = pat.split("@", 1)
    al, ad = addr.split("@", 1)
    if pl != "*" and pl != al:
        return False
    pd = pd[2:] if pd.startswith("*.") else pd
    if "." not in pd:
        return False
    return ad.endswith(pd) or (_org_label(pd) is not None and _org_label(pd) == _org_label(ad))


def _loose_path(pat: str, path: str, gsem: GlobSem) -> bool:
    """The near_miss_match reading of a path pattern: its folder is read as a plain text prefix, so a sibling folder
    whose name merely starts with it (/data/prod/* vs /data/production/q3.csv) is taken as the same folder."""
    if "*" not in pat:
        return False
    lit = pat[:pat.index("*")]
    if not lit.endswith("/") or len(lit) < 2:
        return False
    folder = lit[:-1]
    if not path.startswith(folder) or path.startswith(lit):
        return False
    rest = path[len(folder):]
    cut = rest.find("/")
    if cut <= 0:
        return False
    return glob_a.match(pat, lit + rest[cut + 1:], gsem)


def _loose(kind: str, pat: str, val: str, gsem: GlobSem) -> bool:
    return _loose_rcpt(pat, val) if kind == "recipient" else _loose_path(pat, val, gsem)


def _target(qform: str, b: int, j: int):
    """Balance by construction: the intended verdict from the seed block b and the slot's index j (label-first,
    display-blind): among the block's slots of the same question form for the verdict forms, among ALL the block's
    yes/no slots for the yes/no forms (G0 v1.2 section 2). Verdicts rotate within a block and across the blocks of one
    policy; yes / no alternate within a block (opposite targets for slots 2m and 2m + 1) and flip between blocks."""
    if qform == "ch_verdict":
        return EFFECTS[(j + b) % 3]
    if qform in YN:
        eff, pol = YN[qform]
        yes = (j + b) % 2 == 0
        if yes == (pol == 1):
            return eff
        others = [e for e in EFFECTS if e != eff]
        return others[((j + b) // 2 + b // 5) % 2]
    if qform == "ch_inverted":
        return "allow"
    return None


def _flip_sem(g: GlobSem) -> GlobSem:
    return GlobSem(star_crosses_slash=not g.star_crosses_slash, anchored=g.anchored, dollar_end=g.dollar_end,
                   question_mark=g.question_mark, double_star=g.double_star, case_sensitive=g.case_sensitive)


# Wording polarity (c2_kit.polarity P1-P4; opt in): the words that would invert a T28 yes/no wording and that
# negcount's closed lexicon does not list: ban words. They never belong to a T28 positive phrasing (G0 section 3: a
# refusal verb for yn_deny, "must not" + a verb of making for yn_mustnot), so a wording that uses one next to a
# syntactic negation ("not barred", "must not ... a flat ban") has two negation layers the form does not declare.
NEGATIVE_PREDICATES = (
    r"off-limits", r"forbidden", r"forbids?", r"banned?", r"bans?", r"barred?", r"bars", r"prohibited", r"prohibits?",
    r"blocked", r"blocks?", r"withheld", r"withholds?",
)


# ------------------------------------------------------------------------------------------------ the plugin
class T28Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "4acd590fd867ae578290226e3198c36711815982f909020b4485b2db4cf11b9d"   # G0 v1.2 (14 Oct 2026; section 10)
    # the G0 the Haiku task files and the frozen pools_v2 were authored under (v1.1 13 Oct, R1; v1 bc3d69cd...):
    # G0_SPEC.v1_1.md is its byte-exact copy, which build_redo2 / build_redo3 / freeze_v2 rebuild from
    G0_SHA256_AUTHORED = "9ec78109c7448f7bad538a0bb7e3e716fbff5a77f54d02ec7d38ebe81c1081ec"
    # the Haiku G0-lite ambiguity pass this freeze resolves (workflow c2-data-stage-a, Ambiguity phase)
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T28"
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "ast_interpreter"
    PARADIGM_B = "regex_compile"
    SOLVER_B_MODULE = "families.T28.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("ch_verdict", "choice", answer_set="closed"),
        QuestionForm("ch_rule", "choice", answer_set="closed"),
        QuestionForm("ch_inverted", "choice", answer_set="closed"),
        QuestionForm("yn_allow", "noul", "verdict_allow", 1, yes_is_bad=False),
        QuestionForm("yn_allow_syn", "noul", "verdict_allow", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_allow_opt", "noul", "verdict_allow", -1, "option_framing", yes_is_bad=True),
        QuestionForm("yn_deny", "noul", "verdict_deny", 1, yes_is_bad=True),
        QuestionForm("yn_deny_syn", "noul", "verdict_deny", -1, "syntactic", yes_is_bad=False),
        QuestionForm("yn_deny_ant", "noul", "verdict_deny", -1, "antonym", yes_is_bad=False),
        QuestionForm("yn_ask", "noul", "verdict_ask", 1, yes_is_bad=True),
        QuestionForm("yn_ask_opt", "noul", "verdict_ask", -1, "option_framing", yes_is_bad=False),
        QuestionForm("yn_mustnot", "noul", "verdict_deny_neg", 1, yes_is_bad=True),
        QuestionForm("yn_mustnot_syn", "noul", "verdict_deny_neg", -1, "syntactic", yes_is_bad=False),
    )}
    # gold-label words plus the permission-claim words of G0 section 9 (H39): G-SL drops any skin or Mode F memo that
    # holds one, and the authoring prompts never contain them (chunker forbid_strings)
    LABEL_WORDS = ("allow", "ask", "deny", "refuse", "permit", "reject", "block", "confirm", "ask the user first",
                   "run the call", "without asking", "approve", "approval", "authorize", "authorise",
                   "authorization", "authorisation", "permission", "consent", "cleared", "clearance")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "chat", "ticket", "email", "json", "yaml", "log", "transcript", "it_chat", "runbook")
    HELD_OUT_REGISTERS = ("it_chat", "runbook")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW: tuple = ()
    # wording polarity (G0 v1.2 section 3, R2): ban words next to a syntactic negation are refused (P1); yn_mustnot
    # carries the one negation of "must not" in its positive phrasing (POLARITY_BASE); yn_deny_ant says "may / can"
    # (an antonym word, no negation) and is exempt; option-framing forms are exempt by the kit. Strict frames stay off:
    # "Is the agent not free to ...?" is a plain negation of the predicate in T28 (lead ruling, section 3 R2)
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_BASE = {"verdict_deny_neg": 1}
    POLARITY_STRICT_FRAMES = False
    POLARITY_SKIP = ("yn_deny_ant",)

    def __init__(self, lexicon=None, packs=None):
        super().__init__(lexicon)
        self.packs = tuple(sorted(packs or PACKS, key=lambda p: p["id"]))
        self._pack_by_id = {p["id"]: p for p in self.packs}
        self._train_packs = tuple(p for p in self.packs if not p.get("held_out"))
        self._dev_packs = tuple(p for p in self.packs if p.get("held_out")) or self._train_packs
        if not self._train_packs:
            raise ContractError("T28 needs at least one training pack")
        self._screened: list = []                      # (ctx, ctx without the failing wordings, {skin id: problems})
        self._skin_index: list = []                    # (ctx, {(held_out, register): [skins by id]})

    # ------------------------------------------------------------------------------------------- lexicon
    def _admitted(self, sem: str, kind: str) -> list:
        if self.lexicon is None:
            raise ContractError("T28 needs its lexicon registry (T28Plugin(lexicon=...))")
        ids = sorted(f for f, x in self.lexicon.forms.items() if x.sem_id == sem and x.kind == kind
                     and self.lexicon.status(f) == "admitted")
        if not ids:
            raise ContractError(f"no admitted {kind} form for {sem}")
        return ids

    def _clause(self, sem: str, kind: str, pick, bind: dict) -> S.Slot:
        ids = self._admitted(sem, kind)
        fid = pick(ids)
        return self.lexicon.clause(fid, bind=bind)

    def _clause_det(self, sem: str, kind: str, salt: str, bind: dict) -> S.Slot:
        return self._clause(sem, kind, lambda ids: min(ids, key=lambda f: uhash(FAMILY, salt, f)), bind)

    # ------------------------------------------------------------------------------------------- sampling
    @staticmethod
    def _group_key(seed: int, sampler: str) -> tuple:
        """The slot group of a seed (G0 v1.2 section 2): yes/no slots in pairs (2m, 2m + 1), verdict slots in triples
        (3m .. 3m + 2) of one 40-seed block, any other slot alone. Everything that decides an overlay partner (a
        complement, a twin, an equiv or attack partner, the twin's target) or the label-blind mask draw is hashed
        from the GROUP, never from the seed or the gold, so the targets of a group (opposite yes / no, three different
        verdicts) meet the same overlay and cancel."""
        slot, b = seed % len(QFORM_SLOTS), seed // len(QFORM_SLOTS)
        q = QFORM_SLOTS[slot]
        if q in YN:
            return (sampler, b, "yn", SLOT_G[slot] // 2)
        if q == "ch_verdict":
            return (sampler, b, "v", SLOT_J[slot] // 3)
        return (sampler, seed, "own")

    def _pack_pool(self, sampler: str) -> tuple:
        """The packs a sampler draws its cards from: each training pack serves one or two of the training samplers
        (a window of ceil(1.5 m / 4) packs per sampler over the sorted pack ids, circular), so a card is one
        (sampler, pack) pair of about 20-50 rows at the family's size (spec 3.0: rows per card <= 64, median 30-45,
        >= max(20, rows / 45) cards, >= 5 wordings per card). S5 draws from the held-out packs."""
        if sampler in self.HELD_OUT_SAMPLERS:
            return self._dev_packs
        train = [x for x in self.SAMPLERS if x not in self.HELD_OUT_SAMPLERS]
        m = len(self._train_packs)
        width = max(1, min(m, -(-3 * m // (2 * len(train)))))
        start = (train.index(sampler) * m) // len(train)
        return tuple(self._train_packs[(start + t) % m] for t in range(width))

    def _rule_plan(self, seed: int, sampler: str, n_rules: int | None = None):
        """The display plan of a ch_rule row (c2_kit.choiceplan; G0 v1.2 S19): the number of rules n is drawn from the
        row key, the "No rule applies" option is always shown (k = n + 1) and is the gold with probability 1 / k. Only
        n and the abstain outcome are used: the option ORDER stays the plain hash order of render() (a twin must show
        the same list), whose gold position is uniform whichever option the gold is."""
        key = f"{FAMILY}|{seed}|{sampler}|ch_rule"
        if n_rules is None:
            lo, hi = SAMPLER_CFG[sampler]["n"]
            n_rules = lo + int(uhash(key, "n_rules") * (hi - lo + 1))
        return plan_choice(key, closed=n_rules, abstain=True, show_rate=1.0)

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        if self.lexicon is None:
            raise ContractError("T28 needs its lexicon registry (T28Plugin(lexicon=...))")
        slot = seed % len(QFORM_SLOTS)
        qform = QFORM_SLOTS[slot]
        b = seed // len(QFORM_SLOTS)
        policy = POLICY_IDS[b % len(POLICY_IDS)]
        target = _target(qform, b, SLOT_G[slot] if qform in YN else SLOT_J[slot])
        pool = self._pack_pool(sampler)
        pack = pool[int(uhash(FAMILY, "pack", sampler, seed) * len(pool))]
        plan = self._rule_plan(seed, sampler) if qform == "ch_rule" else None
        masked = qform == "ch_verdict" and uhash(FAMILY, "mask", *self._group_key(seed, sampler)) < P_MASKED
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        for it in range(400):
            spec = self._attempt(rng, seed, sampler, qform, policy, target, pack, plan, masked, it)
            if spec is not None:
                return self.derive(spec)
        raise ContractError(f"T28: no valid spec for seed {seed}, sampler {sampler}")

    def _attempt(self, rng, seed, sampler, qform, policy, target, pack, plan, masked, it=0):
        cfg = SAMPLER_CFG[sampler]
        gkey = rng.choice(GLOB_DRAW)
        gsem = GLOB_SEMS[gkey]
        n = rng.randint(*cfg["n"]) if plan is None else plan.closed
        spec_order = rng.choice(("tool_first", "conds_first")) if policy == "P3" else None
        inverted = qform == "ch_inverted"
        ch_rule = qform == "ch_rule"
        v = target if target is not None else rng.choice(EFFECTS)
        call = self._draw_call(rng, pack, role_ok=not inverted)
        default_decides = (rng.random() < P_DEFAULT) if plan is None else plan.gold_abstain
        built = self._arrange(rng, pack, call, gsem, n, policy, v, ch_rule, sampler, spec_order, default_decides)
        if built is None:
            return None
        rules, d, prio = built
        ids = self._ids(rng, n)
        default = v if default_decides else rng.choice(EFFECTS)
        codes = rng.sample(CODE_WORDS, 3) if masked else None
        styles = (rng.choice(cfg["policy"]), rng.choice(cfg["call"]))
        names = (rng.choice(USERS), rng.choice(AGENTS))
        prec = self._clause(PREC_SEM[policy], "precedence", rng.choice, {})
        spec = self._assemble(seed, sampler, "ch_verdict" if inverted else qform, pack, gkey, policy, spec_order,
                              rules, ids, prio, default, call, None, codes, styles, names, prec, rng)
        dec = RL.resolve(self._ruleset(spec, self._frames(spec)[0]), spec.env())
        want_rid = None if d is None else ids[d]
        if dec.effect != v or dec.rule_id != want_rid or (ch_rule and len(dec.tied) > 1):
            return None
        if inverted:
            cands = self._inverted_candidates(rng, pack, spec, call, gsem, it)
            if cands is None:
                return None
            spec = self._assemble(seed, sampler, qform, pack, gkey, policy, spec_order, rules, ids, prio, default,
                                  None, cands, None, styles, names, prec, rng, reuse=spec)
            try:
                self.solve_a(spec)
            except ContractError:
                return None
        return spec.replace(tags=self._tags(spec))

    def _ids(self, rng, n: int) -> list:
        if rng.random() < 0.3:
            nums = rng.sample(range(1, 13), n)
        else:
            nums = list(range(1, n + 1))
        return [f"R{x}" for x in nums]

    # ---- calls and values
    def _tools(self, pack) -> list:
        return [(f"{ns}.{verb}", args) for ns in sorted(pack["ns"]) for verb, args in sorted(pack["ns"][ns].items())]

    def _draw_call(self, rng, pack, *, role_ok=True) -> _Call:
        name, kinds = rng.choice(self._tools(pack))
        args = {a: self._draw_value(rng, pack, a) for a in ARG_KINDS if a in kinds}
        role = rng.choice(sorted(ROLE_SET)) if role_ok and rng.random() < 0.5 else None
        return _Call(name, args, role)

    def _draw_value(self, rng, pack, kind: str, thresholds=()):
        if kind == "recipient":
            dom = _domains(pack)
            key = rng.choices(("internal", "sub", "partner", "outside", "nm_tld", "nm_hyphen"),
                              weights=(4, 2, 2, 2, 1, 1))[0]
            return f"{rng.choice(pack['locals'])}@{dom[key]}"
        if kind == "path":
            roots = sorted(pack["roots"])
            root = rng.choice(roots) if rng.random() < 0.8 else pack["roots"][rng.choice(roots)]
            f = rng.choice(pack["files"])
            return f"{root}/{f}" if rng.random() < 0.5 else f"{root}/{rng.choice(pack['subdirs'])}/{f}"
        if kind == "amount":
            t = rng.choice(tuple(thresholds) or THRESHOLDS)
            u = rng.random()
            if u < 0.3:
                return t
            if u < 0.55:
                return max(1, t + rng.choice((-1, 1, -100, 100, -500, 500)))
            return max(1, int(t * rng.uniform(0.2, 3.0)))
        if kind == "owner":
            return rng.choice(sorted(OWNER_SET))
        if kind == "env":
            return rng.choice(sorted(ENV_SET))
        raise ContractError(kind)

    def _rcpt_patterns(self, pack, addr: str | None) -> list:
        dom = _domains(pack)
        c = {f"*@{d}" for d in dom.values()} | {f"*@*.{dom['internal']}", "*@*.example"}
        if addr is not None:
            local, d = addr.split("@", 1)
            labels = d.split(".")
            c |= {f"*@{d}", f"{local}@{d}", f"*@*.{labels[-1]}"}
            if len(labels) >= 3:
                c.add("*@*." + ".".join(labels[1:]))
        return sorted(c)

    def _path_patterns(self, pack, path: str | None, gsem: GlobSem) -> list:
        roots = sorted(pack["roots"]) + sorted(pack["roots"].values())
        c = set()
        for r in roots:
            c |= {f"{r}/*", f"{r}/*.csv"}
            if gsem.double_star:
                c.add(f"{r}/**")
            for sd in pack["subdirs"]:
                c.add(f"{r}/{sd}/*")
        if path is not None:
            c.add(path)
        return sorted(c)

    # ---- conditions and rules
    def _cond(self, rng, pack, call: _Call, kind: str, want: bool, gsem: GlobSem, near=False):
        if kind in ("recipient", "path"):
            val = call.args.get(kind)
            pats = self._rcpt_patterns(pack, val) if kind == "recipient" else self._path_patterns(pack, val, gsem)
            if val is None:
                return None if want else _Cond(kind, rng.choice(pats))
            good = [p for p in pats if glob_a.match(p, val, gsem) == want]
            if near and not want:
                nm = [p for p in good if _loose(kind, p, val, gsem)]
                good = nm or good
            elif kind == "path" and rng.random() < 0.35:
                flip = _flip_sem(gsem)
                deep = [p for p in good if glob_a.match(p, val, flip) != want]
                good = deep or good
            return _Cond(kind, rng.choice(good)) if good else None
        if kind == "amount":
            amt = call.args.get("amount")
            if amt is None:
                return None if want else _Cond(kind, (rng.choice(CMPS), rng.choice(THRESHOLDS)))
            opts = [(sem, t) for t in sorted(set(THRESHOLDS) | {amt}) for sem in CMPS
                    if _cmp_holds(sem, amt, t) == want]
            at = [o for o in opts if o[1] == amt]
            close = [o for o in opts if abs(o[1] - amt) <= max(500, amt // 4)]
            if at and (near or rng.random() < 0.3):
                return _Cond(kind, rng.choice(at))
            if close and rng.random() < 0.6:
                return _Cond(kind, rng.choice(close))
            return _Cond(kind, rng.choice(opts)) if opts else None
        val = call.role if kind == "role" else call.args.get(kind)
        keys = sorted(CAT_SETS[kind])
        if want:
            return None if val is None else _Cond(kind, val)
        return _Cond(kind, rng.choice([x for x in keys if x != val]))

    def _cond_kinds(self, call: _Call) -> list:
        return [a for a in ARG_KINDS if a in call.args] + (["role"] if call.role else [])

    def _rule_true(self, rng, pack, call: _Call, gsem, effect, tool_kind=None, n_conds=None):
        tk = tool_kind or rng.choices(("exact", "ns", "any"), weights=(4, 3, 2))[0]
        pat = {"exact": call.tool, "ns": call.tool.split(".")[0] + ".*", "any": "*"}[tk]
        kinds = self._cond_kinds(call)
        nc = rng.choice((0, 1, 1, 2)) if n_conds is None else n_conds
        conds = []
        for kind in rng.sample(kinds, min(nc, len(kinds))):
            c = self._cond(rng, pack, call, kind, True, gsem)
            if c is None:
                return None
            conds.append(c)
        return _Rule(effect, pat, conds)

    def _rule_ok(self, rule: _Rule, call: _Call, gsem) -> bool:
        if not glob_a.match(rule.tool, call.tool, gsem):
            return False
        for c in rule.conds:
            if c.kind in ("recipient", "path"):
                val = call.args.get(c.kind)
                if val is None or not glob_a.match(c.value, val, gsem):
                    return False
            elif c.kind == "amount":
                val = call.args.get("amount")
                if val is None or not _cmp_holds(c.value[0], val, c.value[1]):
                    return False
            else:
                val = call.role if c.kind == "role" else call.args.get(c.kind)
                if val is None or val != c.value:
                    return False
        return True

    def _other_tool_pattern(self, rng, pack, call: _Call) -> str:
        ns, verb = call.tool.split(".", 1)
        sib = [f"{ns}.{v}" for v in sorted(pack["ns"][ns]) if v != verb]
        other_ns = [x for x in sorted(pack["ns"]) if x != ns]
        opts = sib + [f"{x}.*" for x in other_ns] + [t for t, _ in self._tools(pack) if not t.startswith(ns + ".")]
        return rng.choice(opts)

    def _rule_false(self, rng, pack, call: _Call, gsem, effect):
        for _ in range(8):
            u = rng.random()
            kinds = self._cond_kinds(call)
            absent = [k for k in ARG_KINDS + ("role",) if k not in kinds]
            if u < 0.4 or not kinds:
                pat = self._other_tool_pattern(rng, pack, call)
                tool_args = dict(self._tools(pack)).get(pat, ())
                pool = [k for k in tool_args] or list(kinds)
                conds = []
                for kind in rng.sample(pool, min(len(pool), rng.choice((0, 1, 1, 2)))):
                    c = self._cond(rng, pack, call, kind, rng.random() < 0.5, gsem)
                    if c is not None:
                        conds.append(c)
                r = _Rule(effect, pat, conds)
            elif u < 0.85 or not absent:
                r = self._rule_true(rng, pack, call, gsem, effect, n_conds=rng.choice((1, 1, 2)))
                if r is None or not r.conds:
                    continue
                i = rng.randrange(len(r.conds))
                c = self._cond(rng, pack, call, r.conds[i].kind, False, gsem, near=rng.random() < 0.5)
                if c is None:
                    continue
                r.conds[i] = c
            else:
                r = self._rule_true(rng, pack, call, gsem, effect, n_conds=0)
                c = self._cond(rng, pack, call, rng.choice(absent), False, gsem)
                if r is None or c is None:
                    continue
                r.conds.append(c)
            if r is not None and not self._rule_ok(r, call, gsem):
                return r
        return None

    def _near_miss(self, rng, pack, call: _Call, gsem, base: _Rule, effect):
        """A copy of `base` that fails on exactly one component (S2 label-first; near-miss strings)."""
        for _ in range(6):
            conds = [_Cond(c.kind, c.value) for c in base.conds]
            if conds and rng.random() < 0.75:
                i = rng.randrange(len(conds))
                c = self._cond(rng, pack, call, conds[i].kind, False, gsem, near=True)
                if c is None:
                    continue
                conds[i] = c
                r = _Rule(effect, base.tool, conds)
            else:
                ns, verb = call.tool.split(".", 1)
                sib = [f"{ns}.{v}" for v in sorted(pack["ns"][ns]) if v != verb]
                pat = rng.choice(sib) if sib else self._other_tool_pattern(rng, pack, call)
                r = _Rule(effect, pat, conds)
            if not self._rule_ok(r, call, gsem):
                return r
        return None

    def _spec_tuple(self, rule: _Rule, order: str) -> tuple:
        rank, n = _tool_rank(rule.tool), len(rule.conds)
        return (rank, n) if order == "tool_first" else (n, rank)

    def _arrange(self, rng, pack, call, gsem, n, policy, v, ch_rule, sampler, spec_order, default_decides):
        rules: list = [None] * n
        near_counts = SAMPLER_CFG[sampler]["near"]
        if default_decides:
            anchor = self._rule_true(rng, pack, call, gsem, rng.choice(EFFECTS), n_conds=rng.choice((1, 2)))
            for p in range(n):
                eff = rng.choice(EFFECTS)
                r = None
                if anchor is not None and anchor.conds and rng.random() < 0.5:
                    r = self._near_miss(rng, pack, call, gsem, anchor, eff)
                rules[p] = r or self._rule_false(rng, pack, call, gsem, eff)
            if any(r is None for r in rules):
                return None
            return rules, None, self._priority(rng, n, None, [])
        d = rng.randrange(n)
        so = spec_order or "tool_first"
        kinds = self._cond_kinds(call)
        argdeny = bool(call.args) and rng.random() < 0.2 and v in ("deny", "allow")
        trap_specific = policy == "P1" and rng.random() < 0.5
        if argdeny and v == "deny":
            D = self._rule_true(rng, pack, call, gsem, "deny", tool_kind="exact", n_conds=1)
        elif argdeny:
            D = _Rule("allow", call.tool, [])
        elif policy == "P3":
            D = self._rule_true(rng, pack, call, gsem, v, tool_kind=rng.choice(("exact", "exact", "ns")),
                                n_conds=min(len(kinds), rng.choice((1, 2, 2))))
        elif trap_specific:
            D = self._rule_true(rng, pack, call, gsem, v, tool_kind=rng.choice(("any", "ns")), n_conds=0)
        else:
            D = self._rule_true(rng, pack, call, gsem, v)
        if D is None:
            return None
        rules[d] = D
        if policy == "P2":
            pos = [p for p in range(n) if p > d]
        elif policy == "P4":
            pos = [p for p in range(n) if p < d]
        else:
            pos = [p for p in range(n) if p != d]
        nc = min(len(pos), rng.choice((0, 1, 1, 2, 2, 2)))
        comp = rng.sample(pos, nc)
        if comp and policy in ("P1", "P3", "P5") and d > 0 and not any(p < d for p in comp) and rng.random() < 0.85:
            comp[0] = rng.randrange(d)
        comp_rules = []
        if argdeny and pos:
            p = comp[0] if comp else rng.choice(pos)
            comp = [p] + [x for x in comp if x != p]
            if v == "deny":
                comp_rules.append((p, _Rule("allow", call.tool, [])))
            else:
                c = self._cond(rng, pack, call, rng.choice(kinds), False, gsem, near=True) if kinds else None
                if c is not None:
                    comp_rules.append((p, _Rule("deny", call.tool, [c])))
        for p in comp:
            if any(p == q for q, _ in comp_rules):
                continue
            eff = self._competitor_effect(rng, policy, v, ch_rule)
            if eff is None:
                continue
            r = None
            for _ in range(6):
                if trap_specific:
                    cand = self._rule_true(rng, pack, call, gsem, eff, tool_kind="exact",
                                           n_conds=min(len(kinds), rng.choice((1, 2))))
                else:
                    cand = self._rule_true(rng, pack, call, gsem, eff)
                if cand is None:
                    continue
                if policy == "P3":
                    sc, sd = self._spec_tuple(cand, so), self._spec_tuple(D, so)
                    if not (sc < sd or (sc == sd and RANK[eff] > RANK[v])):
                        continue
                r = cand
                break
            if r is not None:
                comp_rules.append((p, r))
        for p, r in comp_rules:
            rules[p] = r
        free = [p for p in range(n) if rules[p] is None]
        nn = min(len(free), rng.choice(near_counts))
        for p in rng.sample(free, nn):
            eff = self._strong_effect(rng, policy, v)
            rules[p] = self._near_miss(rng, pack, call, gsem, D, eff)
        for p in range(n):
            if rules[p] is None:
                rules[p] = self._rule_false(rng, pack, call, gsem, rng.choice(EFFECTS))
        if any(r is None for r in rules):
            return None
        return rules, d, self._priority(rng, n, d, [p for p, _ in comp_rules])

    def _competitor_effect(self, rng, policy, v, ch_rule):
        if policy == "P1":
            weaker = [e for e in EFFECTS if RANK[e] > RANK[v]]
            if not ch_rule and rng.random() < 0.15:
                weaker.append(v)
            return rng.choice(weaker) if weaker else None
        others = [e for e in EFFECTS if e != v]
        return rng.choice(others) if rng.random() < 0.9 else v

    def _strong_effect(self, rng, policy, v):
        if policy == "P1":
            stronger = [e for e in EFFECTS if RANK[e] < RANK[v]]
            if stronger:
                return rng.choice(stronger)
        return rng.choice([e for e in EFFECTS if e != v])

    def _priority(self, rng, n, d, comps) -> list:
        order = list(range(n))
        rng.shuffle(order)
        if d is not None and comps:
            first_comp = min(order.index(p) for p in comps)
            if order.index(d) > first_comp:
                order.remove(d)
                order.insert(first_comp, d)
        return order

    # ---- inverted candidates
    def _variant_values(self, rng, pack, kind: str, cur, thresholds) -> list:
        if kind == "recipient":
            local = cur.split("@", 1)[0]
            return [f"{local}@{d}" for d in sorted(set(_domains(pack).values()))]
        if kind == "path":
            out = []
            fname = cur.rsplit("/", 1)[1]
            for r in sorted(pack["roots"]) + sorted(pack["roots"].values()):
                out += [f"{r}/{fname}", f"{r}/{pack['subdirs'][0]}/{fname}"]
            return out
        if kind == "amount":
            out = set()
            for t in thresholds or THRESHOLDS[:3]:
                out |= {t - 1, t, t + 1, t * 2}
            return sorted(x for x in out if x >= 1)
        return sorted(CAT_SETS[kind])

    def _inverted_candidates(self, rng, pack, spec: Spec, call: _Call, gsem, it: int = 0):
        env = spec.env()
        thresholds = sorted({env[f"R{r['k']}_C{c['j']}_AMT"] for r in spec.structure["rules"] for c in r["conds"]
                             if c["kind"] == "amount"})
        pool = {}
        for name, kinds in self._tools(pack):
            if name == call.tool:
                continue
            args = {a: (call.args[a] if a in call.args else self._draw_value(rng, pack, a, thresholds))
                    for a in ARG_KINDS if a in kinds}
            c = _Call(name, args, None)
            pool[call_key(c.as_dict())] = c
        for a in sorted(call.args):
            for nv in self._variant_values(rng, pack, a, call.args[a], thresholds):
                if nv == call.args[a]:
                    continue
                c = _Call(call.tool, {**call.args, a: nv}, None)
                pool[call_key(c.as_dict())] = c
        gold_key = call_key(call.as_dict())
        pool.pop(gold_key, None)
        truth = {k: self._plan_call(spec, c.as_dict())[1] for k, c in pool.items()}
        if self._plan_call(spec, call.as_dict())[1] != "allow":
            return None
        wrong = sorted(k for k, e in truth.items() if e != "allow")
        reads = {name: {k for k in wrong if self._reads_allow(spec, pool[k].as_dict(), var)}
                 for name, var in MODEL_VARIANTS}
        explainable = sorted({k for ks in reads.values() for k in ks})
        kk = INVERTED_K[int(uhash(FAMILY, "k_inverted", spec.seed, spec.sampler) * len(INVERTED_K))]    # from the key
        if it >= 200:                          # a pack too thin for k (never seen with the 46 frozen packs): fewer options
            kk = min(kk, 4 if it < 300 else 3)
        if len(explainable) < kk - 1:
            return None
        for _ in range(40):
            pick = sorted(rng.sample(explainable, kk - 1))
            outs = {min((k for k in pick if k in reads[m]), default=None) for m in reads}
            if set(pick) <= outs:
                cands = [call] + [pool[k] for k in pick]
                rng.shuffle(cands)
                return cands
        return None

    # ---- assembling a Spec
    def _call_slots(self, prefix: str, call: _Call) -> dict:
        out = {f"{prefix}_TOOL": S.id_slot(call.tool)}
        for a in ARG_KINDS:
            if a not in call.args:
                continue
            v, s = call.args[a], f"{prefix}_{SUFFIX[a]}"
            if a in ("recipient", "path"):
                out[s] = S.glob_slot(v)
            elif a == "amount":
                out[s] = S.cents_slot(v)
            else:
                out[s] = S.category_slot(v, CAT_SETS[a])
        if call.role is not None:
            out[f"{prefix}_ROLE"] = S.category_slot(call.role, ROLE_SET)
        return out

    def _assemble(self, seed, sampler, qform, pack, gkey, policy, spec_order, rules, ids, prio, default, call,
                  cands, codes, styles, names, prec, rng, reuse: Spec | None = None) -> Spec:
        slots = {"USER": S.name_slot(names[0]), "AGENT": S.name_slot(names[1]),
                 "DEFAULT": S.category_slot(default, EFFECT_SET), "PREC": prec}
        srules = []
        for i, r in enumerate(rules):
            k = i + 1
            slots[f"R{k}_EFF"] = S.category_slot(r.effect, EFFECT_SET)
            slots[f"R{k}_TOOL"] = S.glob_slot(r.tool)
            sconds = []
            for j, c in enumerate(r.conds, 1):
                base = f"R{k}_C{j}"
                if c.kind in ("recipient", "path"):
                    slots[base] = S.glob_slot(c.value)
                elif c.kind == "amount":
                    slots[base + "_AMT"] = S.cents_slot(c.value[1])
                    if reuse is not None:
                        slots[base + "_CMP"] = reuse.slots[base + "_CMP"]
                    else:
                        slots[base + "_CMP"] = self._clause(c.value[0], "comparator", rng.choice,
                                                            {"X": base + "_AMT"})
                else:
                    slots[base] = S.category_slot(c.value, CAT_SETS[c.kind])
                sconds.append({"kind": c.kind, "j": j})
            srules.append({"rid": ids[i], "k": k, "conds": sconds})
        structure = {"rules": srules, "glob": gkey, "spec_order": spec_order,
                     "priority": [ids[i] for i in prio] if policy == "P5" else None,
                     "call": None, "candidates": None, "codes": codes,
                     "policy_style": styles[0], "call_style": styles[1]}
        if call is not None:
            slots.update(self._call_slots("CALL", call))
            structure["call"] = {"args": [a for a in ARG_KINDS if a in call.args], "role": call.role is not None}
        else:
            cl = []
            for c, cd in enumerate(cands, 1):
                slots.update(self._call_slots(f"K{c}", cd))
                cl.append({"c": c, "args": [a for a in ARG_KINDS if a in cd.args], "role": False})
            structure["candidates"] = cl
        deep = qform == "ch_inverted"
        return Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:{pack['id']}", qform, slots,
                    structure=structure, depth=3 if deep else 2, deep=deep, pack=pack["id"])

    # ------------------------------------------------------------------------------------------- frames / calls
    def _frames(self, spec: Spec) -> list:
        st = spec.structure
        if st.get("call"):
            return [self._frame("CALL", st["call"])]
        return [self._frame(f"K{c['c']}", c) for c in st["candidates"]]

    @staticmethod
    def _frame(prefix: str, d: dict) -> dict:
        f = {"tool": f"{prefix}_TOOL"}
        for a in d["args"]:
            f[a] = f"{prefix}_{SUFFIX[a]}"
        if d.get("role"):
            f["role"] = f"{prefix}_ROLE"
        return f

    @staticmethod
    def _call_of(env: dict, frame: dict) -> dict:
        return {"tool": env[frame["tool"]], "args": {a: env[frame[a]] for a in ARG_KINDS if a in frame},
                "role": env[frame["role"]] if "role" in frame else None}

    # ------------------------------------------------------------------------------------------- solver A
    def _cond_node(self, k: int, c: dict, frame: dict, env: dict, gsem: GlobSem):
        kind, base = c["kind"], f"R{k}_C{c['j']}"
        if kind not in frame:
            return RL.Lit(False)
        if kind in ("recipient", "path"):
            return RL.Glob(RL.Ref(base), RL.Ref(frame[kind]), gsem)
        if kind == "amount":
            return RL.Cmp(CMP_OP[env[base + "_CMP"]], RL.Ref(frame["amount"]), RL.Ref(base + "_AMT"))
        return RL.Cmp("==", RL.Ref(frame[kind]), RL.Ref(base))

    def _ruleset(self, spec: Spec, frame: dict) -> RL.RuleSet:
        env, st = spec.env(), spec.structure
        gsem = GLOB_SEMS[st["glob"]]
        pol = _policy(env)
        order = st.get("spec_order") or "tool_first"
        out = []
        for r in st["rules"]:
            k = r["k"]
            parts = [RL.Glob(RL.Ref(f"R{k}_TOOL"), RL.Ref(frame["tool"]), gsem)]
            parts += [self._cond_node(k, c, frame, env, gsem) for c in r["conds"]]
            rank, n = _tool_rank(env[f"R{k}_TOOL"]), len(r["conds"])
            out.append(RL.Rule(r["rid"], env[f"R{k}_EFF"], RL.And(tuple(parts)),
                               specificity=(rank, n) if order == "tool_first" else (n, rank)))
        return RL.RuleSet(tuple(out), POLICIES[pol], env["DEFAULT"], effect_order=EFFECT_ORDER,
                          priority=tuple(st["priority"]) if pol == "P5" else ())

    def solve_a(self, spec: Spec):
        env = spec.env()
        if spec.qform == "ch_inverted":
            allowed = [call_key(self._call_of(env, f)) for f in self._frames(spec)
                       if RL.resolve(self._ruleset(spec, f), env).effect == "allow"]
            if len(allowed) != 1:
                raise ContractError(f"inverted row with {len(allowed)} calls that run without asking")
            return allowed[0]
        d = RL.resolve(self._ruleset(spec, self._frames(spec)[0]), env)
        if spec.qform == "ch_rule":
            if len(d.tied) > 1:
                raise ContractError("which-rule row with a tie")
            return d.rule_id or "default"
        return _answer(spec.qform, d.effect)

    # ------------------------------------------------------------------------------------------- the plan
    def _holds(self, env, k, c, call: dict, gsem, loose, cmp_map) -> bool:
        kind, base = c["kind"], f"R{k}_C{c['j']}"
        val = call["role"] if kind == "role" else call["args"].get(kind)
        if val is None:
            return False
        if kind == "recipient":
            return glob_a.match(env[base], val, gsem) or (loose and _loose_rcpt(env[base], val))
        if kind == "path":
            return glob_a.match(env[base], val, gsem) or (loose and _loose_path(env[base], val, gsem))
        if kind == "amount":
            sem = env[base + "_CMP"]
            return _cmp_holds((cmp_map or {}).get(sem, sem), val, env[base + "_AMT"])
        return val == env[base]

    def _vector(self, spec: Spec, call: dict, *, gsem=None, loose=False, cmp_map=None, ignore_conds=False,
                order=None) -> list:
        env, st = spec.env(), spec.structure
        gsem = gsem or GLOB_SEMS[st["glob"]]
        order = order or st.get("spec_order") or "tool_first"
        out = []
        for i, r in enumerate(st["rules"]):
            k = r["k"]
            pat = env[f"R{k}_TOOL"]
            ok = glob_a.match(pat, call["tool"], gsem)
            if ok and not ignore_conds:
                ok = all(self._holds(env, k, c, call, gsem, loose, cmp_map) for c in r["conds"])
            rank, n = _tool_rank(pat), len(r["conds"])
            out.append({"rid": r["rid"], "i": i, "num": int(r["rid"][1:]), "effect": env[f"R{k}_EFF"], "ok": ok,
                        "spec": (rank, n) if order == "tool_first" else (n, rank), "n": n, "rank": rank})
        return out

    def _plan_call(self, spec: Spec, call: dict, *, policy=None, spec_order=None, swap_order=False,
                   ignore_conds=False, default=None, cmp_map=None, flip_slash=False, loose=False,
                   lowest_id=False, reverse_priority=False, post=None):
        """(rule id or None, effect, tied ids) by the direct plan; None when the variant does not apply."""
        env, st = spec.env(), spec.structure
        true_pol = _policy(env)
        pol = policy or true_pol
        if swap_order and true_pol != "P3":
            return None
        if (lowest_id and true_pol not in ("P2", "P4")) or (reverse_priority and true_pol != "P5"):
            return None
        order = spec_order or st.get("spec_order") or "tool_first"
        if swap_order:
            order = "conds_first" if order == "tool_first" else "tool_first"
        gsem = GLOB_SEMS[st["glob"]]
        if flip_slash:
            gsem = _flip_sem(gsem)
        vec = self._vector(spec, call, gsem=gsem, loose=loose, cmp_map=cmp_map, ignore_conds=ignore_conds,
                           order=order)
        m = [x for x in vec if x["ok"]]
        if not m:
            eff = default or env["DEFAULT"]
            res = (None, eff, ())
        else:
            pos = "num" if lowest_id else "i"
            if pol == "P2":
                win = min(m, key=lambda x: x[pos])
                tied = [win]
            elif pol == "P4":
                win = max(m, key=lambda x: x[pos])
                tied = [win]
            elif pol == "P5":
                prio = list(st["priority"] or [])
                if reverse_priority:
                    prio = prio[::-1]
                if not prio:
                    return None
                win = min(m, key=lambda x: prio.index(x["rid"]))
                tied = [win]
            elif pol == "P1":
                best = min(RANK[x["effect"]] for x in m)
                tied = [x for x in m if RANK[x["effect"]] == best]
                win = tied[0]
            else:
                key = max((x["spec"], -RANK[x["effect"]]) for x in m)
                tied = [x for x in m if (x["spec"], -RANK[x["effect"]]) == key]
                win = tied[0]
            res = (win["rid"], win["effect"], tuple(x["rid"] for x in tied))
        if post is not None:
            res = (res[0], post[1] if res[1] == post[0] else res[1], res[2])
        return res

    def _reads_allow(self, spec: Spec, call: dict, variant: dict) -> bool:
        res = self._plan_call(spec, call, **variant)
        return res is not None and res[1] == "allow"

    def _predict(self, spec: Spec):
        """The answer the plan predicts (twins and G4); None when it is not a single well-defined answer."""
        if spec.qform == "ch_inverted":
            return None
        rid, eff, tied = self._plan_call(spec, self._call_of(spec.env(), self._frames(spec)[0]))
        if spec.qform == "ch_rule":
            return None if len(tied) > 1 else (rid or "default")
        return _answer(spec.qform, eff)

    def _tags(self, spec: Spec) -> tuple:
        env, st = spec.env(), spec.structure
        tags = []
        nums = [int(r["rid"][1:]) for r in st["rules"]]
        if nums != sorted(nums):
            tags.append("ids_out_of_order")
        if st.get("codes"):
            tags.append("masked_labels")
        if not st.get("call"):
            return tuple(tags + ["inverted"])
        call = self._call_of(env, self._frames(spec)[0])
        vec = self._vector(spec, call)
        rid, eff, _ = self._plan_call(spec, call)
        m = [x for x in vec if x["ok"]]
        gsem = GLOB_SEMS[st["glob"]]
        if not m:
            tags.append("default_decides")
        else:
            if m[0]["effect"] != eff:
                tags.append("first_listed_loses")
            if _policy(env) == "P1":
                top = max(m, key=lambda x: (x["rank"], x["n"]))
                if top["effect"] != eff:
                    tags.append("specific_loses_p1")
        tool_hit = [r for r in st["rules"] if glob_a.match(env[f"R{r['k']}_TOOL"], call["tool"], gsem)]
        if any(env[f"R{r['k']}_EFF"] == "allow" and not r["conds"] for r in tool_hit) and \
                any(env[f"R{r['k']}_EFF"] == "deny" and r["conds"] for r in tool_hit):
            tags.append("arg_deny_vs_tool_allow")
        for r in tool_hit:
            for c in r["conds"]:
                base = f"R{r['k']}_C{c['j']}"
                if c["kind"] == "amount" and env.get(base + "_AMT") == call["args"].get("amount"):
                    tags.append("amount_at_threshold")
                if c["kind"] in ("recipient", "path") and c["kind"] in call["args"]:
                    val = call["args"][c["kind"]]
                    if not glob_a.match(env[base], val, gsem) and _loose(c["kind"], env[base], val, gsem):
                        tags.append("near_miss")
                    if c["kind"] == "path" and glob_a.match(env[base], val, gsem) != glob_a.match(
                            env[base], val, _flip_sem(gsem)):
                        tags.append("star_slash")
        return tuple(sorted(set(tags)))

    # ------------------------------------------------------------------------------------------- canonical
    @staticmethod
    def _cond_canon(env: dict, k: int, c: dict) -> list:
        base = f"R{k}_C{c['j']}"
        if c["kind"] == "amount":
            return ["amount", env[base + "_CMP"], env[base + "_AMT"]]
        return [c["kind"], env[base]]

    def canonical(self, spec: Spec) -> dict:
        env, st = spec.env(), spec.structure
        gsem = GLOB_SEMS[st["glob"]]
        pol = _policy(env)
        rules = [{"id": r["rid"], "effect": env[f"R{r['k']}_EFF"], "tool": env[f"R{r['k']}_TOOL"],
                  "conds": [self._cond_canon(env, r["k"], c) for c in r["conds"]]} for r in st["rules"]]
        out = {"qform": spec.qform, "rules": rules, "precedence": env["PREC"],
               "spec_order": st["spec_order"] if pol == "P3" else None,
               "priority": list(st["priority"]) if pol == "P5" else None,
               "glob": {"star_crosses_slash": gsem.star_crosses_slash, "double_star": gsem.double_star},
               "default": env["DEFAULT"], "codes": list(st["codes"]) if st.get("codes") else None,
               "call": None, "candidates": None, "user": env["USER"], "agent": env["AGENT"]}
        frames = self._frames(spec)
        if st.get("call"):
            out["call"] = self._call_of(env, frames[0])
        else:
            out["candidates"] = sorted(call_key(self._call_of(env, f)) for f in frames)
        return out

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("user", "agent")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"user": c["user"], "agent": c["agent"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("user", "name", "the person the assistant works for, as written"),
                Field("agent", "name", "the name of the AI assistant, as written")]

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def _row_key(spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    @staticmethod
    def _cond_tpls(r: dict) -> list:
        k, out = r["k"], []
        for c in r["conds"]:
            b = f"R{k}_C{c['j']}"
            out.append({"recipient": f"the recipient matches {{{b}}}", "path": f"the path matches {{{b}}}",
                        "amount": f"the amount is {{{b}_CMP}}", "env": f"the environment is {{{b}}}",
                        "owner": f"the owner is {{{b}:s1}}", "role": f"the session role is {{{b}}}"}[c["kind"]])
        return out

    def _policy_tpl(self, spec: Spec) -> str:
        st = spec.structure
        style = st["policy_style"]
        lines = []
        if style == "list":
            lines.append("Permission rules (in listed order):")
            for r in st["rules"]:
                cs = self._cond_tpls(r)
                lines.append(f"{r['rid']}: {{R{r['k']}_EFF}} {{R{r['k']}_TOOL}}" + (f" when {' and '.join(cs)}"
                                                                                    if cs else ""))
        elif style == "memo":
            lines.append("Policy memo, rules in listed order:")
            for r in st["rules"]:
                cs = self._cond_tpls(r)
                lines.append(f"- Rule {r['rid']} ({{R{r['k']}_EFF}}): calls to {{R{r['k']}_TOOL}}"
                             + (f" when {' and '.join(cs)}" if cs else ", with no condition"))
        elif style == "yaml":
            lines += ["permission_policy:", "  rules:"]
            for r in st["rules"]:
                cs = self._cond_tpls(r)
                lines += [f"    - id: {r['rid']}", f"      effect: {{R{r['k']}_EFF}}",
                          f"      tool: \"{{R{r['k']}_TOOL}}\""]
                lines += (["      when:"] + [f"        - \"{c}\"" for c in cs]) if cs else ["      when: []"]
        elif style in ("json", "statements"):
            keys = ("id", "effect", "tool", "when") if style == "json" else ("sid", "effect", "action", "conditions")
            lines.append('{"permission_policy": {"rules": [' if style == "json" else '{"statements": [')
            items = []
            for r in st["rules"]:
                cs = ", ".join(f'"{c}"' for c in self._cond_tpls(r))
                items.append(f'  {{"{keys[0]}": "{r["rid"]}", "{keys[1]}": "{{R{r["k"]}_EFF}}", '
                             f'"{keys[2]}": "{{R{r["k"]}_TOOL}}", "{keys[3]}": [{cs}]}}')
            lines.append(",\n".join(items))
            lines.append("]}}" if style == "json" else "]}")
        else:
            raise ContractError(f"policy style {style}")
        return "\n".join(lines)

    @staticmethod
    def _func_expr(prefix: str, d: dict) -> str:
        args = ", ".join(f'{ARG_NAME[a]}="{{{prefix}_{SUFFIX[a]}{PIN[a]}}}"' for a in d["args"])
        return f"{{{prefix}_TOOL}}({args})"

    def _call_tpl(self, spec: Spec) -> str:
        st = spec.structure
        d, style = st["call"], st["call_style"]
        role = d.get("role")
        expr = self._func_expr("CALL", d)
        if style == "json":
            args = ", ".join(f'"{ARG_NAME[a]}": "{{CALL_{SUFFIX[a]}{PIN[a]}}}"' for a in d["args"])
            return ('Proposed call:\n{"tool": "{CALL_TOOL}", "args": {' + args + "}"
                    + (', "session_role": "{CALL_ROLE}"' if role else "") + "}")
        if style == "func":
            return "Proposed call: " + expr + ("\nSession role: {CALL_ROLE}" if role else "")
        if style == "cli":
            parts = "".join(f' --{ARG_NAME[a]} "{{CALL_AMT}}"' if a == "amount" else
                            f" --{ARG_NAME[a]} {{CALL_{SUFFIX[a]}{PIN[a]}}}" for a in d["args"])
            return "Proposed call: agentctl call {CALL_TOOL}" + parts + ("\nSession role: {CALL_ROLE}" if role else "")
        if style == "transcript":
            return "Agent transcript (proposed call):\n> " + expr + ("\n> session role: {CALL_ROLE}" if role else "")
        if style == "chat":
            return ("IT chat thread (proposed call):\n" + CHAT_PREFIX + expr
                    + ("\n[agent] session role: {CALL_ROLE}" if role else ""))
        raise ContractError(f"call style {style}")

    def _calls_tpl(self, spec: Spec) -> str:
        """Inverted rows (G0 v1.2 S20): the candidate calls, listed in the state as "Call i: <function call>" (the call
        text appears here once; the options are the labels "Call i", so no option text can be matched to the policy)."""
        return CALLS_HEAD + "\n" + "\n".join(f"Call {c['c']}: " + self._func_expr(f"K{c['c']}", c)
                                              for c in spec.structure["candidates"])

    def _card_tpl(self, spec: Spec, style: str = "full") -> str:
        """The card (program text; G0 section 4, v1.2): one line each in the order of section 4. Style "short" shortens
        the reading line, the specificity line, the owner line and the verdict line (MATCH_SHORT ...); every other
        line, and every rule, is the same."""
        if style not in CARD_STYLES:
            raise ContractError(f"card style {style!r}")
        short = style == "short"
        env, st = spec.env(), spec.structure
        pol = _policy(env)
        lines = [MATCH_SHORT if short else MATCH_LINE,
                 "Pattern matching: " + GLOB_SEMS[st["glob"]].card_text() + " " + LITERAL_LINE]
        if self._mentions_owner(spec):
            lines.append(OWNER_SHORT if short else OWNER_LINE)
        lines.append("Precedence: {PREC}.")
        if pol == "P3":
            lines.append((SPEC_SHORT if short else SPEC_LINE)[st["spec_order"]])
        if pol == "P5":
            lines.append(PRIORITY_HEAD + ", ".join(st["priority"]) + ".")
        lines += ["If no rule applies, the verdict is {DEFAULT}.", VERDICT_SHORT if short else VERDICT_LINE]
        if st.get("codes"):
            lines.append("Answer codes: {} = allow, {} = ask, {} = deny.".format(*st["codes"]))
        lines.append(CLOSED_WORLD)
        return "\n".join(lines)

    @staticmethod
    def card_style(spec: Spec) -> str:
        """The card style of a row, drawn from the seed and the sampler only (label-blind; one style for a whole
        relation unit, so a twin, a complement and an equiv partner print the same phrasing)."""
        return CARDS.draw_style(f"{FAMILY}|{spec.seed}|{spec.sampler}|card", CARD_SHARES)

    @staticmethod
    def _mentions_owner(spec: Spec) -> bool:
        st = spec.structure
        calls = [st["call"]] if st.get("call") else list(st["candidates"])
        return any(c["kind"] == "owner" for r in st["rules"] for c in r["conds"]) or any(
            "owner" in c["args"] for c in calls)

    def ctx_for(self, spec: Spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity; Stage B pilot fix F1,
        G0 v1.2 section 3 R2), so neither render() nor the pipeline's complement partner can pick one. Label-blind (it
        reads wording texts and their forms only). Cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    def _skins_of(self, ctx) -> dict:
        for c, idx in self._skin_index:
            if c is ctx:
                return idx
        idx: dict = {}
        for sk in sorted(ctx.skins.values(), key=lambda x: x.skin_id):
            if sk.family == FAMILY and sk.kind == "skin":
                idx.setdefault((sk.held_out, sk.register), []).append(sk)
        self._skin_index.append((ctx, idx))
        return idx

    def _deal_skin(self, ctx, spec: Spec):
        """The narrative skin of a unit, dealt (G0 v1.2 section 2; spec 3.0: each register <= 15% of the rows, each
        skin feeds <= 6 rows): within every aligned run of len(registers) seeds of one sampler each register comes up
        exactly once, in a seeded order, and a register's skins are used once each, in a seeded order per cycle, before
        any is used again. Label-blind (seed, sampler and the pool only). A register the context has no skin for is
        skipped; a context without any dealt skin falls back to the kit's hash pick."""
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        idx = self._skins_of(ctx)
        all_regs = [r for r in self.REGISTERS if (r in self.HELD_OUT_REGISTERS) == held]
        if not any(idx.get((held, r)) for r in all_regs):
            return ctx.pick(FAMILY, "skin", self._row_key(spec), held_out=held)
        grp, pos = divmod(spec.seed, len(all_regs))
        order = sorted(all_regs, key=lambda r: uhash(FAMILY, "regdeal", spec.sampler, grp, r))
        reg = next(r for r in order[pos:] + order[:pos] if idx.get((held, r)))     # the dealt register, or the next
        skins = idx[(held, reg)]                                                    # one with a skin in this context
        cyc, i = divmod(grp, len(skins))
        perm = sorted(range(len(skins)), key=lambda j: uhash(FAMILY, "skindeal", spec.sampler, reg, cyc, j))
        return skins[perm[i]]

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        ctx = self.ctx_for(spec, ctx)                      # never pick a wording that breaks the polarity rule
        key = self._row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or self._deal_skin(ctx, spec)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=held)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        if attack is not None and "\n" in attack.text:
            raise K.RenderError("attack lines are one line")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        st = spec.structure
        blocks = [("calls" if (b == "call" and not st.get("call")) else b) for b in LAYOUT[spec.sampler]]
        note_block = "call" if st.get("call") else "policy"
        tb = TextBuilder()
        for i, b in enumerate(blocks):
            if i:
                tb.add("state", "\n\n")
            if b == "narrative":
                tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
                continue
            tpl = {"policy": self._policy_tpl, "call": self._call_tpl, "calls": self._calls_tpl}[b](spec)
            filled = K.fill(tpl, slots, forms)
            self._check_container(spec, b, filled.text)
            tb.add("state", filled)
            if attack is not None and b == note_block:
                tb.add("state", "\n" + NOTE_PREFIX).add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        style = self.card_style(spec)
        # the rules sit where the served prompt prints them once: row.card on a yes/no row; at the head of the
        # instructions on a choice row (the only place a choice row prints them; kit cards.place_rules)
        placed = CARDS.place_rules(tb, K.fill(self._card_tpl(spec, style), slots, forms),
                                   self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        models = self.error_models()
        if spec.qform == "ch_verdict":
            codes = st.get("codes")
            rk = (lambda e: codes[EFFECTS.index(e)]) if codes else VERDICT_TEXT.__getitem__
            os_ = build_closed(spec, ans, list(EFFECTS), models, row_key=key, render_key=rk)
        elif spec.qform == "ch_rule":
            # a closed set: every rule id and the "No rule applies" option, shown on every row, in one label-blind order
            # of the row key (a twin must show the same option list: G-TW). The plan (_rule_plan) decides k and whether
            # the default is the gold at sampling time; the order is the plain hash order, so the gold's position is
            # uniform whichever option it is.
            os_ = build_closed(spec, ans, [r["rid"] for r in st["rules"]], models, row_key=key,
                               render_key=lambda x: x, abstain=("default", DEFAULT_OPTION), show_abstain=True)
        elif spec.qform == "ch_inverted":
            env = spec.env()
            label = {call_key(self._call_of(env, f)): f"Call {c['c']}"
                     for f, c in zip(self._frames(spec), st["candidates"])}
            os_ = build_closed(spec, ans, sorted(label), models, row_key=key, render_key=label.__getitem__)
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CARDS.defs_style(placed, style))

    @staticmethod
    def _check_container(spec: Spec, block: str, text: str) -> None:
        """Program JSON / YAML blocks must parse (values never hold quotes or backslashes)."""
        st = spec.structure
        try:
            if block == "policy" and st["policy_style"] in ("json", "statements"):
                json.loads(text)
            elif block == "policy" and st["policy_style"] == "yaml":
                import yaml
                yaml.safe_load(text)
            elif block == "call" and st["call_style"] == "json":
                json.loads(text.split("\n", 1)[1])
        except Exception as e:  # noqa: BLE001
            raise K.RenderError(f"{block} block does not parse: {e}") from None

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = spec.qform
        salt = self._group_key(spec.seed, spec.sampler)          # per slot GROUP, not per seed (G0 v1.2 section 2)
        if q in COMPLEMENT_PARTNERS and uhash(FAMILY, "comp", *salt) < P_COMPLEMENT:
            partners = COMPLEMENT_PARTNERS[q]
            out.append(RelationProposal("complement", qform=partners[int(uhash(FAMILY, "ckind", *salt)
                                                                         * len(partners))]))
        u = uhash(FAMILY, "extra", *salt)
        if u < P_EQUIV:
            out.append(RelationProposal("equiv", spec=self._restyle(spec), note="another policy format"))
        elif u < P_EQUIV + P_INV:
            out.append(RelationProposal("inv", note="one attack line in the tool output"))
        if q != "ch_inverted" and uhash(FAMILY, "twin", *salt) < P_TWIN:
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        return out + self._metamorphic(spec)

    def _restyle(self, spec: Spec) -> Spec:
        st = spec.structure
        styles = [s for s in EQUIV_POLICY_STYLES if s != st["policy_style"]]
        new = dict(st, policy_style=styles[int(uhash(FAMILY, "eqp", spec.seed, spec.sampler) * len(styles))])
        if st["call_style"] in PLAIN_CALL_STYLES:
            cs = [s for s in PLAIN_CALL_STYLES if s != st["call_style"]]
            new["call_style"] = cs[int(uhash(FAMILY, "eqc", spec.seed, spec.sampler) * len(cs))]
        return spec.replace(structure=new)

    def _edits(self, spec: Spec, rng) -> list:
        """Candidate one-slot edits for a minimal-edit twin, in a seeded tier order."""
        env, st = spec.env(), spec.structure
        pack = self._pack_by_id[spec.pack]
        call_tier, rule_tier, eff_tier, prec_tier = [], [], [], []
        d = st["call"]
        thresholds = sorted({env[f"R{r['k']}_C{c['j']}_AMT"] for r in st["rules"] for c in r["conds"]
                             if c["kind"] == "amount"})
        for a in d["args"]:
            s = f"CALL_{SUFFIX[a]}"
            for nv in self._variant_values(rng, pack, a, env[s], thresholds):
                if nv == env[s]:
                    continue
                if a in ("recipient", "path"):
                    call_tier.append((s, S.glob_slot(nv)))
                elif a == "amount":
                    call_tier.append((s, S.cents_slot(nv)))
                else:
                    call_tier.append((s, S.category_slot(nv, CAT_SETS[a])))
        if d.get("role"):
            call_tier += [("CALL_ROLE", S.category_slot(x, ROLE_SET)) for x in sorted(ROLE_SET)
                          if x != env["CALL_ROLE"]]
        same_args = [t for t, kinds in self._tools(pack)
                     if t != env["CALL_TOOL"] and [a for a in ARG_KINDS if a in kinds] == list(d["args"])]
        call_tier += [("CALL_TOOL", S.id_slot(t)) for t in same_args]
        for r in st["rules"]:
            k = r["k"]
            for c in r["conds"]:
                base = f"R{k}_C{c['j']}"
                if c["kind"] == "amount" and "amount" in d["args"]:
                    amt = env["CALL_AMT"]
                    for t in (amt - 1, amt, amt + 1):
                        if t >= 1 and t != env[base + "_AMT"]:
                            rule_tier.append((base + "_AMT", S.cents_slot(t)))
                    sem = env[base + "_CMP"]
                    swap = {**DROP_INCL, **ADD_EXCL}[sem]
                    rule_tier.append((base + "_CMP", self._clause_det(swap, "comparator", f"twin|{base}",
                                                                      {"X": base + "_AMT"})))
                elif c["kind"] in CAT_SETS:
                    rule_tier += [(base, S.category_slot(x, CAT_SETS[c["kind"]])) for x in sorted(CAT_SETS[c["kind"]])
                                  if x != env[base]]
            eff_tier += [(f"R{k}_EFF", S.category_slot(e, EFFECT_SET)) for e in EFFECTS if e != env[f"R{k}_EFF"]]
            tool = env["CALL_TOOL"]
            for pat in (tool, tool.split(".")[0] + ".*", "*"):
                if pat != env[f"R{k}_TOOL"]:
                    rule_tier.append((f"R{k}_TOOL", S.glob_slot(pat)))
        eff_tier += [("DEFAULT", S.category_slot(e, EFFECT_SET)) for e in EFFECTS if e != env["DEFAULT"]]
        pol = _policy(env)
        if pol in ("P1", "P2", "P4"):
            prec_tier += [("PREC", self._clause_det(PREC_SEM[p], "precedence", "twin|PREC", {}))
                          for p in ("P1", "P2", "P4") if p != pol]
        for t in (call_tier, rule_tier, eff_tier, prec_tier):
            rng.shuffle(t)
        u = rng.random()
        if u < 0.5:
            order = (call_tier, rule_tier, eff_tier, prec_tier)
        elif u < 0.75:
            order = (rule_tier, call_tier, eff_tier, prec_tier)
        elif u < 0.92:
            order = (eff_tier, call_tier, rule_tier, prec_tier)
        else:
            order = (prec_tier, call_tier, rule_tier, eff_tier)
        return [e for tier in order for e in tier]

    def _twin_want(self, spec: Spec, base):
        """The twin's planned outcome class, from the GROUP key (label-blind; G0 v1.2 section 2): a verdict row's twin
        takes the verdict base + 1 or base + 2 (the same step for the group's three bases, so the twins' verdicts are
        thirds too); a which-rule row's twin is the "No rule applies" option with probability 1 / (k - 1) when the
        base is a rule (so the abstain gold stays 1 / k over bases and twins) and a rule otherwise. Yes/no twins just
        flip. None: no planned class (the first edit that changes the answer is used)."""
        salt = self._group_key(spec.seed, spec.sampler)
        if spec.qform == "ch_verdict":
            step = 1 + int(uhash(FAMILY, "twin_step", *salt) * 2)
            return EFFECTS[(EFFECTS.index(base) + step) % 3]
        if spec.qform == "ch_rule":
            k = len(spec.structure["rules"]) + 1
            if base != "default" and uhash(FAMILY, "twin_abstain", *salt) < 1.0 / (k - 1):
                return "default"
            return "rule"
        return None

    @staticmethod
    def _twin_fits(want, p, base) -> bool:
        if p is None or p == base:
            return False
        if want is None:
            return True
        return (p == "default") if want == "default" else (p != "default") if want == "rule" else p == want

    def _twin(self, spec: Spec):
        """One input slot changed so that the plan predicts another answer (G-TW checks it against solver A). The
        edits are tried in the seeded tier order; the first one that reaches the planned class (_twin_want) wins, and
        when no edit does, the first one that changes the answer."""
        base = self._predict(spec)
        if base is None:
            return None
        rng = random.Random(f"{FAMILY}|twin|{spec.sampler}|{spec.seed}|{spec.qform}")
        want = self._twin_want(spec, base)
        fallback = None
        for name, slot in self._edits(spec, rng):
            try:
                t = spec.with_slot(name, slot)
            except ContractError:
                continue
            p = self._predict(t)
            if p is None or p == base:
                continue
            prop = RelationProposal("twin", spec=t, changed_slot=name, expect=p, note=f"edit {name}")
            if self._twin_fits(want, p, base):
                return prop
            fallback = fallback or prop
        return fallback

    def _metamorphic(self, spec: Spec) -> list:
        env, st = spec.env(), spec.structure
        out = []
        u2 = next(x for x in USERS if x != env["USER"])
        a2 = next(x for x in AGENTS if x != env["AGENT"])
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, "USER": S.name_slot(u2),
                                                                             "AGENT": S.name_slot(a2)}),
                                    expect="same", note="rename the user and the agent"))
        tools = [k for k, s in spec.slots.items() if k.endswith("_TOOL")]
        used_ns = {spec.slots[k].value.split(".")[0] for k in tools}
        call_ns = spec.slots[self._frames(spec)[0]["tool"]].value.split(".")[0]
        new_ns = next(x for x in SPARE_NS if x not in used_ns)
        ren = {}
        for k in tools:
            v = spec.slots[k].value
            if v.startswith(call_ns + "."):
                nv = new_ns + v[len(call_ns):]
                ren[k] = S.id_slot(nv) if spec.slots[k].kind == "id" else S.glob_slot(nv)
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **ren}),
                                    expect=self._renamed_answer(spec, tool=(call_ns, new_ns)),
                                    note="rename the call's namespace everywhere"))
        org = self._pack_by_id[spec.pack]["org"]
        rcpt = [k for k, s in spec.slots.items() if s.kind == "glob" and "@" in s.value and org in s.value]
        if rcpt:
            ren = {k: S.glob_slot(spec.slots[k].value.replace(org, "q" + org)) for k in rcpt}
            out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **ren}),
                                        expect=self._renamed_answer(spec, org=(org, "q" + org)),
                                        note="rename the organisation's domain everywhere"))
        rng = random.Random(f"{FAMILY}|g4|{spec.sampler}|{spec.seed}")
        if _policy(env) in ("P1", "P3", "P5"):
            rules = list(st["rules"])
            rng.shuffle(rules)
            out.append(RelationProposal("metamorphic", spec=spec.replace(structure=dict(st, rules=rules)),
                                        expect="same", note="shuffle the rules under an order-free policy"))
        if len(st["rules"]) < 8:
            k = max(r["k"] for r in st["rules"]) + 1
            rid = f"R{max(int(r['rid'][1:]) for r in st['rules']) + 1}"
            rules = list(st["rules"])
            rules.insert(rng.randrange(len(rules) + 1), {"rid": rid, "k": k, "conds": []})
            new_st = dict(st, rules=rules)
            if st.get("priority"):
                pr = list(st["priority"])
                pr.insert(rng.randrange(len(pr) + 1), rid)
                new_st["priority"] = pr
            spare = next(x for x in SPARE_NS if x not in used_ns)
            slots = {**spec.slots, f"R{k}_EFF": S.category_slot(rng.choice(EFFECTS), EFFECT_SET),
                     f"R{k}_TOOL": S.glob_slot(f"{spare}.{rng.choice(('sync', 'purge', 'export'))}")}
            out.append(RelationProposal("metamorphic", spec=spec.replace(structure=new_st, slots=slots),
                                        expect="same", note="add an inert rule"))
        if st.get("call") and "amount" in st["call"]["args"] and spec.qform != "ch_inverted":
            base = self._predict(spec)
            amt = env["CALL_AMT"]
            for r in st["rules"]:
                for c in r["conds"]:
                    if c["kind"] != "amount" or base is None:
                        continue
                    t = env[f"R{r['k']}_C{c['j']}_AMT"]
                    for nv in (t - 1, t, t + 1):
                        if nv < 1 or nv == amt:
                            continue
                        s2 = spec.with_slot("CALL_AMT", S.cents_slot(nv))
                        p = self._predict(s2)
                        if p is not None and p != base:
                            out.append(RelationProposal("metamorphic", spec=s2, expect=p,
                                                        note="move the amount across a threshold"))
                            return out
        return out

    def _renamed_answer(self, spec: Spec, *, tool=None, org=None):
        """G4 expectation for a rename: "same", except on inverted rows, whose answer key spells the call: the plan's
        allowed candidate with the same rename applied."""
        if spec.qform != "ch_inverted":
            return "same"
        env = spec.env()
        calls = [self._call_of(env, f) for f in self._frames(spec)]
        free = [c for c in calls if self._plan_call(spec, c)[1] == "allow"]
        if len(free) != 1:
            return None
        c = free[0]
        if tool and c["tool"].startswith(tool[0] + "."):
            c = dict(c, tool=tool[1] + c["tool"][len(tool[0]):])
        if org and "recipient" in c["args"]:
            c = dict(c, args=dict(c["args"], recipient=c["args"]["recipient"].replace(org[0], org[1])))
        return call_key(c)

    # ------------------------------------------------------------------------------------------- error models
    def _model_answer(self, spec: Spec, variant: dict):
        q = spec.qform
        if self.QFORMS[q].qtype == "noul":
            return None
        env = spec.env()
        if q == "ch_inverted":
            calls = [self._call_of(env, f) for f in self._frames(spec)]
            for c in sorted(calls, key=call_key):
                if self._plan_call(spec, c)[1] != "allow" and self._reads_allow(spec, c, variant):
                    return call_key(c)
            return None
        res = self._plan_call(spec, self._call_of(env, self._frames(spec)[0]), **variant)
        if res is None:
            return None
        rid, eff, tied = res
        if q == "ch_verdict":
            return eff
        if variant.get("post") or len(tied) > 1:
            return None
        return rid or "default"

    def error_models(self) -> dict:
        return {name: error_model(name, (lambda var: (lambda s: self._model_answer(s, var)))(var))
                for name, var in MODEL_VARIANTS}

