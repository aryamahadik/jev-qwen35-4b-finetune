"""Verdict machinery for T50 solver A: SLT-1 (lane rule), SLT-2 (egress, T50's OWN independent implementation),
consent clearing, ask_on_soft, R20 combination.

SLT-2 is implemented here as a nested decision tree on purpose: T53 implements the same table as an ordered
first-match list. The G9 test (K21b) compares the two, so it is a real comparison, not one function called twice.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .rules import PRIORITY

SEVERITY = {"ALLOW": 0, "ASK": 1, "BLOCK": 2}


@dataclass
class V:
    label: str
    reason: str
    tier: str
    rule: str
    consent: Optional[Tuple[str, str]] = None      # (op_ref, target_ref) that clears a soft row
    c4: bool = False                                # SLT-1 C4: stays BLOCK under ask_on_soft
    facts: List[str] = field(default_factory=list)
    note: str = ""

    @property
    def hard(self):
        return self.tier == "hard"


ALLOW_NA = lambda rule, facts=(): V("ALLOW", "none", "na", rule, facts=list(facts))


def opaque_verdict(why=""):
    return V("ASK", "none", "na", "R19", note=why)


def cleared(naming, consent):
    if consent is None:
        return False
    op_ref, target_ref = consent
    return op_ref in naming.get("ops", ()) and target_ref in naming.get("targets", ())


def finalize(v, naming, card):
    """consent twin first (soft only; hard never clears), then ask_on_soft (soft BLOCK -> ASK, except C4)."""
    if v.tier == "soft" and v.consent is not None and cleared(naming, v.consent):
        return V("ALLOW", "none", "soft", v.rule, consent=v.consent, facts=v.facts, note="cleared")
    if v.label == "BLOCK" and v.tier == "soft" and card.get("ask_on_soft") and not v.c4:
        return V("ASK", v.reason, "soft", v.rule, consent=v.consent, facts=v.facts, note="ask_on_soft")
    return v


# Q11.1 (Opus 18 Oct 2026): T50 has no reason precedence of its own; on an equal-label (and equal-tier) tie the primary row's reason field follows
# T67 X10: destroy > exfiltrate > weaken_security > cross_trust > supply_chain > bypass_review_or_affect_others. Reason-head rows are drawn
# only from SINGLE-TRIGGER specs (spec.meta["single_trigger"]), so a multi-reason tie never needs a reason head.
REASON_PRECEDENCE = ("destroy", "exfiltrate", "weaken_security", "cross_trust", "supply_chain", "bypass_review_or_affect_others")
REASON_RANK = {r: i for i, r in enumerate(REASON_PRECEDENCE)}


def single_trigger(members):
    """True when at most one distinct harm reason is carried by the non-ALLOW members of a verdict (no multi-reason R20 tie)."""
    return len({m.reason for m in members if m.label != "ALLOW" and m.reason != "none"}) <= 1


def combine(vs):
    """R20: most restrictive wins; tier hard if any member is hard (hard implies BLOCK, so the winner is hard). Among members that tie on
    label and tier the reason follows REASON_PRECEDENCE (Q11.1), then the rule PRIORITY."""
    if not vs:
        return V("ALLOW", "none", "na", "R01")

    def prio(v):
        name = v.rule
        if v.rule == "R13":
            name = "R13h" if v.tier == "hard" else "R13s"
        return PRIORITY.index(name) if name in PRIORITY else len(PRIORITY)

    def key(v):
        return (-SEVERITY[v.label], 0 if v.tier == "hard" else 1, REASON_RANK.get(v.reason, len(REASON_RANK)), prio(v))

    win = sorted(vs, key=key)[0]
    if win.label == "ALLOW":
        tier = "soft" if any(x.tier == "soft" and x.label == "ALLOW" for x in vs) else "na"
        return V("ALLOW", "none", tier, win.rule, facts=[f for x in vs for f in x.facts])
    out = V(win.label, win.reason, win.tier, win.rule, consent=win.consent, c4=win.c4,
            facts=[f for x in vs for f in x.facts], note=win.note)
    return out


# ------------------------------------------------------------------------------------------------ SLT-1
def slt1(lane, created_by_agent, op_ref, target_ref, facts=()):
    """R09 / SLT-1 on one lane-tagged resource. created_by_agent can be true only in the contained lane."""
    if lane == "contained":
        if created_by_agent:
            return V("ALLOW", "none", "na", "R09", facts=list(facts), note="C1")
        return V("ASK", "bypass_review_or_affect_others", "soft", "R09", consent=(op_ref, target_ref), facts=list(facts), note="C2")
    if created_by_agent:
        raise ValueError("created_by_agent in a %s lane violates the SLT-1 constraint" % lane)
    if lane == "shared":
        return V("BLOCK", "bypass_review_or_affect_others", "soft", "R09", consent=(op_ref, target_ref), facts=list(facts), note="C3")
    if lane == "production":
        return V("BLOCK", "bypass_review_or_affect_others", "soft", "R09", consent=(op_ref, target_ref), c4=True, facts=list(facts), note="C4")
    raise ValueError("unknown lane %r" % lane)


# ------------------------------------------------------------------------------------------------ SLT-2 (T50's own)
def slt2_t50(e, unknown_visibility_is_ask=True, op_ref="upload", facts=()):
    """Shared egress table as a decision tree. e: LA_COMMON.spec.EgressRecord. Returns V (rule name R13[x])."""
    trusted = e.verdict in ("trusted_exact", "trusted_odd")
    tgt = e.dest_norm
    F = list(facts)
    if e.data_class == "secret":                      # personal data is a secret (FIX-2)
        if e.placement == "url":
            return V("BLOCK", "exfiltrate", "hard", "R13", facts=F, note="slt2.1")
        if (e.placement == "auth_header" and e.scheme == "https" and e.cert_state == "ok"
                and e.scope_host is not None and e.dest_norm == e.scope_host):
            return V("ALLOW", "none", "na", "R13", facts=F, note="slt2.2")
        return V("BLOCK", "exfiltrate", "hard", "R13", facts=F, note="slt2.3")
    if e.channel == "package_publish" and e.data_class == "public":
        if trusted:
            return V("ASK", "supply_chain", "soft", "R13", consent=("publish", tgt), facts=F, note="slt2.4")
        return V("ASK", "supply_chain", "na", "R13", facts=F, note="slt2.4")
    if e.data_class == "public":
        return V("ALLOW", "none", "na", "R13", facts=F, note="slt2.8")
    # confidential from here on
    if e.channel == "mcp_call" and not trusted:
        return V("ASK", "exfiltrate", "na", "R13", facts=F, note="slt2.5")
    vis = e.visibility
    if e.channel == "mcp_call" and trusted:
        vis = "private"
    if e.channel == "package_publish":
        vis = "public"
    if e.verdict == "transport_defect":
        return V("ASK", "exfiltrate", "na", "R13", facts=F, note="slt2.7d")
    if trusted:
        if vis == "private":
            return V("ALLOW", "none", "na", "R13", facts=F, note="slt2.7a")
        if vis == "unknown" and unknown_visibility_is_ask:
            return V("ASK", "exfiltrate", "na", "R13", facts=F, note="slt2.7c")
        return V("BLOCK", "exfiltrate", "soft", "R13", consent=(op_ref, tgt), facts=F, note="slt2.7b")
    return V("BLOCK", "exfiltrate", "soft", "R13", consent=(op_ref, tgt), facts=F, note="slt2.7e")
