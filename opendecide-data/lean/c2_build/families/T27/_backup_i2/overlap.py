"""families/T27/overlap.py: the label-independent request overlap of a ch_next row (fix iteration 2, G6 view c).

Why. A do_step row asks an action that is on the user's list, so its request phrase repeats words that the user's task
and the printed allowed list already hold; a continue / stop_ask row asks an action that is not on the list, so its
phrase brings words the row does not hold yet. A reader that counts which words are present (G6 c: the card and the
content without the question) reads the label from that (iteration 1: 0.488 against the bar 0.353). Matching the task,
the action and the pair frequencies does not remove it: it is the overlap between the request text and the user's text.

What. OVERLAP of a request = the share of its content word stems that the user's text holds. The user's text is the task
clause and the allowed list the card prints for that task (the words a reader sees as "the user's task"). A request is
in a band: none (0), partial (0 < o <= 0.5) or high (o > 0.5). A row has one LEVEL (a band), drawn from the seed alone,
BEFORE and independently of the label, with the same distribution for every label:

  * the shares come from the beyond rows' own (task, actions) joint J (plugin.beyond_joint): every cell is feasible for
    the bands in which some admitted (task form, request form) pair falls, a cell with several bands is split evenly
    across them, so the shares pi are the J-mass of each band and the per-level conditional J_l of a beyond row mixes
    back to J exactly (the task, action and pair marginals of iteration 1 are untouched);
  * a do_step row keeps its iteration-1 (task, actions) draw and renders its task form and request forms into the
    drawn band (an in-scope request may be a paraphrase with disjoint words); a continue / stop_ask row draws its cell
    from J_l and renders into the same band (a beyond request may reuse the user's verb and object);
  * gold never reads wording: it stays the action-class x scope table (solver A) and the solver-B parse of the rendered
    row (verb-lexicon classes decide the actions); the band only chooses WHICH admitted form of the sem is printed.

The mechanism needs admitted forms in every band: `plan()` returns None (levels off, rows as in iteration 1) unless
every beyond cell and every do_step cell is feasible for every level that carries mass. With the frozen pools_v2
lexicon that is not the case (an in-scope request always repeats 0.5-1.0 of the user's words; see
pilot_i2/FIX_I2_NOTES.md), so the in-scope paraphrases are authored (haiku/ovl_i2/) and merged by run_pilot_i2.py.
"""
from __future__ import annotations

import re

BANDS = ("none", "partial", "high")
_STOP = frozenset("a an the to of for and or in on at with this that these those it its is are be will would me my you "
                  "your our us we their them they there as by from then than so if once after before up out all any "
                  "some one no not do does done can could should may might have has had been being which who whom what "
                  "when where while into onto about over just only also very more most such please kindly".split())
_BOILER = frozenset("unlock unlocked shown show shows".split())      # the gate frame words of every request form


def stem(w: str) -> str:
    for s in ("ing", "ed", "es", "s"):
        if w.endswith(s) and len(w) > len(s) + 2:
            w = w[: -len(s)]
            break
    return w[:-1] if w.endswith("e") and len(w) > 3 else w


def stems(text: str) -> frozenset:
    """Content stems of a clause (the {ITEM} slot, stop words and the gate frame words dropped)."""
    text = text.replace("{ITEM}", " ")
    return frozenset(stem(w) for w in re.findall(r"[a-z]+", text.lower()) if w not in _STOP and w not in _BOILER)


def band(o: float) -> str:
    return "none" if o <= 0.0 else ("partial" if o <= 0.5 else "high")


class OverlapModel:
    """o(task, task form, action, request form) over the registry's admitted forms (cached)."""

    def __init__(self, lexicon, task_scope: dict, display: dict):
        self.lex, self.scope, self.display = lexicon, task_scope, display
        self._u: dict = {}
        self._r: dict = {}
        self._o: dict = {}

    def _user(self, task: str, tf: str) -> frozenset:
        k = (task, tf)
        if k not in self._u:
            u = set(stems(self.lex.forms[tf].text))
            for a in self.scope[task]:
                u |= stems(self.display[a])
            self._u[k] = frozenset(u)
        return self._u[k]

    def _req(self, rf: str) -> frozenset:
        if rf not in self._r:
            self._r[rf] = stems(self.lex.forms[rf].text)
        return self._r[rf]

    def o(self, task: str, tf: str, action: str, rf: str) -> float:
        k = (task, tf, rf)
        if k not in self._o:
            r = self._req(rf)
            self._o[k] = len(r & self._user(task, tf)) / len(r) if r else 0.0
        return self._o[k]

    def bands(self, idx: dict, task: str, acts, framings=None) -> frozenset:
        """The levels at which `task` can print requests of `acts` (all in the band) from admitted forms."""
        framings = framings or ["gate"] * len(acts)
        out: set = set()
        for tf in idx[task]:
            per = [{band(self.o(task, tf, a, rf)) for rf in idx[f"req.{a}.{fr}"]} for a, fr in zip(acts, framings)]
            out |= set.intersection(*per)
        return frozenset(out)

    def steer(self, level: str, idx: dict, task: str, reqs: list, rng) -> tuple:
        """(task form, [request form per request]) with every request in the band `level`; reqs = [(action, framing)].
        The forms are picked uniformly among the feasible ones; a request form is not printed twice when avoidable."""
        cands = []
        for tf in idx[task]:
            per = [[rf for rf in idx[f"req.{a}.{fr}"] if band(self.o(task, tf, a, rf)) == level] for a, fr in reqs]
            if all(per):
                cands.append((tf, per))
        if not cands:
            raise ValueError(f"no admitted forms put {reqs} for task {task} in the band {level}")
        tf, per = rng.choice(cands)
        rfs: list = []
        for p in per:
            rfs.append(rng.choice([f for f in p if f not in rfs] or p))
        return tf, rfs


class Plan:
    """The level shares and the per-level beyond cell draws of one sampler (None from `plan` = levels off)."""

    def __init__(self, shares: dict, cells: tuple, cums: dict):
        self.shares, self.cells, self.cums = shares, cells, cums
        self.levels = tuple(l for l in BANDS if shares.get(l, 0.0) > 0.0)

    def level(self, u: float) -> str:
        acc = 0.0
        for l in self.levels:
            acc += self.shares[l]
            if u < acc:
                return l
        return self.levels[-1]

    def cell(self, level: str, u: float) -> tuple:
        idxs, cum = self.cums[level]
        lo, hi = 0, len(cum) - 1
        u *= cum[-1]
        while lo < hi:
            mid = (lo + hi) // 2
            if cum[mid] < u:
                lo = mid + 1
            else:
                hi = mid
        return self.cells[idxs[lo]]


def plan(model: OverlapModel, idx: dict, tasks: tuple, joint: tuple, do_step_cells: list, *, tol: float = 1e-9):
    """Plan | None. `joint` = (cells, cum) of plugin.beyond_joint; `do_step_cells` = [(task, acts)] every do_step row can
    draw. None unless every beyond cell has a band, and every do_step cell can print in every level that has mass."""
    cells, cum = joint
    mass = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, len(cum))]
    tot = cum[-1]
    w: dict = {l: {} for l in BANDS}
    for i, ((t, acts), m) in enumerate(zip(cells, mass)):
        b = model.bands(idx, t, acts)
        if not b:
            return None
        for l in b:
            w[l][i] = m / tot / len(b)
    shares = {l: sum(w[l].values()) for l in BANDS}
    active = [l for l in BANDS if shares[l] > tol]
    if not active:
        return None
    for t, acts in do_step_cells:
        if not set(active) <= model.bands(idx, t, acts):
            return None
    cums = {}
    for l in active:
        ids = sorted(w[l])
        acc, c = 0.0, []
        for i in ids:
            acc += w[l][i]
            c.append(acc)
        cums[l] = (ids, c)
    return Plan({l: shares[l] for l in active}, cells, cums)
