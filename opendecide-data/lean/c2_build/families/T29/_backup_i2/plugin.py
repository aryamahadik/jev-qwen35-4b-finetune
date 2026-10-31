"""c2_build/families/T29/plugin.py: T29, confirmation gates before acting (C2_DATA_SPEC 3.4; frozen G0_SPEC.md).

An agent proposes one call. A confirmation policy of 3-6 rules (tier forbidden or needs confirmation; 12 atom types over
a state snapshot and the action catalog) gives GO AHEAD, ASK FIRST or REFUSE, and CANNOT DECIDE when a missing
snapshot field could change the verdict. The user's explicit earlier confirmation of this same call (action and
target) satisfies needs-confirmation rules, never a forbidden one. Semantics: G0_SPEC.md S1-S28 (frozen sha below).
G0 v1.2 (pilot fix iteration 1, 14 Oct 2026; section 6 of G0_SPEC.md) changed: the confirmation sentence on the card, the
placement of the card (row.card on yes/no rows), equal-length verdict labels, the yes/no and complement shares, one
twin-or-complement partner per yes/no unit, low-discrepancy label-blind draws, a CANNOT DECIDE share of 1 / 4 where it is
shown, card-level depth, register weights, the Haiku pack pool, and the double-negation form yn_go_dneg (no wording
admitted yet: it falls back to yn_go).

  solver A   rules.RuleSet (effect_order refuse > ask, default go) over a rule AST: rules.resolve on complete rows,
             rules.evaluate3 (Kleene) when a field is missing                                 paradigm rule_engine
  solver B   solver_b.py: its own parser of the rendered row, sqlite tables + SQL rule evaluation, enumeration of the
             missing-field completions over boundary witnesses (written from G0_SPEC.md)      paradigm sql_sqlite
  samplers   S1 forward; S2 label-first near-miss; S3 snapshot-table-first; S4 chat-session-first; S5 held out
             (runbook / agent-plan registers, held-out thresholds and windows; mixdev only)
  questions  ch_verdict (closed set, cannot decide shown on ~60%); yn_go / yn_ask / yn_refuse and their complements
             yn_not_go (syntactic), yn_go_framed (option framing), yn_ask_framed (option framing), yn_permitted
             (antonym), yn_not_forbidden (syntactic); ch_rule (which rule decides)
  relations  complement; minimal-edit twin (one slot across one atom's boundary, prediction from the base atom
             truths); premise removal (gold cannot decide); equiv (another register); inv (one pressure line);
             G4 metamorphic (rename the target, rename the organisation domain, shift times by a day, reverse rules)
Construction is label-first but balanced inside every visible partition. The display facts a reader can see without
the rules are seeded draws made before the gold: CANNOT DECIDE shown (60% of ch_verdict), a (missing) field (every
shown row, else 12%), the conversation kind, the featured atom and its tier, answer codes, skin, wording, slot forms,
option order, and the action tone (which reads only the card). The target is then drawn uniformly over the verdicts
those facts allow, and the card is kept fixed while truths and values are retried, so rejection never shapes the
card. Most CANNOT DECIDE golds come from premise-removal twins (G0 S20). The action catalog is a Claude-written
placeholder (code, not data); the packs are the frozen Haiku pool (pools/packs.jsonl, load_pool_packs), the six in-code
PACKS below are the unit tests' stand-ins. Nothing here writes a file.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import random
import re
from pathlib import Path

from c2_kit import cards as CARDS
from c2_kit import paths as KPATHS
from c2_kit import polarity as POL
from c2_kit import rules as RL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.lexicon import question_sem
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.relations import abstain_twin_kept
from c2_kit.rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "T29"

# ---------------------------------------------------------------------------------------- closed sets (G0 S1-S3)
U_RECORD = ("record", "records")
U_HOUR = ("hour", "hours")
U_MIN = ("minute", "minutes")
TEAMS = {"finance": ["Finance"], "legal": ["Legal"], "platform": ["Platform"], "research": ["Research"],
         "sales": ["Sales"], "support": ["Support"]}
ENVS = {"development": ["development"], "production": ["production"], "sandbox": ["sandbox"], "staging": ["staging"]}
CLASSES = {"internal": ["internal"], "personal": ["personal"], "public": ["public"]}
EFFECTS = {"change": ["changes data"], "create": ["creates data"], "delete": ["deletes data"],
           "export": ["exports data"], "grant": ["changes access rights"], "pay": ["pays money out"],
           "send": ["sends messages"]}
OUTBOUND = ("export", "grant", "pay", "send")
REASONS = {"audit": ["audit preparation"], "cleanup": ["quarterly cleanup"], "close": ["month-end close"],
           "incident": ["incident follow-up"], "migration": ["customer migration"],
           "onboarding": ["vendor onboarding"]}

# action catalog (placeholder): name, effect, tone. Tone is drawn independently of the verdict (G0 S24).
ACTIONS = (
    ("clear_old_notifications", "delete", "benign"), ("remove_draft_invoices", "delete", "benign"),
    ("tidy_archived_threads", "delete", "benign"), ("purge_customer_records", "delete", "alarming"),
    ("wipe_device_profiles", "delete", "alarming"), ("drop_report_tables", "delete", "alarming"),
    ("update_shipping_addresses", "change", "benign"), ("rename_project_folders", "change", "benign"),
    ("set_ticket_priority", "change", "benign"), ("override_credit_limits", "change", "alarming"),
    ("force_reset_passwords", "change", "alarming"), ("rewrite_price_list", "change", "alarming"),
    ("create_calendar_invites", "create", "benign"), ("open_followup_tickets", "create", "benign"),
    ("add_onboarding_tasks", "create", "benign"), ("spawn_load_test_cluster", "create", "alarming"),
    ("mass_create_accounts", "create", "alarming"), ("generate_bulk_api_keys", "create", "alarming"),
    ("send_status_digest", "send", "benign"), ("post_team_announcement", "send", "benign"),
    ("send_meeting_recap", "send", "benign"), ("blast_marketing_email", "send", "alarming"),
    ("send_final_dunning_notice", "send", "alarming"), ("broadcast_outage_alert", "send", "alarming"),
    ("top_up_prepaid_cards", "pay", "benign"), ("pay_vendor_invoice", "pay", "benign"),
    ("reimburse_travel_claims", "pay", "benign"), ("wire_settlement_funds", "pay", "alarming"),
    ("release_payroll_batch", "pay", "alarming"), ("force_refund_disputes", "pay", "alarming"),
    ("share_weekly_report", "export", "benign"), ("sync_contacts_to_partner", "export", "benign"),
    ("copy_survey_results", "export", "benign"), ("dump_customer_table", "export", "alarming"),
    ("export_full_user_list", "export", "alarming"), ("extract_payment_history", "export", "alarming"),
    ("add_member_to_channel", "grant", "benign"), ("share_folder_access", "grant", "benign"),
    ("invite_guest_reviewer", "grant", "benign"), ("grant_admin_role", "grant", "alarming"),
    ("elevate_service_permissions", "grant", "alarming"), ("unlock_root_console", "grant", "alarming"),
)
ACTION_TONE = {a: t for a, _, t in ACTIONS}

# packs (the unit tests' stand-ins; T29Plugin(packs=None) loads the frozen Haiku pool): organisation domain, look-alike
# and partner domains, target id prefix, people
PACKS = (
    {"id": "t29-pk-ledger", "org": "ledgerline.example", "lookalike": ("ledger-line.example", "ledgerline.test"),
     "partners": ("paycourier.example", "auditworks.example"), "prefix": "INV",
     "people": ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell")},
    {"id": "t29-pk-crm", "org": "brightdesk.example", "lookalike": ("bright-desk.example", "brightdesks.example"),
     "partners": ("mailorbit.example", "leadharbor.example"), "prefix": "CUS",
     "people": ("Tomas Ferreira", "Aiko Brandt", "Priya Velasco", "Jonah Pike")},
    {"id": "t29-pk-data", "org": "datafjord.example", "lookalike": ("data-fjord.example", "datafjord.test"),
     "partners": ("cloudvault.example", "metricsbay.example"), "prefix": "TBL",
     "people": ("Ines Moreau", "Kofi Mensah", "Hana Sato", "Elias Strand")},
    {"id": "t29-pk-comms", "org": "harborpost.example", "lookalike": ("harbor-post.example", "harborpost.test"),
     "partners": ("sendgate.example", "presswire.example"), "prefix": "MSG",
     "people": ("Maya Lindqvist", "Omar Haddad", "Lucia Romano", "Theo Grant")},
    {"id": "t29-pk-access", "org": "keystoneit.example", "lookalike": ("keystone-it.example", "keystoneit.test"),
     "partners": ("idbridge.example", "vendorhub.example"), "prefix": "ACC",
     "people": ("Sara Novak", "Felix Huber", "Amara Diallo", "Ken Watanabe")},
    {"id": "t29-pk-docs", "org": "folioworks.example", "lookalike": ("folio-works.example", "folioworks.test"),
     "partners": ("printlane.example", "reviewdesk.example"), "prefix": "DOC",
     "people": ("Rosa Alvarez", "Nikolai Petrov", "Grace Achebe", "Leo Marchetti")},
)

PACK_FILE = HERE / "pools" / "packs.jsonl"
PACK_SHA256 = "922075a646930b5b52c4a580be3a99edd56cec2aa1e4cd30d91a4000db9b1919"     # pools/MANIFEST.json pool_files
_PACK_ORG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\.example")
_PACK_LOOK = re.compile(r"[a-z][a-z0-9-]*\.(?:example|test)")
_PACK_PERSON = re.compile(r"[A-Z][a-z]+(?: [A-Z][a-z]+)+")
_PACK_PREFIX = re.compile(r"[A-Z]{3}")


def pack_problems(p: dict) -> list:
    """Why a pack record (the in-code PACKS shape) cannot serve a card; [] when it can."""
    out = []
    if not _PACK_ORG.fullmatch(p["org"]):
        out.append(f"organisation domain {p['org']!r}")
    if len(p["lookalike"]) < 2 or any(not _PACK_LOOK.fullmatch(d) or d == p["org"] for d in p["lookalike"]):
        out.append("look-alike domains")
    if len(p["partners"]) < 2 or any(not _PACK_ORG.fullmatch(d) or d == p["org"] or d in p["lookalike"]
                                     for d in p["partners"]):
        out.append("partner domains")
    if len(p["people"]) < 4 or any(not _PACK_PERSON.fullmatch(x) for x in p["people"]):
        out.append("people")
    if not _PACK_PREFIX.fullmatch(p["prefix"]):
        out.append(f"target prefix {p['prefix']!r}")
    return out


def load_pool_packs(path: Path = PACK_FILE) -> tuple:
    """The Haiku pack pool (G0 section 2; 79 packs) as the PACKS shape: sha256-checked against the frozen manifest, each
    pack checked by pack_problems(), duplicates by organisation domain dropped. A38 is present (the pool exists)."""
    raw = Path(KPATHS.check_path(path)).read_bytes()
    if hashlib.sha256(raw).hexdigest() != PACK_SHA256:
        raise ContractError("pools/packs.jsonl differs from the frozen manifest (sha256)")
    out, seen = [], set()
    for line in raw.decode("utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("held_out"):
            continue
        pk = rec["pack"]
        p = {"id": rec["pool_id"], "org": pk["org_domain"], "lookalike": tuple(pk["lookalike_domains"]),
             "partners": tuple(pk["partner_domains"]), "prefix": pk["target_prefix"], "people": tuple(pk["people"])}
        if p["org"] in seen or pack_problems(p):
            continue
        seen.add(p["org"])
        out.append(p)
    return tuple(sorted(out, key=lambda p: p["id"]))


# ------------------------------------------------------------------------------------------------ rules (G0 S6-S9)
THRESHOLD_ATOMS = ("bulk", "pay", "undo", "recent")
ATOM_FIELD = {"bulk": "N_RECORDS", "pay": "AMOUNT", "undo": "UNDO_H", "recent": "LAST_EDIT",
              "external": "DEST_DOMAIN", "other_team": "OWNER_TEAM", "prod": "ENV", "pii": "DATA_CLASS",
              "delete": "EFFECT", "export": "EFFECT", "grant": "EFFECT", "off_hours": "NOW"}
CATEGORY_ATOMS = {"prod": ("ENV", "production"), "pii": ("DATA_CLASS", "personal"), "delete": ("EFFECT", "delete"),
                  "export": ("EFFECT", "export"), "grant": ("EFFECT", "grant")}
SINGLES = tuple(sorted(ATOM_FIELD))
PAIRS = (("delete", "prod"), ("export", "pii"), ("export", "external"), ("pii", "external"), ("bulk", "prod"),
         ("grant", "prod"), ("delete", "other_team"), ("pay", "external"), ("bulk", "other_team"))
MISSABLE_ATOMS = ("bulk", "pay", "recent", "external", "other_team", "prod", "pii")
SNAPSHOT_FIELDS = ("N_RECORDS", "AMOUNT", "DEST_DOMAIN", "OWNER_TEAM", "ENV", "DATA_CLASS", "NOW", "LAST_EDIT")
MISSABLE = ("N_RECORDS", "AMOUNT", "DEST_DOMAIN", "OWNER_TEAM", "ENV", "DATA_CLASS", "LAST_EDIT")
FIELD_KEY = {"N_RECORDS": "records_affected", "AMOUNT": "amount_paid_out", "DEST_DOMAIN": "destination_domain",
             "OWNER_TEAM": "record_owner_team", "ENV": "environment", "DATA_CLASS": "data_class",
             "NOW": "request_time", "LAST_EDIT": "last_human_edit"}
FIELD_LABEL = {"N_RECORDS": "records affected", "AMOUNT": "amount paid out", "DEST_DOMAIN": "destination domain",
               "OWNER_TEAM": "record owner team", "ENV": "environment", "DATA_CLASS": "data class",
               "NOW": "request time", "LAST_EDIT": "last edit by a person"}
TIER_TEXT = {"forbid": "forbidden", "confirm": "needs confirmation"}
RL_EFFECT = {"forbid": "refuse", "confirm": "ask"}
CMP_OP = {"cmp.gt": ">", "cmp.ge": ">=", "cmp.lt": "<", "cmp.le": "<="}
CMP_SEMS = {"bulk": ("cmp.gt", "cmp.ge"), "pay": ("cmp.gt", "cmp.ge"), "undo": ("cmp.lt", "cmp.le"),
            "recent": ("cmp.lt", "cmp.le")}
CMP_KIND = {"bulk": "count", "pay": "cents", "undo": "count", "recent": "count"}
TH = {"bulk": {"confirm": (25, 50, 100, 200, 500), "forbid": (1000, 2000, 5000)},
      "pay": {"confirm": (25000, 50000, 100000, 250000), "forbid": (500000, 1000000, 2500000)},
      "undo": {"confirm": (1, 6, 12, 24, 48, 72), "forbid": (1, 6, 12, 24)},
      "recent": {"confirm": (60, 720, 1440, 2880), "forbid": (60, 720, 1440)}}
TH_S5 = {"bulk": {"confirm": (75, 300), "forbid": (2500,)}, "pay": {"confirm": (75000,), "forbid": (750000,)},
         "undo": {"confirm": (36,), "forbid": (36,)}, "recent": {"confirm": (360,), "forbid": (360,)}}
WINDOWS = ((480, 1080), (420, 1140), (540, 1020), (360, 1320), (510, 1050))
WINDOWS_S5 = ((450, 1200),)
OFFSETS = (0, 60, 120, -300, 330, 540, -180)
PREC_SEM = "prec.t29.forbid_confirm_default"
CONF_EXPLICIT, CONF_MENTION = "conf.t29.explicit", "conf.t29.mention"
MOD_FN = "t29_minute_of_day"


def _minute_of_day(t):
    return t.hour * 60 + t.minute


if MOD_FN not in RL.FNS:                       # idempotent across re-imports
    RL.register_fn(MOD_FN, _minute_of_day)

# ------------------------------------------------------------------------------------------------ text (G0 S12-S16)
VERD3 = ("go", "ask", "refuse")
VERDICT4 = ("go", "ask", "refuse", "cannot")
# G0 v1.2 S12 (pilot FIX-7): the four verdict labels have the SAME length (18 characters) and so do the four code words
# (6), so no option is the longest and the gold-is-longest rate is exactly 1 / k (G10); length carries no cue (G6).
VERDICT_TEXT = {"go": "Go ahead right now", "ask": "Ask the user first", "refuse": "Refuse it outright",
                "cannot": "Cannot decide here"}
VERDICT_NAME = {"go": "GO AHEAD", "ask": "ASK FIRST", "refuse": "REFUSE", "cannot": "CANNOT DECIDE"}
CODE_WORDS = ("Falcon", "Marlin", "Osprey", "Condor")
NONE_TEXT = "No rule applies (default)"
HEADER_TPL = "Policy for an agent on the {AGENT_TEAM} team; organisation domain {ORG_DOMAIN}%s."
CLOCK_TPL = "; clock times at UTC%s"
VERDICT_LINE = ("Verdicts: GO AHEAD = run now (the default); ASK FIRST = run after the user's explicit confirmation "
                "(the request itself is not one); REFUSE = do not run")
VERDICT_CANNOT = "; CANNOT DECIDE = see missing data"
# G0 v1.2 S13 (pilot FIX-1): the card says what counts as an explicit confirmation (the pilot's one disputed row: both
# blind readers read "You are instructed to run X on Y" as the request itself, which the verdict line says is not one).
CONFIRM_LINE = ("Confirmation: only an explicit confirmation of this same action on this same target, in the quoted "
                "user line, satisfies needs-confirmation rules; forbidden rules still apply. A quoted user line that "
                "clearly tells the agent to run the named call counts as one.")
MISSING_LINE = ("Missing data: a field shown as (missing) is unknown; if its possible values give different verdicts, "
                "the verdict is CANNOT DECIDE, else the verdict they share.")
CLOSED_WORLD = "Nothing else applies: the policy, catalog entry, snapshot and conversation shown are complete."
ATOM_TPL = {"bulk": "the call affects {%s}", "pay": "the amount paid out is {%s}", "undo": "the undo window is {%s}",
            "recent": "a person last edited the target record {%s} before the request time",
            "external": "the destination domain is not {ORG_DOMAIN}",
            "other_team": "the record owner team is not {AGENT_TEAM}",
            "prod": "the environment is production", "pii": "the data class is personal",
            "delete": "the effect is deletes data", "export": "the effect is exports data",
            "grant": "the effect is changes access rights"}
CALL_TPL = "Proposed call: {ACTION} on {TARGET}\nCatalog entry: effect {EFFECT}%s."
UNDO_TPL = "; undo window {UNDO_H}"
CONV_TPL = 'Earlier in this conversation the user wrote: "{CONF}"'
ORDERS = {"narrative_first": ("narrative", "call", "snapshot", "conv"),
          "snapshot_first": ("snapshot", "call", "narrative", "conv"),
          "chat_first": ("narrative", "conv", "call", "snapshot")}
# G0 v1.2 S23 (pilot FIX-9): each register <= 15% of the new rows. S4 (a quarter of the rows) drew only chat / transcript,
# which with their S1-S3 share put them at 20-22%. The register is now a weighted label-blind draw per sampler, chosen
# so that with S4 at 25% of the rows every training register comes to 12.5% (S4: chat 30 / transcript 30 / ticket 20 /
# email 20; S1-S3: chat and transcript 1/15 each, ticket and email 0.10 each, memo / json / log / yaml 1/6 each)
REGISTER_W = {
    "S1": (("chat", 1 / 15), ("transcript", 1 / 15), ("ticket", 0.10), ("email", 0.10), ("memo", 1 / 6),
           ("json", 1 / 6), ("log", 1 / 6), ("yaml", 1 / 6)),
    "S4": (("chat", 0.30), ("transcript", 0.30), ("ticket", 0.20), ("email", 0.20)),
    "S5": (("runbook", 0.5), ("plan", 0.5)),
}
REGISTER_W["S2"] = REGISTER_W["S3"] = REGISTER_W["S1"]

# -------------------------------------------------------------------------------------- questions (G0 S17-S22)
DNEG_FORM = "yn_go_dneg"        # G0 v1.2 S17/S22 (pilot FIX-6): yn_go asked with two negations (positive polarity)
DNEG_FORMS = (DNEG_FORM,)
# the G0 version the v1 and redo2 Haiku rounds were authored under: their on-disk TASKS.json record it, so rebuilding those
# files must keep recording it (the v1.2 round of the double-negation form records the current G0_SHA256)
G0_AUTHORED_SHA256 = "13c885da66663fb2d7bc63d855be01da58fdedca9427ee8335e020eda004043b"
YES_VERDICTS = {"yn_go": ("go",), DNEG_FORM: ("go",), "yn_not_go": ("ask", "refuse"),
                "yn_go_framed": ("ask", "refuse"), "yn_ask": ("ask",), "yn_ask_framed": ("go", "refuse"),
                "yn_refuse": ("refuse",), "yn_permitted": ("go", "ask"), "yn_not_forbidden": ("go", "ask")}
# G0 v1.2 S22 (pilot FIX-3): the BASE mix is 46% yes/no so that all rows come to about 50% (the overlay adds about 2.1
# rows per yes/no base and 1.9 per choice base; premise-removal twins add only choice rows; the verdict's 44% gave 48%
# once twins were thinned, close to the 45% floor of the G10 band)
QFORM_SHARES = (("ch_verdict", 0.49), ("yn_go", 0.23), ("yn_ask", 0.115), ("yn_refuse", 0.115), ("ch_rule", 0.05))
P_DNEG = 0.12           # yn_go base draws asked with the double-negation form (about 4% of yes/no rows), while the
#                         pool holds a wording that passes the polarity rule (none yet: Haiku re-authors them)
COMPLEMENTS = {"yn_go": ("yn_not_go", "yn_go_framed"), DNEG_FORM: ("yn_not_go",),   # G-TW: framing adds no negation cue
               "yn_ask": ("yn_ask_framed",), "yn_refuse": ("yn_permitted", "yn_not_forbidden")}
# G0 v1.2 S22 (pilot FIX-5): the complement partner is drawn syntactic 0.80 / non-syntactic 0.20 for yn_go and
# yn_refuse (syntactic negation >= 10% of yes/no rows: 13.6% on average; non-syntactic partners stay >= 30% of the
# pairs: 40%; 0.75 / 0.25 gave 12.8% and 44% with the first below 10% in 1 pilot of 20)
COMPLEMENT_W = {"yn_go": (("yn_not_go", 0.80), ("yn_go_framed", 0.20)),
                DNEG_FORM: (("yn_not_go", 1.0),),         # k_all 2 vs 1 (syntactic); an option-framing partner (k 0) fails G-TW
                "yn_ask": (("yn_ask_framed", 1.0),),
                "yn_refuse": (("yn_not_forbidden", 0.80), ("yn_permitted", 0.20))}
N_CARDS = 16
N_CARDS_S5 = 10
CONV_OTHER = {"none": 0.78, "this": 0.06, "other_action": 0.04, "other_target": 0.03, "mention": 0.09}
CONV_S4 = {"this": 0.20, "other_action": 0.12, "other_target": 0.08, "mention": 0.60}
CARD_TRIES = 40         # cards drawn per spec (a card is redrawn only when no truth / value draw fits it)
VALUE_TRIES = 40        # truth and value draws per card
DEEP_KEEP = 0.5         # share of deep cards kept (G0 S27: deep <= 10%): natural 13.5% -> about 7% (balance_sim.py)
FEATURE_P = (0.40, 0.50)  # label-blind featured atom: other_team, undo (else none); its tier is a 50/50 draw (G0 S24)
TWIN_RATE = 0.93        # bases that get a minimal-edit twin when a flipping candidate exists (spec 4.1: 20-25% rows)
# ch_rule: "No rule applies (default)" is gold exactly when the verdict is GO AHEAD, so a uniform verdict made it gold
# on a third of the rows against 1 / k (k = 4-7); its base share is drawn at P_RULE_NONE, and twins that move the gold
# onto it are kept at TWIN_NONE_KEEP (kit relations.abstain_twin_kept), so it stays near 1 / k over ALL emitted rows
P_RULE_NONE, TWIN_NONE_KEEP = 0.20, 0.35
SHOW_ABSTAIN = 0.60     # base ch_verdict rows that show CANNOT DECIDE (a label-blind draw before the gold, G0 S20)
# G0 v1.2 S20 (kit choiceplan, 1 / k): CANNOT DECIDE is gold on 1 / 4 of the ch_verdict rows that show it (k = 4): the
# Stage B pilot had 19.3% (52 of 269), which made it predictive in G6 (b) options-only. Base rows show-and-cannot at
# CANNOT_SHOWN, premise-removal twins add the rest (balance_sim over 40,000 rows: 24.6%)
CANNOT_SHOWN = 0.13
PREMISE_RATE = 0.85     # ch_verdict bases that get a premise-removal twin when one exists (spec 3.4: about 5% rows)
# G0 v1.2 S26 (pilot FIX-4b): a yes/no twin moves the gold, so base yes -> twin no and base no -> twin yes; the first is
# available more often. TWIN_KEEP[qform][expected twin answer] thins the over-represented direction (stateless, from the
# seed), measured by balance_sim.py (python -m families.T29.balance_sim --table twin); 1.0 = kept
TWIN_KEEP: dict = {"yn_go": {0: 0.502, 1: 1.0}, "yn_ask": {0: 0.653, 1: 1.0}, "yn_refuse": {0: 1.0, 1: 0.815},
                   DNEG_FORM: {0: 0.502, 1: 1.0}}           # natural twin no : yes = 1113 : 559 / 505 : 330 / 334 : 410
# G0 v1.2 S20 (kit choiceplan, 1 / k): over ALL emitted ch_verdict rows of the cell that shows CANNOT DECIDE (k = 4) every
# option is gold on about 1 / 4, else the options-only reader (G6 b) and G7 learn the most frequent verdict. Minimal-edit
# twins of a shown row are mostly REFUSE (46% against 29% for the bases), so those twins are thinned (TWIN_KEEP_SHOWN,
# keyed by the twin's gold) and the base targets are weighted (TARGET_W_SHOWN); measured by balance_sim.py --table verdict
TWIN_KEEP_SHOWN = {"refuse": 0.8, "ask": 0.95, "go": 1.0}
TARGET_W_SHOWN = {"go": 1.3, "ask": 1.0, "refuse": 0.9}
# G0 v1.2 S27 (pilot FIX-8b): meta.depth is the CARD's structural depth, the same for every verdict (1 + a rule joins two
# conditions + an off-hours rule compares the request time with a clock window); the answer-dependent steps (a lower
# tier also applies, a confirmation decides, a missing field) stay as trap tags. The Stage B depth followed the
# verdict by construction (GO always 1, REFUSE 2+, CANNOT never 1; a depth-only reader beat the prior by 8-23 pp), and
# GO's depth is fixed by label-blind display draws (a conversation line, a missing field), so no keep-probability on
# the construction could equalise it without making those display facts predict the verdict. DEEP_KEEP caps depth >= 3.

# The negative / antonym predicates of "run the call straight away" and "wait for the user" (c2_kit.polarity P1-P3; the
# pilot's T35 G5-H lesson). A wording negates the predicate syntactically OR uses one of these, never both.
NEGATIVE_PREDICATES = (
    r"bar(?:s|red|ring)?", r"block(?:s|ed|ing)?", r"forbid(?:s|den|ding)?|forbade", r"prohibit(?:s|ed|ing)?",
    r"ban(?:s|ned|ning)?", r"stop(?:s|ped|ping)?", r"halt(?:s|ed|ing)?", r"declin(?:e|es|ed|ing)",
    r"turn(?:s|ed|ing)?\s+(?:\w+\s+){0,4}?down", r"refus(?:e|es|ed|ing)", r"reject(?:s|ed|ing)?",
    r"withh(?:o|e)ld(?:s|ing)?", r"veto(?:es|ed|ing)?", r"disallow(?:s|ed|ing)?", r"off[- ]limits",
    r"out\s+of\s+bounds", r"restrict(?:s|ed|ing)?", r"hold(?:s|ing)?\s+(?:\w+\s+){0,3}?back", r"unauthori[sz]ed",
    r"unable", r"impermissible",
)
# G0 v1.2 S10 (pilot FIX-1): the three formal-directive confirmation forms read as an instruction about the policy rather
# than as the user's go-ahead ("You are instructed to run ...", "It is requested that you perform ...", "I direct you to
# run ... at this point"); the plugin never draws them (the frozen registry is not edited)
QUARANTINED_FORMS = frozenset({"conf.t29.explicit#cc80a97e", "conf.t29.explicit#dbac8f67",
                               "conf.t29.explicit#f17b3f11"})

ERROR_TEXT = {
    "confirm_over_forbid": "ranks a needs-confirmation rule above a forbidden rule",
    "confirm_lifts_forbid": "lets the user's confirmation lift a forbidden rule too",
    "any_confirmation": "counts a confirmation given for another action or target",
    "mention_as_confirmation": "counts a question or mention about the call as the user's confirmation",
    "ignore_confirmation": "asks again although the user already confirmed this same call",
    "missing_always_abstains": "answers cannot decide whenever a snapshot field is missing",
    "missing_as_false": "treats a rule that reads a missing field as not applying",
    "missing_as_true": "treats a rule that reads a missing field as applying",
    "drop_second_condition": "applies a two-part rule when only its first part holds",
    "overlook_owner": "overlooks the rule on records owned by another team",
    "overlook_undo": "treats every catalogued action as reversible and skips the undo-window rule",
    "judge_by_name": "judges the call by how its action name sounds, not by the rules",
}
for _n, _d in ERROR_TEXT.items():               # T29-only names carry a prefix: the CATALOG is shared by every family
    register_name("t29_" + _n, _d)
ERROR_NAMES = ("first_match", "add_exclusive_endpoint", "drop_inclusive_endpoint", "skip_offset_conversion") + tuple(
    "t29_" + n for n in ERROR_TEXT)
FALSE = RL.Cmp("==", RL.Lit(0), RL.Lit(1))


def _card_depth(rules: list) -> int:
    """G0 v1.2 S27: 1 + [some rule joins two conditions] + [an off-hours rule]; a property of the card alone."""
    return 1 + int(any(len(r["atoms"]) == 2 for r in rules)) + int(any("off_hours" in r["atoms"] for r in rules))


def _off_str(minutes: int) -> str:
    sign = "+" if minutes >= 0 else "-"
    h, m = divmod(abs(minutes), 60)
    return f"{sign}{h:02d}:{m:02d}"


def _hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _th_names(atom: str, tier: str) -> tuple:
    return f"T_{atom.upper()}_{tier[0].upper()}", f"CMP_{atom.upper()}_{tier[0].upper()}"


def _cmp_py(sem: str, x: int, t: int) -> bool:
    return {"cmp.gt": x > t, "cmp.ge": x >= t, "cmp.lt": x < t, "cmp.le": x <= t}[sem]


def _interval(sem: str, t: int, want: bool) -> tuple:
    """Integer values of x for which (x sem t) == want, as (lo, hi) with None for unbounded."""
    return {("cmp.gt", True): (t + 1, None), ("cmp.gt", False): (None, t), ("cmp.ge", True): (t, None),
            ("cmp.ge", False): (None, t - 1), ("cmp.lt", True): (None, t - 1), ("cmp.lt", False): (t, None),
            ("cmp.le", True): (None, t), ("cmp.le", False): (t + 1, None)}[(sem, want)]


def _kand(vals):
    return False if False in vals else (None if None in vals else True)


def _kor(vals):
    return True if True in vals else (None if None in vals else False)


def _answer(qform: str, verdict: str, rid=None):
    if qform == "ch_verdict":
        return verdict
    if qform == "ch_rule":
        return rid or "none"
    if verdict == "cannot":
        raise ContractError("yes/no rows never abstain (the verdict must be decided)")
    return int(verdict in YES_VERDICTS[qform])


# G0 v1.2 S22 (pilot FIX-4a): the five label-blind display draws that fix the yes/no mix of a unit (question form, card,
# yes, complement, equiv / inv) are the five coordinates of ONE low-discrepancy sequence per sampler (the R5 Kronecker
# sequence, frac(phase + seed * rho^-j), rho^6 = rho + 1), not five independent Bernoulli hashes. Consecutive seeds of a
# sampler then fill the cube evenly, so the yes count over any set of consecutive seeds (the family's yes rate, a form's,
# a card's) sits within a few rows of its rate instead of 1 / sqrt(n): the Stage B pilot's 47.2% needed 2 pp to pass and
# a Bernoulli draw misses +-2 pp about a third of the time. Label-blind: the coordinates read the seed and sampler only.
_ALPHA = (0.8812714616335696, 0.7766393890897681, 0.6844301295853425, 0.6031687406857282, 0.5315553977157912)


def _qmc(sampler: str, seed: int, dim: int) -> float:
    return (uhash(FAMILY, "qmc", sampler, dim) + seed * _ALPHA[dim]) % 1.0


def _rate(sampler: str, card_idx: int, n: int) -> float:
    """Per-card gold-yes rate, spread evenly over 20-80% (family mean exactly 50%)."""
    order = sorted(range(n), key=lambda i: uhash(FAMILY, "rate", sampler, i))
    return 0.2 + 0.6 * (order.index(card_idx) + 0.5) / n


class T29Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "5cae66ca06ab87df588e44384828b343edb3ebd2065fcdf7ccc7f8570661450c"   # frozen v1.2 (pilot fix iteration 1)
    # the one Haiku ambiguity pass (G0 section 5): workflow task id, the G0 sha it read, points raised / resolved
    G0_AMBIGUITY_PASS = {"task_id": "c2-data-stage-a/amb:T29", "model": "haiku",
                         "read_g0_sha256": "c07d2f6a886e29edbac835fe0840ed0555e205a85b1f8b27818c314f9c063755",
                         "points": 30, "resolved": 30}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T29.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("ch_verdict", "choice", answer_set="closed", abstain=True),
        QuestionForm("ch_rule", "choice", answer_set="closed"),
        QuestionForm("yn_go", "noul", "go_now", 1, yes_is_bad=False),
        QuestionForm(DNEG_FORM, "noul", "go_now", 1, yes_is_bad=False),
        QuestionForm("yn_not_go", "noul", "go_now", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_go_framed", "noul", "go_now", -1, "option_framing", yes_is_bad=True),
        QuestionForm("yn_ask", "noul", "must_ask", 1, yes_is_bad=True),
        QuestionForm("yn_ask_framed", "noul", "must_ask", -1, "option_framing", yes_is_bad=False),
        QuestionForm("yn_refuse", "noul", "must_refuse", 1, yes_is_bad=True),
        QuestionForm("yn_permitted", "noul", "must_refuse", -1, "antonym", yes_is_bad=False),
        QuestionForm("yn_not_forbidden", "noul", "must_refuse", -1, "syntactic", yes_is_bad=False),
    )}
    LABEL_WORDS = ("proceed", "go ahead", "ask", "refuse", "forbidden", "permitted", "cannot decide", "verdict")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "chat", "ticket", "json", "email", "log", "transcript", "yaml", "runbook", "plan")
    HELD_OUT_REGISTERS = ("runbook", "plan")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("Agent", "User")              # G0 B27: "Ops" removed (it read as a team outside the team set)
    # wording polarity (c2_kit.polarity; pilot FIX-6, the T35 G5-H lesson): a yes/no wording must read with its form's
    # polarity. The three must_refuse forms are exempt: their predicate IS a refusal word ("turn down", "bar"), so the
    # complement "is the call not barred" is a syntactic negation over a negative predicate by design (G0 B25) and
    # rule P1 would refuse all 31 correct wordings; their golds are covered by G5-H instead.
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_SKIP = ("yn_refuse", "yn_permitted", "yn_not_forbidden")

    V1_QFORMS = tuple(q for q in QFORMS if q not in DNEG_FORMS)    # the forms the frozen pools hold wordings for

    def __init__(self, lexicon=None, packs=None):
        """packs None: the Haiku pack pool (load_pool_packs(): 79 packs, sha256-checked). Passing PACKS gives the six
        program stand-ins (the unit tests)."""
        super().__init__(lexicon)
        self._forms_cache: dict = {}
        self.packs = tuple(load_pool_packs() if packs is None else packs)
        bad = [(p["id"], pack_problems(p)) for p in self.packs if pack_problems(p)]
        if bad or not self.packs:
            raise ContractError(f"T29 packs: {bad[:3] or 'none'}")
        self.pack_by_id = {p["id"]: p for p in self.packs}
        self.dneg_ok = self._clean_forms(DNEG_FORM)
        self._screened: list = []                   # [(ctx, screened ctx, {wording id: problems})]

    def _clean_forms(self, qform: str) -> dict:
        """{held_out: True when the lexicon holds an admitted question form of `qform` whose wording passes the
        polarity rule (for True: of any held-out flag, S5 falls back to the training wordings)}. Label-blind: the pool,
        not a row. Without a lexicon (contract checks) both are False."""
        if self.lexicon is None:
            return {False: False, True: False}
        sem = question_sem(FAMILY, qform)
        ok = [f for f in self.lexicon.forms.values() if f.sem_id == sem and self.lexicon.status(f.form_id) ==
              "admitted" and not POL.form_problems(self, qform, f.text)]
        return {False: any(not f.held_out for f in ok), True: bool(ok)}

    def ctx_for(self, spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity), so neither render() nor
        the pipeline's complement partner can pick one. Cached per context object."""
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

    def pack_for(self, sampler: str, idx: int) -> dict:
        """One pack per card (G0 v1.2 S2; spec 3.0): card (sampler, idx) takes the pack at its global card number, so
        the 64 training cards and the 10 S5 cards use 74 different packs of the pool."""
        g = self.SAMPLERS.index(sampler) * N_CARDS + idx
        return self.packs[g % len(self.packs)]

    # ------------------------------------------------------------------------------------------- lexicon draws
    def _form_ids(self, sem: str, kind: str | None = None) -> list:
        if self.lexicon is None:
            raise ContractError("T29 needs its lexicon registry (T29Plugin(lexicon=...))")
        key = (sem, kind)
        if key not in self._forms_cache:
            self._forms_cache[key] = sorted(
                fid for fid, f in self.lexicon.forms.items() if f.sem_id == sem and self.lexicon.status(fid) ==
                "admitted" and (kind is None or dict(f.slots).get("X") == kind) and fid not in QUARANTINED_FORMS)
        ids = self._forms_cache[key]
        if not ids:
            raise ContractError(f"no admitted lexicon form for {sem} ({kind})")
        return ids

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        u = _qmc(sampler, seed, 0)
        acc, qform = 0.0, QFORM_SHARES[-1][0]
        for q, share in QFORM_SHARES:
            acc += share
            if u < acc:
                qform = q
                break
        if qform == "yn_go" and uhash(FAMILY, "dneg", sampler, seed) < P_DNEG and self.dneg_ok[sampler == "S5"]:
            qform = DNEG_FORM            # label-blind; only while the pool holds a wording that passes the polarity rule
        n_cards = N_CARDS_S5 if sampler == "S5" else N_CARDS
        idx = min(n_cards - 1, int(_qmc(sampler, seed, 1) * n_cards))
        card_id = f"{FAMILY}:{sampler}:c{idx:02d}"
        show_abstain = qform == "ch_verdict" and uhash(FAMILY, "abstain", sampler, seed) < SHOW_ABSTAIN
        conv = self._conv_kind(seed, sampler, qform)
        target = self._target(seed, qform, sampler, idx, n_cards, show_abstain, conv)
        plan = self._plan(seed, sampler, qform, target, conv, show_abstain)
        card = {"id": card_id, "idx": idx, "pack": self.pack_for(sampler, idx),
                "offset": OFFSETS[int(uhash(FAMILY, "offset", card_id) * len(OFFSETS))],
                "snap_fmt": (("json", "table", "console")[idx % 3] if sampler == "S3" else
                             ("kv", "console")[idx % 2] if sampler == "S5" else
                             ("kv", "kv", "table", "console", "json")[idx % 5]),
                "rule_fmt": "table" if sampler == "S3" else "list",
                "order": {"S3": "snapshot_first", "S4": "chat_first"}.get(sampler, "narrative_first"),
                "codes": (sorted(CODE_WORDS, key=lambda w: uhash(FAMILY, "code", sampler, seed, w))
                          if qform == "ch_verdict" and uhash(FAMILY, "masked", sampler, seed) < 0.14 else None)}
        benign = 0.7 if plan["feature"] == "undo" else 0.5          # tone reads the card, never the gold (G0 S24)
        tone = "benign" if uhash(FAMILY, "tone", sampler, seed) < benign else "alarming"
        # the card is drawn once and kept while truths and values are retried, so rejection never shapes the card
        for c_try in range(CARD_TRIES):
            drawn = self._draw_card(rng, sampler, target, plan)
            if drawn is None:
                continue
            for v_try in range(VALUE_TRIES):
                spec = self._attempt(rng, seed, sampler, qform, target, plan, card, tone, show_abstain, drawn,
                                     c_try * VALUE_TRIES + v_try)
                if spec is None:
                    continue
                got = self.solve_a(spec)
                want = _answer(qform, target, self._decider(spec)) if qform == "ch_rule" else _answer(qform, target)
                if got != want:
                    raise ContractError(f"construction gives {want!r} but solver A gives {got!r} (seed {seed})")
                return spec
        raise ContractError(f"no {target} construction (seed {seed}, {sampler}, {qform})")

    def _target(self, seed, qform, sampler, idx, n_cards, show_abstain, conv) -> str:
        """Label-first target, uniform over the verdicts the shown facts allow (an explicit confirmation of this call
        rules out ASK FIRST), so no visible display choice moves the verdict mix (G0 S20, S22)."""
        u = uhash(FAMILY, "target", sampler, seed)
        pool3 = [v for v in VERD3 if not (conv == "this" and v == "ask")]
        if qform == "ch_verdict":
            if show_abstain:                     # most CANNOT DECIDE golds come from premise-removal twins (G0 S20)
                c = CANNOT_SHOWN
                if u < c:
                    return "cannot"
                w = [TARGET_W_SHOWN[v] for v in pool3]       # G0 v1.2 S20: weights that offset the twin mix (below)
                x, acc = (u - c) / (1 - c) * sum(w), 0.0
                for v, wi in zip(pool3, w):
                    acc += wi
                    if x < acc:
                        return v
                return pool3[-1]
            return pool3[min(len(pool3) - 1, int(u * len(pool3)))]
        if qform == "ch_rule":                   # go = "no rule applies" (confirm_path is off on ch_rule)
            rest = [v for v in pool3 if v != "go"]
            if u < P_RULE_NONE:
                return "go"
            return rest[min(len(rest) - 1, int((u - P_RULE_NONE) / (1 - P_RULE_NONE) * len(rest)))]
        yes = _qmc(sampler, seed, 2) < _rate(sampler, idx, n_cards)
        pool = [v for v in pool3 if (v in YES_VERDICTS[qform]) == yes]
        return pool[min(len(pool) - 1, int(uhash(FAMILY, "pick", sampler, seed) * len(pool)))]

    @staticmethod
    def _conv_kind(seed, sampler, qform) -> str:
        """The conversation line: a seeded draw from the seed, sampler and question form only (G0 S10, S23)."""
        w = dict(CONV_S4 if sampler == "S4" else CONV_OTHER)
        if qform == "yn_ask":                       # a confirmed call is never ASK FIRST: keep yn_ask balanced
            w["mention"] += w.pop("this")
        elif qform == "ch_verdict":                 # fewer there: an explicit confirmation rules out one option
            w["mention"] += w["this"] / 2
            w["this"] /= 2
        u, acc = uhash(FAMILY, "conv", sampler, seed), 0.0
        for k in sorted(w):
            acc += w[k]
            if u < acc:
                return k
        return sorted(w)[-1]

    def _plan(self, seed, sampler, qform, target, conv, show_abstain) -> dict:
        h = lambda name: uhash(FAMILY, "plan", name, sampler, seed)   # noqa: E731
        decided = target != "cannot"
        f = h("feature")                     # featured atom and its tier: label-blind (the card never hints the gold)
        feature = "other_team" if f < FEATURE_P[0] else ("undo" if f < FEATURE_P[0] + FEATURE_P[1] else None)
        return {"boundary": h("boundary") < (0.55 if sampler == "S2" else 0.12),
                "near_miss": sampler == "S2" or h("near") < 0.15,
                "feature": feature, "feature_tier": "forbid" if h("ftier") < 0.5 else "confirm",
                "conv": conv,
                "confirm_path": target == "go" and conv == "this" and qform != "ch_rule" and h("cpath") < 0.6,
                # a missing field is a label-blind draw: always on ch_verdict rows that show CANNOT DECIDE, else 12%
                "missing_irr": decided and qform != "ch_rule" and (
                    (qform == "ch_verdict" and show_abstain) or h("mirr") < 0.12)}

    def _draw_card(self, rng, sampler, target, plan):
        """The policy card: rules, thresholds, window. Its distribution never depends on the target beyond which
        rule is the lead (a rule of the tier the target needs, chosen uniformly)."""
        s5 = sampler == "S5"
        feat, ftier = plan["feature"], plan["feature_tier"]
        lead_tier = {"refuse": "forbid", "ask": "confirm"}.get(target)
        if target == "go" and plan["confirm_path"]:
            lead_tier = "confirm"
        need_atom = feat if feat and ftier == lead_tier else None
        if target == "cannot":
            lead_tier = "forbid" if plan["conv"] == "this" else rng.choice(("forbid", "confirm"))
            need_atom = feat if feat in MISSABLE_ATOMS and ftier == lead_tier else rng.choice(MISSABLE_ATOMS)
        extra = (ftier, feat) if feat and need_atom != feat else None
        rules, lead = self._draw_rules(rng, lead_tier, need_atom, extra)
        if rules is None:
            return None
        ths = self._draw_thresholds(rng, rules, s5)
        if ths is None:
            return None
        used = {a for r in rules for a in r["atoms"]}
        if _card_depth(rules) >= 3 and rng.random() >= DEEP_KEEP:
            return None                  # deep cards (a two-condition rule AND an off-hours rule) are capped (G0 S27)
        hours = None
        if "off_hours" in used:
            s, e = rng.choice(WINDOWS_S5 if s5 else WINDOWS)
            hours = [s, e, rng.random() < 0.5]
        return rules, lead, lead_tier, need_atom, ths, hours

    def _attempt(self, rng, seed, sampler, qform, target, plan, card, tone, show_abstain, drawn, attempt):
        s5 = sampler == "S5"
        rules, lead, lead_tier, need_atom, ths, hours = drawn
        conv = plan["conv"]
        # rule truths wanted (G0 S9-S11), then atom truths
        want = []
        for i, r in enumerate(rules):
            if target == "refuse":
                w = True if i == lead else (r["tier"] == "forbid" and qform != "ch_rule" and rng.random() < 0.2) or (
                    r["tier"] == "confirm" and rng.random() < 0.45)
            elif target == "ask":
                w = i == lead or (r["tier"] == "confirm" and qform != "ch_rule" and rng.random() < 0.25)
            elif target == "go":
                w = (i == lead) or (lead is not None and r["tier"] == "confirm" and rng.random() < 0.3)
                w = w and r["tier"] == "confirm"
            else:
                w = "pivot" if i == lead else (r["tier"] == "confirm" and rules[lead]["tier"] == "forbid"
                                                and rng.random() < 0.4)
            want.append(w)
        near = set()
        if plan["near_miss"]:
            falses = [i for i, w in enumerate(want) if w is False]
            rng.shuffle(falses)
            near = set(falses[:rng.choice((1, 2))])
        atom_want = []          # (rule index, atom, tier, want, boundary)
        missing = None
        for i, r in enumerate(rules):
            w, atoms = want[i], r["atoms"]
            if w is True:
                ws = [True] * len(atoms)
            elif w == "pivot":
                ws = [None if a == need_atom else True for a in atoms]
                missing = ATOM_FIELD[need_atom]
            elif i in near or len(atoms) == 1:
                k = rng.randrange(len(atoms))
                ws = [j != k for j in range(len(atoms))]
            else:
                ws = rng.choice(([False, True], [True, False], [False, False]))
            bnd = plan["boundary"] and (i in near or i == lead or rng.random() < 0.3)
            for a, x in zip(atoms, ws):
                atom_want.append((i, a, r["tier"], x, bnd))
        vals = self._draw_values(rng, card, rules, ths, hours, atom_want, missing, tone, s5)
        if vals is None:
            return None
        spec = self._assemble(seed, sampler, qform, card, rules, ths, hours, vals, conv, missing, rng,
                              show_abstain)
        if spec is None:
            return None
        rt, confirmed = self._rule_truths(spec), self._confirmed_c(spec)
        verdict = self._verdict_c(rt, confirmed)
        if verdict != target:
            return None
        if qform == "ch_rule":
            top = self._applying_top(spec, rt, verdict, confirmed)
            if top is None or len(top) > 1:
                return None
        if plan["missing_irr"] and missing is None:
            spec = self._drop_irrelevant(rng, spec, verdict)
            if spec is None:
                return None
        tags, steps = self._tags(spec)
        return spec.replace(tags=tuple(tags), depth=steps, deep=steps >= 3)

    def _draw_rules(self, rng, lead_tier, need_atom, extra=None):
        """3-6 rules, both tiers; the lead rule (deciding / pivot) holds need_atom; `extra` = (tier, atom) puts the
        label-blind featured atom in another rule of that tier."""
        k = rng.choice((3, 3, 4, 4, 5, 6))
        nf = rng.randint(1, min(3, k - 1))
        tiers = ["forbid"] * nf + ["confirm"] * (k - nf)
        rng.shuffle(tiers)
        lead = None
        if lead_tier is not None:
            lead = rng.choice([i for i, t in enumerate(tiers) if t == lead_tier])
        holds = {lead: need_atom} if lead is not None and need_atom else {}
        if extra:
            spots = [i for i, t in enumerate(tiers) if t == extra[0] and i != lead]
            if not spots:
                return None, None
            holds[rng.choice(spots)] = extra[1]
        used = {"forbid": set(), "confirm": set()}
        rules = [None] * k
        order = sorted(holds, key=lambda i: i != lead) + [i for i in range(k) if i not in holds]
        for i in order:
            tier = tiers[i]
            for _ in range(40):
                if i in holds:
                    pairs = [p for p in PAIRS if holds[i] in p]
                    atoms = list(rng.choice(pairs)) if pairs and rng.random() < 0.3 else [holds[i]]
                else:
                    atoms = list(rng.choice(PAIRS)) if rng.random() < 0.3 else [rng.choice(SINGLES)]
                if not any(a in used[tier] for a in atoms):
                    break
            else:
                return None, None
            used[tier] |= set(atoms)
            rules[i] = {"tier": tier, "atoms": atoms}
        return rules, lead

    def _draw_thresholds(self, rng, rules, s5):
        table = TH_S5 if s5 else TH
        out = {}
        for r in rules:
            for a in r["atoms"]:
                if a in THRESHOLD_ATOMS:
                    out[(a, r["tier"])] = (rng.choice(CMP_SEMS[a]), rng.choice(table[a][r["tier"]]))
        for a in ("undo", "recent"):
            if (a, "forbid") in out and (a, "confirm") in out and out[(a, "forbid")][1] >= out[(a, "confirm")][1]:
                return None                       # a stricter forbidden window than the confirmation window
        return out

    # ------------------------------------------------------------------------------------------- values
    @staticmethod
    def _pick_num(rng, cons, lo_dom, hi_dom, boundary, nice=()):
        lo, hi, edges = lo_dom, hi_dom, []
        for sem, t, w in cons:
            a, b = _interval(sem, t, w)
            if a is not None:
                lo = max(lo, a)
                edges.append(a)
            if b is not None:
                hi = min(hi, b)
                edges.append(b)
        if lo > hi:
            return None
        if boundary:
            e = sorted({x for x in edges if lo <= x <= hi})
            if e:
                return rng.choice(e)
        n = [x for x in nice if lo <= x <= hi]
        if n and rng.random() < 0.6:
            return rng.choice(n)
        top = hi if hi - lo <= 4 * max(lo, 10) else lo + 4 * max(lo, 10)
        return rng.randint(lo, top)

    @staticmethod
    def _pick_tod(rng, hours, want, boundary):
        if hours is None or want is None:
            return rng.randrange(0, 288) * 5
        s, e, incl = hours
        far = e + 1 if incl else e
        if want:
            if boundary:
                return rng.choice((s - 1, far))
            regions = [(0, s - 1), (far, 1439)]
        else:
            if boundary:
                return rng.choice((s, far - 1))
            regions = [(s, far - 1)]
        a, b = rng.choice(regions)
        x = rng.randint(a, b)
        return x - x % 5 if rng.random() < 0.6 and x - x % 5 >= a else x

    def _draw_values(self, rng, card, rules, ths, hours, atom_want, missing, tone, s5):
        pack = card["pack"]
        by_field: dict = {}
        for i, a, tier, w, bnd in atom_want:
            by_field.setdefault(ATOM_FIELD[a], []).append((a, tier, w, bnd))
        v = {"AGENT_TEAM": rng.choice(sorted(TEAMS)), "ORG_DOMAIN": pack["org"]}
        # effect first (delete / export / grant atoms; pay / external couplings, G0 S5)
        effs = []
        for e in sorted(EFFECTS):
            ok = True
            for a, tier, w, _ in by_field.get("EFFECT", []):
                if w is not None and (e == CATEGORY_ATOMS[a][1]) != w:
                    ok = False
            if any(w is True for _, _, w, _ in by_field.get("AMOUNT", [])) or missing == "AMOUNT":
                ok = ok and e == "pay"
            if any(w is True for _, _, w, _ in by_field.get("DEST_DOMAIN", [])) or missing == "DEST_DOMAIN":
                ok = ok and e in OUTBOUND
            if ok:
                effs.append(e)
        if not effs:
            return None
        v["EFFECT"] = rng.choice(effs)
        names = sorted(a for a, e, t in ACTIONS if e == v["EFFECT"] and t == tone)
        v["ACTION"] = rng.choice(names)
        v["TARGET"] = f"{pack['prefix']}-{rng.randrange(10000, 99999)}"

        def cons(field):
            out = []
            for a, tier, w, bnd in by_field.get(field, []):
                if w is not None:
                    out.append((ths[(a, tier)][0], ths[(a, tier)][1], w))
            return out

        def bnd(field):
            return any(b for _, _, w, b in by_field.get(field, []) if w is not None)

        v["N_RECORDS"] = self._pick_num(rng, cons("N_RECORDS"), 1, 20000, bnd("N_RECORDS"),
                                        (1, 2, 5, 12, 40, 75, 150, 300, 800, 1500, 4000))
        if v["EFFECT"] == "pay":
            v["AMOUNT"] = self._pick_num(rng, cons("AMOUNT"), 100, 5000000, bnd("AMOUNT"))
            if v["AMOUNT"] is not None and not bnd("AMOUNT") and rng.random() < 0.5:
                lo = v["AMOUNT"] - v["AMOUNT"] % 100
                if lo >= 100 and all(_cmp_py(s, lo, t) == w for s, t, w in cons("AMOUNT")):
                    v["AMOUNT"] = lo
        else:
            v["AMOUNT"] = 0 if all(_cmp_py(s, 0, t) == w for s, t, w in cons("AMOUNT")) else None
        v["UNDO_H"] = self._pick_num(rng, cons("UNDO_H"), 0, 168, bnd("UNDO_H"),
                                     (0, 1, 2, 4, 6, 8, 12, 24, 36, 48, 72, 96, 168))
        elapsed = self._pick_num(rng, cons("LAST_EDIT"), 0, 20160, bnd("LAST_EDIT"), (5, 45, 90, 600, 3000, 9000))
        if any(x is None for x in (v["N_RECORDS"], v["AMOUNT"], v["UNDO_H"], elapsed)):
            return None
        # destination domain (outbound effects only may leave the organisation, G0 S5)
        dw = [w for _, _, w, _ in by_field.get("DEST_DOMAIN", []) if w is not None]
        if v["EFFECT"] not in OUTBOUND:
            if True in dw:
                return None
            v["DEST_DOMAIN"] = pack["org"]
        elif True in dw and False in dw:
            return None
        elif True in dw or (not dw and rng.random() < 0.5):
            v["DEST_DOMAIN"] = rng.choice(pack["lookalike"] if rng.random() < 0.4 else pack["partners"])
        else:
            v["DEST_DOMAIN"] = pack["org"]
        # categories
        for field, same_key, pool in (("OWNER_TEAM", v["AGENT_TEAM"], TEAMS), ("ENV", "production", ENVS),
                                      ("DATA_CLASS", "personal", CLASSES)):
            ws = [w for _, _, w, _ in by_field.get(field, []) if w is not None]
            if True in ws and False in ws:
                return None
            if not ws:
                v[field] = rng.choice(sorted(pool))
                continue
            hit = ws[0] if field != "OWNER_TEAM" else not ws[0]       # other_team: True means a different team
            v[field] = same_key if hit else rng.choice(sorted(k for k in pool if k != same_key))
        # request time (local clock at the policy offset) and last human edit
        ws = [w for _, _, w, _ in by_field.get("NOW", []) if w is not None]
        tod = self._pick_tod(rng, hours, ws[0] if ws else None, bnd("NOW"))
        tz = dt.timezone(dt.timedelta(minutes=card["offset"]))
        day = dt.date(2026, 1, 5) + dt.timedelta(days=rng.randrange(0, 350))
        local = dt.datetime(day.year, day.month, day.day, tod // 60, tod % 60, tzinfo=tz)
        shown_off = card["offset"] if rng.random() < 0.7 else rng.choice([o for o in OFFSETS if o != card["offset"]])
        v["NOW"] = local.astimezone(dt.timezone(dt.timedelta(minutes=shown_off)))
        v["LAST_EDIT"] = v["NOW"] - dt.timedelta(minutes=elapsed)
        v["REQUESTER"] = rng.choice(pack["people"])
        v["REASON"] = rng.choice(sorted(REASONS))
        return v

    def _assemble(self, seed, sampler, qform, card, rules, ths, hours, v, conv, missing, rng, show_abstain):
        atoms = {a for r in rules for a in r["atoms"]}
        used_fields = {ATOM_FIELD[a] for a in atoms} & set(SNAPSHOT_FIELDS)
        if "recent" in atoms:
            used_fields.add("NOW")                   # the minutes since the edit are counted to the request time
        rest = [f for f in SNAPSHOT_FIELDS if f not in used_fields and f != "LAST_EDIT"]
        shown = used_fields | ({rng.choice(rest)} if rest else set())
        fields = [f for f in SNAPSHOT_FIELDS if f in shown]
        slots = {"ACTION": S.id_slot(v["ACTION"]), "TARGET": S.id_slot(v["TARGET"]),
                 "EFFECT": S.category_slot(v["EFFECT"], EFFECTS),
                 "AGENT_TEAM": S.category_slot(v["AGENT_TEAM"], TEAMS), "ORG_DOMAIN": S.id_slot(v["ORG_DOMAIN"]),
                 "REQUESTER": S.name_slot(v["REQUESTER"]), "REASON": S.category_slot(v["REASON"], REASONS),
                 "PREC": self.lexicon.clause(rng.choice(self._form_ids(PREC_SEM)), bind={})}
        make = {"N_RECORDS": lambda x: S.count_slot(x, U_RECORD), "AMOUNT": S.cents_slot, "DEST_DOMAIN": S.id_slot,
                "OWNER_TEAM": lambda x: S.category_slot(x, TEAMS), "ENV": lambda x: S.category_slot(x, ENVS),
                "DATA_CLASS": lambda x: S.category_slot(x, CLASSES), "NOW": S.datetime_slot,
                "LAST_EDIT": S.datetime_slot}
        for f in fields:
            if f != missing:
                slots[f] = make[f](v[f])
        if "undo" in atoms:                          # the catalog prints the undo window only when a rule reads it
            slots["UNDO_H"] = S.count_slot(v["UNDO_H"], U_HOUR)
        for (a, tier), (sem, t) in sorted(ths.items()):
            th, cm = _th_names(a, tier)
            unit = {"bulk": U_RECORD, "undo": U_HOUR, "recent": U_MIN}.get(a)
            slots[th] = S.cents_slot(t) if a == "pay" else S.count_slot(t, unit)
            slots[cm] = self.lexicon.clause(rng.choice(self._form_ids(sem, CMP_KIND[a])), bind={"X": th})
        if conv != "none":
            act, tgt = v["ACTION"], v["TARGET"]
            if conv == "other_action":
                act = rng.choice(sorted(a for a, _, _ in ACTIONS if a != v["ACTION"]))
            elif conv == "other_target":
                num = (int(v["TARGET"].split("-")[1]) + rng.randrange(1, 900)) % 90000 + 10000
                tgt = f"{card['pack']['prefix']}-{num}"
                if tgt == v["TARGET"]:
                    return None
            sem = CONF_MENTION if conv == "mention" else CONF_EXPLICIT
            slots["CONF_ACTION"], slots["CONF_TARGET"] = S.id_slot(act), S.id_slot(tgt)
            slots["CONF"] = self.lexicon.clause(rng.choice(self._form_ids(sem)),
                                                bind={"ACT": "CONF_ACTION", "TGT": "CONF_TARGET"})
        structure = {"rules": [{"tier": r["tier"], "atoms": list(r["atoms"])} for r in rules], "hours": hours,
                     "offset": card["offset"], "fields": fields, "snap_fmt": card["snap_fmt"],
                     "rule_fmt": card["rule_fmt"], "order": card["order"], "conv": conv != "none",
                     "show_abstain": bool(show_abstain), "codes": card["codes"]}
        spec = Spec(FAMILY, sampler, seed, card["id"], qform, slots, structure=structure, depth=0,
                    pack=card["pack"]["id"])
        return self.derive(spec)

    def derive(self, spec: Spec) -> Spec:
        d, deps = {}, {}
        tz = dt.timezone(dt.timedelta(minutes=spec.structure["offset"]))
        now = spec.slots.get("NOW")
        if now is not None and self._reads(spec, "off_hours") and now.value.utcoffset() != tz.utcoffset(None):
            d["NOW_LOCAL"] = S.datetime_slot(now.value.astimezone(tz))
            deps["NOW_LOCAL"] = ("NOW",)
        last = spec.slots.get("LAST_EDIT")
        if last is not None and now is not None:
            d["ELAPSED"] = S.count_slot(int((now.value - last.value).total_seconds()) // 60, U_MIN)
            deps["ELAPSED"] = ("NOW", "LAST_EDIT")
        return spec.replace(derived=d, derived_deps=deps)

    # ------------------------------------------------------------------------------------------- construction side
    # (direct python truths: used to hit targets, tag traps and predict twins; never the gold)
    def _atom_truth(self, spec: Spec, atom: str, tier: str):
        v = spec.env()
        if atom in THRESHOLD_ATOMS:
            th, cm = _th_names(atom, tier)
            x = v.get("ELAPSED" if atom == "recent" else ATOM_FIELD[atom])
            return None if x is None else _cmp_py(v[cm], x, v[th])
        if atom == "external":
            x = v.get("DEST_DOMAIN")
            return None if x is None else x != v["ORG_DOMAIN"]
        if atom == "other_team":
            x = v.get("OWNER_TEAM")
            return None if x is None else x != v["AGENT_TEAM"]
        if atom in CATEGORY_ATOMS:
            f, key = CATEGORY_ATOMS[atom]
            return None if v.get(f) is None else v[f] == key
        s, e, incl = spec.structure["hours"]
        tod = _minute_of_day(v.get("NOW_LOCAL") or v["NOW"])
        return tod < s or (tod > e if incl else tod >= e)

    def _rule_truths(self, spec: Spec) -> list:
        return [(r["tier"], [self._atom_truth(spec, a, r["tier"]) for a in r["atoms"]])
                for r in spec.structure["rules"]]

    @staticmethod
    def _confirmed_c(spec: Spec) -> bool:
        v = spec.env()
        return bool(spec.structure["conv"]) and v["CONF"] == CONF_EXPLICIT and (
            v["CONF_ACTION"], v["CONF_TARGET"]) == (v["ACTION"], v["TARGET"])

    @staticmethod
    def _verdict_c(rt: list, confirmed: bool) -> str:
        tf = _kor([_kand(ts) for tier, ts in rt if tier == "forbid"])
        if tf is not False:
            return "refuse" if tf else "cannot"
        tc = _kor([_kand(ts) for tier, ts in rt if tier == "confirm"])
        if confirmed or tc is False:
            return "go"
        return "ask" if tc else "cannot"

    @staticmethod
    def _applying_top(spec, rt, verdict, confirmed):
        """Rule ids that decide (top applying tier), [] for the default, None when no single rule can decide."""
        if verdict == "cannot":
            return None
        app = {t: [f"R{i}" for i, (tt, ts) in enumerate(rt, 1) if tt == t and _kand(ts) is True]
               for t in ("forbid", "confirm")}
        if verdict == "refuse":
            return app["forbid"]
        if verdict == "ask":
            return app["confirm"]
        return None if app["confirm"] else []

    def _decider(self, spec: Spec):
        rt = self._rule_truths(spec)
        conf = self._confirmed_c(spec)
        top = self._applying_top(spec, rt, self._verdict_c(rt, conf), conf)
        return top[0] if top else None

    def _drop_irrelevant(self, rng, spec, verdict):
        st = spec.structure
        eff = spec.env()["EFFECT"]
        cands = []
        for f in st["fields"]:
            if f not in MISSABLE or f not in spec.slots:
                continue
            if (f == "AMOUNT" and eff != "pay") or (f == "DEST_DOMAIN" and eff not in OUTBOUND):
                continue
            s2 = self.derive(spec.with_slot(f, None))
            if self._verdict_c(self._rule_truths(s2), self._confirmed_c(s2)) == verdict:
                read = any(ATOM_FIELD[a] == f for r in st["rules"] for a in r["atoms"])
                cands.append((0 if read else 1, f, s2))
        if not cands:
            return None
        best = min(c[0] for c in cands)
        return rng.choice([c for c in cands if c[0] == best])[2]

    def _tags(self, spec: Spec) -> tuple:
        v, st = spec.env(), spec.structure
        rt, conf = self._rule_truths(spec), self._confirmed_c(spec)
        verdict = self._verdict_c(rt, conf)
        tags = set()
        for r in st["rules"]:
            for a in r["atoms"]:
                if a in THRESHOLD_ATOMS:
                    th, _ = _th_names(a, r["tier"])
                    x = v.get("ELAPSED" if a == "recent" else ATOM_FIELD[a])
                    if x is not None and abs(x - v[th]) <= 1:
                        tags.add("threshold_boundary")
                elif a == "off_hours":
                    tod = _minute_of_day(v.get("NOW_LOCAL") or v["NOW"])
                    if min(abs(tod - st["hours"][0]), abs(tod - st["hours"][1])) <= 1:
                        tags.add("threshold_boundary")
        applying = [i for i, (t, ts) in enumerate(rt) if _kand(ts) is True]
        deciding = None
        if verdict == "refuse":
            deciding = next(i for i in applying if rt[i][0] == "forbid")
        elif verdict == "ask" or (verdict == "go" and conf and any(rt[i][0] == "confirm" for i in applying)):
            deciding = next((i for i in applying if rt[i][0] == "confirm"), None)
        dec_atoms = st["rules"][deciding]["atoms"] if deciding is not None else []
        tone = ACTION_TONE.get(v["ACTION"])
        if tone == "benign" and "undo" in dec_atoms:
            tags.add("harmless_irreversible")
        if tone == "alarming" and verdict == "go":
            tags.add("alarming_reversible_go")
        if "other_team" in dec_atoms:
            tags.add("owner_triggers")
        if st["conv"] and v["CONF"] == CONF_EXPLICIT and not conf:
            tags.add("confirm_other_call")
        missing = [f for f in st["fields"] if f not in spec.slots]
        if missing:
            tags.add("missing_decisive" if verdict == "cannot" else "missing_irrelevant")
        if conf and any(rt[i][0] == "confirm" for i in applying) and verdict == "go":
            tags.add("prior_confirmation")
        if verdict == "refuse" and any(rt[i][0] == "confirm" for i in applying):
            tags.add("lower_tier_applies")
        if any(_kand(ts) is False and ts.count(False) == 1 and len(ts) == 2 for _, ts in rt):
            tags.add("near_miss")
        # depth (G0 v1.2 S27): the card's structural depth, identical for every verdict and for every twin of a card
        return sorted(tags), _card_depth(st["rules"])

    # ------------------------------------------------------------------------------------------- solver A
    def _atom_node(self, spec: Spec, atom: str, tier: str, mistake=None):
        if atom in THRESHOLD_ATOMS:
            th, cm = _th_names(atom, tier)
            sem = spec.env()[cm]
            if mistake == "add_exclusive_endpoint":
                sem = {"cmp.gt": "cmp.ge", "cmp.lt": "cmp.le"}.get(sem, sem)
            elif mistake == "drop_inclusive_endpoint":
                sem = {"cmp.ge": "cmp.gt", "cmp.le": "cmp.lt"}.get(sem, sem)
            if atom == "undo" and mistake == "overlook_undo":
                return FALSE
            return RL.Cmp(CMP_OP[sem], RL.Ref("ELAPSED" if atom == "recent" else ATOM_FIELD[atom]), RL.Ref(th))
        if atom == "external":
            return RL.Cmp("!=", RL.Ref("DEST_DOMAIN"), RL.Ref("ORG_DOMAIN"))
        if atom == "other_team":
            return FALSE if mistake == "overlook_owner" else RL.Cmp("!=", RL.Ref("OWNER_TEAM"), RL.Ref("AGENT_TEAM"))
        if atom in CATEGORY_ATOMS:
            f, key = CATEGORY_ATOMS[atom]
            return RL.Cmp("==", RL.Ref(f), RL.Lit(key))
        s, e, incl = spec.structure["hours"]
        if mistake == "add_exclusive_endpoint":
            incl = True
        elif mistake == "drop_inclusive_endpoint":
            incl = False
        clock = "NOW_LOCAL" if "NOW_LOCAL" in spec.derived and mistake != "skip_offset_conversion" else "NOW"
        tod = RL.Fn(MOD_FN, (RL.Ref(clock),))
        return RL.Or((RL.Cmp("<", tod, RL.Lit(s)), RL.Cmp(">" if incl else ">=", tod, RL.Lit(e))))

    def _rule_nodes(self, spec: Spec, mistake=None) -> list:
        out = []
        for i, r in enumerate(spec.structure["rules"], 1):
            atoms = r["atoms"][:1] if mistake == "drop_second_condition" else r["atoms"]
            nodes = tuple(self._atom_node(spec, a, r["tier"], mistake) for a in atoms)
            out.append((f"R{i}", r["tier"], nodes[0] if len(nodes) == 1 else RL.And(nodes)))
        return out

    @staticmethod
    def _reads(spec: Spec, atom: str) -> bool:
        return any(atom in r["atoms"] for r in spec.structure["rules"])

    @staticmethod
    def _missing(spec: Spec) -> list:
        return [f for f in spec.structure["fields"] if f not in spec.slots]

    @staticmethod
    def _confirmed(env: dict, st: dict, mistake=None) -> bool:
        if not st["conv"] or mistake == "ignore_confirmation":
            return False
        same = (env["CONF_ACTION"], env["CONF_TARGET"]) == (env["ACTION"], env["TARGET"])
        if mistake == "any_confirmation":
            return env["CONF"] == CONF_EXPLICIT
        if mistake == "mention_as_confirmation":
            return same
        return env["CONF"] == CONF_EXPLICIT and same

    def _judge(self, spec: Spec, mistake=None) -> tuple:
        """(verdict, deciding rule id) by Kleene logic over the rule AST, with one named mistake (None: the card)."""
        env, st = spec.env(), spec.structure
        if mistake == "judge_by_name":
            return ("refuse" if ACTION_TONE.get(env["ACTION"]) == "alarming" else "go"), None
        if mistake == "missing_always_abstains":
            return ("cannot", None) if self._missing(spec) else self._judge(spec)
        nodes = self._rule_nodes(spec, mistake)
        truth = {}
        for rid, _, node in nodes:
            t = RL.evaluate3(node, env)
            if t is None and mistake in ("missing_as_false", "missing_as_true"):
                t = mistake == "missing_as_true"
            truth[rid] = t
        confirmed = self._confirmed(env, st, mistake)
        if mistake == "first_match":
            for rid, tier, _ in nodes:
                if truth[rid]:
                    return ("refuse" if tier == "forbid" else "go" if confirmed else "ask"), rid
            return "go", None
        tiers = ("confirm", "forbid") if mistake == "confirm_over_forbid" else ("forbid", "confirm")
        for tier in tiers:
            if tier == "forbid" and mistake == "confirm_lifts_forbid" and confirmed:
                continue
            if tier == "confirm" and confirmed:
                continue
            app = [rid for rid, t, _ in nodes if t == tier and truth[rid] is True]
            if app:
                return RL_EFFECT[tier], app[0]
            if any(truth[rid] is None for rid, t, _ in nodes if t == tier):
                return "cannot", None
        return "go", None

    def _solve(self, spec: Spec) -> tuple:
        if self._missing(spec):
            return self._judge(spec)                       # Kleene (rules.evaluate3): exact here, G0 S28
        env = spec.env()
        rs = RL.RuleSet(tuple(RL.Rule(rid, RL_EFFECT[tier], node) for rid, tier, node in self._rule_nodes(spec)),
                        "effect_order", "go", ("refuse", "ask"))
        d = RL.resolve(rs, env)
        if d.effect == "ask" and self._confirmed(env, spec.structure):
            return "go", None
        if spec.qform == "ch_rule" and d.effect != "go" and len(d.tied) > 1:
            raise ContractError("two rules of the deciding tier apply: no single rule decides")
        return d.effect, d.rule_id

    def solve_a(self, spec: Spec):
        verdict, rid = self._solve(spec)
        return _answer(spec.qform, verdict, rid)

    # ------------------------------------------------------------------------------------------- canonical facts (G3)
    def canonical(self, spec: Spec) -> dict:
        st, a, env = spec.structure, spec.all_slots(), spec.env()

        def c(k):
            return S.canonical(a[k]) if k in a else None

        rules = []
        for i, r in enumerate(st["rules"], 1):
            atoms = []
            for t in r["atoms"]:
                if t in THRESHOLD_ATOMS:
                    th, cm = _th_names(t, r["tier"])
                    atoms.append({"type": t, "cmp": env[cm], "value": c(th)})
                elif t == "off_hours":
                    atoms.append({"type": t, "start": st["hours"][0], "end": st["hours"][1],
                                  "end_incl": st["hours"][2]})
                else:
                    atoms.append({"type": t})
            rules.append({"rid": f"R{i}", "tier": r["tier"], "atoms": atoms})
        printed = {}
        if "NOW_LOCAL" in spec.derived:
            printed["request_time_local"] = c("NOW_LOCAL")
        if "LAST_EDIT" in st["fields"]:
            printed["minutes_since_edit"] = c("ELAPSED")
        conv = None
        if st["conv"]:
            conv = {"sem": env["CONF"], "action": c("CONF_ACTION"), "target": c("CONF_TARGET")}
        return {"qform": spec.qform, "action": c("ACTION"), "target": c("TARGET"), "effect": c("EFFECT"),
                "undo_h": c("UNDO_H"), "agent_team": c("AGENT_TEAM"), "org_domain": c("ORG_DOMAIN"),
                "offset": _off_str(st["offset"]) if self._reads(spec, "off_hours") else None,
                "precedence": env["PREC"], "rules": rules,
                "snapshot": {FIELD_KEY[f]: c(f) for f in st["fields"]}, "printed": printed, "conv": conv,
                "codes": dict(self._code_pairs(spec)) if st["codes"] else None,
                "requester": c("REQUESTER"), "reason": c("REASON")}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("requester", "reason")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"requester": c["requester"], "reason": c["reason"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("requester", "name", "the person who made the request, as written"),
                Field("reason", "category", "the work the request is part of", spec.slots["REASON"].params)]

    # ------------------------------------------------------------------------------------------- render
    def _pick_skin(self, ctx, spec, key, held):
        reg = self._register_for(spec, key)
        if reg is not None:
            try:
                return ctx.pick(FAMILY, "skin", key, register=reg, held_out=held)
            except LookupError:
                pass
        return ctx.pick(FAMILY, "skin", key, held_out=held)

    def _pick_wording(self, ctx, spec, key, held):
        if held:
            try:
                return ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=True)
            except LookupError:
                pass
        return ctx.pick(FAMILY, "wording", key, qform=spec.qform)

    def _snapshot(self, spec: Spec, slots: dict, forms: dict) -> list:
        st = spec.structure
        off = _off_str(st["offset"])
        rows = []                                   # (label, json key, slot name or None for missing)
        for f in st["fields"]:
            rows.append((FIELD_LABEL[f], FIELD_KEY[f], f if f in slots else None))
            if f == "NOW" and "NOW_LOCAL" in slots:
                rows.append((f"request time at UTC{off}", "request_time_local", "NOW_LOCAL"))
            if f == "LAST_EDIT":
                rows.append(("minutes since that edit", "minutes_since_edit", "ELAPSED" if "ELAPSED" in slots
                             else None))
        fmt = st["snap_fmt"]
        if fmt == "json":
            body = ", ".join(f'"{k}": ' + ("{%s}" % s if s else "null") for _, k, s in rows)
            return ["State snapshot (JSON):\n", K.fill("{" + body + "}", slots, forms, escape="json")]
        head = {"kv": "State snapshot:", "table": "State snapshot:\n| field | value |\n|---|---|",
                "console": "admin-console> show snapshot"}[fmt]
        line = {"kv": "- %s: %s", "table": "| %s | %s |", "console": "%s = %s"}[fmt]
        out = [head]
        for label, _, s in rows:
            out.append("\n")
            out.append(K.fill(line % (label, "{%s}" % s), slots, forms) if s else line % (label, "(missing)"))
        return out

    def _offers_cannot(self, spec: Spec) -> bool:
        """CANNOT DECIDE is an option: shown by the label-blind draw, or the gold itself (a premise-removal twin; the
        option set always holds the gold, distractors.build_closed)."""
        if spec.qform != "ch_verdict":
            return False
        return bool(spec.structure["show_abstain"]) or (bool(self._missing(spec)) and self._solve(spec)[0] == "cannot")

    def _code_pairs(self, spec: Spec) -> list:
        """G0 S12 / B23: the answer-code legend lists exactly the verdicts offered as options."""
        codes = spec.structure["codes"]
        if not codes:
            return []
        keep = VERD3 + (("cannot",) if self._offers_cannot(spec) else ())
        return [(c, k) for c, k in zip(codes, VERDICT4) if k in keep]

    def _shows_missing_line(self, spec: Spec) -> bool:
        """G0 S13 / B23: the missing-data line is printed iff a field is (missing) or CANNOT DECIDE is offered."""
        return bool(self._missing(spec)) or self._offers_cannot(spec)

    def _card(self, tb: TextBuilder, spec: Spec, slots: dict, forms: dict) -> str:
        """Print the policy card; returns the row field it went to. G0 v1.2 S13 (pilot FIX-2, c2_kit.cards): the served
        prompt prints row.instructions twice and row.card once (yes/no rows only), so a yes/no row carries the policy in
        row.card (the "Definitions:" block, counted once) and its instructions are the question alone; a choice row
        keeps the policy in the instructions, the only place it prints. Same words, same order."""
        st = spec.structure
        fld = "card" if self.QFORMS[spec.qform].qtype == "noul" else "instructions"

        def add(piece, nl=True):
            tb.add(fld, piece)
            if nl:
                tb.add(fld, "\n")

        clock = CLOCK_TPL % _off_str(st["offset"]) if self._reads(spec, "off_hours") else ""
        add(K.fill(HEADER_TPL % clock, slots, forms))
        missing_line = self._shows_missing_line(spec)
        add(VERDICT_LINE + (VERDICT_CANNOT if missing_line else "") + ".")
        add("Rules:")
        if st["rule_fmt"] == "table":
            add("| rule | tier | applies when |")
            add("|---|---|---|")
        for i, r in enumerate(st["rules"], 1):
            conds = []
            for a in r["atoms"]:
                if a in THRESHOLD_ATOMS:
                    conds.append(ATOM_TPL[a] % _th_names(a, r["tier"])[1])
                elif a == "off_hours":
                    s, e, incl = st["hours"]
                    end = f"after {_hhmm(e)}" if incl else f"at {_hhmm(e)} or later"
                    conds.append(f"the request time at UTC{_off_str(st['offset'])} is before {_hhmm(s)} or {end}")
                else:
                    conds.append(ATOM_TPL[a])
            cond = " and ".join(conds)
            text = (f"| R{i} | {TIER_TEXT[r['tier']]} | {cond} |" if st["rule_fmt"] == "table"
                    else f"R{i} ({TIER_TEXT[r['tier']]}): {cond}.")
            add(K.fill(text, slots, forms))
        add(K.fill("Precedence: {PREC}", slots, forms))
        if st["conv"]:
            add(CONFIRM_LINE)
        if missing_line:
            add(MISSING_LINE)
        if st["codes"]:
            add("Answer codes: " + ", ".join(f"{c} = {VERDICT_NAME[k]}" for c, k in self._code_pairs(spec)) + ".")
        add(CLOSED_WORLD, nl=False)
        text = tb.text(fld) or ""
        if fld == "card" and any(ln.startswith(("- Yes: ", "- No: ")) for ln in text.split("\n")):
            raise K.RenderError("a yes/no card line '- Yes: ' / '- No: ' is glued to the option by decoder_io")
        return fld

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        st = spec.structure
        skin = skin or self._pick_skin(ctx, spec, key, held)
        wording = wording or self._pick_wording(ctx, spec, key, held)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        narrative = skin.fill(slots, forms)
        if "\n\n" in narrative.text or narrative.text != narrative.text.strip():
            raise K.RenderError(f"skin {skin.skin_id}: a narrative is one block (no blank line, no outer space)")
        call = CALL_TPL % (UNDO_TPL if "UNDO_H" in slots else "")
        blocks = {"narrative": [narrative], "call": [K.fill(call, slots, forms)],
                  "snapshot": self._snapshot(spec, slots, forms)}
        if st["conv"]:
            blocks["conv"] = [K.fill(CONV_TPL, slots, forms)]
        tb = TextBuilder()
        for n, name in enumerate(b for b in ORDERS[st["order"]] if b in blocks):
            if n:
                tb.add("state", "\n\n")
            for piece in blocks[name]:
                tb.add("state", piece, skin_id=skin.skin_id if name == "narrative" else None)
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        fld = self._card(tb, spec, slots, forms)
        if fld == "instructions":
            tb.add("instructions", "\n\n")
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_verdict":
            codes = st["codes"]
            text = (lambda k: codes[VERDICT4.index(k)]) if codes else VERDICT_TEXT.__getitem__
            os_ = build_closed(spec, ans, list(VERD3), self.error_models(), row_key=key, render_key=text,
                               abstain=("cannot", text("cannot")), show_abstain=st["show_abstain"])
        elif spec.qform == "ch_rule":
            rids = [f"R{i}" for i in range(1, len(st["rules"]) + 1)] + ["none"]
            os_ = build_closed(spec, ans, rids, self.error_models(), row_key=key,
                               render_key=lambda k: NONE_TEXT if k == "none" else f"Rule {k}")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CARDS.defs_style(fld, "full"))

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = spec.qform
        p = self._premise(spec) if q == "ch_verdict" and uhash(FAMILY, "premise", spec.sampler, spec.seed) < PREMISE_RATE \
            else None
        t = None
        if p is None and uhash(FAMILY, "twin", spec.sampler, spec.seed) < TWIN_RATE:
            t = self._twin(spec)
        # G0 v1.2 S26 (pilot FIX-4): a yes/no unit holds a twin OR a complement partner, never both and never neither.
        # Both partners carry the opposite answer of the base, so each unit's yes - no is (base sign) x (1 - 1 + equiv),
        # and the yes rate of the family no longer rides on which bases happen to get which partner (the Stage B pilot's
        # 47.2%). Complements are still >= 20% of the yes/no rows and a third or more of the pairs are non-syntactic.
        if q in COMPLEMENTS and t is None:
            out.append(RelationProposal("complement", qform=self._complement_partner(spec)))
        u = _qmc(spec.sampler, spec.seed, 4)
        if u < 0.14:
            out.append(RelationProposal("equiv", register=self._equiv_register(spec)))
        elif u < 0.23:
            out.append(RelationProposal("inv"))
        if p is not None:
            out.append(p)
        elif t is not None:
            out.append(t)
        return out + self._metamorphic(spec)

    @staticmethod
    def _complement_partner(spec: Spec) -> str:
        """The complement question form: syntactic 0.80 / non-syntactic 0.20 (G0 v1.2 S22), a label-blind draw."""
        u, acc = uhash(FAMILY, "ckind", spec.sampler, spec.seed), 0.0
        parts = COMPLEMENT_W[spec.qform]
        for qf, w in parts:
            acc += w
            if u < acc:
                return qf
        return parts[-1][0]

    def _register_for(self, spec: Spec, key: str) -> str:
        """The register of the narrative skin: weighted by sampler (REGISTER_W), from the row key only."""
        regs = REGISTER_W.get(spec.sampler)
        if regs is None:
            return None
        u, acc = uhash(key, "register"), 0.0
        for r, w in regs:
            acc += w
            if u < acc:
                return r
        return regs[-1][0]

    def _equiv_register(self, spec: Spec):
        """The equiv partner's register: another one of the sampler's weights than the base row's (G0 v1.2 S23)."""
        regs = REGISTER_W.get(spec.sampler)
        if regs is None:
            return None
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        base = self._register_for(spec, key)
        rest = [(r, w) for r, w in regs if r != base]
        tot, u, acc = sum(w for _, w in rest), uhash(key, "equiv_register"), 0.0
        for r, w in rest:
            acc += w / tot
            if u < acc:
                return r
        return rest[-1][0]

    def _flip(self, spec: Spec, atom: str, tier: str, new: bool):
        """(slot name, new slot) that moves one field across `atom`'s boundary so the atom reads `new`."""
        v, st = spec.env(), spec.structure
        if atom in THRESHOLD_ATOMS:
            th, cm = _th_names(atom, tier)
            sem, t = v[cm], v[th]
            lo, hi = _interval(sem, t, new)
            x = lo if lo is not None else hi                 # the value next to the threshold
            if atom == "recent":
                if x < 0:
                    return None
                return "LAST_EDIT", S.datetime_slot(v["NOW"] - dt.timedelta(minutes=x))
            if atom == "bulk" and x < 1 or x < 0:
                return None
            if atom == "pay":
                return "AMOUNT", S.cents_slot(x)
            return ATOM_FIELD[atom], S.count_slot(x, U_RECORD if atom == "bulk" else U_HOUR)
        pack = self.pack_by_id[spec.pack]
        if atom == "external":
            other = pack["lookalike"][0] if uhash(FAMILY, "dom", spec.sampler, spec.seed) < 0.5 else pack["partners"][0]
            dom = other if new else v["ORG_DOMAIN"]
            return "DEST_DOMAIN", S.id_slot(dom)
        if atom == "other_team":
            team = sorted(k for k in TEAMS if k != v["AGENT_TEAM"])[spec.seed % 5] if new else v["AGENT_TEAM"]
            return "OWNER_TEAM", S.category_slot(team, TEAMS)
        if atom in ("prod", "pii"):
            f, key = CATEGORY_ATOMS[atom]
            pool = ENVS if atom == "prod" else CLASSES
            val = key if new else sorted(k for k in pool if k != key)[spec.seed % (len(pool) - 1)]
            return f, S.category_slot(val, pool)
        if atom == "off_hours":
            s, e, incl = st["hours"]
            far = e + 1 if incl else e
            tod = (far if spec.seed % 2 else s - 1) if new else (s if spec.seed % 2 else far - 1)
            local = v.get("NOW_LOCAL") or v["NOW"]
            moved = local.replace(hour=tod // 60, minute=tod % 60)
            now2 = moved.astimezone(v["NOW"].tzinfo)
            if "LAST_EDIT" in v and v["LAST_EDIT"] is not None and now2 < v["LAST_EDIT"]:
                return None
            return "NOW", S.datetime_slot(now2)
        return None

    def _twin(self, spec: Spec):
        """One input slot moved across one atom's boundary; the new verdict is predicted from the base truths."""
        st, v = spec.structure, spec.env()
        rt, conf = self._rule_truths(spec), self._confirmed_c(spec)
        verdict = self._verdict_c(rt, conf)
        if verdict == "cannot":
            return None
        readers: dict = {}
        for r in st["rules"]:
            for a in r["atoms"]:
                readers[ATOM_FIELD[a]] = readers.get(ATOM_FIELD[a], 0) + 1
        if "recent" in {a for r in st["rules"] for a in r["atoms"]}:
            readers["NOW"] = readers.get("NOW", 0) + 1         # NOW also moves the printed minutes
        cands = []
        for i, r in enumerate(st["rules"]):
            for j, a in enumerate(r["atoms"]):
                f = ATOM_FIELD[a]
                if f == "EFFECT" or readers.get(f) != 1 or f not in spec.slots:
                    continue
                if (f == "AMOUNT" and v["EFFECT"] != "pay") or (f == "DEST_DOMAIN" and v["EFFECT"] not in OUTBOUND):
                    continue
                cur = rt[i][1][j]
                new_rt = [(t, list(ts)) for t, ts in rt]
                new_rt[i][1][j] = not cur
                new_v = self._verdict_c(new_rt, conf)
                if new_v in (verdict, "cannot"):
                    continue
                flip = self._flip(spec, a, r["tier"], not cur)
                if flip is None:
                    continue
                cands.append((flip, new_v, new_rt, conf))
        if st["conv"] and v["CONF"] == CONF_EXPLICIT:
            same_act, same_tgt = v["CONF_ACTION"] == v["ACTION"], v["CONF_TARGET"] == v["TARGET"]
            if conf:
                other = sorted(a for a, _, _ in ACTIONS if a != v["ACTION"])[spec.seed % (len(ACTIONS) - 1)]
                flip, new_conf = ("CONF_ACTION", S.id_slot(other)), False
            elif same_act != same_tgt:
                flip = ("CONF_TARGET", S.id_slot(v["TARGET"])) if same_act else ("CONF_ACTION", S.id_slot(v["ACTION"]))
                new_conf = True
            else:
                flip = None
            if flip is not None:
                new_v = self._verdict_c(rt, new_conf)
                if new_v not in (verdict, "cannot"):
                    cands.append((flip, new_v, rt, new_conf))
        base_top = self._applying_top(spec, rt, verdict, conf)
        base = _answer(spec.qform, verdict, base_top[0] if base_top else None)
        keep = []
        for flip, new_v, new_rt, new_conf in cands:          # the question's answer must flip, not only the verdict
            if spec.qform == "ch_rule":
                top = self._applying_top(spec, new_rt, new_v, new_conf)
                if top is None or len(top) > 1:
                    continue
                expect = top[0] if top else "none"
            else:
                expect = _answer(spec.qform, new_v)
            if expect != base and (spec.qform != "ch_rule" or abstain_twin_kept(
                    f"{FAMILY}|{spec.sampler}|{spec.seed}", base, expect, "none", TWIN_NONE_KEEP)):
                keep.append((flip, new_v, expect))
        if not keep:
            return None
        (slot, new_slot), new_v, expect = keep[int(uhash(FAMILY, "twinpick", spec.sampler, spec.seed) * len(keep))]
        kept = TWIN_KEEP.get(spec.qform, {}).get(expect, 1.0)          # G0 v1.2 S26: thin the over-represented direction
        if spec.qform == "ch_verdict" and spec.structure["show_abstain"]:
            kept = TWIN_KEEP_SHOWN.get(expect, 1.0)
        if kept < 1.0 and uhash(FAMILY, "twinkeep", spec.sampler, spec.seed) >= kept:
            return None
        return RelationProposal("twin", spec=self._retag(spec.with_slot(slot, new_slot)), changed_slot=slot,
                                expect=expect, note=f"{slot} across one boundary: {verdict} -> {new_v}")

    def _retag(self, spec: Spec) -> Spec:
        """A twin or premise-removal partner carries ITS OWN trap tags, depth and deep flag (pilot FIX-8a: Spec.with_slot
        keeps the base row's, which stamped a gold-cannot row 'alarming_reversible_go' and mis-sized the deep share)."""
        spec = self.derive(spec)
        tags, steps = self._tags(spec)
        return spec.replace(tags=tuple(tags), depth=steps, deep=steps >= 3)

    def _premise(self, spec: Spec):
        """A field of the deciding (or near-firing) rule removed so the verdict cannot be decided (G0 S26)."""
        st, v = spec.structure, spec.env()
        if self._missing(spec):
            return None
        cands = []
        for f in st["fields"]:
            if f not in MISSABLE or (f == "AMOUNT" and v["EFFECT"] != "pay") or (
                    f == "DEST_DOMAIN" and v["EFFECT"] not in OUTBOUND):
                continue
            s2 = self.derive(spec.with_slot(f, None))
            if self._verdict_c(self._rule_truths(s2), self._confirmed_c(s2)) == "cannot":
                cands.append(f)
        if not cands:
            return None
        f = cands[int(uhash(FAMILY, "premisepick", spec.sampler, spec.seed) * len(cands))]
        return RelationProposal("premise_removal", spec=self._retag(spec.with_slot(f, None)), changed_slot=f,
                                expect="cannot", note=f"{f} removed")

    def _metamorphic(self, spec: Spec) -> list:
        v, st = spec.env(), spec.structure
        out = []
        pack = self.pack_by_id[spec.pack]
        n = int(v["TARGET"].split("-")[1])
        new_t = f"{pack['prefix']}-{(n - 10000 + 4321) % 90000 + 10000}"
        s1 = spec.with_slot("TARGET", S.id_slot(new_t))
        if st["conv"] and v["CONF_TARGET"] == v["TARGET"]:
            s1 = s1.with_slot("CONF_TARGET", S.id_slot(new_t))
        out.append(RelationProposal("metamorphic", spec=s1, expect="same", note="rename the target"))
        org = next(p["org"] for p in self.packs if p["org"] not in (v["ORG_DOMAIN"], v.get("DEST_DOMAIN")))
        s2 = spec.with_slot("ORG_DOMAIN", S.id_slot(org))
        if v.get("DEST_DOMAIN") == v["ORG_DOMAIN"]:
            s2 = s2.with_slot("DEST_DOMAIN", S.id_slot(org))
        out.append(RelationProposal("metamorphic", spec=s2, expect="same", note="rename the organisation domain"))
        day = dt.timedelta(days=1)
        moved = {k: S.datetime_slot(v[k] + day) for k in ("NOW", "LAST_EDIT") if k in spec.slots}
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **moved}), expect="same",
                                    note="shift every time by one day"))
        n_rules = len(st["rules"])
        rev = spec.replace(structure={**st, "rules": list(reversed(st["rules"]))})
        expect = "same"
        if spec.qform == "ch_rule":
            rid = self._decider(spec)
            expect = f"R{n_rules + 1 - int(rid[1:])}" if rid else "none"
        out.append(RelationProposal("metamorphic", spec=rev, expect=expect, note="reverse the rule order"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def make(name):
            def fn(spec):
                if spec.qform not in ("ch_verdict", "ch_rule"):
                    return None
                verdict, rid = self._judge(spec, name.removeprefix("t29_"))
                if spec.qform == "ch_rule":
                    return None if verdict == "cannot" else (rid or "none")
                return verdict
            return fn

        return {name: error_model(name, make(name)) for name in ERROR_NAMES}
