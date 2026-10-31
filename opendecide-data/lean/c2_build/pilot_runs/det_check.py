import sys, hashlib, json, os
sys.path.insert(0, '.')
import pilot as P, pilot_loaders as PL
fid = sys.argv[1]
with PL.open_family(fid) as kit:
    b = P.build_pilot(kit, P.N_ROWS, run_g15=False)
    body = "".join(json.dumps(i.row, ensure_ascii=False) + "\n" for i in b.infos)
rep = json.load(open(PL.family_dir(fid) / 'pilot' / 'PILOT_REPORT.json'))
print(fid, os.environ.get('PYTHONHASHSEED'), hashlib.sha256(body.encode()).hexdigest()[:16], rep['files']['rows_sha256'][:16],
      'SAME' if hashlib.sha256(body.encode()).hexdigest() == rep['files']['rows_sha256'] else 'DIFF', flush=True)
