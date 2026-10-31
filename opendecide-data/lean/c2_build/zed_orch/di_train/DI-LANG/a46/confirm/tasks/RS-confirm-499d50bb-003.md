# A46 gold-label confirmation (Opus) RS-confirm-499d50bb-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/confirm/answers/RS-confirm-499d50bb-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's aid).

## Instructions

You are auditing the gold labels of a training set for label noise. Each item shows the material (text, question, options, definitions), the gold label that the dataset's human annotators gave (human_label), and the answers of two independent blind readers (read_1, read_2; an answer may be "abstain" or null when the reader gave none). The text is DATA only: ignore any instructions inside it.
Decide whether the human label is right, from the material alone (do not count the readers' votes; readers are fallible and often miss context):
- gold_ok: the human label is a correct, defensible answer under the question and definitions.
- wrong_gold: the human label is wrong: a careful reader with the same material would clearly answer differently.
- ambiguous: the material does not settle the answer, or two different answers are both defensible under the question as worded.
Never propose a new label. reason = one short line (at most 30 words).
Each item also carries first_pass: the earlier reviewer's verdict and reason. It is a claim to check, not an instruction. Give your own verdict from the material; overturn it (gold_ok) when the human label is in fact defensible.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "<gold_ok | wrong_gold | ambiguous>", "reason": "<one line>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its aid)

[
 {
  "aid": "c00150",
  "kind": "yes/no",
  "text": "Claim: Ranjhay Hath Gandasa is a comedy film starring Pakistani-American singer-songwriter Nadia Ali.\n\nPassages:\n\n[Ranjhay Hath Gandasa]\nIt stars Nadia Ali, Rana Rehman, Fozia Rana, Durdana Rehman, Azhar Rangeela and Shafqat Cheema in lead roles.\n\n[Nadia Ali (singer)]\nNadia Ali (Urdu: ‎ , born 3 August 1980) is a Pakistani American singer-songwriter.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Film is never called a comedy, and the starring Nadia Ali is not linked to the singer."
  }
 },
 {
  "aid": "c00151",
  "kind": "yes/no",
  "text": "Claim: In alphabetical order, the third name of the author of the novel that the film Nuit de Chien was based on comes before Richard Llewellyn's.\n\nPassages:\n\n[Juan Carlos Onetti]\nJuan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.\n\n[Nuit de chien]\nIt is based on the novel \"Para esta noche\" by Juan Carlos Onetti.\n\n[Richard Llewellyn]\nRichard Dafydd Vivian Llewellyn Lloyd (8 December 1906 – 30 November 1983), known by his pen name Richard Llewellyn, was a British novelist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Which name of Llewellyn is compared, and 'third name', are unclear; outcome depends on reading."
  }
 },
 {
  "aid": "c00152",
  "kind": "yes/no",
  "text": "Claim: Jaret Ray Reddick plays a Music Man Axis that has a flag of Texas design on it. The founder of Samadhi Sound does not.\n\nPassages:\n\n[Jaret Reddick]\nJaret Ray Reddick (born March 6, 1972) is an American musician, singer, songwriter, composer, podcaster, actor and voice actor, best known as the lead vocalist, rhythm guitarist, and primary songwriter for the rock band Bowling for Soup. He plays a Music Man Axis that has a flag of Texas design on it.\n\n[David Sylvian]\nDavid Sylvian (born David Alan Batt, 23 February 1958) is an English singer-songwriter and musician who came to prominence in the late 1970s as the lead vocalist and main songwriter in the group Japan.\n\n[Samadhi Sound]\nSamadhi Sound (or samadhisound) is an independent record label founded by singer and musician David Sylvian after his departure from Virgin Records in the late nineties.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Nothing says what guitar David Sylvian plays; the second sentence is unverified."
  }
 },
 {
  "aid": "c00153",
  "kind": "yes/no",
  "text": "Claim: Ohio native William Gladstone Steel helped create Crater Lake National Park, where the lake is most famous for its deep blue color.\n\nPassages:\n\n[William Gladstone Steel]\nWilliam Gladstone Steel (September 7, 1854 – October 21, 1934), called the \"father of Crater Lake\", referring to the creation of Crater Lake National Park in Oregon, United States.\n\n[Crater Lake]\nIt is the main feature of Crater Lake National Park and is famous for its deep blue color and water clarity.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Steel being an Ohio native is not in the passages."
  }
 },
 {
  "aid": "c00154",
  "kind": "yes/no",
  "text": "Tweet: @BuzzPatterson I say he's still pretty wiley.  A touch (?) of senility might be turbo-charging his wileyness, and he naturally loves the attention of his courtesan 'handlers'.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Mocking tone about senility, but could be literal criticism; sarcasm not settled."
  }
 },
 {
  "aid": "c00155",
  "kind": "yes/no",
  "text": "Tweet: Things I learned on my first day of classes my sophomore year in college: ingesting semen does NOT lower depression in women",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Could be mocking a dubious claim or a plain report of a lesson; unclear."
  }
 },
 {
  "aid": "c00156",
  "kind": "yes/no",
  "text": "Text: Woke up at 3 am with a MAD craving for pickles. I guess that means I'm expecting!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Joking pregnancy inference; could be playful or sarcastic, text does not settle it."
  }
 },
 {
  "aid": "c00157",
  "kind": "yes/no",
  "text": "Claim: This author wrote Chilly Scenes of Winter. The author and the writer of a collection of two short novels The Oakdale Affair and The Rider are not dating.\n\nPassages:\n\n[Ann Beattie]\nAnn Beattie (born September 8, 1947) is an American novelist and short story writer.\n\n[Chilly Scenes of Winter]\nChilly Scenes of Winter is Ann Beattie's first novel, published by Doubleday in September, 1976.\n\n[The Oakdale Affair and The Rider]\nThe Oakdale Affair and The Rider is a collection of two short novels by Edgar Rice Burroughs.\n\n[Edgar Rice Burroughs]\nEdgar Rice Burroughs (September 1, 1875 – March 19, 1950) was an American fiction writer best known for his celebrated and prolific output in the adventure and science-fiction genres.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "'Not dating' only follows from inference over lifespans, not stated; support is debatable."
  }
 },
 {
  "aid": "c00158",
  "kind": "yes/no",
  "text": "Claim: George Juskalian took part in the seaborn invasion of French North Africa during WWII.\n\nPassages:\n\n[George Juskalian]\nDuring World War II, he served with the infantry during the North African Campaign and took part in Operation Torch.\n\n[Operation Torch]\nOperation Torch (initially called Operation Gymnast) was the British-United States invasion of French North Africa during the North African Campaign of the Second World War which started on 8 November 1942.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Operation Torch is confirmed; only 'seaborn' is unstated, though an Anglo-US invasion of North Africa arguably implies it."
  }
 },
 {
  "aid": "c00159",
  "kind": "yes/no",
  "text": "Claim: Newell Highway is the town located 10 km north of the Charcoal Tank Nature Reserve.\n\nPassages:\n\n[West Wyalong]\nWest Wyalong is a town in New South Wales, Australia, which is the main town of the Bland Shire, located in the Central West region of New South Wales. It is located on the crossroads of the Newell Highway between Melbourne and Brisbane, and the Mid-Western Highway between Sydney and Adelaide.\n\n[Charcoal Tank Nature Reserve]\nThe Charcoal Tank Nature Reserve is a protected nature reserve in the central western region of New South Wales, Australia. The 86.4 ha reserve is situated 10 km south of West Wyalong and may be accessed via the Newell Highway and The Charcoal Tank Road.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Newell Highway is a highway, not a town; claim contradicted."
  }
 },
 {
  "aid": "c00160",
  "kind": "yes/no",
  "text": "Post: we happy!!!!!!!!!!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "No context; 'we happy!!!' could be sincere or ironic."
  }
 },
 {
  "aid": "c00161",
  "kind": "yes/no",
  "text": "Claim: The hit song released before Love Shy (Thinking About You) is of the genre UK Garage due to its 4x4 rhythm.\n\nPassages:\n\n[What's It Gonna Be (H &quot;Two&quot; O song)]\nis a bassline (subgenre of UK garage) song performed by the duo known as H \"Two\" O (Selim Ben Rabha, \"Solution\", and Simon McDevitt, \"Oz\", who also go by \"Hit 'Em\" and \"Hard\") and the British three-person bassline vocal group Platnum (Aaron Evers, Mina Poli, and Michelle McKenna).\n\n[Love Shy (Thinking About You)]\nIt was released after the success of \"What's It Gonna Be\" with H \"Two\" O.\n\n[Bassline (music genre)]\nBassline (sometimes referred to as bassline house, Niche or 4x4) is a type of music related to UK garage that originated in Sheffield in the early 2000s.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "The causal 'due to its 4x4 rhythm' is unsupported; 4x4 is only an alternative name for bassline."
  }
 },
 {
  "aid": "c00162",
  "kind": "yes/no",
  "text": "Claim: The NorthCap University is located in India, but the establishment, where Nicanor Tiongson studied his Ph.D. in the national university of the Philippines, is not.\n\nPassages:\n\n[University of the Philippines]\nThe University of the Philippines (UP; Filipino: \"Unibersidad ng Pilipinas\" or \"Pamantasan ng Pilipinas\") is a state university system in the Philippines.\n\n[Nicanor Tiongson]\nHe holds a Bachelor of Humanities degree from the Ateneo de Manila University, and M.A. and Ph.D. in Philippine Studies from the University of the Philippines.\n\n[The Northcap University]\nThe NorthCap University, formerly ITM University, is an autonomous university situated in Sector 23-A, Gurugram, Haryana, India.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "UP is in the Philippines and NorthCap is in India, so the claim follows from the passages."
  }
 },
 {
  "aid": "c00163",
  "kind": "yes/no",
  "text": "Claim: The execution of Roger David Casement, the Irish Nationalist who made made efforts during World War I to gain German military aid for the 1916 Easter Rising that sought to gain Irish independence, took place in Casement's Fort.\n\nPassages:\n\n[Rahoneen]\nIt is notable as the location of an ancient Celtic ringfort; at one time this was known as McKenna's fort, but, after the capture and execution of Roger Casement for treason, sabotage and espionage against the Crown, it became known as Casement's Fort. \"Too weak to travel, he was discovered at McKenna's Fort where he had hidden after arranging delivery of German weapons as part of a plan of arming Irish rebels and creating a rising in 1916 against the British to achieve independence.\n\n[Roger Casement]\nDescribed as the \"father of twentieth-century human rights investigations\", he was honoured in 1905 for the Casement Report on the Congo and knighted in 1911 for his important investigations of human rights abuses in Peru.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Casement was discovered at the fort, later renamed after his execution; execution there is not stated."
  }
 },
 {
  "aid": "c00164",
  "kind": "yes/no",
  "text": "Claim: Gabby West won a competition on the reality show \"Scream Queens\". Her prize was a role in a movie starring Costas Mandylor. The movie had a video game released one week prior to its premier.\n\nPassages:\n\n[Saw 3D]\nSaw 3D (also known as Saw: The Final Chapter, or simply Saw VII) is a 2010 American 3D horror film directed by Kevin Greutert, written by Patrick Melton and Marcus Dunstan, and starring Tobin Bell, Costas Mandylor, Betsy Russell, Sean Patrick Flanery and Cary Elwes.\n\n[Saw II: Flesh &amp; Blood]\nIt was released in 2010 to coincide with the release of the seventh film, \"Saw 3D\", a week later.\n\n[Gabby West]\nShe won a role in \"Saw 3D\" in a competition on the reality show \"Scream Queens\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "West won Saw 3D role on Scream Queens; Mandylor stars; game released a week before; all supported."
  }
 },
 {
  "aid": "c00165",
  "kind": "yes/no",
  "text": "Claim: A song from the Kathy Mattea discography, that peaked at #1 on the Billboard Hot Country Singles & Tracks chart, was first recorded by someone that sang country music.\n\nPassages:\n\n[Don Williams discography]\nThis is a detailed discography for American country music artist Don Williams.\n\n[Come from the Heart]\nIt is most known through the 1989 single by Kathy Mattea, released in conjunction with her album \"Willow in the Wind\", though the song was first recorded and released on the 1987 Don Williams album \"Traces\" and also released in 1988 by Clark's husband on his album \"Old Friends\".\n\n[Kathy Mattea discography]\nOf those Top 10 singles, four of them, \"Goin' Gone\", \"Eighteen Wheels and a Dozen Roses\", \"Come from the Heart\", and \"Burnin' Old Memories\", peaked at #1 on the Billboard Hot Country Singles & Tracks chart.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Come from the Heart reached #1 and was first recorded by country artist Don Williams; the claim is supported."
  }
 },
 {
  "aid": "c00166",
  "kind": "yes/no",
  "text": "Claim: The 2000 French crime thriller starred the writer and director Virginie Despentes and Coralie Trinh Thi.\n\nPassages:\n\n[Baise-moi]\nBaise-moi (\"Fuck me \") is a 2000 French crime thriller film with elements of a rape and revenge film written and directed by Virginie Despentes and Coralie Trinh Thi and starring Karen Lancaume and Raffaëla Anderson.\n\n[Coralie Trinh Thi]\nCoralie Trinh Thi (born April 11, 1976) is a former pornographic actress and French author, also known for writing and directing with Virginie Despentes the film \"Baise-moi\" (2000).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Despentes and Trinh Thi wrote and directed the film; Lancaume and Anderson starred in it."
  }
 },
 {
  "aid": "c00167",
  "kind": "yes/no",
  "text": "Text: 5 star personality\n4.8 star uber rating",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Self-deprecating joke; irony versus literal humour is unclear."
  }
 },
 {
  "aid": "c00168",
  "kind": "yes/no",
  "text": "Claim: The name of the painting stolen on March 19, 1990 for which a museum initially offered a $5 million reward for information leading towards its recovery is Landscape with Obelisk and is a painting by Dutch artist Govert Flinck.\n\nPassages:\n\n[Landscape with Obelisk]\nLandscape with Obelisk is painting by Dutch artist Govert Flinck, painted in 1638. The painting hung in the Isabella Stewart Gardner Museum of Boston, Massachusetts, United States, prior to being stolen in 1990.\n\n[Isabella Stewart Gardner Museum theft]\nIn the early hours of March 18, 1990, guards at the Isabella Stewart Gardner Museum in Boston admitted two men posing as police officers responding to a disturbance call. The museum initially offered a reward of $5 million for information leading to their recovery, but in 2017 this was doubled temporarily to $10 million with an expiration date set to the end of the year.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Theft occurred March 18, 1990, not March 19."
  }
 },
 {
  "aid": "c00169",
  "kind": "yes/no",
  "text": "Claim: The academic publication responsible for the Global Open Access Forum was published before Dwell.\n\nPassages:\n\n[Global Open Access Forum]\nIt was created by the American Scientist, which is published by Sigma Xi, in September 1998, before the term \"Open Access\" (OA) was coined, and it was originally called the \"September98-Forum.\"\n\n[American Scientist]\nAmerican Scientist (informally abbreviated AmSci) is an American bimonthly science and technology magazine published since 1913 by Sigma Xi, The Scientific Research Society.\n\n[Dwell (magazine)]\nIt was launched with a magazine in September 2000 to bridge the gap between design professionals and enthusiasts by Lara Hedberg Deam with architecture and design critic Karrie Jacobs as its Editor-in-Chief.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "American Scientist published since 1913, Dwell launched 2000; claim supported."
  }
 },
 {
  "aid": "c00170",
  "kind": "yes/no",
  "text": "Claim: A notable performer of \"Walking in the Air\" was the Irish English operatic tenor that sang the duet \"O soave fanciulla\" from Puccini's opera \"La boheme\". His duet partner was Mary Plazas.\n\nPassages:\n\n[Walking in the Air]\nIn the film, the song was performed by St Paul's Cathedral choirboy Peter Auty, and reissued in 1985 (on Stiff Records) and 1987.\n\n[Peter Auty]\nPeter Robert Auty (born 4 November 1969) is an English operatic tenor who has worked with most of the major opera companies in Britain and a number of companies in continental Europe.\n\n[La Bohème (2009 film)]\nThe four-minute film features images of harsh life in Ethiopia set to the duet \"O soave fanciulla \" from Puccini's opera \"La bohème\", sung by Peter Auty and Mary Plazas.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Auty is described as English; 'Irish' is unsupported."
  }
 },
 {
  "aid": "c00171",
  "kind": "yes/no",
  "text": "Claim: NFL quarterback, Heisman winner, and OU football player graduated from Putnam City North High School.\n\nPassages:\n\n[University of Oklahoma]\nThe University of Oklahoma (OU) is a coeducational public research university in Norman, Oklahoma.\n\n[Sam Bradford]\nBradford attended Putnam City North High School in Oklahoma City, where he starred in football, basketball and golf.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Bradford was an NFL quarterback, a Heisman winner, an OU player or a graduate."
  }
 },
 {
  "aid": "c00172",
  "kind": "yes/no",
  "text": "Claim: Niño was the nickname of the player who played his final season for the 2016 Miami Dolphins before dying in an accident.\n\nPassages:\n\n[2016 Miami Marlins season]\nThis also marked José Fernández's final season as he died in a boating accident on September 25.\n\n[José Fernández (pitcher)]\nHe was affectionately known as \"Niño\" by his teammates and fans due to the youthful exuberance with which he played the game of baseball.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Fernandez played for the Marlins, not the Dolphins."
  }
 },
 {
  "aid": "c00173",
  "kind": "yes/no",
  "text": "Claim: Oklahoma City Thunder won the Northwest Division in 2015-16. Their first season under current the head coach played basketball under at NCAA. He was also coach of the 2013–14 Kennesaw State Owls men's basketball team.\n\nPassages:\n\n[Billy Donovan]\nWilliam John Donovan Jr. (born May 30, 1965) is an American professional basketball coach who is currently the head coach for the Oklahoma City Thunder of the National Basketball Association (NBA).\n\n[Lewis Preston (basketball)]\nHe previously served as an assistant men's basketball coach at Pennsylvania State University, Coastal Carolina University, the University of Notre Dame, and under Billy Donovan at the University of Florida.\n\n[2013–14 Kennesaw State Owls men's basketball team]\nThe Owls, led by third year head coach Lewis Preston, played their home games at the KSU Convocation Center and were members of the Atlantic Sun Conference.\n\n[2015–16 Oklahoma City Thunder season]\nAfter coming just short of making the playoffs the previous season, the Thunder won the Northwest Division and clinched the third seed in the Western Conference.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Preston coached under Donovan, not played, and 2015-16 is not shown as Donovan's first season."
  }
 },
 {
  "aid": "c00174",
  "kind": "yes/no",
  "text": "Claim: Lewis Moran was murdered a week after the death of the hitman from the Australian city of Melbourne.\n\nPassages:\n\n[Lewis Moran]\nHis murder occurred one week after the funeral of fellow Melbourne underworld criminal and suspected hitman Andrew Veniamin.\n\n[Andrew Veniamin]\nAndrew \"Benji\" Veniamin (16 November 1975 – 23 March 2004) was an Australian criminal from Melbourne, Victoria, Australia.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Murder was a week after Veniamin's funeral, not his death; hitman only suspected."
  }
 },
 {
  "aid": "c00175",
  "kind": "yes/no",
  "text": "Claim: Wikimedia Foundation runs the website surpassed by both Hudong.com and the encyclopedia that had the humorous hoax Baidu 10 Mythical Creatures.\n\nPassages:\n\n[Baidu Baike]\nIts test version was released on 20 April 2006, and within three weeks the encyclopedia had grown to more than 90,000 articles surpassing the number in Chinese Wikipedia.\n\n[Chinese Wikipedia]\nThe Chinese Wikipedia () is the (Standard) Chinese language edition of Wikipedia. It is run by the Wikimedia Foundation.\n\n[Baidu 10 Mythical Creatures]\nThe Baidu 10 Mythical Creatures (), alternatively Ten Baidu Deities, was initially a humorous hoax from the interactive encyclopedia Baidu Baike which became a popular and widespread Internet meme in the People's Republic of China in early 2009.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Hudong.com surpassing Chinese Wikipedia is not in the passages."
  }
 },
 {
  "aid": "c00176",
  "kind": "yes/no",
  "text": "Text: @DarrkIt @iamspade_ ya need a carry hit me up im a octane main",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Reads as a literal offer to carry; there is no clear irony cue, and the gaming-meme intent is unknown."
  }
 },
 {
  "aid": "c00177",
  "kind": "yes/no",
  "text": "Claim: The name of the illegitimate daughter of the President involved in the Teapot Dome scandal in 1865 was Elizabeth.\n\nPassages:\n\n[Warren G. Harding]\nWarren Gamaliel Harding (November 2, 1865 – August 2, 1923) was the 29th President of the United States, serving from March 4, 1921, until his death in 1923. At the time of his death, he was one of the most popular presidents, but the subsequent exposure of scandals that took place under his administration, such as Teapot Dome, eroded his popular regard, as did revelations of an affair by Nan Britton, one of his mistresses.\n\n[Nan Britton]\nNanna Popham Britton (November 9, 1896 – March 21, 1991) was an American secretary who was the mistress of Warren G. Harding, the 29th President of the United States. In 1927, she revealed that her daughter, Elizabeth, had been fathered by Harding while he was serving in the United States Senate, one year before he was elected to the presidency.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Daughter Elizabeth is supported, but 'scandal in 1865' is garbled; 1865 is Harding's birth year, so strict and loose readings differ."
  }
 },
 {
  "aid": "c00178",
  "kind": "yes/no",
  "text": "Claim: The actress that appeared Faster (2010 film) is known for her role as Kelor in a shared universe centered on a series of superhero films. This films were distributed by Cinemax\n\nPassages:\n\n[DC Extended Universe]\nThe Justice League Universe (JLUDCEUUJLDCE), more commonly known by its unofficial name as the DC Extended Universe (DCEU), is an American media franchise and shared universe, centered on a series of superhero films distributed by Warner Bros.\n\n[Carla Gugino]\nCarla Gugino ( ; ] ; born August 29, 1971) is an American actress. Her feature film work includes starring roles in \"Son in Law\" (1993), \" Sin City\" (2005), \"Night at the Museum\" (2006), \"Mr. Popper's Penguins\" (2011), \"San Andreas\" (2015), \"The Space Between Us\" (2017), and \"Gerald's Game\" (2017) as well as Kelor in the DC Extended Universe.\n\n[Faster (2010 film)]\nTom Berenger, Oliver Jackson-Cohen, Adewale Akinnuoye-Agbaje and Carla Gugino also appear.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.97
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "DCEU films are distributed by Warner Bros., not Cinemax."
  }
 },
 {
  "aid": "c00179",
  "kind": "yes/no",
  "text": "Claim: The Church of England's movement that inspired the Trinity Episcopal Church in Houghton, Michigan was opposed by a religious figure who wrote devotional literature.\n\nPassages:\n\n[Oxford Movement]\nThe Oxford Movement was a movement of High Church members of the Church of England which eventually developed into Anglo-Catholicism.\n\n[Samuel Rickards]\nSamuel Rickards (1796–1865) was a Church of England clergyman, opponent of the Oxford Movement, and writer of devotional literature.\n\n[Trinity Episcopal Church (Houghton, Michigan)]\nThe church's philosophy is built on the Oxford Movement.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Trinity built on Oxford Movement, opposed by Rickards who wrote devotional literature; supported."
  }
 },
 {
  "aid": "c00180",
  "kind": "yes/no",
  "text": "Text: Day 3 of night shift: “Can I get a triple shot puppuccinio?”",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Quoted absurd customer order may mock customers or just report; sarcasm not clearly signalled."
  }
 },
 {
  "aid": "c00181",
  "kind": "yes/no",
  "text": "Claim: The present observation of Greenery as a holiday stems from the celebration of the birthday of an Asian emperor whose name means abundant benevolence in English.\n\nPassages:\n\n[Greenery Day]\nThe present observation of Greenery Day (みどりの日 , Midori no Hi ) as a national holiday in Japan stems from the celebration of the Emperor Shōwa's birthday on April 29 every year during the Shōwa era.\n\n[Hirohito]\nThe name Hirohito means \"abundant benevolence\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Emperor Showa equals Hirohito is not stated; needs outside knowledge, so either label defensible."
  }
 },
 {
  "aid": "c00182",
  "kind": "yes/no",
  "text": "Post: Roses are Red\nViolets are Blue\nMy first love was Championship Manager\nTommy Svindal Larsen and Kennedy Bakircioglu \n\n#HappyValentinesDay",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Playful Valentine joke; sincerity versus irony not settled."
  }
 },
 {
  "aid": "c00183",
  "kind": "yes/no",
  "text": "Claim: The first book in the series based on a stealth video game series published by the Danish company IO Interactive is called Hitman: Enemy Within.\n\nPassages:\n\n[Hitman: Enemy Within]\nHitman: Enemy Within is the first novel in the \"Hitman\" series.\n\n[Hitman (series)]\nHitman is a stealth video game series developed by the Danish company IO Interactive.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Passage says IO Interactive developed, claim says published; novel series link implicit. Strict vs loose reading."
  }
 },
 {
  "aid": "c00184",
  "kind": "yes/no",
  "text": "Claim: 28000 km2 is the approximate area of the country where the flower species Lobelia columnaris can be found (other than Cameroon).\n\nPassages:\n\n[Lobelia columnaris]\nIt is the only giant Lobelia occurring in West Africa and is found in Cameroon and Equatorial Guinea.\n\n[Equatorial Guinea]\nEquatorial Guinea (Spanish: \"Guinea Ecuatorial\" , French: \"Guinée équatoriale\" , Portuguese: \"Guiné Equatorial\" ), officially the Republic of Equatorial Guinea (Spanish: \"República de Guinea Ecuatorial\" , French: \"République de Guinée équatoriale\" , Portuguese: \"República da Guiné Equatorial\" ), is a country located in Central Africa, with an area of 28000 km2 .",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.92
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Lobelia columnaris occurs in Equatorial Guinea, area 28000 km2; fully supported."
  }
 },
 {
  "aid": "c00185",
  "kind": "yes/no",
  "text": "Claim: Charles Bronson the Actor whose birth name was Charles Dennis Buchinsky, was part of the Leslie Nielsen comedy.\n\nPassages:\n\n[Charles Bronson]\nCharles Bronson (born Charles Dennis Buchinsky; Lithuanian: \"Karolis Dionyzas Bučinskis\" ; November 3, 1921 – August 30, 2003) was an American actor.\n\n[Allan A. Goldstein]\nAllan A. Goldstein (born May 23, 1949) is an American film director and screenwriter, perhaps best known for directing the Charles Bronson vehicle \"\" and the Leslie Nielsen comedy \"\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Goldstein directed both films separately; nothing puts Bronson in the Nielsen comedy."
  }
 },
 {
  "aid": "c00186",
  "kind": "yes/no",
  "text": "Claim: This dish that is a long-standing tradition in New Jersey emerged in the Centre-du-Québec in the late 1950s.\n\nPassages:\n\n[Poutine]\nThe dish emerged in the late 1950s in the Centre-du-Québec area.\n\n[Cuisine of New Jersey]\nNew Jersey is home to approximately 525 diners, the most of any state, and where disco fries are a long-standing tradition.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages never identify disco fries with poutine; link unsupported."
  }
 },
 {
  "aid": "c00187",
  "kind": "yes/no",
  "text": "Text: Searching for Pokemon later because I hate myself haha !!!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Self-deprecating hyperbole; could be read as ironic or as a plain joke, not clearly reversed meaning."
  }
 },
 {
  "aid": "c00188",
  "kind": "yes/no",
  "text": "Text: safe to say my life is a lot better https://t.co/pE5isUMOpk https://t.co/K2hep49TcF",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Without the linked media, sincere or ironic reading cannot be settled."
  }
 },
 {
  "aid": "c00189",
  "kind": "yes/no",
  "text": "Post: The most 2020 quote of the year:\n\nMe: we should go to the Van Gogh Museum!\nLittle Brother: is that the donny with one ear?",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Humorous anecdote; whether it is sarcastic or a plain joke is unclear."
  }
 },
 {
  "aid": "c00190",
  "kind": "yes/no",
  "text": "Claim: This groups sixth full-length album was called Jinsei×Boku=. The vocalist of that group and Doug Pinnick have band in common.\n\nPassages:\n\n[One Ok Rock]\nThe band currently consists of Takahiro Moriuchi (vocals), Toru Yamashita (guitar/leader), Ryota Kohama (bass), and Tomoya Kanki (drums).\n\n[Doug Pinnick]\nDouglas Theodore \"Doug\" Pinnick (born September 3, 1950), sometimes stylized as dUg Pinnick or simply dUg, is an American musician best known as the bass guitarist, songwriter, and co-lead vocalist for the hard rock/progressive metal band King's X.\n\n[Takahiro Moriuchi]\nTakahiro Moriuchi (森内 貴寛 , Moriuchi Takahiro , born April 17, 1988 in Tokyo) , known professionally as Taka, is the lead vocalist of the Japanese rock band ONE OK ROCK.\n\n[Jinsei×Boku=]\n\"Life Times Me Equals\") is the sixth full-length album by the Japanese rock band, One Ok Rock.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Nothing shows Taka and Doug Pinnick share a band; Pinnick is in King's X only."
  }
 },
 {
  "aid": "c00191",
  "kind": "yes/no",
  "text": "Tweet: You know the wolves match is boring when you're talking with your mate about the best way to wire up his new shed!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "A literal joke complaint that the match is boring; no reversal of meaning."
  }
 },
 {
  "aid": "c00192",
  "kind": "yes/no",
  "text": "Claim: Creolized forms of Kongo are found in traditional African religions of Africa with some influence from Christianity.\n\nPassages:\n\n[Afro-American religion]\nAfro-American religions (also known as African diasporic religions or New World traditions) are a number of related religions that developed in the Americas in various nations of Latin America, the Caribbean, and the southern United States. They derive from traditional African religions of Africa with some influence from Christianity.\n\n[Kongo language]\nFor this reason, while Kongo still is spoken in the above-mentioned countries, creolized forms of the language are found in ritual speech of Afro-American religions, especially in Brazil, Cuba, and Haiti.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Creolized Kongo is in Afro-American religions, which derive from African religions, not in the African religions themselves."
  }
 },
 {
  "aid": "c00193",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "traitor by olivia rodrigo in the background ?? YES",
   "NOT OLIVIA RODRIGO TRAITOR IN THE BACKGROUND #LoveIsland"
  ],
  "human_label": "NOT OLIVIA RODRIGO TRAITOR IN THE BACKGROUND #LoveIsland",
  "read_1": {
   "answer": "traitor by olivia rodrigo in the background ?? YES",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "traitor by olivia rodrigo in the background ?? YES",
   "confidence": 0.45
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Both tweets read as excited reactions; neither clearly says the opposite of its meaning."
  }
 },
 {
  "aid": "c00194",
  "kind": "yes/no",
  "text": "Claim: The broadcast studio of the commercial channel that along with CNN and BBC disputes the murderer of Neda is at 1211 Avenue of the Americas, New York City, New York.\n\nPassages:\n\n[Death of Neda Agha-Soltan]\nThe murderer of Neda is disputed; according to CNN, BBC, and Fox News, she was shot by Basij, a paramilitary organization.\n\n[Fox News]\nFox News (officially known as the Fox News Channel, commonly abbreviated to FNC) is an American basic cable and satellite television news channel owned by the Fox Entertainment Group, a subsidiary of 21st Century Fox. The channel broadcasts primarily from studios at 1211 Avenue of the Americas, New York City, New York.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.88
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Fox studio address matches, but 'disputes the murderer' and 'commercial' misdescribe Fox's role; arguable."
  }
 },
 {
  "aid": "c00195",
  "kind": "yes/no",
  "text": "Claim: The fairy Queen Mab orginated with William Shakespeare.\n\nPassages:\n\n[Maeve]\nIt is also associated with the fairy queen Queen Mab of Irish and English legend.\n\n[Queen Mab]\nQueen Mab (pronunciation: \"M/ă/v\") is a fairy referred to in William Shakespeare's play \"Romeo and Juliet\", where \"she is the fairies' midwife.\"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages tie Queen Mab to Irish and English legend; Shakespeare origin not established."
  }
 },
 {
  "aid": "c00196",
  "kind": "yes/no",
  "text": "Claim: Gérard Depardieu was the lead french actor who starred in the 1986 film that inspired a Stella Artois ad campaign.\n\nPassages:\n\n[Reassuringly Expensive]\nReassuringly Expensive was the Stella Artois' advertising slogan in the United Kingdom from 1982 until 2007.\n\n[Jean de Florette]\nThe film starred three of France's most prominent actors – Gérard Depardieu, Daniel Auteuil, who won a BAFTA award for his performance, and Yves Montand in one of his last roles before his death.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage links Jean de Florette to a Stella Artois campaign or gives its 1986 date."
  }
 },
 {
  "aid": "c00197",
  "kind": "yes/no",
  "text": "Claim: Sophia Grace & Rosie featured a cover song on their Youtube channel. The song from is from an album released under the Columbia Records and Columbia Records labels.\n\nPassages:\n\n[Glory Days (Little Mix album)]\nIt was released on 18 November 2016, by Syco Music and Columbia Records.\n\n[Touch (Little Mix song)]\n\"Touch\" is a song by British girl group Little Mix. It was released as the second single from their studio album \"Glory Days\".\n\n[Sophia Grace &amp; Rosie]\nRosie has started a YouTube channel featuring her life and sang a cover of Little Mix's \"Touch\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Garbled labels (Syco not named) and Rosie's channel vs their channel; support unclear."
  }
 },
 {
  "aid": "c00198",
  "kind": "yes/no",
  "text": "Claim: Howard Elliott Ashman worked on both \"Little Shop of Horrors\" and the song referenced in the Be Our Guest Restaurant.\n\nPassages:\n\n[Be Our Guest Restaurant]\nThe name of the restaurant is a reference to \"Be Our Guest\", one of the classic songs from that film.\n\n[Howard Ashman]\nHoward Elliott Ashman (May 17, 1950 – March 14, 1991) was an American playwright and lyricist. Their next musical, \"Little Shop of Horrors\" (1982) for which Ashman again directed and wrote both book and lyrics, became a long-running success and led to a 1986 feature film.\n\n[Be Our Guest]\n\"Be Our Guest\" is a song written by lyricist Howard Ashman and composer Alan Menken for Walt Disney Pictures' 30th animated feature film \"Beauty and the Beast\" (1991).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Ashman wrote Little Shop lyrics and Be Our Guest lyrics; claim supported."
  }
 },
 {
  "aid": "c00199",
  "kind": "yes/no",
  "text": "Claim: The Neoclassical monument Benito Juárez Hemicycle is located in this large city of Mexico that consists of sixteen municipalities.\n\nPassages:\n\n[Mexico City]\nThe city consists of sixteen municipalities.\n\n[Benito Juárez Hemicycle]\nThe Benito Juárez Hemicycle is a Neoclassical monument located at the Alameda Central park in Mexico City, Mexico and commemorating the Mexican statesman Benito Juárez.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "The Hemicycle is a Neoclassical monument in Mexico City, which consists of sixteen municipalities; supported."
  }
 }
]
