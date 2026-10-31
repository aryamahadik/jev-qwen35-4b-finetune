"""T67 render round trip (generator-side render-fidelity check; NOT solver B). The rendered row is parsed with the validators (JSON / YAML / SQL
parsers), the card, session notes, table card and user turn are read back from the text, the engine is run on the RECONSTRUCTED spec, and the recovered
(label, reason, tier) must equal the stored gold. Also the GV12 naming check on the user turn (nothing added, nothing removed). -> list of problems."""
import re

from . import config as C
from . import engine, render as R, sqlmodel as SQ, userturn as UT


def _split_context(ctx_text):
    k = ctx_text.rfind("\n\nProposed ")
    return ctx_text[:k], ctx_text[k + 2:]


def _lst(v):
    return [] if v in ("none", "") else v.split(", ")


def card_from_text(card_text, carrier):
    kv = {}
    name = None
    tag_ok = False
    lock = False
    for ln in card_text.split("\n"):
        if ln.startswith("Policy card "):
            name = ln[len("Policy card "):]
        elif ln.startswith("tags from trusted sources are acceptable"):
            tag_ok = True
        elif ln.startswith("migration lock review: on"):
            lock = True
        elif ": " in ln:
            k, v = ln.split(": ", 1)
            kv[k] = v
    return {"display_name": name, "context_lists": {l: _lst(kv.get("%s contexts" % l, "none")) for l in ("contained", "shared", "production")},
            "database_lists": {l: _lst(kv.get("%s databases" % l, "none")) for l in ("contained", "shared", "production")},
            "trusted_principals": _lst(kv.get("trusted principals", "")), "trusted_image_registries": _lst(kv.get("trusted image registries", "")),
            "trusted_action_owners": _lst(kv.get("trusted action owners", "")), "trusted_hosts": _lst(kv.get("trusted hosts", "")),
            "digest_pin_requirement": "required" if kv.get("fetched scripts need a checksum") == "yes" else "not_required",
            "ask_on_soft": kv.get("soft blocks are raised to ASK") == "yes", "pin_policy": "tag_ok" if tag_ok else "require_pin", "lock_review": lock}


def _naming_from_user_turn(ut_text, addresses):
    ops = {ref for ref, word in UT.OP_WORD.items() if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(word), ut_text)}
    # an op word that is a prefix of a longer word of the lexicon ('grant' in 'grant access on') is counted once for the longer one
    return {"ops": ops, "targets": {a for a in addresses if a in ut_text}}


def reconstruct(rec):
    spec = rec["spec"]
    carrier = spec["carrier"]
    ctx = rec["rendered"]["context"]
    head, artifact_all = _split_context(ctx)
    blocks = head.split("\n\n")
    card = card_from_text(blocks[1], carrier)
    notes_or_table = blocks[2]
    ut_block = blocks[3]
    ut_text = ut_block[len("User: "):].split("\nEnvironment:")[0]
    session = {"agent_created": [], "existing": [], "new": [], "required_checks": []}
    table = None
    notes_ctx = {}
    if carrier != "MIGRATION_SQL":
        failed = set()
        for ln in notes_or_table.split("\n"):
            if ln.startswith("created by the agent this session: "):
                session["agent_created"] = _lst(ln.split(": ", 1)[1])
            elif ln.startswith("required checks: "):
                for tok in _lst(ln.split(": ", 1)[1]):
                    m = re.fullmatch(r"(\S+) \(in (\S+)\)", tok)
                    session["required_checks"].append({"id": m.group(1), "path": m.group(2), "last_failed": False})
            elif ln.startswith("last run of "):
                m = re.fullmatch(r"last run of (\S+): failed", ln)
                failed.add(m.group(1))
            elif ln.startswith("objects already in "):
                m = re.fullmatch(r"objects already in (\S+): (.*)", ln)
                notes_ctx["existing"] = m.group(1)
                session["existing"] = _lst(m.group(2))
            elif ln.startswith("objects not yet in "):
                m = re.fullmatch(r"objects not yet in (\S+): (.*)", ln)
                notes_ctx["new"] = m.group(1)
                session["new"] = _lst(m.group(2))
        for rc in session["required_checks"]:
            rc["last_failed"] = rc["id"] in failed
        if failed - {rc["id"] for rc in session["required_checks"]}:
            raise ValueError("last run of an unlisted check")
    else:
        m = re.search(r"table: (\S+)\napproximate rows: ([\d,]+)\nbackup: (yes|no)", notes_or_table)
        n = int(m.group(2).replace(",", ""))
        table = {"name": m.group(1), "rows": n, "size_class": SQ.size_class(n), "backup": m.group(3) == "yes"}
    header, _, body = artifact_all.partition(":\n")                    # header = 'Proposed ...' line + file label; body = the file text
    out = {"carrier": carrier, "card": card, "session": session, "table": table, "items": [], "statements": [], "context": None, "database": None, "workflow": None,
           "meta": {}}
    if carrier == "PLAN_JSON":
        p = R.parse_plan(body)
        out["context"] = p["workspace"]
        for ch in p["changes"]:
            acts = list(ch["actions"])
            b, a = ch["before"], ch["after"]
            if acts == ["no-op"]:
                attrs, before = {}, None
            elif "delete" in acts and "create" not in acts:
                attrs, before = b, None
            elif "delete" in acts and "create" in acts:
                attrs, before = a, b
            elif "update" in acts:
                attrs, before = a, b
            else:
                attrs, before = a, None
            tags = {}
            for st in (a, b):
                if st and "tags" in st:
                    tags = dict(st["tags"])
            attrs = {k: v for k, v in (attrs or {}).items() if k != "tags"}
            before = {k: v for k, v in before.items() if k != "tags"} if before else None
            out["items"].append({"address": ch["address"], "kind": ch["type"], "actions": acts, "attrs": attrs, "before": before, "tags": tags})
    elif carrier == "K8S_MANIFEST":
        m = re.match(r"Proposed call: kubectl (\w+) -f manifest\.yaml --context (\S+)", header)
        verb, out["context"] = m.group(1), m.group(2)
        out["meta"] = {"verb": verb}
        if set(notes_ctx.values()) != {out["context"]} or set(notes_ctx) != {"existing", "new"}:
            raise ValueError("existence facts missing or naming another context")
        for it in R.parse_k8s(body):
            it["actions"] = ["delete"] if verb == "delete" else ["update"]          # the engine takes create-vs-update from the session facts (engine.k8s_actions)
            it["before"] = None
            out["items"].append(it)
    elif carrier == "CI_WORKFLOW":
        wf = R.parse_workflow(body)
        path = re.match(r"Proposed write: (\S+)", header).group(1)
        jobs = []
        for j in wf["jobs"]:
            steps = []
            for s in j["steps"]:
                s = dict(s)
                if s["kind"] in ("uses", "checkout"):
                    s["ref_kind"] = "commit" if re.fullmatch(r"[0-9a-f]{40}", s["ref_text"]) else "tag"
                steps.append(s)
            jobs.append(dict(j, steps=steps, container=(dict(j["container"]) if j["container"] else None)))
        out["workflow"] = {"name": wf["name"], "path": path, "on": wf["on"], "permissions": {k: v for k, v in wf["permissions"].items()} if isinstance(wf["permissions"], dict) else {},
                           "permissions_all": wf["permissions"] if isinstance(wf["permissions"], str) else None, "jobs": jobs}
    else:
        m = re.match(r"Proposed call: psql -d (\S+) -f migration\.sql", header)
        out["database"] = m.group(1)
        forms = R.parse_sql(body)
        sqltxt = re.sub(r"--[^\n]*", "", body)
        pred = " where " in sqltxt.lower()
        for f, t in forms:
            if f.startswith("MG-S"):
                kind = SQ.KIND_OF_FORM[f]
                if f == "MG-S13":
                    kind = "truncate" if "truncate" in sqltxt.lower() else "drop"
                out["statements"].append({"form": f, "kind": kind, "predicate": f == "MG-S14"})
            else:
                kind = {"DML-DEL": "delete", "DML-UPD": "update", "DML-INS": "insert", "GRANT": "grant"}[f]
                out["statements"].append({"form": None, "kind": kind, "predicate": pred})
    targets = [it["address"] for it in out["items"]]
    if out["workflow"]:
        wf_ = out["workflow"]
        targets.append(wf_["path"])
        for j in wf_["jobs"]:
            if j["container"]:
                targets.append("%s#%s" % (wf_["path"], j["id"]))
            for s in j["steps"]:
                if s["kind"] in ("uses", "checkout"):
                    targets.append("%s/%s" % (s["owner"], s["action"]))
                elif s["kind"] == "fetch_run":
                    targets.append("%s/%s" % (s["host"], s["path"]))
    if out["table"]:
        targets.append(out["table"]["name"])
    out["naming"] = _naming_from_user_turn(ut_text, targets)
    out["_targets"] = targets
    out["_ut_text"] = ut_text
    out["_body"] = body
    return out


def _session_norm(sess):
    return {"agent_created": sorted(sess["agent_created"]), "existing": sorted(sess.get("existing", ())), "new": sorted(sess.get("new", ())),
            "required_checks": sorted((c["id"], c["path"], bool(c.get("last_failed"))) for c in sess["required_checks"])}


def check(rec, lock_table=None):
    bad = []
    spec = rec["spec"]
    try:
        rc = reconstruct(rec)
    except Exception as e:                                                    # noqa: BLE001
        return ["parse_error:%s" % type(e).__name__]
    bad += R.validate(spec, rc["_body"])
    if spec["carrier"] != "MIGRATION_SQL" and _session_norm(rc["session"]) != _session_norm(spec["session"]):
        bad.append("session")                                                  # the session facts (agent-created, existing / new objects, required checks, last runs) read back
    # card fidelity
    shown = {"ask_on_soft": True, "pin_policy": spec["carrier"] in ("K8S_MANIFEST", "CI_WORKFLOW"), "lock_review": spec["carrier"] == "MIGRATION_SQL",
             "digest_pin_requirement": spec["carrier"] == "CI_WORKFLOW"}
    for k, vis in shown.items():
        if vis and spec["card"][k] != rc["card"][k]:
            bad.append("card:" + k)
    lists_ok = (rc["card"]["database_lists"] == spec["card"]["database_lists"]) if spec["carrier"] == "MIGRATION_SQL" else \
        (rc["card"]["context_lists"] == spec["card"]["context_lists"])
    if rc["card"]["display_name"] != spec["card"]["display_name"] or not lists_ok:
        bad.append("card:lists")
    # the engine on the reconstructed spec must reproduce the stored triple
    cspec = dict(rc)
    cspec["card"] = dict(spec["card"], ask_on_soft=rc["card"]["ask_on_soft"])
    if shown["pin_policy"]:
        cspec["card"]["pin_policy"] = rc["card"]["pin_policy"]
    if shown["lock_review"]:
        cspec["card"]["lock_review"] = rc["card"]["lock_review"]
    for k in ("trusted_principals", "trusted_image_registries", "trusted_action_owners", "trusted_hosts"):
        if rc["card"][k]:
            cspec["card"][k] = rc["card"][k]
    if spec["carrier"] == "MIGRATION_SQL":
        cspec["card"]["database_lists"] = rc["card"]["database_lists"]
    else:
        cspec["card"]["context_lists"] = rc["card"]["context_lists"]
    if shown["digest_pin_requirement"]:
        cspec["card"]["digest_pin_requirement"] = rc["card"]["digest_pin_requirement"]
    try:
        got = engine.gold(cspec, lock_table)
    except Exception as e:                                                    # noqa: BLE001
        return bad + ["engine_on_parsed:%s" % type(e).__name__]
    if got != rec["gold_triple"]:
        bad.append("engine_on_parsed")
    # GV12 naming round trip
    d = rec.get("decisive")
    cell = spec["user_turn"]["cell"]
    known = list(dict.fromkeys(rc["_targets"] + ([d["target"]] if d is not None else [])))
    bad += ["naming:" + x for x in UT.naming_check(rc["_ut_text"], cell, d, known)]
    return bad
