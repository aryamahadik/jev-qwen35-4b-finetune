"""T63 POOL WRITER: the only code that turns kept rows into a pool file. Opus ruling Q3 (3a), recorded "before any pool rows" (Sun 18 Oct 2026).

Ruling (RULINGS_T59_T60_T63.md, Q3 / 3a): every EXISTS-B row (EX-B1 and EX-B2) is built only from the sha-bound L-0 image-record stdlib symbol
export, every LIC row only from the hashed Opus table T63-LIC-TABLE. So this writer
  * requires the literal `standin=False` (a stand-in, test or dry run never reaches a pool file);
  * REFUSES any row (and any source) whose sha is a FIXTURE sha, and any fixture-flagged source;
  * REFUSES EX-B rows without the real export + the L-0 image record, and LIC rows without the real table + the Opus table record (`SourceMissing`
    names each missing file and who produces it; nothing is faked, nothing is written);
  * requires the export sha / image id / table sha on the rows to equal the ones RECORDED outside the family (L-0 image record, Opus table record);
  * re-reads every EX-B row against the real export (membership, the shown B1 list) and every LIC row against the real table (cell, label, cell used once);
  * accepts only stamped rows (G13 verdict clean, not the test double's stamp), writes all-or-nothing, and never overwrites a batch file.

No row exists yet (every T63 row waits for the target-set freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record),
and neither production source exists yet (see SOURCES): this writer is code only and was run on CPU tests with clearly flagged test sources.
"""
import functools
import json
import os

from LP_COMMON import paths, util

from . import exists, lic, schema

# role -> (file name inside the L-0 folder by default, who produces it). The folder is overridable (`base_dir`); the NAMES are what the writer reads.
SOURCES = {
    "stdlib_export": ("T63_STDLIB_EXPORT.json",
                      "L-0 (image build: runner.stdlib_export.python / .node / .go on the pinned image, 3 identical runs, names only, DECLARED sha256, "
                      "not a fixture; gated by the Wed 21 Oct sandbox sign-off)"),
    "image_record": ("L0_IMAGE_RECORD.json",
                     "L-0 (the image record of the same pinned image; must record `image_id` and `stdlib_export_sha256`, written when the export is hashed)"),
    "lic_table": ("T63_LIC_TABLE.json",
                  "a SEPARATE fresh Opus 5.5 high session (LANE_L-P licence-ID table owner, T63-B6): T63-LIC-TABLE, every dep x project x use x dist cell, "
                  "identifiers only, DECLARED sha256, not a fixture"),
    "lic_table_record": ("T63_LIC_TABLE_RECORD.json",
                         "the same Opus session (its hashed record of the table: `table_id` = T63-LIC-TABLE and `sha256`, written before any LIC row)"),
}
EX_B_SUBS = ("EX-B1", "EX-B2")
TABLE_ID = "T63-LIC-TABLE"


class PoolRefused(ValueError):
    """The writer refuses; nothing was written."""


class SourceMissing(PoolRefused):
    """A production source file does not exist (yet). `.missing` = [(role, path, producer)]."""

    def __init__(self, missing):
        self.missing = list(missing)
        super().__init__("MISSING production source(s), nothing written: " + "; ".join(
            "%s = %s (produced by %s)" % (role, path, who) for role, path, who in self.missing))


# ---- fixtures ---------------------------------------------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=1)
def fixture_shas():
    """The shas of the family's own FIXTURE export and FIXTURE licence table (dry run / tests). No row built from them may reach a pool."""
    from . import dryrun                                              # lazy: dryrun imports the generator, which imports this module
    return frozenset((dryrun.fixture_exports().sha, lic.fixture_table().sha))


def refuse_fixture_sha(sha, what):
    if sha in fixture_shas():
        raise PoolRefused("%s sha %s is a FIXTURE sha (dry run / tests only): refused" % (what, sha))


# ---- sources ----------------------------------------------------------------------------------------------------------------------------
def source_paths(base_dir=None):
    base = base_dir or paths.L0
    return {role: os.path.join(base, fname) for role, (fname, _who) in SOURCES.items()}


def _missing(roles, pmap):
    return [(r, pmap[r], SOURCES[r][1]) for r in roles if not os.path.isfile(pmap[r])]


def _read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_sources(base_dir=None, need_export=True, need_table=True):
    """-> {"exports", "image_record"} and/or {"table", "table_record"}. Raises `SourceMissing` listing every missing file with its producer."""
    pmap = source_paths(base_dir)
    roles = (["stdlib_export", "image_record"] if need_export else []) + (["lic_table", "lic_table_record"] if need_table else [])
    miss = _missing(roles, pmap)
    if miss:
        raise SourceMissing(miss)
    out = {}
    if need_export:
        out["exports"] = exists.ExportSet.load(pmap["stdlib_export"])
        out["image_record"] = _read_json(pmap["image_record"])
    if need_table:
        out["table"] = lic.LicTable.load(pmap["lic_table"])
        out["table_record"] = _read_json(pmap["lic_table_record"])
    return out


def check_export_binding(ex, rec):
    """The export must be real, not a fixture, and be the one the L-0 image record names (sha and image id)."""
    try:
        ex.require_real()
    except ValueError as e:
        raise PoolRefused("stdlib export refused: %s" % e)
    refuse_fixture_sha(ex.sha, "stdlib export")
    if not isinstance(rec, dict) or not rec.get("stdlib_export_sha256") or not rec.get("image_id"):
        raise PoolRefused("the L-0 image record must record `image_id` and `stdlib_export_sha256`")
    if rec["stdlib_export_sha256"] != ex.sha:
        raise PoolRefused("the export sha is not the one recorded by the L-0 image record")
    if rec["image_id"] != ex.image_id:
        raise PoolRefused("the export's image id is not the one recorded by the L-0 image record")


def check_table_binding(tb, rec):
    """The table must be real, not a fixture, and be the one the Opus table record names."""
    try:
        tb.require_real()
    except ValueError as e:
        raise PoolRefused("licence table refused: %s" % e)
    refuse_fixture_sha(tb.sha, "licence table")
    if not isinstance(rec, dict) or rec.get("table_id") != TABLE_ID or not rec.get("sha256"):
        raise PoolRefused("the Opus table record must name `table_id` = %s and `sha256`" % TABLE_ID)
    if rec["sha256"] != tb.sha:
        raise PoolRefused("the licence table sha is not the one recorded by the Opus table record")


# ---- rows -------------------------------------------------------------------------------------------------------------------------------
def _row_shas(row):
    """Every export / table sha a row carries (spec, witness, manifest pins)."""
    spec, w, pins = row.get("spec") or {}, row.get("witness_inputs") or {}, (row.get("manifest") or {}).get("pins") or ""
    out = [spec.get("export_sha"), spec.get("table_sha"), w.get("export_sha"), w.get("table_sha")]
    if ";export:" in pins:
        out.append(pins.split(";export:", 1)[1])
    return [s for s in out if s]


def _ex_b_problems(row, ex):
    spec, w = row["spec"], row["witness_inputs"]
    why = []
    if not (spec.get("export_sha") == w.get("export_sha") == ex.sha):
        why.append("export_sha_mismatch")
    if spec.get("image_id") != ex.image_id:
        why.append("image_id_mismatch")
    if (row.get("manifest") or {}).get("pins") != "image:%s;export:%s" % (ex.image_id, ex.sha):
        why.append("pins_mismatch")
    mods = ex.modules(spec["lang"]) if spec.get("lang") in ex.langs else {}
    full = mods.get(spec.get("module"))
    if full is None:
        return why + ["module_not_in_export"]
    if row["gold"] != exists.gold_b(spec, ex):
        why.append("gold_not_export_membership")
    if spec["sub"] == "EX-B1":
        srt = sorted(full)
        lo_hi = spec.get("range")
        want = [n for n in srt if lo_hi[0] <= n <= lo_hi[1]] if lo_hi else srt
        if spec.get("shown") != want:
            why.append("b1_list_not_export_slice")
    return why


def _lic_problems(row, tb, seen):
    spec, w = row["spec"], row["witness_inputs"]
    why = []
    if not (spec.get("table_sha") == w.get("table_sha") == tb.sha):
        why.append("table_sha_mismatch")
    cell = (spec.get("dep"), spec.get("project"), spec.get("use"), spec.get("dist"))
    k = lic.key(*cell)
    if k not in tb.cells:
        return why + ["cell_not_in_table"]
    if row["meta"].get("construction_id") != "LC:" + k:
        why.append("cell_id_mismatch")
    if row["gold"] != tb.label(*cell):
        why.append("gold_not_table_label")
    if k in seen:
        why.append("cell_used_twice")
    seen.add(k)
    return why


def row_problems(row, ex=None, tb=None, seen_cells=None):
    """Reasons the writer refuses ONE row ([] = writable). `seen_cells` is the 'each LIC cell once' ledger of the batch."""
    why = ["schema_" + p.replace(" ", "_") for p in schema.validate_row(row)]
    if why:
        return why
    st = row.get("stamp")
    if not isinstance(st, dict) or st.get("verdict") != "clean" or st.get("row_id") != row["row_id"] or not st.get("registry_sha") or not st.get("generator_sha"):
        why.append("not_stamped_clean")
    elif st.get("method_set_version") == "test-double" or set(st["registry_sha"]) == {"0"}:
        why.append("test_double_stamp")                                  # the pipeline's TEST DOUBLE hook marks its stamps; they are never G13 evidence
    if any(s in fixture_shas() for s in _row_shas(row)):
        why.append("fixture_sha")
    spec = row["spec"]
    if row["head"] == "EXISTS" and spec.get("sub") in EX_B_SUBS:
        why += ["no_export"] if ex is None else _ex_b_problems(row, ex)
    elif row["head"] == "LIC":
        why += ["no_table"] if tb is None else _lic_problems(row, tb, seen_cells if seen_cells is not None else set())
    return why


# ---- the writer -------------------------------------------------------------------------------------------------------------------------
def write_pool(rows, out_path, *, standin, sources=None, base_dir=None):
    """Write one batch of kept rows to `out_path` (JSON lines, write-once, atomic). All-or-nothing: any refusal raises `PoolRefused` and writes nothing.

    standin   must be the literal False (tests and dry runs are `True` and are refused).
    sources   the dict `load_sources` returns ({"exports", "image_record"} for EX-B rows, {"table", "table_record"} for LIC rows); when None it is loaded
              from `base_dir` (default: the L-0 folder), and a missing file raises `SourceMissing` naming the file and its producer.
    Batches without EX-B and LIC rows need no source."""
    if standin is not False:
        raise PoolRefused("the pool writer requires standin=False (got %r): stand-in rows never reach a pool" % (standin,))
    rows = list(rows)
    if not rows:
        raise PoolRefused("no rows")
    if os.path.exists(out_path):
        raise PoolRefused("%s exists: batch files are write-once" % out_path)
    need_ex = any(r.get("head") == "EXISTS" and (r.get("spec") or {}).get("sub") in EX_B_SUBS for r in rows)
    need_tb = any(r.get("head") == "LIC" for r in rows)
    if need_ex or need_tb:
        if sources is None:
            sources = load_sources(base_dir, need_export=need_ex, need_table=need_tb)
        else:
            pmap = source_paths(base_dir)
            have = {"stdlib_export": "exports", "image_record": "image_record", "lic_table": "table", "lic_table_record": "table_record"}
            roles = (["stdlib_export", "image_record"] if need_ex else []) + (["lic_table", "lic_table_record"] if need_tb else [])
            miss = [(r, pmap[r], SOURCES[r][1]) for r in roles if sources.get(have[r]) is None]
            if miss:
                raise SourceMissing(miss)
    sources = sources or {}
    ex = sources.get("exports") if need_ex else None
    tb = sources.get("table") if need_tb else None
    if need_ex:
        check_export_binding(ex, sources["image_record"])
    if need_tb:
        check_table_binding(tb, sources["table_record"])
    seen, bad = set(), []
    for r in rows:
        why = row_problems(r, ex, tb, seen)
        if why:
            bad.append((r.get("row_id"), why))
    if bad:
        raise PoolRefused("%d of %d rows refused, nothing written; first: %s" % (len(bad), len(rows), "; ".join("%s: %s" % (i, ",".join(w)) for i, w in bad[:5])))
    lines = [json.dumps(r, sort_keys=True, ensure_ascii=True) for r in rows]
    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, out_path)
    return {"path": out_path, "rows": len(rows), "file_sha256": util.sha256_file(out_path),
            "export_sha": ex.sha if ex else None, "image_id": ex.image_id if ex else None, "table_sha": tb.sha if tb else None,
            "ex_b_rows": sum(1 for r in rows if r["head"] == "EXISTS" and r["spec"].get("sub") in EX_B_SUBS), "lic_rows": sum(1 for r in rows if r["head"] == "LIC")}
