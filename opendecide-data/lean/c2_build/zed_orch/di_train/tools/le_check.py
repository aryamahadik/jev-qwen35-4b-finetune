"""Propositional-logic truth-table checker for logical-entailment rows (program gold check, drop only). Pure functions, no eval()."""
import re
TOK=re.compile(r"\s*([()~&|>]|[a-z])")
def tokenize(s):
    pos=0; out=[]
    s=s.strip()
    while pos<len(s):
        m=TOK.match(s,pos)
        if not m: raise ValueError("bad token at %d in %r"%(pos,s))
        out.append(m.group(1)); pos=m.end()
    return out
def parse(toks):
    i=0
    def expr():
        nonlocal i
        t=toks[i]
        if t=='~': i+=1; return ('not',expr())
        if t=='(':
            i+=1; a=expr()
            if toks[i] in '&|>' and toks[i] not in '()':
                op=toks[i]; i+=1; b=expr(); node=({'&':'and','|':'or','>':'imp'}[op],a,b)
            else: node=a
            if toks[i]!=')': raise ValueError("expected )")
            i+=1; return node
        if re.fullmatch(r'[a-z]',t): i+=1; return ('var',t)
        raise ValueError("unexpected "+t)
    e=expr()
    if i!=len(toks): raise ValueError("trailing tokens")
    return e
def variables(e,acc=None):
    acc=set() if acc is None else acc
    if e[0]=='var': acc.add(e[1])
    else:
        for c in e[1:]: variables(c,acc)
    return acc
def ev(e,env,full):
    k=e[0]
    if k=='var': return env[e[1]]
    if k=='not': return full ^ ev(e[1],env,full)
    a=ev(e[1],env,full); b=ev(e[2],env,full)
    if k=='and': return a&b
    if k=='or': return a|b
    if k=='imp': return (full^a)|b
def entails(A,B):
    ea,eb=parse(tokenize(A)),parse(tokenize(B))
    vs=sorted(variables(ea)|variables(eb)); n=len(vs); N=1<<n; full=(1<<N)-1
    env={}
    for j,v in enumerate(vs):
        m=0
        for x in range(N):
            if (x>>j)&1: m|=1<<x
        env[v]=m
    a=ev(ea,env,full); b=ev(eb,env,full)
    return (a & (full^b))==0, n
