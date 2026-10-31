# Item 10 card authoring i10a_learning_4

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_learning_4.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are passages from community-written learning resources and course notes on many subjects.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: level: how much the passage assumes the learner already knows, where neighbouring answers are easy to confuse.
Card 2 angle: course role: what job the passage does inside a course, where neighbouring answers are easy to confuse.
Card 3 angle: learning purpose: what the text is meant to help a learner do, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_learning_4",
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
  "text": "Ancient Sri Lanka\nAccording to the Mahavamsa (text written in Pali of the Kings of Sri Lanka), a traditional date of ancient Sri Lanka is the landing of Vijaya, who arrived in Sri Lanka (because he was banned by King Vanga of India) with 700 followers with him and ruled Sri Lanka from 543 BC – 505 BC (Modern time now: 38 years!). Vijaya played an important role in Sri Lanka, such as the establishment of the Kingdom of Tambapanni. Vijaya played an important role in the country's ancient history.\nAnother annual date of ancient Sri Lanka is the arrival of Buddhism from Devanampiya Tissa, son of monarch Mutasiva of Anuradhapura. Though another source states that Buddhism was founded by a man named \"Mahinda\", which then integrated into Sinhalese culture. Epigraphic sources show the appearance of Buddhism around the 3rd century B.C.\nThe entire ancient period of ancient Sri Lanka is dominated by the Anuradhapura Kingdom, which includes Sri Lanka's ancient history in one place. The Sri Lanka Kingdom moved into Anuradhapura in 380 B.C.. From there onwards, the city of Anuradhapura stayed as the capital of Sri Lanka for more than 1000 years, until the fall of the kingdom in 1017 A.D., when Rajendra I sent a large invasion on the kingdom. Thus, the capital then moved to Polonnaruwa.\nAfter more than a century under Chola control, Vijayabahu I of Polonnaruwa successfully drove off the Chola Empire, thus, reuniting the country back together once again. Also, reuniting the country back in Buddhism culture too when Vijayabahu I, in request, sent monks from Burma to Sri Lanka. Though Sinhalese king Vijayabahu I was a strong leader who fought off the powerful Chola empire out of Sri Lanka, after his death, weak rulers took over after him. Eventually, Sri Lanka broke into independent states.\nThough, in 1153, a Sinhalese king named Prākramabāhu I, also called Parākramabāhu The Great, reunited Sri Lanka and repaired the irrigation systems that were made for water to be easily used in Sri Lanka. Prākramabāhu I also reformed Buddhist establishments (made new temples), and allowed Hindus to worship.\nIn the 13th century, Sri Lanka suffered from Indian invasion. The irrigation system was damaged, and the capital of Sri Lanka (Polonnuwara) was abandoned (in 1255)."
 },
 {
  "sid": "s02",
  "text": "Participants - Participants\nIf you're interested in joining the Mentoring program, add your name in the appropriate list below, along with what time zone you're in! If you like, you can add what elements of French you are either most interested in learning, or most prepared to teach.\nNote: Only those who have registered an account at Wikiversity will be kept on this list. The rest will be removed.\nAnother Note: Students who are listed in italics have been assigned a Mentor.\nA record of Mentors & Students is kept here for organizational purposes."
 },
 {
  "sid": "s03",
  "text": "Electric Field\nIn physics, an electric field or E-field is an effect produced by an Electric Charge that exerts a force on charged objects in its vicinity. The SI units of the electric field are newtons per coulomb or volts per meter (both are equivalent). Electric fields are composed of photons and contain electrical energy with energy density proportional to the square of the field intensity. In the static case, an electric field is composed of virtual photons being exchanged by the charged particle(s) creating the field. In the dynamic case the electric field is accompanied by a magnetic field, by a flow of energy, and by real photons.\nThe electric field is a vector quantity, and the electric field strength is the magnitude of this vector.\nThe mathematical definition of the electric field is developed as follows. Coulomb's law gives the force between two point charges (infinitesimally small charged objects) as\nIn the SI system of units, force is given in newtons, charge in coulombs, and distance in metres. Thus, has units of.\nThis was known empirically. Suppose one of the charges is taken to be fixed, and the other one to be a moveable \"test charge\". Note that according to this equation, the force on the test object is proportional to its charge. The electric field is defined as the proportionality constant between charge and force:\nHowever, note that this equation is only true in the case of electrostatics, that is to say, when there is nothing moving. The more general case of moving charges causes this equation to become the Lorentz equation. When we speak of a \"moveable test charge\", this means that the charge can be moved to, and held at, any position.\nFurthermore, Coulomb's law is actually a special case of Gauss's Law, a more fundamental description of the relationship between the distribution of electric charge in space and the resulting electric field. Gauss's law is one of Maxwell's equations, a set of four laws governing electromagnetics.\nAccording to Equation (1) above, the electric field is dependent on position. The electric field due to any single charge falls off as the square of the distance from that charge.\nElectric fields follow the superposition principle."
 },
 {
  "sid": "s04",
  "text": "Mathematics - The threat of extinction\nThe only possibility of escaping the threat of extinction of civilization is to attain peace in its broadest sense, in all its dimensions, that is inner peace, social peace, environmental peace and military peace.\nI see peace not as the inexistence of conflicts, since, as discussed in the beginning of this paper, every human being experiences different biological, physical, social, psychological, spiritual needs and also different wants. Since the individual and the other are different, conflicts are to be expected. The crucial point is to resolve the conflicts without violence. Violence ranges from evident confrontation and aggression and the resource of prepotency, but also in more subtle forms of arrogance and bigotry, intolerance and fanaticism.\nThe only road to peace is through conflict resolution, based on a global understanding of the life phenomenon and intermediacies created by man, which implies the acknowledgement of differences in the inter- and intra-cultural dialogue.\nA primordial ethics recognizes the mutual essentiality of the three vertices and three sides of the primordial triangle and aims at the preservation of its integrity and survival with dignity. This primordial ethics is synthesized in the box:"
 },
 {
  "sid": "s05",
  "text": "Educational Competition Optimizer - Pseudo-code of ECO Algorithm\nBelow is the simplified pseudo-code for the ECO algorithm, outlining its steps:\nIn the ECO algorithm, the optimization process begins with the random generation of a population of candidate solutions. Throughout iterative updates, ECO's search strategy explores regions near the optimal solution and adjusts each solution's position based on the current best solution. ECO is designed to maintain a balance between exploration and exploitation by introducing six different search strategies across three stages: primary school, middle school, and high school competitions, where schools and students interact at different levels to refine the search process."
 },
 {
  "sid": "s06",
  "text": "The Art of Witnessing - Introduction:\nWitnessing, as a social skill, involves the act of observing and acknowledging the experiences, emotions, and actions of others. It goes beyond mere passive observation; it encompasses an empathetic understanding of someone else's reality. The importance of witnessing lies in its ability to foster deep connections, build trust, and contribute to a supportive social environment. In this essay, we will explore what is meant by witnessing, why it is important, when it is crucial, and provide concrete suggestions on how individuals can develop and enhance this invaluable skill."
 },
 {
  "sid": "s07",
  "text": "Empirical MO methods - Explanation of the empirical MO approach\nEmpirical methods are differentiated from semi-empirical methods in general by the choice of Hamiltonian operator. Empirical methods use a Hamiltonian which is simply a sum of one-electron terms. The two-electron electron repulsion term is in effect averaged into the one-electron terms. In contrast, semi-empirical methods use the correct Hamiltonian with both one- and two-electron terms. In both cases the resulting integrals that arise from the terms in the Hamiltonian are often approximated, neglected or fitted to experimental data.\nAll the methods we will discuss, both empirical and semi-empirical, use the molecular orbital single determinant method, although, in general, this is not a restriction. The PCILO (perturbative configuration interaction using localised orbitals) method, for example, uses an approach which goes beyond the molecular orbital approach while still using the same approximations as other semi-empirical methods."
 },
 {
  "sid": "s08",
  "text": "Input and Output - Simple input\nscanf reads formatted input which means it will need the format string to function.\naddress of x to scanf. We can do that with the \"address\" operator &.\nscanf essentially uses the very same format strings as printf, see them on the top of this page."
 },
 {
  "sid": "s09",
  "text": "200 - Overview of citable references\nIn general, the most reliable sources are peer-reviewed journals and books published in university presses; university-level textbooks; magazines, journals, and books published by respected publishing houses; and mainstream newspapers. As a rule of thumb, the greater the degree of scrutiny involved in checking facts, analyzing legal issues, and scrutinizing the evidence and arguments of a particular work, the more reliable it is.\nWhere can I ask and discuss if a specific source is reliable?"
 },
 {
  "sid": "s10",
  "text": "Transformer Architecture - Model Components\nThe transformer architecture, as introduced by Vaswani et al. (2017) has two high-level components: the encoder and decoder (see Figure 1). The encoder and decoder are both composed of a series of blocks of the same design. The major sub-components of the transformer blocks are:"
 },
 {
  "sid": "s11",
  "text": "Hypomania Checklist - CSV shell for sharing\nHere is a shell data file that you could use in your own research. The variable names in the shell corresponds with the scoring code in the code for all three statistical programs.\nNote that our CSV includes several demographic variables, which follow current conventions in most developmental and clinical psychology journals. You may want to modify them, depending on where you are working. Also pay attention to the possibility of \"deductive identification\" -- if we ask personal information in enough detail, then it may be possible to figure out the identity of a participant based on a combination of variables.\nWhen different research projects and groups use the same variable names and syntax, it makes it easier to share the data and work together on integrative data analyses or \"mega\" analyses (which are different and better than meta-analysis in that they are combining the raw data, versus working with summary descriptive statistics)."
 },
 {
  "sid": "s12",
  "text": "Epistemology\nEpistemology deals with the question of how \"knowledge is acquired\" and how reliable that knowledge is. In essence, it is the theory of knowledge, and has focused on how knowledge relates to concepts such as truth, belief, and evidence. Epistemology is a very general topic and is constantly debated.\nA good place to start in the study of epistemology is the definition of \"knowledge\". A simple and old answer is \"a justified, true belief\". However, Edmund Gettier famously argued against that definition."
 }
]
