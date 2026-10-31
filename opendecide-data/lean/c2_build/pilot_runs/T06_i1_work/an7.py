from an6 import *
def rec_counts(s):  # record count lines/keys
    s=re.sub(r'(days from [^\n:|]*(?:[:|]\s*)?)\d+ days?', r'\1X', s)
    s=re.sub(r'("days_[a-z_]*": ")\d+ days?', r'\1X', s)
    return s
def periods(s):
    return re.sub(r'within \d+ days', 'within X days', re.sub(r'lasts \d+ days', 'lasts X days', s))
def dates(s):
    s=re.sub(r'\b\d{4}-\d\d-\d\d\b','D',s); s=re.sub(r'\b\d{1,2} [A-Z][a-z]+ \d{4}\b','D',s); s=re.sub(r'\b[A-Z][a-z]+ \d{1,2}, \d{4}\b','D',s)
    return s
print(R[3]['ctx'][:2500])
for nm,f in (('rec_counts',rec_counts),('dates',dates),('periods',periods),('rc+dates',lambda s:dates(rec_counts(s))),('rc+periods',lambda s:periods(rec_counts(s)))):
    print(nm, accs([mk(r,f(r['ctx'])) for r in R])[0], flush=True)
