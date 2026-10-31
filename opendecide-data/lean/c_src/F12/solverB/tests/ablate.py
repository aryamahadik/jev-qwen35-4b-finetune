"""Sensitivity check for solver B: switch off one rule at a time and count gold/outcome disagreements on a subset.
A rule that is decisive somewhere must produce disagreements when removed (shows the agreement is not vacuous)."""
import sys, os, json, importlib, collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['F12B_LIMIT'] = sys.argv[1] if len(sys.argv) > 1 else '2500'
import solver_b as B
reads, _ = B.pack_reads(['candidates_r1', 'qc_sample', 'mixdev_S5'])
orig = {k: getattr(B.Row, k) for k in ('match_sql', 'answer_shown', 'chain', 'load_mentions')}
orig_yn, orig_compile, orig_defects = B.yn, B.compile_schema, B.Audit.defects

def m_noscope(self, tids):
    r = orig['match_sql'](self, tids); return {k: (True, v[1], v[2]) for k, v in r.items()}
def m_nopre(self, tids):
    r = orig['match_sql'](self, tids); return {k: (v[0], True, v[2]) for k, v in r.items()}
def m_norole(self, tids):
    r = orig['match_sql'](self, tids); return {k: (v[0], v[1], False if False else True) for k, v in r.items()}
def nofresh(self, req, walk):
    f = self.pol.get('fresh'); self.pol['fresh'] = None
    try: return orig['answer_shown'](self, req, walk)
    finally: self.pol['fresh'] = f
def nochain(self, *a): return None
def nolimits(tool, ctx):
    t2 = json.loads(json.dumps(tool))
    for p in t2['params']:
        p['min'] = p['max'] = None; p['minlen'] = p['maxlen'] = None
    return orig_compile(t2, ctx)
def nocons(tool, ctx):
    t2 = dict(tool); t2['cons'] = []; return orig_compile(t2, ctx)
def noframing(base, framing, neg, nmean): return orig_yn(base, None, neg, nmean)
def noneg(base, framing, neg, nmean): return orig_yn(base, framing, 0, nmean)
ABL = {'scope': ('Row.match_sql', m_noscope), 'precondition': ('Row.match_sql', m_nopre),
       'role': ('Row.match_sql', m_norole), 'freshness': ('Row.answer_shown', nofresh), 'chain': ('Row.chain', nochain),
       'limits': ('compile_schema', nolimits), 'cross_param': ('compile_schema', nocons),
       'framing': ('yn', noframing), 'negation': ('yn', noneg)}
res = {}
for name, (tgt, fn) in ABL.items():
    if tgt.startswith('Row.'):
        setattr(B.Row, tgt[4:], fn)
    else:
        setattr(B, tgt, fn)
    tot = collections.Counter()
    for f in ('candidates_r1', 'qc_sample'):
        r, m = B.check_file(f, reads)
        tot['rows'] += r['rows']; tot['gold'] += r['gold_mismatch']; tot['outcome'] += r['outcome_mismatch']
        tot['flags'] += r['flags']
    res[name] = dict(tot)
    for k, v in orig.items(): setattr(B.Row, k, v)
    B.yn, B.compile_schema = orig_yn, orig_compile
    print(name, dict(tot), flush=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ablation.json'), 'w'), indent=1)
