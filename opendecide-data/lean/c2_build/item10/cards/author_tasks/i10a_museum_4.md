# Item 10 card authoring i10a_museum_4

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_museum_4.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of artworks and objects, written for an art museum's collection website.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: material or technique: how the object was made, where neighbouring answers are easy to confuse.
Card 2 angle: curator task: what job a museum team would give the description (catalogue, label, story, loan file), where neighbouring answers are easy to confuse.
Card 3 angle: description focus: what the description spends most of its words on (looks, maker, history, use, meaning), where neighbouring answers are easy to confuse.
The three cards must ask three different decisions, not three wordings of one decision.

Rules for all three cards:
1. A careful reader must be able to decide the answer from the text alone, with no outside knowledge.
2. The question must apply to most texts of this kind, not only to these 12 examples.
3. Use plain everyday words. No jargon and no academic terms.
4. Options must not overlap: for any text exactly one option fits best. The last option may be a catch-all (for example
   "something else"), and its definition must say exactly when to pick it.
5. Give every option a one-sentence definition that says exactly when to pick it.
6. Boundary rule, the heart of this task: build the options as near neighbours. At least two pairs of options must be easy to
   confuse for a hurried reader. For every such pair, the two definitions must state the dividing line: what the text must say
   or do to belong to the first option and not to the second.
7. Balance: choose questions where each option is the right answer for a fair share of texts of this kind. No option should
   fit more than half of the texts.
8. Do not copy label names or label sets from public datasets or benchmarks (for example positive/negative/neutral sentiment
   scales, entailment/contradiction, star ratings, standard emotion lists, standard news or topic category lists, or intent
   lists from chatbot or banking datasets). Invent labels that fit the real decision.
9. Do not ask about anyone's identity, health or other personal traits, and do not ask for an opinion about a named person.
10. Do not label, summarise or quote the example texts. Your output holds only the 3 cards.

Labels are short (1 to 5 words), lower case unless a proper noun, and unique within a card. expected_share is your rough guess
for texts of this kind in general, not a count over the examples; the shares of a card sum to 1.

## Answer contract

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top.

{"task_id": "i10a_museum_4",
  "cards": [
    {"kind": "choice",
      "who_decides": "one sentence: who makes this decision and why",
      "question": "the question, ending with a question mark",
      "options": [{"label": "short label", "definition": "one sentence"}, "... 4 to 8 options in total"],
      "expected_share": {"<each label>": 0.2}},
    "... exactly 3 cards in total"
  ]}

The items below are read-only context (the example texts). Your answer holds exactly 3 cards.

## Example texts (JSON; read-only context, not items to answer)

[
 {
  "sid": "s01",
  "text": "Rectangular Cauldron\nUnlike most bronze vessels whose shapes were derived from prehistoric ceramic forms, this type of rectangular container was invented by Shang bronze artisans. Each side features a pair of profile birds with long, trailing tailfeathers. The black material in sunken areas of this design contains carbon. This filler is common to many Shang bronzes and seems to have been deliberately applied after casting in order to emphasize the surface decoration."
 },
 {
  "sid": "s02",
  "text": "Courting Komachi (Kayoi Komachi), from the series Seven Fashionable Figures of Ono no Komachi (Furyu nana Komachi yatushi sugata-e)\nIn this print, a contemporary courtesan and her attendant walk at night, presumably to visit a client. The latter holds a lantern that shines a beam of light across the design, changing the color of all that passes through it. The sheen on the lit portion of the courtesan’s sash was created with animal glue, an adhesive made of rendered animal tissue. This scene is meant to recall an episode in which famed poet Ono no Komachi asked one of her suitors to visit her on 100 successive days in order to prove his love."
 },
 {
  "sid": "s03",
  "text": "The Flatiron\nIn an article in 1946, Stieglitz recalled photographing the newly erected Flatiron Building on the day of a great snowstorm. “I suddenly saw the Flat-Iron Building as I had never seen it before. It looked, from where I stood, as if it were moving toward me like the bow of a monster ocean steamer, a picture of the new America which was in the making.”\n\nFor more on the Alfred Stieglitz collection at the Art Institute, along with in-depth object information, please visit the website: The Alfred Stieglitz Collection ."
 },
 {
  "sid": "s04",
  "text": "Hunting Cleaver (Waidpraxe) of Ernst August II Konstantin, Duke of Saxe-Weimar-Eisenach\nThis 18th-century Waidpraxe or chopper belonged to Ernst August II, Duke of Saxe- Weimar-Eisenach. The base of the sheath depicts a hunter who holds a chopper in one hand while presenting a severed boar head to the goddess of the hunt, Diana, with the other.\n\nEtiquette strictly regulated who was allowed to dress the game and present the head or cut the heart. Offenders (men or women) who violated the rules were subjected to the embarrassment of “blading,” whereby the offender was made to bend over the deer carcass and receive three blows on the rear from the flat of the broad-bladed chopper."
 },
 {
  "sid": "s05",
  "text": "Margaret of Austria, Queen of Spain\nMargaret of Austria, wife of King Philip III of Spain, stands resplendently dressed, her royal authority conveyed through the portrait’s formality as well as her sumptuous attire. She is bedecked with jewels: Her brocade skirt is held closed with decorative clasps called puntas; large pearls and gemstones adorn her chest, waist, and arms. The rigidity and painstaking detail of portraits of the Spanish royal family were traditional for paintings that were frequently copied to serve as diplomatic gifts. This painting is a copy of a portrait of the queen by the official court painter Juan Pantoja de la Cruz (Museo del Prado, Madrid)."
 },
 {
  "sid": "s06",
  "text": "Chicago\nShoji Osato began his career as a newspaper photographer in Nebraska before relocating in 1925 to Chicago, where he opened his own studio. Here, he photographed the Art Institute lions on a foggy day, framing them dramatically against the Chicago skyline.\n\nWhen the Chicago World’s Fair opened in 1933, Osato quit photography to operate a tea shop in the newly constructed Japanese garden in Jackson Park, where the Japanese-built Phoenix Pavilion from the 1893 Fair had been relocated. In 1942 the federal government incarcer-ated him as an “enemy alien” for several months; unlike his fellow Japanese Chicagoan Harry K. Shigeta, Osato never returned to photography."
 },
 {
  "sid": "s07",
  "text": "F House\nFrom his earliest experiences as a sign painter, Ed Ruscha developed an abiding interest in the visual and conceptual tensions between text and image. In the late 1980s, he produced a succession of airbrush paintings featuring nocturnal, silhouetted images derived from photographs. F House can be seen as an exploration of the relationship between photography and painting; the block-style letter F that floats on the house may even allude to the f-stop on a camera. The superimposition of the red motif over the house could also imply surveillance by means of a telescopic lens, or perhaps even the scope of a gun. Suggesting intrusive examination and potential harm, the image evokes scenes from Hollywood suspense thrillers and infuses a vision of middle-class prosperity unsettling, perhaps malevolent, overtones."
 },
 {
  "sid": "s08",
  "text": "Fleeing Ghost\nPaul Klee’s artistic skills were diverse: he was a painter, printmaker, critic, and theoretician. He taught at the Bauhaus for most of the famed school’s existence; initially head of the bookbinding department, he also supervised the glass-painting workshop. His greatest influence, however, was as a lecturer for the basic design course on the theory of form in art. In lectures, Klee developed his ideas about the \"polyphony\" of painting, which was based on his interest in simultaneous sensational effects that could be created by various layered formal elements. He believed that this type of creative experimentation could \"issue forth a transformed beholder of art\" and thus pave the way for total abstraction."
 },
 {
  "sid": "s09",
  "text": "Tapper (Iroke Ifa)\nA Yoruba diviner strikes a tapper against his tray to call the deity of fate, Orunmila, to the proceedings. The middle section of this ivory tapper depicts a kneeling hunter who clutches a bow and arrow in his right hand and a large crocodile in his left."
 },
 {
  "sid": "s10",
  "text": "Goldweight Depicting a Man with a Pipe and a Powder Keg\nThe Akan used the lost-wax technique to create brass-cast weights for economic transactions that involved gold. Stylistic studies of goldweights have provided rough dates for the creation of these works. Abstract goldweights are assigned to sometime between 1500 and 1720. Akan artists also created a variety of figurative motifs in executing such miniature brass castings. These forms, which are less common than the abstract weights and are remarkably ornate, appear to have been modeled in the period of hegemony of the Asante kingdom, from 1700 through 1874. Humans and animals appear as solitary forms, but there are also narrative compositions. Regardless of whether the figures are single or part of a larger composition, their intention seems to have been to communicate a message of collective or personal nature.\n\nThis weight in the form of a warrior or hunter with a gun, carrying a keg of gunpowder and smoking a pipe, is a classic didactic figure that can be interpreted variously. The imagery is often said to encapsulate the following proverb: “Even in time of trouble we still need to enjoy the little pleasures of life.” Yet, the work could also be urging prudence in all social action in the same way as another proverb– ogya ne atuduru nna (fire and gunpowder do not sleep together)–suggests that a lack of circumspection can have dangerous consequences. This goldweight graphically conveys the foolishness of smoking so close to a medium as volatile and flammable as gunpowder. But the image, thus interpreted, may glamorize nonchalance, for the capacity to do the unthinkable can become a metaphor of power.\n–Revised from Nii Otokunor Quarcoopome, “Art of the Akan,” African Art at the Art Institute of Chicago, Museum Studies, vol. 23, no. 2 (1997), pp. 135-147."
 },
 {
  "sid": "s11",
  "text": "Lion (One of a Pair, North Pedestal)\nIconic guardians of the Art Institute of Chicago, the Lions have stood at the Michigan Avenue entrance since the building’s inaugural year. The site became the museum’s permanent home at the conclusion of the 1893 World’s Columbian Exposition, where the new structure had hosted lectures and other events for fairgoers. Modeled by Edward Kemeys, an essentially self-taught artist and the nation’s first great animalier (sculptor of animals), the lion pair was unveiled on May 10, 1894. Kemeys focused his talents on sculptural portrayals of North American wildlife, capturing such native creatures in anatomical, naturalistic detail. For the Art Institute, he modeled larger-than-life African lions, the one positioned north of the steps “on the prowl” and the lion to the south “in an attitude of defiance,” (1893.1a) in Kemeys’s words. These behavioral distinctions are visible in the variation of head, tail, and stance. Each weighing in at more than two tons, the Lions were cast in Chicago by the American Bronze Founding Company."
 },
 {
  "sid": "s12",
  "text": "Table\nLightweight and portable, this table could be moved from room to room as needed to hold and display household goods. Yet it could also stand alone as an object to be admired, attesting to the celebration of functional items as art objects that flourished during the Aesthetic Movement of the late 19th century. Its luxurious materials, including rosewood, ebony, and mother-of-pearl, enhance the dynamic hexagonal design with its asymmetrical inlay of iridescent insects crawling across the surface."
 }
]
