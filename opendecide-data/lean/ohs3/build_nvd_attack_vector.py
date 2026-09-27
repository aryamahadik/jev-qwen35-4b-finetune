"""OHS-3 part: nvd_attack_vector (label-verification yes/no form, Amendment 1, over the 4 CVSS v3.1 Attack Vector values).

Source: NVD CVE API 2.0, CVEs published 2026-06-01T00:00:00.000 .. 2026-09-26T23:59:59.999.
Input is ONLY the frozen raw snapshot in ohs3/cache/nvd_attack_vector/ (made once by ohs3/fetch_nvd_snapshot.py;
pages saved verbatim, gzip-compressed, sha256 of each uncompressed page in manifest.json). Re-runs give identical rows.

Rules (task spec + ohs3/selection_criteria.md):
- Label = cvssData.attackVector of the NVD 'Primary' cvssMetricV31 entry. If there is no Primary entry, the only
  cvssMetricV31 entry is used when there is exactly one. Dropped: no v3.1 entry; no Primary and 2+ Secondary entries;
  any v3.1 entry whose attackVector conflicts with the label; vulnStatus 'Rejected'.
- State = the English description only (lang 'en'), whitespace normalised. No CVSS vector, score, CWE, vendor data
  or any other field. Descriptions that themselves carry a CVSS vector or score ('CVSS', 'AV:N'-style tokens,
  'base score'; mostly Oracle CPU texts) or name the attack vector ('attack vector', 'vector is physical') are DROPPED.
- Verification fix: CNA templates that mechanically restate the CNA's own Attack Vector field (VulDB sentence,
  Microsoft trailing phrase, Adobe 'administrative network zone' sentence; see strip_av_markers) are STRIPPED from
  the text; the removed strings are kept in meta.state_redactions.
- Dedup: exact and normalised-whitespace (case-folded) description match. A text that appears under two different
  labels is dropped entirely; otherwise the lowest CVE id is kept.
- Design (seed 20261026): 36 CVEs per gold label (144). Per label, 18 are yes rows (asked = gold, gold 1) and 18 are
  no rows (gold 0) whose asked label is one of the other 3, 6 each. So every label is asked 36 times (18 in the yes
  half, 18 in the no half) and is gold for 36 CVEs; yes/no is exactly 72/72.
- Card: the asked label with its official definition, FIRST CVSS v3.1 specification, Section 2.1.1, Table 1
  (verbatim; footnote marker removed). The builder checks each definition against the cached spec page.
"""
import collections
import gzip
import hashlib
import html
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / "nvd_attack_vector"
SPEC_HTML = CACHE / "first_cvss_v31_spec.html"
OUT = LEAN / "data" / "ohs3_parts" / "nvd_attack_vector.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "nvd_attack_vector_summary.json"

TASK = "nvd_attack_vector"
SEED = 20261026
PER_LABEL = 36          # 18 yes + 18 no rows with this gold
YES_PER_LABEL = 18
MIN_CH, MAX_CH = 20, 6000
TRACK_CUTOFF = "2026-06-01"
PUB_RANGE = ("2026-06-01T00:00:00.000", "2026-09-26T23:59:59.999")

LABELS = ["Network", "Adjacent", "Local", "Physical"]
NVD2LABEL = {"NETWORK": "Network", "ADJACENT_NETWORK": "Adjacent", "LOCAL": "Local", "PHYSICAL": "Physical"}
DEFS = {
    "Network": ("The vulnerable component is bound to the network stack and the set of possible attackers extends "
                "beyond the other options listed below, up to and including the entire Internet. Such a vulnerability "
                "is often termed “remotely exploitable” and can be thought of as an attack being exploitable at the "
                "protocol level one or more network hops away (e.g., across one or more routers). An example of a "
                "network attack is an attacker causing a denial of service (DoS) by sending a specially crafted TCP "
                "packet across a wide area network (e.g., CVE‑2004‑0230)."),
    "Adjacent": ("The vulnerable component is bound to the network stack, but the attack is limited at the protocol "
                 "level to a logically adjacent topology. This can mean an attack must be launched from the same shared "
                 "physical (e.g., Bluetooth or IEEE 802.11) or logical (e.g., local IP subnet) network, or from within a "
                 "secure or otherwise limited administrative domain (e.g., MPLS, secure VPN to an administrative network "
                 "zone). One example of an Adjacent attack would be an ARP (IPv4) or neighbor discovery (IPv6) flood "
                 "leading to a denial of service on the local LAN segment (e.g., CVE‑2013‑6014)."),
    "Local": ("The vulnerable component is not bound to the network stack and the attacker’s path is via "
              "read/write/execute capabilities. Either: the attacker exploits the vulnerability by accessing the target "
              "system locally (e.g., keyboard, console), or remotely (e.g., SSH); or the attacker relies on User "
              "Interaction by another person to perform actions required to exploit the vulnerability (e.g., using "
              "social engineering techniques to trick a legitimate user into opening a malicious document)."),
    "Physical": ("The attack requires the attacker to physically touch or manipulate the vulnerable component. "
                 "Physical interaction may be brief (e.g., evil maid attack) or persistent. An example of such an attack "
                 "is a cold boot attack in which an attacker gains access to disk encryption keys after physically "
                 "accessing the target system. Other examples include peripheral attacks via FireWire/USB Direct Memory "
                 "Access (DMA)."),
}
INSTRUCTIONS = "Does the CVSS v3.1 Attack Vector value in the card apply to this vulnerability?"
LABEL_SOURCE = ("Official: FIRST, Common Vulnerability Scoring System v3.1: Specification Document, Section 2.1.1 "
                "Attack Vector, Table 1 (https://www.first.org/cvss/v3.1/specification-document); verbatim, footnote "
                "marker after 'evil maid attack' removed.")
LICENCE = ("NVD data: US government work, public domain (https://nvd.nist.gov/developers/terms-of-use); CVE "
           "descriptions: CVE Terms of Use, copyright The MITRE Corporation, free to use with attribution "
           "(https://www.cve.org/Legal/TermsOfUse). This product uses data from the NVD API but is not endorsed or "
           "certified by the NVD.")
CUE_RE = re.compile(r"(?i)CVSS|\bAV:[NALP]\b|base\s+score|attack\s+vector|\bvector\s+is\s+(?:network|adjacent|local|physical)")
# Source-specific attack-vector markers (verification fix): CNA description templates that render the CNA's own
# CVSS Attack Vector field as fixed text, ~1:1 with the label in the whole snapshot. Stripped (not dropped):
#  - VulDB (cna@vuldb.com): one stand-alone template sentence, e.g. "The attack can be launched remotely." (AV:N),
#    "Attacking locally is a requirement." (AV:L), "The attack needs to be done within the local network." (AV:A),
#    "It is possible to launch the attack on the physical device." (AV:P). Matched as a letters-and-spaces-only
#    sentence that contains 'attack' and remote/local/physical.
#  - Microsoft (secure@microsoft.com): the trailing phrase " locally" / " over a network" / " over an adjacent
#    network" / " with a physical attack" at the end of the "allows an ... attacker to ..." sentence.
#  - Adobe (psirt@adobe.com): the sentence "The vulnerable component is restricted to an administrative network zone
#    by default." (all 13 snapshot cases are AV:A; it echoes the Adjacent definition).
VULDB_SENT_RE = re.compile(r"(?:(?<=[.!?])\s+|^)([A-Z][A-Za-z ]{8,90}\.)(?=\s|$)")
MSRC_RE = re.compile(r" (?:locally|over a network|over an adjacent network|with a physical attack)(?=\.(?:\s|$))")
ADOBE_SENT = "The vulnerable component is restricted to an administrative network zone by default."
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def strip_av_markers(text, src):
    removed = []
    if src == "cna@vuldb.com":
        def sub(m):
            s = m.group(1)
            if re.search(r"(?i)\battack", s) and re.search(r"(?i)remote|local|physical", s):
                removed.append(s)
                return ""
            return m.group(0)
        text = VULDB_SENT_RE.sub(sub, text)
    if src == "secure@microsoft.com":
        removed += [m.group(0).strip() for m in MSRC_RE.finditer(text)]
        text = MSRC_RE.sub("", text)
    if ADOBE_SENT in text:
        removed.append(ADOBE_SENT)
        text = text.replace(ADOBE_SENT, "")
    return norm_ws(text), removed


def norm_ws(s):
    s = (s or "").replace("\r", "")
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def check_defs():
    t = SPEC_HTML.read_text(encoding="utf-8")
    t = re.sub(r"<sup[^>]*>.*?</sup>", "", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\s+", " ", t)
    for lab, d in DEFS.items():
        assert re.sub(r"\s+", " ", d) in t, f"definition for {lab} not found verbatim in cached spec"
    return hashlib.sha256(SPEC_HTML.read_bytes()).hexdigest()


def load_snapshot():
    manifest = json.loads((CACHE / "manifest.json").read_text())
    cves = []
    for p in manifest["pages"]:
        body = gzip.decompress((CACHE / p["file"]).read_bytes())
        assert hashlib.sha256(body).hexdigest() == p["sha256_uncompressed"], f"snapshot changed: {p['file']}"
        vs = json.loads(body)["vulnerabilities"]
        assert len(vs) == p["n"]
        cves.extend(v["cve"] for v in vs)
    assert len(cves) == manifest["totalResults"] == len({c["id"] for c in cves}), "incomplete snapshot"
    return manifest, cves


def cve_key(cid):
    _, y, n = cid.split("-")
    return (int(y), int(n))


def label_of(c, dropped):
    m = c.get("metrics", {}).get("cvssMetricV31", [])
    if not m:
        dropped["no_cvss_v31"] += 1
        return None
    prim = [x for x in m if x["type"] == "Primary"]
    if len(prim) == 1:
        chosen = prim[0]
    elif len(prim) == 0 and len(m) == 1:
        chosen = m[0]
    else:
        dropped["no_primary_and_multiple_v31_entries" if not prim else "multiple_primary"] += 1
        return None
    avs = {x["cvssData"]["attackVector"] for x in m}
    if len(avs) > 1:
        dropped["conflicting_v31_attack_vectors"] += 1
        return None
    return chosen


def main():
    spec_sha = check_defs()
    manifest, cves = load_snapshot()
    dropped = collections.Counter()
    dropped_redact = collections.Counter()
    removed_forms = collections.Counter()
    cands = []
    for c in sorted(cves, key=lambda c: cve_key(c["id"])):
        if not (PUB_RANGE[0] <= c["published"] <= PUB_RANGE[1]):
            dropped["published_out_of_range"] += 1
            continue
        if c.get("vulnStatus") == "Rejected":
            dropped["rejected"] += 1
            continue
        en = [d["value"] for d in c.get("descriptions", []) if d["lang"] == "en"]
        if len(en) != 1:
            dropped["no_single_english_description"] += 1
            continue
        chosen = label_of(c, dropped)
        if chosen is None:
            continue
        state, removed = strip_av_markers(norm_ws(en[0]), c.get("sourceIdentifier"))
        if CUE_RE.search(state):
            dropped["description_contains_cvss_vector_or_score"] += 1
            continue
        if not (MIN_CH <= len(state) <= MAX_CH):
            dropped["state_length"] += 1
            continue
        cands.append({"cve": c, "state": state, "label": NVD2LABEL[chosen["cvssData"]["attackVector"]],
                      "metric": chosen, "removed": removed})
        if removed:
            dropped_redact[(c.get("sourceIdentifier"), NVD2LABEL[chosen["cvssData"]["attackVector"]])] += 1
            removed_forms[" | ".join(removed)] += 1
    stats = {"snapshot_cves": len(cves), "dropped_before_dedup": dict(dropped),
             "av_marker_stripped_by_source_and_label": {f"{k[0]}|{k[1]}": v for k, v in sorted(dropped_redact.items())},
             "av_marker_forms_stripped": dict(sorted(removed_forms.items(), key=lambda kv: (-kv[1], kv[0])))}

    # ---- dedup (exact + normalised whitespace, case-folded)
    by_text = collections.defaultdict(list)
    for x in cands:
        by_text[re.sub(r"\s+", " ", x["state"]).strip().lower()].append(x)
    pool = {lab: [] for lab in LABELS}
    dd = collections.Counter()
    for key, xs in by_text.items():
        if len({x["label"] for x in xs}) > 1:
            dd["duplicate_text_conflicting_labels"] += len(xs)
            continue
        dd["duplicate_text_same_label_extra"] += len(xs) - 1
        x = xs[0]  # lowest CVE id (cands sorted)
        pool[x["label"]].append(x)
    stats["dedup_dropped"] = dict(dd)
    stats["eligible_pool_by_label"] = {lab: len(pool[lab]) for lab in LABELS}

    # ---- sampling + asked-label assignment
    chosen = []
    for lab in LABELS:
        p = sorted(pool[lab], key=lambda x: cve_key(x["cve"]["id"]))
        assert len(p) >= PER_LABEL, f"pool too small for {lab}: {len(p)}"
        pick = random.Random(f"{SEED}|sample|{lab}").sample(p, PER_LABEL)
        others = [o for o in LABELS if o != lab]
        n_each = (PER_LABEL - YES_PER_LABEL) // len(others)
        asked_no = [o for o in others for _ in range(n_each)]
        random.Random(f"{SEED}|asked|{lab}").shuffle(asked_no)
        for i, x in enumerate(pick):
            if i < YES_PER_LABEL:
                chosen.append((x, lab, 1))
            else:
                chosen.append((x, asked_no[i - YES_PER_LABEL], 0))

    rows = []
    for x, asked, gold in chosen:
        c, m = x["cve"], x["metric"]
        cid = c["id"]
        rows.append({
            "id": "r_" + sha(f"ohs3|{TASK}|{cid}")[:12],
            "group_id": f"g:ohs3:{TASK}:{cid}",
            "call_id": "c_" + sha(x["state"])[:12],
            "split": "ohs3",
            "track": "F" if c["published"][:10] >= TRACK_CUTOFF else "U",
            "source": TASK,
            "state": x["state"],
            "qtype": "noul",
            "instructions": INSTRUCTIONS,
            "options": None,
            "gold": gold,
            "role": "aff",
            "card": f"- {asked}: {DEFS[asked]}",
            "meta": {
                "task": TASK,
                "dataset": "NVD CVE API 2.0 (services.nvd.nist.gov/rest/json/cves/2.0)",
                "cve_id": cid,
                "url": f"https://nvd.nist.gov/vuln/detail/{cid}",
                "api_url": f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cid}",
                "published": c["published"],
                "lastModified_at_snapshot": c["lastModified"],
                "vulnStatus_at_snapshot": c.get("vulnStatus"),
                "cve_source_identifier": c.get("sourceIdentifier"),
                "attackVector": m["cvssData"]["attackVector"],
                "gold_label": x["label"],
                "label_name": asked,
                "vectorString_source": m["source"],
                "vectorString_type": m["type"],
                "n_cvss_v31_entries": len(c["metrics"]["cvssMetricV31"]),
                "state_redactions": x["removed"],
                "snapshot_fetched_utc": manifest["fetched_utc"],
                "licence": LICENCE,
            },
        })

    # ---- validation
    assert len(rows) == PER_LABEL * len(LABELS), len(rows)
    assert len({r["id"] for r in rows}) == len(rows), "duplicate ids"
    assert len({r["group_id"] for r in rows}) == len(rows), "duplicate group ids"
    assert len({r["call_id"] for r in rows}) == len(rows), "duplicate states"
    assert sum(r["gold"] for r in rows) * 2 == len(rows)
    asked_ct = collections.Counter((r["meta"]["label_name"], r["gold"]) for r in rows)
    for lab in LABELS:
        assert asked_ct[(lab, 1)] == YES_PER_LABEL and asked_ct[(lab, 0)] == YES_PER_LABEL, asked_ct
    for r in rows:
        assert MIN_CH <= len(r["state"]) <= MAX_CH
        assert not CUE_RE.search(r["state"])
        assert strip_av_markers(r["state"], r["meta"]["cve_source_identifier"])[1] == []
        assert (r["gold"] == 1) == (r["meta"]["label_name"] == r["meta"]["gold_label"])
        assert set(r) == {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
                          "instructions", "options", "gold", "role", "card", "meta"}
    rows.sort(key=lambda r: r["id"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(body)

    pub = sorted(r["meta"]["published"] for r in rows)
    lens = sorted(len(r["state"]) for r in rows)
    summary = {
        "task": TASK, "split": "ohs3", "qtype": "noul", "form": "label-verification yes/no (Amendment 1)",
        "rows": len(rows), "seed": SEED,
        "gold_balance": {"1": sum(r["gold"] for r in rows), "0": sum(1 - r["gold"] for r in rows)},
        "asked_label_counts": dict(sorted(collections.Counter(r["meta"]["label_name"] for r in rows).items())),
        "asked_label_x_gold": {f"{k[0]}|{k[1]}": v for k, v in sorted(asked_ct.items())},
        "true_attack_vector_counts": dict(sorted(collections.Counter(r["meta"]["gold_label"] for r in rows).items())),
        "no_rows_asked_vs_true": dict(sorted(collections.Counter(
            f"asked {r['meta']['label_name']} / true {r['meta']['gold_label']}" for r in rows if r["gold"] == 0).items())),
        "vectorString_source_counts": dict(collections.Counter(
            f"{r['meta']['vectorString_source']} ({r['meta']['vectorString_type']})" for r in rows).most_common()),
        "cve_source_identifier_top": dict(collections.Counter(
            r["meta"]["cve_source_identifier"] for r in rows).most_common(10)),
        "track": dict(collections.Counter(r["track"] for r in rows)),
        "published_range_sample": [pub[0], pub[-1]],
        "query_date_range": list(PUB_RANGE),
        "state_chars": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "instructions": INSTRUCTIONS,
        "card_template": "- <asked label>: <official definition>",
        "labels": {lab: DEFS[lab] for lab in LABELS},
        "label_definition_source": LABEL_SOURCE,
        "spec_page_sha256": spec_sha,
        "author_written_definitions": [],
        "licence": LICENCE,
        "redactions": [
            "CNA template text that restates the CNA's CVSS Attack Vector is removed from the description (see "
            "build_stats.av_marker_forms_stripped): VulDB stand-alone attack-location sentence; Microsoft trailing "
            "'locally' / 'over a network' / 'over an adjacent network' / 'with a physical attack'; Adobe 'The vulnerable "
            "component is restricted to an administrative network zone by default.'. Descriptions mentioning 'attack "
            "vector' or 'vector is <value>' are dropped. Per row: meta.state_redactions.",
        ],
        "rows_with_redaction": sum(1 for r in rows if r["meta"]["state_redactions"]),
        "provenance": {
            "snapshot_dir": str(CACHE.relative_to(LEAN)),
            "snapshot_fetched_utc": manifest["fetched_utc"],
            "api": manifest["api"],
            "totalResults": manifest["totalResults"],
            "pages": manifest["pages"],
            "cve_ids": sorted((r["meta"]["cve_id"] for r in rows), key=cve_key),
        },
        "state_fields": ["descriptions[lang=en].value"],
        "build_stats": stats,
        "output_sha256": sha(body),
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("provenance", "labels")}, indent=1,
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
