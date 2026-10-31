"""c2_kit/polarity.py: does a yes/no question WORDING mean what its question form declares? (G-LEX meaning check).

Why (T35 pilot, G5-H: 3 confirmed wrong golds, all yn_double_neg). The admitted wordings "Under these rules, is it not
the case that they do not bar the crawler from fetching this URL?" carry two syntactic negations (negcount k_syn =
k_all = 2, exactly the declared profile) AND a negative predicate ("bar") that negcount's closed lexicon does not
list. Their literal meaning is "yes = the crawler may NOT fetch", the reverse of the form (yes = may fetch). No gate
could see it: negcount counts only its lexicon, G-LEX admits a sem by pattern, G-TW asserts gold(Q) = not gold(not-Q)
on the plugin's polarity, and G2 / G3 test the program, not the English. The same pool also held wordings under a
contracted negative frame ("Isn't it true that ... is not forbidden ...?"), which reads either way.

The rule (fixed once here; a family supplies only its predicate lexicon, as plugin attributes):
  S   k_syn of the wording (negcount, placeholders read as a neutral word).
  L   lexical negatives: negcount's implicit entries (a match with no L_core token: lack, deny, prevent ... from,
      refuse to, fail to, rule out, without, except, unless, false ...) plus the family's NEGATIVE / antonym predicate
      patterns (POLARITY_NEGATIVES: bar, block, skip, out of bounds ...), outside the negcount matches.
  P1  mixed: S >= 1 and L >= 1 is refused. A syntactic negation over a negative predicate is the inverted class;
      a wording negates a positive predicate syntactically, or uses a negative predicate, never both.
  P2  parity: the wording's polarity is (-1) ** (S + [L > 0] + base), base = the negations the family's positive
      predicate phrasing itself carries (POLARITY_BASE[predicate], default 0). It must equal the form's declared
      polarity. Coordinated negative predicates ("skip it and leave it alone") count once.
  P3  contracted negative question frame: the question's first auxiliary is a contracted negative ("Isn't it ...",
      "Under these rules, aren't ...", "Doesn't ..."). A negative polar question reads either way; refused.
  P4  (POLARITY_STRICT_FRAMES only) the uncontracted negative question frame "aux + subject + not" ("Is the crawler
      not ...", "Would an auditor not agree ..."), except the explicit outer frame "aux it not (the case | true | so
      | correct | accurate | right | fair) ...".
Choice forms and option-framing complements are not checked (their negation lives in the listed alternatives);
POLARITY_SKIP exempts more forms by name.

Where it runs (opt in: POLARITY_CHECK = True on the plugin):
  - authoring: problems(text, ...) / form_problems(plugin, qform, text) in the family's wording admission check, so a
    re-authored wording that breaks the rule never enters a pool;
  - generation: screen(ctx, plugin) returns the kit context without the failing wordings (call it from the plugin's
    ctx_for hook, so neither render() nor the pipeline's complement partner can pick one), plus the quarantine list;
  - gate: pipeline.check_rendered adds row_problems() as G-LEX problems (a failing wording that reached a row drops
    the unit and fails the pilot's G-LEX bar).
It never sets or changes a label: a failing wording is quarantined and the rows are regenerated.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from . import paths  # noqa: F401  (negcount on sys.path)
import negcount  # noqa: E402

_PH = re.compile(r"\{[^{}]*\}")
_CORE = frozenset(negcount.L_CORE)
_SKIP_CLASSES = frozenset({"core", "comparator", "comparator_alias"})
# auxiliaries that open a polar question ("ca", "wo", "sha" are negcount's stems of can't, won't, shan't)
AUX = frozenset({"is", "are", "was", "were", "am", "do", "does", "did", "has", "have", "had", "can", "ca", "could",
                 "will", "wo", "would", "shall", "sha", "should", "must", "may", "might", "need"})
EXPLICIT_FRAME = frozenset({"the", "true", "so", "correct", "accurate", "right", "fair", "false"})
FRAMES = ("plain", "explicit", "contracted", "subject_not")


@dataclass(frozen=True)
class PolarityRead:
    k_syn: int
    lexical: tuple             # surfaces of the lexical negatives (L), in text order
    frame: str                 # plain | explicit | contracted | subject_not

    @property
    def mixed(self) -> bool:
        return self.k_syn > 0 and bool(self.lexical)

    @property
    def layers(self) -> int:
        return self.k_syn + (1 if self.lexical else 0)


def _compile(patterns) -> list:
    out = []
    for p in patterns:
        out.append(p if isinstance(p, re.Pattern) else re.compile(r"(?<![\w-])(?:" + p + r")(?![\w-])", re.I))
    return out


_CLAUSE_BREAK = frozenset({",", ":", ";"})
_SCAN_STOP = frozenset({"that", "whether", "if", "?", ".", ";", ":"})


def _frame(toks: list) -> str:
    """The question frame, read at the question's opening auxiliary: the first auxiliary that starts a clause (the
    first word, or the first word after a leading phrase closed by "," or ":"). negcount tokens split "isn't" into
    "is" + "n't". No clause-opening auxiliary (a declarative question): "plain"."""
    lows = [t.low for t in toks]
    starts = [0] + [j + 1 for j, w in enumerate(lows) if w in _CLAUSE_BREAK]
    i = next((j for j in starts if j < len(lows) and lows[j] in AUX), None)
    if i is None:
        return "plain"
    nxt = lows[i + 1] if i + 1 < len(lows) else ""
    if nxt == "n't":
        return "contracted"
    if nxt == "it" and i + 2 < len(lows) and lows[i + 2] == "not":
        after = lows[i + 3] if i + 3 < len(lows) else ""
        return "explicit" if after in EXPLICIT_FRAME else "subject_not"
    for j in range(i + 1, min(len(lows), i + 10)):
        w = lows[j]
        if w in _SCAN_STOP or w in AUX:          # an embedded clause or a second verb group: its "not" is not the frame's
            break
        if w == "not":
            return "subject_not"
    return "plain"


def read(text: str, negatives=(), affixed=()) -> PolarityRead:
    """S, the lexical negatives and the question frame of one wording (placeholders read as a neutral word)."""
    src = _PH.sub("X", text or "")
    nc = negcount.count(src, affixed)
    toks = negcount.tokenize(src)
    spans, lexical = [], []
    for m in nc.matches:
        a = [toks[i] for i in m.anchors]
        spans += [(t.start, t.end) for t in a]
        if m.cls not in _SKIP_CLASSES and not any(t.low in _CORE for t in a):
            lexical.append((a[0].start, m.surface))
    for rx in _compile(negatives):
        for hit in rx.finditer(src):
            if not any(s < hit.end() and hit.start() < e for s, e in spans):
                lexical.append((hit.start(), hit.group()))
                spans.append((hit.start(), hit.end()))
    return PolarityRead(nc.k_syn, tuple(s for _, s in sorted(lexical)), _frame(toks))


def problems(text: str, polarity: int, *, base: int = 0, negatives=(), strict_frames: bool = False,
             affixed=()) -> list:
    """Rule P1-P4 for one wording whose form declares `polarity` (+1 asks the predicate, -1 its complement)."""
    if polarity not in (1, -1):
        raise ValueError("polarity is +1 or -1")
    r = read(text, negatives, affixed)
    out = []
    if r.frame == "contracted":
        out.append("P3 contracted negative question frame (a negative polar question reads either way)")
    if strict_frames and r.frame == "subject_not":
        out.append("P4 negative question frame 'aux + subject + not' (strict frames)")
    if r.mixed:
        out.append(f"P1 syntactic negation (k_syn {r.k_syn}) over a negative predicate {list(r.lexical)}")
    elif (-1) ** (r.layers + base) != polarity:
        out.append(f"P2 reads with polarity {(-1) ** (r.layers + base):+d} (k_syn {r.k_syn}, lexical "
                   f"{list(r.lexical)}, base {base}); the form declares {polarity:+d}")
    return out


# ------------------------------------------------------------------------------------------------ plugin level

def enabled(plugin) -> bool:
    return bool(getattr(plugin, "POLARITY_CHECK", False))


def checked_form(plugin, qform: str):
    """The QuestionForm when the rule applies to it (yes/no, not option framing, not skipped), else None."""
    q = (getattr(plugin, "QFORMS", {}) or {}).get(qform)
    if q is None or q.qtype != "noul" or q.complement_kind == "option_framing":
        return None
    if qform in tuple(getattr(plugin, "POLARITY_SKIP", ()) or ()):
        return None
    return q


def form_problems(plugin, qform: str, text: str) -> list:
    """problems() with the plugin's lexicon, base and frame setting; [] when the plugin has not opted in or the form is
    not checked."""
    if not enabled(plugin):
        return []
    q = checked_form(plugin, qform)
    if q is None:
        return []
    base = int((getattr(plugin, "POLARITY_BASE", {}) or {}).get(q.predicate, 0))
    return problems(text, q.polarity, base=base, negatives=tuple(getattr(plugin, "POLARITY_NEGATIVES", ()) or ()),
                    strict_frames=bool(getattr(plugin, "POLARITY_STRICT_FRAMES", False)))


def config_problems(plugin) -> list:
    """validate_plugin: the opt-in attributes are well formed."""
    if not enabled(plugin):
        return []
    probs = []
    for p in getattr(plugin, "POLARITY_NEGATIVES", ()) or ():
        try:
            _compile([p])
        except re.error as e:
            probs.append(f"POLARITY_NEGATIVES pattern {p!r}: {e}")
    for k, v in (getattr(plugin, "POLARITY_BASE", {}) or {}).items():
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            probs.append(f"POLARITY_BASE[{k!r}] must be an int >= 0")
    qf = getattr(plugin, "QFORMS", {}) or {}
    for q in getattr(plugin, "POLARITY_SKIP", ()) or ():
        if q not in qf:
            probs.append(f"POLARITY_SKIP names an unknown question form {q!r}")
    return probs


def screen(ctx, plugin) -> tuple:
    """(ctx without the failing wordings, {skin_id: problems}). Wording skins of checked yes/no forms only; every other
    skin is kept. Label-blind: it reads the wording text and its form, never a row or a gold."""
    from .plugin import KitCtx
    if not enabled(plugin):
        return ctx, {}
    bad = {}
    for sid, sk in ctx.skins.items():
        if sk.kind == "wording" and sk.qform:
            p = form_problems(plugin, sk.qform, sk.text)
            if p:
                bad[sid] = p
    if not bad:
        return ctx, {}
    return KitCtx(skins={k: v for k, v in ctx.skins.items() if k not in bad}, lexicon=ctx.lexicon), bad


def row_problems(plugin, spec, rr, ctx) -> list:
    """Pipeline safety net: [("G-LEX", detail)] when a yes/no row's wording breaks the rule."""
    if not enabled(plugin) or not rr.wording_id or rr.row.get("qtype") != "noul":
        return []
    try:
        wd = ctx.skin(rr.wording_id)
    except KeyError:
        return []
    return [("G-LEX", f"wording {rr.wording_id} polarity: {p}") for p in form_problems(plugin, spec.qform, wd.text)]
