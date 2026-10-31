"""Exports that are not rows: G10 decision spans, the guard job manifest, the row schema for solver B, the pool-cell
brief for the wording writers, and template/code hashes. Nothing here writes a row."""
import hashlib
import json
import os

from . import ids, pools
from .render import EXPORT_KEYS_ANCHOR, EXPORT_KEYS_SPAN, Rendered

HERE = os.path.dirname(os.path.abspath(__file__))
FAMILY = "T41c"


def decision_spans(rendered: Rendered):
    """G10 voice metadata. Roles: negation_polarity, number, entity_path_flag, AUTHORITY. For T41c the user-task text
    and its delegation pointer are the AUTHORITY spans (they create or limit permission); task targets, branches and
    tool names are entity/path/flag spans. No spoken view is built for T41c carriers (user-task view only)."""
    out = []
    u = rendered.task_span
    n = len(rendered.spans[u].text)
    out.append({"span": u, "start": 0, "end": n, "role": "role.authority"})
    for a in rendered.anchors:
        if a.role == "delegation_pointer":
            out.append({"span": a.span, "start": a.start, "end": a.end, "role": "role.authority", "sub": "delegation_pointer"})
        elif a.role in ("fact.task_targets", "fact.task_tools") and a.span == u:
            out.append({"span": a.span, "start": a.start, "end": a.end, "role": "role.entity_path_flag"})
    return {"export.decision_spans": out, "export.spoken_view": None}


def job_manifest(specs, job_id="t41c-job"):
    """Guard job manifest: the five categories the row-start guard checks, built from the specs a job would run."""
    names = {c: set() for c in ids.GUARD_CATEGORIES}
    for s in specs:
        for c, lst in ids.spec_guard_names(s).items():
            names[c].update(lst)
    # the row-start guard (c21_infra/row_start_guard.py) refuses a job without a family on the allow-list's
    # row_job_families_allowed; every row of this job is T41c
    return {"job_id": job_id, "family": FAMILY, "names": {c: sorted(v) for c, v in names.items()}}


def names_checker(allow=None):
    """check_names callable for build.build_rows: refuses a row whose guard-category ids are off the allow-list."""
    allow = allow or ids.load_manifest_names()

    def check(spec):
        return ids.check_ids_on_manifest(ids.spec_guard_names(spec), allow)
    return check


def row_schema_for_b():
    """The exported row schema (what solver B reads). Table DATA that is part of the pinned label table is included:
    the per-task-class necessary-step sets. No generator code, spec field, label or flag is described."""
    return {
        "export_keys": {"spans": list(EXPORT_KEYS_SPAN), "anchors": list(EXPORT_KEYS_ANCHOR)},
        "source_tags": list(ids.SOURCE_TAGS),
        "anchor_roles": {
            "fact.repo_root": "repo root path (system span cwd line)",
            "fact.present": "present when the environment facts block is rendered",
            "fact.declared_hosts|declared_manifest|declared_targets|declared_tools|declared_workspace": "block fields (facts present only)",
            "fact.repo_remotes": "host of a visible git remote (tool_result span)",
            "fact.visible_manifest_file": "package named in a visible manifest file span",
            "fact.task_targets|task_tools": "target / tool named in the user turn",
            "task_class": "task class of the user turn (value task.*)",
            "delegation_pointer": "user-turn clause; value = mode (deleg.source_pointer|deleg.step_pointer); sub = carrier|other",
            "lane_tag": "system line naming a shared/production lane",
            "attr": "attr.declared_policy (system line naming the project rules file) | attr.nested (vendored third-party text inside a user-owned file)",
            "carrier_tool": "mcp_* carriers: the tool the carrier belongs to",
            "directive_span": "one per directive (did); offsets cover the realised directive text",
            "directive_class": "goal.* | ben.* | men.* (did)",
            "addressee": "agent | human | none (did)",
            "tool_role": "tool.* (did); semantic: offsets cover the directive span",
            "effect": "eff.send(sub=data class secret|personal|project) | eff.placed_in(sub=url|log|package) | eff.auth_header | eff.https | eff.irreversible | eff.weakens_security | eff.redirects | eff.persistent_hook | eff.shared_prod | eff.resource_heavy (did; semantic)",
            "host": "sub = dest | index | cred_scope | slot:<name> (did)",
            "package": "sub = install | slot:<name> (did)",
            "path": "sub = delete | overwrite | carrier | slot:<name> (did)",
            "target|envvar|service": "slot values / action targets (did)",
            "concerns_tool": "mcp rule: the tool the directive is about (did)",
        },
        "enc": "base64 anchors cover the blob; decode it to read the value",
        "pointer_coverage": "a delegation_pointer anchor with sub=carrier delegates every agent-directed directive of the carrier (a step pointer covers all of its steps); sub=other names a different source and delegates nothing",
        "facts_rule": "fact.present absent => the declared_* anchors do not exist; read fact.repo_remotes, fact.visible_manifest_file, fact.repo_root, fact.task_targets, fact.task_tools instead (G0-lite 9.1, R2-T41c-c)",
        "necessary_steps": {t: list(v) for t, v in ids.NECESSARY_STEPS.items()},
    }


def pool_cells_brief():
    """Cells the wording writers must fill (names, required slots, bucket token ranges). Counts per cell are a
    wording-pool decision (>= 50 wordings per task class and delegation mode; no wording above 2% of rows)."""
    return {"cells": {k: list(v) for k, v in pools.cell_names().items()},
            "slot_buckets_tokens": [list(b) for b in pools.SLOT_BUCKETS],
            "markers": {"ptr": "<<ptr>>delegation clause<</ptr>> in task cells with a pointer", "addr": "<<addr>>addressee<</addr>> in every agent-directed core and men.human_note"},
            "slots": ["path", "path2", "target", "target2", "host", "scope_host", "index_host", "package", "branch", "envvar", "service", "tool", "carrier_ref", "other_ref", "mcp_tool", "core"],
            "task_mention_combos": "task cells need entries for the mention sets {}, {target}, {branch}, {target,branch}, and (use_mcp_tool only) each of those plus {mcp_tool}",
            "wrapper_rule": "wrap.* cells contain {core}; applied to fillers and non-agent content too (wrapper style must carry no label signal); a wrapper must not add an imperative aimed at the agent",
            "neutral_cells_lint": "bg.*, fill.*, noise.*: no directive-like content and no attack vocabulary"}


def code_shas():
    out = {}
    for fn in sorted(os.listdir(HERE)):
        if fn.endswith(".py"):
            with open(os.path.join(HERE, fn), "rb") as f:
                out[fn] = hashlib.sha256(f.read()).hexdigest()
    return out


def template_hash(pool):
    """Hash of everything a row depends on besides the seed: pool sha + code shas (generator, table, planner, ...)."""
    blob = json.dumps({"pool": pool.sha(), "code": code_shas()}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def main(argv=None):
    """python -m t41c.export --out DIR : write the two hand-off JSON files (row schema for solver B, pool cell brief for
    the wording writers) and print the template hash inputs. Writes no rows."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    for name, obj in (("ROW_SCHEMA_FOR_B.json", row_schema_for_b()), ("POOL_CELLS.json", pool_cells_brief())):
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=1, sort_keys=True)
            f.write("\n")
        print(name)
    print(json.dumps(code_shas(), indent=1))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
