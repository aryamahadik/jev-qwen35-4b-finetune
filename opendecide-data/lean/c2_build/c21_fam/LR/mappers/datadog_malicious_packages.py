"""LR-04 DataDog malicious-software-packages-dataset mapper (labels / manifests / metadata ONLY; P1 realism, family T63).

LR-B5 (Opus b1): DataDog rows are T63 realism rows, not block R. LR-04 MAPS NOTHING before the T63 G0-lite is approved AND the
T63-M3 learnability precondition holds (Opus b1b, 18 Oct): `Mapper.map_records` raises MapperBlocked unless (1) an Opus approval
row for T63 exists in families/G0_APPROVALS*.md (`t63_g0_lite_approved`; it exists since batch 1b) and (2) the MEASURED field
record logs/LR04_FIELD_RECORD.json (`measure_field_record`, train manifests only) shows a visible label-bearing field outside
the payloads (`field_record_allows_mapping`). The measured record shows only package name, ecosystem and the affected-version
list, i.e. condition (2) does NOT hold, so the mapper stays blocked: the T63-M3 decision (leave the slice out, a C2.2 item) is the
orchestrator's / Opus's, not this mapper's. The LR-04 S-pre PASS is the orchestrator's gate (row-start guard / conformance). Negatives are T63 generator rows (seeded training namespace, T63's own gold by construction)
handed in through ctx['t63_negatives']; R7 balance and the T63 name-shape probe are read on the COMBINED slice.

Fields read (the record the LR-B5 text asks for): ecosystem (from the file name), package name (key), and the manifest value
(null = malicious-intent package, all versions; list = compromised legitimate package, listed versions are malicious).
NOTHING is read from inside the encrypted payload ZIPs (they are never fetched). The label depends on the real package name
(typosquats, brand-jacks) so every positive carries the recorded T63-gate exception 'real package name, label depends on it'
(counted and reported); the training-namespace swap is T63's call, not made here.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "datadog_malicious_packages"
FORM = "lr_datadog_pkg_malicious"
FORMS = {FORM: "Is this package manifest malicious?"}
FAMILIES_DIR = os.path.join(lc.BUILD_DIR, "zed_orch", "c21", "families")

RECAST_TABLE = {
    "dataset_id": "DataDog/malicious-software-packages-dataset@8a74a4c8ee0e1a2927f0419e0710968702ded609 (manifest.json files only)",
    "train_file": "<eco>.manifest.train.json", "split_field": "none (own seeded 10% hold-out by package name)",
    "source_label_set": ["manifest entry present: null = malicious intent; [versions] = compromised versions"],
    "recast_option_set": ["Yes", "No"], "target_format": "yes/no",
    "mapping": {"manifest entry (null)": "Yes", "manifest entry ([versions], only these versions)": "Yes",
                "T63 generator negative": "No"},
    "distractor_policy": "n/a", "declared_balancing": "yes rate 40-60% on the COMBINED slice (positives + T63 negatives)",
    "declared_drops": ["R12 guards", "package names with CVE/GHSA ids"], "question_form_ids": [FORM],
    "span_selection_rule": "none", "expected_token_mean": 40,
    "recorded_exception": "real package name, label depends on it (T63-gate exception, counted and reported)",
}
META = {"dataset": DATASET, "lr_id": "LR-04", "family": "T63", "tier": "A", "cap": 500, "share_alike": False,
        "p1_realism": True, "recast_table": RECAST_TABLE}


class MapperBlocked(lc.RowStartRefused):
    pass


def t63_g0_lite_approved(families_dir=None):
    """True only if a verdict row for T63 in families/G0_APPROVALS*.md says APPROVE / APPROVED (Opus approval record)."""
    d = families_dir or FAMILIES_DIR
    rx = re.compile(r"^\|\s*T63/[^|]*\|[^|]*\|\s*(APPROVE|REVISE\s*->\s*APPROVED)", re.M)
    for p in sorted(glob.glob(os.path.join(d, "G0_APPROVALS*.md"))):
        with open(p, "r", encoding="utf-8") as f:
            if rx.search(f.read()):
                return True
    return False


FIELD_RECORD_PATH = os.path.join(HERE, "logs", "LR04_FIELD_RECORD.json")


def measure_field_record(train_dir=None, out_path=FIELD_RECORD_PATH):
    """MEASURE which fields the TRAIN manifest files carry outside the payload ZIPs (T63-M3 / LR-B5 field record) and write
    logs/LR04_FIELD_RECORD.json. Counts only; no package name is written. The manifest.json format is a flat mapping
    name -> null (malicious intent, all versions) | [versions] (compromised legitimate package)."""
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    rec = {"schema": "lr04-field-record-1", "dataset": DATASET, "source": "samples/<eco>/manifest.json (train part only)",
           "ecosystems": {}, "fields_read": ["package name (JSON key)", "ecosystem (from the file name)",
                                             "affected versions (null = all versions, or a list of version strings)"],
           "fields_NOT_read": ["anything inside the encrypted payload ZIPs (never fetched)"]}
    value_types = {}
    extra_keys = 0
    for p in sorted(glob.glob(os.path.join(d, "*.manifest.train.json"))):
        eco = os.path.basename(p).split(".manifest.train.json")[0]
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        nulls = sum(1 for v in data.values() if v is None)
        lists = sum(1 for v in data.values() if isinstance(v, list))
        other = len(data) - nulls - lists
        lens = [len(v) for v in data.values() if isinstance(v, list)]
        for v in data.values():
            if isinstance(v, dict):
                extra_keys += len(v)
        value_types[eco] = {"entries": len(data), "null_all_versions": nulls, "version_list": lists, "other_value_types": other,
                            "version_list_len_max": max(lens) if lens else 0}
    rec["ecosystems"] = value_types
    rec["extra_metadata_keys_per_entry"] = extra_keys
    rec["label_bearing_field_outside_payload"] = bool(extra_keys > 0)
    rec["reading"] = ("The files carry only name / version list / ecosystem. The only candidate signals are the package name (T63 K3/K4 "
                      "forbid real names in negatives and require every non-label field uninformative) and the version list, which "
                      "exists only on compromised-package positives and is itself a function of the label. No description, script, "
                      "dependency, date, author or hash field exists outside the payloads: condition of T63-M3 does NOT hold.")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
    return rec


def field_record_allows_mapping(path=FIELD_RECORD_PATH):
    """True only if the measured field record exists and says a label-bearing field exists outside the payloads."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return bool(json.load(f).get("label_bearing_field_outside_payload"))
    except (OSError, ValueError):
        return False


def read_train(train_dir=None):
    """Train-only reader: <eco>.manifest.train.json files. Yields {ecosystem, name, versions}."""
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for p in sorted(glob.glob(os.path.join(d, "*.manifest.train.json"))):
        eco = os.path.basename(p).split(".manifest.train.json")[0]
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        for name, vers in data.items():
            yield {"ecosystem": eco, "name": name, "versions": vers, "_src_line": "%s:%s" % (eco, name)}


def _card(eco, name, versions):
    v = "all versions" if versions is None else ", ".join(versions)
    return "ecosystem: %s\npackage: %s\naffected versions: %s" % (eco, name, v)


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def __init__(self, pools, seed=0, dry_run=True, mapper_file=None, approved_fn=None, stamp_fn=None, record_fn=None):
        super().__init__(pools, seed=seed, dry_run=dry_run, mapper_file=mapper_file, stamp_fn=stamp_fn)
        self.approved_fn = approved_fn or t63_g0_lite_approved
        self.record_fn = record_fn or field_record_allows_mapping

    def build(self, src, ctx):
        if src.get("negative"):
            return [{"form": FORM, "kind": "yesno", "context": _card(src["ecosystem"], src["name"], src.get("versions")),
                     "options": ["Yes", "No"], "gold_text": "No", "source_row_id": "t63neg:%s" % src["id"],
                     "extra": {"t63_negative": True}}]
        if not isinstance(src.get("name"), str) or not src["name"].strip():
            self.drops.add("empty_name", src.get("_src_line"))
            return []
        return [{"form": FORM, "kind": "yesno", "context": _card(src["ecosystem"], src["name"], src["versions"]),
                 "options": ["Yes", "No"], "gold_text": "Yes", "source_row_id": "datadog:%s" % src["_src_line"],
                 "extra": {"t63_gate_exception": "real package name, label depends on it", "ecosystem": src["ecosystem"],
                           "manifest_kind": "malicious_intent" if src["versions"] is None else "compromised_versions"}}]

    def independent_gold(self, src, cand):
        if src.get("negative"):
            return "No"                       # T63 negative by construction
        # every manifest entry is a confirmed malicious package (null = all versions, list = those versions)
        return "Yes" if (src["versions"] is None or isinstance(src["versions"], list)) else "?"

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        if not self.approved_fn():
            raise MapperBlocked("LR-B5: LR-04 maps nothing before the T63 G0-lite is approved (no Opus approval row for T63)")
        if not self.record_fn():
            raise MapperBlocked("T63-M3: the measured LR-04 field record shows no label-bearing field outside the payloads; "
                                "the slice is for the orchestrator / Opus to leave out (C2.2 item), nothing is mapped")
        ctx = ctx or {}
        positives = list(records)
        cap = cap if cap is not None else META["cap"]
        rows = []
        for src in positives:
            for cand in self.build(src, ctx):
                r = self.finish_candidate(src, cand)
                if r:
                    rows.append(r)
        rows = self.select(rows, cap, key=lambda r: r["extra"]["ecosystem"] + "/" + r["extra"]["manifest_kind"]) \
            if len(rows) > cap else rows
        for neg in ctx.get("t63_negatives", []):
            n = dict(neg, negative=True)
            for cand in self.build(n, ctx):
                r = self.finish_candidate(n, cand)
                if r:
                    rows.append(r)
        return rows
