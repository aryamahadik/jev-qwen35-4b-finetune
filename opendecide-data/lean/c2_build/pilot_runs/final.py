import sys, json; sys.path.insert(0, '.')
import pilot_loaders as PL
key = json.load(open('pilot_runs/keyfind.json'))
fams = ['T35','T30','T24','T33','T29','T31','T32','T23','T15','T12','T25','t37b','T36','T21','T20']
PROG = ("G2", "G3", "G4", "G-SL", "G-LEX", "G-TW", "G15", "schema", "options")
def compact(g):
    out = []
    for name, d in g.items():
        v = d.get('verdict')
        if name == 'pilot_size':
            out.append(f"pilot_size {v}: {d['value']} rows (bar >= 1,000)")
        elif name in PROG:
            out.append(f"{name} {v}: {d['units_failed']}/{d['units_attempted']} units failed (bar 100%" + (", failing rows dropped" if name == 'G-SL' else "") + ")")
        elif name == 'drops_outside_gates':
            if d['counts']: out.append(f"other drops (report): {d['counts']}")
        elif name == 'S14_floors_caps':
            r = d['report']
            out.append(f"S14 floors/caps {v}: implicit {r.get('implicit_share')}, non-syntactic {r.get('non_syntactic_share')}, max source {round(r.get('max_source_share') or 0, 3)}, max wording key {round(r.get('max_template_share') or 0, 3)} (bars: >= 0.25, >= 0.30 of complements; source <= floor(10%), wording key <= max(1, floor(2%)) of rows)")
        elif name == 'G6':
            parts = []
            for part in ('yes_no', 'choice'):
                p = d.get(part) or {}
                if p.get('n') and 'skipped' not in p:
                    best = max((p[vw][m], vw, m) for vw in p if isinstance(p[vw], dict) and 'lr' in p[vw] for m in ('lr', 'gbt'))
                    parts.append(f"{part} n={p['n']} chance {p['chance']} max {best[0]} ({best[1]}/{best[2]})")
            out.append(f"G6 {v}: {'; '.join(parts)}; {len(d['fails'])} view/model fails (bar chance + 2 pp)")
        elif name == 'G7':
            out.append(f"G7 {v}: {d['n_tests']} features, fails raw {d['n_yes_no_raw_fails']} / card-adjusted {d['n_yes_no_card_adjusted_fails']} / choice {d['n_choice_fails']} (bar 0 at Bonferroni alpha 0.01)")
        elif name in ('G10', 'overlay', 'spec_3_0'):
            fails = []
            for k in d['failing']:
                c = d['checks'][k]; val = c['value']
                if isinstance(val, dict): val = json.dumps(val.get('chi2_p', val), separators=(',', ':'))[:80]
                fails.append(f"{k}={val} (bar {c['bar'].split(' (')[0]})")
            out.append(f"{name} {v}" + (": fails " + "; ".join(fails) if fails else ": all checks pass"))
        elif name in ('G3-H', 'G5-H', 'S13'):
            n = d.get('items', d.get('rows', d.get('units'))) or 0
            out.append(f"{name} {v}: {d.get('tasks', 0)} task file(s), {n} item(s)" + (f" - {d['note']}" if v == 'n/a' else ""))
    return "\n".join(out)
fam_out = []
for f in fams:
    pdir = PL.family_dir(f) / 'pilot'
    rep = json.load(open(pdir / 'PILOT_REPORT.json'))
    s, b = rep['summary'], rep['build']
    units = b.get('units_written'); att = b.get('units_attempted', b.get('candidates'))
    status = (f"Pilot {s['verdict']}. {rep['files']['n_rows']} rows in {units} passing units written ({att} attempted) "
              f"to {pdir}/rows.jsonl with relations.jsonl and PILOT_REPORT.json. Failing: {', '.join(s['fail']) or 'none'}. "
              f"Pending (Haiku chunks written): {', '.join(s['pending']) or 'none'}. " + key[f])
    chunks = [{"file": t['task_file'], "answer_file": t['answer_file']} for ts in rep['chunks'].values() for t in ts]
    fam_out.append({"id": f, "status": status, "gates": compact(rep['gates']), "chunks": chunks})
json.dump(fam_out, open('pilot_runs/final_families.json', 'w'), indent=1)
print(sum(len(x['chunks']) for x in fam_out), 'chunks;', len(json.dumps(fam_out)), 'chars')
