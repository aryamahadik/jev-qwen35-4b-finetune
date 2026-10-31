"""T01 scratch: what-if. The frozen pools plus the fixture double-negation stand-ins (admitted in memory only, NOT a pool):
program gates and the double-negation share of the pilot. Report only."""
import sys, json
sys.path.insert(0, '.')
import dataclasses
import pilot, pilot_loaders as PL
from c2_kit.lexicon import question_sem
from c2_kit.plugin import KitCtx
from c2_kit.skin import make_skin
from families.T01 import fixtures as FX, plugin as P
with PL.open_family("T01") as kit:
    reg = kit.ctx.lexicon
    for qf, meaning in FX.DNEG_MEANINGS.items():
        reg.declare(question_sem("T01", qf), "question", meaning)
    skins = dict(kit.ctx.skins)
    for wid, qf, text, slots in FX.DNEG_WORDINGS:
        f = reg.add(text, question_sem("T01", qf), slots=dict(slots), family="T01")
        reg.unit_test_all()
        for e in range(f.required):
            reg.record_extraction(f.form_id, f"fixture:stand-in-{e+1}", f.sem_id)
        skins[wid] = make_skin(wid, "T01", text, dict(slots), kind="wording", register="question", qform=qf,
                               lexicon_ids=(f.form_id,))
    ctx = KitCtx(skins=skins, lexicon=reg)
    plugin = P.T01(lexicon=reg)
    kit2 = dataclasses.replace(kit, plugin=plugin, ctx=ctx)
    print("dneg_ok", plugin.dneg_ok, flush=True)
    b = pilot.build_pilot(kit2, 1000, run_g15=True, log=lambda m: None)
    print("built", b.stats["rows_written"], "units", b.stats["units_written"], "attempted", b.stats["units_attempted"], "drops", b.stats["drops_by_gate"])
    pg = pilot.program_gates(b)
    print({k: v["verdict"] for k, v in pg.items()})
    g10 = pilot.g10(b.infos, b.units, plugin)
    c = g10["checks"]
    print("G10", g10["verdict"], g10["failing"], "double_negation", c["double_negation_share"]["value"], "syn", c["syntactic_negation_share"]["value"], "yes_rate", c["yes_rate"]["value"])
    yn = [i for i in b.infos if i.row["qtype"] == "noul"]
    dn = [i for i in yn if i.row["meta"]["qform"].startswith("yn_dneg")]
    print("dneg rows", len(dn), "of", len(yn), "yes/no rows")
