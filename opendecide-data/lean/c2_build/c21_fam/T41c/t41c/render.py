"""Realise a spec as source-tagged spans plus an anchor map.

Program writes: the system/developer facts block, cwd / lane / rules-file lines, the git-remote and manifest
context spans, the serialisation skeleton, the hidden-variant transforms, the nested-provenance markers.
Pools (Claude-authored) write: the user turn, background items, fillers and directive cores/wrappers.

Output: Rendered(spans, anchors). `export_for_b` is the ONLY view solver B gets: rendered text plus anchors, with
no spec, label, risk, tier, subtype or flag. Anchor roles (G0-lite 2, solver B):
  src_tag, attr, directive_span, addressee, tool_role, effect, host(sub dest|index|cred_scope), package,
  path(sub carrier|delete|overwrite|source), target, delegation_pointer, lane_tag, and the fact anchors
  fact.declared_hosts / declared_manifest / declared_workspace / declared_targets / declared_tools /
  repo_remotes / visible_manifest_file / repo_root / task_targets / task_tools.
An anchor is (role, value, span, start, end, did, sub, enc); `enc` is "base64" when the value only exists inside a
base64 blob (the offsets then cover the blob).
"""
import base64
import random
import re
from dataclasses import dataclass, field
from typing import List, Optional

from . import ids
from . import artifacts as art
from .artifacts import Item
from .names import NameProvider
from .pools import PoolError, SLOT_BUCKETS, approx_tokens, fill_template
from .spec import Spec

EXPORT_KEYS_SPAN = ("idx", "tag", "text", "attrs")
EXPORT_KEYS_ANCHOR = ("role", "value", "span", "start", "end", "did", "sub", "enc")


class RowDrop(Exception):
    """A row that cannot be realised; the reason is a stable code (counted for K9)."""
    def __init__(self, code, detail=""):
        super().__init__("%s %s" % (code, detail))
        self.code, self.detail = code, detail


@dataclass
class Span:
    idx: int
    tag: str
    text: str
    attrs: dict = field(default_factory=dict)


@dataclass
class Anchor:
    role: str
    value: str
    span: int
    start: int
    end: int
    did: Optional[str] = None
    sub: str = ""
    enc: str = ""


@dataclass
class Rendered:
    row_id: str
    spans: List[Span]
    anchors: List[Anchor]
    task_span: int
    carrier_span: int
    proxy_names: bool = False
    slot_tokens: int = 0
    slot_texts: tuple = ()
    placement_actual: tuple = ()    # (did, bin) as measured on the rendered carrier text
    pool_sha: str = ""
    meta: dict = field(default_factory=dict)

    def flat(self):
        return flatten(self)


def flatten(r):
    out = []
    for s in r.spans:
        a = "".join(' %s="%s"' % (k, v) for k, v in sorted(s.attrs.items()))
        out.append("<%s%s>\n%s\n</%s>" % (s.tag, a, s.text, s.tag))
    return "\n".join(out)


def export_for_b(r):
    """Rendered row + anchor map only. No spec, label, risk, tier, subtype, flags, pair or group ids."""
    return {
        "spans": [{k: getattr(s, k) for k in EXPORT_KEYS_SPAN} for s in r.spans],
        "anchors": [{k: getattr(a, k) for k in EXPORT_KEYS_ANCHOR} for a in r.anchors],
    }


# ---------------------------------------------------------------------------------------------------------------
# effect anchors from an Action (the generator's own table; B reads them as given)
# ---------------------------------------------------------------------------------------------------------------
def action_effects(a):
    """[(role, value, sub)] anchor facts for an action, none of which carries a risk or label."""
    out = [("tool_role", a.tool_role, "")]
    s = a.send
    if s is not None:
        out.append(("effect", "eff.send", s.data_class))
        if s.placed_in:
            out.append(("effect", "eff.placed_in", s.placed_in))
        if s.auth_header:
            out.append(("effect", "eff.auth_header", ""))
        if s.https:
            out.append(("effect", "eff.https", ""))
        if s.host:
            out.append(("host", s.host, "dest"))
        if s.cred_scope_host:
            out.append(("host", s.cred_scope_host, "cred_scope"))
    for p in a.delete_paths:
        out.append(("path", p, "delete"))
    for p in a.overwrite_paths:
        out.append(("path", p, "overwrite"))
    for code, flag in (("eff.irreversible", a.irreversible), ("eff.weakens_security", a.weakens_security),
                       ("eff.redirects", a.redirects), ("eff.persistent_hook", a.persistent_hook),
                       ("eff.shared_prod", a.shared_prod), ("eff.resource_heavy", a.resource_heavy)):
        if flag:
            out.append(("effect", code, ""))
    if a.install_pkg:
        out.append(("package", a.install_pkg, "install"))
        if a.install_index:
            out.append(("host", a.install_index, "index"))
    for t in a.targets:
        out.append(("target", t, ""))
    return out


# ---------------------------------------------------------------------------------------------------------------
# hidden-variant transforms: (text, [(abs_start, abs_end, tag)] marks) -> (text, marks)
# ---------------------------------------------------------------------------------------------------------------
def _map_marks(marks, mapper):
    return [(mapper(a), mapper(b), t) for a, b, t in marks]


def apply_hidden(variant, text, fmt):
    """Returns (new_text, mapper(offset)->offset, enc). `enc` is "base64" when the content is only in a blob."""
    if variant == "hid.html_comment":
        return "<!-- " + text + " -->", (lambda o: o + 5), ""
    if variant == "hid.alt_text":
        if '"' in text or "]" in text:
            raise RowDrop("HIDDEN_UNSAFE_CHARS", variant)
        if fmt == "fmt.html":
            return '<img alt="' + text + '" src="a.png">', (lambda o: o + 10), ""
        return "![" + text + "](a.png)", (lambda o: o + 2), ""
    if variant == "hid.zero_width":
        def mapper(o, t=text):
            return o + t[:o].count(" ")
        return text.replace(" ", " ​"), mapper, ""
    if variant == "hid.base64":
        blob = base64.b64encode(text.encode("utf-8")).decode("ascii")
        return "b64:" + blob, (lambda o: 4), "base64"
    if variant == "hid.split_chunks":
        return text, (lambda o: o), ""
    raise RowDrop("HIDDEN_UNKNOWN", variant)


HIDDEN_FORMATS = {
    "hid.html_comment": ("fmt.html", "fmt.markdown"),
    "hid.alt_text": ("fmt.html", "fmt.markdown"),
    "hid.zero_width": ids.FORMATS, "hid.base64": ids.FORMATS, "hid.split_chunks": ids.FORMATS,
}


def split_chunks(text, k, protected):
    """Split into k >= 2 pieces at spaces that are not inside a protected (start, end) range."""
    if k <= 1:
        return [text]
    cuts = [m.start() for m in re.finditer(r" ", text)
            if not any(a <= m.start() < b for a, b in protected)]
    if len(cuts) < k - 1:
        raise RowDrop("CHUNK_SPLIT_IMPOSSIBLE")
    step = len(cuts) / float(k)
    pick = sorted({cuts[min(len(cuts) - 1, int(step * (i + 1)) - 1)] for i in range(k - 1)})
    if len(pick) < k - 1:
        raise RowDrop("CHUNK_SPLIT_IMPOSSIBLE")
    out, prev = [], 0
    for c in pick:
        out.append(text[prev:c])
        prev = c + 1
    out.append(text[prev:])
    return out


# ---------------------------------------------------------------------------------------------------------------
# directive text
# ---------------------------------------------------------------------------------------------------------------
def _core_cell(d, bucket):
    if d.cls in ids.MENTION_CLASSES:
        return "men.%s.S%d" % (d.cls.split(".")[1], bucket)
    pre = "atk" if d.cls.startswith("goal.") else "ben"
    return "%s.%s.%s.S%d" % (pre, d.cls.split(".")[1], d.variant, bucket)


def template_slots_needed(d):
    from .pools import VARIANTS, MENTION_SLOTS
    if d.cls in ids.MENTION_CLASSES:
        return MENTION_SLOTS[d.cls]
    if d.variant == "truth":                       # truth-table specs (tests only): exactly the slots they carry
        return tuple(sorted(d.slotdict()))
    return VARIANTS[d.cls][d.variant][1]


EXPANDING_HIDDEN = ("hid.zero_width", "hid.base64")      # these inflate the token count ~2x: draw cores one bucket down


def compose_slot(pool, core_cell, slotvals, required, wrapper, hidden, fmt, bucket, rng, tries=60, wrng=None):
    """Compose core + wrapper (+ hidden transform) so the slot text lands in the slot-length bucket.
    Returns dict(text, marks=[(start, end, tag)], enc, tokens)."""
    lo, hi = SLOT_BUCKETS[bucket]
    if wrapper == "wrap.hidden" and hidden in EXPANDING_HIDDEN and bucket >= 1:
        core_cell = core_cell[:-1] + str(bucket - 1)
    last = None
    for _ in range(tries):
        core_ent = pool.pick(core_cell, rng, require_slots=list(required))
        try:
            core_text, slot_marks, role_marks = fill_template(core_ent["text"], slotvals)
            w_ent = pool.pick("wrap." + wrapper.split(".")[1], wrng or rng, require_slots=["core"])
            text, w_slots, _ = fill_template(w_ent["text"], {"core": core_text})
        except PoolError as e:
            raise RowDrop("POOL_TEMPLATE", str(e))
        off = [n for n in w_slots if n[0] == "core"][0][2]
        marks = ([(a + off, b + off, "role:" + r) for r, a, b in role_marks]
                 + [(a + off, b + off, "slot:%s=%s" % (n, v)) for n, v, a, b in slot_marks])
        enc = ""
        if wrapper == "wrap.hidden" and hidden and hidden != "hid.split_chunks":
            if fmt not in HIDDEN_FORMATS[hidden]:
                raise RowDrop("HIDDEN_FORMAT_MISMATCH", "%s in %s" % (hidden, fmt))
            text, mapper, enc = apply_hidden(hidden, text, fmt)
            marks = _map_marks(marks, mapper)
        tok = approx_tokens(text)
        last = tok
        if lo <= tok <= hi:
            return {"text": text, "marks": marks, "enc": enc, "tokens": tok, "ent": core_ent["id"], "went": w_ent["id"]}
    raise RowDrop("SLOT_LENGTH_UNMATCHED", "%s bucket %d last=%s" % (core_cell, bucket, last))


def compose_directive(d, pool, rng, fmt, wrng=None):
    return compose_slot(pool, _core_cell(d, d.slot_bucket), d.slotdict(), template_slots_needed(d), d.wrapper, d.hidden,
                        fmt, d.slot_bucket, rng, wrng=wrng)


def compose_filler(fl, carrier, pool, rng, fmt, wrng=None):
    return compose_slot(pool, "%s.%s.S%d" % (fl.kind, carrier.split(".")[1], fl.bucket), {}, (), fl.wrapper, fl.hidden,
                        fmt, fl.bucket, rng, wrng=wrng)


# ---------------------------------------------------------------------------------------------------------------
# row assembly
# ---------------------------------------------------------------------------------------------------------------
SLOT_ROLE = {"host": "host", "index_host": "host", "scope_host": "host", "package": "package", "path": "path",
             "path2": "path", "target": "target", "target2": "target", "branch": "target", "envvar": "envvar",
             "service": "service"}


def facts_block_text(f):
    return ["environment facts:",
            "  workspace: %s" % f.declared_workspace,
            "  hosts: %s" % (", ".join(f.declared_hosts) or "-"),
            "  packages: %s" % (", ".join(f.declared_manifest) or "-"),
            "  targets: %s" % (", ".join(f.declared_targets) or "-"),
            "  tools: %s" % (", ".join(f.declared_tools) or "-")]


def _ext(fmt):
    return {"fmt.markdown": ".md", "fmt.json": ".json", "fmt.yaml": ".yaml", "fmt.plain": ".txt", "fmt.html": ".html",
            "fmt.log_lines": ".log", "fmt.toml": ".toml"}[fmt]


def task_values(spec):
    """Values for the user-turn slots, taken from the spec facts (the planner put them there)."""
    f = spec.facts
    # world.make_facts lists the task targets in the order (target, branch) for the mentions the user turn names, so the
    # roles come from `task_mentions`, never from the SHAPE of a name (the namespace branch kind has no fixed prefix)
    tt = list(f.task_targets)
    tg, br = [], []
    if "target" in spec.task_mentions and tt:
        tg.append(tt.pop(0))
    if "branch" in spec.task_mentions and tt:
        br.append(tt.pop(0))
    vals = {"carrier_ref": art.CARRIER_REF[spec.carrier_type], "other_ref": art.OTHER_REF[spec.carrier_type]}
    if tg:
        vals["target"] = tg[0]
    if br:
        vals["branch"] = br[0]
    tool = spec.carrier_tool or (f.task_tools[0] if f.task_tools else None)
    if tool:
        vals["mcp_tool"] = tool
    return vals


def build_row(spec: Spec, pool, proxy_names=False, deny_check=None, wording_salt=""):
    """Realise one row (rows are built in memory; callers decide whether anything is ever written).
    `wording_salt` re-draws ONLY the wording (user turn, directive/filler cores, wrappers); the skeleton (names, artifact
    grammar, placement, facts) is seeded by art_seed alone and does not move (addendum 1.3: a non-G13 answer-check drop is
    regenerated on the SAME skeleton with a fresh wording seed). The salt is group-level, so a pair group stays a pair."""
    ws = ("|" + wording_salt) if wording_salt else ""
    from .spec import validate_spec
    bad = validate_spec(spec)
    if bad:
        raise RowDrop("SPEC_INVALID", "; ".join(bad))
    names = NameProvider(spec.art_seed, proxy=proxy_names, deny_check=deny_check)
    rng = random.Random("row|%s%s" % (spec.row_id, ws))
    spans: List[Span] = []
    anchors: List[Anchor] = []
    f = spec.facts

    def add_span(tag, text, **attrs):
        spans.append(Span(len(spans), tag, text, attrs))
        return len(spans) - 1

    def anchor_in(role, value, span, lo, hi, did=None, sub=""):
        pos = spans[span].text.find(value, lo, hi)
        if pos < 0:
            raise RowDrop("ANCHOR_MISSING", role)
        anchors.append(Anchor(role, value, span, pos, pos + len(value), did, sub))

    # ---- system / developer span ---------------------------------------------------------------------------------
    carrier_path = names.path_in(f.repo_root, "carrier|" + spec.art_seed, depth=1) + _ext(spec.carrier_format)
    lines = ["cwd: %s" % f.repo_root]
    if spec.declared_policy_file:
        lines.append("project rules file: %s" % carrier_path)
    if f.lane_tag:
        lines.append("lane: shared-production")
    if f.present:
        lines += facts_block_text(f)
    sys_i = add_span(ids.SRC_SYSTEM, "\n".join(lines))
    st = spans[sys_i].text
    anchor_in("fact.repo_root", f.repo_root, sys_i, 0, len(st))
    if spec.declared_policy_file:
        k = st.find("project rules file")
        anchor_in("path", carrier_path, sys_i, k, len(st), sub="carrier")
        anchors.append(Anchor("attr", ids.ATTR_DECLARED_POLICY, sys_i, k, k + len("project rules file: ") + len(carrier_path)))
    if f.lane_tag:
        k = st.find("lane:")
        anchors.append(Anchor("lane_tag", "shared-production", sys_i, k, k + len("lane: shared-production")))
    if f.present:
        blk = st.find("environment facts:")
        anchors.append(Anchor("fact.present", "facts.present", sys_i, blk, len(st)))
        anchor_in("fact.declared_workspace", f.declared_workspace, sys_i, blk, len(st))
        for role, vals in (("fact.declared_hosts", f.declared_hosts), ("fact.declared_manifest", f.declared_manifest),
                           ("fact.declared_targets", f.declared_targets), ("fact.declared_tools", f.declared_tools)):
            for v in vals:
                anchor_in(role, v, sys_i, blk, len(st))

    # ---- user turn -----------------------------------------------------------------------------------------------
    mode = spec.pointer.mode.split(".")[1]
    cell = "task.%s.%s" % (spec.task_class.split(".")[1], mode)
    if spec.pointer.mode != "deleg.none" and not spec.pointer.points_at_carrier:
        cell += ".other"
    allm = ("target", "branch", "mcp_tool")
    trng = random.Random("task|%s|%s|%s|%s%s" % (spec.art_seed, spec.task_class, spec.pointer.mode, spec.pointer.points_at_carrier, ws))
    ent = pool.pick(cell, trng, require_slots=[m for m in allm if m in spec.task_mentions],
                    forbid_slots=[m for m in allm if m not in spec.task_mentions])
    tvals = task_values(spec)
    try:
        ttext, tmarks, trole = fill_template(ent["text"], tvals)
    except PoolError as e:
        raise RowDrop("TASK_SLOT_UNFILLED", str(e))
    user_i = add_span(ids.SRC_USER, ttext)
    anchors.append(Anchor("task_class", spec.task_class, user_i, 0, len(ttext)))
    for n, v, a, b in tmarks:
        if n in ("target", "branch"):
            anchors.append(Anchor("fact.task_targets", v, user_i, a, b))
        elif n == "mcp_tool":
            anchors.append(Anchor("fact.task_tools", v, user_i, a, b))
    ptr = [m for m in trole if m[0] == "ptr"]
    if spec.pointer.mode != "deleg.none":
        if len(ptr) != 1:
            raise RowDrop("POINTER_MARKER_MISSING", cell)
        anchors.append(Anchor("delegation_pointer", spec.pointer.mode, user_i, ptr[0][1], ptr[0][2],
                              sub="carrier" if spec.pointer.points_at_carrier else "other"))
    elif ptr:
        raise RowDrop("POINTER_MARKER_UNEXPECTED", cell)

    # ---- context spans: git remote line (tool_result), visible manifest (user-owned file) -------------------------
    if f.repo_remotes:
        org = names.get("ns.org", "org|" + spec.art_seed).split(" ")[0].lower()
        repo = names.get("ns.repo", "repo|" + spec.art_seed)
        rl = ["origin\thttps://%s/%s/%s.git (fetch)" % (f.repo_remotes[0], org, repo),
              "origin\thttps://%s/%s/%s.git (push)" % (f.repo_remotes[0], org, repo)]
        rl += ["upstream\thttps://%s/%s/%s.git (fetch)" % (h, org, repo) for h in f.repo_remotes[1:]]
        ri = add_span(ids.SRC_TOOL, "$ git remote -v\n" + "\n".join(rl))
        for h in f.repo_remotes:
            anchor_in("fact.repo_remotes", h, ri, 0, len(spans[ri].text))
    if f.visible_manifest:
        mt = "dependencies:\n" + "\n".join("  - %s" % p for p in f.visible_manifest)
        mi = add_span(ids.SRC_USER_FILE, mt, path=f.repo_root.rstrip("/") + "/manifest")
        for p in f.visible_manifest:
            anchor_in("fact.visible_manifest_file", p, mi, 0, len(mt))

    # ---- carrier: background + slots -----------------------------------------------------------------------------
    meta = {"title": names.get("ns.project", "title|" + spec.art_seed), "lang": spec.code_lang,
            "stub_names": [names.get("ns.path_stem", "stub|%s|%d" % (spec.art_seed, i)).replace("-", "_") for i in range(3)]}
    budget = sum((SLOT_BUCKETS[d.slot_bucket][0] + SLOT_BUCKETS[d.slot_bucket][1]) // 2 for d in spec.directives) + sum(
        (SLOT_BUCKETS[x.bucket][0] + SLOT_BUCKETS[x.bucket][1]) // 2 for x in spec.fills)
    base = art.build_background(pool, spec.carrier_type, spec.len_target, spec.art_seed, names, slot_budget=budget)
    vrng = random.Random("vend|%s" % spec.art_seed)
    vend_idx = vrng.randrange(len(base)) if spec.has_nested_span else None
    base_items = [Item(it.kind, it.key, it.text, vendored=(i == vend_idx)) for i, it in enumerate(base)]

    plans = [{"kind": "dir", "d": d, "placement": d.placement, "bucket": d.slot_bucket,
              "chunks": d.chunks if (d.wrapper == "wrap.hidden" and d.hidden == "hid.split_chunks") else 1}
             for d in spec.directives]
    plans += [{"kind": fl.kind, "fl": fl, "placement": fl.placement, "bucket": fl.bucket,
               "chunks": fl.chunks if (fl.wrapper == "wrap.hidden" and fl.hidden == "hid.split_chunks") else 1}
              for fl in spec.fills]
    keys = art.FREE_KEYS[spec.carrier_type]
    # trim background so the SERIALISED carrier stays inside its length class (D6 / G6). The fit uses placeholder slots
    # of the bucket maximum, so it depends on the spec only and twins keep an identical skeleton.
    if spec.len_target < 3:
        hi = art.LEN_TARGETS[spec.len_target][1]
        dummy = [Item("slot", keys[0], "w " * int(SLOT_BUCKETS[pl["bucket"]][1] / 1.25), "fit%d" % i) for i, pl in enumerate(plans)]
        trim = random.Random("trim|%s" % spec.art_seed)
        while len(base_items) > art.MIN_ITEMS[spec.len_target]:
            t, _ = art.serialize(spec.carrier_type, spec.carrier_format, base_items + dummy, meta, spec.art_seed)
            if approx_tokens(t) <= hi:
                break
            base_items.pop(trim.randrange(len(base_items)))
    groups, comps = [], []
    for pi, pl in enumerate(plans):
        if pl["kind"] == "dir":
            # seeded by the SLOT (not the row): a task-edit pair carries the identical directive text in both members
            c = compose_directive(pl["d"], pool, random.Random("slot|%s|%d|%s%s" % (spec.art_seed, pi, pl["d"].did, ws)),
                                  spec.carrier_format, wrng=random.Random("wrap|%s|%d%s" % (spec.art_seed, pi, ws)))
        else:
            c = compose_filler(pl["fl"], spec.carrier_type, pool, rng, spec.carrier_format,
                               wrng=random.Random("wrap|%s|%d%s" % (spec.art_seed, pi, ws)))
        comps.append(c)
        if pl["chunks"] > 1:
            protected = [(a, b) for a, b, t in c["marks"]]
            pieces = split_chunks(c["text"], pl["chunks"], protected)
        else:
            pieces = [c["text"]]
        kr = random.Random("slotkey|%s|%d" % (spec.art_seed, pi))       # same draw in every twin
        key = keys[kr.randrange(len(keys))]
        hid = pl["d"].hidden if pl["kind"] == "dir" else pl["fl"].hidden
        raw = spec.carrier_format == "fmt.html" and hid in ("hid.html_comment", "hid.alt_text")
        groups.append([Item("slot", key, p, "s%d.c%d" % (pi, ci), vendored=(spec.vendor_slot and pi == 0), raw=raw)
                       for ci, p in enumerate(pieces)])
    prng = random.Random("place|%s" % spec.art_seed)
    slot_specs = [{"key": groups[pi][0].key, "chunks": len(groups[pi]), "want": pl["placement"]}
                  for pi, pl in enumerate(plans)]
    gaps = art.choose_gaps(spec.carrier_type, spec.carrier_format, base_items, slot_specs, meta, spec.art_seed, prng)
    if gaps is None:
        raise RowDrop("PLACEMENT_UNREACHABLE", ",".join(pl["placement"] for pl in plans))
    items = art._assemble(base_items, groups, gaps)
    ctext, ispans = art.serialize(spec.carrier_type, spec.carrier_format, items, meta, spec.art_seed)
    carrier_i = add_span(spec.carrier_src, ctext, path=carrier_path)
    idx_of = {it.slot_id: i for i, it in enumerate(items) if it.kind == "slot"}
    if spec.carrier_tool:
        anchors.append(Anchor("carrier_tool", spec.carrier_tool, carrier_i, 0, len(ctext)))
    wording = {"task": ent["id"], "core": [], "wrapper": []}
    placed, regions_out, slot_tok, slot_texts = [], [], 0, []
    slot_sets = [{idx_of["s%d.c%d" % (pi, ci)] for ci in range(len(groups[pi]))} for pi in range(len(plans))]
    for pi, pl in enumerate(plans):
        c = comps[pi]
        n_ch = len(groups[pi])
        first, last = idx_of["s%d.c0" % pi], idx_of["s%d.c%d" % (pi, n_ch - 1)]
        s0, e0 = ispans[first][0], ispans[last][1]
        regions_out.append((carrier_i, s0, e0))
        placed.append((pl["d"].did if pl["kind"] == "dir" else "fill%d" % pi,
                       art.bin_of(art.skeleton_fraction(ctext, ispans, slot_sets, pi))))
        slot_tok += c["tokens"]
        slot_texts.append(c["text"])
        wording["core"].append(c.get("ent"))
        wording["wrapper"].append(c.get("went"))
        if pl["kind"] != "dir":
            continue
        d = pl["d"]
        anchors.append(Anchor("directive_span", "directive", carrier_i, s0, e0, d.did))
        anchors.append(Anchor("directive_class", d.cls, carrier_i, s0, e0, d.did))
        if d.concerns_tool:
            anchors.append(Anchor("concerns_tool", d.concerns_tool, carrier_i, s0, e0, d.did))
        if d.nested:
            anchors.append(Anchor("attr", ids.ATTR_NESTED, carrier_i, s0, e0, d.did))
        enc = c["enc"]
        item_regions = [ispans[idx_of["s%d.c%d" % (pi, ci)]] for ci in range(n_ch)]
        for role, value, sub in _directive_anchor_facts(d):
            if enc:
                anchors.append(Anchor(role, value, carrier_i, s0, e0, d.did, sub, enc))
            elif role in ("tool_role", "effect"):
                anchors.append(Anchor(role, value, carrier_i, s0, e0, d.did, sub))   # semantic: covers the directive span
            else:
                for a, b in item_regions:
                    p = ctext.find(value, a, b)
                    if p >= 0:
                        anchors.append(Anchor(role, value, carrier_i, p, p + len(value), d.did, sub))
                        break
                else:
                    raise RowDrop("ANCHOR_MISSING", "%s %s" % (role, d.did))
        addr = [m for m in c["marks"] if m[2] == "role:addr"]
        if addr:
            a_text = c["text"][addr[0][0]:addr[0][1]]
            val = "agent" if d.agent_directed else "human"
            if enc:
                anchors.append(Anchor("addressee", val, carrier_i, s0, e0, d.did, "", enc))
            else:
                p = ctext.find(a_text, s0, e0)
                if p < 0:
                    raise RowDrop("ANCHOR_MISSING", "addressee %s" % d.did)
                anchors.append(Anchor("addressee", val, carrier_i, p, p + len(a_text), d.did))
        elif d.agent_directed:
            raise RowDrop("ADDRESSEE_MARKER_MISSING", d.did)
        else:
            anchors.append(Anchor("addressee", "none", carrier_i, s0, e0, d.did))
    return Rendered(spec.row_id, spans, anchors, user_i, carrier_i, proxy_names=names.used_proxy, slot_tokens=slot_tok,
                    slot_texts=tuple(slot_texts), placement_actual=tuple(placed), pool_sha=pool.sha(),
                    meta={"carrier_path": carrier_path, "slot_regions": regions_out, "wording": wording})


def _directive_anchor_facts(d):
    """(role, value, sub) the realised text must carry for this directive: its slot values plus the semantic
    effect anchors of its action. Action values that are not slot values stay semantic only."""
    out, seen = [], set()
    sv = d.slotdict()
    slotvals = set(sv.values())
    for n, v in sv.items():
        t = (SLOT_ROLE.get(n, "path"), v, "slot:" + n)
        if t not in seen:
            seen.add(t)
            out.append(t)
    if d.agent_directed and d.action is not None:
        for role, value, sub in action_effects(d.action):
            if role in ("tool_role", "effect") or value in slotvals:
                t = (role, value, sub)
                if t not in seen:
                    seen.add(t)
                    out.append(t)
    return out
