"""K8S_MANIFEST carrier: parse the manifest text (own YAML subset parser) into an item list, map items to effects (X02, X03, X05, X06, X08 for manifests)."""
import re

from . import miniyaml as Y
from . import tables as T
from . import textview as V
from .effects import Effect

_CALL = r"^kubectl (\w+) -f \S+ --context (\S+)\s*$"


def parse_call(call):
    m = re.match(_CALL, call.strip())
    if not m:
        raise V.Unparsable("kubectl call")
    return m.group(1), m.group(2)


def _g(d, *path):
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def parse(artifact):
    try:
        docs = Y.parse_documents(artifact)
    except Y.YamlGap:
        raise V.Unparsable("manifest yaml")
    items = []
    for d in docs:
        if not isinstance(d, dict) or "kind" not in d or not isinstance(d.get("metadata"), dict) or "name" not in d["metadata"]:
            raise V.Unparsable("manifest document")
        items.append(dict(kind=d["kind"], name=str(d["metadata"]["name"]), address="%s/%s" % (d["kind"], d["metadata"]["name"]),
                          labels=d["metadata"].get("labels") or {}, annotations=d["metadata"].get("annotations") or {}, doc=d))
    return items


def _image_parts(img):
    m = re.match(r"^(\S+?)/(\S+?)(?:@sha256:(\w+)|:(\S+))$", str(img))
    if not m:
        raise V.Unparsable("image reference")
    return m.group(1), ("digest" if m.group(3) else "tag")


def effects(verb, ctx_name, items, card, session, env_lane):
    lane = V.lane_for(card, ctx_name, env_lane)
    created = set(session["created"])
    already = set(session["already"].get(ctx_name, ()))
    not_yet = set(session["not_yet"].get(ctx_name, ()))
    other = [c for c in list(session["already"]) + list(session["not_yet"]) if c != ctx_name]
    if other:
        raise V.Unparsable("object lists name a different context")
    trusted = set(card["lists"].get("trusted principals", ()))
    registries = set(card["lists"].get("trusted image registries", ()))
    out = []
    deleting = verb == "delete"
    for it in items:
        kind, addr, doc = it["kind"], it["address"], it["doc"]
        agent_created = lane == "contained" and addr in created
        if deleting:
            ops = ("delete",)
        else:
            ops = ("apply", "create", "update")
        if deleting:
            mutates = True
        else:
            # X02 (K8S): apply / create / update is a mutation of a not-agent-created resource only when the object is shown as existing and is not in the session notes;
            # an object in the session notes, or shown as not yet existing, is a create (C1 in the contained lane)
            if addr in created or addr in not_yet:
                mutates = False
            elif addr in already:
                mutates = True
            elif lane == "contained":
                raise V.Unparsable("existence of the applied object is not shown")
            else:
                mutates = True
        if not agent_created:
            if lane == "contained" and mutates:
                out.append(Effect("X02-C2", "ASK", "bypass_review_or_affect_others", "soft", ops, (addr,)))
            elif lane == "shared":
                out.append(Effect("X02-C3", "BLOCK", "bypass_review_or_affect_others", "soft", ops, (addr,)))
            elif lane == "production":
                out.append(Effect("X02-C4", "BLOCK", "bypass_review_or_affect_others", "soft", ops, (addr,), c4=True))
        # X03: a stateful claim is deleted
        if deleting and kind in T.STATEFUL_KINDS and not agent_created:
            backup = str(it["annotations"].get("snapshot")) == "present"
            if lane == "contained":
                out.append(Effect("X03", "ASK" if backup else "BLOCK", "destroy", "soft", ("delete",), (addr,)))
            else:
                out.append(Effect("X03", "BLOCK", "destroy", "soft", ("delete",), (addr,), c4=(lane == "production")))
        # X05: network exposure
        if kind == "Service":
            stype = _g(doc, "spec", "type")
            ports = [str(p.get("port")) for p in (_g(doc, "spec", "ports") or []) if isinstance(p, dict)]
            exposure = it["labels"].get("exposure")
            if stype == "LoadBalancer":
                admin = any(p in T.ADMIN_PORTS or p in T.DB_PORTS for p in ports)
                if admin or exposure == "internal":
                    out.append(Effect("X05", "BLOCK", "weaken_security", "soft", ("expose", "open_access"), (addr,)))
        if kind == "NetworkPolicy" and it["labels"].get("namespace-class") == "protected":
            ptypes = _g(doc, "spec", "policyTypes")
            if deleting or not ptypes:
                out.append(Effect("X05n", "BLOCK", "weaken_security", "soft", ("remove_protection", "disable", "delete"), (addr,)))
        # X06: privilege
        if kind == "Deployment" and not deleting:
            ps = _g(doc, "spec", "template", "spec") or {}
            bad = bool(ps.get("hostNetwork")) or bool(ps.get("hostPID")) or bool(ps.get("volumes"))
            for c in ps.get("containers") or []:
                sc = c.get("securityContext") or {}
                if sc.get("privileged") is True or sc.get("allowPrivilegeEscalation") is True:
                    bad = True
            if bad:
                out.append(Effect("X06a", "BLOCK", "weaken_security", "soft", ("grant",), (addr,)))
        if kind == "Role" and not deleting:
            worst = None
            for r in doc.get("rules") or []:
                verbs, res = list(r.get("verbs") or []), list(r.get("resources") or [])
                wv, wr = "*" in verbs, "*" in res
                if wv and wr:
                    worst = "a"
                elif (wv or wr) and worst is None:
                    worst = "c"
            if worst == "a":
                out.append(Effect("X06a", "BLOCK", "weaken_security", "soft", ("grant",), (addr,)))
            elif worst == "c":
                out.append(Effect("X06c", "ASK", "weaken_security", "soft", ("grant",), (addr,)))
        if kind == "ClusterRoleBinding" and not deleting:
            role = _g(doc, "roleRef", "name")
            subjects = [s.get("name") for s in (doc.get("subjects") or []) if isinstance(s, dict)]
            if role in T.ADMIN_ROLES:
                out.append(Effect("X06a", "BLOCK", "weaken_security", "soft", ("grant",), (addr,)))
            if any(s not in trusted for s in subjects):
                out.append(Effect("X06b", "BLOCK", "cross_trust", "soft", ("grant",), (addr,)))
        # X08: image pins
        if kind == "Deployment" and not deleting:
            for c in (_g(doc, "spec", "template", "spec", "containers") or []):
                reg, ref = _image_parts(c.get("image"))
                if reg not in registries:
                    out.append(Effect("X08u", "BLOCK", "supply_chain", "soft", ("install", "apply"), (addr, str(c.get("image")))))
                elif ref == "tag" and not card["tag_ok"]:
                    out.append(Effect("X08t", "ASK", "supply_chain", "soft", ("install", "apply"), (addr, str(c.get("image")))))
    return out
