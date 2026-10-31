"""DI-TS wording: instructions, definitions (cards) and option sets, written for this project (Claude writes wording only; labels come from the sources)."""
SEED = 20261013
LE_OPTS = ["A entails B", "A does not entail B"]
LE_DEFS = {
 "A entails B": ["B is true under every assignment of true/false to the letters that makes A true.",
                 "No assignment of true/false to the letters makes A true while making B false.",
                 "Whenever A holds, B holds too, for every possible setting of the letters.",
                 "B cannot be false when A is true, whatever values the letters take."],
 "A does not entail B": ["At least one assignment of true/false to the letters makes A true and B false.",
                         "There is a way to set the letters so that A is true but B is false.",
                         "A can hold while B fails, for some setting of the letters.",
                         "B can be false even though A is true under some values of the letters."]}
LE_INSTR = [
 "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
 "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
 "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
 "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
 "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B."]

NLI_OPTS3 = ["entailment", "neutral", "contradiction"]
NLI_OPTS2 = ["entailment", "contradiction"]
NLI_DEFS = {
 "entailment": ["Statement 2 must be true whenever statement 1 is true.",
                "If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.",
                "The times in statement 1 settle that statement 2 is correct.",
                "Taking statement 1 as true, statement 2 cannot be false."],
 "contradiction": ["Statement 2 cannot be true if statement 1 is true.",
                   "The times in statement 1 rule out statement 2.",
                   "If statement 1 is true, statement 2 is guaranteed to be false.",
                   "Statement 1 and statement 2 cannot both be true."],
 "neutral": ["Statement 1 leaves open whether statement 2 is true or false.",
             "Statement 2 may be true or may be false; statement 1 does not decide it.",
             "The times in statement 1 neither confirm nor rule out statement 2.",
             "Both truth values of statement 2 are possible given statement 1."]}
CS_INSTR = {
 "cs1": [
  "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1."],
 "cs2": [
  "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1."],
 "cs3": [
  "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account."]}
PS_OPTS = ["supports", "undermines"]
PS_DEFS = {
 "supports": ["The perspective gives a reason to accept the claim.",
              "Someone who holds this perspective would be more likely to agree with the claim.",
              "The perspective argues in favour of the claim.",
              "The perspective backs the position the claim takes."],
 "undermines": ["The perspective gives a reason to reject the claim.",
                "Someone who holds this perspective would be less likely to agree with the claim.",
                "The perspective argues against the claim.",
                "The perspective works against the position the claim takes."]}
PS_INSTR = [
 "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
 "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
 "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
 "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
 "Judge the stance of the perspective toward the claim."]
