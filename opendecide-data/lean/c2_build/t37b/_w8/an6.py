import pickle,sys,re,collections as C
ch=pickle.load(open(sys.argv[1],'rb'))
fs={'sum':lambda n:sum(n),'last':lambda n:n[-1],'major':lambda n:n[0],'minor':lambda n:n[1] if len(n)>1 else 0,'nzero':lambda n:-sum(1 for x in n if x==0),'maxc':lambda n:max(n),'ncomp':lambda n:len(n),'lex':lambda n:tuple(n)}
for name,f in fs.items():
    for k in (3,4):
        wins=ties=tot=0;above=below=0
        for r,_ in ch:
            if len(r['options'])!=k or r['gold'][0].isdigit()==False: continue
            vs=[o for o in r['options'] if o[0].isdigit()]
            val=lambda o:f([int(x) for x in re.findall(r'\d+',o.split('-')[0].split('+')[0])])
            g=val(r['gold']); ot=[val(o) for o in vs if o!=r['gold']]
            tot+=1
            above+=sum(1 for x in ot if x<g)/len(ot) ; below+=sum(1 for x in ot if x>g)/len(ot)
        print(name,k,tot,'gold>others',round(above/tot,3),'gold<others',round(below/tot,3))
