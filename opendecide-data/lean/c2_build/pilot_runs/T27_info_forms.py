import sys, collections
sys.dont_write_bytecode=True
sys.path.insert(0,'.'); sys.path.insert(0,'families/T27')
import run_pilot as RP
with RP._t27() as kit:
    P=kit.plugin
    from families.T27 import plugin as M
    print(M.CLASSES)
    idx=P._index()
    for k in M.CLASSES:
        fids=idx.get(f"info.{k}",[])
        print(k,len(fids), [kit.ctx.lexicon.forms[f].text[:90] if hasattr(kit.ctx.lexicon.forms[f],'text') else str(kit.ctx.lexicon.forms[f])[:90] for f in fids[:2]])
    print("neutral",[kit.ctx.lexicon.forms[f].text[:80] for f in idx["info.neutral"][:2]])
    print(M.KIND_OF)
