from pathlib import Path
H=Path('.')
def sub(f, old, new, count=1):
    s=(H/f).read_text()
    assert s.count(old)==count, (f, old[:70], s.count(old))
    (H/f).write_text(s.replace(old,new))
sub('plugin.py','''        want_d = plan.gold_abstain
        target = "D" if want_d else LABELS[seed % 3]       # stratified: consecutive seeds cycle A, B, C''','''        want_d = plan.gold_abstain
        # stratified: consecutive seeds cycle A, B, C. A D row is built like any other row (the SAME skeleton: core edit + guard +
        # rewrites, label drawn from the row key) and then made inapplicable (shifted header or one stale line), so the size and the
        # shape of the patch cannot tell D (w4: D patches used to be short single-hunk diffs, +3.5 pp in G6 d_meta)
        target = LABELS[int(uhash(key, "dskel") * 3)] if want_d else LABELS[seed % 3]''')
sub('plugin.py','''        for batch in range(8):
            Rb = random.Random(f"{key}|{self._salt}{attempt}|b{batch}")
            if want_d:
                got = self._d_patch(Rb, orig, mut, held)
                if got:
                    return got, None
                continue
            n_pad''','''        for batch in range(8):
            Rb = random.Random(f"{key}|{self._salt}{attempt}|b{batch}")
            n_pad''')
sub('plugin.py','''                if E.label_of(full) != target:
                    bump("patch:seeded_disagrees")
                    continue
                return PT.make_diff(mut, src, TX.FILE), src''','''                if E.label_of(full) != target:
                    bump("patch:seeded_disagrees")
                    continue
                diff = PT.make_diff(mut, src, TX.FILE)
                if want_d:
                    bad = self._inapplicable(diff, mut, Rb)
                    if bad is None:
                        bump("patch:d_no_corruption")
                        continue
                    return bad, None
                return diff, src''')
sub('plugin.py','''    def _d_patch(self, R, orig, mut, held):''','''    @staticmethod
    def _inapplicable(diff: str, mut: str, R):
        """The same diff made inapplicable: a patch for another version of the file (header shifted) or with one stale context /
        removed line. Same lines, same hunks, same size as an applying patch."""
        for _ in range(6):
            if R.random() < 0.5:
                d = PT.shift_header(diff, R.choice([-2, -1, 1, 2, 3]))
            else:
                ls = diff.split("\\n")
                idx = [i for i, ln in enumerate(ls) if ln[:1] in (" ", "-") and not ln.startswith("---") and ln[1:].strip()]
                if not idx:
                    continue
                i = idx[R.randrange(len(idx))]
                body = ls[i][1:]
                m = re.search(r"\\d", body)
                if m:
                    body = body[:m.start()] + str((int(m.group()) + 1 + R.randrange(8)) % 10) + body[m.end():]
                else:
                    m = re.search(r"[a-z]", body)
                    if not m:
                        continue
                    body = body[:m.start()] + chr((ord(m.group()) - 97 + 1 + R.randrange(24)) % 26 + 97) + body[m.end():]
                ls[i] = ls[i][0] + body
                d = "\\n".join(ls)
            if d != diff and PT.parse_diff(d) and PT.apply_diff(mut, d) is None:
                return d
        return None

    def _d_patch(self, R, orig, mut, held):''')
# edge calls in the test pool; more attempts
sub('plugin.py','ATTEMPTS, ATTEMPTS_HELD = 60, 240','ATTEMPTS, ATTEMPTS_HELD = 200, 240')
sub('plugin.py','''        for _ in range(30):
            c = call_text(entry, gen_args(R, types))
            if c not in seen:
                seen.add(c)
                calls.append(c)
''','''        for _ in range(30):
            c = call_text(entry, gen_args(R, types))
            if c not in seen:
                seen.add(c)
                calls.append(c)
        for edge in range(3):                       # edge calls (empty list / zero / empty text): a mutation that only shows there stays observable
            a = gen_args(R, types)
            for pos, t in enumerate(types):
                a[pos] = ([[], [0], [1]][edge] if t == "ints" else ((0 if edge != 2 else 1) if t == "int" and pos == 0 else (a[pos] if t != "str" else ["", "a", " "][edge])))
            c = call_text(entry, a)
            if c not in seen:
                seen.add(c)
                calls.append(c)
        R.shuffle(calls)
''')
