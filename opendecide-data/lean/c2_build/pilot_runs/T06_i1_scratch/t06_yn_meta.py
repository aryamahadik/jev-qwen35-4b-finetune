import sys, json, collections, importlib, random, copy, numpy as np
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import pilot
rp = importlib.import_module('families.T06.run_pilot')
N = int(sys.argv[1])
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
yn=[i for i in b.infos if i.row['qtype']=='noul']
y = np.array([int(i.row['gold']) for i in yn])
folds = pilot._folds([i.row['meta']['card_id'] for i in yn])
print('n', len(yn), 'yes', y.mean())
drv = pilot.meta_drivers(yn, y, folds, top=12)
for d in drv: print(d)
