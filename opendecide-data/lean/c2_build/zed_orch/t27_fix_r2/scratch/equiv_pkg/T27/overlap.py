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

The mechanism needs admitted forms in the bands: the in-scope paraphrases are authored (haiku/ovl_i2/) and merged by
run_pilot_i2.py. v1.4 (fix iteration 2b): `plan()` DROPS a level that some do_step cell cannot print (here `partial`:
the levels left are none and high), removes the few beyond cells with no band left (the joint is then refitted by
plugin.beyond_joint(exclude=...)), and is None (levels off, rows as in iteration 1) only when no level is left or
the removed mass exceeds MAX_DROPPED. Request forms come from ONE pool per (action, level) for both scopes (`pool`):
the forms in the band against some (task, task form) that allows the action; a beyond row draws from the same pool,
filtered by its own task, so the form's identity carries no scope cue. A do_step row draws its task from the task
marginal of its level (`Plan.task`), so the task given the level is the same under every label.
"""
from __future__ import annotations

import re

BANDS = ("none", "partial", "high")
MAX_DROPPED = 0.10          # most beyond-joint mass that `plan` may leave undrawn (cells no pool form can print)
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
        self._p: dict = {}

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

    def pool(self, idx: dict, action: str, framing: str, level: str) -> frozenset:
        """v1.4: THE request-form pool of (action, framing, level), the same for an in-scope and a beyond request: the
        forms that fall in the band `level` against some (task, task form) whose allowed list holds the action. A beyond
        row draws from this pool too (filtered by its own task), so a form's identity says nothing about the scope."""
        k = (action, framing, level)
        if k not in self._p:
            out = set()
            for t, acts in self.scope.items():
                if action not in acts:
                    continue
                for tf in idx.get(t, ()):
                    out |= {rf for rf in idx.get(f"req.{action}.{framing}", ()) if band(self.o(t, tf, action, rf)) == level}
            self._p[k] = frozenset(out)
        return self._p[k]

    def _forms(self, idx: dict, task: str, tf: str, action: str, framing: str, level: str) -> list:
        pl = self.pool(idx, action, framing, level)
        return [rf for rf in idx.get(f"req.{action}.{framing}", ()) if rf in pl and band(self.o(task, tf, action, rf)) == level]

    def candidates(self, idx: dict, task: str, reqs: list, level: str) -> list:
        """[(task form, [pool forms per request])] feasible at `level`. The task form is drawn from the forms that can print
        EVERY action of the task's own list at the level (the in-scope cell), for every label; a beyond row also needs its
        own requests printable (when no such form exists the own-cell feasible ones are used)."""
        own, full = [], []
        for tf in idx[task]:
            per = [self._forms(idx, task, tf, a, fr, level) for a, fr in reqs]
            if not all(per):
                continue
            own.append((tf, per))
            if all(self._forms(idx, task, tf, a, "gate", level) for a in self.scope[task]):
                full.append((tf, per))
        return full or own

    def bands(self, idx: dict, task: str, acts, framings=None) -> frozenset:
        """The levels at which `task` can print requests of `acts` (all in the band) from the pool forms."""
        reqs = list(zip(acts, framings or ["gate"] * len(acts)))
        return frozenset(l for l in BANDS if self.candidates(idx, task, reqs, l))

    def steer(self, level: str, idx: dict, task: str, reqs: list, rng) -> tuple:
        """(task form, [request form per request]) with every request in the band `level`; reqs = [(action, framing)].
        The forms are picked uniformly among the feasible ones; a request form is not printed twice when avoidable."""
        cands = self.candidates(idx, task, reqs, level)
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
        self.dropped, self.dropped_cells = 0.0, frozenset()
        self.tasks: dict = {}                       # level -> (task list, cumulative mass): the task marginal of J_level
        for l in self.levels:
            ids, cum = cums[l]
            m: dict = {}
            prev = 0.0
            for i, c in zip(ids, cum):
                m[cells[i][0]] = m.get(cells[i][0], 0.0) + (c - prev)
                prev = c
            ts = sorted(m)
            acc, cc = 0.0, []
            for t in ts:
                acc += m[t]
                cc.append(acc)
            self.tasks[l] = (ts, cc)

    def task(self, level: str, u: float) -> str:
        """A task drawn from the task marginal of the level's beyond cells: a do_step row draws its task here, so the
        task distribution given the level is the same under every label."""
        ts, cc = self.tasks[level]
        u *= cc[-1]
        for t, c in zip(ts, cc):
            if u < c:
                return t
        return ts[-1]

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
    draw. v1.4: a level that some do_step cell cannot print is DROPPED (the levels left are the ones every cell can
    print) and each beyond cell's mass is split over the bands it has among the levels left. A beyond cell that has no
    band left (no pool form prints its actions at a level left) is not drawn at any level, whatever the label: its mass
    is removed and the rest renormalised, `Plan.dropped` keeps the removed share. None when no level is left or when the
    removed share exceeds MAX_DROPPED."""
    cells, cum = joint
    mass = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, len(cum))]
    tot = cum[-1]
    keep = set(BANDS)
    for t, acts in do_step_cells:
        keep &= model.bands(idx, t, acts)
    if not keep:
        return None
    w: dict = {l: {} for l in BANDS}
    dropped, gone = 0.0, []
    for i, ((t, acts), m) in enumerate(zip(cells, mass)):
        b = model.bands(idx, t, acts) & keep
        if not b:
            dropped += m / tot
            gone.append((t, acts))
            continue
        for l in b:
            w[l][i] = m / tot / len(b)
    if dropped > MAX_DROPPED:
        return None
    shares = {l: sum(w[l].values()) / (1.0 - dropped) for l in BANDS}
    active = [l for l in BANDS if shares[l] > tol]
    if not active:
        return None
    cums = {}
    for l in active:
        ids = sorted(w[l])
        acc, c = 0.0, []
        for i in ids:
            acc += w[l][i]
            c.append(acc)
        cums[l] = (ids, c)
    out = Plan({l: shares[l] for l in active}, cells, cums)
    out.dropped, out.dropped_cells = dropped, frozenset(gone)
    return out
