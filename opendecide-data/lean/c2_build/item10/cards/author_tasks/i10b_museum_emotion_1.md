# Item 10 card authoring i10b_museum_emotion_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10b_museum_emotion_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of artworks and objects, written for an art museum's collection website.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: feeling and tone. Invent your own 5 to 8 feeling or mood labels that suit this kind of text. Spell out the dividing line between similar feelings by what the text says or does. The last option must be a catch-all for texts with no clear feeling. Do not use any ready-made emotion list (not the usual handful of basic emotions, not a positive / negative / neutral scale, not a list of dozens of emotions).
Card 1 angle: writer's feeling: the feeling the writer shows or describes.
Card 2 angle: reader's feeling: the feeling a typical reader would most likely have after reading the text.
Card 3 angle: overall mood: the mood or tone the text gives off as a whole, apart from any one sentence.
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

{"task_id": "i10b_museum_emotion_1",
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
  "text": "Untitled\nA principal author of 1980s “appropriation art,” Richard Prince had worked early on in the tear-sheet department of Time Life, building a personal archive of advertising remnants. Then, in 1984, he began to draw wholesale copies of quintessential one-liner cartoons published in the New Yorker magazine—soon separating the images from their captions and assigning them new ones. In his White Paintings series, Prince explored a still more complex jumbling of image and text, combining numerous disjointed jokes, lines borrowed from songs and ads, and graphic cartoon outtakes. On the one hand, Prince was turning the medium of painting, almost literally, into a joke. On the other hand, a work like Untitled —which marks Prince’s transition into the White Paintings—is surprisingly haunting, rich with detail but also ghostly, as if about to dissolve."
 },
 {
  "sid": "s02",
  "text": "Hikers climbing up to a Mountain Chalet\nWhen Rousseau was a toll operator for one of Paris’s city gates, he made the decision to become an artist. With no academic training, he started copying works at the Musée du Louvre in 1884 and two years later exhibited his works with the Neo-Impressionists at the Salon des Indépendants. In this drawing Rousseau’s lack of formal training is evident in the flattened forms and odd spatial relations of the landscape. These idiosyncrasies would inspire artists such as Vasily Kandinsky and Pablo Picasso."
 },
 {
  "sid": "s03",
  "text": "Neo-Huaco #3 from the series ¿Y qué hacemos con nuestra historia? (So What Do We Do with Our History?)\nIn Peru, ancient ceramics are often called huacos , derived from the Quechua word huaca , which the Incas used for sacred objects and places. In turn, pot-hunters or looters are often called huaqueros . While these activities are now illegal, for much of the 20th century pot-hunting was a critical source of livelihood, especially in poorer areas.\n\nAna De Orbegoso’s “new huaco ” recalls this complicated past in asking how Peruvians should now relate to their history. Its mirrored surface allows Peruvian viewers to gaze upon this modern “portrait vessel” and see their own reflection, offering an embodied connection to their ancestors. She has transformed the traditional ceramic into a gleaming metallic surface, calling to mind the lust for gold and silver that fueled Spanish colonialism. This material also alludes to the commodification of Andean antiquities and the contemporary art market. As the artist has stated, “That’s how culture transcends, transforming the past while keeping the roots.”"
 },
 {
  "sid": "s04",
  "text": "Untitled (Hôtel de la Duchesse-Anne)\nThis box has formal similarities to Yellow Chamber in its use of white panels and in its balance between asymmetry and regularity. It also includes similar components: the bird, the metal springs, the ring, and the metal rod. But the idea of travel is more strongly evoked here, not least through the contrast between the white interior of the box and the tiny, brilliantly colored stamps, which are colorful and exotic in both a metaphoric and literal sense. The contrast between their small scale and the expanse of whiteness also suggests geographic distance. The idea of the box as a surrogate for travel is indeed very present here. Some of the openings in the white lattice at the right contain bingo chips, which conjure ocean voyages where deck games and gambling played a large part in the entertainment provided on board. Other lattice openings contain wood blocks with constellations on a blue background, which similarly recall navigation. The parrot contributes to the exotic atmosphere and introduces an element of tension, as it suggests both the freedom of travel and a bird caged or trapped. A coiled spring curls over the bird’s head to form a target like shape, while the bird itself seems to eye the butterfly and beetles on the stamps as if they might become its lunch.\n\nThe names of two hotels are included in this box: the Hotel des Voyageurs in Brest, a port in Brittany, and the Hotel dc la Duchesse-Anne in Nantes. The latter may have appealed to Cornell because of its association with the Surrealists: Andre Breton had spent part of World War I in Nantes, where he met Jacques Vache, whose anarchic humor had a strong influence on him. The name Anne also recalls one of Cornell’s favorite heroines, Thomas De Quincey’s Ann (see Ann—in Memory ).\n\n— Entry, Dawn Ades, Surrealist Art: The Lindy and Edwin Bergman Collection at the Art Institute of Chicago , 1997, p. 85."
 },
 {
  "sid": "s05",
  "text": "The Place du Havre, Paris\nAfter a period of experimentation with the Neo-Impressionist style developed by Georges Seurat , Camille Pissarro returned to the loose, multidirectional brushstrokes that he had used in his earlier Impressionist works. He also revisited an Impressionist subject that his colleagues had all but abandoned by the 1890s—the modern city. This bustling scene, alive with the noise and movement of traffic and pedestrians, was the view from his window at the Hôtel Garnier in Paris, where he stayed for a few weeks early in 1893. The building at the left edge of the canvas is the Gare Saint-Lazare."
 },
 {
  "sid": "s06",
  "text": "couch and fern, GLITTER AND THE LION’S MANE\nIn this installation, an upturned sofa displays a video shot from a moving car and accompanied by audio of Sondra Perry and psychotherapist Bola Shonubi talking. The two discuss the artist’s grandmother’s life in the Jim Crow South and Perry’s search for the land where her grandmother was a sharecropper. Throughout their conversation, they explore themes of aging, mortality, and Black generational trauma. The inclusion of a barbershop chair overgrown with lion’s mane mushrooms, which are thought to improve cogni-tion and combat aging, serves as a healing agent for the continued impact of the past on the present. Of the work’s many dates, 2020, 2021, 2022, and 2023 indicate the years that different iterations of couch and fern, GLITTER AND THE LION’S MANE were installed before it arrived at this final form, and 1.8 Ga, or 1.8 billion years, corresponds with the age of a prehistoric fern species."
 },
 {
  "sid": "s07",
  "text": "Philip IV Appointing Prince Ferdinand Governor of the Netherlands, plate 25 from Casperius Gevartius, Pompa Introitus Honori Serenissimi Principis Ferdinandi (Triumphal Entry of the Most Serene and Honorable Cardinal-Infante Ferdinand)\nOn the occasion of Cardinal-Infante Ferdinand’s triumphal entry into Antwerp in 1635, Peter Paul Rubens designed temporary arches and stages to decorate his procession route through the city. Triumphal processions of this kind were common forms of political theater, enacted to consolidate the power of a regent or monarch. The stage in memory of Isabella Clara Eugenia (2015.11) served to reinforce the dynastic transfer of authority from Ferdinand’s predecessor, who had governed the southern Netherlands from 1598 until the time of her death in 1633. The central image of the stage in her honor, enlarged in the accompanying print (2015.12), shows Ferdinand’s appointment by Philip IV, while the flanking columns represent effects of good government—public health and public safety."
 },
 {
  "sid": "s08",
  "text": "Dagger with Tiger-Head Pommel\nThis dagger has a plain, double-edged steel blade and an exquisitely decorated hilt. The cross guard is inlaid with quartz gemstones and displays the heads of two blue, tusked elephants. A cerise-colored enameled handle separates the cross guard from the golden tiger’s head pommel, which is adorned with additional jewels arranged in floral and foliate patterns. The process for creating this haft, known as kundan , entails using soft gold for setting and polychrome enameling. Richly embellished daggers like this one would have been worn tucked into the waist sash of a prominent individual."
 },
 {
  "sid": "s09",
  "text": "Sharecropper\nElizabeth Catlett created this linocut in Mexico, where she moved in 1946 to work at the Taller de Gráfica Popular (People’s Graphic Arts Workshop). She was influenced by the spirit of activism at the workshop, which inspired her to produce art that could be used in the fight for equality and justice for African Americans. Sharecropper , like many of her other works, shows Catlett’s determination to showcase the lives of black women in the South, here drawing attention to the inequitable system of tenant farming that often resulted in a ceaseless cycle of increasing debt.\n\nThis impression was printed from the original linoleum block in 1970, many years after Catlett first produced the image and, in it, Catlett added color whereas the earlier printings were black and white. Once a block is cut, an artist can reprint it as long as they find the image it produces acceptable. In Sharecropper , the monumentalized the figure and is depicted with humanity and strength."
 },
 {
  "sid": "s10",
  "text": "Albrecht Dürer\nHere Wenceslaus Hollar reproduced an Albrecht Dürer self-portrait painting (now in the Prado, Madrid) as an etching in reverse. In 1498, at the age of 26, Dürer depicted himself as a gentleman artist at the height of his creative prowess. On a diplomatic trip through Dürer’s hometown of Nuremberg in 1636, the Earl of Arundel received the painting as a gift for King Charles I of England. Hollar made the etching from the original for Arundel, who was his major patron."
 },
 {
  "sid": "s11",
  "text": "Green Mountains, Canada\nIn this panoramic landscape, Georgia O’Keeffe captured the massive Gaspé Peninsula mountains in Quebec, Canada, as they rise sharply from the water’s edge. O’Keeffe traveled to the region in the summer of 1932, accompanied by fellow artist (and husband Alfred Stieglitz’s niece) Georgia Engelhard. The old barns and crosses built by the Peninsula’s French settlers fascinated O’Keeffe, as did the lush green terrain. She painted the mountains and sun-streaked sky with texture and depth, while the water in the foreground moves in flat, zig-zag swaths that accentuate color over representational depth. Although she enjoyed her trip to Canada, and returned again that year, ultimately O’Keeffe preferred the New Mexican landscape, specifically its brilliant sunshine."
 },
 {
  "sid": "s12",
  "text": "Watering Place at Marly\nIn 1875 Alfred Sisley moved to the village of Marly-le-Roi, where in the 1600s King Louis XIV had built an elegant country retreat. The artist’s home on the rue de l’Abreuvoir flanked the pool, or “watering place,” featured on the left of this canvas. The pool was all that remained of the water gardens that had been part of the king’s park.\n\nSisley remained faithful to landscape subjects throughout his career, spending most of his life painting in the villages along the Seine River, in the region referred to as the cradle of Impressionism."
 }
]
