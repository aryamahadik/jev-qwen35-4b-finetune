"""Determinism of the T15 iteration-1 pilot: rows / relations sha256 under this PYTHONHASHSEED vs pilot_i1/PILOT_REPORT.json."""
import sys, hashlib, json, os
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
import pilot as P, pilot_loaders as PL
with PL.open_family('T15') as kit:
    b = P.build_pilot(kit, P.N_ROWS, run_g15=False)
    rows = "".join(json.dumps(i.row, ensure_ascii=False) + "\n" for i in b.infos)
    rels = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in b.rels)
rep = json.load(open(PL.family_dir('T15') / 'pilot_i1' / 'PILOT_REPORT.json'))
hr, hl = hashlib.sha256(rows.encode()).hexdigest(), hashlib.sha256(rels.encode()).hexdigest()
print('PYTHONHASHSEED', os.environ.get('PYTHONHASHSEED'), 'rows', hr[:16], 'relations', hl[:16],
      'rows==report', hr == rep['files']['rows_sha256'], 'relations==report', hl == rep['files']['relations_sha256'], flush=True)
