# G9 re-read confirmation (Opus, ambiguous flags) GB-CAMB-000 (family GB)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/fam/GB/confirm_amb/answers/GB-CAMB-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 1. Answers expected: 1 (one per item, each with that item's qid).

## Instructions

A first reader flagged each item below as wrong_gold or ambiguous (their flag and reason are shown as first_flag / first_reason). Re-judge each item yourself from the text, definitions and question alone, without deferring to the first reader. program_answer is the dataset program's answer.
- gold_ok: program_answer is correct and no other answer is defensible;
- wrong_gold: program_answer is wrong;
- ambiguous: two answers are defensible, or the item does not settle the answer.
You only flag. Never propose a new label. Give a short reason (at most 25 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "gold_ok" | "wrong_gold" | "ambiguous", "reason": "<at most 25 words>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "aid": "a0021",
  "kind": "choice",
  "text": "Structure of a bacterial ribonucleoprotein complex central to the control of cell envelope biogenesis\nThe biogenesis of the essential precursor of the bacterial cell envelope, glucosamine-6-phosphate (GlcN6P), is controlled through intricate post-transcription networks mediated by GlmZ, a small regulatory RNA (sRNA). GlmZ stimulates translation of the mRNA encoding GlcN6P synthetase in Escherichia coli, but when bound by the protein RapZ, it becomes inactivated through cleavage by the endoribonuclease RNase E. Here we report the cryoEM structure of the RapZ:GlmZ complex, revealing a complementary match of the protein tetrameric quaternary structure to an imperfect structural repeat in the RNA. The RNA is contacted mostly through a highly conserved domain of RapZ that shares deep evolutionary relationship with phosphofructokinase and suggests links between metabolism and riboregulation. We also present the structure of a pre-cleavage encounter intermediate formed between the binary RapZ:GlmZ complex and RNase E that reveals how GlmZ is presented and recognised for cleavage. The structures suggest how other encounter complexes might guide recognition and action of endoribonucleases on target transcripts, and how structured substrates in polycistronic precursors are recognised for processing.",
  "question": "What is the main kind of thing this study is about?",
  "options": [
   "people",
   "animal, plant or ecosystem",
   "microbe or virus",
   "cell, protein or molecule",
   "method or software"
  ],
  "definitions": "- people: Pick this when the main subject is human health, human behaviour or the human body, such as patients or volunteers.\n- animal, plant or ecosystem: Pick this when the main subject is a whole living animal or plant, or a natural place such as a forest, pond or field, and not people or microbes.\n- microbe or virus: Pick this when the main subject is a bacterium, fungus or virus, including its genes, growth or behaviour.\n- cell, protein or molecule: Pick this when the main subject is cells grown in a lab, or proteins, drugs or other molecules, rather than a whole living body or organism.\n- method or software: Pick this when the main thing described is a new technique, calculation, computer model or software that others could use.",
  "program_answer": "cell, protein or molecule",
  "first_flag": "ambiguous",
  "first_reason": "E. coli RNA-protein complex structure: microbe (bacterial genes) or molecule both defensible."
 }
]
