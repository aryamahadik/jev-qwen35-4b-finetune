# Item 10 card authoring i10a_office_help_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_office_help_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are questions that people posted on a help forum for an office software suite (documents, spreadsheets, presentations, databases).
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: problem type: what kind of problem the poster describes, where neighbouring answers are easy to confuse.
Card 2 angle: symptom: how the problem shows itself to the poster, where neighbouring answers are easy to confuse.
Card 3 angle: stage: how far the poster has already got (nothing tried, tried some fixes, found a partial answer), where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_office_help_2",
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
  "text": "How to block image on background so that it stays put when exporting as epub\nHi,\n\nI’m trying for the first time to format a novel with LibreOffice. I have an image that goes on the background of every chapter title, but when I export it as an epub the image is not places as in the original document but both image and chapter title are separated.\n\nI tried anchoring the image both to Paraghaph and to Character but it does not change. Do you have any suggestions?\n\n(Edit: I attatched the images to make it more clear what I meant)\n\nLibreOffice help 906×490 444 KB"
 },
 {
  "sid": "s02",
  "text": "Copy pasete issue with writer unwanted blank lines\nI’m hitting a issue with the latest version of Libre Office. This did not happen with the prior version.\n\nIf I copy text from a web site, into a Writer document I am getting unwanted blank lines (paragraph breaks?). This happens whether I am copy pasting a single sentence or more than one paragraph\n\nPaste unformatted text is not a solution because if the copied text is more than one paragraph and I use paste unformatted text I lose a wanted paragraph break.\n\nAgain, this did not happen in the prior version of LO. It is a new issue."
 },
 {
  "sid": "s03",
  "text": "[somved]Base form is slow 13min to load\nIf open the form called “1)BedsDone” it takes over 13 minutes\n\n[ ](download the database from dropbox)\n\nBuild ID: d401f2107ccab8f924a8e2df40f573aab7605b6f\n\nCPU threads: 4; OS: Linux 6.8; UI render: default; VCL: gtk3\n\nLocale: en-CA (en_CA.UTF-8); UI: en-US\n\nCalc: threaded"
 },
 {
  "sid": "s04",
  "text": "How to set or change a cell's color by 'Theme' or 'Tint'?\nIn Microsoft Excel a cell’s fill color/background color is set by default with Theme and Tint attributes, whereas in LibreCalc it is ‘Standard’/RGB hexadecimal.\n\nI tried, Left Click on Cell > Navigate to Format> Cells, then Font Tab.\n\nThere’s only option to change font name/style, the size. I tried Background tab> Color button, I see a drop down menu with Standard set to default. I plan to use OpenPyxl to hopefully get and set the tint and theme values.\n\nThe page here:\n\nSays Format> Theme\n\nTheme does not appear under Format. I only see Spredsheet Theme which affects all cells."
 },
 {
  "sid": "s05",
  "text": "Print multiple word documents in alphabetic order\nHello. I am using LibreOffice 26.2.1 version on Win10 pro. I encountered a problem with printing from the context menu that is called by right-clicking in the Explorer. Previously, I used Excel to print documents, but now I need to print from LibreOffice Calc. The problem is that the documents are printed in a different order than alphabetical. I still haven’t figured out what order is used for printing. I only found confirmation on the Internet that many people experience this when printing documents. It’s just that I print a lot of documents, and sorting them later becomes challenging.\n\nI decided to find out from the experts if there is any add-on in Libreoffice that will allow you to print documents in bulk alphabetically from the Explorer? It just didn’t work when printing from Excel, but Excel had other issues.\n\nAt the moment, I have implemented printing via powershell, but I would like to have the ability to print in bulk via the context menu from the Explorer. I would appreciate any advice."
 },
 {
  "sid": "s06",
  "text": "FInd Char in SQL Query in Base\nI am linking to a remote database and trying to SELECT part of a field which is a name e.g. “John Smith” by locating the space character. But failing to find a way to do this.\n\nSELECT LEFT(recommended,3) will get the first three characters\n\nBut SELECT LEFT (recommended,FIND(\" \";recommended)) fails\n\nWhat is the right syntax/function"
 },
 {
  "sid": "s07",
  "text": "Saving document from an xltx file as xlsx crashes the program\nI’m using Manjaro i3wm.\n\nBuild ID: 620(Build:3)\n\nCPU threads: 2; OS: Linux 6.6; UI render: default; VCL: gtk3\n\nLocale: en-US (en_US.UTF-8); UI: en-US\n\n26.2.0-4\n\nCalc: threaded\n\nIf asking for the file, maybe DM me, it’s a private document so I don’t really want to share it here."
 },
 {
  "sid": "s08",
  "text": "Update has stopped Office working\nHello,\n\nI have good reasons to remain on Widows 7 and until today was using v 25.2.3 and all was well.\n\nToday a brief message on starting Writer said that something had been updated. OK, i clicked again to start and this failure came up: oops, new user and can’t attach screen shot...\n\nIt said that the following file was missing: api-ms-win-core-path-l1-1-0.dll\n\nI searched and found that the latest version of LO requires Win 10 so I tried repairing the installation without success, then uninstalled and made a fresh installation of v 25.2.3\n\nOn starting Writer it showed the opening splash screen and then went into a loop of “Updating version” (or similar and then the splash screen. I broke out of that after many iterations, restarted Windows and can’t even get to the opening screen with the missing dll error above.\n\nI’m stumped and any help (other than change to Win 10) would be gratefully accepted. For what it’s worth I have contributed in the past and will happily do so again if I can overcome this problem.\n\nBest wishes to all,\n\nDavid"
 },
 {
  "sid": "s09",
  "text": "In the latest verson of Writer, my text often gets distorted when I open older existing documents, which were originally created by LOW. I have turned on the non-printting characters to expecting to see extra spaces or stuff like that, but they all looked legit. No extra space anywhere. But the lines look disproportionate. This happens in both English and non-English texts (i.e., where non-Roman script is used). Maybe I’m doing something wrong. But then I need to find out what it is. This phenomenon didn’t exist in the preceding version of LOW.\n\nI am pasting a screenshot here.\n\nLet’s hope someone would be kind enough to help me.\n\nClipboard_03-26-2026_01 905×276 107 KB"
 },
 {
  "sid": "s10",
  "text": "Can't enlarge template - and it's taken over Writer!\nHaving a weird problem. I downloaded a resume template. When I opened it up to work on it, it is small and centered in the page. I can’t increase the size - the little ruler at the top does not go all the way across, but it small and centered.\n\nI have tried to go from normal to web view, no help. I have tried to format the page, no. The print preview shows that it will print standard letter size, so it’s not that. It’s tickling in my brain that it should be simple to have the little ruler (and hence, the document) all the way across the screen, so I opened a new document to compare ...and it’s the template!!\n\nI must have made a mistake, so I try again. It’s the template. I close writer and re-open it ...to the template! I can open old documents, but all new ones are the template. Please help!\n\nScreenshot (117) 1680×1050 198 KB"
 },
 {
  "sid": "s11",
  "text": "Remember multiple window positions in windows\nin calc (and i assume writer, too) if i hold down the right crtl+shift and close the window, it remembers the window position. if i then reopen the document, the window position is saved, even upon reboot, and isn’t required again. also, the currently/last edited worksheet and cell position is also saved, regardless of ctrl+shift close.\n\nwhat i want is to be able to save the window position when i have multiple windows of the same document open - how do i do this?\n\nedit: perhaps my explanation of my question isn’t clear\n\nin calc, when i go to the Window menu and New Window, it creates a new window of the same document, where i can update the same file\n\nwhat i want, is to be able to auto-start calc and have both windows open at the same scroll position and worksheet as when it was closed\n\nis this possible via a script native to libreoffice?"
 },
 {
  "sid": "s12",
  "text": "Solved:How can extract the price info?\n\nI have this JSON string in cell A1 of a LibreOffice Calc spreadsheet:\n\nThe following REGEX formulas do not extract the price value as expected:\n\nHowever, this MID-based formula does work correctly:\n\nI would prefer a simpler expression (ideally using REGEX in a single function) that reliably extracts the price. What is the correct way to write the REGEX formula, considering proper escaping of double quotes in LibreOffice Calc?"
 }
]
