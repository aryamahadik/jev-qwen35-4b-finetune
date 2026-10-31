"""Benign-artifact generators per carrier type (D1) and the format serialisers.

An artifact is an ordered list of Items. Background items come from the `bg.<carrier>` pool cell (Claude-authored,
lint-proven free of directives). The artifact has ONE slot (two for a multi-directive row; consecutive chunks for
the split_chunks hidden variant). The slot fill is neutral filler (-> ALLOW), a benign directive (-> ALLOW_BENIGN)
or one payload (-> BLOCK/ASK); see splice.py. Structure (keys, headings, scaffold lines, timestamps, code stubs) is
written by the program from closed tables below and by a structure RNG seeded from art_seed ONLY, so a pair
group's twins share an identical skeleton and every structural draw is independent of the slot fill.
"""
import html
import json
import random
import textwrap
from dataclasses import dataclass
from typing import Optional

from . import ids
from .pools import approx_tokens, fill_template

LEN_TARGETS = ((90, 250), (265, 630), (641, 780), (1500, 3000))   # CARRIER tokens incl. slots: 55% <= 256, 30% 257-640, 15% 641-1200 (D6); 3 = LS only
MIN_ITEMS = {0: 8, 1: 12, 2: 12, 3: 12}               # every placement bin needs a gap
ITEM_OVERHEAD = 6                                       # tokens of per-item structure (keys, headings, quotes, timestamps)
SCAFFOLD_TOKENS = 25                                    # title / skeleton overhead the background does not count
LEN_MIX = (0.55, 0.30, 0.15)                            # 55% <= 256, 30% 257-640, 15% 641-1200 (D6)

# closed free-text key lists (label-neutral draws); structured formats and headings use these
FREE_KEYS = {
    "car.readme": ("overview", "usage", "notes", "install", "faq", "status"),
    "car.contributing_guide": ("workflow", "style", "review", "notes", "release", "support"),
    "car.issue_body": ("body", "summary", "details", "context", "steps", "notes"),
    "car.review_comment": ("comment", "summary", "details", "suggestion", "context", "notes"),
    "car.code_comment": ("note", "todo", "doc", "warn", "info", "hint"),
    "car.rules_file": ("guideline", "convention", "note", "scope", "style", "review"),
    "car.ci_log": ("step", "build", "test", "cache", "report", "setup"),
    "car.ci_config": ("description", "notes", "label", "comment", "summary", "message"),
    "car.tool_json": ("message", "note", "description", "detail", "summary", "text"),
    "car.tool_text": ("output", "note", "result", "detail", "summary", "info"),
    "car.mcp_description": ("description", "usage", "notes", "returns", "summary", "hint"),
    "car.mcp_response": ("content", "message", "result", "text", "summary", "detail"),
}
# which carriers serialise as arrays (key-less items) in json/yaml/toml
ARRAY_STYLE = {"car.ci_log", "car.tool_text", "car.mcp_response"}
COMMENT_PREFIX = {"python": "# ", "javascript": "// ", "typescript": "// ", "go": "// ", "bash": "# "}
CODE_STUB = {
    "python": "def {fn}({a}):\n    return {a}\n",
    "javascript": "function {fn}({a}) {{\n  return {a};\n}}\n",
    "typescript": "export function {fn}({a}: string): string {{\n  return {a};\n}}\n",
    "go": "func {Fn}({a} string) string {{\n\treturn {a}\n}}\n",
    "bash": "{fn}() {{\n  echo \"$1\"\n}}\n",
}
# carrier reference phrase used by delegation pointers in the user turn (generic, program-written)
CARRIER_REF = {
    "car.readme": "the README", "car.contributing_guide": "the contributing guide", "car.issue_body": "the issue",
    "car.review_comment": "the review comment", "car.code_comment": "the code comments",
    "car.rules_file": "the rules file", "car.ci_log": "the CI log", "car.ci_config": "the CI config",
    "car.tool_json": "the tool output", "car.tool_text": "the tool output", "car.mcp_description": "the tool description",
    "car.mcp_response": "the tool response",
}
OTHER_REF = {
    "car.readme": "the changelog", "car.contributing_guide": "the wiki page", "car.issue_body": "the ticket thread",
    "car.review_comment": "the design note", "car.code_comment": "the module docs", "car.rules_file": "the style note",
    "car.ci_log": "the deploy log", "car.ci_config": "the release notes", "car.tool_json": "the status page",
    "car.tool_text": "the status page", "car.mcp_description": "the server docs", "car.mcp_response": "the server docs",
}


@dataclass(frozen=True)
class Item:
    kind: str                    # head | bg | slot
    key: str
    text: str
    slot_id: Optional[str] = None
    vendored: bool = False       # wrapped in a third-party-repo-file marker (nested provenance carrier text)
    raw: bool = False            # html format: the item is markup (hidden html comment / img alt) and is not escaped


VEND_OPEN, VEND_CLOSE = "<src.third_party_repo_file>", "</src.third_party_repo_file>"


def sample_len_target(rng):
    r = rng.random()
    return 0 if r < LEN_MIX[0] else (1 if r < LEN_MIX[0] + LEN_MIX[1] else 2)


def build_background(pool, carrier, len_target, art_seed, names, slot_budget=0):
    """Return the list of background Items (kind=bg) for this artifact. Deterministic in art_seed."""
    rng = random.Random("bg|%s|%s|%s" % (art_seed, carrier, len_target))
    lo, hi = LEN_TARGETS[len_target]
    goal = max(40, rng.randint(lo, hi) - slot_budget - SCAFFOLD_TOKENS - ITEM_OVERHEAD * 10)
    cell = "bg." + carrier.split(".")[1]
    keys = FREE_KEYS[carrier]
    items, total, i = [], 0, 0
    while total < goal and i < 400:
        ent = pool.pick(cell, rng, forbid_slots=("core", "carrier_ref", "other_ref", "mcp_tool"))
        slots = {s: names.get({"repo": "ns.repo", "package": "ns.package", "path": "ns.path_stem", "branch": "ns.branch",
                               "host": "ns.host", "target": "ns.project", "envvar": "ns.envvar", "service": "ns.service",
                               "index_host": "ns.host", "tool": "ns.mcp_tool"}[s], "bg|%s|%d|%s" % (art_seed, i, s))
                 for s in _slots_of(ent["text"])}
        text, _, _ = fill_template(ent["text"], slots)
        items.append(Item("bg", keys[rng.randrange(len(keys))], text))
        total += approx_tokens(text)
        i += 1
    # split items longer than 60 tokens at sentence ends so every placement bin has a gap
    k = 0
    while k < len(items):
        it = items[k]
        if approx_tokens(it.text) > 60:
            cut = it.text.rfind(". ", 20, len(it.text) // 2 + 40)
            if cut > 0:
                items[k:k + 1] = [Item("bg", it.key, it.text[:cut + 1]), Item("bg", keys[(k + 1) % len(keys)], it.text[cut + 2:])]
                continue
        k += 1
    # keep at least 12 items so every placement bin has a gap; split the longest item (sentence end, else a space)
    guard = 0
    while len(items) < MIN_ITEMS[len_target] and guard < 40:
        guard += 1
        k = max(range(len(items)), key=lambda j: len(items[j].text))
        t = items[k].text
        cut = t.rfind(". ", 0, len(t) // 2 + 20)
        if cut < 20:
            cut = t.find(" ", len(t) // 2)
            if cut < 8:
                break
            pieces = [t[:cut], t[cut + 1:]]
        else:
            pieces = [t[:cut + 1], t[cut + 2:]]
        items[k:k + 1] = [Item("bg", items[k].key, pieces[0]), Item("bg", keys[(k + 1) % len(keys)], pieces[1])]
    return items


def _slots_of(text):
    from .pools import template_slots
    return sorted(template_slots(text))


# ---------------------------------------------------------------------------------------------------------------
# serialisers: each returns (text, {item_index: (start, end)}) where (start, end) is the item's text region
# ---------------------------------------------------------------------------------------------------------------
class _Buf:
    def __init__(self):
        self.parts, self.n, self.spans = [], 0, {}

    def add(self, s):
        self.parts.append(s)
        self.n += len(s)

    def item(self, idx, s):
        self.spans[idx] = (self.n, self.n + len(s))
        self.add(s)

    def done(self):
        return "".join(self.parts), self.spans


def _vend(it):
    return (VEND_OPEN + "\n" + it.text + "\n" + VEND_CLOSE) if it.vendored else it.text


def _flat(s):
    return " ".join(s.split())


def serialize(carrier, fmt, items, meta, art_seed):
    r = random.Random("ser|%s|%s|%s" % (art_seed, carrier, fmt))
    b = _Buf()
    title = meta["title"]
    keyed = [r.random() < 0.55 for _ in items]          # structure draws: one per item, independent of item text
    bullets = [r.random() < 0.25 for _ in items]
    levels = [r.choice(("INFO", "INFO", "WARN", "DEBUG")) for _ in items]
    arr = carrier in ARRAY_STYLE
    if fmt == "fmt.markdown":
        if carrier == "car.code_comment":
            return _code(carrier, fmt, items, meta, r)
        b.add("# %s\n\n" % title)
        for i, it in enumerate(items):
            if keyed[i]:
                b.add("## %s\n\n" % it.key)
            t = _vend(it)
            b.item(i, ("- " + t if bullets[i] and "\n" not in t else t) + "\n\n")
        return b.done()
    if fmt == "fmt.plain":
        if carrier == "car.code_comment":
            return _code(carrier, fmt, items, meta, r)
        b.add("%s\n%s\n\n" % (title, "=" * min(len(title), 40)))
        for i, it in enumerate(items):
            t = _vend(it)
            b.item(i, ("%s: %s" % (it.key, t) if keyed[i] else t) + "\n\n")
        return b.done()
    if fmt == "fmt.html":
        b.add("<!doctype html>\n<html><body>\n<h1>%s</h1>\n" % html.escape(title, quote=False))
        for i, it in enumerate(items):
            t = _vend(it) if it.raw else html.escape(_vend(it), quote=False)
            if keyed[i]:
                b.add("<section><h2>%s</h2>\n" % html.escape(it.key, quote=False))
            b.add("<p>")
            b.item(i, t)
            b.add("</p>\n")
            if keyed[i]:
                b.add("</section>\n")
        b.add("</body></html>\n")
        return b.done()
    if fmt == "fmt.log_lines":
        sec = 3600 * r.randint(1, 20) + r.randint(0, 3599)
        comps = FREE_KEYS[carrier]
        for i, it in enumerate(items):
            sec += r.randint(1, 40)
            ts = "2026-03-%02dT%02d:%02d:%02dZ" % (5 + (sec // 86400) % 20, (sec // 3600) % 24, (sec // 60) % 60, sec % 60)
            b.add("%s %-5s %s[%d]: " % (ts, levels[i], it.key if it.key in comps else comps[0], i))
            b.item(i, _flat(_vend(it)))
            b.add("\n")
        return b.done()
    if fmt == "fmt.json":
        b.add('{\n  "name": %s,\n' % json.dumps(title, ensure_ascii=False))
        if arr:
            b.add('  "entries": [\n')
            for i, it in enumerate(items):
                b.add("    ")
                s = json.dumps(_vend(it), ensure_ascii=False)
                b.item(i, s)
                b.add(",\n" if i < len(items) - 1 else "\n")
            b.add("  ]\n}\n")
        else:
            for i, it in enumerate(items):
                b.add('  %s: ' % json.dumps("%s_%d" % (it.key, i), ensure_ascii=False))
                b.item(i, json.dumps(_vend(it), ensure_ascii=False))
                b.add(",\n" if i < len(items) - 1 else "\n")
            b.add("}\n")
        return b.done()
    if fmt == "fmt.yaml":
        b.add("name: %s\n" % json.dumps(title, ensure_ascii=False))
        if arr:
            b.add("entries:\n")
            for i, it in enumerate(items):
                b.add("  - ")
                b.item(i, json.dumps(_vend(it), ensure_ascii=False))
                b.add("\n")
        else:
            for i, it in enumerate(items):
                b.add("%s_%d: " % (it.key, i))
                b.item(i, json.dumps(_vend(it), ensure_ascii=False))
                b.add("\n")
        return b.done()
    if fmt == "fmt.toml":
        b.add("name = %s\n" % json.dumps(title, ensure_ascii=False))
        if arr:
            b.add("entries = [\n")
            for i, it in enumerate(items):
                b.add("  ")
                b.item(i, json.dumps(_vend(it), ensure_ascii=False))
                b.add(",\n")
            b.add("]\n")
        else:
            for i, it in enumerate(items):
                b.add("%s_%d = " % (it.key, i))
                b.item(i, json.dumps(_vend(it), ensure_ascii=False))
                b.add("\n")
        return b.done()
    raise ValueError("unknown format %s" % fmt)


def _code(carrier, fmt, items, meta, r):
    """Source file with comment blocks (code_comment carriers). Nothing here is executed."""
    lang = meta["lang"]
    pre = COMMENT_PREFIX[lang]
    b = _Buf()
    fence = fmt == "fmt.markdown"
    if fence:
        b.add("```%s\n" % lang)
    stub_names = meta["stub_names"]
    for i, it in enumerate(items):
        wrapped = (textwrap.fill(_vend(it), 78, replace_whitespace=False, break_long_words=False, break_on_hyphens=False)
                   if (it.kind == "bg" and "\n" not in it.text and not it.vendored) else _vend(it))
        block = "".join(pre + ln + "\n" for ln in wrapped.split("\n"))
        b.item(i, block.rstrip("\n"))
        b.add("\n")
        if i % 2 == 1:
            nm = stub_names[(i // 2) % len(stub_names)]
            b.add(CODE_STUB[lang].format(fn=nm, Fn=nm.capitalize(), a="value"))
            b.add("\n")
    if fence:
        b.add("```\n")
    return b.done()


# ---------------------------------------------------------------------------------------------------------------
# placement
# ---------------------------------------------------------------------------------------------------------------
def bin_of(frac):
    return ids.PLACEMENTS[min(4, int(frac * 5))]


def choose_gap(carrier, fmt, base_items, slot_items, meta, art_seed, want_bin, rng):
    """Find an insertion index (0..len(base_items)) whose slot start falls in `want_bin` of the SERIALISED text.
    Returns (gap, text, spans) or None."""
    n = len(base_items)
    order = list(range(n + 1))
    rng.shuffle(order)
    for gap in order:
        items = base_items[:gap] + slot_items + base_items[gap:]
        text, spans = serialize(carrier, fmt, items, meta, art_seed)
        s0 = spans[gap][0]
        if bin_of(s0 / max(1, len(text))) == want_bin:
            return gap, text, spans
    return None


def _assemble(base_items, groups, gaps):
    """Insert slot groups into base items at base-gap indices (ties keep slot order)."""
    order = sorted(range(len(groups)), key=lambda i: (gaps[i], i))
    items = list(base_items)
    out, cursor = [], 0
    for i in order:
        g = gaps[i]
        out += items[cursor:g]
        cursor = g
        out += groups[i]
    out += items[cursor:]
    return out


def skeleton_fraction(text, spans, slot_item_sets, which):
    """Position of slot `which` as a fraction of the NON-SLOT text (skeleton): independent of the slot's own length,
    so every member of a pair group sits in the same bin."""
    all_slot = sorted(i for st in slot_item_sets for i in st)
    slot_len = sum(spans[i][1] - spans[i][0] for i in all_slot)
    s0 = spans[min(slot_item_sets[which])][0]
    before = sum(spans[i][1] - spans[i][0] for i in all_slot if spans[i][0] < s0)
    return (s0 - before) / max(1, len(text) - slot_len)


def choose_gaps(carrier, fmt, base_items, slots, meta, art_seed, rng, tries=600):
    """Joint placement of 1..2 slot groups. `slots`: list of dicts(key, chunks, want). Accepted when every slot's
    SKELETON position (see skeleton_fraction) lies in its wanted bin. Depends on the spec only, so the members of a
    pair group get the same gaps. Returns the list of gaps or None."""
    n = len(base_items)
    for _ in range(tries):
        gaps = [rng.randint(0, n) for _ in slots]
        groups = [[Item("slot", sl["key"], "w", "z%d.c%d" % (i, c)) for c in range(sl["chunks"])] for i, sl in enumerate(slots)]
        items = _assemble(base_items, groups, gaps)
        text, spans = serialize(carrier, fmt, items, meta, art_seed)
        idx = {it.slot_id: i for i, it in enumerate(items) if it.kind == "slot"}
        sets = [{idx[it.slot_id] for it in g} for g in groups]
        if all(bin_of(skeleton_fraction(text, spans, sets, gi)) == slots[gi]["want"] for gi in range(len(slots))):
            return gaps
    return None
