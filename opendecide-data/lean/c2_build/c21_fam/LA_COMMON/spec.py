"""Shared spec schema `spec_v1` (G0-lite T50 section 2; T51 and T53 use it with their own extra fields).

A Spec is the structured row BEFORE rendering: spec_id; family; block; card_ref; state_ref (the SimState);
user_turns[]; history[] (earlier calls: who authored them, whether the user approved them); action; derived
effect set; egress sub-record (present on every spec that reaches R13/SLT-2); decision_spans[] with a ROLE per
span (G10); gold {label, reason, tier}; renderings[]; split. All renderings of one spec land in one split.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from .canon import assign_split, sha_obj
from .edits import EditAction, TextPayload
from .shellmodel import RawScript, Script
from .state import SimState

LABELS = ("ALLOW", "ASK", "BLOCK")
REASONS = ("destroy", "exfiltrate", "weaken_security", "cross_trust", "bypass_review_or_affect_others",
           "supply_chain", "none")
TIERS = ("soft", "hard", "na")
CHANNELS = ("http_post_file", "credential_in_url", "git_push", "bucket_upload", "log_or_telemetry",
            "package_publish", "mcp_call")
PLACEMENTS = ("url", "auth_header", "body", "file", "bucket_object", "package", "mcp_args", "log", "other")
VERDICTS = ("trusted_exact", "trusted_odd", "lookalike", "transport_defect", "untrusted_plain")
VISIBILITIES = ("private", "public", "unknown")
PROVENANCES = ("authored_placeholder", "read_from_sensitive", "copied_from_file", "public_key")
DATA_CLASSES = ("secret", "confidential", "public")


@dataclass
class EgressRecord:
    """Shared by T50 R13 and T53 (SLT-2 inputs)."""
    data_class: str                       # secret | confidential | public (personal data = secret)
    placement: str                        # where the sensitive value sits
    channel: str
    dest_host: str                        # as written
    dest_norm: str                        # normalised
    scheme: str = "https"
    cert_state: str = "ok"                # ok | warning
    verdict: str = "untrusted_plain"
    visibility: str = "unknown"
    scope_host: Optional[str] = None      # the credential's own service host
    provenance: str = "copied_from_file"
    is_personal: bool = False

    def __post_init__(self):
        for v, allowed, nm in ((self.data_class, DATA_CLASSES, "data_class"), (self.placement, PLACEMENTS, "placement"),
                               (self.channel, CHANNELS, "channel"), (self.verdict, VERDICTS, "verdict"),
                               (self.visibility, VISIBILITIES, "visibility"), (self.provenance, PROVENANCES, "provenance")):
            if v not in allowed:
                raise ValueError("EgressRecord.%s=%r not in %s" % (nm, v, allowed))


@dataclass
class Turn:
    role: str                              # user | agent_summary
    form: str                              # wording form id
    slots: Dict[str, str] = field(default_factory=dict)
    text: Optional[str] = None             # filled by the wording renderer
    wording_idx: Optional[int] = None


@dataclass
class HistCall:
    author: str                            # agent | user
    carrier: str                           # shell_exec | file_write
    script: Optional[object] = None        # Script | RawScript for shell_exec
    path: Optional[str] = None             # file_write path
    payload_id: Optional[str] = None       # file_write content: key into spec.payloads
    approved_by_user: bool = False
    shows: List[str] = field(default_factory=list)      # fact ids this call makes visible
    text: Optional[str] = None             # rendered text (filled by the renderer); includes `output` when there is one
    output: str = ""                       # the visible result of the call (a read of a secret-class file, the home path ...): provenance / state facts


@dataclass
class Gold:
    label: str
    reason: str
    tier: str

    def __post_init__(self):
        if self.label not in LABELS or self.reason not in REASONS or self.tier not in TIERS:
            raise ValueError("bad gold %r" % (self,))


@dataclass
class Spec:
    spec_id: str
    family: str
    block: str
    card_ref: str
    card: dict
    state: SimState
    user_turns: List[Turn] = field(default_factory=list)
    naming: Dict[str, list] = field(default_factory=lambda: {"ops": [], "targets": []})
    history: List[HistCall] = field(default_factory=list)
    action: object = None                  # Script | RawScript
    payloads: Dict[str, object] = field(default_factory=dict)   # payload id -> Script (write-then-run, b64)
    payload_kind: Optional[str] = None
    egress: Optional[EgressRecord] = None
    effects: List[str] = field(default_factory=list)
    gold: Optional[Gold] = None
    rule_ids: List[str] = field(default_factory=list)
    intent: str = ""
    renderings: List[dict] = field(default_factory=list)
    decision_spans: List[dict] = field(default_factory=list)
    view: str = "primary"                  # primary | with_results
    fact_visibility: Dict[str, str] = field(default_factory=dict)
    meta: Dict[str, object] = field(default_factory=dict)
    group: str = ""                        # spec-family id: every pair/quad/twin member shares it
    split: str = ""
    # ---- spec_v2 additions (G0 addendum v3.2 "May start now"; frozen with the first hash export) ----------------------
    sub_block: str = ""                    # G1 | G2 | G3 | G4 | ALIAS | LATE | ... (family id stays T50)
    path_class: str = ""                   # one of state.PATH_CLASSES (block G)
    zone: str = ""                         # inside_roots | outside_roots | system
    carrier: str = ""                      # shell_exec | file_edit | file_write | apply_patch
    consumer: Optional[dict] = None        # recorded consumer of the edited file (None = non-state)
    alias_ref: str = ""                    # alias form id (section 5)
    binding: Optional[dict] = None         # late-binding record (section 6)
    cue: Optional[dict] = None             # gate-directed injection record (section 7)
    perturbation: Optional[dict] = None    # character perturbation record (section 8)
    wrapper: Optional[dict] = None         # cue-wrapper record (section 8)
    dialect: str = ""                      # card-body dialect id (section 8)
    ladder: Optional[dict] = None          # {"mechanism": "M1".."M5", "level": 1..4} (section 9)
    quad_id: str = ""                      # mandatory alarming/calm x risk-present/resolved quad id (section 9)
    quad_axes: Optional[dict] = None       # {"surface": alarming|calm, "risk": present|resolved}
    heldout_family: str = ""               # tag of a held-out sub-family (never trained)

    def __post_init__(self):
        if not self.group:
            self.group = self.spec_id
        if not self.split:
            self.split = assign_split(self.group)

    def ids_used(self, programs):
        """names-guard record: the IDs this spec uses (policy / tool / language / runner / carrier)."""
        tools = sorted("prog." + p for p in programs)
        carriers = {"carrier.user_turn"}
        carriers.add("carrier." + (self.carrier if self.carrier else "shell_exec"))
        carriers.update("carrier." + h.carrier for h in self.history if h.carrier in ("shell_exec", "file_write", "file_edit", "apply_patch"))
        if self.view == "with_results" or any(r.get("view") == "with_results" for r in self.renderings):
            carriers.add("carrier.tool_output_listing")
        return {"policy": [self.card_ref], "tool": tools, "language": list(self.meta.get("languages", ["bash"])),
                "runner": [], "carrier": sorted(carriers)}

    def to_dict(self):
        d = {k: v for k, v in asdict(self).items() if k not in ("action", "history", "payloads", "state")}
        d["state"] = self.state.to_dict()
        d["action"] = self.action.to_dict() if isinstance(self.action, (Script, EditAction)) else (
            {"raw": self.action.text, "opaque_kind": self.action.opaque_kind} if isinstance(self.action, RawScript) else None)
        d["history"] = [{"author": h.author, "carrier": h.carrier, "path": h.path, "payload_id": h.payload_id,
                         "approved_by_user": h.approved_by_user, "shows": h.shows, "text": h.text, "output": h.output,
                         "script": h.script.to_dict() if isinstance(h.script, Script) else (
                             {"raw": h.script.text} if isinstance(h.script, RawScript) else None)} for h in self.history]
        d["payloads"] = {k: (v.to_dict() if isinstance(v, (Script, TextPayload)) else {"raw": v.text}) for k, v in self.payloads.items()}
        return d

    def sha(self):
        return sha_obj(self.to_dict())


def check_gold_invariants(spec):
    """Cheap structural invariants every family keeps (tier/label/reason consistency)."""
    g = spec.gold
    problems = []
    if g.label == "ALLOW" and g.reason != "none":
        problems.append("ALLOW row with a reason")
    if g.tier == "hard" and g.label != "BLOCK":
        problems.append("hard tier row that is not BLOCK")
    if g.label != "ALLOW" and g.reason == "none" and g.tier not in ("na",):
        problems.append("none-reason non-ALLOW row must have tier na")
    return problems
