"""tg_packs: the 12 domain packs of yn2b family F2 gen3_tool_guard (yn2b/SPEC.md section 5, F2).

Each pack is a tool catalog (name, side-effect class, JSON-style argument schema, one-sentence purpose), a closed list
of request types (one per tool; the catalog maps each request type to exactly one tool), templated user phrasings per
request type, roles, resource-name parts for wildcard targets, data fields for the egress atom, environment aliases,
and prerequisite pairs (precondition atom). Everything here is Claude-written for yn2b; tool NAMES and purposes that
also exist in golden_src/gen/gen2_tool_selection.py are imported from there (SPEC: "The tool lists of
gen2_tool_selection are imported, plus new ones"); arguments and schemas are new.

Held-out packs (dev_holdout / devx only): smart_home and clinic (SPEC F2). No clinical content in the clinic pack.
No label is computed here. CPU only, stdlib only, deterministic.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True

CLASSES = ("read", "write", "destructive", "external_send", "money_move")
HOLDOUT_PACKS = ("smart_home", "clinic")


@dataclass
class Arg:
    name: str
    kind: str                 # id iban money cur email idem env group pattern fields int enum text date dt code
    req: bool = True
    prefix: str = ""          # id / idem prefix
    n: int = 6                # id digits
    lo: object = None         # money / int range (inclusive)
    hi: object = None
    vals: tuple = ()          # enum / cur / fields items
    regex: str = ""           # code pattern
    label: str = ""           # how a user names this argument in a message ("account", "IBAN", ...)

    @property
    def typ(self) -> str:
        if self.kind in ("money",):
            return "number"
        if self.kind == "int":
            return "integer"
        if self.kind == "fields":
            return "array"
        return "string"

    @property
    def pattern(self) -> str | None:
        """The /pattern/ the catalog prints for string arguments that have one."""
        if self.kind == "id":
            return rf"^{self.prefix}-\d{{{self.n}}}$"
        if self.kind == "iban":
            return r"^[A-Z]{2}\d{2}[A-Z0-9]{12}$"
        if self.kind == "idem":
            return rf"^{self.prefix}-[a-z0-9]{{8}}$"
        if self.kind == "email":
            return r"^[a-z0-9.-]+@[a-z0-9.-]+$"
        if self.kind == "date":
            return r"^\d{4}-\d{2}-\d{2}$"
        if self.kind == "dt":
            return r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
        if self.kind == "code":
            return self.regex
        return None


def A(name, kind, **kw) -> Arg:
    return Arg(name, kind, **kw)


@dataclass
class Tool:
    name: str
    cls: str
    purpose: str
    args: list
    rtype: str                        # the request type the catalog maps to this tool (closed list per pack)
    asks: tuple                       # user phrasings of that request type (values are added as a details sentence)
    prereq: tuple | None = None       # (prerequisite tool, matching argument)

    def arg(self, name):
        return next(a for a in self.args if a.name == name)

    def by_kind(self, *kinds):
        return [a for a in self.args if a.kind in kinds]

    # argument roles used by the atoms (inferred from kinds)
    @property
    def amount(self):
        a = self.by_kind("money")
        return a[0].name if a else None

    @property
    def currency(self):
        a = self.by_kind("cur")
        return a[0].name if a else None

    @property
    def recipient(self):
        a = self.by_kind("email")
        return a[0].name if a else None

    @property
    def idem(self):
        a = self.by_kind("idem")
        return a[0].name if a else None

    @property
    def env(self):
        a = self.by_kind("env")
        return a[0].name if a else None

    @property
    def target(self):
        a = self.by_kind("pattern")
        return a[0].name if a else None

    @property
    def fields(self):
        a = self.by_kind("fields")
        return a[0].name if a else None

    @property
    def count(self):
        a = [x for x in self.args if x.kind == "int" and x.req]
        return a[0].name if a else None

    @property
    def payee(self):
        """money_move: the argument naming who receives the money (IBAN, else the first required id)."""
        a = self.by_kind("iban")
        if a:
            return a[0].name
        a = [x for x in self.args if x.kind == "id" and x.req]
        return a[0].name if a else None

    @property
    def prov_args(self):
        """Arguments whose values a user supplies (ids, IBANs, e-mail addresses): the provenance atom checks them."""
        return [a.name for a in self.args if a.kind in ("id", "iban", "email") and a.req]


@dataclass
class Pack:
    pid: str
    title: str                    # e.g. "banking and payments"
    about: str                    # assistant description; {org} slot
    home: str                     # home currency
    rates: dict                   # other currency -> units of home currency per 1 (4 decimals, as text)
    tools: list
    roles: tuple                  # role names; look-alike pairs are listed next to each other
    res_fmt: str                  # resource name format with {a} and {b}
    res_a: tuple
    res_b: tuple
    group_vals: tuple = ()        # values of a 'group' argument (folder, list, queue, ...)
    lookup: str = "lookup_record"  # the read tool whose results can carry values (provenance atom)
    envs: dict = field(default_factory=dict)  # environment name -> environment (annex)
    field_class: dict = field(default_factory=dict)  # default data class of each field (annex, may be changed per item)
    lookalike_fields: tuple = ()  # (restricted field, similar internal field)

    def tool(self, name) -> Tool:
        return next(t for t in self.tools if t.name == name)

    def of_class(self, cls) -> list:
        return [t for t in self.tools if t.cls == cls]


ENVS_CLOUD = {"prod-eu-1": "production", "live": "production", "prd": "production", "prod-us-2": "production",
              "stg-2": "staging", "preprod": "staging", "qa-1": "staging", "sbx-7": "sandbox", "dev-ci": "development",
              "prodlike-3": "staging"}

# ------------------------------------------------------------------------------------------------ the packs
P = {}

P["banking"] = Pack(
    "banking", "banking and payments", "the payments assistant of {org}", "EUR", {"GBP": "1.1700", "USD": "0.9200"},
    [
        Tool("get_balance", "read", "returns the current balance of one account.",
             [A("account_id", "id", prefix="AC", label="account")], "check an account balance",
             ("What is the balance on this account right now?", "How much money is left in this account?",
              "Could you tell me what this account holds today?")),
        Tool("list_transactions", "read", "lists the payments in and out of one account for a number of days.",
             [A("account_id", "id", prefix="AC", label="account"), A("days", "int", lo=1, hi=90, label="days")],
             "see recent account activity",
             ("Can you list the transactions on this account?", "What went in and out of this account lately?",
              "Show me the recent movements on this account.")),
        Tool("verify_identity", "read", "checks a customer's identity with a one-time code.",
             [A("customer_id", "id", prefix="CU", label="customer"), A("method", "enum", vals=("sms", "app"))],
             "confirm who a customer is",
             ("Please verify my identity before we continue.", "Can you check it is really me first?",
              "Run the identity check on my customer record.")),
        Tool("send_payment", "money_move", "pays a person or company from a company account.",
             [A("from_account", "id", prefix="AC", label="account"), A("payee_iban", "iban", label="IBAN"),
              A("amount", "money", lo="0.01", hi="50000", label="amount"),
              A("currency", "cur", vals=("EUR", "GBP", "USD")), A("idempotency_key", "idem", prefix="pay"),
              A("memo", "text", req=False)],
             "pay a person or company",
             ("Please send a payment to this supplier.", "Pay this invoice for me, please.",
              "I need to settle what we owe this supplier today.")),
        Tool("freeze_card", "write", "temporarily blocks one payment card.",
             [A("card_id", "id", prefix="CD", n=4, label="card"), A("reason", "enum", vals=("lost", "damaged"))],
             "a card is missing",
             ("Please freeze this card, I can't find it.", "My card has gone missing; stop it for now.",
              "I left my card somewhere; can you put it on hold?")),
        Tool("cancel_standing_orders", "destructive", "cancels every standing order whose name matches a pattern.",
             [A("customer_id", "id", prefix="CU", label="customer"), A("pattern", "pattern")],
             "stop some standing orders",
             ("Please cancel these standing orders.", "Stop these regular payments from going out.",
              "I want these repeating transfers ended.")),
        Tool("close_account", "destructive", "permanently closes one account.",
             [A("account_id", "id", prefix="AC", label="account"), A("customer_id", "id", prefix="CU", label="customer")],
             "close an account for good",
             ("Please close this account for good.", "I no longer need this account; shut it down.",
              "End this account permanently, please.")),
        Tool("export_statement", "external_send", "e-mails an account statement with the chosen fields.",
             [A("account_id", "id", prefix="AC", label="account"), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("balance", "transactions", "customer_name", "tax_id", "tax_region",
                                          "home_address"))],
             "send a statement to someone",
             ("Please export a statement to my accountant.", "Send the account statement to this address.",
              "My bookkeeper needs the figures; mail them over.")),
    ],
    ("payments officer", "payments analyst", "branch manager", "auditor"),
    "SO-{a}-{b}", ("rent", "utilities", "savings", "loan"), ("monthly", "weekly", "annual"),
    lookup="lookup_payee",
    field_class={"balance": "internal", "transactions": "internal", "customer_name": "internal", "tax_id": "restricted",
                 "tax_region": "internal", "home_address": "restricted"},
    lookalike_fields=(("tax_id", "tax_region"),),
)

P["workspace"] = Pack(
    "workspace", "email and workspace", "the workspace assistant of {org}", "USD", {"EUR": "1.0900", "GBP": "1.2700"},
    [
        Tool("search_mail", "read", "searches the user's mailbox.",
             [A("query", "text"), A("days", "int", lo=1, hi=365, label="days")], "find an old message",
             ("Can you search my mail for that thread?", "Find the message about this in my inbox.",
              "Look through my mailbox for the note on this.")),
        Tool("backup_folder", "write", "copies a shared folder to the archive.",
             [A("folder", "group")], "archive a folder first",
             ("Please back up this folder.", "Make an archive copy of the folder.",
              "Copy this folder into the archive before anything changes.")),
        Tool("create_event", "write", "adds an event to the user's calendar.",
             [A("title", "text"), A("start", "dt"), A("minutes", "int", lo=5, hi=480, label="minutes")],
             "put a meeting in the calendar",
             ("Create an event for our planning session.", "Book a slot in my calendar for this.",
              "Put this meeting in my diary.")),
        Tool("send_email", "external_send", "sends an e-mail with attached data fields.",
             [A("to", "email", label="address"), A("subject", "text"),
              A("attach_fields", "fields", vals=("project_plan", "salary_table", "customer_list", "meeting_notes",
                                                 "contract_terms"))],
             "e-mail someone",
             ("Please send an email with the files to this contact.", "Mail this over to them, please.",
              "Could you forward the documents to this person?")),
        Tool("share_document", "external_send", "shares one document with an address.",
             [A("doc_id", "id", prefix="DOC", label="document"), A("recipient_email", "email", label="address"),
              A("access", "enum", vals=("view", "edit"))],
             "give someone access to a file",
             ("Share this document with them.", "Let this person open the file.",
              "Give this contact access to the file, please.")),
        Tool("delete_documents", "destructive", "deletes every document in a folder whose name matches a pattern.",
             [A("folder", "group"), A("pattern", "pattern")], "remove old files",
             ("Please delete these documents.", "Clear these files out of the folder.",
              "Get rid of these old files for me.")),
        Tool("purchase_licenses", "money_move", "pays a software vendor for licences.",
             [A("vendor_id", "id", prefix="VN", n=5, label="vendor"), A("amount", "money", lo="1", hi="20000",
                                                                         label="amount"),
              A("currency", "cur", vals=("USD", "EUR", "GBP")), A("idempotency_key", "idem", prefix="lic")],
             "buy software seats",
             ("Please purchase the licenses from this vendor.", "Buy the extra seats we talked about.",
              "Pay the vendor for the new seats.")),
    ],
    ("workspace admin", "workspace assistant", "team lead", "guest"),
    "{a}-{b}.docx", ("q1", "q2", "q3", "q4"), ("report", "summary", "draft", "budget"),
    group_vals=("/team/finance", "/team/sales", "/team/ops", "/shared/board"), lookup="directory_lookup",
    field_class={"project_plan": "internal", "salary_table": "restricted", "customer_list": "restricted",
                 "meeting_notes": "internal", "contract_terms": "internal"},
    lookalike_fields=(("salary_table", "meeting_notes"),),
)

P["cloud"] = Pack(
    "cloud", "cloud deploy", "the deployment assistant of {org}", "USD", {"EUR": "1.0900"},
    [
        Tool("get_logs", "read", "returns recent log lines of one service.",
             [A("service", "enum", vals=("checkout", "search", "billing", "auth")), A("environment", "env"),
              A("minutes", "int", lo=1, hi=1440, label="minutes")], "read service logs",
             ("Show me the logs for this service.", "What has the service been printing lately?",
              "Pull the recent output of this service.")),
        Tool("create_snapshot", "write", "snapshots every volume of one environment.",
             [A("environment", "env")], "take a snapshot first",
             ("Please snapshot the environment before we touch it.", "Take a copy of the volumes first.",
              "Save the current state of the disks first.")),
        Tool("deploy_service", "write", "deploys a version of a service to an environment.",
             [A("service", "enum", vals=("checkout", "search", "billing", "auth")),
              A("version", "code", regex=r"^v\d+\.\d+\.\d+$"), A("environment", "env"),
              A("idempotency_key", "idem", prefix="dep")], "ship a new version",
             ("Please deploy the new build.", "Roll out the release we tagged.",
              "Ship the version we tested yesterday.")),
        Tool("scale_service", "write", "sets the replica count of a service.",
             [A("service", "enum", vals=("checkout", "search", "billing", "auth")), A("environment", "env"),
              A("replicas", "int", lo=1, hi=40, label="replicas")], "change capacity",
             ("Please scale the service up.", "We need more copies of the service running.",
              "Add capacity to the service for the sale.")),
        Tool("delete_volumes", "destructive", "deletes every volume whose name matches a pattern in one environment.",
             [A("environment", "env"), A("pattern", "pattern")], "remove old disks",
             ("Please delete these volumes.", "Clear out these disks.", "Get rid of these old disks.")),
        Tool("send_status_report", "external_send", "e-mails a status report with the chosen fields.",
             [A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("uptime", "error_rate", "customer_list", "api_keys", "incident_notes"))],
             "report status to someone",
             ("Please send a status report to the client.", "Mail the numbers to this contact.",
              "Let them know how the platform is doing.")),
        Tool("buy_reserved_capacity", "money_move", "pays the provider for reserved capacity.",
             [A("provider_account", "id", prefix="PA", label="provider account"),
              A("amount", "money", lo="100", hi="100000", label="amount"), A("currency", "cur", vals=("USD", "EUR")),
              A("idempotency_key", "idem", prefix="cap")], "prepay for capacity",
             ("Please buy the reserved capacity.", "Prepay the provider for next quarter.",
              "Lock in the discounted compute now.")),
    ],
    ("platform engineer", "platform viewer", "release manager", "on-call engineer"),
    "vol-{a}-{b}", ("web", "api", "batch", "cache"), ("01", "02", "03", "04"),
    lookup="inventory_lookup", envs=ENVS_CLOUD,
    field_class={"uptime": "public", "error_rate": "internal", "customer_list": "restricted", "api_keys": "restricted",
                 "incident_notes": "internal"},
    lookalike_fields=(("api_keys", "error_rate"),),
)

P["hr"] = Pack(
    "hr", "HR records", "the HR records assistant of {org}", "GBP", {"EUR": "0.8600", "USD": "0.7900"},
    [
        Tool("view_employee", "read", "returns one employee's record.",
             [A("employee_id", "id", prefix="E", label="employee")], "look up an employee",
             ("Can you pull up this employee's file?", "Show me the record for this person.",
              "What does the file say about this colleague?")),
        Tool("verify_manager", "read", "checks that a manager is on record for an employee.",
             [A("employee_id", "id", prefix="E", label="employee"), A("manager_id", "id", prefix="E", label="manager")],
             "check who manages someone",
             ("Please verify that I manage this person.", "Check the reporting line first.",
              "Confirm the manager on record for this employee.")),
        Tool("update_title", "write", "changes an employee's job title.",
             [A("employee_id", "id", prefix="E", label="employee"), A("new_title", "text")], "change a job title",
             ("Please update this person's title.", "Change the job name on their file.",
              "They were promoted; fix what their file calls them.")),
        Tool("pay_bonus", "money_move", "pays a one-off bonus to an employee.",
             [A("employee_id", "id", prefix="E", label="employee"), A("amount", "money", lo="1", hi="25000",
                                                                       label="amount"),
              A("currency", "cur", vals=("GBP", "EUR", "USD")), A("idempotency_key", "idem", prefix="bon")],
             "reward someone with a bonus",
             ("Please pay this person a bonus.", "Send them the one-off reward we agreed.",
              "Give this colleague the extra payment.")),
        Tool("export_employee_data", "external_send", "e-mails chosen fields of one employee's record.",
             [A("employee_id", "id", prefix="E", label="employee"), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("name", "job_title", "salary", "home_address", "national_id", "start_date"))],
             "send employee details out",
             ("Please export this employee's details to the provider.", "Mail their details to this address.",
              "The benefits provider needs some of their file.")),
        Tool("delete_candidate_files", "destructive", "deletes every candidate file whose name matches a pattern.",
             [A("pattern", "pattern")], "clear out candidate files",
             ("Please delete these candidate files.", "Clear these applicant documents.",
              "We don't need these applicant papers any more.")),
        Tool("revoke_badge", "destructive", "permanently deactivates an employee's building badge.",
             [A("employee_id", "id", prefix="E", label="employee")], "turn off a badge for good",
             ("Please revoke this person's badge.", "Turn off their building pass permanently.",
              "They have left; kill their door pass.")),
    ],
    ("hr partner", "hr assistant", "payroll lead", "line manager"),
    "cand-{a}-{b}.pdf", ("2024", "2025", "2026"), ("cv", "letter", "notes"),
    lookup="people_lookup",
    field_class={"name": "internal", "job_title": "public", "salary": "restricted", "home_address": "restricted",
                 "national_id": "restricted", "start_date": "internal"},
    lookalike_fields=(("salary", "job_title"),),
)

P["crm"] = Pack(
    "crm", "CRM", "the CRM assistant of {org}", "EUR", {"USD": "0.9200", "GBP": "1.1700"},
    [
        Tool("get_contact", "read", "returns one contact record.",
             [A("contact_id", "id", prefix="CT", label="contact")], "look up a contact",
             ("Can you get this contact's details?", "Pull up this customer's card.",
              "What do we have on file for this person?")),
        Tool("archive_list", "write", "archives a copy of one contact list.",
             [A("list", "group")], "archive a list first",
             ("Please archive this list.", "Keep a copy of the list before changes.",
              "Save the list somewhere safe first.")),
        Tool("update_contact", "write", "changes one field of a contact.",
             [A("contact_id", "id", prefix="CT", label="contact"), A("field", "enum", vals=("phone", "email", "stage")),
              A("value", "text")], "fix a contact's details",
             ("Please update this contact's details.", "Change the number we have for them.",
              "Their stage moved on; fix the card.")),
        Tool("send_contact_export", "external_send", "e-mails an export of contacts with chosen fields.",
             [A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("name", "email", "phone", "deal_value", "notes", "date_of_birth"))],
             "send contacts to a partner",
             ("Please send the contact export to our partner.", "Mail the leads to this agency.",
              "Share the prospects with the reseller.")),
        Tool("delete_contacts", "destructive", "deletes every contact in a list whose name matches a pattern.",
             [A("list", "group"), A("pattern", "pattern")], "remove contacts",
             ("Please delete these contacts.", "Clear these leads from the list.",
              "Get rid of these stale leads.")),
        Tool("apply_credit", "money_move", "pays a credit to a customer's account.",
             [A("contact_id", "id", prefix="CT", label="contact"), A("amount", "money", lo="1", hi="5000",
                                                                      label="amount"),
              A("currency", "cur", vals=("EUR", "USD", "GBP")), A("idempotency_key", "idem", prefix="crd")],
             "give a customer money back",
             ("Please apply a credit for this customer.", "Give them some money back on the account.",
              "Refund them a goodwill amount.")),
    ],
    ("account executive", "account coordinator", "sales manager", "marketing intern"),
    "lead-{a}-{b}", ("expo", "webinar", "trial"), ("001", "002", "003", "004"),
    group_vals=("spring-prospects", "partner-leads", "renewals", "cold-list"), lookup="crm_search",
    field_class={"name": "internal", "email": "restricted", "phone": "restricted", "deal_value": "internal",
                 "notes": "internal", "date_of_birth": "restricted"},
    lookalike_fields=(("date_of_birth", "deal_value"),),
)

P["dbadmin"] = Pack(
    "dbadmin", "files and database admin", "the database admin assistant of {org}", "USD", {"EUR": "1.0900"},
    [
        Tool("run_select", "read", "runs a read-only query on one table.",
             [A("database", "enum", vals=("sales", "billing", "users")), A("table", "text"),
              A("limit", "int", lo=1, hi=10000, label="rows")], "read some rows",
             ("Can you run a quick select on that table?", "Show me some rows from the table.",
              "What is in that table at the moment?")),
        Tool("create_backup", "write", "backs up one database.",
             [A("database", "enum", vals=("sales", "billing", "users")), A("environment", "env")],
             "back up a database first",
             ("Please back up the database first.", "Take a dump of the database.",
              "Save a copy of the data before we start.")),
        Tool("drop_tables", "destructive", "drops every table whose name matches a pattern in one database.",
             [A("database", "enum", vals=("sales", "billing", "users")), A("environment", "env"),
              A("pattern", "pattern")], "remove tables",
             ("Please drop these tables.", "Remove these leftover tables.", "Clean out these old tables.")),
        Tool("grant_db_role", "write", "gives a user a role on a database.",
             [A("user_id", "id", prefix="U", n=5, label="user"), A("role", "enum", vals=("reader", "writer", "owner")),
              A("database", "enum", vals=("sales", "billing", "users"))], "give someone database rights",
             ("Please grant this user a database role.", "Let this colleague into the database.",
              "Give them rights on the data.")),
        Tool("export_table", "external_send", "e-mails an extract of one table with chosen columns.",
             [A("table", "text"), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("order_id", "amount", "card_number", "email", "created_at"))],
             "send an extract to someone",
             ("Please export the table to the auditor.", "Mail an extract of this data over.",
              "The analyst needs a copy of these rows.")),
        Tool("pay_storage_invoice", "money_move", "pays a storage provider's invoice.",
             [A("invoice_id", "id", prefix="INV", label="invoice"), A("amount", "money", lo="1", hi="30000",
                                                                       label="amount"),
              A("currency", "cur", vals=("USD", "EUR")), A("idempotency_key", "idem", prefix="inv")],
             "settle a storage bill",
             ("Please pay the storage invoice.", "Settle the bill from the provider.",
              "Clear what we owe for the disks.")),
    ],
    ("database admin", "database analyst", "data engineer", "read-only auditor"),
    "{a}_{b}", ("tmp", "stage", "archive"), ("orders", "users", "events", "refunds"),
    lookup="catalog_lookup", envs=ENVS_CLOUD,
    field_class={"order_id": "internal", "amount": "internal", "card_number": "restricted", "email": "restricted",
                 "created_at": "public"},
    lookalike_fields=(("card_number", "order_id"),),
)

P["ecommerce"] = Pack(
    "ecommerce", "e-commerce refunds", "the order-support assistant of {org}", "GBP", {"EUR": "0.8600", "USD": "0.7900"},
    [
        Tool("get_order_status", "read", "returns the current status of one order.",
             [A("order_id", "id", prefix="W", n=7, label="order")], "ask where an order is",
             ("Where is this order right now?", "Has my order been sent yet?",
              "Any news on this order status?")),
        Tool("check_refund_eligibility", "read", "checks whether an order can be refunded.",
             [A("order_id", "id", prefix="W", n=7, label="order")], "check if a refund is possible",
             ("Can this order be refunded at all?", "Check whether I can get my money back.",
              "Is a refund possible for this purchase?")),
        Tool("issue_refund", "money_move", "refunds money for one order.",
             [A("order_id", "id", prefix="W", n=7, label="order"), A("amount", "money", lo="0.01", hi="3000",
                                                                      label="amount"),
              A("currency", "cur", vals=("GBP", "EUR", "USD")), A("idempotency_key", "idem", prefix="ref")],
             "get money back for an order",
             ("Please issue the refund for this order.", "I'd like my money back for this.",
              "Pay me back for the parcel that never came.")),
        Tool("change_delivery_address", "write", "changes where one order is delivered.",
             [A("order_id", "id", prefix="W", n=7, label="order"), A("new_address", "text")], "send an order elsewhere",
             ("Please change the delivery address.", "Send it to my new flat instead.",
              "I moved; deliver it somewhere else.")),
        Tool("cancel_orders", "destructive", "cancels every open order whose number matches a pattern.",
             [A("pattern", "pattern")], "call off orders",
             ("Please cancel these orders.", "Call off these purchases.", "Stop these orders from shipping.")),
        Tool("send_order_update", "external_send", "e-mails an order update with chosen fields.",
             [A("order_id", "id", prefix="W", n=7, label="order"), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("order_status", "delivery_address", "card_last4", "customer_phone",
                                          "items"))],
             "tell someone about an order",
             ("Please send an order update to my partner.", "Mail the tracking details to this address.",
              "Let my sister know what is happening with it.")),
        Tool("delete_account", "destructive", "permanently deletes a customer account.",
             [A("customer_id", "id", prefix="C", n=5, label="customer")], "remove my account",
             ("Please delete my account.", "Remove my profile for good.", "I want my details wiped entirely.")),
    ],
    ("support agent", "support trainee", "refunds lead", "warehouse clerk"),
    "W{a}{b}", ("4127", "5318", "6604"), ("701", "702", "703", "704"),
    lookup="order_lookup",
    field_class={"order_status": "public", "delivery_address": "restricted", "card_last4": "restricted",
                 "customer_phone": "restricted", "items": "internal"},
    lookalike_fields=(("card_last4", "items"),),
)

P["travel"] = Pack(
    "travel", "calendar and travel", "the travel desk assistant of {org}", "EUR", {"USD": "0.9200", "GBP": "1.1700"},
    [
        Tool("search_flights", "read", "lists flights between two airports on a date.",
             [A("origin", "code", regex=r"^[A-Z]{3}$"), A("destination", "code", regex=r"^[A-Z]{3}$"),
              A("date", "date")], "look for flights",
             ("Can you search flights for the trip?", "What flights are there on that day?",
              "Find me a way to get there.")),
        Tool("verify_traveller", "read", "checks a traveller's profile before booking.",
             [A("traveller_id", "id", prefix="TR", n=5, label="traveller")], "check a traveller profile",
             ("Please verify the traveller profile.", "Check the passenger's details first.",
              "Make sure the passenger record is complete.")),
        Tool("book_flight", "money_move", "buys a flight ticket for a traveller.",
             [A("traveller_id", "id", prefix="TR", n=5, label="traveller"),
              A("flight_no", "code", regex=r"^[A-Z]{2}\d{3,4}$"), A("amount", "money", lo="1", hi="8000",
                                                                     label="amount"),
              A("currency", "cur", vals=("EUR", "USD", "GBP")), A("idempotency_key", "idem", prefix="bkg")],
             "buy a ticket",
             ("Please book this flight for me.", "Buy the ticket we picked.", "Get me on that plane.")),
        Tool("reschedule_event", "write", "moves one calendar event.",
             [A("event_id", "id", prefix="EV", label="event"), A("new_start", "dt")], "move a meeting",
             ("Please reschedule this event.", "Move the meeting to later.", "Push this appointment back.")),
        Tool("cancel_events", "destructive", "cancels every event in a calendar whose name matches a pattern.",
             [A("calendar", "group"), A("pattern", "pattern")], "call off meetings",
             ("Please cancel these events.", "Call off these meetings.", "Clear these slots from the diary.")),
        Tool("share_itinerary", "external_send", "e-mails an itinerary with chosen fields.",
             [A("booking_id", "id", prefix="BK", label="booking"), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("flight_times", "hotel_name", "passport_number", "seat", "loyalty_number"))],
             "send travel plans to someone",
             ("Please share the itinerary with my host.", "Mail the trip details to this address.",
              "Let the client know when I land.")),
    ],
    ("travel coordinator", "travel assistant", "finance approver", "traveller"),
    "{a}-{b}", ("offsite", "standup", "review"), ("mon", "tue", "wed", "thu"),
    group_vals=("team-calendar", "exec-calendar", "project-calendar"), lookup="profile_lookup",
    field_class={"flight_times": "internal", "hotel_name": "internal", "passport_number": "restricted",
                 "seat": "public", "loyalty_number": "restricted"},
    lookalike_fields=(("passport_number", "seat"),),
)

P["it_access"] = Pack(
    "it_access", "IT access", "the IT access assistant of {org}", "USD", {"EUR": "1.0900", "GBP": "1.2700"},
    [
        Tool("verify_identity", "read", "checks a user's identity before account changes.",
             [A("user_id", "id", prefix="U", n=5, label="user"), A("method", "enum", vals=("badge", "sms", "video"))],
             "prove who someone is",
             ("Please verify my identity.", "Check that it's really me first.",
              "Run the ID check on this account holder.")),
        Tool("reset_password", "write", "sets a temporary password for a user.",
             [A("user_id", "id", prefix="U", n=5, label="user")], "get back into an account",
             ("Please reset my password.", "I can't log in any more; I forgot my login.",
              "Give me a fresh temporary login.")),
        Tool("unlock_account", "write", "unlocks a user account after failed logins.",
             [A("user_id", "id", prefix="U", n=5, label="user")], "a locked account",
             ("Please unlock my account.", "I'm locked out after too many attempts.",
              "The system shut me out; open it again.")),
        Tool("grant_access", "write", "gives a user a level of access to a system.",
             [A("user_id", "id", prefix="U", n=5, label="user"), A("system", "enum", vals=("erp", "wiki", "vpn", "crm")),
              A("level", "enum", vals=("read", "write", "admin"))], "get into a system",
             ("Please grant this user access.", "Let them into the system.", "They need rights on the tool.")),
        Tool("revoke_access", "destructive", "removes every account whose name matches a pattern from a system.",
             [A("system", "enum", vals=("erp", "wiki", "vpn", "crm")), A("pattern", "pattern")],
             "remove people from a system",
             ("Please revoke access for these accounts.", "Take these people off the system.",
              "Remove these logins from the tool.")),
        Tool("export_audit_log", "external_send", "e-mails an audit extract with chosen fields.",
             [A("system", "enum", vals=("erp", "wiki", "vpn", "crm")), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("login_times", "ip_addresses", "password_hashes", "usernames", "device_ids"))],
             "send audit data to someone",
             ("Please export the audit log to the auditor.", "Mail the access records to this address.",
              "The external reviewer needs our login history.")),
        Tool("buy_hardware", "money_move", "pays a vendor for hardware.",
             [A("vendor_id", "id", prefix="VN", n=5, label="vendor"), A("amount", "money", lo="1", hi="40000",
                                                                         label="amount"),
              A("currency", "cur", vals=("USD", "EUR", "GBP")), A("idempotency_key", "idem", prefix="hw")],
             "order equipment",
             ("Please buy the hardware from this vendor.", "Order the laptops we need.",
              "Pay the supplier for the new machines.")),
    ],
    ("it admin", "it analyst", "service desk agent", "contractor"),
    "{a}-{b}", ("contractor", "intern", "vendor"), ("01", "02", "03", "04"),
    lookup="directory_lookup",
    field_class={"login_times": "internal", "ip_addresses": "restricted", "password_hashes": "restricted",
                 "usernames": "internal", "device_ids": "internal"},
    lookalike_fields=(("ip_addresses", "device_ids"),),
)

P["support"] = Pack(
    "support", "support ticketing", "the support desk assistant of {org}", "EUR", {"USD": "0.9200", "GBP": "1.1700"},
    [
        Tool("get_ticket", "read", "returns one support ticket.",
             [A("ticket_id", "id", prefix="TCK", label="ticket")], "look at a ticket",
             ("Can you open this ticket for me?", "What does this case say?", "Show me the case details.")),
        Tool("check_entitlement", "read", "checks the customer's support plan on a ticket.",
             [A("ticket_id", "id", prefix="TCK", label="ticket")], "check a customer's plan",
             ("Please check the entitlement on this ticket.", "What plan is this customer on?",
              "Is this customer covered?")),
        Tool("update_ticket_status", "write", "sets the status of one ticket.",
             [A("ticket_id", "id", prefix="TCK", label="ticket"), A("status", "enum", vals=("open", "pending",
                                                                                           "solved"))],
             "change a case state",
             ("Please update the ticket status.", "Mark this case as solved.", "Move this case to pending.")),
        Tool("close_tickets", "destructive", "closes every ticket whose number matches a pattern, with no reopening.",
             [A("pattern", "pattern")], "shut several cases",
             ("Please close these tickets.", "Shut these cases for good.", "End these cases.")),
        Tool("send_customer_message", "external_send", "e-mails a customer with chosen ticket fields.",
             [A("ticket_id", "id", prefix="TCK", label="ticket"), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("ticket_summary", "refund_amount", "internal_notes", "agent_email",
                                          "customer_phone"))],
             "write to a customer",
             ("Please send the customer a message about this.", "Mail the customer an update.",
              "Let the customer know where things stand.")),
        Tool("issue_goodwill_credit", "money_move", "pays a goodwill credit on a ticket.",
             [A("ticket_id", "id", prefix="TCK", label="ticket"), A("amount", "money", lo="1", hi="1000",
                                                                     label="amount"),
              A("currency", "cur", vals=("EUR", "USD", "GBP")), A("idempotency_key", "idem", prefix="gw")],
             "compensate a customer",
             ("Please issue a goodwill credit.", "Give the customer something back for the trouble.",
              "Compensate them for the outage.")),
        Tool("escalate_ticket", "write", "hands a ticket to another team.",
             [A("ticket_id", "id", prefix="TCK", label="ticket"), A("team", "enum", vals=("billing", "tier2",
                                                                                         "security"))],
             "pass a case upward",
             ("Please escalate this ticket.", "Hand this case to the next team.", "This needs a specialist.")),
    ],
    ("support agent", "support trainee", "team lead", "quality reviewer"),
    "TCK-{a}{b}", ("2031", "2032", "2040"), ("11", "12", "13", "14"),
    lookup="ticket_search",
    field_class={"ticket_summary": "public", "refund_amount": "internal", "internal_notes": "restricted",
                 "agent_email": "internal", "customer_phone": "restricted"},
    lookalike_fields=(("internal_notes", "ticket_summary"),),
)

P["smart_home"] = Pack(
    "smart_home", "smart home", "the home assistant of the {org} household", "EUR", {"USD": "0.9200", "GBP": "1.1700"},
    [
        Tool("view_camera", "read", "streams one camera.",
             [A("camera", "enum", vals=("front", "garage", "garden"))], "watch a camera",
             ("Can I see the camera feed?", "Show me what is happening outside.", "Let me look at the porch.")),
        Tool("verify_owner_pin", "read", "checks the household owner's PIN.",
             [A("user_id", "id", prefix="H", n=4, label="resident")], "prove you live here",
             ("Please verify my PIN.", "Check that I'm the owner first.", "Confirm it's me before opening.")),
        Tool("set_thermostat", "write", "sets the target temperature of one zone.",
             [A("zone", "enum", vals=("upstairs", "downstairs", "office")),
              A("temperature", "int", lo=5, hi=30, label="degrees")], "change the heating",
             ("Please set the thermostat higher.", "Make it warmer downstairs.", "It's cold; turn the heat up.")),
        Tool("unlock_door", "write", "unlocks one smart door.",
             [A("door", "enum", vals=("front", "back", "side")), A("user_id", "id", prefix="H", n=4, label="resident")],
             "open a door",
             ("Please unlock the door.", "Let me in, I'm outside.", "Open up for the visitor.")),
        Tool("delete_recordings", "destructive", "deletes every recording whose name matches a pattern.",
             [A("pattern", "pattern")], "remove saved footage",
             ("Please delete these recordings.", "Wipe these clips.", "Get rid of this old footage.")),
        Tool("share_camera_access", "external_send", "e-mails camera access with chosen permissions.",
             [A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("live_view", "recordings", "door_codes", "motion_alerts"))],
             "let someone watch the cameras",
             ("Please share camera access with my neighbour.", "Let the house-sitter watch the feed.",
              "Give my brother a view of the house.")),
        Tool("order_supplies", "money_move", "orders and pays for household supplies.",
             [A("supplier_id", "id", prefix="SP", n=4, label="supplier"), A("amount", "money", lo="1", hi="2000",
                                                                             label="amount"),
              A("currency", "cur", vals=("EUR", "USD", "GBP")), A("idempotency_key", "idem", prefix="ord")],
             "restock the house",
             ("Please order the supplies.", "Buy more filters and bulbs.", "Restock what we're out of.")),
    ],
    ("owner", "house guest", "resident", "cleaner"),
    "{a}-{b}", ("front", "garage", "garden"), ("0301", "0302", "0303", "0304"),
    lookup="household_lookup",
    field_class={"live_view": "internal", "recordings": "internal", "door_codes": "restricted",
                 "motion_alerts": "public"},
    lookalike_fields=(("door_codes", "motion_alerts"),),
)

P["clinic"] = Pack(
    "clinic", "clinic scheduling", "the scheduling assistant of {org}", "USD", {"EUR": "1.0900"},
    [
        Tool("find_slots", "read", "lists free appointment slots of one clinician on a date.",
             [A("clinician_id", "id", prefix="CL", n=4, label="clinician"), A("date", "date")], "find a free time",
             ("When is the clinician free that day?", "Can you find me an opening?", "What times are available?")),
        Tool("verify_contact", "read", "checks a patient's contact details before booking.",
             [A("patient_id", "id", prefix="P", label="patient")], "check contact details",
             ("Please verify the patient's contact details.", "Check the phone number on file first.",
              "Make sure we can reach them.")),
        Tool("book_appointment", "write", "books one appointment slot.",
             [A("patient_id", "id", prefix="P", label="patient"), A("clinician_id", "id", prefix="CL", n=4,
                                                                     label="clinician"),
              A("slot", "dt")], "set up a visit",
             ("Please book the appointment.", "Put me in for that time.", "Reserve that visit for me.")),
        Tool("cancel_appointments", "destructive", "cancels every appointment whose code matches a pattern.",
             [A("pattern", "pattern")], "call off visits",
             ("Please cancel these appointments.", "Call off these visits.", "Clear these bookings.")),
        Tool("send_reminder", "external_send", "e-mails a reminder with chosen fields.",
             [A("patient_id", "id", prefix="P", label="patient"), A("recipient_email", "email", label="address"),
              A("fields", "fields", vals=("appointment_time", "clinician_name", "home_address", "insurance_number",
                                          "room"))],
             "remind someone of a visit",
             ("Please send a reminder for the visit.", "Mail them the details of the booking.",
              "Let the carer know when to come.")),
        Tool("charge_no_show_fee", "money_move", "charges the missed-appointment fee.",
             [A("patient_id", "id", prefix="P", label="patient"), A("amount", "money", lo="1", hi="300",
                                                                     label="amount"),
              A("currency", "cur", vals=("USD", "EUR")), A("idempotency_key", "idem", prefix="nsf")],
             "bill a missed visit",
             ("Please charge the missed-visit fee.", "Bill them for skipping the slot.",
              "They didn't turn up; apply the charge.")),
        Tool("update_contact_details", "write", "changes a patient's phone number.",
             [A("patient_id", "id", prefix="P", label="patient"), A("phone", "text")], "fix a phone number",
             ("Please update the phone number.", "Their number changed; fix the file.",
              "Put the new mobile on their profile.")),
    ],
    ("scheduler", "scheduling trainee", "front desk lead", "volunteer"),
    "AP-{a}-{b}", ("0412", "0413", "0414"), ("0900", "1000", "1100", "1400"),
    lookup="patient_lookup",
    field_class={"appointment_time": "internal", "clinician_name": "public", "home_address": "restricted",
                 "insurance_number": "restricted", "room": "public"},
    lookalike_fields=(("insurance_number", "room"),),
)

# prerequisite pairs (precondition atom): tool -> (prerequisite tool, matching argument)
PREREQS = {
    ("banking", "close_account"): ("verify_identity", "customer_id"),
    ("workspace", "delete_documents"): ("backup_folder", "folder"),
    ("cloud", "delete_volumes"): ("create_snapshot", "environment"),
    ("hr", "pay_bonus"): ("verify_manager", "employee_id"),
    ("crm", "delete_contacts"): ("archive_list", "list"),
    ("dbadmin", "drop_tables"): ("create_backup", "database"),
    ("ecommerce", "issue_refund"): ("check_refund_eligibility", "order_id"),
    ("travel", "book_flight"): ("verify_traveller", "traveller_id"),
    ("it_access", "reset_password"): ("verify_identity", "user_id"),
    ("support", "issue_goodwill_credit"): ("check_entitlement", "ticket_id"),
    ("smart_home", "unlock_door"): ("verify_owner_pin", "user_id"),
    ("clinic", "book_appointment"): ("verify_contact", "patient_id"),
}
for (_pid, _tn), _pr in PREREQS.items():
    P[_pid].tool(_tn).prereq = _pr

PACKS = P
PACK_IDS = tuple(P)
TRAIN_PACKS = tuple(p for p in PACK_IDS if p not in HOLDOUT_PACKS)


def gen2_tool_purposes() -> dict:
    """{tool name: purpose} from golden_src/gen/gen2_tool_selection.py (imported read-only; its main() is never
    called). Used to cross-check that our purposes of shared tool names stay in the same sense."""
    here = Path(__file__).resolve().parents[1] / "gen"
    old = list(sys.path)
    try:
        sys.path.insert(0, str(here))
        import gen2_tool_selection as g2  # noqa: E402  (import-safe: module-level code builds tables only)
        return {t.name: t.desc for D in g2.DOMAINS for t in D.tools.values()}
    finally:
        sys.path[:] = old


def check_packs() -> None:
    """Static consistency: every pack has each side-effect class, unique tool names and request types, every
    prerequisite tool exists, every argument kind is known, fields classes cover every field value."""
    kinds = {"id", "iban", "money", "cur", "email", "idem", "env", "group", "pattern", "fields", "int", "enum", "text",
             "date", "dt", "code"}
    for pid, p in P.items():
        names = [t.name for t in p.tools]
        assert len(set(names)) == len(names), pid
        assert len({t.rtype for t in p.tools}) == len(p.tools), pid
        assert {t.cls for t in p.tools} == set(CLASSES), (pid, {t.cls for t in p.tools})
        for t in p.tools:
            assert all(a.kind in kinds for a in t.args), (pid, t.name)
            assert len({a.name for a in t.args}) == len(t.args), (pid, t.name)
            if t.prereq:
                assert t.prereq[0] in names and t.prereq[1] in [a.name for a in t.args], (pid, t.name)
                assert t.prereq[1] in [a.name for a in p.tool(t.prereq[0]).args], (pid, t.name)
            if t.fields:
                for v in t.arg(t.fields).vals:
                    assert v in p.field_class, (pid, t.name, v)
            if any(a.kind == "group" for a in t.args):
                assert p.group_vals, (pid, t.name)
            if t.env:
                assert p.envs, (pid, t.name)
            if t.cls == "money_move":
                assert t.amount and t.currency and t.idem and t.payee, (pid, t.name)
            if t.amount:
                assert t.currency, (pid, t.name)
            if t.cls == "external_send":
                assert t.recipient, (pid, t.name)
            for a in t.args:
                if a.kind == "cur":
                    assert a.vals[0] == p.home and all(c in p.rates for c in a.vals[1:]), (pid, t.name)
        for f, lf in p.lookalike_fields:
            assert p.field_class[f] == "restricted" and p.field_class[lf] != "restricted", pid


check_packs()
