# Item 10 card authoring i10a_recipes_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_recipes_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are home-cooking recipes from a community cookbook: a short description, an ingredient list and preparation steps.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: dish type: what kind of dish the recipe makes, where neighbouring answers are easy to confuse.
Card 2 angle: occasion: the setting or meal the dish is best suited to, where neighbouring answers are easy to confuse.
Card 3 angle: dietary fit: who could eat the dish, judged only from the ingredients and steps, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_recipes_1",
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
  "text": "Crown Roast of Lamb\nIngredients:\n- 2 racks of lamb, trimmed and frenched\n- 2 tbsp thyme, finely chopped\n- 1 tbsp rosemary, finely chopped\n- Kosher salt\n- Freshly-ground black pepper\n- Olive oil\n- 1 1⁄2 tbsp smoked paprika\n- 1 tbsp garlic powder\nProcedure:\n- Brush both racks of lamb with olive oil. Sprinkle with paprika, garlic powder, and kosher salt and freshly ground black pepper. Rub seasonings into the meat.\n- Place both racks in a bundt pan and tie the end bones together with butcher's twine.\n- Place on the middle rack of the oven and roast for 30–35 minutes, until the meat reaches an internal temperature of 145°F for medium rare.\n- Remove and let rest 10 minutes. Serve."
 },
 {
  "sid": "s02",
  "text": "Cream Puff\nPastry:\n- 1 cup (240 ml) water\n- 1⁄2 cup (120 g) shortening\n- 1 cup (120 g) flour\n- 1⁄8 teaspoon salt\n- 3 eggs\n- 2 teaspoons baking powder\nFilling:\n- 1 cup (240 g) white granulated sugar\n- 1⁄3 cup (80 g) cornstarch\n- 1⁄3 teaspoon salt\n- 1 egg\n- 2 cups (480 ml) scalded milk\n- 1 teaspoon vanilla extract\nPastry:\n- Sift together the flour and salt.\n- Heat water and shortening in saucepan until it boils.\n- All at once, add the flour mixture and stir vigorously to make a dough.\n- Remove from heat.\n- Cool the dough, and mix in unbeaten eggs one at a time.\n- Add baking powder; mix.\n- Drop by spoonfuls 11⁄2 inches (4 cm) apart on greased baking sheet, shaping into a circular form with a spoon but keeping mixture mounded in the center.\n- Bake about 30 minutes in hot oven. Cool.\n- Cut with sharp knife near the base to allow for filling.\nFilling:\n- Mix dry sugar, cornstarch, and salt together.\n- Add slightly beaten egg.\n- Gradually stir in the scalded milk.\n- Cook about 15 minutes in a double boiler, stirring constantly until thickened.\n- Cool slightly, add vanilla extract, and whisk vigorously for creaminess.\n- Cool completely, then fill the puffs with the filling.\nNotes, tips, and variations:\n- Sweetened whipped cream may be used instead of this filling.\n- Rather than cutting the pastries open, spoon the filling into a pastry bag, then inject it from the bottom.\n- Dust with powdered sugar or drizzle with semi-sweet chocolate"
 },
 {
  "sid": "s03",
  "text": "Friar's Omelette\nFriar's Omelette is a traditional Scottish recipe for eggs and apples. However, apple can be substituted by other fruit such as rhubarb, plum (with stones removed), or blackberry.\nIngredients:\n- 6 medium cooking apples\n- 4 ounces (125 g / 1 stick) butter plus butter for greasing a baking dish\n- 2 ounces (50 g / 4 tablespoons) white sugar\n- 1 ounce (25 g / 1 rounded tablespoon) white sugar for decoration\n- 2 eggs, well beaten\n- 4 ounces (125 g / 1 cup) breadcrumbs\n- 1⁄4 pint (150 ml) water\n- Squeeze of lemon juice\nProcedure:\n- Peel and core the apples, slice them, and place in a saucepan with the water.\n- Cook until soft (similar to applesauce), then remove from heat and add butter, sugar and lemon juice; mix well.\n- While this is cooling, beat the eggs very well. When the apple mixture is cool, mix in the eggs as well.\n- Butter a deep baking dish and spread the breadcrumbs around it so that they stick to the bottom and the sides, keeping a good amount for the top.\n- Pour the apple and egg mixture into the dish and cover with a thick layer of breadcrumbs.\n- Bake in a moderate oven (350°F / 180°C / Gas Mark 4) for about half an hour.\n- Turn out onto a flat dish and sprinkle with sugar before serving."
 },
 {
  "sid": "s04",
  "text": "Deep Fried Urad and Rice Flour Dough Balls (Murukku)\nIngredients::\n- 2 cups rice flour\n- 1⁄2 cup urad dal\n- 2 tsp jeera\n- 4 tsp sesame seeds\n- 1 tsp red chile powder\n- Salt to taste\n- 3 tbsp oil (hot)\n- Oil for deep frying\nProcedure:\n- Dry roast the urad dal. Grind it into a fine powder, and keep it aside.\n- In a wide bowl combine the rice flour, urad dal powder, chili powder, salt, sesame seeds, and jeera. Mix it well, then mix in the oil.\n- Mix in enough water to make a dough of roti consistency.\n- In a deep frying pan heat enough oil for deep frying.\n- Once the oil is hot enough for frying, press dough into a murukku mould. Fry the murukku in batches until they are light golden brown in color.\n- Drain the finished fritters on a paper towel.\nNotes, tips, and variations:\n- The frying oil should not be too hot, or the murukku will burn.\n- These can keep up to 2 weeks in an airtight container."
 },
 {
  "sid": "s05",
  "text": "Molasses Taffy\nIngredients:\n- 1⁄2 cup fancy molasses\n- 1 1⁄2 cups granulated sugar\n- 1 1⁄2 Tbsp vinegar\n- 1⁄2 cup water\n- 1⁄4 tsp cream of tartar\n- 4 Tbsp butter\n- 1⁄8 tsp baking soda\nProcedure:\n- Combine molasses, sugar, vinegar and water in a heavy saucepan over medium heat.\n- Cook to 255–270°F (124–132°C). The hotter the syrup, the harder the final taffy will be.\n- Remove from heat and stir in butter, cream of tartar, and baking soda.\n- Pour into buttered pan or onto marble surface, and let cool slightly.\n- When cool and thick enough to handle, grease your hands. Grab the candy mixture with both hands, and stretch it apart while twisting slightly. Repeat this process, pulling and twisting the candy until light in color. This pulling and twisting process incorporates air and lightens the candy.\n- Cut into 1-inch pieces; wrap in squares of waxed paper."
 },
 {
  "sid": "s06",
  "text": "Chocolate Squares\nA chocolate square recipe that tastes delicious.\nBase and topping:\n- 1⁄2 cup (120 g) margarine, softened\n- 1 cup (240 g) brown sugar\n- 1 egg\n- 1 teaspoon vanilla\n- 1 1⁄4 cup (300 g) all-purpose flour\n- 1 1⁄2 cup (350 g) rolled oats\n- 1⁄2 teaspoon baking soda\n- 1⁄2 teaspoon salt\nFilling:\n- 2⁄3 cup (160 ml) sweetened condensed milk\n- 1 cup (240 g) chocolate chips\n- 2 tablespoons hard margarine\n- 1 teaspoon vanilla\n- 1⁄4 teaspoon salt\nBase and topping:\n- Cream together the margarine and brown sugar until light and fluffy.\n- Beat in egg and vanilla.\n- In a mixing bowl, blend together the flour, oats, baking soda and salt.\n- Mix flour mixture into creamed mixture, using a wooden spoon to start, until crumbly looking.\n- Reserve roughly 1⁄3 of the mixture in a bowl and set aside.\n- Press remaining mixture into a greased, lined square pan.\nFilling:\n- In a mixing bowl over a pot of boiling water, heat all filling ingredients until chocolate chips are just melted.\n- Spread chocolate mixture evenly over prepared base, keeping the sides of the pan clean.\n- Take reserved mixture and sprinkle over the top. Note that it will not cover the whole surface.\n- Bake at 350°F (180°C) for 20 to 25 minutes, or just until oatmeal mixture has a light golden colour.\n- Let cool, cut, and serve."
 },
 {
  "sid": "s07",
  "text": "Indian Chai\nIngredients:\n- 1⁄2 cup water\n- 1⁄2 cup milk\n- 1 teaspoon tea leaves\n- 2 teaspoons sugar OR 1 packet artificial sweetener (adjust according to taste)\n- Dash of chai masala (a little more than a pinch depending on your taste)\nEquipment:\n- 1 saucepan\n- 1 tea cup\n- 1 strainer\nProcedure:\n- Add all the ingredients to the saucepan.\n- Bring to a boil, and let simmer for no more than a minute, unless you like a stronger tea taste.\n- Strain the mixture into a cup.\nNotes, tips, and variations:\n- Milk-like beverages can take the place of milk.\n- Most ordinary supermarket teas are okay. You can also go to an Indian store.\n- Adjust the milk/water quantities to your taste.\n- When water comes to boil, you can add some grated ginger, a pinch or two of powdered cinnamon, or fresh tulsi leaves.\n- To make a stronger tea: boil around 3⁄4 cup water, add sugar and tea, turn off the flame, and cover the pot with a lid. Strain the black tea into a cup, and then add hot milk to taste."
 },
 {
  "sid": "s08",
  "text": "Sukiyaki\nSukiyaki is a kind of shabu-shabu (a Japanese dish) but it is a bit sweeter.\nIngredients:\n- Beef, sliced thin\n- 1 napa cabbage\n- Green onions\n- Firm tofu\n- Shiitake mushrooms\n- Spinach\n- Shirataki noodles\nSauce:\n- Soy sauce\n- Sake\n- Sugar\n- Water\nProcedure:\n- Wash the vegetables, and cut them into large pieces.\n- Soak the mushrooms in warm water for 15 minutes.\n- Mix the sauce ingredients in a small bowl.\n- Heat an electric skillet on low heat, and grease with a little bit of oil.\n- Put a few slices of beef into the skillet, and cook them until brown.\n- Add sauce (don't add all of them at the same time).\n- Sort the beef slices to the sides. Add the rest of the ingredients in an organized fashion.\n- Serve the sukiyaki with bowls of rice, with a raw egg yolk as the dip. Add more ingredients as necessary."
 },
 {
  "sid": "s09",
  "text": "Pineapple Curry\nThai pineapple curry (แกงสับปะรด / kaeng sap pa rod) is a traditional curry of Southern Thailand. The recipe has crushed pineapple with juice, so it tastes both sweet and sour. It is often served over rice and garnished with peeled orange slices, diced green onion, or celery.\nIngredients:\n- 175 grams pineapple pieces\n- 2 tablespoons Thai red curry paste\n- 1⁄2 cup coconut milk\n- 8 oz shrimp, or whatever meat desired\n- 1⁄2 tablespoons palm sugar\n- 1⁄2 tablespoons fish sauce\n- 11⁄2 tablespoons ripe tamarind\nProcedure:\n- Simmer the coconut milk in a saucepan over medium heat for 5 minutes and add red curry paste.\n- Put the sliced pineapple in the curry and wait until it is soft.\n- Bring to a boil over high heat, then add the shrimp.\n- Flavor the curry by adding the palm sugar, fish sauce, and ripe tamarind. Add more palm sugar for a sweeter curry, add more fish sauce for a salty curry, and add more ripe tamarind for a sour flavor."
 },
 {
  "sid": "s10",
  "text": "Sausage and Egg Breakfast Roll\nIngredients:\n- 2 small breakfast sausages\n- 1 egg\n- Cream cheese\n- 1 ciabatta roll, sliced open\n- Salt\n- Pepper\nProcedure:\n- Cut the sausages into small pieces and fry until done. Drain grease if needed and, if you desire, rinse very lightly, using a colander, then return to the pan.\n- Add the egg and mix into the sausage pieces until all the liquid is gone. Add salt and pepper for taste.\n- Thickly spread the cream cheese onto the ciabatta roll, and pile the egg and sausage mix into the roll.\n- Serve classic sandwich style or keep the halves separate."
 },
 {
  "sid": "s11",
  "text": "Poticza\nThis recipe, adapted from The King Arthur Flour Baker's Companion, makes two standard loaves of very rich bread.\n\nTo serve poticza, slice the cooled loaf into half-inch (1 cm) slices; you should get about 16 slices per loaf. Serve warm or at room temperature with coffee or hot tea. It can be made a day or two in advance.\nIngredients:\nThe bread and the filling are prepared separately. Three ingredients (sugar, flour, eggs) appear in this list twice, because they are added in separate steps.\nSpecial equipment:\n- 2 loaf pans (8.5 x 4.5 inches / 21.5 x 11.5 cm)\n- Rolling pin\nProcedure:\nThis process will take you straight through, from start to finish. If you'd like to divide the work across two days, the dough and/or the nut filling can be mixed the day before and stored in a covered bowl in the refrigerator until needed in the assembly process.\nDough:\n- Heat the milk and butter together in a microwave or in a small pan on the stovetop until the butter is melted and the milk is very warm, but not boiling. Set it aside to cool until it is warm but not uncomfortable to the touch.\n- Combine 1⁄4 cup sugar, 1 tsp salt, 3 cups flour, potato flour (optional), and yeast into a large mixing bowl. Stir the dry ingredients briefly to mix.\n- Stir in the melted butter, warm milk, vanilla extract, and eggs. Using either the dough hook on an electric mixer, a big spoon, or your hands, mix and knead until the dough is smooth and uniform. This is a \"slack\" (wet) dough, so it will be quite sticky when you start mixing it. It should come together after a couple of minutes.\n- Cover the kneaded dough and put it in a warm place to rise for about an hour. Alternatively, the dough can be brought to this point, placed in a bowl and covered with plastic wrap or a tightly fitting lid, and left in the refrigerator overnight.\nFilling:\n- Stir together the chopped nuts, nut meal, the remaining 1 cup of sugar, the remaining 1⁄3 cup of flour, pinch of salt, cinnamon, and the remaining 3 eggs. The mixture will be a thick paste. However, if it's too thick, you won't be able to spread it."
 },
 {
  "sid": "s12",
  "text": "Tuwo Shinkafa (Nigerian Mashed Rice)\nTuwo shinkafa is a type of Nigerian swallow made from mashed non-parboiled rice or corn. It is mostly eaten by the Hausa in the northern part of the country. Tuwo shinkafa is usually prepared from scratch with short grain rice, but it can also be prepared with rice flour. It is easy to prepare and usually serves as an accompaniment for soups and stews.\nIngredients:\n- 500 g (2 milk tin cups) short-grain non-parboiled rice\n- Water (about twice the volume of the rice)\nEquipment:\n- Pot\n- Potato masher or wooden spatula\n- Small container or wrapping nylon\nProcedure:\n- Wash the rice thoroughly, then drain.\n- Add water to pot and bring to a boil.\n- Add the rinsed rice to the pot of boiling water.\n- Simmer the rice until the water is absorbed and the rice is soft and sticky. If the rice hasn't softened when all the water is gone, add additional water as needed.\n- Use the spatula to thoroughly mash the soft rice until it forms a soft dough.\n- Mold into desired container and allow to take shape of the container or wrap inside nylon\n- Serve hot with your preferred soup.\nNotes, tips, and variations:\n- Non-parboiled rice is preferred because it is more sticky\n- Ensure thorough mashing to reduce rice lumps"
 }
]
