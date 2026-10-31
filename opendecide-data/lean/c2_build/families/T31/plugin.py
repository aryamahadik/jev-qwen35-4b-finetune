"""families/T31/plugin.py: T31 "authority at time t" (C2_DATA_SPEC 2.1 T31, 3.8; G0_SPEC.md frozen, sha below).

Two tracks on one card family (G0 M1; G0 v1.1 after the Haiku ambiguity pass):
  appr   who holds the single accountable (A) role for a request at its time: a RACI matrix (the default A holder),
         1-3 delegations with windows and amount bands, 0-2 notices (a revocation of a delegation, or an override
         naming a person). Precedence: latest covering override > covering delegation > default; two people at the
         deciding level -> escalate.
  agent  may the deepest agent of a grant chain use a scope at the request time: grants with windows and 2-6 scopes,
         attenuation (child = own list AND parent may use it), 0-2 revocations (one scope, or a whole grant).

  solver A   rule engine: one kit rule AST (rules.Cmp / And / Not / In / Or over aware datetimes and integer cents)
             per record, evaluated by rules.evaluate, then the tier precedence / chain conjunction  paradigm rule_engine
  solver B   solver_b.py: its own parser of the rendered row, epoch-minute half-open interval table scanned at the
             request minute, integer-cents sign table, set intersection down the chain           paradigm interval_scan
  status     a third, construction-only table (_appr_status / _decide, _agent_status / _usable): it steers the
             label-first samplers and predicts minimal-edit twins (one flipped condition), never the gold
  samplers   S1 forward + rejection to a target; S2 near-miss (every time at T-1 / T / T+1 minute, amounts at bounds);
             S3 config export (log style, larger org, more scopes); S4 narrative / transcript (conversion-heavy);
             S5 held out (held-out skins and registers, other offsets; mixdev only)
  questions  ch_approver (open set of people + escalate abstain), yn_holder (+ complements other / not),
             yn_agent_ok (+ complements beyond / lacks / not), ch_scope (open set of scopes)
  relations  complement, minimal-edit twin, equiv, inv, G4 metamorphic (rename, shift, re-offset)

Fix iteration 1 (14 Oct 2026; G0 v1.2; PILOT_VERDICT F01-F10, P1-P5):
  packs      the frozen pools_v2 packs (34 appr, 36 agent) and 320 names are wired: pack = f(card), one pack per card
             (24 training cards + 6 S5 cards per track); the in-code stand-ins below stay for the Haiku authoring
             tools (haiku_author / topup rebuild their frozen task files from them) and for nothing else
  choices    ch_approver / ch_scope draw a c2_kit.choiceplan plan from the row key BEFORE any structure: k, escalate
             display (40% of rows), escalate gold 1/k of the rows that show it, gold position and gold length rank
             (balanced per block of 32 seeds); a row that shows escalate has no twin (it would dilute the 1/k)
  cards      the rule block in three styles (CARD_TEXT: full 30%, compact 55%, short 15%; c2_kit.cards draw_style /
             place_rules / variant_problems); yes/no rows print it in row.card (once), choice rows keep it in the
             instructions; solver B reads both through cards.split_rules
  forms      the agent yes/no base form is drawn from all four forms (yes = bad 50%); a yes/no base has a one-slot flip
             with probability 0.90; double-negation forms yn_holder_dneg / yn_agent_dneg exist and are drawn only
             while the lexicon admits a polarity-clean wording of them (until Haiku authors them: 0% double negation)
  quarantine 20 skins with {cap|ITEM} (G3), Mode F documents that keep a name or a pronoun outside the slot (G3-H)
             and wordings that break the c2_kit.polarity rule (screened in ctx_for)
The in-code pools below (people, roles, processes, scopes, agent ids) are the v1 stand-ins; nothing here writes a file.
"""
from __future__ import annotations

import copy
import dataclasses
import datetime as dt
import hashlib
import json
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as CD  # noqa: E402
from c2_kit import choiceplan as CP  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import rules as RL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import build_options, error_model, register_name, uhash  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from c2_kit.plugin import (C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec,  # noqa: E402
                           choose_forms)
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T31"
# the v1.1 spec (G0_SPEC_v1_1.md, archived verbatim) the Haiku pools were authored and frozen under: haiku_author, topup,
# glex_admit and freeze_v2 record and check this pin, never the current one
POOL_G0_SHA256 = "d4f83e96c71012a8e041c64aa2554db588bda98e4014928a0defa3809f91c210"
UTC = dt.timezone.utc
MINUTE = dt.timedelta(minutes=1)
ESCALATE = "escalate"
ESCALATE_TEXT = "Escalate: no unique approver"
NO_BAND = "of any size"
CMP_OP = {"cmp.le": "<=", "cmp.lt": "<", "cmp.ge": ">=", "cmp.gt": ">"}
TO_INCLUSIVE = {"cmp.lt": "cmp.le", "cmp.gt": "cmp.ge"}       # add_exclusive_endpoint
TO_EXCLUSIVE = {"cmp.le": "cmp.lt", "cmp.ge": "cmp.gt"}       # drop_inclusive_endpoint
MAX_TRIES = 2000

# ------------------------------------------------------------------------------------------------ pools (stand-ins)
PEOPLE = ("Priya Raman", "Tomas Lindqvist", "Ana Ruiz", "Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell",
          "Aiko Brandt", "Jonas Feld", "Nadia Kowal", "Owen Pryce", "Sara Ilves", "Malik Osei", "Ines Duarte",
          "Kofi Mensah", "Hana Sato", "Lucas Brenner", "Eva Marsh", "Theo Kalnins", "Yara Haddad", "Bruno Lacerda",
          "Freya Holm", "Iris Vance", "Omar Saleh", "Clara Weiss", "Felix Ortega", "Maya Lindgren", "Paolo Greco",
          "Ruth Adeyemi", "Simon Achterberg", "Talia Brook", "Vikram Desai", "Wen Zhao", "Zoe Carrick", "Aaron Pike",
          "Bea Novak", "Caleb Strand", "Dina Farouk", "Elias Moreau", "Gita Rao")
RESERVE_PEOPLE = ("Quinn Arbeloa", "Rosa Templeton", "Ugo Barzani", "Vera Lindahl")    # G4 renames only
ROLE_TITLES = ("Head of Procurement", "Procurement Manager", "Finance Controller", "Legal Counsel", "VP Operations",
               "Category Lead", "Senior Buyer", "Contracts Analyst", "Treasury Lead", "Internal Auditor",
               "Security Lead", "Facilities Manager", "Chief of Staff", "Project Sponsor", "Budget Owner",
               "Compliance Officer", "Regional Director", "Operations Analyst", "Vendor Manager", "Payroll Lead")
APPR_PACKS = {
    "contracts": ("vendor contract sign-off", ("vendor contract", "supplier renewal", "framework agreement")),
    "capex": ("capital purchase sign-off", ("forklift purchase", "office fit-out", "server rack order")),
    "software": ("software renewal sign-off", ("analytics licence", "design tool renewal", "helpdesk subscription")),
    "travel": ("travel budget sign-off", ("conference trip", "client visit", "team offsite")),
    "marketing": ("marketing spend sign-off", ("trade show booth", "print campaign", "video shoot")),
    "hiring": ("hiring budget sign-off", ("contractor extension", "agency fee", "relocation package")),
}
AGENT_PACKS = {
    "office": (("calendar.read", "calendar.write", "mail.read", "mail.send", "files.read", "files.write",
                "files.share", "contacts.read", "contacts.write", "docs.share"),
               ("calendar cleanup", "newsletter send", "meeting booking", "document filing")),
    "finance": (("billing.read", "billing.write", "payments.create", "payments.refund", "invoices.read",
                 "invoices.send", "ledger.read", "ledger.post", "reports.export", "vendors.read"),
                ("invoice run", "customer refund", "expense report", "vendor payout")),
    "devops": (("repo.read", "repo.push", "ci.run", "ci.stop", "deploy.staging", "deploy.prod", "logs.read",
                "secrets.read", "tickets.read", "tickets.update"),
               ("release build", "log review", "ticket sweep", "staging deploy")),
    "travel": (("trips.read", "trips.book", "hotels.book", "cars.book", "cards.charge", "profiles.read",
                "profiles.write", "receipts.upload", "policy.read", "visas.apply"),
               ("travel booking", "hotel change", "visa filing", "receipt upload")),
}
RESERVE_SCOPES = ("archive.read", "archive.write", "audit.read", "notes.write", "wiki.edit", "maps.read")
AGENT_IDS = ("planner-a", "orchestrator-b", "mail-helper", "booking-agent", "ledger-bot", "research-agent",
             "filing-bot", "sync-worker", "triage-bot", "billing-runner", "scheduler-c", "report-writer",
             "deploy-bot", "intake-agent", "refund-helper", "travel-desk")
RESERVE_AGENTS = ("relay-agent-x", "relay-agent-y")
OFFSETS = (0, 60, 120, -300, -180, 330, 540, -480, 180, -240)          # minutes east of UTC (fixed; no DST)
OFFSETS_S5 = (345, -570, 525, 630)
BOUNDS = (500000, 1000000, 2000000, 2500000, 5000000, 7500000, 10000000)

# ------------------------------------------------------------------------------------------------ pools (wired)
POOLS_V2 = HERE / "pools_v2"
TRAIN_SAMPLERS = ("S1", "S2", "S3", "S4")
CARDS = 6                                       # per (sampler, track); card parity fixes the window-end rule
N_PACKS_TRAIN = len(TRAIN_SAMPLERS) * CARDS     # 24 training cards per track, one pack each (spec 3.0)
N_PACKS_S5 = CARDS                              # 6 packs reserved for the held-out S5 cards per track (G0 section 7)
I1_QUARANTINED_SKINS = frozenset((
    # F01: every skin with {cap|ITEM} fails G3 (skin._decode_groups parses 'Agency fee' for the value 'agency fee')
    "T31-agent-json-q3bc4997384", "T31-agent-json-q87a9dcf9d1", "T31-agent-json-q9047802674",
    "T31-agent-json-qf68674d931", "T31-agent-log-q209fd532de", "T31-agent-log-q8c7d28c9ec",
    "T31-agent-log-qa681d69ca2", "T31-agent-memo-qc8551515c9", "T31-agent-ticket-q14267cd2ac",
    "T31-agent-yaml-q0d2dd10ac5", "T31-agent-yaml-q47d051f5c8", "T31-agent-yaml-q6da22b5ed9",
    "T31-agent-yaml-qa7385397e3", "T31-agent-yaml-qd34a574f8d", "T31-appr-export-q0446ebd718",
    "T31-appr-json-qec9a3e7f5a", "T31-appr-log-q8f6aea4d30", "T31-appr-log-qaac6bc73a0",
    "T31-appr-memo-qaf3d8f072b", "T31-appr-ticket-qca07b4c90a"))
I1_QUARANTINED_DOCUMENTS = frozenset((
    # F03: Mode F documents that keep a first name of the authoring example outside the REQUESTER slot (12 of 116)
    "T31-agent-F-chat-q2fc9aab6f0", "T31-agent-F-chat-q4cb353636f", "T31-agent-F-email-q9f89d3930a",
    "T31-agent-F-email-qa8d0689de9", "T31-agent-F-email-qe967ad76e2", "T31-agent-F-transcript-q23a5fd7978",
    "T31-agent-F-transcript-qad54f497e2", "T31-agent-F-transcript-qcf1aaab38e", "T31-agent-F-transcript-qd643c95d12",
    "T31-agent-F-export-q6febc32dea", "T31-agent-F-runbook-q02bdc78a78", "T31-agent-F-runbook-q92c5a523c8"))
# PILOT_VERDICT watch item: narrative filler that reads like a capability or approval claim ("the setup looks good",
# "the agent has what it takes", "Spend fits the plan") is label-independent (G7 found no feature) but it is an
# outcome-like statement a skin must not make (G0 section 7): such skins and documents are screened out
CLAIM_PHRASES = ("looks good", "looks tidy", "looks fine", "setup looks", "what it takes", "fits the plan", "in good shape",
                 "good to go", "all set", "well within")
_PRONOUN = re.compile(r"(?<![\w-])(?:he|she|him|her|hers|his|himself|herself)(?![\w-])", re.I)
_WORD_TOKEN = re.compile(r"[A-Za-z][A-Za-z'-]*")
_LOWER_PARTICLES = frozenset(("de", "da", "di", "del", "della", "van", "von", "der", "den", "la", "le", "bin", "al",
                              "el", "du", "dos", "das", "ter", "ten", "op", "af"))


def pool_problems(packs: dict) -> list:
    """Shape problems of the wired pools (an empty list = usable)."""
    out = []
    ap, gp, names = packs.get("appr", ()), packs.get("agent", ()), packs.get("names", ())
    if len(ap) < N_PACKS_TRAIN + N_PACKS_S5 or len(gp) < N_PACKS_TRAIN + N_PACKS_S5:
        out.append(f"need >= {N_PACKS_TRAIN + N_PACKS_S5} packs per track, have {len(ap)} appr / {len(gp)} agent")
    for i, p in enumerate(ap):
        if not (isinstance(p.get("process"), str) and len(p.get("items", ())) >= 3 and len(p.get("roles", ())) >= 12):
            out.append(f"appr pack {i}: process, >= 3 items, >= 12 roles")
        elif len(set(p["roles"])) != len(p["roles"]):
            out.append(f"appr pack {i}: duplicate roles")
    for i, p in enumerate(gp):
        if not (len(p.get("scopes", ())) >= 10 and len(p.get("tasks", ())) >= 3 and len(p.get("agents", ())) >= 3):
            out.append(f"agent pack {i}: >= 10 scopes, >= 3 tasks, >= 3 agents")
        elif len(set(p["scopes"])) != len(p["scopes"]) or len(set(p["agents"])) != len(p["agents"]):
            out.append(f"agent pack {i}: duplicate scopes or agents")
    if len(names) < 200 or len(set(names)) != len(names):
        out.append("names: >= 200 distinct")
    return out


def load_packs(root: Path = POOLS_V2) -> dict:
    """The frozen pools_v2 packs (34 appr, 36 agent) and names (320), sha256-checked against the pool MANIFEST (a
    changed frozen pool is refused). {"appr": tuple of dicts, "agent": tuple, "names": tuple}."""
    root = Path(root)
    raw = (root / "packs.json").read_bytes()
    want = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))["sha256"]["packs.json"]
    if hashlib.sha256(raw).hexdigest() != want:
        raise ContractError("pools_v2/packs.json no longer matches its frozen sha256")
    d = json.loads(raw.decode("utf-8"))
    return {"appr": tuple(d["appr"]), "agent": tuple(d["agent"]), "names": tuple(d["names"])}


def claim_phrases(text: str) -> list:
    low = text.lower()
    return [f"claim phrase {c!r}" for c in CLAIM_PHRASES if c in low]


def freeform_leaks(text: str, brief) -> list:
    """F03: problems of a Mode F document that make the FILLED text name two people or contradict the filled name.
    brief: [(slot, brief value)]. Every word of the REQUESTER brief value (first name, last name) must occur only
    inside that value's verbatim occurrences; no gendered pronoun (the filled name may be of another gender)."""
    out = []
    vals = dict(brief)
    req = vals.get("REQUESTER", "")
    rest, pos = [], 0
    spans = sorted((m.start(), m.end()) for m in re.finditer(r"(?<![\w])" + re.escape(req) + r"(?![\w])", text)) \
        if req else []
    for a, b in spans:
        rest.append(text[pos:a])
        pos = b
    rest.append(text[pos:])
    outside = " ".join(rest)
    toks = {t.lower() for t in _WORD_TOKEN.findall(req)} - _LOWER_PARTICLES
    for t in sorted(toks):
        if re.search(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", outside, re.I):
            out.append(f"name word {t!r} outside the REQUESTER value")
    m = _PRONOUN.search(outside)
    if m:
        out.append(f"gendered pronoun {m.group()!r}")
    return out


# ------------------------------------------------------------------------------------------------ card text (G0 v1.2)
# The rule block in three styles (c2_kit.cards; spec 3.0 "a short or no card on about 15% of rows"). Same rules, same
# clauses: cards.variant_problems(full, variant) is clean for compact and short (tests). {END} and {TIMES} are program
# placeholders, replaced by _rules(); no digit appears in card text. The old heading line is gone (F09 B): the
# approver is defined in the "first level" bullet, and the agent bullet states what "may use" means.
END_PHRASE = {"incl": "through its end time (the end time is included)",
              "excl": "until its end time (the end time is excluded)"}
END_PHRASE_SHORT = {"incl": "through its end time (included)", "excl": "until its end time (excluded)"}
CLOSED_WORLD = "The listed records are complete: no other record exists."
TIME_RULE = {False: "Compare times as instants.",
             True: "Compare times as instants; a time in another offset shows the same instant in square brackets."}
CARD_STYLES = {"full": 0.20, "compact": 0.65, "short": 0.15}         # draw_style; short <= the 15% of spec 3.0
CARD_TEXT = {
    "appr": {
        "full": (
            "- A delegation covers the request when the amount is in its band and the request time is from its start "
            "time {END}, before any revocation of it.\n"
            "- An override covers the request when the amount is in its band and the request time is at or after its "
            "issue time.\n"
            "- The first level with a covering record decides the approver (the holder of the accountable (A) role): "
            "overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked "
            "A in the standing RACI matrix.\n"
            "- If that level gives two different people, the answer is \"" + ESCALATE_TEXT + "\". {TIMES}\n"
            "- Listing order and who issued a record do not matter.\n" + CLOSED_WORLD),
        "compact": (
            "- A delegation covers the request when the amount is in its band and the request time is from its start "
            "{END}, before any revocation of it; an override, when the amount is in its band and the request time is "
            "at or after its issue time.\n"
            "- The first level with a covering record decides the approver (the holder of the accountable (A) role): "
            "overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked "
            "A in the RACI matrix.\n"
            "- If that level gives two different people, the answer is \"" + ESCALATE_TEXT + "\". {TIMES}\n"
            "- Listing order and who issued a record do not matter. " + CLOSED_WORLD),
        "short": (
            "- Delegation: covers the request if the amount is in its band and the request time is from its start "
            "{END}, before any revocation of it. Override: covers it if the amount is in its band and the request time "
            "is at or after its issue time.\n"
            "- Approver (holder of the accountable (A) role): the first level with a covering record decides; "
            "overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person "
            "marked A in the RACI matrix.\n"
            "- If that level gives two different people: \"" + ESCALATE_TEXT + "\". {TIMES}\n"
            "- Listing order and who issued a record do not matter. " + CLOSED_WORLD)},
    "agent": {
        "full": (
            "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists "
            "the scope, the instant is from the grant's start time {END}, no revocation of that scope from that agent "
            "or of the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made "
            "its grant) may use the scope at that instant.\n"
            "- {TIMES}\n"
            "- Listing order and who issued a revocation do not matter.\n" + CLOSED_WORLD),
        "compact": (
            "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists "
            "the scope, the instant is from the grant's start {END}, no revocation of that scope from that agent or of "
            "the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its "
            "grant) may use the scope at that instant. {TIMES}\n"
            "- Listing order and who issued a revocation do not matter. " + CLOSED_WORLD),
        "short": (
            "- Each agent holds one grant. It may use a scope at an instant exactly when its grant lists the scope, "
            "the instant is from the grant's start {END}, no revocation of that scope from that agent or of the "
            "whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its grant) "
            "may use the scope then. {TIMES}\n"
            "- Listing order and who issued a revocation do not matter. " + CLOSED_WORLD)}}
APPR_RULES, AGENT_RULES = CARD_TEXT["appr"]["full"], CARD_TEXT["agent"]["full"]

# ------------------------------------------------------------------------------------------------ shares
# Base question forms (share of base specs). The agent yes/no base is drawn from all four agent forms (F06: the
# yes = bad share was 24.6%); the double-negation forms are drawn only while the lexicon admits a polarity-clean
# wording of them (_available), else they fall back to the plain base form: yn_holder 0.21, yn_agent_ok 0.11.
BASE_SHARES = (("ch_approver", 0.36), ("yn_holder", 0.15), ("yn_holder_dneg", 0.04), ("yn_agent_ok", 0.07),
               ("yn_agent_dneg", 0.04), ("yn_agent_beyond", 0.04), ("yn_agent_lacks", 0.04), ("yn_agent_not", 0.04),
               ("ch_scope", 0.22))
FALLBACK_FORM = {"yn_holder_dneg": "yn_holder", "yn_agent_dneg": "yn_agent_ok"}
P_SHAPE_B = 0.30                    # shown rows with one delegation and two overrides (the others: two delegations, one notice)
SHOWN_ESCALATE_LIKE = True          # a row that shows the escalate option has the escalate-like shape whatever its gold
APPR_ABSTAIN_SHOW = 0.40            # share of ch_approver rows that show the escalate option (choiceplan show_rate)
CHOICE_KS = (3, 4)                  # option counts, escalate included when shown
# P(gold is escalate | shown) is 1/k (choiceplan default): about 11.7% of the ch_approver base rows, about 7.5% of all
# ch_approver rows once the twins (which exist only where escalate is not shown) are counted (G0: 5-12%)
TIER_NON_ESCALATE = (("override", 0.30), ("delegation", 0.32), ("default", 0.29))
YN_TIER_SHARES = (("override", 1 / 3), ("delegation", 1 / 3), ("default", 1 / 3))
COMPLEMENTS = {"yn_holder": (("yn_holder_other", 0.6), ("yn_holder_not", 0.4)),
               "yn_holder_dneg": (("yn_holder_not", 1.0),),
               "yn_agent_ok": (("yn_agent_beyond", 0.3), ("yn_agent_lacks", 0.3), ("yn_agent_not", 0.4)),
               "yn_agent_dneg": (("yn_agent_not", 1.0),),
               "yn_agent_beyond": (("yn_agent_ok", 1.0),), "yn_agent_lacks": (("yn_agent_ok", 1.0),),
               "yn_agent_not": (("yn_agent_ok", 1.0),)}
P_COMPLEMENT, P_EQUIV, P_INV = 0.42, 0.15, 0.10
P_TWIN = {"yn": 0.60, "ch": 1.0}        # twin proposals per base spec (yes/no, ch_approver); ch_scope has no twin
P_TWIN_FEASIBLE = 0.90              # F05: a yes/no base (either answer) has a one-slot flip with this probability
SAMPLER_STYLE = {"S1": "list", "S2": "list", "S3": "log", "S4": "list", "S5": "log"}
S4_REGISTERS = ("transcript", "chat", "email")
# F09 D: record counts that keep the family mean at <= 800 rendered tokens (a delegation line costs about 62 tokens,
# a notice 61-69, a grant 84, a matrix line 10.5); the distributions keep every G0 trap reachable
N_DELEGATIONS = {"S1": (1, 1, 1, 2), "S2": (1, 1, 2), "S3": (1, 2, 2), "S4": (1, 1, 1, 2), "S5": (1, 2)}
N_NOTICES = {"S1": (0, 0, 1, 1), "S2": (1, 1, 1), "S3": (0, 0, 1), "S4": (1, 1), "S5": (0, 1, 1)}
N_REVOCATIONS = {"S2": (1, 1), "default": (0, 1, 1)}
MATRIX_SIZES = {"S1": (6, 6, 6, 7), "S2": (6, 6, 6, 7), "S3": (7, 8, 8), "S4": (6, 6, 6, 7), "S5": (6, 7, 8)}
P_CONVERSION = {"S1": 0.2, "S2": 0.2, "S3": 0.2, "S4": 0.4, "S5": 0.2}
START = (("before_far", 92), ("after_far", 5), ("after_1", 3))
START_EDGE = (("before_far", 80), ("after_1", 15), ("at", 5))
END_ANY = (("after_far", 58), ("after_1", 13), ("at", 11), ("before_1", 8), ("before_far", 10))
END_EDGE = (("after_1", 30), ("at", 30), ("before_1", 30), ("after_far", 10))
END_LIVE = (("after_far", 60), ("after_1", 15), ("at", 15), ("before_1", 5), ("before_far", 5))
NOTICE = (("before_1", 24), ("before_far", 32), ("at", 6), ("after_1", 20), ("after_far", 18))
NOTICE_EDGE = (("before_1", 45), ("at", 15), ("after_1", 40))
# register-first skin pick (P1): weights per unit; S4 draws only transcript / chat / email
REGISTER_WEIGHTS = (("transcript", 5.4), ("chat", 5.4), ("email", 5.4), ("memo", 16.8), ("ticket", 16.8),
                    ("json", 16.8), ("yaml", 16.8), ("log", 16.8))
SKIN_ROW_CAP = 6                    # P2: rows per skin (spec 3.0)
PLAN_BLOCK = 1024                   # seeds per block (per sampler) of the stratified escalate gold, gold position and gold rank

QUESTION_FORMS = (
    QuestionForm("ch_approver", "choice", answer_set="open", abstain=True),
    QuestionForm("yn_holder", "noul", "holds_a", 1),
    QuestionForm("yn_holder_dneg", "noul", "holds_a", 1),
    QuestionForm("yn_holder_other", "noul", "holds_a", -1, "implicit"),
    QuestionForm("yn_holder_not", "noul", "holds_a", -1, "syntactic"),
    QuestionForm("yn_agent_ok", "noul", "agent_may_use", 1, yes_is_bad=False),
    QuestionForm("yn_agent_dneg", "noul", "agent_may_use", 1, yes_is_bad=False),
    QuestionForm("yn_agent_beyond", "noul", "agent_may_use", -1, "antonym", yes_is_bad=True),
    QuestionForm("yn_agent_lacks", "noul", "agent_may_use", -1, "implicit", yes_is_bad=True),
    QuestionForm("yn_agent_not", "noul", "agent_may_use", -1, "syntactic", yes_is_bad=True),
    QuestionForm("ch_scope", "choice", answer_set="open"),
)
TRACK = {q.qform: ("appr" if q.qform == "ch_approver" or q.qform.startswith("yn_holder") else "agent")
         for q in QUESTION_FORMS}
POLARITY = {q.qform: q.polarity for q in QUESTION_FORMS}
# The negative / antonym predicates of "holds the A role" and "may use the scope" that negcount does not list
# (c2_kit.polarity P1-P4). negcount's own implicit cues (lack, other than, deny, without ...) count too.
NEGATIVE_PREDICATES = (
    r"exceed(?:s|ed|ing)?", r"beyond", r"outside", r"out\s+of\s+bounds", r"overstep(?:s|ped|ping)?",
    r"unauthori[sz]ed", r"forbid(?:s|den|ding)?|forbade", r"prohibit(?:s|ed|ing)?", r"bar(?:s|red|ring)?",
    r"block(?:s|ed|ing)?", r"revok(?:e|es|ed|ing)", r"withh(?:o|e)ld(?:s|ing)?", r"restrict(?:s|ed|ing)?",
    r"disallow(?:s|ed|ing)?", r"unentitled", r"ineligible",
)

# ------------------------------------------------------------------------------------------------ error models
register_name("t31_default_holder", "takes the standing A holder of the matrix and ignores delegations and overrides")
register_name("t31_ignore_window_end", "keeps a delegation or grant in force after its window has ended")
register_name("t31_future_notice", "applies a notice or revocation issued after the request time")
register_name("t31_ignore_band", "ignores the amount band of delegations and overrides")
register_name("t31_earliest_override", "lets the earliest-issued covering override decide instead of the latest")
register_name("t31_delegation_beats_override", "lets a covering delegation beat a covering override")
register_name("t31_responsible_role", "picks the role marked R (responsible) instead of the accountable one")
register_name("t31_issuer_as_holder", "picks the person who issued the latest notice in force")
register_name("t31_ignore_attenuation", "lets a sub-agent use a scope its parent agent cannot use")
register_name("t31_inherit_parent", "gives a sub-agent every scope its parent may use, listed in its grant or not")
APPR_EM = ("t31_default_holder", "ignore_revocation", "t31_ignore_window_end", "t31_future_notice",
           "add_exclusive_endpoint", "drop_inclusive_endpoint", "t31_ignore_band", "skip_offset_conversion",
           "t31_earliest_override", "t31_delegation_beats_override", "first_match", "last_match",
           "t31_responsible_role", "t31_issuer_as_holder")
SCOPE_EM = ("t31_ignore_attenuation", "t31_inherit_parent", "ignore_revocation", "t31_future_notice",
            "skip_offset_conversion")


# ------------------------------------------------------------------------------------------------ helpers

def _draw(u: float, shares: tuple) -> str:
    acc = 0.0
    for key, share in shares:
        acc += share
        if u < acc:
            return key
    return shares[-1][0]


def _draw_norm(u: float, shares: tuple) -> str:
    """_draw over shares that do not sum to 1 (renormalised)."""
    return _draw(u * sum(x for _, x in shares), shares)


def _yes_target(sampler: str, seed: int) -> bool:
    """Label-first target bit: the two seeds of a pair (2k, 2k + 1) share the question form and get opposite targets,
    so every yes/no form is exactly 50% yes over any run of whole seed pairs (G0 section 4)."""
    return (uhash(FAMILY, "yes", sampler, seed // 2) < 0.5) != bool(seed % 2)


def _wchoice(rng: random.Random, dist: tuple) -> str:
    return rng.choices([k for k, _ in dist], weights=[w for _, w in dist])[0]


def _kind_time(rng: random.Random, t: dt.datetime, kind: str) -> dt.datetime:
    if kind == "before_far":
        return t - MINUTE * rng.randint(95, 20 * 1440)
    if kind == "after_far":
        return t + MINUTE * rng.randint(95, 12 * 1440)
    return t + MINUTE * {"before_1": -1, "at": 0, "after_1": 1}[kind]


def _tz(minutes: int) -> dt.timezone:
    return dt.timezone(dt.timedelta(minutes=minutes))


def _offset_minutes(tz: dt.timezone) -> int:
    return int(tz.utcoffset(None).total_seconds() // 60)


def _new_id(rng: random.Random, prefix: str, used: set) -> str:
    while True:
        x = f"{prefix}-{rng.randrange(1000, 10000)}"
        if x not in used:
            used.add(x)
            return x


def _band_text(rec: dict) -> str:
    return f"{{{rec['band']}}}" if rec.get("band") else NO_BAND


def _fits(v: dict, rec: dict, amount: int) -> bool:
    if not rec.get("band"):
        return True
    b = v[rec["bound"]]
    return {"cmp.le": amount <= b, "cmp.lt": amount < b, "cmp.ge": amount >= b, "cmp.gt": amount > b}[v[rec["band"]]]


def _edge_bound(sem: str, amount: int, ok: bool) -> int:
    """The bound that flips this band's verdict at `amount` (twins: the amount lands on or next to the edge)."""
    if sem == "cmp.le":
        return amount - 1 if ok else amount
    if sem == "cmp.lt":
        return amount if ok else amount + 1
    if sem == "cmp.ge":
        return amount + 1 if ok else amount
    return amount if ok else amount - 1


def _decide(st: dict) -> tuple:
    """Construction table -> (tier, holder): latest covering override > covering delegation > default."""
    live = [o for o in st["ovr"] if o["issued"] and o["band"]]
    if live:
        last = max(o["t"] for o in live)
        names = {o["to"] for o in live if o["t"] == last}
        return ("override", next(iter(names))) if len(names) == 1 else ("escalate", ESCALATE)
    names = {d["to"] for d in st["del"] if d["started"] and d["not_ended"] and not d["revoked"] and d["band"]}
    if len(names) == 1:
        return "delegation", next(iter(names))
    if names:
        return "escalate", ESCALATE
    return "default", st["default"]


def _usable(levels: list) -> bool:
    return all(x["started"] and x["not_ended"] and not x["whole"] and x["has"] and not x["srev"] for x in levels)


def _agent_answer(qform: str, ok: bool):
    return ok if qform == "ch_scope" else int(ok if POLARITY[qform] == 1 else not ok)


def _ident(x):
    return x


TRACK_TAG = re.compile(r"(?:^|[-_.:])(appr|agent)(?=[-_.:]|$)")


def skin_track(skin) -> str | None:
    """G0 section 7: a narrative skin or attack line written for one track carries "appr" or "agent" as a
    separate part of its id (T31-appr-memo-0007); a skin without a tag fits both tracks."""
    m = TRACK_TAG.search(skin.skin_id)
    return m.group(1) if m else None


def _fits_track(skin, track: str) -> bool:
    return skin.family != FAMILY or skin.kind not in ("skin", "attack") or skin_track(skin) in (None, track)


def _name_tokens(name: str) -> frozenset:
    """The name words that must not repeat inside a row (particles such as 'de' do not count)."""
    return frozenset(t.lower() for t in _WORD_TOKEN.findall(name)) - _LOWER_PARTICLES


@dataclass
class T31Ctx(KitCtx):
    """KitCtx whose skin pick is register-first (P1: the register is drawn first, label-blind, with the REGISTER_WEIGHTS;
    each register is then about 12.5% of the units) and, when the plugin sets skin_row_cap (P2), skips a skin that
    would feed more than the cap in rows. The plugin counts the rows a unit may add (base pick: the base row plus its
    complement, twin and attack partners; equiv pick: one row)."""
    plug: Any = None

    def pick(self, family: str, kind: str, row_key: str, *, register: str | None = None, qform: str | None = None,
             exclude: tuple = (), held_out: bool = False, need: int = 1):
        if kind != "skin" or self.plug is None:
            return super().pick(family, kind, row_key, register=register, qform=qform, exclude=exclude,
                                held_out=held_out)
        c = [s for s in self.skins.values() if s.family == family and s.kind == kind and s.held_out == held_out
             and (register is None or s.register == register) and s.skin_id not in exclude]
        if not c:
            raise LookupError(f"no {kind} for {family} (register={register}, held_out={held_out})")
        if register is None:
            regs = sorted({s.register for s in c})
            w = dict(REGISTER_WEIGHTS)
            weights = [w.get(r, 5.4) for r in regs] if not held_out else [1.0] * len(regs)
            u, acc, pick = uhash(row_key, "register") * sum(weights), 0.0, regs[-1]
            for r, x in zip(regs, weights):
                acc += x
                if u < acc:
                    pick = r
                    break
            c = [s for s in c if s.register == pick]
        cap = self.plug.skin_row_cap
        if cap:
            use = self.plug._skin_rows
            room = [s for s in c if use.get(s.skin_id, 0) + need <= cap]
            if room:
                c = room
            else:                        # a pool too small to honour the cap (the in-memory test fixtures): plain pick
                self.plug.cap_overflow += 1
        s = min(c, key=lambda s: uhash(row_key, kind, s.skin_id))
        if cap:
            self.plug._skin_rows[s.skin_id] = self.plug._skin_rows.get(s.skin_id, 0) + need
        return s


class T31(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "1b0668c7a35dbc680ff1573bf79619f2d4a8a55dbd61b6b19308695b1f3bdfd0"   # frozen v1.2 (fix iteration 1); v1.1 = POOL_G0_SHA256
    G0_HAIKU_TASK = "c2-data-stage-a:amb:T31"     # the one Haiku ambiguity pass (45 points; G0 section 8)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "interval_scan"
    SOLVER_B_MODULE = "families.T31.solver_b"
    QFORMS = {q.qform: q for q in QUESTION_FORMS}
    LABEL_WORDS = ("escalate", "escalation", "authorised", "authorized", "unauthorised", "unauthorized",
                   "no unique approver")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "log", "transcript", "runbook", "export")
    HELD_OUT_REGISTERS = ("runbook", "export")
    GSL_EXCEPTIONS = {"approval": "T31 requests are approval requests: the word names the request type, never an "
                                  "outcome (G0 section 7)",
                      "grant": "a grant is a T31 record type: the noun names the record, never its status (G0 7)"}
    NAME_ALLOW = ("RACI", "UTC", "IT", "HR", "VP", "API", "A")     # "A": the RACI letter ("the accountable (A) role")
    POLARITY_CHECK = True                 # c2_kit.polarity: yes/no wordings must read with their form's polarity
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_STRICT_FRAMES = True         # no pool wording uses "aux + subject + not" (checked); keep it that way
    LENGTH_BALANCE = True                 # choice options ranked by visible length, the gold at its planned rank

    def __init__(self, lexicon=None, packs=None):
        """packs None: the frozen pools_v2 packs and names (load_packs(), sha256-checked). Every pack is checked
        (pool_problems) before any row is drawn. skin_row_cap (P2, default SKIN_ROW_CAP = 6; None switches it off): a
        skin that would feed more rows is skipped while another skin of the register has room. The row count lives
        in this instance, so one instance serves one generation run."""
        super().__init__(lexicon)
        self._ems = None
        self._cmp_forms = {}
        packs = load_packs() if packs is None else packs
        probs = pool_problems(packs)
        if probs:
            raise ContractError("T31 packs / names: " + "; ".join(probs[:5]))
        self.names = tuple(packs["names"])
        self._name_toks = {n: _name_tokens(n) for n in self.names}
        self.pack_by_id = {f"t31:{t}:p{i:02d}": p for t in ("appr", "agent") for i, p in enumerate(packs[t])}
        self._ranked = {t: sorted(range(len(packs[t])),
                                  key=lambda i, t=t: uhash(FAMILY, "packrank", t, json.dumps(packs[t][i], sort_keys=True)))
                        for t in ("appr", "agent")}
        self.skin_row_cap = SKIN_ROW_CAP     # P2; None switches the count off
        self.cap_overflow = 0                # picks that found no skin with room left (a pool too small for the cap)
        self._skin_rows: dict = {}
        self._screened: list = []             # [(ctx, screened ctx, {skin id: why})]
        self._rel_cache: dict = {}
        self._plan_cache: dict = {}
        self._block_cache: dict = {}
        self.dneg_ok = {q: self._clean_forms(q) for q in FALLBACK_FORM}

    # ============================================================================================ pools, packs, names
    def pack_for(self, sampler: str, track: str, card: int) -> tuple:
        """(pack id, pack) of a card: one pack per card (24 training cards + 6 S5 cards per track), the packs ranked by a
        hash of their own content so that no pack is tied to an input order (F10)."""
        i = (TRAIN_SAMPLERS.index(sampler) * CARDS + card) if sampler in TRAIN_SAMPLERS else (N_PACKS_TRAIN + card)
        idx = self._ranked[track][i]
        pid = f"t31:{track}:p{idx:02d}"
        return pid, self.pack_by_id[pid]

    def draw_names(self, rng: random.Random, k: int, avoid=()) -> list:
        """k names from the 320 of the pool; no two people of a row share a first or a last name word."""
        seen = set().union(*(self._name_toks.get(n, _name_tokens(n)) for n in avoid)) if avoid else set()
        out: list = []
        pool = list(rng.sample(self.names, min(len(self.names), 4 * k + 12)))
        for n in pool:
            t = self._name_toks[n]
            if not t & seen:
                out.append(n)
                seen |= t
                if len(out) == k:
                    return out
        raise ContractError("T31: not enough distinct names in the pool")

    def _clean_forms(self, qform: str) -> bool:
        """True when the lexicon holds an admitted question form of `qform` whose wording passes the polarity rule
        (label-blind: the pool, not a row). Without a lexicon (contract checks) the form is not available."""
        if self.lexicon is None:
            return False
        sem = question_sem(FAMILY, qform)
        return any(f.sem_id == sem and f.kind == "question" and self.lexicon.status(f.form_id) == "admitted"
                   and not f.held_out and not POL.form_problems(self, qform, f.text)
                   for f in self.lexicon.forms.values())

    def available(self, qform: str) -> str:
        """The form a base draw really asks: a double-negation form falls back to its plain base form while no
        polarity-clean wording of it is admitted (F07: Haiku has to author them first)."""
        return qform if qform not in FALLBACK_FORM or self.dneg_ok.get(qform) else FALLBACK_FORM[qform]

    # ============================================================================================ context (ctx_for)
    def screen_pool(self, ctx) -> tuple:
        """(ctx without the quarantined pieces, {skin id: why}) - cached per context object. Quarantined: the 20
        {cap|ITEM} skins (F01), the Mode F documents that keep a name or a pronoun outside their slot (F03), and the
        wordings that break the c2_kit.polarity rule (F07 safety net)."""
        for c, screened, bad in self._screened:
            if c is ctx:
                return screened, bad
        bad: dict = {}
        for sid, sk in ctx.skins.items():
            if sk.family != FAMILY:
                continue
            if sid in I1_QUARANTINED_SKINS:
                bad[sid] = ["F01 {cap|ITEM} fails G3"]
            elif sk.kind == "skin":                    # (attack lines are fake authority claims by design: not screened)
                why = claim_phrases(sk.text)
                if sk.kind == "skin" and sk.author_mode == "F":
                    why = (["F03 listed document"] if sid in I1_QUARANTINED_DOCUMENTS else []) + freeform_leaks(
                        sk.text, sk.brief) + why
                if why:
                    bad[sid] = why
            elif sk.kind == "wording" and sk.qform:
                p = POL.form_problems(self, sk.qform, sk.text)
                if p:
                    bad[sid] = p
        screened = KitCtx(skins={k: v for k, v in ctx.skins.items() if k not in bad}, lexicon=ctx.lexicon)
        self._screened.append((ctx, screened, bad))
        return screened, bad

    def quarantined(self, ctx) -> dict:
        """{skin id: why} for the pieces ctx_for() leaves out of `ctx`."""
        return self.screen_pool(ctx)[1]

    def ctx_for(self, spec: Spec, ctx) -> KitCtx:
        """pipeline hook: the pool without the quarantined pieces and with only this track's skins and attack lines (and
        neutral ones), so an equiv partner or an inv attack line never comes from the other track (G0 section 7); the
        skin pick is register-first (P1) and, with skin_row_cap set, counts rows per skin (P2)."""
        base, _bad = self.screen_pool(ctx)
        track = spec.structure["track"]
        return T31Ctx(skins={sid: s for sid, s in base.skins.items() if _fits_track(s, track)}, lexicon=base.lexicon,
                      plug=self)

    # ============================================================================================ sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        if self.lexicon is None:
            raise ContractError("T31 needs its lexicon registry (T31(lexicon=...))")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        qform = self.available(_draw(uhash(FAMILY, "qform", sampler, seed // 2), BASE_SHARES))   # pairs share the form
        card = rng.randrange(CARDS)
        base = _tz(rng.choice(OFFSETS_S5 if sampler == "S5" else OFFSETS))
        day = dt.date(2026, 1, 5) + dt.timedelta(days=rng.randrange(0, 330))
        t_req = dt.datetime(day.year, day.month, day.day, rng.randint(7, 20), rng.randrange(60), tzinfo=base)
        ctx = {"seed": seed, "sampler": sampler, "qform": qform, "card": card, "tz": base,
               "T": t_req.astimezone(UTC), "end_rule": ("incl", "excl")[card % 2], "style": SAMPLER_STYLE[sampler]}
        if TRACK[qform] == "appr":
            return self._sample_appr(rng, ctx)
        if qform == "ch_scope":
            return self._sample_scope_choice(rng, ctx)
        return self._sample_agent_yn(rng, ctx)

    def _clause(self, sem: str, rng: random.Random, bound_slot: str) -> S.Slot:
        if sem not in self._cmp_forms:
            self._cmp_forms[sem] = sorted(f for f, x in self.lexicon.forms.items() if x.sem_id == sem
                                          and x.kind == "comparator" and self.lexicon.status(f) == "admitted")
        ids = self._cmp_forms[sem]
        if not ids:
            raise ContractError(f"no admitted comparator form for {sem}")
        return self.lexicon.clause(rng.choice(ids), bind={"X": bound_slot})

    def _odd_tz(self, rng, ctx) -> dt.timezone:
        pool = OFFSETS_S5 if ctx["sampler"] == "S5" else OFFSETS
        base = _offset_minutes(ctx["tz"])
        return _tz(rng.choice([o for o in pool if o != base]))

    def _card_id(self, ctx, track) -> str:
        return f"{FAMILY}:{ctx['sampler']}:{track}:c{ctx['card']:02d}"

    # -------------------------------------------------------------------------------------------- appr
    def _sample_appr(self, rng, ctx) -> Spec:
        seed, qform, sampler = ctx["seed"], ctx["qform"], ctx["sampler"]
        yes, plan = None, None
        if qform == "ch_approver":
            # the display plan comes first, from the row key (c2_kit.choiceplan): the outcome (escalate or not) is
            # planned, the structure is then drawn until solver A agrees; nothing is ever relabelled
            plan = self._plan_by(sampler, seed, qform)
            target = "escalate" if plan.gold_abstain else _draw_norm(uhash(FAMILY, "tier", sampler, seed),
                                                                   TIER_NON_ESCALATE)
        else:
            target = _draw(uhash(FAMILY, "tier", sampler, seed), YN_TIER_SHARES)
            yes = _yes_target(sampler, seed)
        want_twin = qform != "ch_approver" and uhash(FAMILY, "twinfeas", sampler, seed) < P_TWIN_FEASIBLE
        for _ in range(MAX_TRIES):
            spec = self._draw_appr(rng, ctx, target, shown=bool(plan is not None and plan.show_abstain))
            tier, holder = _decide(self._appr_status(spec))
            if tier != target:
                continue
            if yes is not None:
                cand = self._pick_candidate(spec, holder, yes)
                if cand is None:
                    continue
                spec.structure["candidate"] = cand
            spec = self.derive(spec)
            if self._appr_resolve(spec) != holder:
                raise ContractError(f"T31 seed {seed}: construction table and solver A disagree")
            if want_twin and self._twin(spec) is None:
                continue                  # F05: a yes/no base has a one-slot flip with probability 0.90 (both answers)
            if not self._options_ok(spec, strict=True):
                continue                  # a ch_approver case the planned (k, display, rank) cannot fill is redrawn
            return spec
        raise ContractError(f"T31 {ctx['sampler']} seed {seed}: no {target} spec in {MAX_TRIES} draws")

    def _draw_appr(self, rng, ctx, target, shown: bool = False) -> Spec:
        """shown: the row shows the escalate option. Then every row, whatever its gold, has the escalate-like shape (two
        delegations in their window; the band, a revocation or an override decides): the shape of an escalate gold is
        not a cue for the escalate option (G6 d_meta: record counts and number magnitudes predicted it)."""
        sampler, T, tz = ctx["sampler"], ctx["T"], ctx["tz"]
        like = shown and SHOWN_ESCALATE_LIKE
        live2 = target == "escalate" or like
        # the two escalate-like shapes (drawn per seed, never per attempt, so the shape says nothing about the target):
        # A = two delegations in their window + one notice, B = one delegation + two overrides (a tie needs one instant)
        shape_b = like and uhash(FAMILY, "shape", sampler, ctx["seed"]) < P_SHAPE_B
        edge = sampler == "S2"
        pack_id, pack = self.pack_for(sampler, "appr", ctx["card"])
        process, items = pack["process"], pack["items"]
        n = rng.choice(MATRIX_SIZES[sampler])
        people = self.draw_names(rng, n + 1)
        requester, org = people[-1], people[:-1]
        roles = rng.sample(pack["roles"], n)
        n_r = rng.choice((1, 2))
        letters = ["A"] + ["R"] * n_r + [rng.choice("CI") for _ in range(n - 1 - n_r)]
        rng.shuffle(letters)
        a_idx = letters.index("A")
        others = [i for i in range(n) if i != a_idx]
        nd = rng.choice(N_DELEGATIONS[sampler])
        nd = (1 if shape_b else 2) if like else (max(2, nd) if live2 else nd)
        delegates = rng.sample(others, nd)
        dels = []
        for i in range(nd):
            start = _kind_time(rng, T, _wchoice(rng, START_EDGE if edge else START))
            end_dist = END_LIVE if (live2 and i < 2) else (END_EDGE if edge else END_ANY)
            end = _kind_time(rng, T, _wchoice(rng, end_dist))
            if end <= start:
                start = end - MINUTE * rng.randint(1440, 20 * 1440)
            band = None
            if rng.random() >= (0.45 if live2 else 0.25):
                band = (rng.choice(sorted(CMP_OP)), rng.choice(BOUNDS))
            dels.append({"to": delegates[i], "start": start, "end": end, "band": band})
        notices = []
        if shape_b:
            t0 = _kind_time(rng, T, rng.choice(("before_1", "before_far", "at")))
            for p in rng.sample(others, 2):
                t = t0 if target == "escalate" else _kind_time(rng, T, _wchoice(rng, NOTICE_EDGE if edge else NOTICE))
                band = None if rng.random() < 0.45 else (rng.choice(sorted(CMP_OP)), rng.choice(BOUNDS))
                notices.append({"kind": "override", "t": t, "person": p,
                                "by": rng.choice([x for x in range(n) if x != p]), "band": band})
        else:
            revocable = list(range(nd))
            for _ in range(1 if like else rng.choice(N_NOTICES[sampler])):
                t = _kind_time(rng, T, _wchoice(rng, NOTICE_EDGE if edge else NOTICE))
                started = [i for i in revocable if dels[i]["start"] < t]   # G0 M6: issued after its start
                if started and rng.random() < 0.5:
                    i = rng.choice(started)
                    revocable.remove(i)
                    by = a_idx if rng.random() < 0.6 else rng.choice([x for x in others if x != delegates[i]])
                    notices.append({"kind": "revoke", "t": t, "target": i, "by": by})
                else:
                    p = rng.choice(others)
                    band = None if rng.random() < 0.45 else (rng.choice(sorted(CMP_OP)), rng.choice(BOUNDS))
                    notices.append({"kind": "override", "t": t, "person": p,
                                    "by": rng.choice([x for x in range(n) if x != p]), "band": band})
        bounds = [r["band"][1] for r in dels + notices if r.get("band")]
        if bounds and rng.random() < (0.6 if edge else 0.33):
            amount = rng.choice(bounds)
        else:
            amount = max(100, int(rng.choice(BOUNDS) * rng.uniform(0.3, 1.7)))
            if rng.random() < 0.5:
                amount = max(100, amount // 100 * 100)
        # time slots and their offsets (at most one time in a second offset: the conversion)
        tzs = {}
        if rng.random() < P_CONVERSION[sampler]:
            pick = ([("n", j) for j in range(len(notices))] or [("e", j) for j in range(nd)])
            tzs[rng.choice(pick)] = self._odd_tz(rng, ctx)
        odd = {("n", j): f"NOT_{j + 1}_TIME" for j in range(len(notices))}
        odd.update({("e", i): f"DEL_{i + 1}_END" for i in range(nd)})
        used: set = set()
        slots = {"PROCESS": S.name_slot(process), "REQUESTER": S.name_slot(requester),
                 "ITEM": S.name_slot(rng.choice(items)), "REQ_ID": S.id_slot(_new_id(rng, "REQ", used)),
                 "REQ_AMOUNT": S.cents_slot(amount), "REQ_TIME": S.datetime_slot(T.astimezone(tz))}
        for i in range(n):
            slots[f"ROLE_{i + 1}"] = S.name_slot(roles[i])
            slots[f"PERSON_{i + 1}"] = S.name_slot(org[i])

        def person(i):
            return f"PERSON_{i + 1}"

        d_struct, n_struct = [], []
        for i, d in enumerate(dels):
            k = f"DEL_{i + 1}"
            slots[f"{k}_ID"] = S.id_slot(_new_id(rng, "DLG", used))
            slots[f"{k}_START"] = S.datetime_slot(d["start"].astimezone(tz))
            slots[f"{k}_END"] = S.datetime_slot(d["end"].astimezone(tzs.get(("e", i), tz)))
            rec = {"id": f"{k}_ID", "from": person(a_idx), "to": person(d["to"]), "start": f"{k}_START",
                   "end": f"{k}_END", "band": None, "bound": None}
            if d["band"]:
                slots[f"{k}_BOUND"] = S.cents_slot(d["band"][1])
                slots[f"{k}_BAND"] = self._clause(d["band"][0], rng, f"{k}_BOUND")
                rec.update(band=f"{k}_BAND", bound=f"{k}_BOUND")
            d_struct.append(rec)
        for j, x in enumerate(notices):
            k = f"NOT_{j + 1}"
            slots[f"{k}_ID"] = S.id_slot(_new_id(rng, "NTC", used))
            slots[f"{k}_TIME"] = S.datetime_slot(x["t"].astimezone(tzs.get(("n", j), tz)))
            rec = {"id": f"{k}_ID", "kind": x["kind"], "time": f"{k}_TIME", "by": person(x["by"]), "target": None,
                   "person": None, "band": None, "bound": None}
            if x["kind"] == "revoke":
                rec["target"] = x["target"]
            else:
                rec["person"] = person(x["person"])
                if x["band"]:
                    slots[f"{k}_BOUND"] = S.cents_slot(x["band"][1])
                    slots[f"{k}_BAND"] = self._clause(x["band"][0], rng, f"{k}_BOUND")
                    rec.update(band=f"{k}_BAND", bound=f"{k}_BOUND")
            n_struct.append(rec)
        structure = {"track": "appr", "style": ctx["style"], "end_rule": ctx["end_rule"],
                     "base_offset": _offset_minutes(tz), "odd": next((odd[k] for k in tzs), None),
                     "matrix": [[f"ROLE_{i + 1}", person(i), letters[i]] for i in range(n)],
                     "default": person(a_idx), "delegations": d_struct, "notices": n_struct}
        spec = Spec(FAMILY, ctx["sampler"], ctx["seed"], self._card_id(ctx, "appr"), ctx["qform"], slots,
                    structure=structure, depth=2, deep=False, pack=pack_id)
        return spec.replace(tags=self._appr_tags(spec))

    def _pick_candidate(self, spec: Spec, holder: str, yes: bool):
        """yn_holder: the gold holder (yes) or the person the first error model (seeded order) names (no)."""
        v = spec.env()
        slot_of = {v[p]: p for _, p, _ in spec.structure["matrix"]}
        if holder == ESCALATE:
            return None
        if yes:
            return slot_of[holder]
        for name in sorted(APPR_EM, key=lambda m: uhash(FAMILY, "cand", spec.seed, m)):
            out = self._appr_resolve(spec, frozenset({name}))
            if out not in (None, ESCALATE, holder) and out in slot_of:
                return slot_of[out]
        return None

    def _appr_tags(self, spec: Spec) -> tuple:
        v, st = spec.env(), spec.structure
        T, amount = v["REQ_TIME"], v["REQ_AMOUNT"]
        tags = set()
        for x in st["notices"]:
            t = v[x["time"]]
            tags |= {"rev_1min"} if t == T - MINUTE else ({"notice_after"} if t == T + MINUTE else
                                                         ({"notice_at"} if t == T else set()))
        if amount in [v[r["bound"]] for r in st["delegations"] + st["notices"] if r.get("bound")]:
            tags.add("band_edge")
        status = self._appr_status(spec)
        if any(d["started"] and not d["not_ended"] for d in status["del"]):
            tags.add("lapsed")
        if any(not d["started"] for d in status["del"]):
            tags.add("not_started")
        if (sum(d["started"] and d["not_ended"] for d in status["del"]) >= 2
                or sum(o["issued"] for o in status["ovr"]) >= 2):
            tags.add("escalate_like")
        if st.get("odd"):
            tags.add("conversion")
        return tuple(sorted(tags))

    # -------------------------------------------------------------------------------------------- agent
    def _sample_agent_yn(self, rng, ctx) -> Spec:
        yes = _yes_target(ctx["sampler"], ctx["seed"])
        want_ok = yes if POLARITY[ctx["qform"]] == 1 else not yes        # the base form may be a negative one (F06)
        want_twin = uhash(FAMILY, "twinfeas", ctx["sampler"], ctx["seed"]) < P_TWIN_FEASIBLE
        for _ in range(MAX_TRIES):
            spec = self._draw_agent(rng, ctx, want_ok)
            ok = _usable(self._agent_status(spec, spec.env()["REQ_SCOPE"]))
            if ok != want_ok:
                continue
            spec = self.derive(spec)
            if self._agent_usable(spec, spec.env()["REQ_SCOPE"]) != ok:
                raise ContractError(f"T31 seed {ctx['seed']}: construction table and solver A disagree")
            if want_twin and self._twin(spec) is None:
                continue                  # F05 (see _sample_appr)
            return spec
        raise ContractError(f"T31 {ctx['sampler']} seed {ctx['seed']}: no agent spec with answer {yes}")

    def _depth(self, rng, ctx, minimum=1) -> int:
        if ctx["sampler"] in ("S1", "S3"):
            d = rng.choices((1, 2, 3), weights=(35, 57, 8))[0]
        else:
            d = rng.choices((1, 2), weights=(40, 60))[0]
        return max(minimum, d)

    def _draw_agent(self, rng, ctx, yes) -> Spec:
        """yes: the scope is usable (the answer to the plain 'may use' question)."""
        sampler, T = ctx["sampler"], ctx["T"]
        edge = sampler == "S2"
        depth = self._depth(rng, ctx)
        pack_id, pack = self.pack_for(sampler, "agent", ctx["card"])
        universe, items = pack["scopes"], pack["tasks"]
        universe = list(universe)
        rng.shuffle(universe)
        top = 6 if sampler == "S3" else 5
        lists = [rng.sample(universe, rng.randint(2, top))]
        for _ in range(1, depth):
            parent = lists[-1]
            want = rng.randint(2, top)
            outside = [x for x in universe if x not in parent]
            extra = min(1 if rng.random() < 0.6 else 0, len(outside))
            child = rng.sample(parent, min(len(parent), want - extra)) + rng.sample(outside, extra)
            rng.shuffle(child)
            lists.append(child)
        own = lists[-1]
        parent_only = [x for x in lists[-2] if x not in own] if depth > 1 else []
        outside = [x for x in universe if x not in own]
        if not yes and parent_only and rng.random() < 0.3:
            scope = rng.choice(parent_only)                       # the inherit trap: only the parent lists it
        elif yes or not outside or rng.random() < 0.85:
            scope = rng.choice(own)
        else:
            scope = rng.choice(outside)
        windows = []
        for _ in range(depth):
            start = _kind_time(rng, T, _wchoice(rng, START_EDGE if edge else START))
            end = _kind_time(rng, T, _wchoice(rng, END_EDGE if edge else (END_LIVE if yes else END_ANY)))
            if end <= start:
                start = end - MINUTE * rng.randint(1440, 20 * 1440)
            windows.append((start, end))
        revs, taken = [], set()
        for _ in range(rng.choice(N_REVOCATIONS["S2"] if edge else N_REVOCATIONS["default"])):
            j = rng.randrange(depth)
            t = _kind_time(rng, T, _wchoice(rng, NOTICE_EDGE if edge else NOTICE))
            if t <= windows[j][0]:
                continue                          # G0 M10: a revocation is issued after its grant's start
            if rng.random() < 0.2 and ("grant", j) not in taken:
                taken.add(("grant", j))
                target = ("grant", j, None)
            else:
                sc = scope if (scope in lists[j] and rng.random() < 0.5) else rng.choice(lists[j])
                if ("scope", j, sc) in taken:
                    continue
                taken.add(("scope", j, sc))
                target = ("scope", j, sc)
            revs.append((target, t, "parent" if (j > 0 and rng.random() < 0.5) else "principal"))
        return self._build_agent(rng, ctx, (pack_id, pack), items, lists, windows, revs, scope, depth)

    def _build_agent(self, rng, ctx, pack, items, lists, windows, revs, scope, depth) -> Spec:
        pack_id, pack = pack
        tz = ctx["tz"]
        tzs = {}
        if rng.random() < P_CONVERSION[ctx["sampler"]]:
            pick = [("r", i) for i in range(len(revs))] or [("e", j) for j in range(depth)]
            tzs[rng.choice(pick)] = self._odd_tz(rng, ctx)
        principal, requester = self.draw_names(rng, 2)
        agents = rng.sample(pack["agents"], depth)
        used: set = set()
        slots = {"PRINCIPAL": S.name_slot(principal), "REQUESTER": S.name_slot(requester),
                 "ITEM": S.name_slot(rng.choice(items)), "REQ_ID": S.id_slot(_new_id(rng, "TASK", used)),
                 "REQ_TIME": S.datetime_slot(ctx["T"].astimezone(tz))}
        if scope is not None:
            slots["REQ_SCOPE"] = S.id_slot(scope)
        grants = []
        for j in range(depth):
            g = f"GRANT_{j + 1}"
            slots[f"AGENT_{j + 1}"] = S.id_slot(agents[j])
            slots[f"{g}_ID"] = S.id_slot(_new_id(rng, "GRT", used))
            slots[f"{g}_START"] = S.datetime_slot(windows[j][0].astimezone(tz))
            slots[f"{g}_END"] = S.datetime_slot(windows[j][1].astimezone(tzs.get(("e", j), tz)))
            names = []
            for i, sc in enumerate(lists[j]):
                slots[f"G{j + 1}_S{i + 1}"] = S.id_slot(sc)
                names.append(f"G{j + 1}_S{i + 1}")
            grants.append({"id": f"{g}_ID", "by": "PRINCIPAL" if j == 0 else f"AGENT_{j}", "to": f"AGENT_{j + 1}",
                           "scopes": names, "start": f"{g}_START", "end": f"{g}_END"})
        r_struct = []
        for i, ((kind, j, sc), t, issuer) in enumerate(revs):
            r = f"REV_{i + 1}"
            slots[f"{r}_ID"] = S.id_slot(_new_id(rng, "RVK", used))
            slots[f"{r}_TIME"] = S.datetime_slot(t.astimezone(tzs.get(("r", i), tz)))
            rec = {"id": f"{r}_ID", "time": f"{r}_TIME", "by": "PRINCIPAL" if issuer == "principal" else f"AGENT_{j}",
                   "agent": f"AGENT_{j + 1}", "scope": None, "grant": None}
            if kind == "grant":
                rec["grant"] = j
            else:
                slots[f"{r}_SCOPE"] = S.id_slot(sc)
                rec["scope"] = f"{r}_SCOPE"
            r_struct.append(rec)
        odd = {("r", i): f"REV_{i + 1}_TIME" for i in range(len(revs))}
        odd.update({("e", j): f"GRANT_{j + 1}_END" for j in range(depth)})
        structure = {"track": "agent", "style": ctx["style"], "end_rule": ctx["end_rule"],
                     "base_offset": _offset_minutes(tz), "odd": next((odd[k] for k in tzs), None),
                     "chain": [f"AGENT_{j + 1}" for j in range(depth)], "grants": grants, "revocations": r_struct}
        spec = Spec(FAMILY, ctx["sampler"], ctx["seed"], self._card_id(ctx, "agent"), ctx["qform"], slots,
                    structure=structure, depth=depth, deep=depth > 2, pack=pack_id)
        return spec.replace(tags=self._agent_tags(spec))

    def _sample_scope_choice(self, rng, ctx) -> Spec:
        """ch_scope: exactly one scope of the deepest agent's grant is usable; the planned option set (k, gold position
        and gold length rank, all drawn from the row key) can be filled from the error models."""
        T = ctx["T"]
        incl = ctx["end_rule"] == "incl"
        pack_id, pack = self.pack_for(ctx["sampler"], "agent", ctx["card"])
        for _ in range(MAX_TRIES):
            depth = self._depth(rng, ctx, minimum=2)
            universe, items = pack["scopes"], pack["tasks"]
            pool = list(universe)
            rng.shuffle(pool)
            gold, pool = pool[0], pool[1:]
            na, nb, nx = rng.choice((1, 1, 2)), rng.choice((0, 1, 1)), rng.choice((1, 1, 2))
            a, b, x = pool[:na], pool[na:na + nb], pool[na + nb:na + nb + nx]
            child, parent = [gold] + a + b, [gold] + b + x
            lists = [parent, child]
            if depth == 3:
                rest = pool[na + nb + nx:]
                lists.insert(0, parent + rest[:rng.choice((0, 1))])
            for li in lists:
                rng.shuffle(li)
            live = tuple(k for k in END_LIVE if k[0] in ("after_far", "after_1") or (incl and k[0] == "at"))
            windows = []
            for _ in range(depth):
                start = T - MINUTE * rng.randint(95, 20 * 1440)
                windows.append((start, _kind_time(rng, T, _wchoice(rng, live))))
            revs = []
            for sc in b:
                j = depth - 1 if rng.random() < 0.6 else depth - 2
                kind = rng.choices(("before_1", "before_far", "at"), weights=(60, 30, 10))[0]
                t = _kind_time(rng, T, kind)
                if t > windows[j][0]:             # G0 M10 (else the scope stays usable and the case is redrawn)
                    revs.append((("scope", j, sc), t, "parent" if j > 0 else "principal"))
            if len(revs) < 2 and rng.random() < 0.35:
                revs.append((("scope", depth - 1, gold), T + MINUTE, "parent"))
            spec = self._build_agent(rng, ctx, (pack_id, pack), items, lists, windows, revs, None, depth)
            usable = [s for s in self._own_scopes(spec) if _usable(self._agent_status(spec, s))]
            if usable != [gold]:
                continue
            spec = self.derive(spec)
            if self.solve_a(spec) != gold:
                raise ContractError(f"T31 seed {ctx['seed']}: construction table and solver A disagree")
            if not self._options_ok(spec, strict=True):
                continue                  # fewer distinct error-model scopes than the planned k needs: redraw
            return spec
        raise ContractError(f"T31 {ctx['sampler']} seed {ctx['seed']}: no ch_scope spec")

    def _agent_tags(self, spec: Spec) -> tuple:
        v, st = spec.env(), spec.structure
        T = v["REQ_TIME"]
        tags = set()
        for r in st["revocations"]:
            t = v[r["time"]]
            tags |= {"rev_1min"} if t == T - MINUTE else ({"notice_after"} if t == T + MINUTE else
                                                         ({"notice_at"} if t == T else set()))
        lists = [[v[x] for x in g["scopes"]] for g in st["grants"]]
        if any(any(s not in lists[j - 1] for s in lists[j]) for j in range(1, len(lists))):
            tags.add("sub_broader")
        incl = st["end_rule"] == "incl"
        for g in st["grants"]:
            s, e = v[g["start"]], v[g["end"]]
            if s <= T and not (T <= e if incl else T < e):
                tags.add("lapsed")
            if s > T:
                tags.add("not_started")
        if len(lists) > 1 and ((v.get("REQ_SCOPE") in lists[-2] and v.get("REQ_SCOPE") not in lists[-1])
                               or ("REQ_SCOPE" not in v and any(x not in lists[-1] for x in lists[-2]))):
            tags.add("inherit_trap")
        if st.get("odd"):
            tags.add("conversion")
        if spec.deep:
            tags.add("deep_chain")
        return tuple(sorted(tags))

    # ============================================================================================ derive
    def derive(self, spec: Spec) -> Spec:
        derived, deps = {}, {}
        st = spec.structure
        odd = st.get("odd")
        if odd:
            derived[f"{odd}_SAME"] = S.datetime_slot(spec.slots[odd].value.astimezone(_tz(st["base_offset"])))
            deps[f"{odd}_SAME"] = (odd,)
        if st.get("candidate"):
            derived["CANDIDATE"] = spec.slots[st["candidate"]]
            deps["CANDIDATE"] = (st["candidate"],)
        if st["track"] == "agent":
            derived["REQ_AGENT"] = spec.slots[st["chain"][-1]]
            deps["REQ_AGENT"] = (st["chain"][-1],)
        return spec.replace(derived=derived, derived_deps=deps)

    # ============================================================================================ solver A
    def _env(self, spec: Spec, mods: frozenset) -> dict:
        env = spec.env()
        if "skip_offset_conversion" in mods:
            for name, s in spec.slots.items():
                if s.kind == "datetime":
                    env[name] = s.value.replace(tzinfo=UTC)          # the wall clock read as if it were UTC
        return env

    @staticmethod
    def _end_op(rule: str, mods: frozenset) -> str:
        if "add_exclusive_endpoint" in mods:
            rule = "incl"
        if "drop_inclusive_endpoint" in mods:
            rule = "excl"
        return "<=" if rule == "incl" else "<"

    def _appr_resolve(self, spec: Spec, mods: frozenset = frozenset()):
        """Solver A (mods empty) and the ch_approver error models (one rule swapped): a person's name or escalate."""
        env = self._env(spec, mods)
        st = spec.structure
        T = RL.Ref("REQ_TIME")
        end_op = self._end_op(st["end_rule"], mods)

        def band(rec):
            if not rec["band"] or "t31_ignore_band" in mods:
                return []
            sem = env[rec["band"]]
            if "add_exclusive_endpoint" in mods:
                sem = TO_INCLUSIVE.get(sem, sem)
            if "drop_inclusive_endpoint" in mods:
                sem = TO_EXCLUSIVE.get(sem, sem)
            return [RL.Cmp(CMP_OP[sem], RL.Ref("REQ_AMOUNT"), RL.Ref(rec["bound"]))]

        def issued(rec):
            return RL.Lit(True) if "t31_future_notice" in mods else RL.Cmp("<=", RL.Ref(rec["time"]), T)

        covering_d = []
        for i, d in enumerate(st["delegations"]):
            conds = [RL.Cmp("<=", RL.Ref(d["start"]), T)]
            if "t31_ignore_window_end" not in mods:
                conds.append(RL.Cmp(end_op, T, RL.Ref(d["end"])))
            conds += band(d)
            if "ignore_revocation" not in mods:
                conds += [RL.Not(issued(n)) for n in st["notices"] if n["kind"] == "revoke" and n["target"] == i]
            if RL.evaluate(RL.And(tuple(conds)), env):
                covering_d.append(d)
        covering_o = [n for n in st["notices"] if n["kind"] == "override"
                      and RL.evaluate(RL.And(tuple([issued(n)] + band(n))), env)]
        default = env[st["default"]]
        if "t31_default_holder" in mods:
            return default
        if "t31_responsible_role" in mods:
            return next(env[p] for _, p, letter in st["matrix"] if letter == "R")
        if "t31_issuer_as_holder" in mods:
            live = [n for n in st["notices"] if RL.evaluate(issued(n), env)]
            if not live:
                return None
            last = max(env[n["time"]] for n in live)
            by = {env[n["by"]] for n in live if env[n["time"]] == last}
            return next(iter(by)) if len(by) == 1 else None
        if "first_match" in mods or "last_match" in mods:
            listed = [env[d["to"]] for d in covering_d] + [env[n["person"]] for n in covering_o]
            if not listed:
                return default
            return listed[0] if "first_match" in mods else listed[-1]
        levels = [("o", covering_o), ("d", covering_d)]
        if "t31_delegation_beats_override" in mods:
            levels.reverse()
        for kind, recs in levels:
            if not recs:
                continue
            if kind == "o":
                pick = min if "t31_earliest_override" in mods else max
                t = pick(env[n["time"]] for n in recs)
                names = {env[n["person"]] for n in recs if env[n["time"]] == t}
            else:
                names = {env[d["to"]] for d in recs}
            return next(iter(names)) if len(names) == 1 else ESCALATE
        return default

    def _agent_usable(self, spec: Spec, scope: str, mods: frozenset = frozenset()) -> bool:
        """Solver A for one scope of the deepest agent (and the ch_scope error models)."""
        env = self._env(spec, mods)
        st = spec.structure
        T = RL.Ref("REQ_TIME")
        end_op = self._end_op(st["end_rule"], mods)
        levels = []
        for j, g in enumerate(st["grants"]):
            conds = [RL.Cmp("<=", RL.Ref(g["start"]), T)]
            if "t31_ignore_window_end" not in mods:
                conds.append(RL.Cmp(end_op, T, RL.Ref(g["end"])))
            conds.append(RL.In(RL.Lit(scope), tuple(RL.Ref(x) for x in g["scopes"])))
            if "ignore_revocation" not in mods:
                for r in st["revocations"]:
                    hit = RL.Lit(True) if "t31_future_notice" in mods else RL.Cmp("<=", RL.Ref(r["time"]), T)
                    if r["grant"] == j:
                        conds.append(RL.Not(hit))
                    elif r["grant"] is None and r["agent"] == g["to"]:
                        conds.append(RL.Not(RL.And((RL.Cmp("==", RL.Ref(r["scope"]), RL.Lit(scope)), hit))))
            levels.append(RL.And(tuple(conds)))
        if "t31_ignore_attenuation" in mods:
            node = levels[-1]
        else:
            node = RL.And(tuple(levels))
            if "t31_inherit_parent" in mods and len(levels) > 1:
                node = RL.Or((node, RL.And(tuple(levels[:-1]))))
        return RL.evaluate(node, env)

    def _own_scopes(self, spec: Spec) -> list:
        v = spec.env()
        return [v[x] for x in spec.structure["grants"][-1]["scopes"]]

    def _scope_err(self, spec: Spec, name: str):
        """ch_scope error model: the first scope (deepest grant first, then up the chain) the misreading adds."""
        v = spec.env()
        true = {s for s in self._own_scopes(spec) if self._agent_usable(spec, s)}
        seen = []
        for g in reversed(spec.structure["grants"]):
            for x in g["scopes"]:
                if v[x] not in seen:
                    seen.append(v[x])
        for s in seen:
            if s not in true and self._agent_usable(spec, s, frozenset({name})):
                return s
        return None

    def solve_a(self, spec: Spec):
        q = spec.qform
        if TRACK[q] == "appr":
            holder = self._appr_resolve(spec)
            if q == "ch_approver":
                return holder
            if holder == ESCALATE:
                raise ContractError("T31: a yes/no approver question on a case without a unique approver")
            same = holder == spec.env()["CANDIDATE"]
            return int(same if POLARITY[q] == 1 else not same)
        if q == "ch_scope":
            usable = [s for s in self._own_scopes(spec) if self._agent_usable(spec, s)]
            if len(usable) != 1:
                raise ContractError(f"T31 ch_scope: {len(usable)} usable scopes (exactly one by construction)")
            return usable[0]
        return _agent_answer(q, self._agent_usable(spec, spec.env()["REQ_SCOPE"]))

    # ============================================================================================ construction table
    def _appr_status(self, spec: Spec) -> dict:
        v, st = spec.env(), spec.structure
        T, amount = v["REQ_TIME"], v["REQ_AMOUNT"]
        incl = st["end_rule"] == "incl"
        dels = []
        for i, d in enumerate(st["delegations"]):
            s, e = v[d["start"]], v[d["end"]]
            revs = [v[n["time"]] for n in st["notices"] if n["kind"] == "revoke" and n["target"] == i]
            dels.append({"started": s <= T, "not_ended": (T <= e) if incl else (T < e),
                         "revoked": any(r <= T for r in revs), "band": _fits(v, d, amount), "to": v[d["to"]]})
        ovr = [{"issued": v[n["time"]] <= T, "band": _fits(v, n, amount), "t": v[n["time"]], "to": v[n["person"]]}
               for n in st["notices"] if n["kind"] == "override"]
        return {"del": dels, "ovr": ovr, "default": v[st["default"]]}

    def _agent_status(self, spec: Spec, scope: str) -> list:
        v, st = spec.env(), spec.structure
        T = v["REQ_TIME"]
        incl = st["end_rule"] == "incl"
        out = []
        for j, g in enumerate(st["grants"]):
            s, e = v[g["start"]], v[g["end"]]
            whole = [v[r["time"]] for r in st["revocations"] if r["grant"] == j]
            srev = [v[r["time"]] for r in st["revocations"]
                    if r["grant"] is None and r["agent"] == g["to"] and v[r["scope"]] == scope]
            out.append({"started": s <= T, "not_ended": (T <= e) if incl else (T < e),
                        "whole": any(t <= T for t in whole), "has": scope in [v[x] for x in g["scopes"]],
                        "srev": any(t <= T for t in srev)})
        return out

    # ============================================================================================ facts (G3)
    def canonical(self, spec: Spec) -> dict:
        a = spec.all_slots()

        def c(name):
            return S.canonical(a[name]) if name else None

        st = spec.structure
        out = {"track": st["track"], "qform": spec.qform, "style": st["style"], "end_rule": st["end_rule"],
               "requester": c("REQUESTER"), "item": c("ITEM")}
        if st["track"] == "appr":
            dels = st["delegations"]
            out.update(
                process=c("PROCESS"),
                matrix=[[c(r), c(p), letter] for r, p, letter in st["matrix"]],
                delegations=[{"id": c(d["id"]), "from": c(d["from"]), "to": c(d["to"]), "start": c(d["start"]),
                              "end": c(d["end"]), "band": [c(d["band"]), c(d["bound"])] if d["band"] else None}
                             for d in dels],
                notices=[{"id": c(n["id"]), "kind": n["kind"], "time": c(n["time"]), "by": c(n["by"]),
                          "target": c(dels[n["target"]]["id"]) if n["kind"] == "revoke" else None,
                          "person": c(n["person"]), "band": [c(n["band"]), c(n["bound"])] if n["band"] else None}
                         for n in st["notices"]],
                request={"id": c("REQ_ID"), "amount": c("REQ_AMOUNT"), "time": c("REQ_TIME")},
                question={"candidate": c("CANDIDATE")} if spec.qform != "ch_approver" else {})
            return out
        grants = st["grants"]
        out.update(
            principal=c("PRINCIPAL"),
            grants=[{"id": c(g["id"]), "by": c(g["by"]), "to": c(g["to"]), "scopes": [c(x) for x in g["scopes"]],
                     "start": c(g["start"]), "end": c(g["end"])} for g in grants],
            revocations=[{"id": c(r["id"]), "time": c(r["time"]), "by": c(r["by"]),
                          "agent": c(r["agent"]), "scope": c(r["scope"]),
                          "grant": c(grants[r["grant"]]["id"]) if r["grant"] is not None else None}
                         for r in st["revocations"]],
            request={"id": c("REQ_ID"), "agent": c(st["chain"][-1]),
                     "scope": c("REQ_SCOPE") if "REQ_SCOPE" in a else None, "time": c("REQ_TIME")},
            question=({"agent": c("REQ_AGENT")} if spec.qform == "ch_scope"
                      else {"agent": c("REQ_AGENT"), "scope": c("REQ_SCOPE")}))
        return out

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("requester", "item")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"requester": c["requester"], "item": c["item"], "req_id": c["request"]["id"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("requester", "name", "the person who raised the request, as written"),
                Field("item", "str", "what the request is about: the noun phrase only, without a leading article "
                                     "(the, a, an), exactly as written"),
                Field("req_id", "id", "the request or task reference, as written")]

    # ============================================================================================ render
    def _row_key(self, spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    def card_style(self, spec: Spec) -> str:
        """The card style of a row (full / compact / short), a label-blind draw from (seed, sampler, track) only: a
        twin, a complement and an equiv / inv partner of one base share it (G-TW compares the card)."""
        return CD.draw_style(f"{FAMILY}|{spec.seed}|{spec.sampler}|{spec.structure['track']}", CARD_STYLES)

    def _rules(self, spec: Spec, style: str = "full") -> str:
        st = spec.structure
        end = (END_PHRASE if style == "full" else END_PHRASE_SHORT)[st["end_rule"]]
        return CARD_TEXT[st["track"]][style].replace("{END}", end).replace("{TIMES}", TIME_RULE[bool(st.get("odd"))])

    def block_template(self, spec: Spec) -> str:
        """The program-written record block as a slot template (G0 1.2)."""
        st = spec.structure
        log = st["style"] == "log"
        odd = st.get("odd")

        def _tm(slot):
            return f"{{{slot}}} [same instant: {{{slot}_SAME}}]" if slot == odd else f"{{{slot}}}"

        lines = ["Records:"]
        if st["track"] == "appr":
            dels = st["delegations"]
            if log:
                lines.append("process | {PROCESS}")
                lines += [f"matrix | {{{r}}} | {{{p}}} | {letter}" for r, p, letter in st["matrix"]]
                for d in dels:
                    lines.append(f"{_tm(d['start'])} | delegation {{{d['id']}}} starts | {{{d['from']}}} -> "
                                 f"{{{d['to']}}} | ends {_tm(d['end'])} | amounts {_band_text(d)}")
                for n in st["notices"]:
                    if n["kind"] == "revoke":
                        lines.append(f"{_tm(n['time'])} | revocation {{{n['id']}}} issued | by {{{n['by']}}} | revokes "
                                     f"{{{dels[n['target']]['id']}}}")
                    else:
                        lines.append(f"{_tm(n['time'])} | override {{{n['id']}}} issued | by {{{n['by']}}} | A role to "
                                     f"{{{n['person']}}} | amounts {_band_text(n)}")
                lines.append(f"{_tm('REQ_TIME')} | request {{REQ_ID}} made | amount {{REQ_AMOUNT}}")
            else:
                lines += ["Process: {PROCESS}", "Standing RACI matrix:"]
                lines += [f"- {{{r}}}: {{{p}}} [{letter}]" for r, p, letter in st["matrix"]]
                lines.append("Delegations:")
                for d in dels:
                    lines.append(f"- {{{d['id']}}}: {{{d['from']}}} delegates the A role to {{{d['to']}}}, from "
                                 f"{_tm(d['start'])} to {_tm(d['end'])}; amounts {_band_text(d)}.")
                lines.append("Notices:" if st["notices"] else "Notices: none.")
                for n in st["notices"]:
                    if n["kind"] == "revoke":
                        lines.append(f"- {{{n['id']}}}, issued {_tm(n['time'])} by {{{n['by']}}}: delegation "
                                     f"{{{dels[n['target']]['id']}}} is revoked.")
                    else:
                        lines.append(f"- {{{n['id']}}}, issued {_tm(n['time'])} by {{{n['by']}}}: override, the A "
                                     f"role goes to {{{n['person']}}}; amounts {_band_text(n)}.")
                lines.append(f"Request {{REQ_ID}}: amount {{REQ_AMOUNT}}, made at {_tm('REQ_TIME')}.")
        else:
            grants, ask = st["grants"], "REQ_SCOPE" in spec.slots
            agent = st["chain"][-1]
            if log:
                lines.append("principal | {PRINCIPAL}")
                for g in grants:
                    sc = ", ".join(f"{{{x}}}" for x in g["scopes"])
                    lines.append(f"{_tm(g['start'])} | grant {{{g['id']}}} starts | {{{g['by']}}} -> {{{g['to']}}} | "
                                 f"scopes {sc} | ends {_tm(g['end'])}")
                for r in st["revocations"]:
                    what = (f"grant {{{grants[r['grant']]['id']}}} in full" if r["grant"] is not None
                            else f"scope {{{r['scope']}}} from {{{r['agent']}}}")
                    lines.append(f"{_tm(r['time'])} | revocation {{{r['id']}}} issued | by {{{r['by']}}} | {what}")
                act = "scope {REQ_SCOPE}" if ask else "about to act"
                lines.append(f"{_tm('REQ_TIME')} | request {{REQ_ID}} made | {{{agent}}} | {act}")
            else:
                lines += ["Principal: {PRINCIPAL}", "Grants:"]
                for j, g in enumerate(grants):
                    sc = ", ".join(f"{{{x}}}" for x in g["scopes"])
                    sub = "sub-agent " if j else ""
                    lines.append(f"- {{{g['id']}}}: {{{g['by']}}} grants {sub}{{{g['to']}}} the scopes {sc}; in "
                                 f"effect from {_tm(g['start'])} to {_tm(g['end'])}.")
                lines.append("Revocations:" if st["revocations"] else "Revocations: none.")
                for r in st["revocations"]:
                    what = (f"grant {{{grants[r['grant']]['id']}}} is withdrawn in full" if r["grant"] is not None
                            else f"scope {{{r['scope']}}} is removed from {{{r['agent']}}}")
                    lines.append(f"- {{{r['id']}}}, issued {_tm(r['time'])} by {{{r['by']}}}: {what}.")
                act = "asks to use scope {REQ_SCOPE}" if ask else "is about to act"
                lines.append(f"Request {{REQ_ID}}: at {_tm('REQ_TIME')}, {{{agent}}} {act}.")
        lines.append("End of records.")
        return "\n".join(lines)

    def unit_rows_bound(self, spec: Spec) -> int:
        """The rows one relation unit of this spec feeds to ONE skin: the base row and its complement, twin and attack
        partners (an equiv partner uses another skin). Upper bound: a proposal may still fail a gate."""
        return 1 + sum(1 for p in self._relations_cached(spec) if p.kind in ("complement", "twin", "inv"))

    def _pick_skin(self, ctx, spec: Spec, key: str, held: bool):
        track = spec.structure["track"]
        other = tuple(sid for sid, s in ctx.skins.items() if not _fits_track(s, track))
        kw = {"need": self.unit_rows_bound(spec)} if isinstance(ctx, T31Ctx) and self.skin_row_cap else {}
        if spec.sampler == "S4":
            reg = S4_REGISTERS[int(uhash(key, "register") * len(S4_REGISTERS))]
            try:
                return ctx.pick(FAMILY, "skin", key, register=reg, held_out=held, exclude=other, **kw)
            except LookupError:
                pass
        return ctx.pick(FAMILY, "skin", key, held_out=held, exclude=other, **kw)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self._row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or self._pick_skin(ctx, spec, key, held)
        for piece in (skin, attack):
            if piece is not None and not _fits_track(piece, spec.structure["track"]):
                raise K.RenderError(f"{piece.skin_id} is written for the other track")
        if skin.family == FAMILY and skin.kind == "skin" and skin.author_mode == "F":
            leaks = freeform_leaks(skin.text, skin.brief)
            if leaks:
                raise K.RenderError(f"{skin.skin_id}: Mode F text keeps {leaks[0]} (F03)")
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=held)   # A54 (2): S5 uses held-out wordings
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        qtype = self.QFORMS[spec.qform].qtype
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n").add("state", K.fill(self.block_template(spec), slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        style = self.card_style(spec)
        field = CD.place_rules(tb, self._rules(spec, style), qtype)    # yes/no: row.card (once); choice: instructions
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if qtype == "choice":
            os_ = self._options(spec, ans)
            if os_ is None:
                raise K.RenderError(f"{spec.qform}: the planned options cannot be filled by the error models")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CD.defs_style(field, style))

    # ============================================================================================ relations
    def _plan(self, spec: Spec):
        """The display plan of a choice row (c2_kit.choiceplan): None for yes/no forms. See _plan_by."""
        if spec.qform not in ("ch_approver", "ch_scope"):
            return None
        return self._plan_by(spec.sampler, spec.seed, spec.qform)

    def _plan_by(self, sampler: str, seed: int, qform: str):
        """The display plan of one choice row: ch_approver shows the escalate option on 40% of the rows (k 3 or 4 counts
        it) and escalate is gold on 1/k of the rows that show it; ch_scope has no abstain option. k and the display are
        the kit's hash draws from the row key. Whether the gold is escalate, the gold position and the gold length rank
        are STRATIFIED: over the seeds of one block of PLAN_BLOCK seeds of one sampler, the m-th seed of a cell takes the
        m-th entry of a seeded cycle of permutations (escalate gold: exactly one row in k of the cell (form, k, shown);
        position: uniform over the k of the cell (form, k); rank: uniform over the n ordered options of the cell (form,
        n, gold not escalate)). So every sampler, form and option count carries the gold's position, length rank and
        escalate rate it is supposed to have, instead of the +- 2-3 pp a 100-row cell gets from independent draws; a
        feature that tells the samplers apart can then not predict the gold (G6 d_meta). Label-blind: nothing here
        reads a solved gold, and a base row whose structure disagrees with the plan is redrawn, never relabelled."""
        key = (sampler, seed, qform)
        hit = self._plan_cache.get(key)
        if hit is None:
            plan = self._plan_raw(sampler, seed, qform)
            ga, pos, rank = self._block_table(sampler, seed // PLAN_BLOCK, qform)[seed]
            hit = dataclasses.replace(plan, gold_abstain=ga, pos=pos, rank=rank)
            if len(self._plan_cache) >= 8192:
                self._plan_cache.clear()
            self._plan_cache[key] = hit
        return hit

    def _plan_raw(self, sampler: str, seed: int, qform: str):
        key = f"{FAMILY}|{seed}|{sampler}|{qform}"
        if qform == "ch_approver":
            return CP.plan_choice(key, ks=CHOICE_KS, abstain=True, show_rate=APPR_ABSTAIN_SHOW)
        return CP.plan_choice(key, ks=CHOICE_KS, abstain=False)

    def _block_table(self, sampler: str, block: int, qform: str) -> dict:
        """{seed: (gold is escalate, gold position, gold length rank or None)} for the seeds of one block that ask `qform`
        (the question form is drawn per seed pair, so it is known without building anything)."""
        ck = (sampler, block, qform)
        hit = self._block_cache.get(ck)
        if hit is not None:
            return hit
        seeds = [s for s in range(block * PLAN_BLOCK, (block + 1) * PLAN_BLOCK)
                 if self.available(_draw(uhash(FAMILY, "qform", sampler, s // 2), BASE_SHARES)) == qform]
        raw = {s: self._plan_raw(sampler, s, qform) for s in seeds}

        def cycle(members: list, n: int, tag: str) -> dict:
            out, order = {}, None
            for m, s in enumerate(members):
                if m % n == 0:
                    order = sorted(range(n), key=lambda i: uhash(FAMILY, tag, sampler, block, qform, n, m // n, i))
                out[s] = order[m % n]
            return out
        ga: dict = {}
        for k in sorted({r.k for r in raw.values()}):
            shown = [s for s in seeds if raw[s].k == k and raw[s].show_abstain]
            ga.update({s: slot == 0 for s, slot in cycle(shown, k, "gaperm").items()})
        pos: dict = {}
        for k in sorted({r.k for r in raw.values()}):
            pos.update(cycle([s for s in seeds if raw[s].k == k], k, "posperm"))
        rank: dict = {}
        for n in sorted({r.n_ordered for r in raw.values()}):
            rank.update(cycle([s for s in seeds if raw[s].n_ordered == n and not ga.get(s, False)], n, "rankperm"))
        table = {s: (ga.get(s, False), pos[s], rank.get(s)) for s in seeds}
        self._block_cache[ck] = table
        return table

    def _options(self, spec: Spec, ans, strict: bool = False):
        """The planned option set (k, escalate display, gold position and gold length rank from the plan). strict:
        a base row, whose gold must agree with the plan; partner rows (twins, G4 variants) adapt the plan to their
        own gold. None when the error models give too few distinct wrong answers: the spec is resampled (sample) or
        the partner is not proposed (relations), never re-tried with a smaller k."""
        key, plan = self._row_key(spec), self._plan(spec)
        abstain = (ESCALATE, ESCALATE_TEXT) if spec.qform == "ch_approver" else None

        def build(pl, strict_plan):
            return build_options(spec, ans, self.error_models(), row_key=key, render_key=_ident, abstain=abstain,
                                 plan=pl, length_balance=self.LENGTH_BALANCE, strict_plan=strict_plan)
        os_ = build(plan, strict)
        if os_ is not None or strict:
            return os_
        # a partner row cannot be redrawn: its new gold decides which length ranks the error models can fill, so the
        # planned rank is tried first, then the other ranks in a seeded order (never a different k or display)
        p2 = plan.for_gold(abstain is not None and ans == ESCALATE)
        if p2.rank is None:
            return None
        for r in sorted((r for r in range(p2.n_ordered) if r != p2.rank), key=lambda r: uhash(key, "partner_rank", r)):
            os_ = build(dataclasses.replace(p2, rank=r), False)
            if os_ is not None:
                return os_
        return None

    def _options_ok(self, spec: Spec, strict: bool = False) -> bool:
        return spec.qform not in ("ch_approver", "ch_scope") or self._options(spec, self.solve_a(spec), strict) is not None

    def relations(self, spec: Spec) -> list:
        return list(self._relations_cached(spec))

    def _relations_cached(self, spec: Spec) -> list:
        """relations() is a pure function of the spec; the pipeline, the skin pick (unit_rows_bound) and the tests ask
        for it more than once per unit, so the last few answers are kept."""
        ck = (spec.seed, spec.sampler, spec.qform, spec.structure_hash())
        hit = self._rel_cache.get(ck)
        if hit is None:
            hit = self._relations(spec)
            if len(self._rel_cache) >= 16:
                self._rel_cache.pop(next(iter(self._rel_cache)))
            self._rel_cache[ck] = hit
        return hit

    def _relations(self, spec: Spec) -> list:
        out = []
        key = self._row_key(spec)
        comp = COMPLEMENTS.get(spec.qform)
        if comp and uhash(FAMILY, "comp", key) < P_COMPLEMENT:
            out.append(RelationProposal("complement", qform=_draw(uhash(FAMILY, "ckind", key), comp)))
        u = uhash(FAMILY, "extra", key)
        if u < P_EQUIV:
            out.append(RelationProposal("equiv"))
        elif u < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        # a ch_approver row that shows the escalate option has no twin: its twin would be a non-escalate row in a cell
        # whose escalate share must stay 1/k, so the rows that show escalate are the base and its copies (equiv, attack)
        shows = spec.qform == "ch_approver" and self._plan(spec).show_abstain
        if (spec.qform != "ch_scope" and not shows
                and uhash(FAMILY, "twin", key) < P_TWIN["ch" if spec.qform == "ch_approver" else "yn"]):
            t = self._twin(spec)
            if t is not None and self._options_ok(self.derive(t.spec)):
                out.append(t)
        return out + [m for m in self._metamorphic(spec) if self._options_ok(self.derive(m.spec))]

    def _twin(self, spec: Spec):
        return self._twin_appr(spec) if spec.structure["track"] == "appr" else self._twin_agent(spec)

    def _appr_answer(self, spec: Spec, holder):
        if spec.qform == "ch_approver":
            return holder
        same = holder == spec.env()["CANDIDATE"]
        return int(same if POLARITY[spec.qform] == 1 else not same)

    def _twin_appr(self, spec: Spec):
        """Move one slot so exactly one condition of one record flips; predict from the construction table."""
        v, st = spec.env(), spec.structure
        T, amount = v["REQ_TIME"], v["REQ_AMOUNT"]
        base = self._appr_status(spec)
        base_ans = self._appr_answer(spec, _decide(base)[1])
        ops = []
        o_index = {id(n): k for k, n in enumerate([n for n in st["notices"] if n["kind"] == "override"])}
        for n in st["notices"]:
            t = v[n["time"]]
            new_t = (T + MINUTE if t <= T else T - MINUTE).astimezone(t.tzinfo)
            if n["kind"] == "revoke" and new_t <= v[st["delegations"][n["target"]]["start"]]:
                pass                              # G0 M6: never move a revocation to or before its target's start
            elif n["kind"] == "revoke":
                ops.append((n["time"], S.datetime_slot(new_t), ("del", n["target"], "revoked", t > T, None)))
            else:
                ops.append((n["time"], S.datetime_slot(new_t), ("ovr", o_index[id(n)], "issued", t > T, new_t)))
            if n["kind"] == "override" and n["band"]:
                ok = base["ovr"][o_index[id(n)]]["band"]
                nb = _edge_bound(v[n["band"]], amount, ok)
                if nb >= 1:
                    ops.append((n["bound"], S.cents_slot(nb), ("ovr", o_index[id(n)], "band", not ok, None)))
        for i, d in enumerate(st["delegations"]):
            s, e = v[d["start"]], v[d["end"]]
            if s <= T - MINUTE:
                ended = not base["del"][i]["not_ended"]
                new_e = (T + MINUTE if ended else T - MINUTE)
                if new_e > s:
                    ops.append((d["end"], S.datetime_slot(new_e.astimezone(e.tzinfo)),
                                ("del", i, "not_ended", ended, None)))
            if d["band"]:
                ok = base["del"][i]["band"]
                nb = _edge_bound(v[d["band"]], amount, ok)
                if nb >= 1:
                    ops.append((d["bound"], S.cents_slot(nb), ("del", i, "band", not ok, None)))
        ops.sort(key=lambda op: uhash(FAMILY, "twinop", spec.seed, op[0]))
        for slot, new, (part, idx, field, value, new_t) in ops:
            st2 = copy.deepcopy(base)
            st2[part][idx][field] = value
            if new_t is not None:
                st2[part][idx]["t"] = new_t
            holder2 = _decide(st2)[1]
            if holder2 == ESCALATE:                   # G0 6: a twin never turns into escalate
                continue
            ans2 = self._appr_answer(spec, holder2)
            if ans2 == base_ans:
                continue
            twin = spec.with_slot(slot, new)
            if self._appr_status(twin) != st2:
                continue
            return RelationProposal("twin", spec=twin, changed_slot=slot, expect=ans2, note=f"{part}{idx}.{field}")
        return None

    def _fresh_scope(self, spec: Spec):
        """A scope id the row does not use: from the row's own pack first, else the in-code reserve."""
        taken = {s.value for s in spec.slots.values() if s.kind == "id"}
        pool = list(self.pack_by_id[spec.pack]["scopes"]) + list(RESERVE_SCOPES)
        return next((x for x in pool if x not in taken), None)

    def _twin_agent(self, spec: Spec):
        v, st = spec.env(), spec.structure
        T, scope = v["REQ_TIME"], v["REQ_SCOPE"]
        base = self._agent_status(spec, scope)
        ok = _usable(base)
        fresh = self._fresh_scope(spec)
        ops = []
        for j, g in enumerate(st["grants"]):
            s, e = v[g["start"]], v[g["end"]]
            if s <= T - MINUTE:
                ended = not base[j]["not_ended"]
                new_e = T + MINUTE if ended else T - MINUTE
                if new_e > s:
                    ops.append((g["end"], S.datetime_slot(new_e.astimezone(e.tzinfo)), j, "not_ended", ended))
            names = [v[x] for x in g["scopes"]]
            if scope in names and fresh:
                ops.append((g["scopes"][names.index(scope)], S.id_slot(fresh), j, "has", False))
            elif scope not in names:
                slot = g["scopes"][int(uhash(FAMILY, "hslot", spec.seed, j) * len(names))]
                ops.append((slot, S.id_slot(scope), j, "has", True))
        chain = st["chain"]
        for r in st["revocations"]:
            if r["grant"] is None and (r["agent"] not in chain or v[r["scope"]] != scope):
                continue
            t = v[r["time"]]
            new_t = (T + MINUTE if t <= T else T - MINUTE).astimezone(t.tzinfo)
            j, field = (r["grant"], "whole") if r["grant"] is not None else (chain.index(r["agent"]), "srev")
            if new_t <= v[st["grants"][j]["start"]]:
                continue                          # G0 M10
            ops.append((r["time"], S.datetime_slot(new_t), j, field, t > T))
        ops.sort(key=lambda op: uhash(FAMILY, "twinop", spec.seed, op[0]))
        for slot, new, j, field, value in ops:
            st2 = copy.deepcopy(base)
            st2[j][field] = value
            ok2 = _usable(st2)
            if ok2 == ok:
                continue
            twin = spec.with_slot(slot, new)
            if self._agent_status(twin, scope) != st2:
                continue
            return RelationProposal("twin", spec=twin, changed_slot=slot, expect=_agent_answer(spec.qform, ok2),
                                    note=f"level{j}.{field}")
        return None

    def _metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): renames, a common time shift and an offset rewrite leave the answer as
        predicted."""
        v, st = spec.env(), spec.structure
        out = []
        names = {s.value for s in spec.slots.values() if s.kind == "name"}
        used_toks = set().union(*(_name_tokens(n) for n in names))
        fresh_names = [n for n in sorted(self.names, key=lambda n: uhash(FAMILY, "reserve", spec.seed, n))
                       if not _name_tokens(n) & used_toks][:2]
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("REQUESTER", S.name_slot(fresh_names[0])),
                                    expect="same", note="rename the requester"))
        shift = dt.timedelta(minutes=97)
        moved = {k: S.datetime_slot(s.value + shift) for k, s in spec.slots.items() if s.kind == "datetime"}
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **moved}), expect="same",
                                    note="shift every time by 97 minutes"))
        t = v["REQ_TIME"]
        other = next(_tz(o) for o in OFFSETS if _tz(o).utcoffset(None) != t.utcoffset())
        rewritten = spec.with_slot("REQ_TIME", S.datetime_slot(t.astimezone(other)))
        out.append(RelationProposal("metamorphic", spec=rewritten, expect="same",
                                    note="rewrite the request time in another offset"))
        if st["track"] == "appr":
            if spec.qform == "ch_approver":
                gold = self.solve_a(spec)
                if gold != ESCALATE:
                    slot = next(p for _, p, _ in st["matrix"] if v[p] == gold)
                    out.append(RelationProposal("metamorphic", spec=spec.with_slot(slot, S.name_slot(fresh_names[1])),
                                                expect=fresh_names[1], note="rename the gold person"))
            elif st.get("candidate"):
                out.append(RelationProposal("metamorphic",
                                            spec=spec.with_slot(st["candidate"], S.name_slot(fresh_names[1])),
                                            expect="same", note="rename the candidate"))
            return out
        taken = {s.value for s in spec.slots.values() if s.kind == "id"}
        new_agent = next(a for a in list(self.pack_by_id[spec.pack]["agents"]) + list(RESERVE_AGENTS)
                         if a not in taken)
        out.append(RelationProposal("metamorphic", spec=spec.with_slot(st["chain"][-1], S.id_slot(new_agent)),
                                    expect="same", note="rename the requesting agent"))
        if spec.qform == "ch_scope":
            gold = self.solve_a(spec)
            new_scope = self._fresh_scope(spec)
            renamed = {k: S.id_slot(new_scope) for k, s in spec.slots.items() if s.kind == "id" and s.value == gold}
            out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **renamed}),
                                        expect=new_scope, note="rename the gold scope everywhere"))
        return out

    # ============================================================================================ error models
    def error_models(self) -> dict:
        if self._ems is None:
            ems = {}
            for name in dict.fromkeys(APPR_EM + SCOPE_EM):
                def fn(spec, name=name):
                    if spec.qform == "ch_approver" and name in APPR_EM:
                        return self._appr_resolve(spec, frozenset({name}))
                    if spec.qform == "ch_scope" and name in SCOPE_EM:
                        return self._scope_err(spec, name)
                    return None
                ems[name] = error_model(name, fn)
            self._ems = ems
        return self._ems
