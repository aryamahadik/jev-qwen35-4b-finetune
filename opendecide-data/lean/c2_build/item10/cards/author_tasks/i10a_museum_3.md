# Item 10 card authoring i10a_museum_3

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_museum_3.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of artworks and objects, written for an art museum's collection website.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: subject shown: what the object shows or represents, where neighbouring answers are easy to confuse.
Card 2 angle: visitor use: what a visitor would use the description for, where neighbouring answers are easy to confuse.
Card 3 angle: kind of object: what sort of object the description is about, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_museum_3",
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
  "text": "Truth has died, plate 79 from The Disasters of War\nThough not the last plate of the series, this print finalizes its central themes in a profound manner, claiming that truth itself is dead. Here, personified by a shining corpse about to be buried, truth connotes constitutional liberty. Justice is featured at the right, clasping her scales in her left hand. She covers her face, perhaps weeping, as if she cannot bear the scene before her. By ending the series on this note of despair, Francisco de Goya brought an answer to the question of what must come to pass ( plate one )—the final blow of war is that truth is dead and justice despondent."
 },
 {
  "sid": "s02",
  "text": "Pictograph\nIn 1941 Adolph Gottlieb began a series of paintings, prints, and drawings that he called Pictographs . These represent the artist’s first efforts at reconciling elements of abstraction with an exploration of the unconscious drawn from Surrealism. His aim was to create a new, uniquely American expression that would bring significant content to abstraction. The ideas Gottlieb explored in his Pictographs were so varied and complex that the series occupied him for more than 10 years. This print was created in the course of Gottlieb’s intensive exploration of the theme."
 },
 {
  "sid": "s03",
  "text": "9 Objects\nGerhard Richter's continued interest in subtly pointing out the artifice and subjectivity of photographic images is clearly communicated in this print made to resemble a photographic reproduction. This image, one of a suite of nine, depicts a geometric structure fabricated out of recognizable materials. The lithograph's photographic quality, the constructed nature of the object, and its placement in defined spaces amidst familiar surroundings imbue the representation with a deceptive truthfulness. However, given the implausibility of the object's shapes, the illusory reality it conveys creates a trompe-l'oeil, or trick of the eye, effect."
 },
 {
  "sid": "s04",
  "text": "Mouth (for L'Oréal), New York\nWorking for almost 70 years, Irving Penn produced groundbreaking images that blurred the boundaries between advertising and art. By the early 1950s, he had established a successful career as an editorial photographer at Vogue magazine and began taking on freelance advertising assignments, creating innovative photographs that stood out for their striking simplicity and unexpected details. This advertising image for L’Oréal cosmetics likens a model’s lips to a painter’s palette—offering an enticing twist on conventional representations of beauty."
 },
 {
  "sid": "s05",
  "text": "A Game in Hell: A Poem (Igra v adu: Poema)\nBooks by progressive Russian artists and poets, made between the revolutions of 1905 and 1917, aimed to overthrow conventions of art and society simultaneously. Their makers believed that art and language needed to become immediate and real—part of everyday life—and as a result these Futurist books were willfully made with cheap materials, and appeared purposely unrefined, as if they were products of wild and primitive behavior."
 },
 {
  "sid": "s06",
  "text": "Peter Berg Silver Designs Collection\nBorn in Drammen, Norway, Peter Berg trained as a metalsmith in Norway before immigrating to Chicago around 1900. By 1909 he was working as a silversmith in the noted Kalo Shop in Chicago, where he designed and executed flatware and tableware in an Arts and Crafts style. This collection includes four graphite drawings for various items of silver tableware and one template for a silver tray. These designs are believed to have been created for Kalo Shop production.\n\nView finding aid.\nView entirely digitized collection.\n\nCollection access:\nCollections may be accessed in the Franke Reading Room of the Research Center at The Art Institute of Chicago, by appointment only. For further information, consult the FAQ .\n\nFinding aids by subject\nBrowse all finding aids\nBrowse images and media\nOral histories\n\nContact the Ryerson and Burnham Art and Architecture Archives:"
 },
 {
  "sid": "s07",
  "text": "Bamboo-Covered Stream in Spring Rain\nThis fifty-foot composition reveals a “slit-view” perspective of bamboo growing along a stream. In single brushstrokes of varied tonality, leaves and stalks are depicted close up, cut off at top and bottom. Xia Chang executed this painting with great breadth and boldness as a gift for a friend who had planted a bamboo grove around his retirement villa.\n\nAs it bends without breaking, bamboo evoked human values of resiliency and endurance for intellectual painters of premodern China. Xia’s dedicatory inscription on this scroll, describing the bamboo garden as “washing away ordinary thought,” expresses their desire for retreat from the trials of official life. He had served the government in roles of calligrapher, draftsman, and administrative secretary before retiring for a decade in 1439, initially to care for his aged mother. This painting exhibits his style of angular rocks, ink-washed shoreline, and fluent brushwork that matured during that period."
 },
 {
  "sid": "s08",
  "text": "Living Sculpture\nIn the late 1960s the term Arte Povera was coined to describe the radical style of a group of Italian artists who began to engage everyday materials. Marisa Merz was included in the important Arte Povera + Azioni Povere exhibition in 1968 as one of the movement’s leading practitioners. She spent the majority of her career, however, retreating from the public sphere, creating works in intimate settings such as her home. Merz has in fact stated, “There has never been any division between my life and my work.” This three-part work belongs to the larger series Untitled (Living Sculptures) , begun in 1965. These extraordinary objects, crafted from thin folds of pliant, layered sheet metal, were made to hang from the ceiling of her Turin apartment. Her living and working spaces became, to varying degrees, a forest, a hive, a cave, and a womb. Merz’s process turned simple industrial materials into fluid, organic forms. Removed from any social or narrative context, her abstract, formal inventions operate within their own temporal logic, reflecting the artist’s belief in the enduring effect of each artwork beyond its material realization and the constraints of time and place."
 },
 {
  "sid": "s09",
  "text": "Untitled\nFour doll arms emerge from a ravine of plastic flora, each manicured hand holding a bottle filled with amber liquid. A white label in the foreground reads “Dana TABU,” referring to the women’s fragrance created by the Spanish company House of Dana. After the company relocated to the United States in 1940, Yuichi “Eugene” Idaka and Ryuichi Sugasawara (who anglicized his name to Riley O’Suga) were commissioned to make this photograph, which they signed jointly as “Idak–O’Suga.” While teaching at the New Bauhaus in Chicago (later the Institute of Design), Idaka opened a commercial studio with O’Suga, where they created advertisements that reflected the school’s experimental approach to photography."
 },
 {
  "sid": "s10",
  "text": "Collar\nFrom the early years of her career, Livingstone has demonstrated a strong interest in the human body. She began making sculptural work in felt that consciously referred to the body in 1990. Felt seemed a perfect metaphor for skin, resembling hide while acting as a membrane. Initially abstract and sensual, by 1994 the bodily references were more overt and organ-like, with wrinkled areas, projecting tubes, and bloody coloring. Throat, Collar, and Vent, conceived as a set, are powerful works that present the viewer with an uncomfortable paradox: from a distance they represent something normally hidden and repugnant, while close up they are actually quite beautiful in color and surface treatment."
 },
 {
  "sid": "s11",
  "text": "Pair of Braziers with Eared Cups\nEared cups with warming stands were probably used to heat sauces for meat. Each side of these warming stands is cast with one of the Animals of the Four Directions (si shen)—the Green Dragon of the East, the White Tiger of the West, the Black Warrior (tortoise and snake) of the North, and the Red Bird of the South. In Han art, the pervasive appearance of these symbolic animals reflects a desire to center the owner within the favorable influences of the universe."
 },
 {
  "sid": "s12",
  "text": "Herbert and Katherine Jacobs Residence and Frank Lloyd Wright Records\nFrank Lloyd Wright designed three houses for the Jacobses, two of which were built. The first house, known as Usonia #1, was built in 1937 in Madison, Wisconsin; the second house, the \"Solar Hemicycle,\" was built in 1948 in Middleton, Wisconsin. This collection documents the construction of these houses through correspondence, annotations, newspaper articles, photographs, periodical literature, and drawings. The collection is augmented by photographs of other buildings designed by Frank Lloyd Wright, newspaper articles about Wright's architecture and life, brochures on Taliesin projects and Wright memorabilia: announcements, programs, candid photographs, and Taliesin publications. The collection comprehensively records the design development and construction of Wright's first Usonian residence, an important summation of Wright's theories on the use of materials and space.\n\nView finding aid.\nView selected images from this collection.\nFind all Frank Lloyd Wright digital images.\n\nCollection access:\nCollections may be accessed in the Franke Reading Room of the Research Center at The Art Institute of Chicago, by appointment only. For further information, consult the FAQ .\n\nFinding aids by subject\nBrowse all finding aids\nBrowse images and media\nOral histories\n\nContact the Ryerson and Burnham Art and Architecture Archives:"
 }
]
