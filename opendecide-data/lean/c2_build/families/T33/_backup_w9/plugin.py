"""families/T33/plugin.py: T33, outcome verification against tool logs (C2_DATA_SPEC 3.3; G0_SPEC.md, frozen below).

Two checks on an agent's trace, built on one shared simulator:
  (a) step success: a stated criterion (1-3 checks from a closed set) over one numbered step of a tool log with HTTP
      statuses, retries with idempotency keys, async jobs (202, then polls) and partial writes;
  (b) claims vs log: the agent's final message holds 2-4 claim clauses (lexicon forms with target and value slots);
      0-2 of them are made wrong by the program (status flip, x100 unit scale, value swap, wrong target, no call).

  construction  PATTERNS (the simulator's ground truth: every pattern's designed outcome) builds each step; claims get
                designed verdicts. Both are kept in spec.structure["intent"]: sample() asserts solver A agrees, and
                relations() predicts twin answers from them (never from solver A)
  solver A      replays the log lines in order through a per-step state machine, then applies the criterion checks
                or the claim matcher (paradigm simulator); every error model is solver A with one rule swapped
  solver B      solver_b.py: re-parses the RENDERED log into sqlite and decides by SQL with its own unit table and
                claim-to-step join (paradigm sql_sqlite)
  samplers      S1 forward episode (natural failure injection, accepted on a label-blind target draw); S2 label-first
                (one decisive defect at a near-miss value); S3 table-first (CSV / markdown, 2-4 steps); S4 ticket or
                PR summary (message first); S5 held out (held-out skins and registers; mixdev only)
  questions     (a) yn_step_ok / yn_step_failed (antonym) / yn_step_fail_to (implicit) / yn_step_not_ok (syntactic) /
                yn_dneg_step_ok (double negation), ch_failed_check (listed checks + None); (b) yn_all_supported /
                yn_any_bad (option framing) / yn_not_all_supported (syntactic) / yn_dneg_all_supported (double
                negation), ch_bad_claim (claim targets + None), ch_claim_verdict (3 verdicts). The double-negation
                forms are drawn only while an admitted wording passes the polarity rule (else the positive form)
  relations     complement on 30% of yes/no rows (the other polarity); minimal-edit twins (one log value, claim value,
                claim target or criterion bound), thinned by form and twin gold so the twin golds are balanced
                (TWIN_KEEP); equiv (sub-form a: other log container + a skin of another register); inv (one attack
                line); G4 metamorphic: rename the user, rename a tool, change an idempotency key
  card          cardtext.py: the rules block, need-to-know, styles full / short; yes/no rows carry it in row.card,
                choice rows at the head of the instructions (cards.place_rules; solver B reads cards.split_rules)
  balance       R_MAX (1 or 2) is drawn before the episode; ch_failed_check / ch_bad_claim draw their display plan
                (c2_kit.choiceplan, None is gold on 1 / k) before the structure; register first, then the least-loaded
                skin; one wording per antithetic pair (_BalancedCtx); the question form of a pair comes from a
                golden-ratio sequence (stateful picks: one sequential run, reset_balance() starts another)
Mode F (free-form) skins are not rendered in this version (G0 section 5).
"""
from __future__ import annotations

import math
import random
import re
from pathlib import Path

from c2_kit import cards as CD
from c2_kit import polarity as POL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import plan_choice
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.lexicon import question_sem
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.relations import abstain_twin_kept
from c2_kit.rows import TextBuilder, assemble_row

from . import cardtext as CT

HERE = Path(__file__).resolve().parent
FAMILY = "T33"

# ------------------------------------------------------------------------------------------------ simulator vocabulary
# Built-in packs (G0 S1): 6 tool namespaces x 5 invented tools = 30 mock APIs. Each tool: (name, verb, target kind).
PACKS = {
    "shopfront": (("shop.issue_refund", "refund", "order"), ("shop.charge_card", "charge", "account"),
                  ("inventory.import_stock", "import", "dataset"), ("mail.send_receipt", "send", "contact"),
                  ("orders.cancel_order", "cancel", "order")),
    "ledgerline": (("ledger.post_credit", "credit", "account"), ("payouts.send_payout", "payout", "vendor"),
                   ("warehouse.export_table", "export", "dataset"), ("crm.update_contact", "update", "contact"),
                   ("notify.send_notice", "send", "contact")),
    "tripdesk": (("travel.charge_fare", "charge", "booking"), ("travel.refund_fare", "refund", "booking"),
                 ("travel.book_seat", "book", "booking"), ("travel.cancel_booking", "cancel", "booking"),
                 ("reports.export_trips", "export", "dataset")),
    "clinicbook": (("clinic.book_visit", "book", "booking"), ("clinic.cancel_visit", "cancel", "booking"),
                   ("billing.charge_copay", "charge", "account"), ("records.sync_charts", "sync", "dataset"),
                   ("sms.send_reminder", "send", "contact")),
    "datapipe": (("etl.import_rows", "import", "dataset"), ("etl.sync_mirror", "sync", "dataset"),
                 ("etl.export_rows", "export", "dataset"), ("billing.credit_usage", "credit", "account"),
                 ("alerts.send_page", "send", "contact")),
    "payroll_hub": (("payroll.send_payout", "payout", "vendor"), ("payroll.import_hours", "import", "dataset"),
                    ("hr.update_record", "update", "record"), ("benefits.refund_premium", "refund", "account"),
                    ("mail.send_payslip", "send", "contact")),
}
VERB_ARCH = {"refund": "money", "charge": "money", "credit": "money", "payout": "money", "import": "bulk",
             "export": "bulk", "sync": "bulk", "send": "action", "book": "action", "cancel": "action",
             "update": "action"}
VALUE_ARCH = ("money", "bulk")
REQ_KEY = {"money": "amount_cents", "bulk": "rows_requested"}        # JSON / text logs: the request field
RES_KEY = {"money": "amount_cents", "bulk": "rows_written"}          # JSON / text logs: the result field
TABLE_FIELD = {"money": "amount_cents", "bulk": "rows"}             # table logs: the field column
VALUE_FORM = {"money": "int_cents", "bulk": "plain"}
STATES = {"queued": ["queued"], "running": ["running"], "succeeded": ["succeeded"], "failed": ["failed"]}
OK_CODES = {"money": (200, 201), "action": (200, 201, 204)}
TRANSIENT = (429, 500, 502, 503, 504)
HARD = {"money": (400, 402, 404, 422), "action": (400, 403, 404, 422)}
# pattern: (archetypes, async, designed done, draw weight). G0 S3: the simulator's ground truth.
PATTERNS = {
    "sync_ok": (("money", "action"), False, True, 0.55),          # [2xx]
    "sync_retry_ok": (("money", "action"), False, True, 0.15),    # [5xx/429, 2xx]
    "sync_three_ok": (("money", "action"), False, True, 0.05),    # [5xx/429, 5xx/429, 2xx]
    "sync_retry_409": (("action",), False, True, 0.17),           # [500/502/504, 409 same key]
    "sync_fail": (("money", "action"), False, False, 0.60),       # [4xx/5xx]
    "sync_retry_fail": (("money", "action"), False, False, 0.40),  # [5xx/429, 4xx/5xx (never 409)]
    "async_ok": (("money", "bulk"), True, True, 0.78),             # [202] polls [running?, succeeded]
    "async_retry_ok": (("money", "bulk"), True, True, 0.22),       # [5xx/429, 202] polls [running?, succeeded]
    "async_nopoll": (("money", "bulk"), True, False, 0.30),        # [202] never polled
    "async_running": (("money", "bulk"), True, False, 0.35),       # [202] polls [queued|running, running?]
    "async_failed": (("money", "bulk"), True, False, 0.35),        # [202] polls [running?, failed]
}
# transient answers before a step's final try (the pattern's own retries); need-driven episodes may override it to meet
# a max_tries need (G0 S3 as amended in section 8: R_MAX is drawn first, then the tries are built to the need)
PATTERN_PRE = {"sync_ok": 0, "sync_retry_ok": 1, "sync_three_ok": 2, "sync_retry_409": 1, "sync_fail": 0,
               "sync_retry_fail": 1, "async_ok": 0, "async_retry_ok": 1, "async_nopoll": 0, "async_running": 0,
               "async_failed": 0}
R_MAX_CHOICES = (1, 2)        # label-blind, drawn from the seed before any episode (pilot F2: the bound predicted the gold)
INTERIM_POLL_P = 0.10         # an optional extra "running" poll before a job's last poll (G0 S3; was .3, length F5)
INTERIM_POLL_P_S4 = 0.0       # sampler S4 prints no interim poll (G0 section 10, spec 3.0 length lever 2)
ASYNC_MONEY_P = 0.6
# ch_failed_check twins that move the gold onto one of these checks are kept at these rates (note in _twin)
TWIN_CHECK_KEEP = {"crit.finished": 0.30, "crit.amount_match": 0.60, "crit.all_written": 0.60, "none": 0.80}
P_LATER_FAIL = 0.50           # ch_failed_check plans: each check after the first failing one fails with this rate
P_EQUIV = 0.22                # sub-form (a) bases that get an equiv format twin (spec 4.1: 5-10% of rows)
P_TWIN, P_TWIN_FCC = 1.00, 0.25   # twin proposals; fewer on ch_failed_check, whose twins cannot move a bound check
# minimal-edit twins are kept with this probability given the form and the twin's gold (pilot F3): a twin exists far more
# often in one direction (breaking a claim is always possible, fixing one only when exactly one claim is bad), so the
# kept twin golds are balanced per form (yes/no 50/50, ch_claim_verdict 1/3 each). Rates measured over >= 5,000 specs.
TWIN_KEEP: dict = {
    ("yn_step_ok", 0): 0.74, ("yn_dneg_step_ok", 0): 0.74, ("yn_step_failed", 1): 0.80, ("yn_step_fail_to", 1): 0.76,
    ("yn_step_not_ok", 1): 0.72, ("yn_all_supported", 0): 0.34, ("yn_dneg_all_supported", 0): 0.34,
    ("yn_any_bad", 1): 0.38, ("yn_not_all_supported", 1): 0.31,
    ("ch_claim_verdict", "not_shown"): 0.38, ("ch_claim_verdict", "contradicted"): 0.64,
    ("ch_bad_claim", "item", 3): 0.41, ("ch_bad_claim", "item", 4): 0.38, ("ch_bad_claim", "item", 5): 0.33,
}
NAMES = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt", "Jonah Pell",
         "Priya Natesan", "Kofi Mensah", "Elsa Lindqvist", "Marco Ibarra", "Hana Sato")
DATASET_WORDS = ("orders", "invoices", "contacts", "events", "stock", "payroll", "visits", "trips", "hours", "ledger")
LETTERS = "ABCDEFGHJKMPRSTUVWXYZ"
TARGET_MAKERS = {
    "order": lambda r: f"ORD-{r.randrange(10000, 99999)}",
    "account": lambda r: f"acct-{r.randrange(1000, 9999)}",
    "vendor": lambda r: f"VND-{r.randrange(100, 999)}{r.choice(LETTERS)}",
    "dataset": lambda r: f"ds_{r.choice(DATASET_WORDS)}_{r.randrange(10, 99)}",
    "contact": lambda r: f"cust-{r.randrange(10000, 99999)}",
    "booking": lambda r: f"BK-{r.randrange(1000, 9999)}{r.choice(LETTERS)}",
    "record": lambda r: f"rec-{r.randrange(100000, 999999)}",
}
PACKS_PER_STREAM = 10        # G0 S1: one pack per card; a (sampler, sub-form) stream uses 10 packs (cards ~30-45 rows)
FORMATS = ("jsonl", "text", "csv", "md")
SAMPLER_FORMATS = {"S1": ("text", "jsonl", "text"), "S2": FORMATS, "S3": ("csv", "md"), "S4": ("jsonl", "text"),
                   "S5": ("text", "jsonl")}
STEP_CHOICES = (2, 3, 3, 4)                      # steps per episode outside sampler S3 (S3: 2-4)
TAIL_CAP_P = 1.00                                # of the 4-step draws (seed-drawn, section 11) 4 becomes 3; 4 steps only when 4 claims
MAX_LINES = 12                                   # log lines (+ 1-2 table header lines): <= 20 (spec 3.3)

# ------------------------------------------------------------------------------------------------ card text (G0 S7-S9)
LOG_HEAD = "Tool log:"
REQ_HEAD = "Request from {USER}:\n"
MSG_HEAD = "Agent's final message to {USER}:\n"
CSV_HEADER = "step,line,tool,target,idempotency_key,field,requested,status,job,state,result,duration_ms"
MD_HEADER = "| " + " | ".join(CSV_HEADER.split(",")) + " |"
MD_RULE = "|" + "---|" * len(CSV_HEADER.split(","))
# the rules block (log rules, criterion or claim rules, tie line, closed-world sentence) is built per row by cardtext.py
# (need-to-know bullets, styles full / short; yes/no rows carry it in row.card, choice rows in the instructions)
CLOSED_WORLD = CT.CLOSED_WORLD
VERDICTS = ("supported", "contradicted", "not_shown")
VERDICT_TEXT = {"supported": "Supported by the log", "contradicted": "Contradicted by the log",
                "not_shown": "Not shown in the log"}
NONE_CHECK = "None: every check holds"
NONE_CLAIM = "None: every claim is supported"
CLAIM_OPTION = "The claim about {}"
CHECK_SEMS = ("crit.finished", "crit.all_written", "crit.amount_match", "crit.max_tries", "crit.max_duration")
VALUE_CHECKS = ("crit.all_written", "crit.amount_match")
CHECK_BIND = {"crit.max_tries": ("R", "R_MAX"), "crit.max_duration": ("D", "D_MAX")}
TRY_UNIT = ("try", "tries")
SECOND_UNIT = ("second", "seconds")

# ------------------------------------------------------------------------------------------------ questions (G0 S10)
QFORM_SHARES = (("yn_step_ok", 0.092), ("yn_step_failed", 0.048), ("yn_step_fail_to", 0.024),
                ("yn_step_not_ok", 0.048), ("yn_dneg_step_ok", 0.015), ("ch_failed_check", 0.237),
                ("yn_all_supported", 0.092), ("yn_any_bad", 0.066), ("yn_not_all_supported", 0.045),
                ("yn_dneg_all_supported", 0.015), ("ch_bad_claim", 0.125), ("ch_claim_verdict", 0.193))
SUB_OF = {"yn_step_ok": "a", "yn_step_failed": "a", "yn_step_fail_to": "a", "yn_step_not_ok": "a",
          "yn_dneg_step_ok": "a", "ch_failed_check": "a", "yn_all_supported": "b", "yn_any_bad": "b",
          "yn_not_all_supported": "b", "yn_dneg_all_supported": "b", "ch_bad_claim": "b", "ch_claim_verdict": "b"}
PARTNERS = {"yn_step_ok": (("yn_step_failed", 0.4), ("yn_step_fail_to", 0.2), ("yn_step_not_ok", 0.4)),
            "yn_step_failed": (("yn_step_ok", 1.0),), "yn_step_fail_to": (("yn_step_ok", 1.0),),
            "yn_step_not_ok": (("yn_step_ok", 0.6), ("yn_dneg_step_ok", 0.4)),
            "yn_dneg_step_ok": (("yn_step_not_ok", 1.0),),
            "yn_all_supported": (("yn_any_bad", 0.6), ("yn_not_all_supported", 0.4)),
            "yn_any_bad": (("yn_all_supported", 1.0),),
            "yn_not_all_supported": (("yn_all_supported", 0.6), ("yn_dneg_all_supported", 0.4)),
            "yn_dneg_all_supported": (("yn_not_all_supported", 1.0),)}
# double-negation forms (positive polarity, two syntactic negations, spec 3.0 >= 2% of yes/no rows): drawn only while an
# admitted question form passes the polarity rule, else the positive form of the same predicate (label-blind fallback)
DNEG_FALLBACK = {"yn_dneg_step_ok": "yn_step_ok", "yn_dneg_all_supported": "yn_all_supported"}
# The negative / antonym predicates of "the step meets its criterion" and "the log backs the claim" (c2_kit.polarity rules
# P1-P3; G5-H lesson of T35): a wording negates a positive predicate syntactically OR uses one of these, never both.
NEGATIVE_PREDICATES = (
    r"fail(?:s|ed|ing|ure)?", r"miss(?:es|ed|ing)?", r"fall(?:s|ing)?\s+short", r"fell\s+short",
    r"come(?:s)?\s+up\s+short", r"break(?:s|ing)?", r"broke(?:n)?", r"violat(?:e|es|ed|ing|ion)",
    r"flunk(?:s|ed|ing)?", r"contradict(?:s|ed|ing|ion)?", r"absent", r"unsupported", r"cut(?:s)?\s+against",
    r"refut(?:e|es|ed|ing)", r"disprove(?:s|d)?",
)
A_REGISTERS = ("task_ticket", "runbook", "chat_request", "email_request", "incident_channel")
B_REGISTERS = ("support_agent", "pr_summary", "ops_bot", "travel_agent", "finance_assistant", "scheduling_bot",
               "ticket_thread")
EQUIV_REGISTERS = ("task_ticket", "runbook", "chat_request", "email_request")
# message voices that suit each pack (a label-blind preference; any fitting skin is used when none of these fits)
PACK_VOICES = {"shopfront": ("support_agent", "finance_assistant"), "ledgerline": ("finance_assistant", "ops_bot"),
               "tripdesk": ("travel_agent", "support_agent"), "clinicbook": ("scheduling_bot", "support_agent"),
               "datapipe": ("ops_bot", "pr_summary"), "payroll_hub": ("finance_assistant", "pr_summary")}

# ------------------------------------------------------------------------------------------------ error models (G0 S12)
FLAWS = {
    "status_word": "",                 # kit CATALOG
    "cents_as_dollars": "",            # kit CATALOG
    "first_try_only": "judges a step by its first try and ignores later retries",
    "conflict_as_failure": "reads a 409 on a same-key retry as a failure",
    "polls_as_tries": "counts job polls as tries",
    "request_as_result": "reads the requested amount or row count as the step's result (misses partial writes)",
    "ms_as_seconds": "compares duration_ms with a limit in seconds without converting",
    "missing_value_passes": "lets a check pass when the log shows no value for it",
    "missing_call_contradicted": "calls a claim whose target is not in the log contradicted",
    "missing_call_supported": "calls a claim whose target is not in the log supported because nothing contradicts it",
    "claim_value_ignored": "checks only that the step finished and ignores the amount or count the claim states",
    "value_on_other_target": "accepts a claimed value that the log shows on another target",
    "last_qualifying": "answers with the last failing check or bad claim instead of the first",
}
for _name, _why in FLAWS.items():
    if _why:
        register_name(_name, _why)


def ph(name: str, form: str | None = None) -> str:
    """A program-template placeholder."""
    return "{" + name + (":" + form if form else "") + "}"


# G0 section 11: the log-line count is drawn from the seed too (per step count, about the pooled distribution of iteration
# i2b), and an episode is kept only if it has that many lines (+-1 per 25 failed attempts), so that no label's episodes
# are bigger or smaller than another's (a failing check used to need retries: about half a line more than a pass).
LINES_PMF = {2: ((3, .35), (4, .40), (5, .25)), 3: ((4, .20), (5, .33), (6, .30), (7, .17)),
             4: ((6, .25), (7, .30), (8, .28), (9, .17))}


def _row_lines(sampler: str, seed: int, n_steps: int) -> int:
    u, acc = uhash(FAMILY, "lines", sampler, seed), 0.0
    pmf = LINES_PMF[n_steps]
    for n, p in pmf:
        acc += p
        if u < acc:
            return n
    return pmf[-1][0]


# G0 section 11: the number of retry lines (try lines beyond one per step) is drawn from the seed as well; a row that lists a
# tries check starts from R_MAX retries (a failing tries check cannot have fewer), so the retries on a card are not a cue
# to which check fails (a failing tries check used to bring about one more retry line than any other gold).
RETRY_EXTRA_PMF = {True: ((0, .7), (1, .3)), False: ((0, .6), (1, .3), (2, .1))}


def _row_retries(sampler: str, seed: int, tries_listed: bool, r_max: int) -> int:
    u, acc = uhash(FAMILY, "retries", sampler, seed), 0.0
    pmf = RETRY_EXTRA_PMF[tries_listed]
    for n, p in pmf:
        acc += p
        if u < acc:
            return n + (r_max if tries_listed else 0)
    return pmf[-1][0] + (r_max if tries_listed else 0)


def _row_steps(sampler: str, seed: int, n_claims: int = 0) -> int:
    """G0 section 11: the episode's step count, drawn from the row seed alone (never from the rng stream or the label), with
    the tail cap (a share of the 4-step draws becomes 3; section 10) applied here. Sub-form (b) needs a step per claim
    (n_claims is itself seed-drawn), so the count is at least n_claims for every label. Fixed before any structure, so
    every label sees the same step-count distribution."""
    u = uhash(FAMILY, "nsteps", sampler, seed)
    n = 2 + min(2, int(u * 3)) if sampler == "S3" else STEP_CHOICES[min(3, int(u * 4))]
    if n == 4 and uhash(FAMILY, "tailcap", sampler, seed) < TAIL_CAP_P:
        n = 3
    return max(n, n_claims)


def _value_slot(arch: str, v: int) -> S.Slot:
    return S.cents_slot(v) if arch == "money" else S.count_slot(v)


def _first_fail(vec: list) -> int | None:
    return next((i for i, ok in enumerate(vec) if not ok), None)


def map_a(qform: str, sems: list, vec: list, last: bool = False):
    """Answer of a sub-form (a) question from the check results (listed order)."""
    ok = all(vec)
    if qform in ("yn_step_ok", "yn_dneg_step_ok"):
        return int(ok)
    if qform in ("yn_step_failed", "yn_step_fail_to", "yn_step_not_ok"):
        return int(not ok)
    fails = [sems[i] for i, v in enumerate(vec) if not v]
    if not fails:
        return "none"
    return fails[-1] if last else fails[0]


def map_b(qform: str, targets: list, verdicts: list, asked: int | None, last: bool = False):
    """Answer of a sub-form (b) question from the claim verdicts (message order)."""
    ok = all(v == "supported" for v in verdicts)
    if qform in ("yn_all_supported", "yn_dneg_all_supported"):
        return int(ok)
    if qform in ("yn_any_bad", "yn_not_all_supported"):
        return int(not ok)
    if qform == "ch_claim_verdict":
        return verdicts[asked - 1]
    bad = [targets[i] for i, v in enumerate(verdicts) if v != "supported"]
    if not bad:
        return "none"
    return bad[-1] if last else bad[0]


class _BalancedCtx(KitCtx):
    """The kit context with a balanced, pair-consistent wording pick (pilot F7, G10 cells). A wording is drawn once per
    antithetic pair of seeds and question form (so both seeds, which carry opposite golds, read the same wording, and a
    complement partner's wording is the same for both seeds too) and is the LEAST-USED wording of that form so far, so
    no wording nears the 2% cap and no wording x negation cell grows past the 50 rows where the +-2 pp bar starts.
    Label-blind: loads count pairs, never golds. Every other pick is the kit's seeded hash draw."""
    plugin = None

    def pick(self, family, kind, row_key, *, register=None, qform=None, exclude=(), held_out=False):
        if kind == "wording" and qform is not None and self.plugin is not None:
            got = self.plugin._pick_wording(self, row_key, qform, held_out, exclude)
            if got is not None:
                return got
        return super().pick(family, kind, row_key, register=register, qform=qform, exclude=exclude,
                            held_out=held_out)


class T33Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "ea73985d7e9aaddc00264a187b3c2b913b6f966bf6afd6c0a07dd9298163859a"   # G0_SPEC.md after amendment i2c (section 11)
    # the Haiku ambiguity pass that preceded this freeze (G0 section 6): workflow c2-data-stage-a, phase Ambiguity
    AMB_PASS = {"task": "amb:T33", "model": "haiku", "n_points": 37,
                "points_file": "haiku/ambiguity/amb_T33_points.json",
                "points_sha256": "b1fdb5cff855c874b4c1212bfb82bc3b209346a467457ce0789b884aae8e01e9",
                "g0_before": "6978a5a13948bb4ed5099b1eb924b13067abab123713e5552a8967e6c554e575"}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    _interim_on = False          # G0 section 11: whether this row's jobs print an interim poll, drawn from the seed in sample()
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "simulator"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T33.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("yn_step_ok", "noul", "step_ok", 1, yes_is_bad=False),
        QuestionForm("yn_step_failed", "noul", "step_ok", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_step_fail_to", "noul", "step_ok", -1, "implicit", yes_is_bad=True),
        QuestionForm("yn_step_not_ok", "noul", "step_ok", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_dneg_step_ok", "noul", "step_ok", 1, yes_is_bad=False),
        QuestionForm("ch_failed_check", "choice", answer_set="closed", abstain=True),
        QuestionForm("yn_all_supported", "noul", "all_supported", 1, yes_is_bad=False),
        QuestionForm("yn_any_bad", "noul", "all_supported", -1, "option_framing", yes_is_bad=True),
        QuestionForm("yn_not_all_supported", "noul", "all_supported", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_dneg_all_supported", "noul", "all_supported", 1, yes_is_bad=False),
        QuestionForm("ch_bad_claim", "choice", answer_set="closed", abstain=True),
        QuestionForm("ch_claim_verdict", "choice", answer_set="closed"),
    )}
    LABEL_WORDS = ("support", "unsupported", "contradict", "not shown", "succeed", "fail")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = A_REGISTERS + B_REGISTERS
    HELD_OUT_REGISTERS = ("incident_channel", "ticket_thread")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("PR",)
    # wording polarity (c2_kit.polarity; STAGE_B lesson of T35): a yes/no wording must read with its form's polarity
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES

    # skin balance (pilot F6): register first, then the least-loaded skin; a skin feeds at most SKIN_CAP rows (spec 3.0)
    SKIN_CAP = 6.0

    def __init__(self, lexicon=None, packs: dict | None = None, voices: dict | None = None):
        """packs: {name: ((tool, verb, target kind), ...)} (default: the 6 built-in packs); voices: {pack: message
        registers that suit it} (a label-blind skin preference; default PACK_VOICES). Every pack needs a money, a bulk
        and an action tool (G0 S1)."""
        super().__init__(lexicon)
        self.packs = dict(packs or PACKS)
        self.voices = dict(PACK_VOICES if voices is None else voices)
        for name, tools in self.packs.items():
            archs = {VERB_ARCH.get(t[1]) for t in tools}
            if not {"money", "bulk", "action"} <= archs or any(t[2] not in TARGET_MAKERS for t in tools):
                raise ContractError(f"pack {name}: needs money, bulk and action tools with known target kinds")
        self.dneg_ok = {q: self._clean_form(q) for q in DNEG_FALLBACK}
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]
        self.reset_balance()

    def reset_balance(self) -> None:
        """Forget the skin loads and picks (a new generation run starts balanced)."""
        self._skin_memo: dict = {}                 # row key -> skin id (a key renders with one skin, whatever is asked)
        self._skin_load: dict = {}                 # skin id -> rows (estimated) it feeds
        self._reg_load: dict = {}                  # (sub-form, register) -> rows (estimated)
        self._reg_of: dict = {}                    # row key -> register of its skin
        self._wording_memo: dict = {}              # (pair, sampler, qform, held out) -> wording id
        self._wording_load: dict = {}              # wording id -> pairs it has served

    # ------------------------------------------------------------------------------------------- polarity (wordings)
    def _clean_form(self, qform: str) -> bool:
        """True when the lexicon holds an admitted question form of `qform` whose wording passes the polarity rule.
        Label-blind: the pool, not a row. Without a lexicon (contract checks) True."""
        if self.lexicon is None:
            return True
        sem = question_sem(FAMILY, qform)
        return any(f.sem_id == sem and self.lexicon.status(f.form_id) == "admitted"
                   and not POL.form_problems(self, qform, f.text) for f in self.lexicon.forms.values())

    def usable_qform(self, qform: str) -> bool:
        """False for a double-negation form that no admitted, polarity-clean wording can ask."""
        return self.dneg_ok.get(qform, True)

    def ctx_for(self, spec: Spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity), so neither render()
        nor the pipeline's complement partner can pick one, and with the balanced wording pick (_BalancedCtx).
        Cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        balanced = _BalancedCtx(skins=screened.skins, lexicon=screened.lexicon)
        balanced.plugin = self
        self._screened.append((ctx, balanced, bad))
        self._screened.append((balanced, balanced, bad))
        return balanced

    def _pick_wording(self, kctx, row_key: str, qform: str, held_out: bool, exclude=()):
        """The least-used wording of a form for the antithetic pair a row key belongs to (None: not a T33 row key, or no
        wording: the kit's draw / LookupError applies)."""
        m = re.match(rf"^{FAMILY}\|(\d+)\|(S\d)\|", row_key)
        if not m:
            return None
        pair, sampler = int(m.group(1)) // 2, m.group(2)
        mk = (pair, sampler, qform, bool(held_out))
        sid = self._wording_memo.get(mk)
        if sid is not None and sid in kctx.skins and sid not in exclude:
            return kctx.skins[sid]
        cands = sorted((x for x in kctx.skins.values() if x.family == FAMILY and x.kind == "wording"
                        and x.qform == qform and x.held_out == bool(held_out) and x.skin_id not in exclude),
                       key=lambda x: x.skin_id)
        if not cands:
            return None
        w = min(cands, key=lambda x: (self._wording_load.get(x.skin_id, 0), uhash(f"{FAMILY}|{pair}|{sampler}|{qform}",
                                                                                   "wording", x.skin_id)))
        self._wording_memo[mk] = w.skin_id
        self._wording_load[w.skin_id] = self._wording_load.get(w.skin_id, 0) + 1
        return w

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    def stream_packs(self, sampler: str, sub: str) -> list:
        """The packs one (sampler, sub-form) stream draws from (G0 S1): all packs when there are at most
        PACKS_PER_STREAM, else a fixed seeded subset of PACKS_PER_STREAM, so a card holds about 30-45 rows."""
        names = sorted(self.packs)
        if len(names) <= PACKS_PER_STREAM:
            return names
        return sorted(sorted(names, key=lambda n: uhash(FAMILY, "packset", sampler, sub, n))[:PACKS_PER_STREAM])

    # ------------------------------------------------------------------------------------------- lexicon draws
    def _clause(self, rng: random.Random, sem: str, bind: dict) -> S.Slot:
        if self.lexicon is None:
            raise ContractError("T33 needs its lexicon registry (T33Plugin(lexicon=...))")
        ids = sorted(f for f, x in self.lexicon.forms.items()
                     if x.sem_id == sem and self.lexicon.status(f) == "admitted")
        if not ids:
            raise ContractError(f"no admitted lexicon form for {sem}")
        return self.lexicon.clause(rng.choice(ids), bind=bind)

    # ------------------------------------------------------------------------------------------- simulator
    def _tool(self, rng, pack: str, arch: str | None = None) -> tuple:
        tools = [t for t in self.packs[pack] if arch is None or VERB_ARCH[t[1]] == arch]
        return rng.choice(tools)

    @staticmethod
    def _fresh_target(rng, kind: str, taken: set) -> str:
        for _ in range(200):
            t = TARGET_MAKERS[kind](rng)
            if t not in taken:
                taken.add(t)
                return t
        raise ContractError("no fresh target")

    @staticmethod
    def _near_miss(rng, t: str, taken: set) -> str:
        """The same id with two adjacent digits swapped or one digit changed (a mistyped target)."""
        digits = [i for i, ch in enumerate(t) if ch.isdigit()]
        for _ in range(40):
            if len(digits) >= 2 and rng.random() < 0.6:
                x = rng.randrange(len(digits) - 1)
                a, b = digits[x], digits[x + 1]
                if b != a + 1 or t[a] == t[b]:
                    continue
                cand = t[:a] + t[b] + t[a] + t[b + 1:]
            else:
                i = rng.choice(digits)
                cand = t[:i] + str((int(t[i]) + rng.randint(1, 9)) % 10) + t[i + 1:]
            if cand != t and cand not in taken:
                taken.add(cand)
                return cand
        raise ContractError("no near-miss target")

    @staticmethod
    def _patterns(arch: str, is_async: bool, done: bool) -> list:
        return sorted(p for p, (archs, asy, d, _w) in PATTERNS.items() if arch in archs and asy == is_async
                      and d == done)

    @staticmethod
    def _pick(rng, patterns: list) -> str:
        """A weighted draw among the given patterns (PATTERNS weights)."""
        return rng.choices(patterns, [PATTERNS[x][3] for x in patterns])[0]

    def _plan(self, rng, arch: str, pattern: str, *, result_mode: str = "full", has_dur: bool = False,
              boundary: bool = False, pre: int | None = None) -> dict:
        """One step as the simulator designs it: try codes, polls (state, value, duration) and the designed facts.
        pre: the number of transient answers (5xx / 429; 500 / 502 / 504 before a 409) before the final try; the
        pattern's own count when None (PATTERN_PRE). A need-driven episode sets it to meet a max_tries need."""
        archs, is_async, done, _w = PATTERNS[pattern]
        if arch not in archs:
            raise ContractError(f"pattern {pattern} does not fit a {arch} step")
        n_pre = PATTERN_PRE[pattern] if pre is None else pre
        if n_pre < 0 or (pattern == "sync_retry_409" and n_pre < 1):
            raise ContractError(f"pattern {pattern} with {n_pre} transient tries")
        req = None
        if arch == "money":
            req = rng.randrange(5, 2500) * 100 if rng.random() < 0.6 else rng.randrange(500, 250000)
        elif arch == "bulk":
            req = rng.randrange(12, 4800) * 10
        ok = OK_CODES.get(arch, OK_CODES["money"])
        hard = HARD.get(arch, HARD["money"])

        def head(pool=TRANSIENT) -> list:
            return [rng.choice(pool) for _ in range(n_pre)]
        codes = {
            "sync_ok": lambda: head() + [rng.choice(ok)],
            "sync_retry_ok": lambda: head() + [rng.choice(ok)],
            "sync_three_ok": lambda: head() + [rng.choice(ok)],
            "sync_retry_409": lambda: head((500, 502, 504)) + [409],
            "sync_fail": lambda: head() + [rng.choice(hard + TRANSIENT)],
            "sync_retry_fail": lambda: head() + [rng.choice(TRANSIENT + hard)],
            "async_ok": lambda: head() + [202], "async_retry_ok": lambda: head() + [202],
            "async_nopoll": lambda: head() + [202], "async_running": lambda: head() + [202],
            "async_failed": lambda: head() + [202],
        }[pattern]()
        states = {
            "async_ok": lambda: ["running"] * self._interim_on + ["succeeded"],
            "async_retry_ok": lambda: ["running"] * self._interim_on + ["succeeded"],
            "async_running": lambda: [rng.choice(("queued", "running"))] + ["running"] * self._interim_on,
            "async_failed": lambda: ["running"] * self._interim_on + ["failed"],
        }.get(pattern, lambda: [])()
        sync_value = arch == "money" and not is_async and done
        result = None
        if sync_value or (states and arch in VALUE_ARCH):
            if result_mode == "partial":
                d = 1 if boundary else rng.randint(1, max(1, req // 4))
                result = max(1, req - d)
            else:
                result = req
        polls = []
        has_dur = bool(has_dur and is_async)
        if states:
            n = len(states)
            vals = ([result] * n if arch == "money" else
                    sorted(rng.randint(0, result // 2) for _ in range(n - 1)) + [result])
            durs = [None] * n
            if has_dur:
                final = rng.randrange(200, 24000) * 10
                durs = sorted(rng.randrange(10, final // 10) * 10 for _ in range(n - 1)) + [final]
            polls = [(states[x], vals[x], durs[x]) for x in range(n)]
        dur = polls[-1][2] if polls else None
        return {"arch": arch, "pattern": pattern, "async": is_async, "has_dur": has_dur, "req": req, "codes": codes,
                "polls": polls, "res_try": len(codes) if sync_value else None,
                "silent": done and codes[-1] in (204, 409),
                "retried_ok": done and len(codes) > 1,
                "queued_2xx": (not done) and 202 in codes,
                "intent": {"done": done, "result": result, "req": req, "tries": len(codes), "dur": dur}}

    def _set_final_dur(self, plan: dict, dur: int) -> None:
        st, val, _ = plan["polls"][-1]
        plan["polls"][-1] = (st, val, dur)
        if len(plan["polls"]) > 1:
            plan["polls"] = [(s, v, min(d, dur - 10)) for s, v, d in plan["polls"][:-1]] + [plan["polls"][-1]]
        plan["intent"]["dur"] = dur

    def _natural_plan(self, rng, arch: str, *, is_async: bool | None = None, done_p: float = 0.68,
                      partial_p: float = 0.22, dur_p: float = 0.45) -> dict:
        """A step drawn forward: about a third of steps fail (spec 3.3: 30% injected failures)."""
        if is_async is None:
            is_async = arch == "bulk" or (arch == "money" and rng.random() < ASYNC_MONEY_P)
        done = rng.random() < done_p
        pattern = self._pick(rng, self._patterns(arch, is_async, done))
        return self._plan(rng, arch, pattern, result_mode="partial" if rng.random() < partial_p else "full",
                          has_dur=rng.random() < dur_p)

    def _episode(self, rng, entries: list) -> tuple:
        """Number the steps in log order, lay out their lines (a job's polls may come after the next step's tries)
        and make every slot. Returns (slots, steps, lines, intent per step)."""
        slots, steps, lines, intent = {}, [], [], {}

        def add_poll(k, p, x):
            st_, val, dur = p["polls"][x]
            i = len(lines) + 1
            res = p["arch"] in VALUE_ARCH
            lines.append({"step": k, "kind": "poll", "try": None, "job": False, "res": res, "dur": dur is not None})
            slots[f"L{i}_STATE"] = S.category_slot(st_, STATES)
            if res:
                slots[f"L{i}_VAL"] = _value_slot(p["arch"], val)
                intent[str(k)]["rl"] = i
            if dur is not None:
                slots[f"L{i}_DUR"] = S.count_slot(dur)
            intent[str(k)]["lp"] = i

        pending = []
        for k, e in enumerate(entries, 1):
            p = e["plan"]
            arch = p["arch"]
            slots[f"S{k}_TOOL"] = S.id_slot(e["tool"])
            slots[f"S{k}_ENT"] = S.id_slot(e["target"])
            slots[f"S{k}_KEY"] = S.id_slot(e["key"])
            if arch in VALUE_ARCH:
                slots[f"S{k}_REQ"] = _value_slot(arch, p["req"])
            if p["async"]:
                slots[f"S{k}_JOB"] = S.id_slot(e["job"])
            steps.append({"n": k, "arch": arch, "verb": e["verb"], "async": p["async"], "dur": p["has_dur"]})
            intent[str(k)] = {**p["intent"], "lt": None, "lp": None, "rl": None}
            for t, code in enumerate(p["codes"], 1):
                i = len(lines) + 1
                res = p["res_try"] == t
                lines.append({"step": k, "kind": "try", "try": t, "job": code == 202, "res": res, "dur": False})
                slots[f"L{i}_CODE"] = S.count_slot(code)
                if res:
                    slots[f"L{i}_VAL"] = _value_slot(arch, p["intent"]["result"])
                    intent[str(k)]["rl"] = i
                intent[str(k)]["lt"] = i
            for kk, pp in pending:
                for x in range(len(pp["polls"])):
                    add_poll(kk, pp, x)
            pending = []
            if p["polls"]:
                if k < len(entries) and rng.random() < 0.35:
                    pending.append((k, p))
                else:
                    for x in range(len(p["polls"])):
                        add_poll(k, p, x)
        for kk, pp in pending:
            for x in range(len(pp["polls"])):
                add_poll(kk, pp, x)
        return slots, steps, lines, intent

    def _entry(self, rng, pack: str, plan: dict, taken: set, tool: tuple | None = None) -> dict:
        """A step's tool, target, idempotency key and job id (all unique within the episode)."""
        name, verb, kind = tool or self._tool(rng, pack, plan["arch"])
        ids = {}
        for what, prefix in (("key", "ik"), ("job", "job")):
            while True:
                ids[what] = f"{prefix}-{rng.randrange(0x10, 0xFF):02x}"
                if ids[what] not in taken:
                    taken.add(ids[what])
                    break
        return {"plan": plan, "tool": name, "verb": verb, "kind": kind, "target": self._fresh_target(rng, kind, taken),
                **ids}

    # ------------------------------------------------------------------------------------------- design (construction)
    @staticmethod
    def design_checks(checks: list, it: dict, r_max, d_max) -> list:
        """The designed result of each listed check (construction side; G0 S8)."""
        out = []
        for sem in checks:
            if sem == "crit.finished":
                out.append(it["done"])
            elif sem in VALUE_CHECKS:
                out.append(it["result"] is not None and it["result"] == it["req"])
            elif sem == "crit.max_tries":
                out.append(it["tries"] <= r_max)
            else:
                out.append(it["dur"] is not None and it["dur"] <= d_max * 1000)
        return out

    @staticmethod
    def design_verdict(value, it: dict | None) -> str:
        """The designed verdict of one claim (construction side; G0 S9). it None: the target is not in the log."""
        if it is None:
            return "not_shown"
        if not it["done"]:
            return "contradicted"
        if value is not None and value != it["result"]:
            return "contradicted"
        return "supported"

    def designed_answer(self, spec: Spec, vec: list | None = None, verdicts: list | None = None):
        st = spec.structure
        if st["sub"] == "a":
            return map_a(spec.qform, st["checks"], vec if vec is not None else st["intent"]["checks"])
        targets = [spec.slots[f"K{j}_ENT"].value for j in range(1, len(st["claims"]) + 1)]
        return map_b(spec.qform, targets, verdicts if verdicts is not None else st["intent"]["verdicts"], st["asked"])

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        self._interim_on = uhash(FAMILY, "interim", sampler, seed) < (
            INTERIM_POLL_P_S4 if sampler == "S4" else INTERIM_POLL_P)      # G0 sections 10, 11: a row-level, label-blind draw
        # antithetic pairs: seeds 2m and 2m + 1 share the question form and get opposite yes/no answers (a per-pair
        # random flip decides which is yes), so yes/no gold is 50/50 by construction over whole pairs
        pair = seed // 2
        # the question form of a pair comes from a golden-ratio (Kronecker) sequence over the pair index, offset per
        # sampler: label-blind like a hash draw, but every window of consecutive pairs holds the shares almost exactly
        # (a 1,000-row pilot has about 300 pairs: independent draws move the yes/no share by +-3 pp)
        u, acc, qform = (pair * 0.6180339887498949 + uhash(FAMILY, "qoff", sampler)) % 1.0, 0.0, QFORM_SHARES[-1][0]
        for q, share in QFORM_SHARES:
            acc += share
            if u < acc:
                qform = q
                break
        if qform in DNEG_FALLBACK and not self.usable_qform(qform):     # no clean wording: the positive form (label-blind)
            qform = DNEG_FALLBACK[qform]
        want_yes = (seed % 2 == 0) != (uhash(FAMILY, "flip", sampler, pair) < 0.5)
        sub = SUB_OF[qform]
        pack = rng.choice(self.stream_packs(sampler, sub))
        fmt = rng.choice(SAMPLER_FORMATS[sampler])
        order = "msg_first" if (sampler == "S4" and sub == "b") else "log_first"
        card = f"{FAMILY}:{sampler}:{sub}:{pack}"
        if len(self.packs) < PACKS_PER_STREAM:            # few packs (the built-in set): split each card in two
            card += f":c{rng.randrange(2)}"
        user = rng.choice(NAMES)
        build = self._sample_a if sub == "a" else self._sample_b
        slots, structure, depth, deep, tags = build(rng, sampler, qform, pack, seed, want_yes)
        slots["USER"] = S.name_slot(user)
        structure.update(sub=sub, fmt=fmt, order=order)
        spec = Spec(FAMILY, sampler, seed, card, qform, slots, structure=structure, depth=depth, deep=deep,
                    tags=tuple(sorted(tags)), pack=pack)
        spec = self.derive(spec)
        want, got = self.designed_answer(spec), self.solve_a(spec)
        if want != got:
            raise ContractError(f"T33 construction says {want!r} but solver A says {got!r} ({sampler}, seed {seed})")
        return spec

    def _draw_checks(self, rng, arch: str, is_async: bool, at_least_two: bool, finished_first: bool = False) -> list:
        """The listed checks. finished_first (ch_failed_check): crit.finished is listed first, so no value check is
        ever read before it. A failed or running money job still prints its amount and a running bulk job may
        already print every row (S4, S7); a reader who takes "the step's result equals the requested amount" as
        failing on a step that is not done would otherwise answer that check where the card's first failing check
        is "finished" (review fix: 3.7% of ch_failed_check rows). On the yes/no forms the order changes nothing."""
        avail = ([("crit.all_written" if arch == "bulk" else "crit.amount_match")] if arch in VALUE_ARCH else [])
        avail.append("crit.max_tries")
        if is_async:
            avail.append("crit.max_duration")
        n_extra = rng.choices((0, 1, 2), (0.12, 0.58, 0.30))[0]
        n_extra = min(len(avail), max(n_extra, 1 if at_least_two else 0))
        extra = rng.sample(avail, n_extra)
        if finished_first:
            return ["crit.finished"] + extra
        checks = ["crit.finished"] + extra
        rng.shuffle(checks)
        return checks

    def _bounds(self, rng, plan: dict, checks: list, need: dict | None, boundary: bool, r_max: int | None) -> tuple | None:
        """R_MAX and D_MAX. R_MAX is drawn FIRST from the seed (label-blind, R_MAX_CHOICES) and the episode is built to
        the need (pilot F2: a bound drawn after the episode predicted the gold: 1 try was gold on 45% of its
        showings, 3 tries on none), so it comes in unchanged; D_MAX is natural (forward) or built to the need."""
        it = plan["intent"]
        d_max = None
        if "crit.max_tries" not in checks:
            r_max = None
        if "crit.max_duration" in checks:
            nd = None if need is None else need["crit.max_duration"]
            dur = it["dur"]
            if nd is None:
                d_max = rng.randint(5, 240) if dur is None else max(1, math.ceil(dur / 1000) + rng.randint(-12, 12))
            elif nd:
                if dur is None:
                    return None
                d_max = math.ceil(dur / 1000)
                if boundary:
                    self._set_final_dur(plan, d_max * 1000)
                else:
                    d_max += rng.randint(0, 25)
            else:
                if dur is None:
                    d_max = rng.randint(5, 240)
                else:
                    d_max = (dur - 1) // 1000 - (0 if boundary else rng.randint(0, 25))
                    if d_max < 1:
                        return None
                    if boundary:                                  # S2: 10 ms over the limit
                        self._set_final_dur(plan, d_max * 1000 + 10)
        return r_max, d_max

    def _need_step(self, rng, arch: str, is_async: bool, checks: list, need: dict, boundary: bool, r_max: int | None):
        nf = need["crit.finished"]
        vc = next((c for c in checks if c in VALUE_CHECKS), None)
        nv = need.get(vc) if vc else None
        nt, nd = need.get("crit.max_tries"), need.get("crit.max_duration")
        cands = []
        for p in self._patterns(arch, is_async, nf):
            shows = (arch == "money" and not is_async and nf) or (is_async and p != "async_nopoll")
            if nv is True and not shows:
                continue
            if nd is True and (not is_async or p == "async_nopoll"):
                continue
            if nt is True and r_max == 1 and p == "sync_retry_409":     # a 409 needs a try before it: 2 tries > R_MAX
                continue
            cands.append(p)
        if not cands:
            return None
        pattern = self._pick(rng, cands)
        pre = None
        if nt is not None:                       # build the tries to the need: failing = R_MAX + 1, holding <= R_MAX
            nat = PATTERN_PRE[pattern]
            if nt is False:
                pre = r_max
            elif boundary or rng.random() < 0.5:
                pre = r_max - 1
            else:
                pre = min(nat, r_max - 1)
            if pattern == "sync_retry_409":
                pre = max(1, pre)
        mode = "full" if nv is True else ("partial" if nv is False else ("partial" if rng.random() < 0.2 else "full"))
        plan = self._plan(rng, arch, pattern, result_mode=mode,
                          has_dur=(nd is not None) or rng.random() < 0.4, boundary=boundary, pre=pre)
        b = self._bounds(rng, plan, checks, need, boundary, r_max)
        if b is None:
            return None
        return plan, b[0], b[1]

    def _sample_a(self, rng, sampler, qform, pack, seed, want_yes):
        q = self.QFORMS[qform]
        boundary = sampler == "S2"
        forward = sampler != "S2"
        n_steps = _row_steps(sampler, seed)
        n_lines = _row_lines(sampler, seed, n_steps)
        r_max0 = R_MAX_CHOICES[min(len(R_MAX_CHOICES) - 1, int(uhash(FAMILY, "rmax", sampler, seed) * len(R_MAX_CHOICES)))]
        u_gold = uhash(FAMILY, "fcc_gold", sampler, seed)
        fcc = qform == "ch_failed_check"
        for attempt in range(120):
            if not fcc or attempt in (0, 100):        # ch_failed_check: one draw (a last-resort redraw at 100)
                arch = rng.choices(("money", "bulk", "action"), (0.38, 0.37, 0.25))[0]
                is_async = arch == "bulk" or (arch == "money" and rng.random() < ASYNC_MONEY_P)
                checks = self._draw_checks(rng, arch, is_async, at_least_two=fcc, finished_first=fcc)
            if fcc:
                # the display plan is drawn from the row key before any structure (c2_kit.choiceplan): None is gold on
                # 1 / k of the rows (k = listed checks + None), else the gold check is uniform over the listed checks;
                # the checks stay fixed while plans are drawn, so every check type is gold on about 1 / k of the rows
                # that show it (redrawing the checks until a plan fits picked the check types that fail easily)
                cplan = plan_choice(self._okey(sampler, seed, qform), closed=len(checks), abstain=True)
                tpos = None if cplan.gold_abstain else min(len(checks) - 1, int(u_gold * len(checks)))
            else:
                ok_target = want_yes == (q.polarity == 1)
            r_max = r_max0 if "crit.max_tries" in checks else None
            if forward and attempt < (40 if fcc else 80):
                plan_ = self._natural_plan(rng, arch, is_async=is_async,
                                           dur_p=0.85 if "crit.max_duration" in checks else 0.45)
                b = self._bounds(rng, plan_, checks, None, False, r_max)
                if b is None:
                    continue
                r_max, d_max = b
            else:
                if qform == "ch_failed_check":
                    vec = [True] * len(checks)
                    if tpos is not None:
                        vec = ([True] * tpos + [False]
                               + [rng.random() >= P_LATER_FAIL for _ in checks[tpos + 1:]])
                else:
                    vec = [True] * len(checks)
                    if not ok_target:
                        n_fail = 2 if len(checks) >= 2 and rng.random() < 0.25 else 1
                        for i in rng.sample(range(len(checks)), n_fail):
                            vec[i] = False
                got = self._need_step(rng, arch, is_async, checks, dict(zip(checks, vec)), boundary, r_max)
                if got is None:
                    continue
                plan_, r_max, d_max = got
            vec = self.design_checks(checks, plan_["intent"], r_max, d_max)
            if qform == "ch_failed_check":
                if _first_fail(vec) != tpos:
                    continue
            elif all(vec) != ok_target:
                continue
            taken: set = set()
            asked = rng.randint(1, n_steps)
            entries = []
            for k in range(1, n_steps + 1):
                if k == asked:
                    entries.append(self._entry(rng, pack, plan_, taken))
                else:
                    a2 = rng.choices(("money", "bulk", "action"), (0.38, 0.37, 0.25))[0]
                    entries.append(self._entry(rng, pack, self._natural_plan(rng, a2), taken))
            slots, steps, lines, istep = self._episode(rng, entries)
            n_retries = sum(1 for ln in lines if ln["kind"] == "try") - n_steps
            if (len(lines) > MAX_LINES or abs(len(lines) - n_lines) > attempt // 25
                    or abs(n_retries - _row_retries(sampler, seed, "crit.max_tries" in checks, r_max0)) > attempt // 25):
                continue
            break
        else:
            raise ContractError(f"T33 (a): no episode for {sampler} seed {seed}")
        plan = plan_
        slots["STEP"] = S.count_slot(asked)
        for c, sem in enumerate(checks, 1):
            bind = {}
            if sem in CHECK_BIND:
                fslot, sslot = CHECK_BIND[sem]
                bind = {fslot: sslot}
            slots[f"CHK{c}"] = self._clause(rng, sem, bind)
        if r_max is not None:
            slots["R_MAX"] = S.count_slot(r_max, TRY_UNIT)
        if d_max is not None:
            slots["D_MAX"] = S.count_slot(d_max, SECOND_UNIT)
        it = istep[str(asked)]
        structure = {"steps": steps, "lines": lines, "checks": list(checks), "asked": asked,
                     "intent": {"steps": istep, "checks": vec}}
        tags = set()
        if plan["queued_2xx"]:
            tags.add("status_2xx_unfinished")
        if plan["retried_ok"]:
            tags.add("retry_then_success")
        if plan["silent"]:
            tags.add("silent_success")
        if any(c in VALUE_CHECKS for c in checks) and it["result"] is not None and it["result"] != it["req"]:
            tags.add("partial_write")
        if "crit.max_duration" in checks:
            tags.add("ms_vs_seconds")
        if (r_max is not None and r_max == it["tries"]) or (
                d_max is not None and it["dur"] is not None and abs(it["dur"] - d_max * 1000) < 1000):
            tags.add("boundary")
        depth = 1 + sum(c in ("crit.max_tries", "crit.max_duration") for c in checks)
        return slots, structure, depth, depth >= 3, tags

    # ---- sub-form (b)
    def _need_claims(self, rng, pack, need: list, boundary: bool):
        taken: set = set()
        entries, claims = [], []
        for v in need:
            if v == "supported":
                arch = rng.choices(("money", "bulk", "action"), (0.4, 0.35, 0.25))[0]
                is_async = arch == "bulk" or (arch == "money" and rng.random() < ASYNC_MONEY_P)
                plan = self._plan(rng, arch, self._pick(rng, self._patterns(arch, is_async, True)),
                                  result_mode="partial" if rng.random() < 0.2 else "full",
                                  has_dur=rng.random() < 0.4)
                e = self._entry(rng, pack, plan, taken)
                entries.append(e)
                claims.append({"verb": e["verb"], "target": e["target"], "value": plan["intent"]["result"],
                               "entry": e, "cause": "ok"})
            elif v == "contradicted":
                arch = rng.choices(("money", "bulk", "action"), (0.4, 0.35, 0.25))[0]
                causes = ["status"] + (["scale", "scale"] if arch == "money" else []) + (
                    ["swap_req", "swap_other"] if arch in VALUE_ARCH else [])
                cause = rng.choice(causes)
                is_async = arch == "bulk" or (arch == "money" and rng.random() < ASYNC_MONEY_P)
                done = cause != "status"
                mode = "partial" if cause == "swap_req" else ("partial" if rng.random() < 0.2 else "full")
                plan = self._plan(rng, arch, self._pick(rng, self._patterns(arch, is_async, done)), result_mode=mode,
                                  has_dur=rng.random() < 0.4, boundary=boundary)
                e = self._entry(rng, pack, plan, taken)
                entries.append(e)
                it = plan["intent"]
                if cause == "status":
                    value = it["req"]
                elif cause == "scale":
                    value = it["result"] * 100
                elif cause == "swap_req":
                    value = it["req"]
                else:
                    donor = self._plan(rng, arch, self._pick(rng, self._patterns(arch, is_async, True)),
                                       has_dur=rng.random() < 0.4)
                    if donor["intent"]["result"] == it["result"]:
                        return None
                    entries.append(self._entry(rng, pack, donor, taken))
                    value = donor["intent"]["result"]
                claims.append({"verb": e["verb"], "target": e["target"], "value": value, "entry": e, "cause": cause})
            else:
                claims.append({"cause": rng.choice(("near_miss", "no_call")), "entry": None})
        for c in claims:                                       # not-shown claims last: they may need a source step
            if c["entry"] is not None or c["cause"] not in ("near_miss", "no_call"):
                continue
            if c["cause"] == "near_miss":
                src = self._entry(rng, pack, self._natural_plan(rng, rng.choice(("money", "bulk", "action"))), taken)
                entries.append(src)
                it = src["plan"]["intent"]
                c.update(verb=src["verb"], target=self._near_miss(rng, src["target"], taken),
                         value=(it["result"] if it["result"] is not None else it["req"]))
            else:
                name, verb, kind = self._tool(rng, pack)
                arch = VERB_ARCH[verb]
                value = None
                if arch == "money":
                    value = rng.randrange(5, 2500) * 100
                elif arch == "bulk":
                    value = rng.randrange(12, 4800) * 10
                c.update(verb=verb, target=self._fresh_target(rng, kind, taken), value=value)
        return entries, claims, taken

    def _forward_claims(self, rng, pack, n_claims: int, n_steps: int):
        taken: set = set()
        entries = [self._entry(rng, pack, self._natural_plan(rng, rng.choices(
            ("money", "bulk", "action"), (0.4, 0.35, 0.25))[0], done_p=0.7, partial_p=0.2), taken)
            for _ in range(n_steps)]
        no_call = 1 if rng.random() < 0.2 else 0
        linked = rng.sample(entries, min(n_claims - no_call, len(entries)))
        claims = []
        for e in linked:
            it = e["plan"]["intent"]
            arch = e["plan"]["arch"]
            value, cause = None, "ok"
            if arch in VALUE_ARCH:
                if not it["done"]:
                    value, cause = it["req"], "status"
                else:
                    r = rng.random()
                    others = sorted({o["plan"]["intent"]["result"] for o in entries if o is not e
                                     and o["plan"]["arch"] == arch and o["plan"]["intent"]["result"] is not None}
                                    - {it["result"]})
                    if r < 0.64:
                        value = it["result"]
                    elif arch == "money" and r < 0.78:
                        value, cause = it["result"] * 100, "scale"
                    elif r < 0.94 and others:
                        value, cause = rng.choice(others), "swap_other"
                    elif it["result"] != it["req"]:
                        value, cause = it["req"], "swap_req"
                    else:
                        if arch == "money":
                            value, cause = it["result"] * 100, "scale"
                        else:
                            value, cause = it["result"] + rng.randint(1, 50) * 10, "swap_value"
            elif not it["done"]:
                cause = "status"
            target = e["target"]
            entry = e
            if rng.random() < 0.1:
                target, entry, cause = self._near_miss(rng, e["target"], taken), None, "near_miss"
            claims.append({"verb": e["verb"], "target": target, "value": value, "entry": entry, "cause": cause})
        if no_call:
            name, verb, kind = self._tool(rng, pack)
            arch = VERB_ARCH[verb]
            value = rng.randrange(5, 2500) * 100 if arch == "money" else (
                rng.randrange(12, 4800) * 10 if arch == "bulk" else None)
            claims.append({"verb": verb, "target": self._fresh_target(rng, kind, taken), "value": value,
                           "entry": None, "cause": "no_call"})
        rng.shuffle(claims)
        return entries, claims, taken

    def _sample_b(self, rng, sampler, qform, pack, seed, want_yes):
        q = self.QFORMS[qform]
        boundary = sampler == "S2"
        forward = sampler != "S2"
        u_gold, u_pos = uhash(FAMILY, "gold", sampler, seed), uhash(FAMILY, "goldpos", sampler, seed)
        # the claim count is drawn from the seed (label-blind) and fixed while structures are tried; a choice row's
        # display plan (k = claims + None) is drawn from the row key before any structure (c2_kit.choiceplan)
        n_claims = (2, 3, 3, 4)[min(3, int(uhash(FAMILY, "nclaims", sampler, seed) * 4))]
        n_steps = _row_steps(sampler, seed, n_claims)
        n_lines = _row_lines(sampler, seed, n_steps)
        for attempt in range(150):
            asked = None
            if qform == "ch_claim_verdict":
                asked = min(n_claims, 1 + int(u_pos * n_claims))
                v_target = VERDICTS[min(2, int(u_gold * 3))]
            elif qform == "ch_bad_claim":
                cplan = plan_choice(self._okey(sampler, seed, qform), closed=n_claims, abstain=True)
                tpos = None if cplan.gold_abstain else min(n_claims - 1, int(u_pos * n_claims))
            else:
                ok_target = want_yes == (q.polarity == 1)
            if forward and attempt < 100:
                entries, claims, taken = self._forward_claims(rng, pack, n_claims, n_steps)
            else:
                bad = lambda: "contradicted" if rng.random() < 0.6 else "not_shown"  # noqa: E731
                need = ["supported"] * n_claims
                if qform == "ch_claim_verdict":
                    need[asked - 1] = v_target
                    for i in range(n_claims):
                        if i != asked - 1 and rng.random() < 0.25 and sum(v != "supported" for v in need) < 2:
                            need[i] = bad()
                elif qform == "ch_bad_claim":
                    if tpos is not None:
                        need[tpos] = bad()
                        for i in range(tpos + 1, n_claims):
                            if rng.random() < 0.3 and sum(v != "supported" for v in need) < 2:
                                need[i] = bad()
                elif not ok_target:
                    n_bad = 2 if n_claims >= 3 and rng.random() < 0.25 else 1
                    for i in rng.sample(range(n_claims), n_bad):
                        need[i] = bad()
                got = self._need_claims(rng, pack, need, boundary)
                if got is None:
                    continue
                entries, claims, taken = got
                if len(entries) > n_steps:       # the step count is fixed by the seed, not by what the label needs
                    continue
                while len(entries) < n_steps:    # neutral filler steps, the same count for every label
                    entries.append(self._entry(rng, pack, self._natural_plan(
                        rng, rng.choice(("money", "bulk", "action"))), taken))
                rng.shuffle(entries)
            if not 2 <= len(claims) <= 4 or not 2 <= len(entries) <= 6:
                continue
            verdicts = [self.design_verdict(c["value"], c["entry"]["plan"]["intent"] if c["entry"] else None)
                        for c in claims]
            targets = [c["target"] for c in claims]
            if qform == "ch_claim_verdict":
                if len(claims) != n_claims or verdicts[asked - 1] != v_target:
                    continue
            elif qform == "ch_bad_claim":
                tp = next((i for i, v in enumerate(verdicts) if v != "supported"), None)
                if len(claims) != n_claims or tp != tpos:
                    continue
            elif all(v == "supported" for v in verdicts) != ok_target:
                continue
            if sum(v != "supported" for v in verdicts) > 2 or len(set(targets)) != len(targets):
                continue
            slots, steps, lines, istep = self._episode(rng, entries)
            if len(lines) > MAX_LINES or abs(len(lines) - n_lines) > attempt // 25:
                continue
            break
        else:
            raise ContractError(f"T33 (b): no episode for {sampler} seed {seed}")
        number = {id(e): k for k, e in enumerate(entries, 1)}
        links = [number[id(c["entry"])] if c["entry"] is not None else None for c in claims]
        for j, c in enumerate(claims, 1):
            arch = VERB_ARCH[c["verb"]]
            slots[f"K{j}_ENT"] = S.id_slot(c["target"])
            bind = {"T": f"K{j}_ENT"}
            if arch in VALUE_ARCH:
                slots[f"K{j}_VAL"] = _value_slot(arch, c["value"])
                bind["V"] = f"K{j}_VAL"
            slots[f"K{j}"] = self._clause(rng, f"claim.{c['verb']}", bind)
        structure = {"steps": steps, "lines": lines, "claims": [{"verb": c["verb"]} for c in claims],
                     "asked": asked, "intent": {"steps": istep, "verdicts": verdicts, "links": links}}
        tags = set()
        results = {int(k): it["result"] for k, it in istep.items()}
        bad = [i for i, v in enumerate(verdicts) if v != "supported"]
        if qform == "ch_claim_verdict":
            decisive = [asked - 1]
        elif qform == "ch_bad_claim":
            decisive = list(range(bad[0] + 1)) if bad else list(range(len(claims)))
        else:
            decisive = bad or list(range(len(claims)))
        for i in decisive:                                    # trap tags read the claims that decide the answer
            c, link = claims[i], links[i]
            if c["cause"] in ("near_miss", "no_call"):
                tags.add("claim_no_call")
            if c["value"] is not None and any(r == c["value"] for k, r in results.items() if k != link):
                tags.add("value_other_entity")
            if link is None:
                continue
            p = c["entry"]["plan"]
            if p["queued_2xx"]:
                tags.add("status_2xx_unfinished")
            if p["retried_ok"]:
                tags.add("retry_then_success")
            if p["silent"]:
                tags.add("silent_success")
            if p["arch"] == "money" and c["value"] is not None:
                tags.add("cents_trap")
            if p["intent"]["result"] is not None and p["intent"]["result"] != p["intent"]["req"]:
                tags.add("partial_write")
        n_bad = sum(v != "supported" for v in verdicts)
        depth = 1 + any(VERB_ARCH[c["verb"]] == "money" for c in claims) + any(c["value"] is not None for c in claims)
        return slots, structure, depth, len(claims) == 4 and n_bad >= 2, tags

    def derive(self, spec: Spec) -> Spec:
        st = spec.structure
        a = st.get("asked")
        if a is None:
            return spec.replace(derived={}, derived_deps={})
        src = f"S{a}_ENT" if st["sub"] == "a" else f"K{a}_ENT"
        return spec.replace(derived={"TARGET": S.id_slot(spec.slots[src].value)}, derived_deps={"TARGET": (src,)})

    # ------------------------------------------------------------------------------------------- solver A
    def _replay(self, spec: Spec, env: dict, flaws: frozenset) -> dict:
        """Solver A: the log lines in order through a per-step state machine (G0 S7)."""
        steps = {}
        for s in spec.structure["steps"]:
            k = s["n"]
            steps[k] = {"target": env[f"S{k}_ENT"], "arch": s["arch"], "req": env.get(f"S{k}_REQ"), "tries": 0,
                        "done": False, "queued": False, "state": None, "result": None, "dur": None}
        for i, ln in enumerate(spec.structure["lines"], 1):
            s = steps[ln["step"]]
            if ln["kind"] == "poll":
                if "polls_as_tries" in flaws:
                    s["tries"] += 1
                s["state"] = env[f"L{i}_STATE"]
                if ln["res"]:
                    s["result"] = env[f"L{i}_VAL"]
                if ln["dur"]:
                    s["dur"] = env[f"L{i}_DUR"]
                continue
            s["tries"] += 1
            if "first_try_only" in flaws and s["tries"] > 1:
                continue
            code = env[f"L{i}_CODE"]
            if code in (200, 201, 204) or ("status_word" in flaws and 200 <= code < 300):
                s["done"] = True
                if ln["res"]:
                    s["result"] = env[f"L{i}_VAL"]
            if code == 202:
                s["queued"] = True
            elif code == 409 and s["tries"] > 1 and "conflict_as_failure" not in flaws:
                s["done"] = True
        for s in steps.values():
            if s["queued"] and s["state"] == "succeeded":
                s["done"] = True
            if "status_word" in flaws and s["queued"]:
                s["done"] = True
            if "request_as_result" in flaws and s["req"] is not None:
                s["result"] = s["req"]
        return steps

    @staticmethod
    def _check(sem: str, s: dict, env: dict, flaws: frozenset) -> bool:
        if sem == "crit.finished":
            return s["done"]
        if sem in VALUE_CHECKS:
            if s["result"] is None:
                return "missing_value_passes" in flaws
            return s["result"] == s["req"]
        if sem == "crit.max_tries":
            return s["tries"] <= env["R_MAX"]
        if sem == "crit.max_duration":
            if s["dur"] is None:
                return "missing_value_passes" in flaws
            return s["dur"] <= env["D_MAX"] * (1 if "ms_as_seconds" in flaws else 1000)
        raise ContractError(f"unknown check {sem}")

    @staticmethod
    def _verdict(target: str, value, steps: dict, flaws: frozenset) -> str:
        hits = [s for s in steps.values() if s["target"] == target]
        if len(hits) > 1:
            raise ContractError(f"claim target {target} binds to two steps")
        if not hits:
            if "missing_call_contradicted" in flaws:
                return "contradicted"
            if "missing_call_supported" in flaws:
                return "supported"
            return "not_shown"
        s = hits[0]
        if "value_on_other_target" in flaws and value is not None and any(
                o["done"] and o["result"] == value for o in steps.values() if o is not s and o["arch"] == s["arch"]):
            return "supported"
        if not s["done"]:
            return "contradicted"
        if value is not None and "claim_value_ignored" not in flaws:
            logged = s["result"]
            if logged is None:
                return "contradicted"
            if "cents_as_dollars" in flaws and s["arch"] == "money":
                logged *= 100
            if logged != value:
                return "contradicted"
        return "supported"

    def answer(self, spec: Spec, flaws: frozenset = frozenset()):
        env = spec.env()
        steps = self._replay(spec, env, flaws)
        last = "last_qualifying" in flaws
        if spec.structure["sub"] == "a":
            n = len(spec.structure["checks"])
            sems = [env[f"CHK{c}"] for c in range(1, n + 1)]
            vec = [self._check(sem, steps[env["STEP"]], env, flaws) for sem in sems]
            return map_a(spec.qform, sems, vec, last)
        n = len(spec.structure["claims"])
        targets = [env[f"K{j}_ENT"] for j in range(1, n + 1)]
        verdicts = [self._verdict(targets[j - 1], env.get(f"K{j}_VAL"), steps, flaws) for j in range(1, n + 1)]
        asked = targets.index(env["TARGET"]) + 1 if spec.qform == "ch_claim_verdict" else None
        return map_b(spec.qform, targets, verdicts, asked, last)

    def solve_a(self, spec: Spec):
        return self.answer(spec)

    # ------------------------------------------------------------------------------------------- canonical (G3)
    def canonical(self, spec: Spec) -> dict:
        env = spec.env()
        st = spec.structure
        steps = [[s["n"], env[f"S{s['n']}_TOOL"], env[f"S{s['n']}_ENT"], env[f"S{s['n']}_KEY"],
                  TABLE_FIELD.get(s["arch"]), env.get(f"S{s['n']}_REQ"), env.get(f"S{s['n']}_JOB")]
                 for s in st["steps"]]
        lines = []
        for i, ln in enumerate(st["lines"], 1):
            val = env[f"L{i}_VAL"] if ln["res"] else None
            if ln["kind"] == "try":
                lines.append([ln["step"], "try", ln["try"], env[f"L{i}_CODE"], None, val, None])
            else:
                lines.append([ln["step"], "poll", None, 200, env[f"L{i}_STATE"], val,
                              env[f"L{i}_DUR"] if ln["dur"] else None])
        c = {"qform": spec.qform, "user": env["USER"], "target": env.get("TARGET"), "steps": steps, "lines": lines}
        if st["sub"] == "a":
            c["step"] = env["STEP"]
            c["checks"] = []
            for x in range(1, len(st["checks"]) + 1):
                sem = env[f"CHK{x}"]
                c["checks"].append([sem, env[CHECK_BIND[sem][1]] if sem in CHECK_BIND else None])
        else:
            c["claims"] = [[env[f"K{j}"], env[f"K{j}_ENT"], env.get(f"K{j}_VAL")]
                           for j in range(1, len(st["claims"]) + 1)]
        return c

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def _line_tpl(fmt: str, ln: dict, i: int, arch: str) -> str:
        k = ln["step"]
        vf = VALUE_FORM.get(arch)
        tool, ent, key, job = ph(f"S{k}_TOOL"), ph(f"S{k}_ENT"), ph(f"S{k}_KEY"), ph(f"S{k}_JOB")
        req = ph(f"S{k}_REQ", vf) if vf else None
        val = ph(f"L{i}_VAL", vf) if ln["res"] else None
        if ln["kind"] == "try":
            code = ph(f"L{i}_CODE", "plain")
            if fmt == "jsonl":
                args = '"target":"' + ent + '","idempotency_key":"' + key + '"'      # compact JSON (G0 S5)
                if req:
                    args += ',"' + REQ_KEY[arch] + '":' + req
                res = ('"job":"' + job + '"') if ln["job"] else (('"' + RES_KEY[arch] + '":' + val) if val else "")
                return ('{"step":%d,"try":%d,"tool":"%s","args":{%s},"status":%s%s}'
                        % (k, ln["try"], tool, args, code, (',"result":{%s}' % res) if res else ""))   # no empty result
            if fmt == "text":
                s = f"step {k} try {ln['try']} | {tool} target={ent} idempotency_key={key}"
                if req:
                    s += f" {REQ_KEY[arch]}={req}"
                s += f" | status {code}"
                if ln["job"]:
                    s += f" | job={job}"
                elif val:
                    s += f" | {RES_KEY[arch]}={val}"
                return s
            cells = [str(k), f"try {ln['try']}", tool, ent, key, TABLE_FIELD.get(arch, ""), req or "", code,
                     job if ln["job"] else "", "", val or "", ""]
        else:
            state = ph(f"L{i}_STATE")
            dur = ph(f"L{i}_DUR", "plain") if ln["dur"] else None
            if fmt == "jsonl":
                extra = ((',"' + RES_KEY[arch] + '":' + val if val else "")
                         + (',"duration_ms":' + dur if dur else ""))
                return '{"step":%d,"poll":"%s","status":200,"result":{"state":"%s"%s}}' % (k, job, state, extra)
            if fmt == "text":
                s = f"step {k} poll {job} | status 200 | state={state}"
                if val:
                    s += f" {RES_KEY[arch]}={val}"
                if dur:
                    s += f" duration_ms={dur}"
                return s
            cells = [str(k), "poll", "", "", "", TABLE_FIELD.get(arch, "") if val else "", "", "200", job, state,
                     val or "", dur or ""]
        return ",".join(cells) if fmt == "csv" else "| " + " | ".join(cells) + " |"

    def _add_log(self, tb: TextBuilder, spec: Spec, slots: dict, forms: dict) -> None:
        st = spec.structure
        arch_of = {s["n"]: s["arch"] for s in st["steps"]}
        tb.add("state", LOG_HEAD)
        heads = {"csv": [CSV_HEADER], "md": [MD_HEADER, MD_RULE]}.get(st["fmt"], [])
        for h in heads:
            tb.add("state", "\n" + h)
        for i, ln in enumerate(st["lines"], 1):
            tb.add("state", "\n").add("state", K.fill(self._line_tpl(st["fmt"], ln, i, arch_of[ln["step"]]), slots,
                                                      forms))

    def _skin_fits(self, sk, spec: Spec) -> bool:
        if sk.family != FAMILY or sk.kind != "skin" or sk.author_mode != "T":
            return False
        decl = set(sk.decl)
        if spec.structure["sub"] == "a":
            return sk.register in A_REGISTERS and bool(decl) and decl <= {"USER", "TARGET"}
        n = len(spec.structure["claims"])
        claims = {f"K{j}" for j in range(1, n + 1)}
        if not (sk.register in B_REGISTERS and claims <= decl <= claims | {"USER"}):
            return False
        # pilot F1 (G3): a claim clause with an internal "and" next to a skin that joins claims with "{Kj} and {Kj+1}"
        # cannot be parsed back (the skin matcher reads a clause up to the first " and "): such a pair never meets
        for j in range(1, n):
            if re.search(r"\{K%d\} and " % j, sk.text, re.I) and re.search(r"\band\b", spec.slots[f"K{j}"].value[2],
                                                                           re.I):
                return False
        return True

    def _key(self, spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    @staticmethod
    def _okey(sampler: str, seed: int, qform: str) -> str:
        """The option-display key of a row: the same string at sampling time (the plan) and at render time."""
        return f"{FAMILY}|{seed}|{sampler}|{qform}|options"

    # ---- skin and register balance (pilot F6)
    def _unit_weight(self, spec: Spec) -> float:
        """Rows a skin will feed for this spec: the base, plus the complement, the attack twin and the minimal-edit twin
        the relation hashes ask for (an equiv partner uses another skin). Label-blind: hashes of the seed only."""
        smp, seed, w = spec.sampler, spec.seed, 1.0
        if spec.qform in PARTNERS and uhash(FAMILY, "comp", smp, seed) < 0.30:
            w += 1.0
        u = uhash(FAMILY, "extra", smp, seed)
        if (spec.structure["sub"] == "a" and P_EQUIV <= u < P_EQUIV + 0.08) or (spec.structure["sub"] == "b"
                                                                                 and u < 0.08):
            w += 1.0
        w += 0.4 * (uhash(FAMILY, "twin", smp, seed) < (P_TWIN_FCC if spec.qform == "ch_failed_check" else P_TWIN))
        return w

    def _pick_skin(self, spec: Spec, ctx, key: str):
        """The unit's skin. Register first (the register whose fitting skins carry the lowest mean load; a message
        voice that suits the pack is preferred while its register is not behind by more than a third of a row), then
        the least-loaded fitting skin of that register (load = estimated rows; a skin stays under SKIN_CAP while any
        skin of the register can). Label-blind: loads count rows, never golds. One key, one skin: a key that renders
        again gets the same skin. Stateful on purpose (a single sequential run; reset_balance() starts a new one):
        a stateless draw cannot hold the 6-rows-per-skin cap, because units differ in size."""
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        sid = self._skin_memo.get(key)
        if sid is not None and sid in ctx.skins and self._skin_fits(ctx.skins[sid], spec):
            return ctx.skins[sid]
        cands = sorted((s for s in ctx.skins.values() if s.held_out == held and self._skin_fits(s, spec)),
                       key=lambda s: s.skin_id)
        if not cands:
            raise ContractError(f"no T33 skin fits this spec (sub {spec.structure['sub']}, held_out={held})")
        sub, w = spec.structure["sub"], self._unit_weight(spec)
        by_reg: dict = {}
        for s in cands:
            by_reg.setdefault(s.register, []).append(s)
        regs = sorted(by_reg)
        # the register whose FITTING skins carry the lowest mean load: every fitting skin of a sub-form ends up equally
        # loaded, so register shares follow the skin counts (the skin cap needs it) and a register that has few skins for
        # this spec (4-claim messages) is not overloaded by the voice preference
        mean = {r: sum(self._skin_load.get(x.skin_id, 0.0) for x in by_reg[r]) / len(by_reg[r]) for r in regs}
        pool = regs
        if sub == "b":
            voiced = [r for r in regs if r in self.voices.get(spec.pack, ()) and mean[r] <= min(mean.values()) + 0.35]
            if voiced and uhash(key, "voice") < 0.7:
                pool = voiced
        reg = min(pool, key=lambda r: (round(mean[r], 6), uhash(key, "reg", r)))
        fit = by_reg[reg]
        under = [s for s in fit if self._skin_load.get(s.skin_id, 0.0) + w <= self.SKIN_CAP]
        skin = min(under or fit, key=lambda s: (self._skin_load.get(s.skin_id, 0.0), uhash(key, "skin", s.skin_id)))
        self._skin_memo[key] = skin.skin_id
        self._skin_load[skin.skin_id] = self._skin_load.get(skin.skin_id, 0.0) + w
        self._reg_load[(sub, reg)] = self._reg_load.get((sub, reg), 0.0) + w
        self._reg_of[key] = reg
        return skin

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule
        key = self._key(spec)
        st = spec.structure
        if skin is None:
            skin = self._pick_skin(spec, ctx, key)
        if not self._skin_fits(skin, spec):
            raise ContractError(f"skin {skin.skin_id} does not fit this spec (T33 renders Mode T skins only)")
        # the wording is drawn once per antithetic pair (_BalancedCtx): both seeds of a pair carry the same wording and
        # opposite golds, so the base rows of every wording cell are 50/50 by construction (pilot F7)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        tb = TextBuilder()
        if st["sub"] == "a":
            tb.add("state", K.fill(REQ_HEAD, slots, forms)).add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
            tb.add("state", "\n\n")
            self._add_log(tb, spec, slots, forms)
            if attack is not None:
                tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        else:
            def message():
                tb.add("state", K.fill(MSG_HEAD, slots, forms)).add("state", skin.fill(slots, forms),
                                                                   skin_id=skin.skin_id)
            if st["order"] == "msg_first":
                message()
                tb.add("state", "\n\n")
            self._add_log(tb, spec, slots, forms)
            if attack is not None:
                tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
            if st["order"] != "msg_first":
                tb.add("state", "\n\n")
                message()
        # the rules block: yes/no rows print it once as the card, choice rows at the head of the instructions
        style = CT.draw_style(spec.seed, spec.sampler)
        used = CD.place_rules(tb, K.fill(CT.block_template(spec, style), slots, forms), self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        okey = self._okey(spec.sampler, spec.seed, spec.qform)
        os_ = None
        # closed label sets: the whole set is shown in one seeded order that does not depend on the gold (a twin that
        # moves the gold keeps the option list, G-TW); the abstain gold share 1 / k comes from the sampler's plan
        if spec.qform == "ch_failed_check":
            env = spec.env()
            n = len(st["checks"])
            chk = {env[f"CHK{c}"]: f"CHK{c}" for c in range(1, n + 1)}
            os_ = build_closed(spec, ans, [env[f"CHK{c}"] for c in range(1, n + 1)],
                               self.error_models(), row_key=okey,
                               render_key=lambda sem: K.fill(slots[chk[sem]].value[2], slots, forms).text,
                               abstain=("none", NONE_CHECK), show_abstain=True)
        elif spec.qform == "ch_bad_claim":
            targets = [slots[f"K{j}_ENT"].value for j in range(1, len(st["claims"]) + 1)]
            os_ = build_closed(spec, ans, targets, self.error_models(), row_key=okey,
                               render_key=lambda t: CLAIM_OPTION.format(t), abstain=("none", NONE_CLAIM),
                               show_abstain=True)
        elif spec.qform == "ch_claim_verdict":
            os_ = build_closed(spec, ans, list(VERDICTS), self.error_models(), row_key=okey,
                               render_key=VERDICT_TEXT.__getitem__)
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CD.defs_style(used, style))

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        st = spec.structure
        seed, smp = spec.seed, spec.sampler
        if spec.qform in PARTNERS and uhash(FAMILY, "comp", smp, seed) < 0.30:
            partners = [(q2, share) for q2, share in PARTNERS[spec.qform] if self.usable_qform(q2)]
            tot = sum(share for _q, share in partners)
            u, acc, q2 = uhash(FAMILY, "ckind", smp, seed) * tot, 0.0, None
            for q2, share in partners:
                acc += share
                if u < acc:
                    break
            if q2 is not None:
                out.append(RelationProposal("complement", qform=q2))
        u = uhash(FAMILY, "extra", smp, seed)
        if st["sub"] == "a" and smp not in self.HELD_OUT_SAMPLERS and u < P_EQUIV:
            fmts = [f for f in FORMATS if f != st["fmt"]]
            fmt2 = fmts[int(uhash(FAMILY, "eqfmt", smp, seed) * len(fmts))]
            base_reg = self._reg_of.get(self._key(spec))          # another register than the base row's (pilot F6)
            regs = [r for r in EQUIV_REGISTERS if r != base_reg]
            reg = regs[int(uhash(FAMILY, "eqreg", smp, seed) * len(regs))]
            out.append(RelationProposal("equiv", spec=spec.replace(structure={**st, "fmt": fmt2}), register=reg,
                                        note=f"log as {fmt2}"))
        elif (st["sub"] == "a" and P_EQUIV <= u < P_EQUIV + 0.08) or (st["sub"] == "b" and u < 0.08):
            out.append(RelationProposal("inv"))
        if uhash(FAMILY, "twin", smp, seed) < (P_TWIN_FCC if spec.qform == "ch_failed_check" else P_TWIN):
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        env = spec.env()
        other = next(n for n in NAMES if n != env["USER"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("USER", S.name_slot(other)), expect="same",
                                    note="rename the user"))
        k = 1 + int(uhash(FAMILY, "meta_k", smp, seed) * len(st["steps"]))
        renamed = spec.with_slot(f"S{k}_TOOL", S.id_slot(env[f"S{k}_TOOL"] + "_v2"))
        out.append(RelationProposal("metamorphic", spec=renamed, expect="same", note="rename a tool"))
        rekeyed = spec.with_slot(f"S{k}_KEY", S.id_slot(env[f"S{k}_KEY"] + "a"))
        out.append(RelationProposal("metamorphic", spec=rekeyed, expect="same", note="change an idempotency key"))
        return out

    def _flip_done_edit(self, spec: Spec, it: dict, k: int, arch: str):
        """(slot, new slot, new done) that flips whether step k is done, touching one log value; None if no such
        value exists (a money step done by a sync try shows its amount on that try, so its code is never flipped)."""
        env = spec.env()
        u = uhash(FAMILY, "flipdone", spec.sampler, spec.seed, k)
        if it["lp"] is not None:
            i = it["lp"]
            state = env[f"L{i}_STATE"]
            new = ("failed" if u < 0.5 else "running") if state == "succeeded" else "succeeded"
            return f"L{i}_STATE", S.category_slot(new, STATES), new == "succeeded"
        if arch == "action":
            i = it["lt"]
            ln = spec.structure["lines"][i - 1]
            code = env[f"L{i}_CODE"]
            if it["done"]:
                new = 422 if code == 409 else 503
            else:
                new = 409 if (ln["try"] > 1 and u < 0.5) else 201
            return f"L{i}_CODE", S.count_slot(new), not it["done"]
        return None

    def _twin(self, spec: Spec):
        """One minimal edit whose effect the construction knows (G0 S11); the answer must change."""
        st = spec.structure
        env = spec.env()
        base = self.designed_answer(spec)
        edits = []                                           # (slot, new slot, new answer)
        if st["sub"] == "a":
            k = st["asked"]
            it = st["intent"]["steps"][str(k)]
            arch = next(s["arch"] for s in st["steps"] if s["n"] == k)
            vec = list(st["intent"]["checks"])
            checks = st["checks"]

            def with_check(sem, v):
                v2 = list(vec)
                v2[checks.index(sem)] = v
                return self.designed_answer(spec, vec=v2)
            fd = self._flip_done_edit(spec, it, k, arch)
            if fd:
                edits.append((fd[0], fd[1], with_check("crit.finished", fd[2])))
            vc = next((c for c in checks if c in VALUE_CHECKS), None)
            if vc and it["rl"] is not None:
                req, res = it["req"], it["result"]
                new = req if res != req else req - 1 - int(uhash(FAMILY, "twinval", spec.seed) * min(req // 4, 400))
                if new >= 1:
                    edits.append((f"L{it['rl']}_VAL", _value_slot(arch, new), with_check(vc, new == req)))
            if spec.qform != "ch_failed_check":            # option texts print the bounds: no bound edit there
                if "crit.max_tries" in checks:
                    r = env["R_MAX"]
                    if r >= it["tries"] and it["tries"] >= 2:
                        edits.append(("R_MAX", S.count_slot(it["tries"] - 1, TRY_UNIT),
                                      with_check("crit.max_tries", False)))
                    elif r < it["tries"]:
                        edits.append(("R_MAX", S.count_slot(it["tries"], TRY_UNIT),
                                      with_check("crit.max_tries", True)))
                if "crit.max_duration" in checks and it["dur"] is not None:
                    d, dur = env["D_MAX"], it["dur"]
                    if dur <= d * 1000 and (dur - 1) // 1000 >= 1:
                        edits.append(("D_MAX", S.count_slot((dur - 1) // 1000, SECOND_UNIT),
                                      with_check("crit.max_duration", False)))
                    elif dur > d * 1000:
                        edits.append(("D_MAX", S.count_slot(math.ceil(dur / 1000), SECOND_UNIT),
                                      with_check("crit.max_duration", True)))
        else:
            verdicts = list(st["intent"]["verdicts"])
            links = st["intent"]["links"]
            taken = {env[f"S{s['n']}_ENT"] for s in st["steps"]} | {
                env[f"K{j}_ENT"] for j in range(1, len(verdicts) + 1)}

            def with_verdict(j, v):
                v2 = list(verdicts)
                v2[j - 1] = v
                return self.designed_answer(spec, verdicts=v2)
            for j, k in enumerate(links, 1):
                if k is None:
                    continue
                it = st["intent"]["steps"][str(k)]
                arch = next(s["arch"] for s in st["steps"] if s["n"] == k)
                val = env.get(f"K{j}_VAL")
                if val is not None and it["done"]:
                    res = it["result"]
                    if val == res:
                        bump = 10 * (1 + int(uhash(FAMILY, "tv", spec.seed) * 40))
                        new = res * 100 if arch == "money" else res + bump
                        edits.append((f"K{j}_VAL", _value_slot(arch, new), with_verdict(j, "contradicted")))
                    else:
                        edits.append((f"K{j}_VAL", _value_slot(arch, res), with_verdict(j, "supported")))
                if spec.qform != "ch_bad_claim":           # option texts print the targets: no target edit there
                    rng = random.Random(f"{FAMILY}|twin-target|{spec.sampler}|{spec.seed}|{j}")
                    new_t = self._near_miss(rng, env[f"K{j}_ENT"], set(taken))
                    edits.append((f"K{j}_ENT", S.id_slot(new_t), with_verdict(j, "not_shown")))
                fd = self._flip_done_edit(spec, it, k, arch)
                if fd:
                    ok = fd[2] and (val is None or val == it["result"])
                    edits.append((fd[0], fd[1], with_verdict(j, "supported" if ok else "contradicted")))
        edits = [e for e in edits if e[2] != base]
        if spec.qform == "ch_failed_check":
            # a ch_failed_check twin can only move "finished" or a value check (option texts print the bounds), so
            # twins piled up on "finished" (54% of twin rows); twins onto it, and onto a value check, are kept at
            # TWIN_CHECK_KEEP so every check type is gold on about 1 / k of the emitted rows that show it (G0 S14)
            key = f"{FAMILY}|{spec.sampler}|{spec.seed}"
            edits = [e for e in edits if all(abstain_twin_kept(key, base, e[2], c, keep)
                                             for c, keep in TWIN_CHECK_KEEP.items())]
        if not edits:
            return None
        slot, new, expect = edits[int(uhash(FAMILY, "twinpick", spec.sampler, spec.seed) * len(edits))]
        cls = "item" if spec.qform == "ch_bad_claim" and expect != "none" else expect
        k = len(st["claims"]) + 1 if spec.qform == "ch_bad_claim" else None
        keep = TWIN_KEEP.get((spec.qform, cls, k), TWIN_KEEP.get((spec.qform, cls), 1.0))
        if keep < 1.0 and uhash(FAMILY, "twinkeep", spec.sampler, spec.seed) >= keep:
            return None                       # F3: thin the twin direction that exists more often (balanced golds)
        return RelationProposal("twin", spec=spec.with_slot(slot, new), changed_slot=slot, expect=expect,
                                note="minimal edit")

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def model(flaw):
            def fn(spec):
                if self.QFORMS[spec.qform].qtype != "choice":
                    return None
                return self.answer(spec, frozenset({flaw}))
            return fn
        return {name: error_model(name, model(name), why) for name, why in FLAWS.items()}
