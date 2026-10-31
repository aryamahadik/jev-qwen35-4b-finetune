import sys, json
sys.path.insert(0,'.')
import calib_dev_analysis as C
FR={'C1':{'noul':1.3,'choice':1.25},'C2':{'noul':0.8,'choice':0.95}}
models={'C1':'q35_4b_main500k_c2','C2':'q35_4b_c2'}
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
out={}
def run(label_prefix, getrows):
    for name,mf in models.items():
        rows=getrows(mf)
        r=C.summarize(rows,f'{label_prefix}|{name}',FR[name])
        print(json.dumps(r))
        out[f'{label_prefix}|{name}']=r
# mixdev
run('mixdev_all', lambda mf: C.rows_for('preds_c2_mixdev','c2_mixdev',mf))
# transfer
run('transfer600', lambda mf: C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf))
for src in ('c2_t19','c2_t21'):
    run(src, lambda mf, src=src: [r for r in C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf) if r['source']==src])
# general pooled
def gen(mf):
    allr=[]
    for d in GEN:
        try:
            allr+=C.rows_for(f'preds_{d}',d,mf)
        except Exception as e:
            print('skip',d,e)
    return allr
run('general_pooled9', gen)
for d in GEN:
    run(d, lambda mf, d=d: C.rows_for(f'preds_{d}',d,mf))
json.dump(out,open('calib_out_main.json','w'),indent=1)
