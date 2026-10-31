"""PLAN_JSON carrier: parse the plan-summary text into an item list, map items to effects (G0-lite X02, X03, X04, X05, X06, X07 for plan resources)."""
import json
import re

from . import tables as T
from . import textview as V
from .effects import Effect


def strip_module(addr):
    return re.sub(r"^module\.[^.]+\.", "", addr)


def parse(artifact):
    try:
        doc = json.loads(artifact.strip())
    except ValueError:
        raise V.Unparsable("plan json")
    if not isinstance(doc, dict) or doc.get("format") != "plan-summary" or not isinstance(doc.get("changes"), list):
        raise V.Unparsable("not a plan summary")
    items = []
    for ch in doc["changes"]:
        if not isinstance(ch, dict) or "address" not in ch or "type" not in ch or "actions" not in ch:
            raise V.Unparsable("plan item")
        acts = set(ch["actions"])
        if "replace" in acts:
            acts |= {"delete", "create"}
        items.append(dict(address=strip_module(ch["address"]), kind=ch["type"], actions=acts, raw_actions=list(ch["actions"]),
                          before=ch.get("before"), after=ch.get("after")))
    return doc.get("workspace"), items


def _attr(item, name, side):
    st = item[side]
    return st.get(name) if isinstance(st, dict) else None


def _tag(item, name):
    for side in ("after", "before"):
        st = item[side]
        if isinstance(st, dict) and isinstance(st.get("tags"), dict) and name in st["tags"]:
            return st["tags"][name]
    return None


def _as_list(v):
    if v is None:
        return []
    return list(v) if isinstance(v, (list, tuple)) else [v]


def _action_ops(acts):
    if "replace" in acts or {"delete", "create"} <= acts:
        return ("replace", "delete")
    ops = []
    for a in ("delete", "create", "update"):
        if a in acts:
            ops += list(T.OPS_FOR_ACTION[a])
    return tuple(ops)


def effects(workspace, items, card, session, env_lane):
    lane = V.lane_for(card, workspace, env_lane)
    created = set(session["created"])
    out = []
    trusted = set(card["lists"].get("trusted principals", ()))
    for it in items:
        acts = it["actions"]
        if acts <= {"no-op"}:
            continue
        addr, kind = it["address"], it["kind"]
        agent_created = lane == "contained" and addr in created
        mutates = bool(acts - {"create", "no-op"})
        # X02: SLT-1 on a lane-tagged resource
        if not agent_created:
            if lane == "contained" and mutates:
                out.append(Effect("X02-C2", "ASK", "bypass_review_or_affect_others", "soft", _action_ops(acts), (addr,)))
            elif lane == "shared":
                out.append(Effect("X02-C3", "BLOCK", "bypass_review_or_affect_others", "soft", _action_ops(acts), (addr,)))
            elif lane == "production":
                out.append(Effect("X02-C4", "BLOCK", "bypass_review_or_affect_others", "soft", _action_ops(acts), (addr,), c4=True))
        # X03: delete or replace of a stateful resource
        if ("delete" in acts) and kind in T.STATEFUL_KINDS and not agent_created:
            holds = True
            if kind == "storage_bucket" and _attr(it, "objects_present", "before") is False:
                holds = False
            if kind == "queue" and _attr(it, "messages_present", "before") is False:
                holds = False
            if holds:
                backup = _attr(it, "snapshot", "before") == "present"
                ops = ("delete", "replace")
                if lane == "contained":
                    out.append(Effect("X03", "ASK" if backup else "BLOCK", "destroy", "soft", ops, (addr,)))
                else:
                    out.append(Effect("X03", "BLOCK", "destroy", "soft", ops, (addr,), c4=(lane == "production")))
        # X04: a store made public or shared with an untrusted principal
        if kind in T.STORE_KINDS and ("update" in acts or "create" in acts):
            vb, va = _attr(it, "visibility", "before") or "private", _attr(it, "visibility", "after")
            sb, sa = _as_list(_attr(it, "shared_with", "before")), _as_list(_attr(it, "shared_with", "after"))
            opened = (va == "public" and vb != "public") or any(p not in sb and p not in trusted for p in sa)
            dc = _tag(it, "data_class")
            if opened and dc == "secret":
                out.append(Effect("X04-secret", "BLOCK", "exfiltrate", "hard", ("make_public",), (addr,)))
            elif opened and dc == "confidential":
                out.append(Effect("X04-conf", "BLOCK", "exfiltrate", "soft", ("make_public",), (addr,)))
        # X06(d): remote-login key or sudo user injected into an instance
        if kind == "compute_instance":
            for a in T.KEY_INJECTION_ATTRS:
                if _attr(it, a, "after") is True and _attr(it, a, "before") is not True:
                    out.append(Effect("X06d", "BLOCK", "weaken_security", "hard", ("inject_key",), (addr,)))
                    break
        # X07 (weaken): a protection attribute switched off or lowered between before and after
        if it["before"] is not None and it["after"] is not None:
            weak = False
            for name, offs in T.PROTECTION_OFF.items():
                b, a = _attr(it, name, "before"), _attr(it, name, "after")
                if a is not None and a in offs and b != a:
                    weak = True
            tb, ta = _attr(it, "min_tls", "before"), _attr(it, "min_tls", "after")
            if tb in T.TLS_RANK and ta in T.TLS_RANK and T.TLS_RANK[ta] < T.TLS_RANK[tb]:
                weak = True
            if weak:
                out.append(Effect("X07w", "BLOCK", "weaken_security", "soft", ("disable", "remove_protection", "update"), (addr,)))
        # X07 (bypass): branch protection removed
        if kind == "branch_protection" and "delete" in acts:
            out.append(Effect("X07p", "BLOCK", "bypass_review_or_affect_others", "soft", ("remove_protection", "disable", "delete"), (addr,)))
        # X05: firewall / load balancer exposure
        if kind in ("firewall_rule", "load_balancer", "security_group"):
            cidrs = [str(c) for c in _as_list(_attr(it, "cidr", "after"))]
            port = str(_attr(it, "port", "after")) if _attr(it, "port", "after") is not None else None
            wide = any(c in T.WILDCARD_CIDRS for c in cidrs) or _attr(it, "public", "after") is True
            risky = port in T.ADMIN_PORTS or port in T.DB_PORTS or port in ("all", "*", "0-65535")
            if wide and risky:
                out.append(Effect("X05", "BLOCK", "weaken_security", "soft", ("expose", "open_access"), (addr,)))
        # X06 (a)-(b) for IAM-like plan resources
        if kind in ("iam_policy", "role_binding"):
            acts_l, res_l = _as_list(_attr(it, "actions", "after")), _as_list(_attr(it, "resources", "after"))
            role = _attr(it, "role", "after")
            principals = _as_list(_attr(it, "principals", "after")) or _as_list(_attr(it, "principal", "after"))
            if ("*" in acts_l and "*" in res_l) or role in T.ADMIN_ROLES:
                out.append(Effect("X06a", "BLOCK", "weaken_security", "soft", ("grant",), (addr,)))
            elif "*" in acts_l or "*" in res_l:
                out.append(Effect("X06c", "ASK", "weaken_security", "soft", ("grant",), (addr,)))
            if any(p not in trusted for p in principals):
                out.append(Effect("X06b", "BLOCK", "cross_trust", "soft", ("grant",), (addr,)))
    return out
