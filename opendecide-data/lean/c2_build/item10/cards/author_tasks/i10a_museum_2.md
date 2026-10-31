# Item 10 card authoring i10a_museum_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_museum_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of artworks and objects, written for an art museum's collection website.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: description focus: what the description spends most of its words on (looks, maker, history, use, meaning), where neighbouring answers are easy to confuse.
Card 2 angle: material or technique: how the object was made, where neighbouring answers are easy to confuse.
Card 3 angle: curator task: what job a museum team would give the description (catalogue, label, story, loan file), where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_museum_2",
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
  "text": "Studies of Lions\nDelacroix created these preliminary images for the nearby Lion of the Atlas Mountains (1927.1646) , which would appear in reverse as a result of the printmaking process. Experimenting with several positions for the lion’s prey, and two expressions for the feline itself, this abbreviated sheet suggests several close sessions at the Jardin des Plantes. Ever diligent in his research, Delacroix even sought permission to arrive before the zoo opened to the public, to watch the lions being fed."
 },
 {
  "sid": "s02",
  "text": "Head of a Guillotined Man\nThéodore Géricault painted this macabre image directly from life. The artist is known to have acquired corpses from his local morgue to study anatomy and the effects of decomposition. Surrounding himself with the stench of decay, he produced several paintings of decapitated heads and severed limbs. By depicting this graying and lifeless head upon on a blood-stained cloth laid over a wooden table, Géricault also referenced—perhaps ironically—the long history of still-life painting in Western art. The head probably belonged to a convicted criminal. At that time in France, executions were carried out by the guillotine, a bladed device that sliced through the necks of its victims."
 },
 {
  "sid": "s03",
  "text": "Pensive Bodhisattva\nBefore the historical Buddha reached Enlightenment, he was a young prince named Siddhartha. Here he is represented in that guise, seated on a cushioned throne, wearing rich silks, abundant jewelry, and an elaborate turban decorated with gems and flowers. Although his left arm does not survive, his pose is that of a pensive bodhisattva, so his right hand would have been raised to point at his head to indicate deep thought. This thinking pose encouraged elite viewers to likewise consider their spiritual state and make efforts to move forward on the path toward Enlightenment."
 },
 {
  "sid": "s04",
  "text": "Dunes\nBrod studied in Prague and later at the competitive Kunstgewerbeschule (Arts and Crafts School) in Vienna before moving to Chicago in 1924. In addition to being a printmaker, Brod was an accomplished textile designer who often incorporated decorative and abstract elements into her art. This watercolor of dunes and foliage near Ox-Bow highlights the verdant scenery of the Michigan retreat and serves as a testament to its attraction to artists."
 },
 {
  "sid": "s05",
  "text": "Snuff Container\nThis snuff container made of cattle horn was worn by a high-ranking man as a pendant. Its material, shape, and use connect it to the spirit world. Cattle have been a primary source of wealth throughout southern Africa, playing a critical role in communications between the living and the dead. Tobacco was part of wedding gifts and also offered to the ancestors."
 },
 {
  "sid": "s06",
  "text": "Blanket\nBrillant color and bold overall patterns with serrated diamonds, chevrons, and interlocking lines are hallmarks of the \"Eye Dazzler\" style of Navajo (Diné) textiles produced from the late-19th to the early-20th century. Earlier Navajo blankets featured broad horizontal bands of indigo blue, white, dark brown, black, and red, subsequently enhanced with the addition of small diamonds, bars, and squares. The lively approach of Eye Dazzler weaving developed out of a period of major cultural and artistic transformation beginning in 1864 when the U.S. government forcefully resettled the Navajo in the Bosque Redondo reservation. From the early 1860s, the Navajo received brightly colored commercial yarns as part of their U.S. government annuities. The new Eye Dazzler weaving also incorporated design elements characteristic of Mexican Saltillo blankets, which featured serrated diamonds and zigzag lines.\nThe creator of this blanket fully utilized the intense color of commercially dyed yarns and the Saltillo style to create a spectacular work. Internlocking serrated undulating lines appear to vibrate over the entire surface. The vivid interplay of red and orange hues with brillant blues, greens, yellow, white, and black produces an energetic, three-dimensional illusion.\nGallery lable, December 2012"
 },
 {
  "sid": "s07",
  "text": "Sonambulo II (Blue)\nIñigo Manglano-Ovalle first gained international recognition for a diverse body of work––consisting of both studio-based objects and activist-inspired public art—that blended contemporary urban culture with poetic meditations on aesthetics, nature, and beauty. Sonambulo II (Blue) speaks precisely to the crucial intersection between his earlier street-based endeavors and his later, more gallery-bound practice. Importantly, it exists as both an individual work of sound art and a site-specific installation commissioned by the Art Institute.\nConsisting mainly of the soothing sounds of a summer thunder- and rainstorm, the audio portion mimics a New Age relaxation tape or therapeutic sleep aid. The origins of the work, however, are quite different: the audio was composed from the sound of a single gunshot that the artist sampled and digitally remastered using state-of-the-art computer editing equipment. The sound loop begins with the explosion of the gunshot, which is followed by eight seconds of tense silence. The gunshot sound is then repeated 385,000 times and seamlessly blended with the beginnings of the simulated thunder. The rainstorm effect follows, and the piece automatically repeats.\nThe conceptual roots of the work can be found in Manglano-Ovalle’s biography. An insomniac, he decided to construct his own relaxation tape directly from the very street noises that were contributing to his sleeplessness. Placing a microphone outside his bedroom window on Chicago’s Northwest Side, he captured the sound of gunfire in a single night. In a poignant act of creative transformation, the artist constructed an escape based in reality, turning the potentially frightening sounds of violence into a soothing means of respite. Sound itself, however, is also a major focus of his thinking: “I don’t use sound in a linear, time-based way. To me sound is very much an extension of sculpture. It has physical form to me. It drives and also occupies space.”\nSonambulo II (Blue) is much more than a personal lullaby: Manglano-Ovalle’s strikingly inventive manipulations contain a compelling social critique. The references to sleep introduce the metaphor of unconsciousness and consciousness. Extending these into the arena of pressing political issues such as gun violence, the work points to the basic differences between awareness and ignorance, social action and neglect. The piece masks the sounds of gunfire with the effect of a natural phenomenon; in doing so, it suggests the ways in which violence and fear too often become the ambient backdrop of contemporary urban life."
 },
 {
  "sid": "s08",
  "text": "Putto\nLike his contemporaries, German sculptor Hans Peiser typically carved figures such as this one in wood to prepare for larger, finished works in bronze. During the Renaissance, artists revived the ancient Roman motif of small male nudes, called putti , which symbolized gaiety, youth, and innocence. Peiser incorporated these frolicking figures into the city fountains he designed in the 1550s. This example closely resembles the statue of a triumphant putto that crowns the fountain in front of Nuremberg’s city hall."
 },
 {
  "sid": "s09",
  "text": "Allegory of Envy\nFlanked by younger couples entwined in erotic poses, an unaccompanied older woman appears to scowl. It is unclear whether the central figure, traditionally identified with envy, is the one experiencing the feeling or merely a visual symbol of it. Secular allegorical subjects were popular with Renaissance printmakers, especially in Italy. In this case, the Florentine engraver Cristofano Robetta copied German prints by Albrecht Dürer for the landscape in the background."
 },
 {
  "sid": "s10",
  "text": "A Stand of Elm Trees (recto); A Study of East Bergholt with the Church (verso)\nIn a time when landscape painting enjoyed unprecedented popularity in England, John Constable secured a place as a leading artist in the genre. This exploratory sketch by Constable is one of his earliest and largest studies of trees and was probably drawn in Dedham Vale, the area of rolling hills and woods surrounding his home on the border of Essex and Suffolk. Hallmarks of Constable’s technique can be observed here, especially the indistinct description of foliage contrasted with sharply delineated trunks and branches. When viewing one of Constable’s studies of trees, William Blake stated, “Why, this is no drawing, but inspiration.”"
 },
 {
  "sid": "s11",
  "text": "Soldier\nLuc Tuymans’s quiet, elegiac paintings, copied from old photographs or newspaper illustrations, draw upon the act of remembrance and the function of collective memory. Describing his process, Tuymans explained, \"I usually finish [a painting] in a single day, partly in order not to lose my concentration and partly in order to have the chance not to come too close to the image I am using as my model.\" Often his canvases refer to his experience growing up in Belgium, a country ravaged by war and haunted by its history of colonial oppression in Africa and Asia. Based on a photograph of a World War I soldier, this work is a haunting, strangely ambiguous partial portrait that suggests that the history of war is more forgotten than remembered."
 },
 {
  "sid": "s12",
  "text": "Portrait of a Man\nDutch-born painter Corneille de Lyon employed a limited selection of colors to great effect in this small painting. The textured, green background accentuates the subject’s velvety black outfit, lace collar, pale skin, and bristly beard. Corneille specialized in this stylized type of small, finely painted precious portraiture, working primarily for the court and bourgeois elite of 16th-century Lyon, France, where he lived most of his life. The sitter’s exaggerated proportions direct the viewer’s attention to his head and thus to his quiet yet self-assured expression. His confident posture and expensive clothes, along with the exceptional reputation of his portraitist, speak to his high social status."
 }
]
