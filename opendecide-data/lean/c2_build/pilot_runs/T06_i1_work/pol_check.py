import sys, importlib
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
rp=importlib.import_module('families.T06.run_pilot')
with rp._t06() as kit:
    q=kit.plugin.quarantined_wordings(kit.ctx)
    print('quarantined', len(q))
    from collections import Counter
    n=Counter(w.qform for w in kit.ctx.wordings.values()) if hasattr(kit.ctx,'wordings') else None
    print(n)
