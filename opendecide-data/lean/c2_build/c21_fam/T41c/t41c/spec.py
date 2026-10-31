"""Row spec and the attack/benign tuple schema (G0-lite section 2, D2).

A row is a structured spec. The label is a pure function of the spec (table.py). Text is realised from the spec
(render.py) with Claude-authored wording pools; the program writes everything else.

Attack/benign tuple (D2), per directive:
  (user task class, authority set = {source tag, nested, declared_policy}, carrier type, carrier format,
   placement bin, directive class, wrapper style, channel visibility, delegation mode, necessary flag,
   risk record = the Action, nested, declared_policy, agent_directed)
"""
import json
from dataclasses import dataclass
from typing import Optional, Tuple

from . import ids
from .table import Action, DirFacts, Facts, Send, resolve_env, row_label, is_necessary


@dataclass(frozen=True)
class Pointer:
    """Delegation pointer in the user task. delegated(d) needs the pointer to reach d's carrier (and d's step for a
    step pointer). A pointer that names a different source exists in some rows on purpose (not delegated)."""
    mode: str = "deleg.none"
    points_at_carrier: bool = False
    steps: Tuple[str, ...] = ()          # directive ids named by a step pointer (empty = every step)

    def covers(self, did: str) -> bool:
        if self.mode == "deleg.none" or not self.points_at_carrier:
            return False
        if self.mode == "deleg.source_pointer":
            return True
        return (not self.steps) or did in self.steps


@dataclass(frozen=True)
class Fill:
    """A neutral filler slot (clean twin / off-topic noise). It carries the same slot-level attributes as a directive
    slot (placement, length bucket, wrapper style, hidden variant, visibility, chunks) so those attributes are
    label-neutral by construction."""
    kind: str = "fill"                    # fill | noise
    placement: str = "place.p2"
    bucket: int = 1
    wrapper: str = "wrap.plain_imperative"
    hidden: Optional[str] = None
    visibility: str = "vis.agent_only"
    chunks: int = 1


@dataclass(frozen=True)
class Directive:
    did: str
    cls: str                              # goal.* | ben.* | men.*
    action: Optional[Action]              # None only for non-agent-directed (men.*) content
    agent_directed: bool
    wrapper: str = "wrap.plain_imperative"
    hidden: Optional[str] = None          # hid.* when wrapper == wrap.hidden
    placement: str = "place.p2"
    visibility: str = "vis.agent_only"
    nested: bool = False
    declared_policy: bool = False
    in_scope: bool = False
    concerns_tool: Optional[str] = None   # MCP rule
    claims_necessity: bool = False        # text-only cue; never changes a label
    claims_authority: bool = False        # text-only cue; never changes a label
    variant: str = ""                     # pools.VARIANTS variant id (or "" for men.*)
    slots: Tuple[Tuple[str, str], ...] = ()   # concrete slot values (path, host, package, ...) used by the wording
    slot_bucket: int = 1                  # slot-length bucket 0..3 (pools.SLOT_BUCKETS); shared by a pair group
    chunks: int = 1                       # number of consecutive slot items (>1 only for hid.split_chunks)

    def slotdict(self):
        return dict(self.slots)


@dataclass(frozen=True)
class Spec:
    row_id: str
    block: str                            # train | ho | bd | ls
    group_id: str
    pair_kind: str                        # single | triple | splice | taskedit
    pair_role: str                        # single | clean | benign | attack | a | b | edit_a | edit_b
    subtype: str                          # sub.* (for attack rows: the att./ask. bucket)
    task_class: str
    pointer: Pointer
    task_mentions: Tuple[str, ...]        # which of target / branch / mcp_tool the user turn names (subset)
    carrier_type: str
    carrier_format: str
    carrier_src: str
    facts: Facts
    directives: Tuple[Directive, ...]
    art_seed: str                         # same value across a pair group's artifact
    len_target: int = 1                   # carrier length bucket target 0..2 (55/30/15 mix)
    carrier_tool: Optional[str] = None    # mcp_* carriers: the tool the span belongs to
    code_lang: Optional[str] = None       # code_comment carriers: ids.LANGS member
    declared_policy_file: bool = False    # a system/developer span names the carrier as the project rules file
    has_nested_span: bool = False         # a vendored third-party block exists elsewhere in the carrier (no directive)
    vendor_slot: bool = False             # slot 0 sits inside a vendored third-party block (nested provenance skeleton)
    fills: Tuple[Fill, ...] = ()          # neutral filler slots (rows without directives; extra slots in multi-slot rows)
    seed: int = 0
    note: str = ""

    # ---- derived ---------------------------------------------------------------------------------------------
    def dir_facts(self, d: Directive) -> DirFacts:
        return DirFacts(
            agent_directed=d.agent_directed, action=d.action,
            delegated=self.pointer.covers(d.did),
            necessary=bool(d.agent_directed and is_necessary(self.task_class, d.cls)),
            nested=d.nested, declared_policy=d.declared_policy, in_scope=d.in_scope,
            src_tag=self.carrier_src, concerns_tool=d.concerns_tool, carrier_tool=self.carrier_tool)

    def env(self):
        return resolve_env(self.facts)

    def facts_flag(self) -> str:
        return ids.FACTS_PRESENT if self.facts.present else ids.FACTS_ABSENT


def solve_a(spec: Spec):
    """SOLVER A: (label, per-directive results). Pure function of the spec."""
    return row_label([spec.dir_facts(d) for d in spec.directives], spec.env())


def label_of(spec: Spec) -> str:
    return solve_a(spec)[0]


def validate_spec(spec: Spec):
    """Structural checks that do not need text. Returns a list of violation strings (empty = valid)."""
    bad = []
    if spec.task_class not in ids.TASK_CLASSES:
        bad.append("bad task_class")
    if spec.carrier_type not in ids.CARRIER_TYPES:
        bad.append("bad carrier_type")
    elif spec.carrier_format not in ids.CARRIER_FORMATS[spec.carrier_type]:
        bad.append("format not available for carrier type")
    if spec.carrier_type in ids.CARRIER_SOURCES and spec.carrier_src not in ids.CARRIER_SOURCES[spec.carrier_type]:
        bad.append("source tag not allowed for carrier type")
    if spec.pointer.mode not in ids.DELEG_MODES:
        bad.append("bad delegation mode")
    if spec.len_target not in (0, 1, 2, 3) or (spec.len_target == 3 and spec.block != "ls"):
        bad.append("bad len_target (3 is the eval-only LS block)")
    dids = set()
    for d in spec.directives:
        if d.did in dids:
            bad.append("duplicate did")
        dids.add(d.did)
        if d.agent_directed:
            if d.action is None:
                bad.append("agent-directed directive %s has no action" % d.did)
            else:
                try:
                    d.action.validate()
                except ValueError as e:
                    bad.append("action %s: %s" % (d.did, e))
                if d.action.tool_role not in ids.TOOL_ROLES:
                    bad.append("bad tool role")
                if d.action.shared_prod and not spec.facts.lane_tag:
                    bad.append("shared_prod without a lane-tag anchor (R2-T41c-b)")
            if d.cls not in ids.GOAL_CLASSES and d.cls not in ids.BENIGN_CLASSES:
                bad.append("agent-directed class must be goal.* or ben.*: %s" % d.cls)
        else:
            if d.cls not in ids.MENTION_CLASSES:
                bad.append("non-agent-directed class must be men.*: %s" % d.cls)
            if d.action is not None:
                bad.append("non-agent-directed directive carries an action")
        if d.wrapper not in ids.WRAPPERS:
            bad.append("bad wrapper")
        if (d.wrapper == "wrap.hidden") != (d.hidden is not None):
            bad.append("hidden variant iff wrap.hidden")
        if d.hidden is not None and d.hidden not in ids.HIDDEN_VARIANTS:
            bad.append("bad hidden variant")
        if d.placement not in ids.PLACEMENTS:
            bad.append("bad placement")
        if d.visibility not in ids.VISIBILITY:
            bad.append("bad visibility")
        if d.nested != (spec.vendor_slot and d.did == spec.directives[0].did):
            bad.append("nested iff slot 0 is vendored")
        if d.nested and spec.carrier_type not in ids.NESTABLE_CARRIERS:
            bad.append("nested directive in a carrier that cannot quote vendored text")
        if d.nested and spec.carrier_src != ids.SRC_USER_FILE:
            bad.append("nested provenance needs a user-owned file carrier")
        if d.declared_policy and not spec.declared_policy_file:
            bad.append("declared_policy directive without a policy-naming system span")
        # rule 5 "in scope": solver B can only read it as "a benign project step (ben.*) inside the declared rules file"
        # (the row schema carries no in_scope anchor), so the spec may not hold a combination B cannot represent
        if d.agent_directed and d.declared_policy and (d.in_scope != d.cls.startswith("ben.")):
            bad.append("declared_policy directive: in_scope must equal (class is ben.*)")
        if (d.concerns_tool is not None) and spec.carrier_src not in (ids.SRC_MCP_DESC, ids.SRC_MCP_RESP):
            bad.append("concerns_tool set outside an mcp carrier")
    if spec.carrier_src in (ids.SRC_MCP_DESC, ids.SRC_MCP_RESP) and spec.carrier_tool is None:
        bad.append("mcp carrier without carrier_tool")
    if spec.declared_policy_file and not (spec.carrier_type == "car.rules_file" and spec.carrier_src == ids.SRC_USER_FILE):
        bad.append("declared_policy_file only on a user-owned rules file")
    if spec.code_lang is not None and (spec.code_lang not in ids.LANGS or spec.carrier_type != "car.code_comment"):
        bad.append("code_lang only for code_comment, from ids.LANGS")
    if spec.carrier_type == "car.code_comment" and spec.code_lang is None:
        bad.append("code_comment needs a code_lang")
    if len(spec.directives) > 2:
        bad.append("more than two directives")
    if not spec.directives and not spec.fills:
        bad.append("a row needs a slot (directive or filler)")
    if spec.vendor_slot and spec.carrier_type not in ids.NESTABLE_CARRIERS:
        bad.append("vendor_slot in a carrier that cannot quote vendored text")
    if spec.vendor_slot and spec.carrier_src != ids.SRC_USER_FILE:
        bad.append("vendor_slot needs a user-owned file carrier")
    for fl in spec.fills:
        if (fl.placement not in ids.PLACEMENTS or fl.bucket not in range(4) or fl.chunks < 1
                or fl.kind not in ("fill", "noise") or fl.wrapper not in ids.WRAPPERS
                or (fl.wrapper == "wrap.hidden") != (fl.hidden is not None)):
            bad.append("bad fill %r" % (fl,))
    # facts-absent rows must still show every anchor the defaults read (9.1): the facts object must carry them
    f = spec.facts
    if not f.repo_root:
        bad.append("no repo root")
    return bad


def spec_to_json(spec: Spec) -> str:
    def enc(o):
        if hasattr(o, "__dataclass_fields__"):
            return {k: enc(getattr(o, k)) for k in o.__dataclass_fields__}
        if isinstance(o, (tuple, list)):
            return [enc(x) for x in o]
        return o
    return json.dumps(enc(spec), sort_keys=True, separators=(",", ":"))


def spec_from_json(s: str) -> Spec:
    o = json.loads(s)

    def act(a):
        if a is None:
            return None
        a = dict(a)
        sd = a.pop("send")
        send = Send(**sd) if sd else None
        for k in ("delete_paths", "overwrite_paths", "targets"):
            a[k] = tuple(a[k])
        return Action(send=send, **a)

    def facts(f):
        f = dict(f)
        for k, v in list(f.items()):
            if isinstance(v, list):
                f[k] = tuple(v)
        return Facts(**f)

    ptr = o["pointer"]
    def d_(d):
        d = dict(d)
        d["action"] = act(d["action"])
        d["slots"] = tuple(tuple(x) for x in d["slots"])
        return Directive(**d)
    dirs = tuple(d_(d) for d in o["directives"])
    fills = tuple(Fill(**x) for x in o["fills"])
    return Spec(**{**o, "pointer": Pointer(ptr["mode"], ptr["points_at_carrier"], tuple(ptr["steps"])),
                   "facts": facts(o["facts"]), "directives": dirs, "fills": fills,
                   "task_mentions": tuple(o["task_mentions"])})
