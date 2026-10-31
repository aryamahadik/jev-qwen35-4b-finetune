# Item 10 card authoring i10a_recipes_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_recipes_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are home-cooking recipes from a community cookbook: a short description, an ingredient list and preparation steps.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: cooking method: the main way the food is cooked or put together, where neighbouring answers are easy to confuse.
Card 2 angle: effort: how much work, time or skill the recipe asks of the cook, where neighbouring answers are easy to confuse.
Card 3 angle: main ingredient role: what the central ingredient of the dish is, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_recipes_2",
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
  "text": "Sev Puri (Crispy Indian Snack with Potato)\nIngredients:\n- 10 flat, crisp puris\n- 1⁄2 cup boiled potato (aloo), cubed\n- 3 tbsp tamarind chutney\n- 3 tbsp coriander chutney\n- 1⁄2 tsp cumin seed (jeera)\n- Salt\n- 1⁄2 tsp red chile pepper (lal mirchi)\n- 1⁄2 cup chopped onion\n- 1 cup fine sev\nProcedure:\n- Arrange the puris on a plate, and make a hole in the center of each puri.\n- Fill with a few chopped boiled potato cubes.\n- Add about 1⁄4 tsp of tamarind and green chutneys in each. Sprinkle with cumin powder, salt, red chilli powder.\n- Sprinkle finely chopped onions over top, then generously sprinkle sev all over the puris.\n- Garnish with finely chopped coriander.\n- Serve fresh."
 },
 {
  "sid": "s02",
  "text": "Chocolate Milk\nChocolate milk is milk flavoured with chocolate.\nIngredients:\n- Milk (as much as you want to make)\n- Chocolate syrup or melted chocolate (to taste)\nProcedure:\n- Pour milk into a glass or jug.\n- Add the chocolate\n- Stir well with a spoon or straw.\n- Enjoy!\nNotes, tips, and variations:\n- You can change the amount of chocolate and milk depending on how much chocolate/milk you like."
 },
 {
  "sid": "s03",
  "text": "Potato and Chicken Stew (Ajiaco)\nAjiaco is a quintessential dish from Bogotá, Colombia.\nSoup:\n- 1 ea. (approximately 750 g) whole skin-on bone-in chicken breast\n- 1 L chicken broth\n- 1 onion, peeled\n- 2 scallions (white part and first 2 cm of green)\n- 2 carrots, peeled\n- 4 cloves garlic, peeled\n- 1 bay leaf\n- 3 ml dried thyme\n- 2 ml ground cumin\n- 4 sprigs fresh cilantro\n- 10 black peppercorns\n- 5 ml tomato paste\n- 0.5 kg small yellow potatoes, peeled\n- 0.5 kg small purple potatoes, peeled\n- 0.5 kg mashing potatoes, peeled and sliced 2 cm thickness\n- 1 L water\n- 2 ml of beef bouillon granules\n- 0.25 ml frozen peas\nGarnishes:\n- 4 ears of corn, quartered lengthwise and cooked\n- 10 ml whipping cream mixed with 10 ml créme fraíche\n- 2 ripe but firm Hass avocados, peeled, pitted and cut into eight slices right before serving\n- 10 ml of finely chopped cilantro\n- 5–10 ml of pickled capers\nProcedure:\n- Combine chicken, broth, onions, scallions, carrots, garlic, bay leaf, thyme, cumin, cilantro and peppercorns in large saucepan and bring to a boil. Skim off froth as it rises. Reduce heat to low and cover when frothing finishes.\n- Remove and reserve chicken after it is cooked through (about 20 minutes).\n- Strain broth through sieve and return to pot, boil again over medium heat. Reserve carrots.\n- Add tomato paste and yellow and purple potatoes. Cover and cook until potatoes are soft (approximately 20 minutes).\n- While yellow and purple potatoes are cooking, boil sliced mashing potatoes in water and beef bouillon in separate pot. Once boiling, reduce to medium heat until potatoes start to fall apart (approximately 30 minutes).\n- Drain and reserve a quarter of the slices and mash the rest of the sliced potatoes. Add mashed and sliced potatoes to soup.\n- Remove bones and skin from chicken and discard. Cut chicken into strips 1 cm wide and 3 cm long.\n- Add chicken and peas to soup and simmer for 5 minutes. Slice the carrots into.5 cm thick rounds and add back into soup. Salt to taste.\n- Serve hot with garnishes available.\nNotes, tips, and variations:\n- If soup is too thick add boiling water in small amounts; the consistency should be like that of heavy cream."
 },
 {
  "sid": "s04",
  "text": "Grilled Cheese Sandwich II\nSee: Grilled Cheese Sandwich\nA toasted cheese sandwich works well as an everyday lunch. It goes well with soda (pop) or tomato soup. Quality greatly depends on ingredient selection and cooking temperature. A good toasted cheese sandwich has a crispy outside and is not mushy.\nIngredients:\n- Mild cheddar cheese\n- Butter\n- Sturdy low-moisture bread\nProcedure:\n- Slice the cheese 1⁄8-inch thick.\n- Butter the two slices of bread on one side each.\n- Cover a bread slice with cheese, over the unbuttered side. If you leave gaps, distribute them evenly throughout the middle.\n- Finish the sandwich with the other slice of bread; again, buttered side out.\n- Place the sandwich into a cool 2-sided contact-based cooking device, like a sandwich-iron, waffle iron, or a grill intended for cooking burgers. Heat the sandwich.\n- Remove the sandwich when all the cheese has melted and the outside is medium-dark brown and crispy.\n- Eat immediately. If you must set this sandwich down, use a heated plate or a loose paper towel to avoid letting condensation ruin the surface.\nNotes, tips, and variations:\n- Use low-moisture cheese. When buying cheese, most likely you will find that the cheeses are labeled for fat, protein, and total weight. Consider the unmentioned part to be moisture, and choose the cheese which minimizes this. For any given amount of protein per weight, choose the cheese with the highest fat content. Likewise, for any given amount of fat per weight, choose the cheese with the highest protein content.\n- Multi-grain bread tends to work well. Sourdough and English toasting bread should also work okay.\n- Add relatively dry tuna, bacon, or pastrami. After cooking, you may pry open the sandwich to add sauerkraut, pickles, or sweet chilli sauce.\n- A bit of Worcestershire Sauce poured on the cheese before cooking also works well.\n- Instead of butter/margarine on the outside of the bread, you can substitute mayonnaise for a tangier sandwich.\n- Thinly-sliced tomato is a nice addition to the sandwich, as are wilted spinach or roasted red peppers. You can also add sliced onion with the tomato to give a more exotic feel.\n- Remember to cool the cooking device a bit before cooking another sandwich."
 },
 {
  "sid": "s05",
  "text": "Baked Pork Chops\nA relatively simple recipe for baked pork chops.\nIngredients:\n- 3–4 bone-in pork chops, 1⁄4 inch (6 mm) thin\n- 1 medium apple, cored and sliced thin\n- 1 medium onion, sliced thin\n- 1 tablespoon (15 ml) honey\n- 1 tablespoon (15 ml) caraway seed (can be salvaged from the bag your rye bread comes in)\n- Garlic salt, black pepper, and Dijon mustard, to taste\nProcedure:\n- Heat oven to 350 °F (180 °C)\n- Layer sliced onion and apple in a baking dish that can be covered; drizzle honey and half the caraway over apple and onion slices\n- Season meat with garlic salt and pepper; spread top of meat with Dijon\n- Sprinkle remainder of caraway\n- Cover and bake for one hour."
 },
 {
  "sid": "s06",
  "text": "Wheat-Free Baking Mix\nThis wheat-free baking mix is a mixture of several other flours that, along with the addition of xanthan gum or guar gum, approximates wheat flour.\nIngredients:\n- 2 parts (28.5%) by weight white rice flour\n- 2 parts (28.5%) by weight brown rice flour\n- 2 parts (28.5%) by weight tapioca starch\n- 1 part (14%) by weight amaranth flour\n- 2–4% by weight xanthan gum (optional)\nProcedure:\n- Combine all ingredients. Mix until very thoroughly blended.\n- Use the blend as a substitute for wheat flour, using the same weight of the blend as of the wheat flour; for example, if a recipe calls for 100 g wheat flour, use 100 g of this blend.\nNotes, tips and variations:\n- Cakes, cookies, and other tender baked goods will need less xanthan gum. Breads and chewier doughs will need more xanthan gum."
 },
 {
  "sid": "s07",
  "text": "Three Sisters Stew\nThree sisters stew is a traditional and contemporary Native American dish. The dish includes the three sister foods of maize, beans, and squash, which are prevalent in many Native American diets. The three traditional ingredients are made together because of farming methods that often included all three crops in the same field with an interdependent relationship. Beans climb the tall maize stalks and fertilize the soil throughout their lives. Squash covers the ground between maize stalks, protecting the bean and maize roots.\nIngredients:\n- 1 ea. (2 lb) small pumpkin or butternut or carnival squash\n- 1 tablespoon olive oil\n- 1 medium onion, chopped\n- 2 cloves garlic, minced\n- 1⁄2 medium green or red bell pepper, cut into short, narrow strips\n- 1 can (14–16 ounces) diced tomatoes, with liquid\n- 2 cups cooked or canned pinto beans\n- 2 cups corn kernels (from 2 large or medium ears)\n- 1 cup water or homemade vegetable stock\n- 1–2 fresh hot chiles, seeded and minced\n- 1 teaspoon ground cumin\n- 1 teaspoon dried oregano\n- Salt, to taste\n- Freshly-ground pepper, to taste\n- 3–4 tablespoons fresh cilantro, minced\nProcedure:\n- Preheat the oven to 400°F.\n- Cut the pumpkin or squash in half lengthwise and remove the seeds and fibers. Cover with aluminum foil and place the halves, cut side up, in a foil-lined shallow baking pan.\n- Bake for 40–50 minutes, or until easily pierced with a knife but still firm (if using squash, prepare the same way). When cool enough to handle, scoop out the pulp, and cut into large dice. Set aside until needed.\n- Heat the oil in a soup pot. Add the onion and sauté over medium-low heat until translucent. Add the garlic and continue to sauté until the onion is golden.\n- Add the pumpkin and all the remaining ingredients except the last 2 and bring to a simmer. Simmer gently, covered, until all the vegetables are tender, about 20–25 minutes. Season to taste with salt and pepper.\n- If time allows, let the stew stand for 1–2 hours before serving, then heat through as needed. Just before serving, stir in the cilantro. The stew should be thick and very moist but not soupy; add additional stock or water if needed. Serve in shallow bowls.\nNotes, tips, and variations:"
 },
 {
  "sid": "s08",
  "text": "Salade Frisee\nIngredients:\n- 16 cups (loosely packed) frisee\n- About 1⁄2 cup Champagne Vinaigrette\n- 8 goat cheese cakes\n- Crumbled crisp bacon pieces, for garnish\nProcedure:\n- In a large mixing bowl, toss frisee with the Champagne Vinaigrette.\n- Divide salad among 8 salad plates.\n- Top each salad with a goat cheese cake.\n- Garnish with crumbled bacon."
 },
 {
  "sid": "s09",
  "text": "Portable Eggs Benedict\nThis is a neat to-go version of our favorite poached egg dish.\nIngredients:\n- 1 dash white vinegar\n- 2 large eggs\n- 1 pita\n- 2 tbsp cream cheese\n- Smoked salmon\nProcedure:\n- Boil enough water to fill a deep pan.\n- Add vinegar to the water.\n- Crack eggs into the boiling water/vinegar mixture. Leave them alone for 5–7 minutes.\n- Cut open the top of a pita. Line the inside of the pita with cream cheese and smoked salmon.\n- Take eggs out of the pan using a slotted spoon and drop them into the pita.\n- Eat immediately."
 },
 {
  "sid": "s10",
  "text": "Rosehip Tea\nRosehips are extremely high in vitamin C and can be brewed into an infusion. The resulting tea may be a pinkish color and taste acidic, but not as acidic as lemon juice.\nIngredients:\n- Rosehips\n- Sweetener (optional)\nProcedure:\n- Boil the rosehips in water for at least 10 minutes, using 2 tbsp rosehips per pint of boiling water. In order for the flavor to fully expand into the water and make the best quality tea, the hips must expand, split, and let the water get at the seeds within.\n- Let cool for a moment, and add sweetener if desired."
 },
 {
  "sid": "s11",
  "text": "Sockerdricka (Swedish Ginger Drink)\nSockerdricka (Swedish for \"sugar drink\") is a soft drink from the 19th century. It is traditionally a fermented drink that contains ginger, but modern commercial versions consist of carbonated water, some sugar, and citric acid.\nIngredients:\n- 20 litres water\n- Peel of 1 lemon\n- 1 kg white granulated sugar\n- 60 g yeast\n- 25 g ginger\n- Raisins\nProcedure:\n- Boil the sugar, water, lemon and crushed ginger for 15 minutes.\n- Strain the mixture and let it cool.\n- Mix in the yeast and let the mixture ferment for 2 days.\n- Put the drink in bottles, and add a raisin to each bottle.\n- Cork the bottles, and let rest for 5 days. After 5 days the sockerdricka is ready for drinking.\nNotes, tips, and variations:\n- The recipe above has lots of yeast, and not much ginger. It would work well with just 10 g yeast. More ginger would be good (e.g. 100 g of fresh ginger for 20 litres)."
 },
 {
  "sid": "s12",
  "text": "Apple Jelly\nApple jelly is a jelly dessert that contains apple. It is sourced from Mrs Beeton's Book of Household Management, which is public domain.\nIngredients:\n- 1 pound (450 g / 4 ea.) apples\n- 3 ounces (85 g / 1⁄3 cup) caster sugar\n- 1⁄2 US pint (240 ml / 1 cup) water\n- 1 lemon, zested and juiced\n- 2 tbsp water\n- 0.5 ounces (14 g) leaf gelatine\nProcedure:\n- Peel and slice the apples, then put them into a pan with the sugar, 1⁄2 pint water, lemon juice, and lemon zest.\n- Simmer until tender, and rub through a fine sieve.\n- Bloom the gelatin in the 2 tbsp water. Melt the bloomed gelatin, strain it, and stir it into the apple mixture, and turn into a prepared mould.\n- Chill in the fridge for a few hours until set."
 }
]
