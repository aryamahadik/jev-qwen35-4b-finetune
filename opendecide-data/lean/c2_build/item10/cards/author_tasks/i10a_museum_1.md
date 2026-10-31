# Item 10 card authoring i10a_museum_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_museum_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of artworks and objects, written for an art museum's collection website.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: kind of object: what sort of object the description is about, where neighbouring answers are easy to confuse.
Card 2 angle: subject shown: what the object shows or represents, where neighbouring answers are easy to confuse.
Card 3 angle: visitor use: what a visitor would use the description for, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_museum_1",
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
  "text": "The Constellation of States\nOne of the earliest posters by Medu, this broadside caricatures P. W. Botha as a grotesque octopus. Botha was South Africa’s prime minister from 1978 to 1984 and its president from 1984 to 1989. In 1979 he attempted to forge economic and military ties with other southern African countries, a plan called the Constellation of Southern African States. This strategic offensive aimed to create a favorable external environment for the growth of the apartheid state, shielding it from internal insurgency and international condemnation. The poster exposes the neocolonial and imperial motivations of Botha’s project, which was flatly rejected by leaders across the region."
 },
 {
  "sid": "s02",
  "text": "Moulin Rouge, La Goulue\nMoulin Rouge , La Goulue was Toulouse-Lautrec’s first commissioned poster, created to advertise the performance of dancer La Goulue and acrobat Valentin le Desossé at the iconic Montmartre dance hall. With thousands of copies pasted around Paris, the poster was an instant success, propelling Toulouse-Lautrec into the artistic limelight and attracting numerous commissions from other performers and cabaret owners. In this image, Toulouse-Lautreccaptured the exhilarating experience of being onstage, but he also designed a composition that traps La Goulue in her spectacle: between the bright yellow stage lights, the anonymous silhouetted crowd, and the provocatively posed Valentin."
 },
 {
  "sid": "s03",
  "text": "The daring of Martincho in the ring at Saragossa, plate 18 from The Art of Bullfighting\nFrancisco de Goya was an enthusiastic bullfighting aficionado and even claimed to have been a torero (bullfighter) in his younger years. Yet it is unlikely that he meant this print series to be seen only as a fan’s outline of the history of bullfighting in Spain. In the early 19th century, when Goya published these prints, bullfighting was a politically charged activity. It was seen either as bread and circus (or pan y toros [bread and bulls], as a reformist tract put it), meant to keep the populace distracted, or as an expression of Spanish nationalism—a spectacle imbued with patriotic fervor."
 },
 {
  "sid": "s04",
  "text": "Lilies (Corey Memorial Window)\nThis memorial window, dedicated to Francis Edwin Corey and his wife, Vernera Leonard Corey, is one of several that Louis Comfort Tiffany’s Tiffany Glass and Decorating Company designed for Christ Reformed Episcopal Church in Chicago. Tiffany used lilies in his stained glass a number of times; the Coreys may have been inspired to commission this design by the well-publicized Field of Lilies Window in Tiffany’s chapel at the 1893 World’s Columbian Exposition in Chicago. Lilies were also considered appropriate for commemorative works, since they symbolized resurrection. When Christ Reformed Episcopal Church was demolished in 1962, the Tiffany windows were moved to St. Andrew Reformed Episcopal Church in Tinley Park, Illinois. The two parts of the Corey Memorial Window are now displayed on either side of this wall."
 },
 {
  "sid": "s05",
  "text": "View on the River Roseau, Dominica\nIn this expansive view of Dominica, people along the riverbank bathe, wash linens, converse, and sell produce. The presence of indigenous Carib, African, Afro-Creole, European, and mixed-race individuals attests to the long history of white-settler colonialism in the West Indies, where valuable crops such as coffee and sugar were cultivated through the labor of enslaved people.\n\nThe Italian-born artist Agostino Brunias settled on the island, painting scenes of Caribbean life for his planter-class patrons as well as white audiences abroad. Eliding the brutal conditions of slavery, his compositions shaped a reassuring vision of British imperialism for those in power. Yet by centering enslaved and free people of color—and focusing on mixed-race interactions—he also foregrounded the human impact of colonialism."
 },
 {
  "sid": "s06",
  "text": "In Lovely Blueness No. 2\nIn the mid 1950s, Sam Francis inaugurated a succession of monumentally scaled paintings informed by a variety of artistic sources, including Abstract Expressionism and French Impressionism. With their spontaneous brushwork and lyrical interplay of primary hues, these paintings established Francis as one of the foremost colorists of the postwar era. The artist often found inspiration in literary works and kept a notebook containing titles of books and verses. He named this and a related painting ( In Lovely Blueness No. 1 , 1955–57) after a poem by the German Romantic writer Friedrich Hölderlin, hoping to capture the poem’s sublime imagery and prophetic vision."
 },
 {
  "sid": "s07",
  "text": "Bust of Anne-Marie-Louise Thomas de Domangeville de Sérilly, Comtesse de Pange\nJean-Antoine Houdon was one of the greatest sculptors of the 18th century, and he had a particular talent for portrait busts. Commissioned in 1780, one year after her first marriage, this bust of Louise de Domangeville presents the sitter as somewhat older than her 18 years. Houdon’s handling of the sculpture strikes a balance between the conversational intimacy of Rococo portraiture and the simplified dignity of Neoclassicism. The turn of the sitter’s head and the precisely cut pupils of her eyes focus her gaze, and Houdon conveyed skin, hair, and fabric through nuances of texture and polish. Her drapery frames the bust and imparts the illusion of Classical repose."
 },
 {
  "sid": "s08",
  "text": "Reading\nMany artists viewed lithography as a tool that would allow them to reproduce paintings and spread their fame. In contrast, Pierre-Paul Prud’hon was an artist who created prints as unique works of art. Working in the period following the French Revolution, his embrace of sensual and classical allegorical figures was initially at odds with the prevailing patriotic and military mood in France. However, the escapist quality of his prints soon gained popularity and fame."
 },
 {
  "sid": "s09",
  "text": "Portrait of Pablo Picasso\nIn 1906 Juan Gris traveled to Paris, where he met Pablo Picasso and Georges Braque and participated in the development of Cubism. Just six years later, Gris too was known as a Cubist and identified by at least one critic as \"Picasso’s disciple.\" Gris’s style draws upon Analytic Cubism—with its deconstruction and simultaneous viewpoint of objects—but is distinguished by a more systematic geometry and crystalline structure. Here he fractured his sitter’s head, neck, and torso into various planes and simple, geometric shapes but organized them within a regulated, compositional structure of diagonals. The artist further ordered the composition of this portrait by limiting his palette to cool blue, brown, and gray tones that, in juxtaposition, appear luminous and produce a gentle undulating rhythm across the surface of the painting.\nGris depicted Picasso as a painter, palette in hand. The inscription, \"Hommage à Pablo Picasso,\" at the bottom right of the painting demonstrates Gris’s respect for Picasso as a leader of the artistic circles of Paris and as an innovator of Cubism. At the same time, the inscription helped Gris solidify his own place within the Paris art world when he exhibited the portrait at the Salon des Indépendants in the spring of 1912."
 },
 {
  "sid": "s10",
  "text": "Inner View\nIn late 1965, after a two-year break from a productive experience at Tamarind, Nevelson returned to making prints at Irwin Hollander's invitation. Hollander, one of the first printers to receive training at Tamarind, established his own workshop in New York in 1964, the first such establishment in the eastern United States to grow out of the Tamarind operation.\n\nOf the fourteen new editions of prints Nevelson produced, only two were lithographs. Innerview , with its collaged element, shows her growing sophistication with printed components. Close inspection reveals that the collaged part is a section of the underlying drawing, printed on a different color of paper, cut out and laid down. Both the method and materiality of this print recall the assemblage technique of Nevelson's sculpture."
 },
 {
  "sid": "s11",
  "text": "Renganeschi's Saturday Night\nJohn Sloan often explored the leisure activities of working-class women and the changing social mores of the 20th century. Here he focused on three women who sit together at the central table of a popular Italian restaurant in New York City. By showing the women celebrating a night out on the town, the artist emphasized their newfound freedom to socialize in public spaces without the need for male escorts. Although he indicated their working-class status through their “unladylike” gestures—legs wrapped around their chairs and pinkies flared in the air—Sloan did not cast judgment on the women’s relaxed behavior. His informal style and loose brushwork enliven this scene of urban leisure with a sense of immediacy and action."
 },
 {
  "sid": "s12",
  "text": "Untitled (Harlequin)\nCornell’s early transition from collage into three-dimensional assemblage and his experiments with the possibilities of movement were often, as here, accompanied by a theatrical element. “Shadow Boxes,” as Cornell called some of his constructions of this period, were among the categories of objects named on the cover of the announcement for Cornell’s Exhibition of Objects at Julien Levy’s in December of 1940. Among the scattered illustrations on this cover is an image of Jean Antoine Watteau’s Gilles (c . 1718, Paris Musée du Louvre; Humphrey Wine. Watteau , London, 1992, pp.56–57, ill.), cut up and arranged to look like an articulated marionette, in a manner similar to the marionette in this box.\n\nToy shadow-box theaters were popular in the United States in the latter part of the nineteenth century and were a simpler version of the miniature toy theaters that were especially popular in Europe. As Lynda Hartigan explained,\n\n\"sold in sets or as separate sheets of hand-colored prints of characters, scenery, and the stage itself, miniature theaters were marketed as educational toys and pastimes to be cut out and assembled at home. The shadow-box toy was less complicated than the miniature theater in structure and frequently included [as in this box by Cornell] single figures of performers and animals that could be manipulated to create a sense of action\" (Lynda Roscoe Hartigan, in Washington, D. C. 1982–83, p. 29).\n\nHalfway between a box and a collage, this work similarly combines elements of a game and of a stage. The pattern of the colored wrapping paper covering the outside of the box and visible along the edges of the glass front is reminiscent of Roman and Italian Renaissance mosaic floors. It creates an optical illusion of cubes that read either as convex or concave and also resembles the diamond-patterned costume of Harlequin from the commedia dell ‘arte.\n\nThe inside walls of the box are covered with colored paper of a more muted, leafy pattern. A mat board, at the center of which has been cut a large opening, is placed directly behind the glass to create the effect of a stage, its edges decorated with paper cutouts of rococo swirls and acanthus leaf patterns appropriate to the romantic theater. The articulated marionette inside the box is suspended from a string extending out of a tiny hole in the top of the box."
 }
]
