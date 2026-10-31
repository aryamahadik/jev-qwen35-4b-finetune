"""ac_report_only.py: OPTION 3, "OHS-4 is the binding test; OHS-AC is report-only for C2" (default OFF, NOT applied).

What the option does, and only when an owner ruling that carries the marker OHSAC_REPORT_ONLY exists in PREREG_FINAL.md and its id is
given (ruling_gate.py): the three OHS-AC targets (ohsac_hash, ohsac_rows, ohsac_gtpl) stop being part of the BINDING drop set of the
G13 logs, and so do the OHS-AC seed quarantines. Every other target stays binding exactly as now: the OHS-4 child (ohs4_hash, ohs4_rows,
ohs4_gtpl), the sob / DI / public targets, the C2 dev targets, A53, A31 (b). The OHS-AC hits are still computed, still logged, and are
written into the mix report AND the mix manifest as `ohsac_report_only` (counts, per-log shas of the id lists; no ids, no text).
Drop set under the option = union over logs of "ids hit by at least one non-OHS-AC target" (an id hit by both stays dropped).
Without the flag nothing here runs: every wrapper hands its argv to the original tool untouched.

Nothing in the pinned tools (g13_c2.py, mix_c2.py, c2_select.py, mixer.py; A64_TOOLS.md shas) is edited. The wrappers patch the running
process only:
  g13_c2_opt3.py   runs g13_c2.main with `derive_hits` / `_record` / `withdraw_waivers` wrapped, so every record gains
                   `drop_ids_by_class` = {"binding": [...], "ohsac_report_only": [...], "units": {...}, "capture": {...}}
                   (binding ids + report-only ids == drop_ids, disjoint). drop_ids itself is NOT changed (still the stricter full set).
  gen_full_c2_opt3.py  (family builds that honour a G13-seed quarantine; today only T27 does) keeps templates quarantined ONLY by OHS-AC targets.
  c2_select_opt3.py / mix_c2_opt3.py   read the binding ids instead of drop_ids (after the original tool's own log checks, so a
                   missing / incomplete / stale log is refused exactly as before).
A G13 log that has an OHS-AC record but no `drop_ids_by_class` is REFUSED under the option (the split cannot be recovered from counts);
a log with no OHS-AC record (the pre-A64 logs) has no OHS-AC drops, so all its drops stay binding.

Seal (defects 4-7 of the A68 review, fixed 17 Oct): every captured split carries `capture` = {ac_targets, module_sha256, set, run,
log_tool_sha256, ruling {id, block_sha256, prereg_sha256}, split_sha256}. split_log recomputes `split_sha256` from the lists and checks set /
run / tool sha against the log itself, so a split moved between logs, edited after the capture, or captured for another set is refused.
The selection record (select_<FAM>.json), the mix manifest + report and the gen_full G13-seed report all carry the `ohsac_report_only` block
(ruling, per-log counts and sha256 of the id lists; no ids). A written mix made under the option can be changed by --remove-sources only
through mix_c2_opt3.py with the same flag (the block is carried over unchanged); the plain tool refuses it.

Library CLI (counts only; reads logs/decontam_counts, writes nothing unless --out is given):
  ../.venv/bin/python -B c2_build/zed_orch/owner_options/ac_report_only.py report [--glob 'acquick_c2_*.json' ...] [--capture-plan]
  ../.venv/bin/python -B c2_build/zed_orch/owner_options/ac_report_only.py seed-split --log LOG --out FILE
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ruling_gate as rg  # noqa: E402

AC_TARGETS = ("ohsac_hash", "ohsac_rows", "ohsac_gtpl")      # == g13_c2.AC_TARGETS (tests/test_targets_match_g13_c2)
CLASSES_KEY = "drop_ids_by_class"
REPORT_KEY = "ohsac_report_only"


class SplitRefused(SystemExit):
    """A log whose binding / report-only split cannot be trusted (the option then refuses the run; nothing is dropped less)."""


def _sha_ids(ids) -> str:
    return hashlib.sha256("\n".join(sorted(map(str, ids))).encode("utf-8")).hexdigest()


def _this_sha() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def split_digest(set_name, run, binding, report_only, tool_sha) -> str:
    """The seal of one captured split: binds the two id lists (as sha256 of the sorted ids) to the set, the run and the tool sha of the log."""
    return hashlib.sha256(json.dumps({"set": set_name, "run": run, "tool_sha256": tool_sha, "binding": _sha_ids(binding),
                                      "ohsac_report_only": _sha_ids(report_only)}, sort_keys=True).encode("utf-8")).hexdigest()


def seal_classes(cl: dict, rec: dict, info: dict | None) -> dict:
    """`cl` (classes_from_hits) with the capture block completed from the finished log record `rec` and the ruling `info`."""
    cap = dict(cl.get("capture") or {})
    cap.update({"set": rec.get("set"), "run": rec.get("run"), "log_tool_sha256": rec.get("tool_sha256"),
                "ruling": ({k: info[k] for k in ("id", "marker", "block_sha256", "prereg_sha256")} if info else None)})
    cap["split_sha256"] = split_digest(cap["set"], cap["run"], cl["binding"], cl["ohsac_report_only"], cap["log_tool_sha256"])
    return {**cl, "capture": cap}


# ------------------------------------------------------------------------------------------------ capture (g13 side)
def classes_from_hits(run_name: str, units: dict, hits: dict) -> dict:
    """The split of one result's hits ({target: {method: {unit key: fields}}}): ids of units hit by a non-OHS-AC target (binding) and ids of
    units hit ONLY by OHS-AC targets (report-only). A seed run has no drop ids (its templates are split by split_quarantine)."""
    non, ac = set(), set()
    for tg, ms in hits.items():
        (ac if tg in AC_TARGETS else non).update(k for d in ms.values() for k in d)
    if run_name == "seed":
        return {"binding": [], "ohsac_report_only": [], "units": {"binding": 0, "ohsac_report_only": 0},
                "capture": {"ac_targets": list(AC_TARGETS), "module_sha256": _this_sha()}}
    only = ac - non
    b = sorted({r for k in non for r in units[k]["rows"]})
    ro = sorted({r for k in only for r in units[k]["rows"]} - set(b))
    return {"binding": b, "ohsac_report_only": ro, "units": {"binding": len(non), "ohsac_report_only": len(only)},
            "capture": {"ac_targets": list(AC_TARGETS), "module_sha256": _this_sha()}}


def install_g13_capture(G, info: dict | None = None) -> None:
    """Wrap g13_c2's derive_hits / _record / withdraw_waivers in THIS process (idempotent). The module file on disk is untouched. `info` = the
    ruling_gate.require result: it is sealed into every captured split (a split captured by a call that passes none carries ruling null)."""
    if getattr(G, "_opt3_capture", False):
        return
    orig_derive, orig_record, orig_withdraw = G.derive_hits, G._record, G.withdraw_waivers
    calls: list = []

    def derive_hits(run_name, units, hits, eng):
        out = orig_derive(run_name, units, hits, eng)
        out[CLASSES_KEY] = classes_from_hits(run_name, units, hits)
        calls.append(out)
        return out

    def _record(*a, **k):
        calls.clear()
        rec = orig_record(*a, **k)
        if calls:                                    # the LAST derive_hits call of _record is the post-A53 one that fills the record
            rec[CLASSES_KEY] = seal_classes(calls[-1][CLASSES_KEY], rec, info)
        return rec

    def withdraw_waivers(rec, unwaived, late):
        did = orig_withdraw(rec, unwaived, late)
        if did and isinstance(unwaived, dict) and CLASSES_KEY in unwaived:
            rec[CLASSES_KEY] = seal_classes(unwaived[CLASSES_KEY], rec, info)   # the no-waiver hits: drop_ids went back to them, so does the split
        return did

    G.derive_hits, G._record, G.withdraw_waivers = derive_hits, _record, withdraw_waivers
    G._opt3_capture = True


# ------------------------------------------------------------------------------------------------ reading a log's split
def split_log(d) -> dict:
    """{"all", "binding", "report_only" (sets), "mode"} of one drop list. mode: "by_class" (the capture record, checked), "no_ac_record" (a log
    or plain list with no OHS-AC step: every drop is non-OHS-AC), "ac_only_run" (a quick OHS-AC-only record: every drop is report-only).
    SplitRefused when the log has an OHS-AC record and no / a wrong split."""
    if not isinstance(d, dict):
        raise SplitRefused("drop list is not a JSON object")
    got = next((d[k] for k in ("drop_ids", "training_ids_to_drop", "ids") if isinstance(d.get(k), list)), None)
    if got is None:
        raise SplitRefused("no drop id list (drop_ids / training_ids_to_drop / ids)")
    allv, name = {str(x) for x in got}, d.get("set") or "a drop list"
    if d.get("mode") == "ohsac_only":
        return {"all": allv, "binding": set(), "report_only": set(allv), "mode": "ac_only_run"}
    cl = d.get(CLASSES_KEY)
    if isinstance(cl, dict):
        b, ro = {str(x) for x in cl.get("binding") or []}, {str(x) for x in cl.get("ohsac_report_only") or []}
        cap = cl.get("capture") or {}
        if tuple(cap.get("ac_targets") or ()) != AC_TARGETS:
            raise SplitRefused(f"{name}: {CLASSES_KEY} was captured for other OHS-AC targets than {AC_TARGETS}")
        if not isinstance(cap.get("ruling"), dict) or not cap["ruling"].get("id"):
            raise SplitRefused(f"{name}: {CLASSES_KEY} was captured without an owner-ruling id (not made by g13_c2_opt3.py --ohsac-report-only)")
        if cap.get("split_sha256") is None or cap.get("set") is None:
            raise SplitRefused(f"{name}: {CLASSES_KEY} is not sealed (no capture.set / split_sha256): it was not made by g13_c2_opt3.py; "
                               "re-run the log with g13_c2_opt3.py --ohsac-report-only <ruling id>")
        if cap.get("set") != d.get("set") or cap.get("run") != d.get("run"):
            raise SplitRefused(f"{name}: {CLASSES_KEY} was captured for set {cap.get('set')!r} / run {cap.get('run')!r}, not this log")
        if cap.get("log_tool_sha256") != d.get("tool_sha256"):
            raise SplitRefused(f"{name}: {CLASSES_KEY} was captured by another g13_c2.py (tool sha256 differs from the log's)")
        if cap["split_sha256"] != split_digest(cap["set"], cap["run"], b, ro, cap.get("log_tool_sha256")):
            raise SplitRefused(f"{name}: {CLASSES_KEY} was edited after the capture (seal differs)")
        if b & ro or (b | ro) != allv:
            raise SplitRefused(f"{name}: {CLASSES_KEY} does not add up to drop_ids (binding {len(b)}, report-only {len(ro)}, drop_ids "
                               f"{len(allv)}): the log changed after the capture; re-run it with g13_c2_opt3.py")
        return {"all": allv, "binding": b, "report_only": ro, "mode": "by_class", "ruling": dict(cap["ruling"]),
                "split_sha256": cap["split_sha256"]}
    if "ohsac" not in d:
        return {"all": allv, "binding": set(allv), "report_only": set(), "mode": "no_ac_record"}
    raise SplitRefused(f"{name}: the log has an OHS-AC record but no {CLASSES_KEY}; the split cannot be recovered from counts: re-run it "
                       "with g13_c2_opt3.py --ohsac-report-only <ruling id>")


class UseLog:
    """What the option read in this process: per-log counts and sha256 of the id lists (the manifest block). No ids, no text."""

    def __init__(self, info: dict | None = None):
        self.info = info                         # the ruling of THIS run (ruling_gate.require); a capture under another ruling is refused
        self.logs: list[dict] = []
        self.seed: dict = {}

    def add(self, path, d, s) -> dict:
        if self.info is not None and s["mode"] == "by_class":
            r = s.get("ruling") or {}
            if r.get("id") != self.info["id"] or r.get("block_sha256") != self.info["block_sha256"]:
                raise SplitRefused(f"{Path(str(path)).name}: the split was captured under ruling {r.get('id')!r} (block sha256 "
                                   f"{str(r.get('block_sha256'))[:12]}), this run is armed by {self.info['id']!r} ({self.info['block_sha256'][:12]}): "
                                   "re-run the capture or use the same ruling")
        row = {"file": Path(str(path)).name, "set": d.get("set") if isinstance(d, dict) else None, "mode": s["mode"],
               "captured_under": (s.get("ruling") or {}).get("id"), "split_sha256": s.get("split_sha256"),
               "drop_ids": len(s["all"]), "binding": len(s["binding"]), "ohsac_report_only": len(s["report_only"]),
               "binding_sha256": _sha_ids(s["binding"]), "ohsac_report_only_sha256": _sha_ids(s["report_only"])}
        self.logs.append(row)
        return row

    def block(self, info: dict) -> dict:
        return {"ruling": info, "armed_by": "mix_c2_opt3 / c2_select_opt3 / g13_c2_opt3 with --ohsac-report-only <ruling id>",
                "report_only_targets": list(AC_TARGETS),
                "binding_targets": "every other target (OHS-4 child, sob, DI, public, C2 dev, A53 / A31 b rules as before)",
                "drop_ids_field_unchanged": True, "logs": list(self.logs), "seed_quarantines": dict(self.seed),
                "totals": {"logs": len(self.logs), "binding_ids_sum": sum(r["binding"] for r in self.logs),
                           "ohsac_report_only_ids_sum": sum(r["ohsac_report_only"] for r in self.logs)},
                "not_changed": ["A61 final-mix 8.5 source gate (--exports all, stricter)", "G13 against OHS-4 and every non-OHS-AC target",
                                "completeness / staleness checks of the G13 logs", "A42-D 13.1 never-train guard"],
                "module_sha256": _this_sha()}


def binding_drop_ids(ilog, files, use: UseLog | None = None) -> tuple[set, list]:
    """mixer.decontam_drop_ids with the OHS-AC report-only ids left out: (binding ids, used). `used` entries carry the counts."""
    ids, used = set(), []
    for f in files or []:
        d = ilog.json(f)
        s = split_log(d)
        ids |= s["binding"]
        row = (use or UseLog()).add(f, d, s)
        used.append({"file": str(f), "ids": len(s["all"]), "binding_ids": len(s["binding"]),
                     "ohsac_report_only_ids": len(s["report_only"]), "mode": row["mode"]})
    return ids, used


# ------------------------------------------------------------------------------------------------ seed quarantines
def is_report_only_entry(q: dict) -> bool:
    """A quarantined template is report-only when every target that hit it is an OHS-AC target. No hit record = binding (strict)."""
    tg = set((q.get("hits") or {}).keys()) if isinstance(q, dict) else set()
    return bool(tg) and tg <= set(AC_TARGETS)


def split_quarantine(entries) -> tuple[list, list]:
    """(binding entries, report-only entries) of a seed log's `quarantine`."""
    b, ro = [], []
    for q in entries or []:
        (ro if is_report_only_entry(q) else b).append(q)
    return b, ro


def binding_seed_log(d: dict) -> dict:
    """A seed log with the OHS-AC-only quarantines moved out of `quarantine` (kept as ohsac_report_only_quarantine: template ids and lines)."""
    b, ro = split_quarantine(d.get("quarantine"))
    out = dict(d)
    out["quarantine"], out["quarantine_templates"] = b, len(b)
    out["ohsac_report_only_quarantine"] = [{k: q.get(k) for k in ("template_id", "file", "line", "hits")} for q in ro]
    return out


def install_seed(GEN, use: UseLog | None = None) -> None:
    """Wrap gen_full_c2.g13_seed_templates: templates quarantined ONLY by OHS-AC targets are not removed (the logs/ file carries the hit
    targets; the VM mirror has none, so a mirror stays fully binding). Idempotent."""
    if getattr(GEN, "_opt3_seed", False):
        return
    orig = GEN.g13_seed_templates

    def g13_seed_templates(fam, root=None):
        r = orig(fam, root)
        f = GEN.G13_SEED_DIR / f"c2_seed_{fam}.json"
        if r is None or not f.is_file():
            return r
        ro = {(q.get("file"), q.get("line"), q.get("template_id")) for q in split_quarantine(json.loads(f.read_bytes()).get("quarantine"))[1]}
        keep = [t for t in r["templates"] if (t["file"], t["line"], t["template_id"]) not in ro]
        if use is not None:
            use.seed[fam] = {"binding": len(keep), "ohsac_report_only": len(r["templates"]) - len(keep)}
        return {**r, "templates": keep, "n_templates": len(keep), "ohsac_report_only_templates": len(r["templates"]) - len(keep)}

    orig_report = getattr(GEN, "g13_report", None)

    def g13_report(fam, ids, kit):
        r = orig_report(fam, ids, kit)
        if r is None:
            return r
        f = GEN.G13_SEED_DIR / f"c2_seed_{fam}.json"
        ro = split_quarantine(json.loads(f.read_bytes()).get("quarantine"))[1] if f.is_file() else []
        return {**r, REPORT_KEY: {"ruling": (use.info if use is not None else None), "templates_not_applied": [
            {k: q.get(k) for k in ("template_id", "file", "line", "hits")} for q in ro], "module_sha256": _this_sha()}}

    GEN.g13_seed_templates, GEN._opt3_seed = g13_seed_templates, True
    if orig_report is not None:
        GEN.g13_report = g13_report


def seed_counts(log_dir: Path) -> dict:
    """{family: {"binding": n, "ohsac_report_only": n}} from logs/decontam_counts/c2_seed_*.json (counts only)."""
    out = {}
    for p in sorted(Path(log_dir).glob("c2_seed_*.json")):
        try:
            d = json.loads(p.read_bytes())
        except (OSError, ValueError):
            continue
        b, ro = split_quarantine(d.get("quarantine"))
        out[p.stem[len("c2_seed_"):]] = {"binding": len(b), "ohsac_report_only": len(ro)}
    return out


# ------------------------------------------------------------------------------------------------ installing into mix_c2 / c2_select
def install_select(sel, use: UseLog, info: dict | None = None) -> None:
    """c2_select --exclude-ids: the original runs its own log checks and returns the full union; the binding union replaces it. Every
    select_<FAM>.json written afterwards carries the `ohsac_report_only` block (ruling, per-log counts and shas), so a selection made under the
    option can be told from a strict one."""
    if getattr(sel, "_opt3", False):
        return
    orig = sel.drop_ids_of
    orig_write = sel.write_select

    def drop_ids_of(ilog, files):
        full = orig(ilog, files)
        ids, _used = binding_drop_ids(ilog, list(files or []), use)
        if not ids <= full:
            raise SplitRefused("binding ids are not a subset of the log's drop ids (internal)")
        return ids

    def write_select(fam, rec, extra):
        return orig_write(fam, rec, {**extra, REPORT_KEY: use.block(use.info or info)})

    sel.drop_ids_of, sel.write_select, sel._opt3 = drop_ids_of, write_select, True


def install_mixer(m, info: dict, use: UseLog, log_dir: Path | None = None) -> None:
    """mix_c2: g13_drop_ids (G13 logs + pool_drops_r1 + the deny lists as the mixer passes them) returns binding ids; the report and the
    manifest gain `ohsac_report_only`. 8.5 (gated_membership / binding_ids / remove_sources) is not touched."""
    if getattr(m, "_opt3", False):
        return
    orig_drop, orig_write, orig_dry = m.g13_drop_ids, m.write_outputs, m.dry_report

    def g13_drop_ids(a, ilog, files, probs):
        full, used = orig_drop(a, ilog, files, probs)            # the original log checks first (--final refuses on any problem)
        ids, bused = binding_drop_ids(ilog, list(files or []), use)
        if not ids <= full:
            raise SplitRefused("binding ids are not a subset of the G13 drop ids (internal)")
        return ids, bused

    def _block():
        blk = use.block(info)
        if log_dir is not None and not use.seed:
            use.seed.update(seed_counts(log_dir))
            blk["seed_quarantines"] = dict(use.seed)
        blk["selections"] = select_stamps(m.c2_select.OUT, info)
        return blk

    def write_outputs(a, rep, rows, rels):
        if getattr(a, "remove_sources", None):
            blk = removal_block(m.OUT_MAN, info)                  # --remove-sources: the G13 logs are not re-read; the written mix's block is kept
        else:
            blk = _block()
        rep[REPORT_KEY] = blk
        orig_wj = m.c2io.write_json

        def wj(path, obj, *x, **k):
            if Path(path) == Path(m.OUT_MAN) and isinstance(obj, dict):
                obj = {**obj, REPORT_KEY: blk}
            return orig_wj(path, obj, *x, **k)

        m.c2io.write_json = wj
        try:
            return orig_write(a, rep, rows, rels)
        finally:
            m.c2io.write_json = orig_wj

    def dry_report(rep):
        rep[REPORT_KEY] = _block()
        return orig_dry(rep)

    m.g13_drop_ids, m.write_outputs, m.dry_report, m._opt3 = g13_drop_ids, write_outputs, dry_report, True


def select_stamps(out_dir, info: dict | None) -> dict:
    """{family: "option3 (<ruling id>)" | "strict" | "other ruling (<id>)"} for the select_<FAM>.json files on disk (counts / ids of rulings only)."""
    out = {}
    for p in sorted(Path(out_dir).glob("select_*.json")):
        try:
            d = json.loads(p.read_bytes())
        except (OSError, ValueError):
            out[p.stem[len("select_"):]] = "unreadable"
            continue
        blk = d.get(REPORT_KEY) if isinstance(d, dict) else None
        rid = ((blk or {}).get("ruling") or {}).get("id")
        out[p.stem[len("select_"):]] = ("strict" if not blk else
                                        f"option3 ({rid})" if info is None or rid == info["id"] else f"other ruling ({rid})")
    return out


def removal_block(man_path, info: dict | None) -> dict:
    """--remove-sources under the option: the written mix's `ohsac_report_only` block carried over unchanged (the removal never re-reads the G13
    logs). Refused when the written manifest has none (the mix was made strict) or names another ruling."""
    try:
        man = json.loads(Path(man_path).read_bytes())
    except (OSError, ValueError):
        raise SystemExit("--remove-sources under --ohsac-report-only: the written mix manifest is unreadable. Nothing was changed.") from None
    blk = man.get(REPORT_KEY) if isinstance(man, dict) else None
    if not isinstance(blk, dict):
        raise SystemExit("--remove-sources under --ohsac-report-only: the written mix was made without the option (its manifest has no "
                         f"{REPORT_KEY} block); remove with the plain mix_c2.py. Nothing was changed.")
    if info is not None and (blk.get("ruling") or {}).get("id") != info["id"]:
        raise SystemExit(f"--remove-sources: the written mix was made under ruling {(blk.get('ruling') or {}).get('id')!r}, not {info['id']!r}. "
                         "Nothing was changed.")
    return {**blk, "removal_pass": {"carried_over_unchanged": True, "module_sha256": _this_sha()}}


# ------------------------------------------------------------------------------------------------ wrappers
def _strip_and_gate(argv: list[str]) -> tuple[list[str], dict | None]:
    argv, rid = rg.pop_flag(list(argv), "--ohsac-report-only")
    if rid is None:
        return argv, None
    return argv, rg.require(rid, rg.OPT3_MARKER)


def _refuse_plain_removal(m) -> None:
    try:
        man = json.loads(Path(m.OUT_MAN).read_bytes())
    except (OSError, ValueError):
        return                                       # no readable manifest: the original tool reports it
    if isinstance(man, dict) and REPORT_KEY in man:
        raise SystemExit(f"--remove-sources without --ohsac-report-only: the written mix was made under owner option 3 (its manifest has an "
                         f"{REPORT_KEY} block). Run mix_c2_opt3.py --remove-sources ... --ohsac-report-only <ruling id> so the disclosure "
                         "is carried over. Nothing was changed.")


def launch(tool: str, argv: list[str] | None = None):
    """Entry point of the three wrappers. No --ohsac-report-only: the original tool's main(argv) runs unchanged."""
    cb = rg.lean_on_path()
    argv, info = _strip_and_gate(sys.argv[1:] if argv is None else argv)
    if tool == "g13":
        import g13_c2 as G
        if info is not None:
            install_g13_capture(G, info)
        return G.main(argv)
    if tool == "select":
        import c2_select as sel
        if info is not None:
            install_select(sel, UseLog(info), info)
        return sel.main(argv)
    if tool == "genfull":
        import gen_full_c2 as GEN
        if info is not None:
            install_seed(GEN, UseLog(info))
        return GEN.main(argv)
    if tool == "mix":
        import mix_c2 as m
        if info is not None:
            install_mixer(m, info, UseLog(info), log_dir=cb.parent / "logs" / "decontam_counts")
        elif any(x == "--remove-sources" or x.startswith("--remove-sources=") for x in argv):
            _refuse_plain_removal(m)                  # a mix written under the option is changed only by the wrapper with the flag
        return m.main(argv)
    raise SystemExit(f"unknown tool {tool!r}")


# ------------------------------------------------------------------------------------------------ library CLI (counts only)
def report(log_dir: Path, patterns: list[str]) -> list[dict]:
    rows = []
    for pat in patterns:
        for p in sorted(Path(log_dir).glob(pat)):
            try:
                d = json.loads(p.read_bytes())
                s = split_log(d)
                rows.append({"file": p.name, "mode": s["mode"], "drop_ids": len(s["all"]), "binding": len(s["binding"]),
                             "ohsac_report_only": len(s["report_only"])})
            except SplitRefused as e:
                rows.append({"file": p.name, "mode": "refused", "why": str(e)[:160]})
            except (OSError, ValueError) as e:
                rows.append({"file": p.name, "mode": "unreadable", "why": type(e).__name__})
    return rows


def capture_plan(log_dir: Path, patterns=("c2_cand_*.json", "c2_carry_*.json", "c2_final*.json")) -> dict:
    """What the capture batch (g13_c2_opt3.py --ohsac-report-only <id>) must produce, from the strict logs on disk (counts only, nothing written).
    Per log: whether it already holds a valid split (then nothing to re-run), its strict drop count, the OHS-AC hit units, and the bounds the
    counts alone allow for the binding / report-only split. The exact split is only knowable from the capture (ids per target are not in the
    log); the bounds use the largest single non-OHS-AC target-and-method count (a lower bound of the binding ids) and the strict drop count."""
    logs, seen = [], set()
    for pat in patterns:
        for p in sorted(Path(log_dir).glob(pat)):
            if p.name in seen:
                continue
            seen.add(p.name)
            try:
                d = json.loads(p.read_bytes())
            except (OSError, ValueError):
                logs.append({"file": p.name, "needs_capture": True, "why": "unreadable"})
                continue
            if not isinstance(d, dict) or d.get("tool") is None:
                continue
            try:
                s = split_log(d)
                have = s["mode"] == "by_class"
                why = None
            except SplitRefused as e:
                have, why = False, str(e)[:100]
            allv = [str(x) for x in d.get("drop_ids") or []]
            nonac_rows = nonac_units = 0
            for tg, ms in (d.get("counts_by_target_and_method") or {}).items():
                if tg in AC_TARGETS:
                    continue
                for c in ms.values():
                    nonac_rows, nonac_units = max(nonac_rows, int(c.get("rows") or 0)), max(nonac_units, int(c.get("units") or 0))
            ac = d.get("ohsac") if isinstance(d.get("ohsac"), dict) else None
            row = {"file": p.name, "set": d.get("set"), "run": d.get("run"), "complete": d.get("complete"),
                   "has_ohsac_record": ac is not None, "needs_capture": ac is not None and not have, "valid_split_present": have,
                   "rows": d.get("rows"), "units": d.get("units"), "strict_drop_rows": len(allv), "strict_drop_units": d.get("drop_units"),
                   "strict_drop_ids_sha256": _sha_ids(allv), "ohsac_hit_units": (ac or {}).get("hit_units"),
                   "binding_rows_at_least": min(nonac_rows, len(allv)), "binding_rows_at_most": len(allv),
                   "report_only_rows_at_most": max(0, len(allv) - min(nonac_rows, len(allv))),
                   "rows_left_under_option3_at_least": (d.get("rows") or 0) - len(allv),
                   "rows_left_under_option3_at_most": (d.get("rows") or 0) - min(nonac_rows, len(allv))}
            qf = Path(log_dir) / f"acquick_{d.get('set')}.json"       # the OHS-AC-only quick record of the same set (ids of units hit by OHS-AC)
            try:
                q = json.loads(qf.read_bytes()) if qf.is_file() else None
            except (OSError, ValueError):
                q = None
            if isinstance(q, dict) and q.get("mode") == "ohsac_only" and isinstance(q.get("drop_ids"), list):
                qa = {str(x) for x in q["drop_ids"]}
                sa = set(allv)
                row["acquick"] = {"file": qf.name, "ohsac_rows": len(qa), "ohsac_rows_not_in_strict": len(qa - sa),
                                  "not_hit_by_ohsac_so_binding": len(sa - qa), "hit_by_ohsac_may_be_report_only": len(sa & qa)}
                row["binding_rows_at_least"] = max(row["binding_rows_at_least"], len(sa - qa))
                row["report_only_rows_at_most"] = min(row["report_only_rows_at_most"], len(sa & qa))
                row["rows_left_under_option3_at_most"] = (d.get("rows") or 0) - row["binding_rows_at_least"]
            if why and ac is not None:
                row["why"] = why
            logs.append(row)
    need = [r["file"] for r in logs if r.get("needs_capture")]
    return {"logs": logs, "needs_capture": need,
            "must_produce": {"key": CLASSES_KEY, "per_log": "drop_ids_by_class = {binding: [row ids], ohsac_report_only: [row ids], units: {binding, "
                             "ohsac_report_only}, capture: {ac_targets, module_sha256, set, run, log_tool_sha256, ruling {id, block_sha256, "
                             "prereg_sha256}, split_sha256}}",
                             "invariants": ["binding and ohsac_report_only are disjoint", "binding union ohsac_report_only == drop_ids of the log",
                                            "ac_targets == " + str(list(AC_TARGETS)), "capture.set / run / log_tool_sha256 equal the log's own",
                                            "capture.ruling.id == the id given to the later select / mix runs"],
                             "if_inputs_unchanged": "drop_ids of the new log equals strict_drop_ids_sha256 of the old one (same sorted ids); a "
                                                    "different sha means an input or a tool changed since that log, and the new log is the one that counts"},
            "totals": {"logs": len(logs), "needs_capture": len(need), "strict_drop_rows_sum": sum(r["strict_drop_rows"] for r in logs),
                       "rows_sum": sum((r.get("rows") or 0) for r in logs)}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report", help="counts-only table of what the split gives for the logs on disk (writes nothing)")
    r.add_argument("--log-dir", default=None)
    r.add_argument("--glob", nargs="*", default=["c2_*.json", "acquick_c2_*.json"])
    r.add_argument("--capture-plan", action="store_true",
                   help="instead of the table: what the capture batch must produce (bounds from counts; candidates / carry / final logs only)")
    s = sub.add_parser("seed-split", help="write a seed log with the OHS-AC-only quarantines moved out (never overwrites)")
    s.add_argument("--log", required=True)
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "report":
        ld = Path(a.log_dir) if a.log_dir else rg.lean_on_path().parent / "logs" / "decontam_counts"
        if a.capture_plan:
            print(json.dumps(capture_plan(ld), indent=1))
            return 0
        for row in report(ld, a.glob):
            print(json.dumps(row))
        print(json.dumps({"seed_quarantines": seed_counts(ld)}))
        return 0
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"{out} exists; seed-split never overwrites")
    out.write_text(json.dumps(binding_seed_log(json.loads(Path(a.log).read_bytes())), indent=1, sort_keys=True), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
