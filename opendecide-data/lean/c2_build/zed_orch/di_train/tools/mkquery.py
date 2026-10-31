import json,sys
sc=sys.argv[1]
C={ # key: (names, parents)
"logical-entailment":(["logical-entailment","logical entailment propositional logic"],[]),
"temporal-nli":(["temporal-nli","temporal expressions nli"],[]),
"lonli":(["lonli","LoNLI"],[]),"SpaceNLI":(["SpaceNLI"],[]),"tracie":(["tracie"],["ROCStories"]),
"resnli":(["resnli","RESNLI"],["snli"]),"wice":(["wice","WiCE"],[]),
"recast_megaveridicality":(["recast_megaveridicality","MegaVeridicality","DNC"],[]),
"recast_verbnet":(["recast_verbnet","VerbNet"],[]),"recast_factuality":(["recast_factuality"],[]),"recast_puns":(["recast_puns"],[]),
"fool-me-twice":(["fool-me-twice","Fool Me Twice"],[]),"arct":(["arct","argument reasoning comprehension"],[]),"arct2":(["arct2"],[]),
"comve":(["comve","commonsense validation"],[]),"perspectrum":(["perspectrum"],[]),"boardgame-qa":(["Boardgame-QA","BoardgameQA"],[]),
"FOL-nli":(["FOL-nli"],[]),"prontoqa":(["prontoqa"],[]),"spartqa-yn":(["spartqa-yn","SpartQA"],[]),"spartqa-mchoice":(["spartqa-mchoice"],[]),
"stepgame":(["stepgame"],[]),"nlsat":(["nlsat"],[]),"naturallogic":(["naturallogic"],[]),"autotnli":(["autotnli","AutoTNLI"],[]),
"SDOH-NLI":(["SDOH-NLI"],[]),"BioNLI":(["BioNLI"],[]),"doc-nli":(["doc-nli","DocNLI"],[]),"med":(["med","MED monotonicity"],[]),
"nli4wills":(["nli4wills"],[]),"dissonance-detection":(["dissonance-detection"],[]),"winowhy":(["winowhy"],[]),"winodict":(["winodict"],[]),
"cycic_classification":(["cycic_classification","cycic"],[]),"discosense":(["discosense"],[]),"feasibilityQA":(["feasibilityQA"],[]),
"conceptrules_v2":(["conceptrules_v2"],[]),"acceptability-prediction":(["acceptability-prediction"],[]),"blimp_classification":(["blimp_classification","BLiMP"],[]),
"subjectivity":(["subjectivity"],[]),"kaggle-claim-type":(["kaggle-claim-type"],[]),"ukpconvarg":(["ukpconvarg"],[]),"acord":(["acord"],[]),
"patent-phrase-similarity":(["patent-phrase-similarity"],[]),"sbic":(["sbic"],[]),"scruples":(["scruples"],[]),"utilitarianism":(["utilitarianism"],[]),
"goal-step-wikihow":(["goal-step-wikihow"],[]),"mega-acceptability-v2":(["mega-acceptability-v2"],[]),"mega":(["mega"],[]),
"syntactic-augmentation-nli":(["syntactic-augmentation-nli"],["snli","mnli"]),"num-glue":(["num-glue"],[]),"lexcomp":(["lexcomp-nc-relation"],[]),
"spartqa":(["spartqa"],[]),"procedural-typed-decisions":(["procedural-typed-decisions"],[]),"synthetic-typed-decisions":(["synthetic-typed-decisions"],[]),
"measuring-hate-speech":(["measuring-hate-speech-votes"],[]),"jigsaw_toxicity":(["jigsaw_toxicity"],[]),"wikipedia-detox-votes":(["wikipedia-detox-votes"],[]),"edos":(["edos"],[]),
"clcd-english":(["clcd-english"],[]),"context_toxicity":(["context_toxicity"],[]),"sentfin":(["sentfin"],[]),"help-desk-tickets":(["help-desk-tickets"],[]),"it-support-tickets":(["it-support-tickets"],[]),
}
json.dump({"purpose":"DI-TS prefilter","sources":{k:{"names":v[0],"datasets":[],"domains":[],"parents":v[1]} for k,v in C.items()}},open(sc+"/dts_query.json","w"),indent=1)
