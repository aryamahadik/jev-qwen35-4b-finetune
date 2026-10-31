from pathlib import Path
H=Path('.')
def sub(f, old, new, count=1):
    s=(H/f).read_text()
    assert s.count(old)==count, (f, old[:70], s.count(old))
    (H/f).write_text(s.replace(old,new))

# ---- templates: build_module can force the type of the target function
sub('templates.py','def build_module(R, n_fn: int, reducer: str, style: int) -> dict:\n    nm = STYLES[style]\n    n_st = n_fn - 2\n    chosen = R.sample(STAGE_ORDER, n_st)\n',
'''def build_module(R, n_fn: int, reducer: str, style: int, force: tuple | None = None) -> dict:
    """force = (position, stage id): the stage at that position is that type (the others are a uniform draw of the remaining types in
    random order), so the type of the gold function is drawn BEFORE the gold and independent of its position (T43 w4)."""
    nm = STYLES[style]
    n_st = n_fn - 2
    if force is not None and force[0] < n_st:
        rest = R.sample([s for s in STAGE_ORDER if s != force[1]], n_st - 1)
        chosen = rest[:force[0]] + [force[1]] + rest[force[0]:]
    else:
        chosen = R.sample(STAGE_ORDER, n_st)
''')

# ---- plugin: cell-first sampling
sub('plugin.py','''        u_fn = uhash(key, "nfn")
        n_fn = (4 + int(u_fn * 2)) if head == "pvm" else (5 if u_fn < 0.35 else 6 if u_fn < 0.65 else 7 if u_fn < 0.85 else 8)
''','''        u_fn = uhash(key, "nfn")
        n_fn = (4 + int(u_fn * 2)) if head == "pvm" else (5 if u_fn < 0.35 else 6 if u_fn < 0.65 else 7 if u_fn < 0.85 else 8)
        if head == "pvm" and not held:
            n_fn = 4 + (seed // 12) % 2                  # balanced with label (seed % 3) and reducer ((seed // 3) % 4)
''')
sub('plugin.py','''        n_att = ATTEMPTS_HELD if held else ATTEMPTS
        for attempt in range(n_att):
            R = random.Random(f"{key}|{self._salt}{attempt}")
            try:
                spec = self._attempt(R, seed, sampler, head, key, held, style, n_fn, plan, qform, attempt)
            except E.ExecError:
                bump("exec_error")
                continue
''','''        n_att = ATTEMPTS_HELD if held else ATTEMPTS
        self._seed = seed
        for attempt in range(n_att):
            R = random.Random(f"{key}|{self._salt}{attempt}")
            try:
                spec = self._attempt(R, seed, sampler, head, key, held, style, n_fn, plan, qform, attempt)
            except E.ExecTimeout:
                bump("timeout_drop")                     # a wall cap is never a label: the attempt is dropped
                continue
            except E.ExecError:
                bump("exec_error")
                continue
''')
sub('plugin.py','''    def _program(self, R, head: str, n_fn: int, style: int, tj: int):
        if head in ("ll", "pvl"):
            order = TP.S5_ORDER if self._held else TP.LINE_ORDER
            return TP.build_line(R, order[R.randrange(len(order))], style)
        return TP.build_module(R, n_fn, TP.REDUCER_ORDER[R.randrange(4)], style)
''','''    def _program(self, R, head: str, n_fn: int, style: int, tj: int):
        """Training samplers draw the CELL before the gold, by the seed counter (consecutive seeds of a sampler cycle exactly):
        ll: line = seed % 6, template = (seed // 6) % 14; pv lines: label = seed % 3, template = (seed // 3) % 14; pv modules:
        label = seed % 3, reducer = (seed // 3) % 4, size = 4 + (seed // 12) % 2; lf: function = seed % n, the TYPE of that function
        (stage or reducer) = (seed // n) % 9 (or % 4). An attempt that fails (no site, short tests, no patch of the label) redraws
        everything BUT the cell, so P(bug line | template), P(label | template) and P(function | type) are flat by construction
        and no feasibility rate moves them (w4: measured rates were .38 to 1)."""
        s = self._seed
        if head in ("ll", "pvl"):
            if self._held:
                return TP.build_line(R, TP.S5_ORDER[R.randrange(len(TP.S5_ORDER))], style)
            order = TP.LINE_ORDER
            return TP.build_line(R, order[((s // 6) if head == "ll" else (s // 3)) % len(order)], style)
        if self._held:
            return TP.build_module(R, n_fn, TP.REDUCER_ORDER[R.randrange(4)], style)
        if head == "pvm":
            return TP.build_module(R, n_fn, TP.REDUCER_ORDER[(s // 3) % 4], style)
        n_st = n_fn - 2                                                     # lf
        if tj < n_st:
            return TP.build_module(R, n_fn, TP.REDUCER_ORDER[R.randrange(4)], style,
                                   force=(tj, TP.STAGE_ORDER[(s // n_fn) % len(TP.STAGE_ORDER)]))
        red = TP.REDUCER_ORDER[(s // n_fn) % 4] if tj == n_st else TP.REDUCER_ORDER[R.randrange(4)]
        return TP.build_module(R, n_fn, red, style)
''')
sub('plugin.py','    _salt = ""                  # reseed audit only','    _seed = 0\n    _salt = ""                  # reseed audit only')
# none rows get as many tests as a bug row (f2p + p2p): the test count may not tell "none"
sub('plugin.py','''            if len(p2p) < 4:
                return None
            return {"f2p": [], "p2p": p2p[:4], "spare": p2p[4:6]}''','''            tot = n_f2p + n_p2p                       # same count as a bug row (1-2 target + 2 other), so the count is label-blind
            if len(p2p) < tot:
                return None
            return {"f2p": [], "p2p": p2p[:tot], "spare": p2p[tot:tot + 2]}''')
