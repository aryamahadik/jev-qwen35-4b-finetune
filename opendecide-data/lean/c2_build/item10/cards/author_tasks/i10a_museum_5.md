# Item 10 card authoring i10a_museum_5

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_museum_5.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of artworks and objects, written for an art museum's collection website.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: visitor use: what a visitor would use the description for, where neighbouring answers are easy to confuse.
Card 2 angle: kind of object: what sort of object the description is about, where neighbouring answers are easy to confuse.
Card 3 angle: subject shown: what the object shows or represents, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_museum_5",
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
  "text": "Untitled\nUntitled is essentially a three-dimensional line drawing: A wire composed of 22 segments extends to an immense height, with the remainder coiled stiffly in a spiral on the floor. Eva Hesse described the sculpture as “endless and yet a thin longish substance that is linked together and one feels the infinity to which it could extend.”\n\nIn the late 1960s, Hesse began to explore the expressive, organic possibilities of abstraction. Using latex and reinforced fiberglass, she created peculiar forms that examined the fundamental properties of sculpture."
 },
 {
  "sid": "s02",
  "text": "Insertions into Ideological Circuits: Coca-Cola Project\nCildo Meireles’s ongoing Coca-Cola Project , part of his larger Insertions into Ideological Circuits series, interrogates how power—socioeconomic and political—is distributed through networks of trade and consumerism. Meireles noted his intention on each bottle: “To register informations and critical opinions on bottles and return them to circulation.” Each bottle also carries a distinct political provocation. These three read, “Yankees go home!,” “Jesse Helms No!,” and “Which is the place of a work of art?” With this project, Meireles took advantage of the global reach of American consumer culture by appropriating and personalizing one of its most popular exports."
 },
 {
  "sid": "s03",
  "text": "New York\nIn 1941 Hedda Sterne fled her home of Bucharest for New York City, where she befriended avant-garde artists including Barnett Newman, Mark Rothko, and Jackson Pollock. Despite her connection to this community of abstract painters, throughout her 60-year career Sterne remained focused on the world around her. As she once explained, “for the sublime and the beautiful and the interesting, you do not have to look far away. You have to know how to see.” In New York Sterne layered opaque and transparent planes to create an intricately composed window onto the density and vibrancy of the city"
 },
 {
  "sid": "s04",
  "text": "Amor Caritas\nThis angelic figure by Augustus Saint-Gaudens, a foremost sculptor of the Gilded Age, is the culmination of his portrayals of allegorical women. He made similar designs for the tomb of Edwin D. Morgan in Hartford, Connecticut, and the mantelpiece in the house of Cornelius Vanderbilt II in New York. Like many other late 19th-century artists, Saint-Gaudens often modeled angels to symbolize the traditional virtues of women. Amor Caritas (Love [and] Charity) probably depicts Davida Clark, the artist’s mistress. Saint-Gaudens brought a level of naturalism to his ideal figure, particularizing the facial features and rendering the drapery so that it suggests the human form beneath."
 },
 {
  "sid": "s05",
  "text": "Lovers\nThis printed textile exemplifies the innovative works produced at Kinngait Studios, an Arctic printmaking workshop established in 1956 and still in operation today. Lovers , a design by Anirnik Oshuitoq, features a repeated pair of seated figures who face one another. The small dots between their noses and outstretched hands hint at an affectionate and even spiritual connection.\n\nIn the mid-20th century, the Canadian government marshalled Inuit art as a tool for constructing national identity. Artists such as Oshuitoq successfully navigated the aesthetic demands of their federal sponsors, whose aims may have included assimilating Indigenous people while asserting their sovereignty through experimental prints like the one seen here."
 },
 {
  "sid": "s06",
  "text": "Seventeenth-Century Interior\nChicagoan Charles Gifford Dyer studied painting in Paris and Munich. The objects depicted here, such as the Chinese blue-and-white vase and Oushak Turkish rug, were likely collected during his extensive travels and represent the tastes of a worldly, wealthy man. The composition recalls 17th-century Dutch still lifes in its focus on surfaces, textures, and illusionism. Similarly, it evokes the fleetingness of life by juxtaposing items that quickly decay, such as fruit and flowers, with the enduring arts of literature and music."
 },
 {
  "sid": "s07",
  "text": "Study for the Muses (Eaglesmere Version)\nBrice Marden considers the process of painting to be “about transformation. Taking that earth, that heavy earthen kind of thing, turning it into air and light.” In the 1980s Marden developed a fluid, calligraphic line that resulted in shimmering, interlaced compositions such as Study for the Muses (Eaglesmere Version) . His paintings slow the spontaneous brushwork of gestural abstraction to an almost meditative pace. Though it is called a “study,” Marden worked and reworked this painting across nearly a decade, completing it in his studio in Eagles Mere, Pennsylvania, which he describes as the most “Zen-like” of his workspaces. The landscape of Eagles Mere is wet and overgrown with moss and hemlock, features echoed in this painting’s muted palette."
 },
 {
  "sid": "s08",
  "text": "Lion Hunt\nIn 1832 Eugène Delacroix joined a diplomatic envoy to French-colonized Algeria. The sights and experiences from this six-month journey fueled the rest of his career, lending his canvases an illusion of accuracy that his less-traveled competitors lacked. The artist expressed in his journals from abroad his admiration for Arab culture, even characterizing it as superior to that of post-revolutionary France. Nevertheless, in paintings like this he catered to violent European fantasies about the Arab world. Having never witnessed a lion hunt, Delacroix skillfully synthesized studies of landscapes, Islamic costume, and zoo animals to bring this narrative to life with theatrical intensity."
 },
 {
  "sid": "s09",
  "text": "Jazz Bowl\nThe Jazz Bowl was originally designed for Eleanor Roosevelt in celebration of her husband Franklin Delano Roosevelt’s re-election as governor of New York, and it has since become an icon of the Jazz Age and an the Art Deco period. Cowan Pottery liked the design, which captures the architecture, music, and nightlife of New York City as Viktor Schreckengost knew it, and the company decided to put the bowl into production. Using Schreckengost’s template and the sgraffito technique, workers scratched the design into the engobe, or black glaze. Schreckengost then inspected and signed the bowl. The final Egyptian blue glaze was applied to reflect New York at night."
 },
 {
  "sid": "s10",
  "text": "The Treatment 12\nToyin Ojih Odutola’s multimedia drawings are informed by her experience of coming of age as an African woman in the American South. Early in her career, she began creating vivid portraits that investigate the social and political dynamics of skin color, the malleability of identity, and the nature of the color black.\nThe Treatment was prompted by an invitation to participate in the 2015 group exhibition Young, Gifted and Black . Ojih Odutola used the title of the exhibition to direct the creation of a series of 43 portraits that was ultimately completed in 2017. In drafting each image she employed her signature black ballpoint pen as a tool for negotiating the formal and social implications of blackness as both skin color and surface treatment. She sourced public headshots and media images of prominent, or “gifted,” Caucasian men in their youth, and then outlined their silhouettes in pencil before filling in their faces with black ballpoint pen. Ojih Odutola redacts the socioeconomic status and white privilege of these subjects through her destabilizing treatment, as “black” becomes the primary identifier for otherwise recognizable men. Portraits from this series are shown in sequence or as a grid to underscore, in the artist’s words, “how an individual can claim one’s identity when rendered in the sameness of a group.”"
 },
 {
  "sid": "s11",
  "text": "After the Hurricane, Bahamas\nRevered as America’s master of watercolor, Winslow Homer did not begin working in the medium until the mature age of thirty-seven. As a watercolorist, Homer adapted his practice to the diverse locales he visited. His sojourns in the tropics took him to the Bahamas, Bermuda, Cuba, and various locations in Florida. In each new environment, the self-taught artist pushed the flexible medium in new directions as he applied his increasingly sophisticated understanding of color and light to a new set of atmospheric conditions. This compelling watercolor was painted during Homer’s second trip to the Bahamas in the winter of 1898–99. Depicting a luckless man washed up on the beach, surrounded by fragments of his shattered craft, the work demonstrates the artist’s fascination with the rapid and dangerous weather changes of the region. Here sunlight glints through gradually thinning storm clouds. Homer employed thickly applied opaque red and yellow pigments for the seaweed tossed on the sand, creating a contrast with the thin washes and fluid brushstrokes that he used to render the receding waves."
 },
 {
  "sid": "s12",
  "text": "On a Balcony\nIn this vibrant portrayal of a woman reading, Cassatt amplified her palette and brushwork, using energetic daubs of red, yellow, pink, and blue to describe the floral backdrop and the figure’s patterned dress. The balcony’s blue rail, visible near the top of the painting, defines the garden’s enclosed space, and her morning attire likewise emphasizes the setting’s intimacy. Reading a newspaper rather than a novel demonstrates that even at home, the woman is connected to the contemporary world. The painting was included in the 1880 Impressionist exhibition, Cassatt’s second showing with the group."
 }
]
