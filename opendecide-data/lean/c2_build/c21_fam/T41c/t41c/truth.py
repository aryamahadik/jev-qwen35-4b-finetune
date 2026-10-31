"""K6(i): exhaustive truth tables, rendered through the REAL renderer so solver B sees real anchors.

Three tables (G0-lite K6(i): "exhaustive over all fact combinations, including the facts-absent defaults"):
  T1 facts-exhaustive: every membership combination of the fixed fact vocabulary (facts present: declared hosts x
     manifest x targets; facts absent: remotes x visible manifest x task target) x ~30 clause-representative actions.
  T2 action-exhaustive: every Action from table.truth_table_actions() (all effect-flag, send, path, install,
     target combinations incl. the R2-T41c-a auth exception) x 6 representative fact sets (3 present, 3 absent).
  T3 rule precedence: all 64 combinations of agent_directed / delegated / necessary / nested / declared_policy /
     in_scope x risk LOW/SOFT/HARD x source (user file | mcp same tool | mcp other tool).
Case specs use the fixed vocabulary names (they are test names, never rows). `TruthPool` supplies a generic template
that carries exactly the slots a case needs, so every value is anchored verbatim.

Solver B interface (the contract B is written against):  solve_b(export) -> {"label": L, "directives": {did: {"risk": R,
"label": L}}}  where `export` is render.export_for_b(rendered) and nothing else.
"""
import itertools
import random

from . import ids, pools, table
from .pools import Pool, make_test_pool, _grow
from dataclasses import replace

from .render import RowDrop, build_row, export_for_b
from .solver_a import row_problems, solve
from .spec import Directive, Pointer, Spec
from .table import Action, Facts, Send

W = "/w/in"
PATHS = ("/w/in/a", "/w/out/b")
HOSTS = table._HOSTS
PKGS = table._PKGS
TARGETS = table._TARGETS


class TruthPool(Pool):
    """Test pool plus a generic directive template for variant 'truth' (exactly the requested slots)."""
    def __init__(self, base=None):
        base = base or make_test_pool(per_cell=6)
        super().__init__({"kind": pools.KIND_TEST, "version": "truth", "cells": base.cells})

    def pick(self, cell, rng, require_slots=(), forbid_slots=(), accept=None, tries=64):
        parts = cell.split(".")
        if len(parts) == 4 and parts[2] == "truth":
            b = int(parts[3][1:])
            slots = sorted(require_slots)
            core = "<<addr>>Assistant<</addr>>, do " + " ".join("{%s}" % s for s in slots) + "." if slots else \
                "<<addr>>Assistant<</addr>>, do it."
            return {"id": "truth#%s" % cell, "text": _grow(rng, core, b)}
        return super().pick(cell, rng, require_slots, forbid_slots, accept, tries)


def _slots_for(a: Action, extra=None):
    """Slot values for an Action: every string value the table reads must be anchored."""
    s = {}
    if a.send:
        if a.send.host:
            s["host"] = a.send.host
        if a.send.cred_scope_host and a.send.cred_scope_host != a.send.host:
            s["scope_host"] = a.send.cred_scope_host
        if a.send.placed_in == "package":
            s["package"] = "p-bundle"
    ps = list(a.delete_paths) + list(a.overwrite_paths)
    for i, p in enumerate(dict.fromkeys(ps)):
        s["path" if i == 0 else "path2"] = p
    if a.install_pkg:
        s["package"] = a.install_pkg
    if a.install_index:
        s["index_host"] = a.install_index
    for i, t in enumerate(a.targets):
        s["target" if i == 0 else "target2"] = t
    s.update(extra or {})
    return tuple(sorted(s.items()))


def _spec(case_id, facts, action, *, cls="ben.set_task_env_flag", task="task.summarise_issue", pointer=None,
          carrier="car.rules_file", fmt="fmt.plain", src=ids.SRC_USER_FILE, agent=True, nested=False, policy=False,
          in_scope=False, carrier_tool=None, concerns=None, mentions=()):
    d = Directive(did="d0", cls=cls if agent else "men.security_writeup", action=action if agent else None,
                  agent_directed=agent, wrapper="wrap.plain_imperative", placement="place.p2", variant="truth" if agent else "",
                  slots=_slots_for(action) if agent and action else (), slot_bucket=1, nested=nested,
                  declared_policy=policy, in_scope=in_scope, concerns_tool=concerns)
    return Spec(row_id=case_id, block="train", group_id=case_id, pair_kind="single", pair_role="single",
                subtype="truth", task_class=task, pointer=pointer or Pointer(), task_mentions=tuple(mentions),
                carrier_type=carrier, carrier_format=fmt, carrier_src=src, facts=facts, directives=(d,), art_seed=case_id,
                len_target=1, carrier_tool=carrier_tool, declared_policy_file=policy, vendor_slot=nested)


# ---- T1 --------------------------------------------------------------------------------------------------------
def _subsets(xs):
    for k in range(len(xs) + 1):
        for c in itertools.combinations(xs, k):
            yield c


def t1_facts():
    for H in _subsets(HOSTS):
        for P in _subsets(PKGS):
            for T in _subsets(TARGETS):
                yield "Tp-%s-%s-%s" % ("".join(map(str, (HOSTS.index(h) for h in H))), "".join(map(str, (PKGS.index(p) for p in P))),
                                       "".join(map(str, (TARGETS.index(t) for t in T)))), Facts(
                    True, declared_hosts=H, declared_manifest=P, declared_workspace=W, declared_targets=T,
                    declared_tools=(), repo_root="/w", repo_remotes=(), visible_manifest=(), task_targets=(), task_tools=())
    for R in _subsets(HOSTS):
        for V in _subsets(PKGS):
            for Tt in ((),) + tuple((t,) for t in TARGETS):
                yield "Ta-%s-%s-%s" % ("".join(map(str, (HOSTS.index(h) for h in R))), "".join(map(str, (PKGS.index(p) for p in V))),
                                       "".join(map(str, (TARGETS.index(t) for t in Tt)))), Facts(
                    False, repo_root=W, repo_remotes=R, visible_manifest=V, task_targets=Tt, task_tools=())


def t1_actions():
    out = []
    for h in HOSTS:
        out.append(Action("tool.http_request", Send("project", h)))
        out.append(Action("tool.http_request", Send("secret", h, None, True, True, h)))
    out.append(Action("tool.http_request", Send("secret", HOSTS[0])))
    for pkg in PKGS:
        out.append(Action("tool.pkg_install", None, install_pkg=pkg))
        out.append(Action("tool.pkg_install", None, install_pkg=pkg, install_index=HOSTS[1]))
    for t in TARGETS:
        out.append(Action("tool.shell_run", None, targets=(t,)))
    out.append(Action("tool.shell_run", None, targets=(TARGETS[0], TARGETS[2])))
    out.append(Action("tool.file_delete", None, delete_paths=(PATHS[0],)))
    out.append(Action("tool.file_delete", None, delete_paths=(PATHS[1],)))
    out.append(Action("tool.file_write", None, overwrite_paths=(PATHS[0],)))
    out.append(Action("tool.file_write", None, overwrite_paths=(PATHS[1],)))
    out.append(Action("tool.file_delete", None, delete_paths=(PATHS[0],), irreversible=True))
    for f in ("weakens_security", "redirects", "persistent_hook", "resource_heavy"):
        out.append(Action("tool.shell_run", None, **{f: True}))
    return out


def t1_cases(limit=None, seed=0):
    acts = t1_actions()
    facts = list(t1_facts())
    rng = random.Random(seed)
    pairs = [(f, a) for f in facts for a in acts]
    if limit:
        pairs = rng.sample(pairs, min(limit, len(pairs)))
    for i, ((fid, f), a) in enumerate(pairs):
        mentions = ("target",) if (not f.present and f.task_targets) else ()
        yield _spec("T1-%s-%d" % (fid, i), f, a, mentions=mentions)


# ---- T2 --------------------------------------------------------------------------------------------------------
def t2_facts():
    return [
        Facts(True, declared_hosts=(), declared_manifest=(), declared_workspace=W, declared_targets=(), declared_tools=(),
              repo_root="/w", lane_tag=True),
        Facts(True, declared_hosts=HOSTS, declared_manifest=PKGS, declared_workspace=W, declared_targets=TARGETS,
              declared_tools=(), repo_root="/w", lane_tag=True),
        Facts(True, declared_hosts=(HOSTS[0], HOSTS[2]), declared_manifest=(PKGS[1],), declared_workspace=W,
              declared_targets=(TARGETS[1],), declared_tools=(), repo_root="/w", repo_remotes=(HOSTS[1],),
              visible_manifest=(PKGS[2],), lane_tag=True),
        Facts(False, repo_root=W, lane_tag=True),
        Facts(False, repo_root=W, repo_remotes=HOSTS, visible_manifest=PKGS, task_targets=(TARGETS[1],), lane_tag=True),
        Facts(False, repo_root=W, repo_remotes=(HOSTS[1],), visible_manifest=(PKGS[0],), task_targets=(TARGETS[0],),
              lane_tag=True),
    ]


def t2_cases(limit=None, seed=0):
    facts = t2_facts()
    acts = list(table.truth_table_actions())
    pairs = [(fi, a) for fi in range(len(facts)) for a in acts]
    if limit:
        pairs = random.Random(seed).sample(pairs, min(limit, len(pairs)))
    for i, (fi, a) in enumerate(pairs):
        f = facts[fi]
        yield _spec("T2-%d-%d" % (fi, i), f, a, mentions=("target",) if (not f.present and f.task_targets) else ())


# ---- T3 --------------------------------------------------------------------------------------------------------
def t3_cases():
    risk_action = {ids.LOW: Action("tool.shell_run"), ids.SOFT: Action("tool.shell_run", resource_heavy=True),
                   ids.HARD: Action("tool.shell_run", weakens_security=True)}
    facts_p = Facts(True, declared_hosts=(HOSTS[0],), declared_manifest=(PKGS[0],), declared_workspace=W,
                    declared_targets=(TARGETS[0],), declared_tools=("mcp-t",), repo_root="/w")
    i = 0
    for ad, dele, nec, nest, pol, ins in itertools.product((True, False), repeat=6):
        for risk, act in risk_action.items():
            for src in ("user", "mcp_same", "mcp_other"):
                i += 1
                if src != "user" and (nest or pol):
                    continue
                if ad and pol and not ins:        # not representable in a row (spec.validate_spec; B reads in-scope as ben.* + policy file)
                    continue
                if nec:
                    task, cls = "task.onboarding_setup", "ben.set_task_env_flag"      # step on the critical path
                else:
                    task, cls = "task.summarise_issue", "ben.set_task_env_flag"       # not on it
                ptr = Pointer("deleg.source_pointer", True) if dele else Pointer()
                kw = dict(cls=cls, task=task, pointer=ptr, agent=ad, nested=nest, policy=pol, in_scope=ins)
                if src == "user":
                    kw.update(carrier="car.rules_file", fmt="fmt.plain", src=ids.SRC_USER_FILE)
                    if not pol and not nest:
                        kw.update(carrier="car.tool_text", fmt="fmt.plain", src=ids.SRC_TOOL)
                else:
                    kw.update(carrier="car.mcp_description", fmt="fmt.plain", src=ids.SRC_MCP_DESC, carrier_tool="mcp-t",
                              concerns="mcp-t" if src == "mcp_same" else "mcp-other")
                yield _spec("T3-%d" % i, facts_p, act, **kw)


# ---- harness ---------------------------------------------------------------------------------------------------
def a_oracle(spec):
    """B-shaped answer computed by solver A (used to test the harness itself)."""
    t = solve(spec)
    return {"label": t["label"], "directives": {d["did"]: {"risk": d["risk"], "label": d["label"]} for d in t["directives"]}}


def run_k6_truth(solve_b, tables=("T1", "T2", "T3"), limit=None, pool=None, seed=0, pass_spec=False):
    """Compare B with A on every case of the requested tables. Returns a gate-style dict.
    pass_spec=True feeds solve_b the SPEC instead of the export (harness self-test with an oracle only)."""
    pool = pool or TruthPool()
    gens = {"T1": lambda: t1_cases(limit, seed), "T2": lambda: t2_cases(limit, seed), "T3": t3_cases}
    tot, bad, bad_ids, render_fail = 0, 0, [], 0
    for tb in tables:
        for sp in gens[tb]():
            r = None
            for attempt in range(4):             # the case semantics do not depend on the artifact seed: re-seed on a layout drop
                try:
                    sp2 = sp if attempt == 0 else replace(sp, art_seed="%s~%d" % (sp.art_seed, attempt))
                    r = build_row(sp2, pool, proxy_names=False)
                    prob = row_problems(sp2, r)
                    if prob:
                        raise ValueError(prob[0])
                    sp = sp2
                    break
                except RowDrop as e:
                    r = None
                    if e.code not in ("PLACEMENT_UNREACHABLE", "SLOT_LENGTH_UNMATCHED"):
                        break
                except Exception:
                    r = None
                    break
            if r is None:
                render_fail += 1
                continue
            tot += 1
            want = a_oracle(sp)
            try:
                got = solve_b(sp if pass_spec else export_for_b(r))
            except Exception as e:
                got = {"label": "ERROR:%s" % type(e).__name__, "directives": {}}
            same = got.get("label") == want["label"] and all(
                got.get("directives", {}).get(k, {}).get("risk") == v["risk"] for k, v in want["directives"].items())
            if not same:
                bad += 1
                bad_ids.append(sp.row_id)
    return {"id": "K6i", "tag": "PRE-FREEZE KILL", "pass": bad == 0 and render_fail == 0 and tot > 0, "cases": tot,
            "mismatches": bad, "render_failures": render_fail, "mismatch_ids": bad_ids[:30]}
