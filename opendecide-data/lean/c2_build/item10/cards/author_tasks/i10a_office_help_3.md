# Item 10 card authoring i10a_office_help_3

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_office_help_3.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are questions that people posted on a help forum for an office software suite (documents, spreadsheets, presentations, databases).
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: program area: which part of the office software the post is about, where neighbouring answers are easy to confuse.
Card 2 angle: answer needed: what kind of answer would settle the post, where neighbouring answers are easy to confuse.
Card 3 angle: request: what the poster wants from a helper, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_office_help_3",
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
  "text": "Multiline Fields\nI am attempting to import a legacy “database” (currently a .xls file) to a new Base database. The difficulty is that multiline cells lose their multiline character on import.\n\nAt present, the .xls cells are made multiline though use of the invisible character within the cells; these cells are being imported into Base fields designated as “Memo” type (and on import I get “too long” error messages but the material seems to come in). However, on import, it loses all line breaks within cells.\n\nExample: the .xls file’s cell might look something like\n\n1 1/2 cups chicken stock\n\n8 oz fresh/refrigerated rice cakes\n\n1 1/2 Tbs gochugaru\n\n(and so on for a variable number of lines, each line ending with a character in the existing .xls file)\n\nbut when imported, whether or not checking the CR/LF block in the import wizard, this results in\n\n1 1/2 cups chicken stock8 oz fresh/refrigerated rice cakes1 1/2 Tbs gochugaru\n\nwhich is obviously unusable. So, what has gone wrong here? (Note: I’m using a “recipe” as a sample template here because it’s a fairly clear example; due to the highly variable number of lines in each cell, ranging from 3 to 40 or so, they CANNOT be converted to individual fields, especially since in the actual database some of those lines are not actually independent of each other but are single data elements that have to output and be edited in a multiline format.)\n\n-\nDoes the .xls file need to include a dummy character instead of the , that can later be mass-changed in the Base file (and if so, I can’t find a clear explanation of how to do this to change to within-field CR/LF or equivalent)?\n\n-\nIs there a different choice or parameter I need to set during import that I’m just not seeing as an option?"
 },
 {
  "sid": "s02",
  "text": "Calibri sometimes doesn't render on opening a document\nI’ve seen one other English thread relating to this, of sometimes when I open an Office document, Calibri font doesn’t render.\n\nI’ve actively seen it in Calc and Writer.\n\nIt’s USUALLY fixed by closing all windows and reopening the document. It’s sometimes fixed by me changing the font then changing it back - though sometimes it will remain when changing back to it. Rarely I need to restart the whole computer to fix it.\n\nIt was common enough in one calc document that I just changed the font to Bahnschrift because I needed the document to work every time.\n\nI’m running\n\nBuild ID: d401f2107ccab8f924a8e2df40f573aab7605b6f\n\nCPU threads: 16; OS: Windows 11 X86_64 (build 22631); UI render: default; VCL: win\n\nLocale: en-NZ (en_NZ); UI: en-GB\n\nCalc: CL threaded\n\non a windows 11 computer with the TTF of calibri light installed as a base file\n\nIt’s set to 12pt Calibri as a default, which I know I can change.\n\nI’m not sure if I should try and create a bug report since it happens seemingly at random, then will take different fixes depending on the day."
 },
 {
  "sid": "s03",
  "text": "Chart Export as Image issue in 2025.2.3.2 Debian\nHaving a very strange issue in Libreoffice Calc. When I use the right click export as image on charts, all the text elements are missing. Only the graphic elements export. I have read that there was a similar bug in Bug153672, however this have been fixed - apparently.\n\nI am using debian 13 (Trixie) and the version that is within debians repository. 2025.2.3.2 .\n\nI have copied the chart into Draw, same issue when exporting to a image file. Even if I add ta text box in Draw, that additional text box is still stripped out.\n\nAll I can do at the moment is take screen shots or export to pdf then edit that."
 },
 {
  "sid": "s04",
  "text": "Color of text in cel is jumping back to black after I have changed it and I leave the cell\nI have been using Linux Mint, and Libre Office also, for a few weeks now. When I want to change the color of the text in a cell in CALC, it jumps back to black after leaving the cell. I assume this is a minor problem in principle, but for me, it is a major problem. Who can help me?"
 },
 {
  "sid": "s05",
  "text": "Lock objects altogether\n- os v.: Ubuntu 22.04.5 LTS\n\n- file format: *.odt\n\nHow do I lock multiple objects at once? Let’s say I add an image, then draw over it or insert a rectangle to highlight a specific feature. Then I would need to lock drawing objects to the image so that I can freely move the image so the objects on the layer change position respectively to the image."
 },
 {
  "sid": "s06",
  "text": "Is there a way to share LO UI settings between Windows and Linux machines?\nI have five computers, all of which have LO installed. My goal is to maintain a shared user profile (or, more accurate to say, part thereof whose sharing is both possible and reasonable) on the file server. The challenge stems from the fact that two of the machines run Windows, whereas the remaining three run Linux.\n\nI have already created several symbolic links in both OSes, which has enabled templates, Basic macros, and Python scripts to be shared. However, AFAIK, this approach cannot be readily applied to due to paths syntax mismatch between Linux and Windows.\n\nThat being said, I make extensive use of customisation which I like to optimise depending on the tasks I am doing in the meantime and am not particularly enthusiastic about having to repeat assigning a hotkey or adding/removing a toolbar button five times. While realising that a complete solution is unlikely to exist (the current approach of storing the entire UI configuration in this file was probably never designed to support sharing across different OSes), I wonder whether the situation can be partially remedied."
 },
 {
  "sid": "s07",
  "text": "Libreoffice 26.2.1 [with some problems]\nWhen a release increases, frequently some features stop to function or continue to badly or not operate.\n\n- Writer - Side bar, table properties, column width: set the value and confirm: LO crashes (at least since 7.6)\n\n- Writer - Document language setting for spelling checker: I can’t set the language (LO Writer doesen’t maintain the setting)\n\n- Writer Spelling checker - It starts and after some checks the window freezes with all the pushbuttons in grey: cannot quit from the window\n\n- Draw - LO suddenly quits during document save.\n\nI’m very sad. I use LO Writer in my job, I’m a technical writer, and the usual tools in our job suffer a lot of thei age. This is the reason why I migrated to LO Writer some years ago.\n\nI don’t know why this happens. In my opinion the software shoud be tested better also by expert, regular and hard users, as I consider to be, due to my long term software use. Undortunately, despite I regularly check about the possibility to collaborate I cant’ figure out I could make so usefully.\n\nI removed 26.2.1 and return back to 7.6, as I did for years with 5.4.\n\nNo ansewer needed."
 },
 {
  "sid": "s08",
  "text": "Hundreds of 'normal' styles in calc\nWhy do I have hundreds of ‘normal’ styles in Calc? I can’t be the only one but I can’t find a reference to the issue.\n\nParts of the spreadsheet were originally from Excel so I suspect that may play a part.\n\nI haven’t done any real troubleshooting because it’s a nuisance but doesn’t impact functionality or noticeably impact performance and I wouldn’t know where to start getting a baseline then tracking when it occurs.\n\nUpdate - Sorry - should have tried this before posting. I thought I’d tried deleting them before but maybe not. I’ve selected and deleted them all and will update the post if they start reappearing.\n\nimage 173×782 10.2 KB"
 },
 {
  "sid": "s09",
  "text": "Tabs mode discuss(11-may-2026)\nAs we discussed it in group, I try to test different collaboration platforms. Heiko Tietze started it today, he published to Penpot and give link to chat. I will try to test using Discourse to discussing.\n\nFirst topic will be related to LibreOffice Tab Mode. I compared tab mode in different office suites and created screenshot (see Home-tab.png - The Document Foundation Nextcloud )\n\nизображение 1916×563 171 KB\n\nFirst question: do you want to use system frame or create own window border?\n\nIt has pros (It takes many place on screen, but cons also it will be not similar with all system and , as you can notice from my screenshot OnlyOffice don’t use my chosen theme to window decoration, what’s why I enabled in window border in Waterfox, even that it takes place in screen."
 },
 {
  "sid": "s10",
  "text": "Style Usage Questions [recipes with sections or frames]\nBackground\n\nMy use of Styles to manage an entire document has been limited. My new goal is to prioritize the use of Styles. I know how to modify, add new, and assign. But I’m a little fuzzy on the hierachy of Styles, positioning, and the use of Sections versus Frames.\n\n.\n\nSo far I have downloaded some LibreOffice templates and examined them.\n\n.\n\nI used the LibreOffice Template Wizard and examined the results.\n\n.\n\nI am slowly making my way through the book, Designing with LibreOffice .\n\n.\n\nMy practical “learning” application is going to be full-page recipes that consist of:\n\n.\n\n.\n\nMany of the examples I viewed used Tables to control location. I was leaning towards Sections or Frames, rather than Tables.\n\n.\n\nLines 02-04, 07-08, 11-12, 15-16 would be Sections with 2 columns.\n\n.\n\nLines 01 is the main heading and 06, 10, 14, 18 are subheadings above their Sections.\n\n.\n\nLines 05, 09, 13, 17 are blank lines for spacing.\n\n.\n\nQuestions\n\n.\n\n- Are Sections the right approach to separate the Picture-plus, Ingredients, Steps, Nutritional Information, and Notes?\n\n.\n\n- When creating any new Style, do you Inherit always from the Default Paragraph Style and modify the attributes as needed?\n\n.\n\nWhen I create a new style, I prefix them with a string so I can identify them, plus it makes the name unique. There is a Tip on page 35 of Designing with LibreOffice suggesting something similar.\n\n.\n\n- When I first started creating styles I started from the top down, but that created a problem with selecting the Next Style. Is it better to create new Styles from the lowest level on the hierachy so you can reference them in the Next Style field as you move up?\n\n.\n\n- How do I add space after a Section? Do I just add an empty paragraph to achieve the blank line or maybe add the space above the subheading?"
 },
 {
  "sid": "s11",
  "text": "Empty column width page in table's property window\nHi, all!\n\nI’m not able to modify the column width of the tables. The relative page in the table’s property window is empty. I have installed LibreOffice via .deb on my Debian 13 yesterday, after a new fresh installation. How could I resolve it?\n\nScreenshot From 2026-03-28 12-08-44 1920×1080 167 KB"
 },
 {
  "sid": "s12",
  "text": "Can we turn off the black 'hover boxes'?\nIt’s usually wanted but those information boxes that pop up when you hover over something, can that be turned off? I’m doing some hopping around in Navigator at the boxes popping up every time I move the mouse is bothersome. Just temporarily mind, I thing that LO’s information boxes are the best I’ve ever seen."
 }
]
