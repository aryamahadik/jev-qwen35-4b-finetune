"""Sonnet first-pass verdicts -> Opus confirm task files. Usage: python -B dits_confirm.py <di_train_dir>"""
import sys, json
D = sys.argv[1]; DT = f"{D}/DI-TS"; R = f"{DT}/reads"
# index in SCORE.json flagged list -> (call, reason <=20 words)
G, W, A = "gold_ok", "wrong_gold", "ambiguous"
FP = {0:(G,"truth table: A true only with f true, h false; w true then makes B false; does not entail"),
1:(W,"after Monday and before Sunday is satisfiable (Tue-Sat), so neutral not contradiction"),
2:(W,"open at 11 AM and open after 23:00 can both hold; not a contradiction"),
3:(W,"after Wednesday and before Sunday is satisfiable"),4:(W,"after Tuesday and before Sunday is satisfiable"),
5:(A,"weekday order is cyclic here; after Saturday before Thursday is reading dependent"),
6:(A,"after 02:00 and before 00:00 depends on whether the day wraps"),
7:(W,"Jan and January are the same month; the statements are equivalent"),8:(W,"Oct and October are the same month; equivalent"),
9:(A,"day granularity: before Wednesday and after Tuesday leaves no whole day; template convention"),
10:(A,"month granularity: before March vs after February leaves no whole month; template convention"),
11:(A,"before Friday vs after Thursday leaves no whole day; template convention"),
12:(A,"after Nov vs before Dec leaves no whole month; template convention"),
13:(A,"before May vs after April leaves no whole month; template convention"),
14:(A,"after September vs before October leaves no whole month; template convention"),
15:(A,"before March vs after February leaves no whole month; template convention"),
16:(A,"before Saturday vs after Friday leaves no whole day; template convention"),
17:(A,"after Friday vs before Saturday leaves no whole day; template convention")}
for i in range(18,28): FP[i]=(A,"inclusive vs exclusive span counting; gold follows one convention, natural reading differs")
for i,c,r in [(28,A,"link between perspective and claim is indirect"),(29,A,"independence as a route out of the EU can cut either way"),
(30,A,"perspective too vague to fix a stance"),(31,W,"argues the US needs its strength, which opposes abolition"),
(32,W,"wide visitor access is an argument against repatriation"),(33,A,"perspective lacks context to fix a stance"),
(34,G,"environmental harm of high speed backs lower limits"),(35,G,"describes tenure protecting experienced teachers, a pro-tenure point"),
(36,A,"threat from Iran can be a reason for or against elimination"),(37,W,"disposal difficulty is an argument against disarming"),
(38,A,"link to a right to nuclear weapons is indirect"),(39,W,"praises the UN, which opposes reform or replacement"),
(40,G,"rapid de-escalation supports tactical weapons"),(41,G,"non-violent first fits blocking access as a milder tool"),
(42,A,"stance toward a scam claim is unclear"),(43,W,"higher prices argue against wind farms"),
(44,A,"healthy diet at home can support or replace a ban"),(45,A,"blame spread over several people cuts against the claim or neutral"),
(46,A,"link to phone ownership is unclear"),(47,W,"unfair patent laws argue for producing generics"),
(48,A,"verbal fight rather than guns neither clearly supports nor undermines winnable"),(49,A,"stance toward consent unclear"),
(50,W,"mental state excuses him, supports the claim"),(51,G,"willing but not paying argues voluntary fee fails"),
(52,A,"double standards argument fits either side"),(53,A,"stance toward protest value unclear"),
(54,A,"conditional policy vs exchange of ideas is indirect"),(55,W,"own propaganda version is an argument for publishing it"),
(56,A,"reading of reduced trust is ambiguous"),(57,G,"better exemption candidates undermines celebrity exemption"),
(58,W,"states cannot afford the cost, an argument that the US must help"),(59,A,"before 12 AM against 2 AM depends on day wrap"),
(60,A,"after 13:00 and before 5 AM are compatible on different days"),(61,W,"after Tuesday and before Sunday is satisfiable"),
(62,A,"inclusive vs exclusive span counting"),(63,W,"fall-back option argues for allowing it, undermining the claim"),
(64,G,"concept needing words supports language controls thought"),(65,A,"devolving below national level has an indirect link")]: FP[i]=(c,r)
S = json.load(open(f"{R}/SCORE.json"))["flagged"]; assert set(FP) == set(range(len(S))), "first pass incomplete"
json.dump({S[i]: {"call": c, "reason": r} for i, (c, r) in FP.items()}, open(f"{R}/FIRST_PASS.json", "w"), indent=1)
key = json.load(open(f"{R}/keys/key.json")); rows = {}
for f in ("candidates_stage.jsonl", "mixdev_S5_stage.jsonl"):
    for l in open(f"{DT}/stage/{f}", encoding="utf8"): x = json.loads(l); rows[x["id"]] = x
inv = {}
for k, v in key.items(): inv.setdefault(v, {})[k[0]] = k.split(":")[1]
T = json.load(open(f"{R}/TASKS.json")); ans = {}
for t in T.values():
    for o in json.load(open(t["answer_file"])): ans[(t["reader"], o["qid"])] = o
called = [S[i] for i in sorted(FP) if FP[i][0] != G]
import os; os.makedirs(f"{DT}/confirm/tasks", exist_ok=True); os.makedirs(f"{DT}/confirm/answers", exist_ok=True)
HEAD = """# A61 DI-TS label-noise confirmation {tid} (Opus)

ANSWER FILE (write your whole answer here, with the Write tool, and nowhere else):
{af}

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web.

Items: {n}. Each item is a training row of a public-source dataset whose gold label was set by the dataset creator (program or crowd). Two blind readers disagreed with the gold (or one disagreed and the other abstained), and a first-pass reviewer called it wrong_gold or ambiguous. You rule on each row.

Verdicts: "wrong_gold" = a careful reader of the text, the options and the definitions would pick a different option than the gold; "ambiguous" = the row has no single defensible answer under the options and definitions, so it should not train the model; "gold_ok" = the gold is the defensible answer and the row stays. Rows are only dropped, never relabelled. Keep the bar: do not drop a row just because it is hard. Template-style rows (temporal, logic) may follow a convention that a careful reader would not infer from the text: if the text alone does not fix the gold, call it ambiguous.

Answer contract: one JSON array, one object per item: {{"id": "<the item id>", "verdict": "gold_ok|wrong_gold|ambiguous", "reason": "<= 25 words"}}. Exactly those keys, valid JSON only, no text before or after.

## Items
"""
tasks = []
for ci in range(0, len(called), 40):
    ch = called[ci:ci + 40]; tid = f"DTS-confirm-{ci // 40:03d}"
    af = f"{DT}/confirm/answers/{tid}.json"; tf = f"{DT}/confirm/tasks/{tid}.md"
    items = []
    for rid in ch:
        x = rows[rid]; opts = x["options"]; opts = eval(opts) if isinstance(opts, str) else opts
        rd = lambda r: (lambda o: o["answer"] if o else "missing")(ans.get((r, inv[rid][r])))
        items.append({"id": "i" + rid.split(":")[1], "text": x["state"], "question": x["instructions"], "options": opts, "definitions": x["card"], "gold": x["gold"], "reader_A": rd("A"), "reader_B": rd("B"), "first_pass": FP[S.index(rid)][0], "first_pass_reason": FP[S.index(rid)][1]})
    open(tf, "w", encoding="utf8").write(HEAD.format(tid=tid, af=af, n=len(items)) + json.dumps(items, ensure_ascii=False, indent=1) + "\n")
    tasks.append({"task_file": tf, "answer_file": af, "model": "opus"})
json.dump(tasks, open(f"{DT}/confirm/TASKS.json", "w"), indent=1)
print(len(called), "called;", len(tasks), "confirm files")
