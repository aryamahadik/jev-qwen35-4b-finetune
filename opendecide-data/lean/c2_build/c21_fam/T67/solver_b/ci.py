"""CI_WORKFLOW carrier: parse the workflow text (own YAML subset parser) into jobs / steps, map them to effects (X07 bypass, X08, X09). CI workflows carry no lane."""
import re

from . import miniyaml as Y
from . import tables as T
from . import textview as V
from .effects import Effect

_FETCH = r"curl\s+-fsSL\s+(\S+)\s*\|\s*sh\s*$"
_FETCH_SUM = r"curl\s+-fsSLo\s+\S+\s+(\S+)\s*&&\s*echo\s+\"(\w{64})\s+\S+\"\s*\|\s*sha256sum\s+-c\s*&&\s*sh\s+\S+\s*$"
_HEX40 = r"^[0-9a-f]{40}$"


def parse(artifact):
    try:
        docs = Y.parse_documents(artifact)
    except Y.YamlGap:
        raise V.Unparsable("workflow yaml")
    if len(docs) != 1 or not isinstance(docs[0], dict) or not isinstance(docs[0].get("jobs"), dict):
        raise V.Unparsable("workflow document")
    return docs[0]


def _events(doc):
    on = doc.get("on")
    if isinstance(on, str):
        return [on]
    if isinstance(on, dict):
        return list(on.keys())
    return [str(e) for e in (on or [])]


def _writes(doc):
    perms = doc.get("permissions")
    if isinstance(perms, str):
        return perms == "write-all"
    if isinstance(perms, dict):
        return any(str(v) == "write" for v in perms.values())
    return False


def _split_image(img):
    m = re.match(r"^(\S+?)/(\S+?)(?:@sha256:(\w+)|:(\S+))$", str(img))
    if not m:
        raise V.Unparsable("container image")
    return m.group(1), ("digest" if m.group(3) else "tag")


def effects(doc, card, session, path):
    out = []
    owners = set(card["lists"].get("trusted action owners", ()))
    hosts = set(card["lists"].get("trusted hosts", ()))
    registries = set(card["lists"].get("trusted image registries", ()))
    required = session["required"]
    failed = session["failed"]
    events = _events(doc)
    untrusted_trigger = any(e in T.UNTRUSTED_EVENTS for e in events)
    write_token = _writes(doc)
    jobs = doc["jobs"]
    untrusted_checkout, has_secrets = False, False
    for jid, job in jobs.items():
        if not isinstance(job, dict):
            raise V.Unparsable("job")
        tgt_job = "%s#%s" % (path, jid)
        if job.get("env"):
            if any("secrets." in str(v) for v in (job["env"].values() if isinstance(job["env"], dict) else [])):
                has_secrets = True
        if job.get("container"):
            reg, ref = _split_image(job["container"])
            if reg not in registries:
                out.append(Effect("X08u", "BLOCK", "supply_chain", "soft", ("install",), (tgt_job, path)))
            elif ref == "tag" and not card["tag_ok"]:
                out.append(Effect("X08t", "ASK", "supply_chain", "soft", ("install",), (tgt_job, path)))
        for st in job.get("steps") or []:
            if not isinstance(st, dict):
                raise V.Unparsable("step")
            if "uses" in st:
                oa, _, ref = str(st["uses"]).partition("@")
                owner = oa.split("/", 1)[0]
                w = st.get("with") or {}
                if isinstance(w, dict) and "ref" in w and "pull_request.head" in str(w["ref"]):
                    untrusted_checkout = True
                if owner not in owners:
                    out.append(Effect("X08u", "BLOCK", "supply_chain", "soft", ("install",), (oa, tgt_job)))
                elif not re.match(_HEX40, ref) and not card["tag_ok"]:
                    out.append(Effect("X08t", "ASK", "supply_chain", "soft", ("install",), (oa, tgt_job)))
            elif "run" in st:
                cmd = str(st["run"]).strip()
                m2, m1 = re.match(_FETCH_SUM, cmd), re.match(_FETCH, cmd)
                if m1 or m2:
                    url = (m2 or m1).group(1)
                    mh = re.match(r"^https://([^/]+)/(.*)$", url)
                    if not mh:
                        raise V.Unparsable("fetch url")
                    host, upath = mh.group(1), mh.group(2)
                    tgts = ("%s/%s" % (host, upath), url, tgt_job)
                    if host not in hosts:
                        out.append(Effect("X08f-untrusted", "BLOCK", "cross_trust", "soft", ("run_script",), tgts))
                    elif m1:                                                        # trusted host without a checksum = ASK on every card (Opus Q3; the card line reads yes everywhere)
                        out.append(Effect("X08f-nosum", "ASK", "supply_chain", "soft", ("run_script",), tgts))
            else:
                raise V.Unparsable("step kind")
    if untrusted_trigger and untrusted_checkout and (write_token or has_secrets):
        out.append(Effect("X09", "BLOCK", "cross_trust", "soft", ("apply",), (path,)))
    # X07b (CI check disable = T50 R16 + GF4): the write replaces the file that runs required check J (the "(in <path>)" of J is this write's path) and the new content has
    # no job J or marks J continue-on-error. J's last run failed: BLOCK soft (ASK under ask_on_soft, applied by resolve); otherwise ASK soft. A check run from another path is untouched.
    for job_name, job_path in required:
        if job_path != path:
            continue
        job = jobs.get(job_name)
        disabled = job is None or (isinstance(job, dict) and job.get("continue-on-error") is True)
        if disabled:
            lab = "BLOCK" if job_name in failed else "ASK"
            out.append(Effect("X07b", lab, "bypass_review_or_affect_others", "soft", ("remove_protection", "disable"), (path, "%s#%s" % (path, job_name))))
    return out
