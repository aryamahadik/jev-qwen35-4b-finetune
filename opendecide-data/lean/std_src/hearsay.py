"""STD domain 'hearsay': US Federal Rules of Evidence hearsay status, FRE 801(a)-(c) only (v0.11 parts).

Each item is an invented courtroom fact pattern that ends by saying what the evidence is offered
to prove; the question asks whether the evidence is hearsay (yes/no, qtype "noul"). Coverage:
effect on the listener (notice, fear, investigation, probable cause), verbal acts and legally
operative words (offers, gifts, permission, threats, defamation, bribes, demands, forged or
false documents), impeachment, circumstantial evidence of state of mind or knowledge,
non-assertive versus assertive conduct, machine and animal output, questions and commands,
implied assertions, prior statements of a witness who testifies, and plain out-of-court
assertions offered for their truth (plus in-court testimony as clean negatives).

Exclusions and exceptions (801(d), 803, 804, 807) are never applied: the card says so, so a
party's own statement, a prior identification or a business record offered for its truth is
hearsay here. Many items come as minimal-pair twins (same facts, changed purpose, answer flips;
same group_id, meta.twin_of). All text is newly written by Claude as the teacher (no external
model, no dataset text).

Writes:
  data/v11_parts/std/hearsay.jsonl        (with gold)
  data/v11_parts/std/hearsay.blind.jsonl  (identical rows, gold removed)
Deterministic and re-runnable.
"""
import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "data" / "v11_parts" / "std"
DOMAIN = "hearsay"
SRC = f"std_{DOMAIN}"
SEED = 20261120

CARD = "\n".join([
    "- statement: a person's oral assertion, written assertion, or nonverbal conduct, if the "
    "person intended it as an assertion",
    "- declarant: the person who made the statement",
    "- hearsay: a statement that the declarant does not make while testifying at the current "
    "trial or hearing, and that a party offers in evidence to prove the truth of the matter "
    "asserted in the statement",
    "- exclusions and exceptions: not applied here; the exclusions in Rule 801(d) and the "
    "exceptions in Rules 803, 804 and 807 are ignored, so evidence that fits the definition "
    "above counts as hearsay even if it would be admissible",
])

Q = {
    0: "Is the evidence hearsay?",
    1: "Is this hearsay?",
    2: "Does the evidence meet the definition of hearsay?",
    3: "Offered for that purpose, is the statement hearsay?",
    4: "Under Rule 801, is the testimony hearsay?",
    5: "Would this evidence be classified as hearsay?",
    6: "Applying only the definition, is the evidence hearsay?",
    7: "Is the proffered evidence hearsay?",
    8: "Setting aside any exclusions or exceptions, is this hearsay?",
    9: "Hearsay status only: is the evidence hearsay?",
    10: "Is the testimony hearsay as offered?",
    11: "Does this evidence count as hearsay under the definition?",
}

HEADERS = ["", "Fact pattern:\n", "Trial record:\n", "Evidence question:\n", "Bench memo:\n"]

ITEMS = []


def T(d, gold, q, state, twin=None):
    """d: difficulty 1-3; gold: 1 = hearsay; q: key into Q or a literal question;
    twin: (edits, gold, q_or_None) where edits is a list of (old, new) replacements."""
    ITEMS.append({"d": d, "gold": gold, "q": q, "state": state, "twin": twin})


# ---------------------------------------------------------------- effect on the listener
T(2, 0, "Is Feld's account of what he told Osei hearsay?",
  '''Dana Pruitt sues Harlan Grocery after falling on the store's back staircase. Harlan's defense is that its manager, Carl Osei, had no idea anything was wrong with the stairs. Pruitt calls Omar Feld, a bread-delivery driver, who testifies that two days before the fall he told Osei, "The third step on your back stairs is cracked clean through." Photographs taken an hour after the fall show the cracked step, and Harlan does not dispute that the step was broken. Pruitt offers Feld's testimony to show that Osei had been told about the step before the fall.''',
  ([('''Photographs taken an hour after the fall show the cracked step, and Harlan does not dispute that the step was broken. Pruitt offers Feld's testimony to show that Osei had been told about the step before the fall.''',
     '''No photographs were taken, and Harlan insists the step was intact. The only disputed issue is whether the step was actually cracked, and Pruitt offers Feld's testimony on that issue.''')], 1, None))

T(2, 1, 3,
  '''Colin Marsh is on trial for assault after hitting Victor Lune with a tire iron in a parking garage; he claims he acted in self-defense. Marsh's friend Rosa Diaz testifies that a week earlier, in a bar, Lune leaned over to Marsh and said, "I've put three men in the hospital, and you're going to be the fourth." The defense asks the jury to find from Diaz's testimony that Lune really had hospitalized three men.''',
  ([('''The defense asks the jury to find from Diaz's testimony that Lune really had hospitalized three men.''',
     '''The defense offers Diaz's testimony to show why Marsh was frightened when Lune walked toward him in the garage; the jury is not asked to decide whether Lune had actually hurt anyone before.''')], 0, None))

T(2, 0, "Is the caller's statement hearsay as the prosecution uses it?",
  '''At Terrence Abel's trial for robbing a pawnshop, Detective Imani Rhodes testifies that she obtained a warrant for storage unit 14 on Keel Street, which Abel rents, after an anonymous caller, who has never been identified, told the tip line, "The guns from the pawnshop job are in unit 14 on Keel Street." The defense has told the jury that Rhodes singled out Abel's unit for no reason. The prosecutor states that the caller's words are offered to explain why Rhodes looked at that unit, and the judge instructs the jury accordingly.''',
  ([('''The defense has told the jury that Rhodes singled out Abel's unit for no reason. The prosecutor states that the caller's words are offered to explain why Rhodes looked at that unit, and the judge instructs the jury accordingly.''',
     '''The search of the unit turned up nothing. The prosecutor offers the caller's words as evidence that the stolen guns had been kept in Abel's unit, and the judge instructs the jury that it may consider them for that purpose.''')], 1, None))

T(2, 1, 0,
  '''Helen Voss is on trial for poisoning her business partner, Arthur Kline. The firm's bookkeeper testifies that a month before Kline died, he stood in Voss's office doorway and said to her, "I know you've been skimming from the company for two years." The prosecution offers the bookkeeper's testimony to prove that Voss had been skimming company money.''',
  ([('''The prosecution offers the bookkeeper's testimony to prove that Voss had been skimming company money.''',
     '''The prosecution offers the testimony to show that Voss knew Kline believed she was stealing, which it says gave her a reason to want him dead; the jury is told not to decide whether any skimming happened.''')], 0, None))

T(3, 0, "Is Senn's testimony about her phone call hearsay?",
  '''Joy Amankwah was assaulted by Rick Dace, a mover employed by Brightline Movers, while he was packing her apartment. She sues Brightline for negligently keeping Dace on staff. A former Brightline customer, Paula Senn, testifies that three months before the assault she phoned Brightline's owner and said, "Your man Dace shoved me into a wall and threatened to come back for me." Amankwah offers Senn's testimony on the question of what Brightline's owner had in fact been told about Dace before the assault.''',
  ([('''Amankwah offers Senn's testimony on the question of what Brightline's owner had in fact been told about Dace before the assault.''',
     '''Amankwah offers Senn's testimony about the call to prove that Dace did shove and threaten Senn.''')], 1, None))

T(2, 0, 5,
  '''Jamal Reyes sues Ferris Lumber, claiming he was fired because of his union organizing. Ferris says it fired him for a safety reason. Ferris's HR director testifies that the morning before the firing, a forklift supervisor, who does not testify, emailed her: "Jamal was drinking from a flask on the forklift this morning." Under the claim being tried, Ferris wins if it genuinely believed there was a safety problem, whether or not Reyes was actually drinking, and Ferris offers the email to show why the HR director believed it.''',
  ([('''Under the claim being tried, Ferris wins if it genuinely believed there was a safety problem, whether or not Reyes was actually drinking, and Ferris offers the email to show why the HR director believed it.''',
     '''Under the claim being tried, Ferris wins only if Reyes was actually drinking on the job, and Ferris offers the email to prove that he was drinking on the forklift that morning.''')], 1, None))

T(2, 0, "Is Pike's testimony about Grady's call hearsay?",
  '''Ana Pike is charged with transporting stolen electronics across state lines and raises a duress defense. She testifies that before she agreed to drive the truck, a man she knew as Grady called her and said, "My brother is parked outside your son's school right now, and he'll stay there until the truck is in Memphis." The defense offers her account of the call to show why she was afraid to refuse. Grady has never been found, and neither side argues about where his brother really was.''')

T(2, 1, "Is Odell's letter hearsay?",
  '''The Okafor family sues Delphin Heaters, claiming that a Delphin space heater's thermostat stuck on high and started a house fire. The Okafors introduce a letter that another customer, Irma Odell, mailed to Delphin's customer-service department eight months before the fire: "My heater's thermostat stuck on high and scorched my carpet." The Okafors offer the letter on the question of whether the thermostat design is defective, and the judge instructs the jury to consider it only for that purpose.''',
  ([('''The Okafors offer the letter on the question of whether the thermostat design is defective, and the judge instructs the jury to consider it only for that purpose.''',
     '''The Okafors' claim for punitive damages requires proof that Delphin was aware of complaints about the thermostat before the fire, and the letter is offered on that issue.''')], 0, None))

T(2, 0, 2,
  '''Ruben Calas sues Officer Glen Moyer for excessive force, alleging that Moyer tackled him outside Flannigan's bar without cause. Moyer testifies that seconds before the tackle, the dispatcher radioed, "Suspect outside Flannigan's is armed with a knife." The question for the jury is whether Moyer's use of force was reasonable given what he knew at that moment, and Moyer offers the dispatch for that purpose.''',
  ([('''The question for the jury is whether Moyer's use of force was reasonable given what he knew at that moment, and Moyer offers the dispatch for that purpose.''',
     '''The only question left for the jury is whether Calas actually had a knife, and Moyer offers the dispatch to prove that he did.''')], 1, None))

T(3, 0, 10,
  '''Samira Oak is charged with insurance fraud. The government says she told her insurer that her boat, the Mariposa, had been stolen from the marina when she knew her cousin had deliberately sunk it. Marina attendant Lev Aronson testifies that the morning before Oak called the insurer, he told her, "Your cousin took the Mariposa out last night and came back in a rowboat without her." The government offers Aronson's testimony to show what Oak had been told before she reported the theft. Divers located the hull, and the sinking itself is undisputed.''',
  ([('''The government offers Aronson's testimony to show what Oak had been told before she reported the theft. Divers located the hull, and the sinking itself is undisputed.''',
     '''The Mariposa has never been found, and the government offers Aronson's testimony to prove that the cousin took the boat out that night and came back without it.''')], 1, None))

T(3, 0, 7,
  '''At Leon Stroud's burglary trial, the defense suggests that the victim, Paulette Grier, invented the burglary because she waited two days before calling the police. On redirect, the prosecutor asks why she waited. Grier answers that her neighbor, who does not testify, told her, "Leon's cousins said they'd burn your house down if you called anybody." The prosecutor offers the answer to explain the two-day delay, and the jury is told not to consider whether any threat was actually made.''',
  ([('''The prosecutor offers the answer to explain the two-day delay, and the jury is told not to consider whether any threat was actually made.''',
     '''Stroud is also charged with witness tampering, and the prosecutor offers the answer to prove that Stroud's cousins made the threat.''')], 1, None))

T(2, 1, "Is Blake's testimony about the student's remark hearsay?",
  '''Kenji Wallace is accused of stealing a laptop from the Eastfield Library. Librarian Nora Blake testifies that at 3:30 p.m. a student she did not know walked up to the desk and said, "The guy in the red hoodie just put a laptop in his backpack." Blake did nothing in response and did not call security. The prosecutor offers Blake's testimony as evidence that Wallace, who wore a red hoodie that afternoon, is the one who took the laptop.''')

T(2, 0, 11,
  '''Norton Paving sues Wexley Development for its unpaid bill; Wexley counters that Norton walked off the job for no reason. Norton's foreman testifies that on May 9, Wexley's project architect came to the site and told him, "Stop pouring. The owner wants all work on the lot halted until further notice." The architect does not testify. Norton offers the architect's words to show that the foreman stopped work because the owner's representative told him to.''')

T(2, 0, "Is the cashier's statement hearsay as Chester uses it?",
  '''Donna Keel sues Chester Hardware for malicious prosecution after its security guard had her arrested for shoplifting; the charge was dropped and Chester now concedes she took nothing. The guard testifies that before he called the police, a cashier told him, "I watched that woman put two cordless drills in her tote bag." The cashier does not testify. The question on the claim is whether the guard had reasonable grounds to report Keel when he did, and Chester offers the cashier's words on that question.''')

# ---------------------------------------------------------------- verbal acts / operative words
T(1, 0, "Is Tilly's testimony about Obi's words hearsay?",
  '''Rowan Tilly sues Grace Obi for breach of contract. Tilly testifies that at the county farm auction, Obi walked up to him and said, "I'll take your red tractor for nine thousand, cash on Friday," and he answered, "Deal, it's yours." Obi admits she was at the auction but denies that any agreement was made. Tilly offers his testimony about Obi's words to establish that an offer was made and accepted.''')

T(2, 0, 4,
  '''Mei Laurent sues Dwight Carro for fraud over the pickup truck he sold her. Laurent testifies that during the test drive Carro told her, "This truck has never been in an accident." A body-shop report shows the frame had been straightened after a serious collision. Laurent's claim is that Carro made the statement, that it was false, and that she relied on it; she offers her testimony about Carro's words as proof that the representation was made.''',
  ([('''Mei Laurent sues Dwight Carro for fraud over the pickup truck he sold her.''',
     '''Mei Laurent sues her insurer, which refused to pay for frame damage to the pickup truck she bought from Dwight Carro.'''),
    ('''A body-shop report shows the frame had been straightened after a serious collision. Laurent's claim is that Carro made the statement, that it was false, and that she relied on it; she offers her testimony about Carro's words as proof that the representation was made.''',
     '''The insurer argues that the frame damage predates her policy. Laurent offers her testimony about Carro's words to prove that the truck had never been in an accident before she bought it.''')], 1, None))

T(1, 0, 1,
  '''Kyle Brandt is on trial for witness intimidation. Lorna Pace testifies that one week before she was due to testify against Brandt's brother, Brandt stopped her in a grocery-store parking lot and said, "People who talk in court tend to have accidents on icy roads." The prosecution offers the remark as the threat charged in the indictment.''')

T(2, 0, "Is the nurse's testimony hearsay?",
  '''Dr. Hollis Yuen sues a former patient, Brent Ailes, for slander. A nurse testifies that at a church picnic last June, Ailes told a group of about ten people, "Dr. Yuen was drunk when he operated on my knee." Yuen offers the nurse's testimony to prove that Ailes spoke those words to other people.''',
  ([('''Dr. Hollis Yuen sues a former patient, Brent Ailes, for slander.''',
     '''Brent Ailes sues his former surgeon, Dr. Hollis Yuen, for malpractice.'''),
    ('''Yuen offers the nurse's testimony to prove that Ailes spoke those words to other people.''',
     '''Ailes offers the nurse's testimony to prove that Yuen was drunk during the operation.''')], 1, None))

T(1, 0, 6,
  '''City building inspector Paul Nakamura is on trial for soliciting a bribe. Contractor Sergio Blanc testifies that Nakamura phoned him the day after the site inspection and said, "Ten thousand in an envelope and your permit clears Monday. Otherwise it sits on my desk till spring." The prosecution offers Blanc's testimony as proof of the solicitation charged in count one.''')

T(2, 0, 3,
  '''After Irene Castel's death, her estate sues her grandson Theo to recover a diamond brooch. Theo's wife testifies that at Christmas dinner, Irene pinned the brooch on Theo's jacket and said, "This was your great-grandmother's, and now it's yours. I want you to have it." The testimony is offered to show that Irene gave the brooch to Theo as a gift.''',
  ([('''her estate sues her grandson Theo to recover a diamond brooch.''',
     '''her grandson Theo sues the Merrow auction house over its catalogue description of a diamond brooch he consigned.'''),
    ('''The testimony is offered to show that Irene gave the brooch to Theo as a gift.''',
     '''Theo offers the testimony to prove that the brooch had belonged to his great-grandmother, which the auction house disputes.''')], 1, None))

T(2, 0, 9,
  '''Glenda Ruiz sues her neighbor Owen Platt for trespass after he drove forty head of cattle across her east pasture. Platt testifies that the previous spring Ruiz leaned on his fence and told him, "You can take your herd across the east pasture to reach the creek any time. That strip is mine, not the county's." Platt offers his testimony to show that Ruiz gave him permission to cross.''',
  ([('''Glenda Ruiz sues her neighbor Owen Platt for trespass after he drove forty head of cattle across her east pasture.''',
     '''The county sues Glenda Ruiz, claiming the strip of her east pasture along the creek is a public right-of-way, and her neighbor Owen Platt is called as a witness.'''),
    ('''Platt offers his testimony to show that Ruiz gave him permission to cross.''',
     '''Ruiz offers Platt's testimony to prove that she, and not the county, owns the strip.''')], 1, None))

T(2, 1, "Is the brochure hearsay as offered?",
  '''In the securities-fraud prosecution of Wade Lorne, the jury is shown a glossy brochure that Lorne handed to prospective investors. It reads, "Our Keystone Income Fund has returned 18 percent every year since 2015." Lorne's defense is that the fund really did earn those returns, and he offers the brochure to prove the fund's performance.''',
  ([('''Lorne's defense is that the fund really did earn those returns, and he offers the brochure to prove the fund's performance.''',
     '''The government offers the brochure to prove that Lorne made this claim to investors; its forensic accountant separately shows that the fund lost money every year.''')], 0, None))

T(2, 0, 2,
  '''Nadia Ferro sues Calder Logistics for a hostile work environment. A co-worker testifies that their shift supervisor said to Ferro in the break room, in front of six people, "Women like you only got hired here to fill a quota, and everyone knows it." Ferro offers the remark as one of the incidents of harassment she had to endure.''',
  ([('''Nadia Ferro sues Calder Logistics for a hostile work environment.''',
     '''Dale Wicke, a man rejected for a dispatcher job, sues Calder Logistics for sex discrimination.'''),
    ('''Ferro offers the remark as one of the incidents of harassment she had to endure.''',
     '''Wicke offers the co-worker's testimony to prove that Calder filled positions by a gender quota.''')], 1, None))

T(2, 0, 10,
  '''Pinecrest Homeowners Association and Verde Lawn Care dispute whether their landscaping contract was still in force in May. Pinecrest's president testifies that on April 2 she phoned Verde's owner and said, "As of today we are ending our contract with you, because your crews wrecked our sprinkler lines." Pinecrest offers her testimony to show that notice ending the contract was given on April 2.''',
  ([('''Pinecrest offers her testimony to show that notice ending the contract was given on April 2.''',
     '''Pinecrest also counterclaims for the cost of repairing the sprinklers, and on that counterclaim it offers her testimony to prove that Verde's crews damaged the lines.''')], 1, None))

T(2, 1, "Is the note hearsay?",
  '''Marcus Dell is on trial for bank robbery. The teller testifies that the robber slid a note across the counter reading, "I have a gun. Put the fifties in the bag and nobody gets hurt." No gun was seen or recovered. The prosecution offers the note on the armed-robbery count, which requires proof that the robber actually had a firearm.''',
  ([('''No gun was seen or recovered. The prosecution offers the note on the armed-robbery count, which requires proof that the robber actually had a firearm.''',
     '''The only count requires proof that the money was taken by intimidation, and the prosecution offers the note to show what the robber demanded and how.''')], 0, None))

T(3, 0, "Applying only the definition, is the consent form hearsay as offered?",
  '''Dr. Anya Moss is sued for battery by a patient who says she never agreed to have her left ovary removed. The consent form the patient signed before surgery reads: "I consent to removal of the left ovary if the surgeon finds it necessary. I have been told the risks include infection and heavy bleeding." Moss offers the form to show that the patient agreed to the procedure.''',
  ([('''Dr. Anya Moss is sued for battery by a patient who says she never agreed to have her left ovary removed.''',
     '''Dr. Anya Moss is sued by a patient who concedes she agreed to the surgery but says no one ever explained its risks.'''),
    ('''Moss offers the form to show that the patient agreed to the procedure.''',
     '''Moss offers the form to prove that the patient had been told of the risks.''')], 1, None))

T(1, 0, 7,
  '''Gavin Tull is charged with lying to federal agents. FBI Agent Lorraine Hsu testifies that when she interviewed Tull at his office, he told her, "I have never met Joel Varga and I've never done business with him." Bank records and photographs show many meetings between Tull and Varga. The government offers Hsu's testimony to prove that Tull made that statement to her.''')

T(2, 1, 0,
  '''Brody Kent sues Alma Fenn, claiming she agreed to sell him her sailboat for $12,000 and then sold it to someone else for more. Fenn says the price was never settled. A marina employee testifies that a week after Kent and Fenn met, the yacht broker who had arranged the meeting told her over coffee, "Brody and Alma settled on twelve thousand for the boat." The broker is not a party and is not called as a witness. Kent offers the employee's testimony to prove the agreed price.''')

T(2, 0, "Are the labels hearsay as offered?",
  '''Importer Dario Venn is prosecuted for selling handbags under false country-of-origin labels. Bags seized from his warehouse bear sewn-in labels that read "Hand made in Florence, Italy." A customs chemist traces the leather to a tannery in Guangzhou. The government offers the labels to show what the bags said about where they were made.''',
  ([('''Importer Dario Venn is prosecuted for selling handbags under false country-of-origin labels.''',
     '''Importer Dario Venn contests a customs duty that applies only to goods made outside the European Union.'''),
    ('''A customs chemist traces the leather to a tannery in Guangzhou. The government offers the labels to show what the bags said about where they were made.''',
     '''Venn offers the labels to prove that the bags were made in Florence.''')], 1, None))

T(1, 0, 6,
  '''Keith Dorn is on trial for stalking his former girlfriend, Tamsin Rowe. The prosecution introduces forty text messages Dorn sent Rowe over three weeks, including "I know where you park now" and "Watched you leave the gym tonight. Nice jacket." The stalking statute makes it a crime to send repeated messages that would cause a reasonable person to fear for her safety, and the prosecution offers the texts as the messages that make up the offense.''')

# ---------------------------------------------------------------- impeachment
T(1, 0, 0,
  '''In a car-crash trial, eyewitness Hector Blum testifies that the defendant drove through a red light. On cross-examination, defense counsel shows Blum an email he sent his sister the evening of the crash: "I didn't really see the light, I was looking at my phone." Counsel offers the email to show that Blum has given a different account, so the jury can decide how much to trust his testimony; the judge instructs the jury to use it only for that purpose.''',
  ([('''Counsel offers the email to show that Blum has given a different account, so the jury can decide how much to trust his testimony; the judge instructs the jury to use it only for that purpose.''',
     '''Counsel asks the jury to treat the email as proof that Blum never saw the light at all.''')], 1, None))

T(2, 1, "Is the cellmate's testimony about Doucet's remark hearsay?",
  '''At Tessa Kuhn's heroin-distribution trial, informant Ray Doucet testifies that Kuhn sold him heroin on three occasions. The defense calls Doucet's former cellmate, who testifies that Doucet told him in jail, "Kuhn never sold me anything. I'm just giving the cops a name so I get out sooner." In closing, the defense argues that the cellmate's testimony proves no sale ever took place.''',
  ([('''In closing, the defense argues that the cellmate's testimony proves no sale ever took place.''',
     '''The defense offers the cellmate's testimony solely to show that Doucet has told conflicting stories, and the jury is instructed that it may not treat the jailhouse remark as evidence of what happened.''')], 0, None))

T(2, 0, 11,
  '''In a slip-and-fall case against Marlow Foods, the plaintiff's friend Ines Carvalho testifies that she saw no warning cone near the spilled yogurt. Marlow then calls its store manager, who testifies that right after the fall Carvalho told him, "There was a yellow cone right beside the spill." The judge limits the manager's testimony to the question of whether Carvalho is a believable witness.''',
  ([('''The judge limits the manager's testimony to the question of whether Carvalho is a believable witness.''',
     '''Marlow does not challenge Carvalho's credibility; it offers the manager's testimony only to prove that a warning cone was in place beside the spill.''')], 1, None))

T(3, 1, 8,
  '''In a wrongful-termination trial, the plaintiff's former supervisor, Lyle Dorsey, testifies that she was fired for missing shifts. The plaintiff then reads to the jury a passage from Dorsey's deposition, given under oath in this case a year earlier: "She was let go because she kept complaining about the safety violations." The plaintiff offers the passage as proof of the real reason she was fired, and the judge instructs the jury that it may consider it for that purpose.''',
  ([('''The plaintiff offers the passage as proof of the real reason she was fired, and the judge instructs the jury that it may consider it for that purpose.''',
     '''The plaintiff offers the passage to show that Dorsey's account has changed, and the jury is told it may use the passage only in weighing his credibility.''')], 0, None))

T(2, 0, "Leaving aside Rule 801(d), is the note hearsay?",
  '''Paul Kerrigan, on trial for setting fire to a warehouse at 2 a.m., testifies that he was at home asleep all night. On cross-examination, the prosecutor shows him a note he left for his landlord the next morning: "Sorry about the noise. I was out till dawn and locked myself out again." The prosecutor offers the note to show that Kerrigan's testimony conflicts with what he wrote, and the court limits it to that use.''',
  ([('''The prosecutor offers the note to show that Kerrigan's testimony conflicts with what he wrote, and the court limits it to that use.''',
     '''The prosecutor offers the note to prove that Kerrigan was out of his home until dawn.''')], 1, None))

T(3, 1, "Is the textbook passage hearsay as used?",
  '''In a malpractice trial over a patient with kidney disease who was given 60 mg of the drug Veltrazine, the defense expert testifies that the dose was safe. On cross-examination, plaintiff's counsel reads a passage from a pharmacology textbook: "Doses above 40 mg are dangerous for patients with reduced kidney function." Counsel asks the jury to accept the passage as proof that the dose was dangerous.''',
  ([('''Counsel asks the jury to accept the passage as proof that the dose was dangerous.''',
     '''Counsel reads it to test whether the expert knows the standard literature, and the jury is told not to treat the passage as proof of a safe or unsafe dose.''')], 0, None))

T(2, 0, 10,
  '''Cyclist Ilse Varga sues Hollin Freight, testifying that the Hollin truck that hit her never signaled before turning. Hollin introduces a claim form Varga filed with her own insurer two days after the crash, where she wrote, "Truck signaled right, then swung left into me." Hollin offers the form to help the jury judge whether Varga's trial account can be believed, and the court gives a limiting instruction.''',
  ([('''Hollin offers the form to help the jury judge whether Varga's trial account can be believed, and the court gives a limiting instruction.''',
     '''Hollin offers the form to prove that the driver actually signaled, and the court declines to limit it to credibility.''')], 1, None))

T(2, 1, 4,
  '''Rafe Cordero's girlfriend, June Tallis, testifies at his trial that he was with her at a movie until midnight on the night of the shooting. The prosecution calls Detective Ames, who testifies that during the investigation Tallis told him, "He dropped me at home at eight and drove off." The prosecution offers Tallis's statement to prove that Cordero was not with her after eight.''',
  ([('''The prosecution offers Tallis's statement to prove that Cordero was not with her after eight.''',
     '''The prosecution offers Tallis's statement only to impeach her, and the judge tells the jury it may not use the statement to decide where Cordero actually was.''')], 0, None))

T(3, 1, 7,
  '''In a tax-fraud trial, the government never calls accountant Neil Ostrow as a witness. Instead, FBI Agent Kim testifies that Ostrow told him, "Harlan ordered me to backdate the invoices." The defendant, Harlan, does not testify. The government calls the statement "impeachment" of the defense theory and asks the jury to conclude from it that Harlan gave the order.''')

T(2, 0, 3,
  '''At Carl Remy's assault trial, his neighbor Doug Pratt testifies for the prosecution that he saw Remy throw the first punch. The defense calls Pratt's ex-wife, who testifies that last year Pratt told her, "Carl Remy ruined my life, and I'm going to make him pay for it." The defense offers the remark to show that Pratt is biased against Remy.''')

# ---------------------------------------------------------------- state of mind / knowledge
T(3, 0, "Is Amy's description to the detective hearsay?",
  '''Julian Reese is charged with kidnapping nine-year-old Amy Lund, who says she was kept for two days in a basement room. Before police took her anywhere near Reese's building, Amy told a detective that the room had "a green couch, a fish tank with one orange fish, and a lighthouse poster over the bed." Police later found exactly those items in Reese's basement apartment. The prosecution offers Amy's description to show that she knew what Reese's apartment looked like, knowledge she could have gained only by being inside it.''',
  ([('''Police later found exactly those items in Reese's basement apartment. The prosecution offers Amy's description to show that she knew what Reese's apartment looked like, knowledge she could have gained only by being inside it.''',
     '''The search of Reese's apartment was suppressed, so there is no evidence of what it contains. The prosecution offers Amy's description to prove what was in the room where she was held.''')], 1, None))

T(1, 0, 1,
  '''Hal Ruston pleads not guilty by reason of insanity to assaulting a mail carrier. His brother testifies that the week before the assault, Ruston told him, "The mail carriers are Martian scouts. I'm the only one who can see their antennae, and they know it." The defense offers the brother's testimony as evidence of Ruston's mental condition.''')

T(2, 0, 9,
  '''Lana Birch is on trial for a hit-and-run on the night of March 3. Officer Tate questioned her the next day, and she told him, "I was at my sister's in Dayton all weekend and never touched the car." Toll records show her car crossing the Harlow Bridge that night. At trial, the prosecution calls Tate to repeat the statement and offers it to show that she lied to the police, which it argues reflects a guilty conscience.''',
  ([('''At trial, the prosecution calls Tate to repeat the statement and offers it to show that she lied to the police, which it argues reflects a guilty conscience.''',
     '''At trial, Birch's lawyer calls Tate as a defense witness to repeat the statement and offers it only to prove that Birch was at her sister's in Dayton that night.''')], 1, None))

T(3, 1, 3,
  '''The estate of Eli Crane sues a scaffolding contractor after a scaffold collapsed on Crane. The contractor claims a falling beam struck Crane's head and killed him instantly. A co-worker testifies that about two minutes after the collapse he heard Crane shout from under the debris, "My legs are pinned, I can't feel my legs!" The estate offers the shout to prove that the beam landed across Crane's legs, which matters to its engineer's reconstruction of the collapse.''',
  ([('''The estate offers the shout to prove that the beam landed across Crane's legs, which matters to its engineer's reconstruction of the collapse.''',
     '''The estate's claim for pain and suffering depends on whether Crane was conscious after the collapse, and it offers the shout to show that he was alive and aware.''')], 0, None))

T(2, 0, 0,
  '''Ana Kovac is charged with making false statements on an English-language customs declaration; her defense is that she cannot read or speak English and did not understand the form. A customs officer testifies that in the arrivals hall he overheard Kovac on the phone saying, in fluent English, "The flight was two hours late, but I'll be at the hotel by ten." The prosecution offers the testimony to show that Kovac speaks English.''',
  ([('''her defense is that she cannot read or speak English and did not understand the form.''',
     '''her defense is that she filled in the form carelessly because her flight was badly delayed and she was rushing to make a connection.'''),
    ('''The prosecution offers the testimony to show that Kovac speaks English.''',
     '''The defense offers the officer's testimony for one purpose only: to prove that Kovac's flight really was two hours late.''')], 1, None))

T(2, 0, 5,
  '''Bramble Coffee sues the owners of a new cafe called Brambell Brew for trademark infringement, claiming customers confuse the two. A Bramble barista testifies that in the month after Brambell Brew opened, at least a dozen customers said to her things like, "Love your new location on Fifth Street!" The customers do not testify. Bramble has no location on Fifth Street; Brambell Brew does. Bramble offers the remarks to show that customers believed the two businesses were connected.''')

T(2, 0, "Is the housekeeper's testimony hearsay?",
  '''In a will contest, Corinne Abbot claims that her father's nephew pressured him into leaving her nothing. The father's housekeeper testifies that a year before he died, he told her, "My nephew is the only one who ever visits. Corinne hasn't called me in ten years." The nephew offers the testimony to show how the father felt about his daughter when he made his will; Corinne's phone habits are not in issue.''',
  ([('''The nephew offers the testimony to show how the father felt about his daughter when he made his will; Corinne's phone habits are not in issue.''',
     '''The only issue the nephew raises with it is whether Corinne actually stopped calling, and he offers the testimony to prove that she had not called her father in ten years.''')], 1, None))

T(2, 1, 8,
  '''Rex Hollister is on trial for murdering his wife, Dana. The defense claims Dana took an overdose on her own; the prosecution wants to show she was afraid of Rex. Dana's sister testifies that two weeks before Dana died, Dana told her, "I'm terrified of Rex. I lock the bedroom door every night." The prosecution offers the testimony to prove that Dana was afraid of Rex.''')

T(2, 1, 2,
  '''In a wrongful-death suit over a highway crash near Tulsa, the defense claims the driver killed in the crash was not Martin Greer, whose family is suing, but a hitchhiker who had taken his truck. Greer's roommate testifies that the night before the crash, Greer told him, "I'm driving to Tulsa tomorrow to pick up my daughter." The family offers the roommate's testimony as evidence that Greer did go to Tulsa and was the driver.''')

T(2, 0, "Leaving aside Rule 801(d), is the neighbor's testimony hearsay?",
  '''In a negligent-entrustment suit, the plaintiff claims Ross Pell lent his pickup to his nephew knowing its brakes were bad. It is conceded that the nephew's crash was caused by brake failure. A neighbor testifies that the day before the crash, Pell told her, "The brakes on that truck are shot. I wouldn't drive it to the corner." The plaintiff offers the remark to show that Pell was aware of the brake problem when he handed over the keys.''',
  ([('''It is conceded that the nephew's crash was caused by brake failure.''',
     '''Pell's defense is that the brakes were fine and the nephew was speeding.'''),
    ('''The plaintiff offers the remark to show that Pell was aware of the brake problem when he handed over the keys.''',
     '''The plaintiff offers the remark to prove that the brakes were actually defective, which is the only contested issue.''')], 1, None))

T(3, 0, "Leaving aside Rule 801(d), is the assistant's testimony about Venn's remark hearsay?",
  '''Executive Carla Venn is charged with insider trading for selling her company stock on June 3. The company's announcement on June 10 that it was closing its Akron plant is not disputed. Her assistant testifies that on June 1, Venn said to her, "Keep this quiet, but Akron is closing next month." The government offers the assistant's testimony to show that Venn was aware of the closing before she sold.''',
  ([('''The company's announcement on June 10 that it was closing its Akron plant is not disputed.''',
     '''The company denies that any decision about its Akron plant had been made by early June.'''),
    ('''The government offers the assistant's testimony to show that Venn was aware of the closing before she sold.''',
     '''The government offers the assistant's testimony to prove that the decision to close Akron had already been made by June 1.''')], 1, None))

T(2, 0, 10,
  '''Rita Fong sues Harbor Mutual for refusing to pay her claim for stolen jewelry. Harbor's defense is that no burglary happened and the claim was made up. The claim form Fong signed states, "On May 14 my house was broken into and my grandmother's pearls and two gold bracelets were taken." Harbor offers the form as the very claim it says Fong made up.''',
  ([('''Harbor offers the form as the very claim it says Fong made up.''',
     '''Fong offers the form herself to prove that the burglary happened and the jewelry was taken.''')], 1, None))

T(2, 0, 4,
  '''Ellis Waite is on trial for murdering a convenience-store clerk. Police never released to the public that the clerk's wrists had been bound with orange nylon rope. Waite's former roommate testifies that two days after the killing, before any arrest, Waite told her, "They tied that clerk up with orange rope, you know." The rope itself was photographed at the scene. The prosecution offers the roommate's testimony to show that Waite knew a detail that only someone involved in the killing would know.''')

T(2, 0, 7,
  '''Walter Briggs, 61, sues Tolland Insurance for age discrimination after he was passed over for a regional manager job. A former HR assistant testifies that at the meeting where the promotion was decided, Tolland's vice president said, "We need younger faces out front; our clients don't want to see grandpa." The vice president is not called as a witness. Briggs offers the remark to show the vice president's attitude toward older employees when he made the promotion decision.''')

# ---------------------------------------------------------------- conduct
T(2, 1, "Is the clerk's pointing hearsay?",
  '''Darnell Owens is on trial for robbing a gas station. The clerk, whose jaw was broken in the robbery and who has since died of unrelated causes, was asked by Officer Pratt at the hospital, "Is the man who robbed you in this photo lineup?" The clerk pointed to Owens's photograph. Officer Pratt testifies to the pointing, which the prosecution offers to prove that Owens was the robber.''',
  ([('''Darnell Owens is on trial for robbing a gas station.''',
     '''The robbery charge against Darnell Owens was dismissed, and Owens now sues Officer Pratt for arresting him without probable cause.'''),
    ('''Officer Pratt testifies to the pointing, which the prosecution offers to prove that Owens was the robber.''',
     '''Pratt testifies to the pointing to show what information he had when he arrested Owens; Owens's guilt is not an issue in this suit.''')], 0, None))

T(2, 0, "Is the evidence of the captain's conduct hearsay?",
  '''After the ferry Saltmarsh sank in a storm, families of passengers sue its owner, claiming it was unseaworthy. A dockhand testifies that on the morning of the voyage, the captain, who had thirty years' experience and died in the sinking, spent an hour inspecting the hull and then brought his wife and two children aboard for the crossing. The owner offers the captain's conduct to show that the ferry appeared seaworthy.''',
  ([('''The owner offers the captain's conduct to show that the ferry appeared seaworthy.''',
     '''The owner also offers the captain's logbook entry from that morning, "Hull inspected, sound," to prove that the ferry was seaworthy.''')], 1, "Is the logbook entry hearsay?"))

T(1, 0, 1,
  '''In a crash case, the defendant says it was pouring rain at 5:10 p.m., which is why she could not see the cyclist. She calls a newsstand owner who testifies that at about 5:10 he saw people on Main Street opening umbrellas, pulling jackets over their heads, and running into doorways. The defendant offers the testimony to prove it was raining.''')

T(1, 0, 6,
  '''When officers knocked on the door of Tyrell Banks's apartment with a search warrant, a neighbor saw Banks climb out the back window, drop into the alley, and run. At Banks's drug trial, the neighbor testifies to what she saw, and the prosecution offers the testimony as evidence of Banks's consciousness of guilt.''')

T(3, 0, 2,
  '''Harbor Grill is sued by a diner who says the grill's raw oysters gave him norovirus on the night of August 9. The grill's manager testifies that 312 other diners ate oysters from the same batch that night and that the restaurant received no complaints or reports of illness from any of them. The grill offers the testimony as evidence that the oysters were not contaminated.''')

T(2, 1, 0,
  '''Ray Kessel was struck by a vehicle and died two days later without regaining the ability to speak. A nurse testifies that in the emergency room she asked him, "Was it the blue pickup that hit you?" and Kessel nodded twice. Kessel's estate, which is suing the owner of a blue pickup, offers the nurse's testimony to prove that the blue pickup struck Kessel.''')

T(2, 1, "Are the two taps hearsay as offered?",
  '''Home-invasion trial of Silas Grant. At 2:14 a.m., homeowner Leah Moss, hiding in a closet, called 911 but was too frightened to speak. The dispatcher said, "If the intruder is still in the house, tap twice on the phone." The recording captures two taps. Moss has since moved abroad and will not testify. The prosecution offers the recording to prove that the intruder was still in the house at 2:14.''',
  ([('''Home-invasion trial of Silas Grant.''', '''Murder trial of Silas Grant.'''),
    ('''Moss has since moved abroad and will not testify. The prosecution offers the recording to prove that the intruder was still in the house at 2:14.''',
     '''Moss was later found dead in the house, and the time of her death is disputed. The prosecution offers the recording to show that she was alive and conscious at 2:14.''')], 0, None))

T(2, 1, 4,
  '''At Luis Ferrante's trial for assaulting a six-year-old girl at a playground, the girl does not testify. Officer Dana Ruiz testifies that when she asked the girl what the man did, the girl took hold of the officer's upper arm, twisted it hard, and pulled it toward the bushes. The prosecution offers the officer's description of the girl's demonstration to prove how the man grabbed her.''')

T(3, 0, "Is the technician's account of the doctor's actions hearsay?",
  '''In a life-insurance dispute, the insurer claims that Paul Varek died of a heart attack caused by a condition he concealed, not an accident. An ER technician testifies that when Varek was brought in, the attending doctor immediately put him on a cardiac monitor, ordered clot-busting drugs, and paged the cardiology team. The insurer offers the technician's testimony as evidence that Varek was having a heart attack.''',
  ([('''The insurer offers the technician's testimony as evidence that Varek was having a heart attack.''',
     '''The insurer also offers the doctor's chart note, "Impression: acute myocardial infarction," as evidence that Varek was having a heart attack; the doctor does not testify.''')], 1, "Is the chart note hearsay?"))

T(2, 0, "Is the trucker's testimony about the other drivers hearsay?",
  '''Lena Park sues the state, claiming the Carver Creek bridge was iced over and should have been salted. A trucker who was behind Park testifies that just before her crash, he watched the three cars ahead of her slow to a crawl as they reached the bridge and creep across in the right lane. Park offers the trucker's testimony to show that the drivers ahead of her perceived ice on the bridge.''',
  ([('''Park offers the trucker's testimony to show that the drivers ahead of her perceived ice on the bridge.''',
     '''Park also offers the incident report of a state trooper, who does not testify, reading, "Bridge deck iced over at time of crash," to prove that the bridge was icy.''')], 1, "Is the trooper's report hearsay?"))

T(3, 1, 8,
  '''Patient Harriet Olsen sues Dr. Owen Vance, claiming he never explained the risks of her spinal surgery. A nurse testifies that before the surgery, she asked Olsen, "Did Dr. Vance go over the risks with you?" and Olsen nodded. Dr. Vance offers the nurse's testimony to prove that he had explained the risks.''',
  ([('''Patient Harriet Olsen sues Dr. Owen Vance, claiming he never explained the risks of her spinal surgery.''',
     '''Patient Harriet Olsen sues Dr. Owen Vance, claiming she was too sedated to give valid consent to her spinal surgery.'''),
    ('''Dr. Vance offers the nurse's testimony to prove that he had explained the risks.''',
     '''Dr. Vance offers the testimony to show that Olsen was alert and able to respond to questions at that moment.''')], 0, None))

T(2, 1, 9,
  '''In a civil case about the disappearance of teenager Colby Ruhl, the question is where he was last seen. Detective Ana Brill testifies that when she asked Colby's aunt, who now lives overseas and is not a witness, where she last saw him, the aunt said nothing but put her finger on the corner of Fifth and Alder on a city map. The detective's testimony is offered to prove that Colby was last seen at Fifth and Alder.''')

# ---------------------------------------------------------------- machines and animals
T(2, 0, 0,
  '''At Owen Grady's drunk-driving trial, the evidence is that the Intoxilyzer 9000 at the station measured his breath sample and automatically printed "0.14 g/210L" with a date and time stamp; no person typed or entered the number. The prosecution offers the printout to prove Grady's breath-alcohol level.''',
  ([('''The prosecution offers the printout to prove Grady's breath-alcohol level.''',
     '''The printout was later lost, so the prosecution offers a form on which Trooper Reyes, who does not testify, copied the result by hand ("Subject blew 0.14") to prove Grady's breath-alcohol level.''')], 1, None))

T(2, 0, 1,
  '''Jerry Voss is on trial for making harassing phone calls to his ex-wife. The prosecution offers a screenshot of her phone's call log, generated automatically by the phone and the carrier's network, showing an incoming call at 11:52 p.m. from Voss's number. The screenshot is offered to prove that a call came from Voss's number at that time.''',
  ([('''The prosecution offers a screenshot of her phone's call log, generated automatically by the phone and the carrier's network, showing an incoming call at 11:52 p.m. from Voss's number. The screenshot is offered to prove that a call came from Voss's number at that time.''',
     '''Her roommate answered the phone that night and wrote on the kitchen whiteboard, "11:52 - Jerry called AGAIN." The roommate has moved away and cannot be found. The prosecution offers a photo of the whiteboard to prove that Voss called at 11:52.''')], 1, None))

T(1, 0, 5,
  '''At Nico Salas's cocaine-trafficking trial, the prosecution wants to show that his car's trunk had held drugs. Officer Hale testifies that he watched his trained drug dog, Rook, circle the car and sit down beside the trunk, which is Rook's trained signal for narcotics odor.''',
  ([('''Officer Hale testifies that he watched his trained drug dog, Rook, circle the car and sit down beside the trunk, which is Rook's trained signal for narcotics odor.''',
     '''Officer Hale, the dog's handler, is on medical leave and does not testify. Instead, the prosecution offers his K-9 log entry: "Rook gave positive final response at trunk of suspect vehicle."''')], 1, None))

T(2, 0, 11,
  '''Anton Weir is on trial for violating a protective order by going within 500 feet of his ex-partner's home on April 12. The prosecution offers a data report from Weir's GPS ankle monitor, recorded and stored automatically by the device and the vendor's server, showing the monitor at 41 Birch Street, next door to her house, from 9:02 to 9:40 p.m. The report is offered to prove where Weir was.''',
  ([('''The prosecution offers a data report from Weir's GPS ankle monitor, recorded and stored automatically by the device and the vendor's server, showing the monitor at 41 Birch Street, next door to her house, from 9:02 to 9:40 p.m. The report is offered to prove where Weir was.''',
     '''The GPS data was overwritten, so the prosecution offers an email from Weir's probation officer, who does not testify, stating, "Weir's monitor showed him next door to her house from 9 to 9:40 on the 12th," to prove where Weir was.''')], 1, None))

T(2, 1, 7,
  '''In a suit between the Delmar Warehouse and a trucking company over missing cargo, the key question is when Van 7 left the loading dock. The warehouse offers the night guard's handwritten shift log, which reads, "Van #7 left Dock 3, 2:40 a.m." The guard quit months ago and does not testify. The log is offered to prove that the van left at 2:40.''',
  ([('''The warehouse offers the night guard's handwritten shift log, which reads, "Van #7 left Dock 3, 2:40 a.m." The guard quit months ago and does not testify. The log is offered to prove that the van left at 2:40.''',
     '''The warehouse offers a still image from its security camera, which automatically stamps each frame with the time; the frame showing Van 7 leaving Dock 3 is stamped 2:40:17 a.m. The image is offered to prove that the van left at 2:40.''')], 0, None))

T(2, 1, "Is the recording of the man's words hearsay?",
  '''After a gas explosion destroyed a house on Lark Lane, the homeowner sues the gas utility. The homeowner offers a recording from a neighbor's video doorbell, which captured a man in a utility vest saying at the neighbor's door, "Gas company. There's a leak next door, everybody needs to get out." The man has never been identified. The recording is offered to prove that gas was leaking next door before the explosion.''',
  ([('''The recording is offered to prove that gas was leaking next door before the explosion.''',
     '''The homeowner also offers the doorbell's automatic motion log, which recorded "Motion detected 18:07:32" when the man approached, to prove what time he arrived.''')], 0, "Is the motion-log entry hearsay?"))

T(1, 0, 3,
  '''At Wade Hurst's burglary trial, a sheriff's deputy testifies that she gave her bloodhound, Juno, the scent of a glove dropped at the broken window, and that Juno followed a trail four blocks and stopped, baying, at Hurst's back door. The prosecution offers the deputy's testimony as evidence that the person who dropped the glove went to Hurst's house.''')

T(2, 0, 6,
  '''In a fraud trial, the prosecution must show that the victim's stolen bank card was used at a particular machine. It offers the bank's ATM transaction log, which the ATM's software generated automatically at the moment of the withdrawal, showing the card number, "$400," "Elm St. ATM 2," and "21:12:05." No person entered any part of the record. The log is offered to prove when and where the card was used.''')

T(1, 0, 10,
  '''At a traffic trial, Officer Ben Liu testifies that his radar unit, which he had tested with tuning forks at the start of his shift, displayed "67" as Tanya Morrow's car passed through the 45 mph zone. The state offers the displayed reading as evidence of Morrow's speed.''')

T(2, 0, 0,
  '''Rider Clare Nguyen sues a stable, claiming a strand of loose wire fencing had been left across the riding trail and caused her fall. Another rider testifies that earlier that morning, at the exact bend where Nguyen later fell, his normally calm horse stopped dead, snorted, and refused to go forward until he dismounted and led it around. The testimony is offered as evidence that something was lying across the trail at the bend.''')

T(2, 1, "Is the extracted text message hearsay?",
  '''At Omar Diallo's smuggling trial, a forensic examiner used extraction software on a phone seized from a co-defendant who has since fled. The software's report lists a text message sent from that phone at 6:04 a.m. on March 2: "The shipment is at Dock 9 under the blue tarp." The prosecution offers the extracted text to prove that the shipment was at Dock 9.''')

T(2, 1, 2,
  '''In a dispute over an unpaid invoice, Kestrel Builders offers a transcript produced automatically by Hollis Supply's voicemail-to-text system. The transcript reads: "Hi, it's Priya from Kestrel Builders. Just letting you know we paid the Hollis invoice this morning by wire." Priya is not called as a witness. Kestrel offers the transcript to prove that it paid the invoice.''')

# ---------------------------------------------------------------- questions and commands
T(2, 1, 3,
  '''Carpenter Jose Pinto lost two fingers on a table saw and sues the saw's manufacturer, claiming a defective latch let the blade guard pop off during his cut. A co-worker testifies that just before the injury, the site foreman shouted to Pinto, "Stop the saw now, the blade guard is off!" The manufacturer offers the co-worker's testimony to prove that the guard was already off before Pinto started cutting.''',
  ([('''The manufacturer offers the co-worker's testimony to prove that the guard was already off before Pinto started cutting.''',
     '''The manufacturer offers the testimony to show that Pinto kept cutting after his foreman ordered him to stop, which it argues makes him partly at fault.''')], 0, None))

T(1, 0, "Is the nurse's question hearsay?",
  '''A patient suffered a severe reaction to penicillin at the Marston Clinic and sues for negligence, claiming nobody asked about allergies. A clinic receptionist testifies that she heard the nurse ask the patient, "Are you allergic to penicillin or any other medicine?" The clinic offers the receptionist's testimony to show that the nurse asked about allergies.''',
  ([('''The clinic offers the receptionist's testimony to show that the nurse asked about allergies.''',
     '''The receptionist also heard the patient answer, "No, never had a problem with any of them," and the clinic offers that answer to prove that the patient had no known allergy.''')], 1,
   "Setting aside any exclusions or exceptions, is the patient's answer hearsay?"))

T(2, 0, "Leaving aside Rule 801(d), is the email hearsay?",
  '''Rourke Health's billing director, Evan Sayle, is on trial on two counts. His assistant testifies that Sayle sent her an email reading, "Shred all the Kessler billing files before Friday. They show we double-billed Medicare." On the obstruction count, the prosecution offers the email to show that Sayle instructed her to destroy records.''',
  ([('''On the obstruction count, the prosecution offers the email to show that Sayle instructed her to destroy records.''',
     '''On the fraud count, the prosecution offers the email to prove that Rourke double-billed Medicare.''')], 1, None))

T(1, 0, 7,
  '''Tenants of the Alder Court apartments sue their landlord over a fire. The landlord claims the tenants abandoned their units without trying to put out the fire, which let it spread. A tenant testifies that when she called 911 about smoke in the hallway, the dispatcher told her, "Get everyone out of the building and wait across the street." The dispatcher does not testify. The testimony is offered to show why the tenants left the building.''')

T(2, 1, 10,
  '''In an eviction case, landlord Victor Haines claims tenant Marisol Duque never paid October's rent. Duque's neighbor testifies that in mid-October she heard Duque shout at Haines in the hallway, "How many times do I have to tell you I paid October on the first?" Duque offers the neighbor's testimony to prove that she paid October's rent on the first.''',
  ([('''In an eviction case, landlord Victor Haines claims tenant Marisol Duque never paid October's rent.''',
     '''Tenant Marisol Duque sues landlord Victor Haines for harassment, claiming he kept sending late-fee notices after she had disputed them; her October payment is conceded.'''),
    ('''Duque offers the neighbor's testimony to prove that she paid October's rent on the first.''',
     '''Duque offers the testimony to show that Haines had been told of her position before he sent the November late-fee notice.''')], 0, None))

T(2, 0, 5,
  '''Pedestrian Olga Ferrin, struck by a Marchetti Bakery delivery van, sues the bakery. The bakery says the driver was on a personal errand, outside his job. The driver's co-worker testifies that an hour before the crash the bakery manager told the driver, "Take the company van, the shop fixed its brakes yesterday, and pick up the pastries for the Harper order." Ferrin offers the testimony to show that the driver was on a job assignment when he hit her.''',
  ([('''The bakery says the driver was on a personal errand, outside his job.''',
     '''The bakery concedes the driver was working, but Ferrin claims the van's brakes had never been repaired.'''),
    ('''Ferrin offers the testimony to show that the driver was on a job assignment when he hit her.''',
     '''The bakery offers the co-worker's testimony to prove that the brakes had been repaired the day before.''')], 1, None))

T(2, 0, 6,
  '''Brenner Tile sues homeowner Lucy Dahl for $4,000. The contract requires a written demand for payment before any suit may be filed, and Dahl says no demand was ever sent. Brenner offers a letter its lawyer sent Dahl on February 2: "You owe Brenner Tile $4,000 for the kitchen job. Pay by March 1 or we will sue." The letter is offered to show that the required demand was made before suit.''',
  ([('''The contract requires a written demand for payment before any suit may be filed, and Dahl says no demand was ever sent.''',
     '''Dahl concedes she received a demand but denies owing anything, saying the job was paid in cash.'''),
    ('''The letter is offered to show that the required demand was made before suit.''',
     '''The letter is offered to prove that Dahl owes Brenner $4,000.''')], 1, None))

T(3, 0, 0,
  '''Carla Rios is charged with child neglect for leaving her two-year-old son alone in their apartment for an evening. A neighbor testifies that at about 7 p.m. she heard the boy through the wall, crying, "Mama? Mama, where are you?" for nearly an hour. The prosecution offers the neighbor's testimony as evidence that the child was alone in the apartment.''')

T(1, 0, 8,
  '''At the trial of Dante Ruiz for robbing a jewelry store, a customer testifies that a masked man came through the door and shouted, "Everybody on the floor, hands where I can see them! Nobody moves!" The robbery statute requires proof that property was taken by force or threat, and the prosecution offers the testimony to prove that element.''')

T(2, 1, 0,
  '''At Kyle Moreno's trial for a Friday-night burglary in Sparks, Nevada, the defense offers a text message that Moreno's friend Tariq, who is not testifying, sent to Moreno's brother on Sunday: "Why'd you tell the cops I was with Kyle Friday night when Kyle and me were at the casino in Reno the whole time?" The defense offers the text to prove that Moreno was at the casino in Reno that night.''')

# ---------------------------------------------------------------- implied assertions and non-truth uses
T(3, 0, 2,
  '''After arresting Lamar Pike, agents kept his cell phone. Over the next hour it rang six times, and an agent answered each call. Each caller asked some version of "You still got the same stuff? I need two bags, same place as last time." The callers were never identified and do not testify. At Pike's drug-distribution trial, the agent testifies to the calls, and the prosecution offers them as evidence that Pike's phone was being used to take drug orders.''')

T(3, 1, 4,
  '''In a dispute over farm rent, landowner Walter Hesse claims the south field rent for 2023 was never paid. That fall, his tenant Gunnar Moll wrote to Walter: "Dear Walter, I've paid the south field rent for this year in full. What do you advise about planting soybeans there next spring? You know that ground better than anyone." Moll offers the letter to prove that he paid the 2023 rent.''',
  ([('''In a dispute over farm rent, landowner Walter Hesse claims the south field rent for 2023 was never paid.''',
     '''After Walter Hesse's death, his children challenge a will he signed in late 2023, claiming he could no longer manage his affairs.'''),
    ('''Moll offers the letter to prove that he paid the 2023 rent.''',
     '''The will's supporters offer the letter as evidence that Walter was still capable of managing his affairs, since Moll wrote to him for advice as one would to a capable landlord; whether the rent was paid is irrelevant to the will contest.''')], 0, None))

T(3, 0, 11,
  '''Ethan Bloch's car crossed the center line and hit Mara Lind's car. Lind claims Bloch had a seizure disorder and should not have been driving. Bloch's neighbor testifies that the morning of the crash she heard Bloch's father call out as Bloch left the house, "Don't forget your seizure pills before you drive!" Bloch's father is not called as a witness. Lind offers the testimony to show that Bloch had a seizure disorder.''')

T(2, 0, 5,
  '''Police raided an apartment at 12 Orchard Place that they believe Nick Soros used as a betting office. While officers searched, the landline rang repeatedly, and an officer took the calls. Callers said things like "Put two hundred on Riverside in the third race" and "Fifty on the Hawks tonight, Nick." The callers do not testify. At Soros's gambling trial, the officer's testimony about the calls is offered to show that the apartment was being used to take bets.''')

T(2, 1, 7,
  '''Marco Delgado sues Fenwick Auto, claiming he was wrongly fired over money missing from the office safe. The dispute is whether the owner, Gil Fenwick, was at the dealership at 9 p.m. when the safe was opened. A mechanic testifies that at 9 p.m. a customer asked a salesman, "Is Mr. Fenwick in the back?" and the salesman, who does not testify, answered, "Well, his car's not in the lot." Delgado offers the salesman's answer as evidence that Fenwick was not at the dealership at 9 p.m.''')

T(3, 0, "Applying only the definition, is the notebook hearsay as offered?",
  '''At Tomas Rett's trial for conspiracy to distribute methamphetamine, the prosecution offers a spiral notebook found in his kitchen drawer. It lists initials, quantities and dollar amounts, such as "T.M. - 2 oz - owes 4,200" and "J.K. - 1 oz - paid." An agent testifies that notebooks like this are tools of the drug trade, and the prosecution offers the notebook only as drug-dealing paraphernalia found in Rett's home, with a limiting instruction that the entries are not proof of any particular sale or debt.''',
  ([('''An agent testifies that notebooks like this are tools of the drug trade, and the prosecution offers the notebook only as drug-dealing paraphernalia found in Rett's home, with a limiting instruction that the entries are not proof of any particular sale or debt.''',
     '''The prosecution offers the entry "T.M. - 2 oz - owes 4,200" to prove that Rett fronted two ounces to Theo Marsh, a charged co-conspirator, who still owed $4,200.''')], 1, None))

T(2, 1, 8,
  '''Elena Mars disappeared on June 8. Her diary entry for that day reads, "Dinner with R. at Marlowe's, 8 pm. Wear the blue dress." At the trial of her ex-boyfriend, Ronan Hale, the prosecution offers the entry to show that Elena planned to meet Hale at Marlowe's that evening.''',
  ([('''At the trial of her ex-boyfriend, Ronan Hale, the prosecution offers the entry to show that Elena planned to meet Hale at Marlowe's that evening.''',
     '''At the trial of her ex-boyfriend, Ronan Hale, the defense claims that a farewell note found in her car was written by Elena; the prosecution offers the diary entry as a sample of Elena's handwriting, for a document examiner to compare with the note.''')], 0, None))

T(2, 1, "Is the letter hearsay as offered?",
  '''Farmer Anke Dorr's barn burned on October 3. A week later she received an unsigned letter: "I'm the one who burned your barn, and your house is next. It'll be a whole nother kind of fire." At the arson trial of her neighbor, Clay Fisk, the prosecution offers the letter to prove that its writer burned the barn, and a document examiner links the handwriting to Fisk.''',
  ([('''At the arson trial of her neighbor, Clay Fisk, the prosecution offers the letter to prove that its writer burned the barn, and a document examiner links the handwriting to Fisk.''',
     '''Her neighbor, Clay Fisk, is on trial only for mailing a threatening communication; the prosecution offers the letter as the threat charged, and a document examiner links the handwriting to Fisk.''')], 0, None))

T(2, 0, 3,
  '''A bankruptcy trustee sues to undo debtor Glen Aster's May 1 transfer of a lake cabin to his brother, arguing that Aster made the transfer knowing he was insolvent and about to be sued. The trustee offers five letters that creditors mailed to Aster in April, such as one from Pell Bank: "Your loan is 90 days past due; we will commence legal action if payment is not received by May 15." The trustee offers the letters to show that Aster had received these warnings when he transferred the cabin.''',
  ([('''The trustee offers the letters to show that Aster had received these warnings when he transferred the cabin.''',
     '''The trustee offers the letters to prove that Aster's loans were in fact past due, which Aster disputes.''')], 1, None))

T(3, 0, 9,
  '''Dr. Stanley Oberg is on trial for running a clinic that sold opioid prescriptions without examinations. An undercover agent testifies that while she sat in the clinic's waiting room, she heard patients asking each other, "How much cash does he want for the thirties?" and "Does he even look at you, or just write it?" The patients do not testify. The prosecution offers the testimony as evidence that the clinic was selling prescriptions for cash.''')

# ---------------------------------------------------------------- prior statements of a testifying witness
T(2, 1, "Is Stein's testimony about what he told his supervisor hearsay?",
  '''Delivery driver Karl Stein sues the company that supplied his truck after its brakes failed on a downhill grade. Stein testifies at trial: "That morning I told my supervisor, Gail, that the brake pedal was going soft and sinking to the floor." The supplier claims the brakes were fine and Stein was speeding. Stein offers his testimony about what he told Gail to prove that the brake pedal was in fact going soft that morning.''',
  ([('''The supplier claims the brakes were fine and Stein was speeding. Stein offers his testimony about what he told Gail to prove that the brake pedal was in fact going soft that morning.''',
     '''Stein also sues his employer for sending him out anyway, and on that claim he offers his testimony about what he told Gail to show that the company had been warned before he left the yard.''')], 0, None))

T(2, 1, 8,
  '''Bank teller Sofia Lang testifies at Aaron Keel's robbery trial and identifies him. The prosecution also calls Detective Ward, who testifies that a week after the robbery Lang looked at a six-photo array and said, "Number four, that's him," pointing to Keel's photo. The prosecution offers Ward's testimony as further proof that Keel was the robber.''')

T(3, 1, 0,
  '''At Glen Parrish's trial for assaulting his wife, Nell, she testifies that he struck her with a lamp on the night of June 2. The prosecution then offers her diary entry written that night: "Glen hit me with the lamp again. Left arm swollen." The prosecution offers the entry as additional proof that Glen struck her.''',
  ([('''The prosecution offers the entry as additional proof that Glen struck her.''',
     '''The defense has argued that Nell invented the assault after she filed for divorce in August. The prosecution offers the June entry only to rebut that charge of recent invention, and the jury is instructed not to treat the entry itself as proof of the assault.''')], 0, None))

T(2, 1, 10,
  '''At Brandon Cole's trial for breaking into cars on Wren Street at 3 a.m., witness Maya Singh testifies. On direct, the prosecutor asks what she told the 911 operator, and she answers: "I told her a man in a Raiders cap was breaking into the Hondas across the street." The prosecution offers her answer to prove that a man in a Raiders cap broke into the cars.''',
  ([('''The prosecution offers her answer to prove that a man in a Raiders cap broke into the cars.''',
     '''The defense claims Singh was asleep and saw nothing, and the prosecution offers her answer, together with the 3:04 a.m. call log, to show that she was awake and on the phone at that hour.''')], 0, None))

T(3, 1, 8,
  '''At Owen Pratt's fraud trial, his former bookkeeper, Rita Snell, testifies that she never saw Pratt alter any invoices. The prosecution then reads to the jury her grand-jury testimony, given under oath six months earlier: "I watched Owen change the dates on the Keller invoices himself." The prosecution offers the grand-jury testimony as proof that Pratt altered the invoices.''',
  ([('''The prosecution offers the grand-jury testimony as proof that Pratt altered the invoices.''',
     '''The prosecution reads it solely to impeach Snell, and the jury is instructed that it may consider the earlier testimony only in deciding whether to believe her trial testimony.''')], 0, None))

T(3, 0, "Is the evidence of the plate number hearsay?",
  '''Warehouse clerk Dana Holt saw a hit-and-run, wrote the fleeing car's plate number on her hand, and later copied it into a notebook. At trial she cannot recall the plate. The prosecutor shows her the notebook; she reads it silently, hands it back, says it has brought the number back to her, and then testifies from memory that the plate was 7KDL412. The prosecution offers her testimony that the plate was 7KDL412.''',
  ([('''she reads it silently, hands it back, says it has brought the number back to her, and then testifies from memory that the plate was 7KDL412. The prosecution offers her testimony that the plate was 7KDL412.''',
     '''she reads it but says it does not bring the number back to her. The prosecutor then reads the notebook entry, "7KDL412," into the record to prove the fleeing car's plate number.''')], 1, None))

T(2, 0, 9,
  '''Payroll clerk Nisha Rao sues Corwin Mills, claiming she was fired in retaliation for reporting wage fraud. She testifies: "On March 3 I told the HR director that my manager was falsifying overtime records." Rao offers her testimony about what she told HR to show that she made a complaint before she was fired.''',
  ([('''Rao offers her testimony about what she told HR to show that she made a complaint before she was fired.''',
     '''In a separate wage suit, her former co-workers call Rao and offer her testimony about what she told HR to prove that the manager was falsifying overtime records.''')], 1, None))

T(2, 1, 2,
  '''At Jalen Cross's trial for a 9 p.m. burglary, his friend Marcus Reed testifies that the two of them were at a baseball game. The defense then offers a text Reed sent his girlfriend at 9:02 that night: "At the stadium with Jalen, section 112." The defense offers the text to prove that Reed and Cross were at the stadium at 9:02.''',
  ([('''The defense offers the text to prove that Reed and Cross were at the stadium at 9:02.''',
     '''The prosecution claims Reed's phone was dead all evening, so he could not have called Cross at 9:15 as he testified; the defense offers the text to show that Reed's phone was working at 9:02.''')], 0, None))

T(1, 1, 11,
  '''In a personal-injury trial, the plaintiff's treating physician, Dr. Lena Chu, is sitting in the courtroom. Rather than calling her, the plaintiff reads excerpts from her deposition taken in the case last spring: "In my opinion the hip fracture was caused by the fall on the stairs." The excerpts are offered to prove the cause of the fracture.''',
  ([('''Rather than calling her, the plaintiff reads excerpts from her deposition taken in the case last spring: "In my opinion the hip fracture was caused by the fall on the stairs." The excerpts are offered to prove the cause of the fracture.''',
     '''The plaintiff calls her to the stand, where she testifies, "In my opinion the hip fracture was caused by the fall on the stairs." Her testimony is offered to prove the cause of the fracture.''')], 0, None))

T(2, 1, 0,
  '''Motorist Hana Oduya testifies at trial that the defendant's van rear-ended her while she was stopped at a light. Her lawyer then reads to the jury a recorded statement Oduya gave her insurance adjuster two days after the crash, in which she said the same thing. The statement is offered as further proof that the van rear-ended her while she was stopped.''')

T(2, 1, 10,
  '''Eight-year-old Mia testifies at her stepfather's trial that he hit her with a belt. Her mother then testifies that the morning after the incident, Mia told her, "Dan hit me with his belt because I spilled the juice." The prosecution offers the mother's testimony as proof that the stepfather hit Mia.''')

T(1, 0, 1,
  '''At a bar-fight trial, bartender Liam Cho testifies: "From behind the bar I saw the defendant pick up a bottle and swing it at the other man's head." Cho gave the police a written statement the same night, but no one offers or mentions the written statement at trial. The prosecution offers Cho's testimony to prove that the defendant swung the bottle.''')

# ---------------------------------------------------------------- plain assertions / in-court testimony
T(3, 0, 7,
  '''At Dean Voss's trial for identity fraud, the prosecution offers the Bayside Motel's registration card for March 14, filled out and signed "Ray Colter, Room 12." Voss concedes that he wrote the card. The prosecution offers it to show that Voss was using the name "Ray Colter," the name on a forged license found in his wallet.''',
  ([('''Voss concedes that he wrote the card. The prosecution offers it to show that Voss was using the name "Ray Colter," the name on a forged license found in his wallet.''',
     '''Voss says a real man named Ray Colter was the one using the forged license, and the defense offers the card, whose writer is unknown, to prove that Ray Colter stayed in Room 12 that night.''')], 1, None))

T(2, 1, "Is the newspaper article hearsay?",
  '''A toddler was hurt when the buckle of a Snugfit car seat, bought on May 20 from Tolley's Baby Store, failed in a crash. The parents offer a May 2 article from the Clarion Gazette headlined "Snugfit recalls 40,000 car seats after buckle failures." In their suit against Snugfit, the parents offer the article to prove that Snugfit buckles had failed before.''',
  ([('''In their suit against Snugfit, the parents offer the article to prove that Snugfit buckles had failed before.''',
     '''In their suit against Tolley's, the parents claim the store kept selling the seat after the recall was made public, and they offer the article to show that the recall had been announced in the local paper before May 20.''')], 0, None))

T(2, 1, 0,
  '''After a street fight, Officer Kurt Dahm wrote a report stating, "Witness Tia Moss stated that Jordan Hale threw the first punch." Hale is sued for battery by the other man, and the plaintiff offers the report to prove that Hale threw the first punch.''',
  ([('''Hale is sued for battery by the other man, and the plaintiff offers the report to prove that Hale threw the first punch.''',
     '''Moss says she never spoke to the officer, and Hale sues Dahm for fabricating evidence; Hale offers the report to show what Dahm wrote in it.''')], 0, None))

T(2, 1, 6,
  '''In a dispute over a roof repair, homeowner Beth Tanaka says she paid Kellan Roofing in full. The receipt at issue, on Kellan letterhead, reads "Paid in full - $3,200 - K. Kellan." Tanaka offers the receipt to prove that she paid the $3,200.''',
  ([('''In a dispute over a roof repair, homeowner Beth Tanaka says she paid Kellan Roofing in full.''',
     '''Homeowner Beth Tanaka is on trial for forging a receipt from Kellan Roofing.'''),
    ('''Tanaka offers the receipt to prove that she paid the $3,200.''',
     '''The prosecution offers the receipt as the forged document itself, to show what Tanaka created and handed to her insurer.''')], 0, None))

T(2, 1, 4,
  '''The owner of the fishing boat Tern sues a marine-engine maker, claiming a fuel-line defect made the boat lose power and capsize. The maker says heavy seas, not the engine, caused the capsizing, and it offers a recording of a Coast Guard radio broadcast from that morning: "Small craft advisory, winds 30 knots, seas 8 to 10 feet." The maker offers the broadcast to prove that winds and seas were that high.''',
  ([('''The maker offers the broadcast to prove that winds and seas were that high.''',
     '''The maker argues that the Tern's captain was careless to go out at all, and it offers the broadcast, which the captain admits he heard on his radio, to show that he had been warned before leaving port.''')], 0, None))

T(2, 1, "Setting aside any exclusions or exceptions, is the doctor's testimony hearsay?",
  '''Office worker Priya Nand sues her landlord, testifying that she slipped on a puddle from a leaking ceiling in the lobby. The landlord calls the emergency-room doctor who treated her, who testifies that Nand told her that day, "I tripped over a loose cable in my own office." The landlord offers the doctor's testimony to prove that Nand tripped over a cable in her office.''',
  ([('''The landlord offers the doctor's testimony to prove that Nand tripped over a cable in her office.''',
     '''The landlord offers the doctor's testimony to show that Nand gave a different account of the fall on the day it happened, and the court limits the jury's use of it to judging her credibility.''')], 0, None))

T(2, 0, 10,
  '''A college student was hospitalized after drinking a bottle of Ember Fizz, a hard seltzer. His family sues the maker, claiming the label gave no warning about its strength. The bottle's label reads in bold print, "Contains 12% alcohol by volume. Drink responsibly." The maker offers the label to show that the bottle carried an alcohol-content warning.''',
  ([('''His family sues the maker, claiming the label gave no warning about its strength.''',
     '''In a separate state tax case, the question is whether Ember Fizz is taxed at the higher rate for drinks above 10% alcohol.'''),
    ('''The maker offers the label to show that the bottle carried an alcohol-content warning.''',
     '''The state offers the label to prove that Ember Fizz contains 12% alcohol by volume.''')], 1, None))

T(2, 0, "Is the ransom note hearsay as offered?",
  '''At Curtis Vane's extortion trial, the prosecution offers a note left in the Hallorans' mailbox: "We have your daughter. $50,000 in the green duffel at the Kemp Road overpass by Friday or you never see her again." The extortion count requires proof that a demand for money was made by threat, and the note is offered for that purpose.''',
  ([('''The extortion count requires proof that a demand for money was made by threat, and the note is offered for that purpose.''',
     '''Vane is also charged with kidnapping; his defense is that the daughter ran away on her own and was never held by anyone, and the prosecution offers the note to prove that she was being held.''')], 1, None))

T(2, 1, 8,
  '''People injured when a bleacher collapsed sue Norcast Fasteners, claiming its bolts were defective. They offer an internal email from a Norcast test engineer, who has since died: "I ran the stress test on bolt lot 44 and three bolts sheared at half their rated load." The plaintiffs offer the email to prove that the lot 44 bolts were weak.''',
  ([('''The plaintiffs offer the email to prove that the lot 44 bolts were weak.''',
     '''The defect is conceded. The plaintiffs' punitive-damages claim turns on whether Norcast executives shipped lot 44 after being warned, and they offer the email, which was copied to those executives, to show that the executives received the warning before the shipment.''')], 0, None))

T(3, 1, 3,
  '''Mickey Dunn is on trial for a burglary in Tacoma, Washington, at 9 p.m. on June 4. A bartender from Denver testifies that at 9 p.m. that night a man she identifies as Dunn sat at her bar and told her, "I flew in from Seattle this morning." The defense offers her account of his words to prove that Dunn took a morning flight out of Seattle, as he claims.''',
  ([('''The defense offers her account of his words to prove that Dunn took a morning flight out of Seattle, as he claims.''',
     '''The defense offers her account to show that Dunn was sitting in her Denver bar, talking with her, at the very time of the Tacoma burglary.''')], 0, None))

T(1, 0, 1,
  '''In a crash case, Rosa Lindqvist testifies: "I was standing at the bus stop and saw the white van run the red light and hit the sedan." The plaintiff offers her testimony to prove that the van ran the red light.''',
  ([('''Rosa Lindqvist testifies: "I was standing at the bus stop and saw the white van run the red light and hit the sedan."''',
     '''Rosa Lindqvist testifies: "My husband was standing at the bus stop, and when he got home he told me he saw the white van run the red light and hit the sedan."''')], 1, None))

T(1, 1, 8,
  '''At Troy Bassett's assault trial, the prosecution plays a 911 recording in which an unidentified caller says, "He's got a knife! He just cut a guy outside the Shell station and he's getting into a red Jeep, heading north on Pine!" The caller has never been found. The recording is offered to prove that the attacker had a knife and drove off in a red Jeep, which Bassett owns.''')

T(1, 1, 9,
  '''Tommy Ruiz is charged with murdering Alan Price. A paramedic testifies that as Price lay bleeding in the ambulance, he said, "I'm not going to make it. Tommy Ruiz shot me over the car money." Price died an hour later. The prosecution offers the paramedic's testimony to prove that Ruiz shot Price.''')

T(1, 1, 2,
  '''In a contract suit, Belmont Grain offers a sworn affidavit from its former shipping manager, who now lives abroad, stating: "On August 9 I personally watched 400 tons of wheat loaded onto the buyer's barge." The affidavit is offered to prove that 400 tons were loaded.''')

T(2, 1, 7,
  '''In a suit over missing inventory, a hardware chain offers the stock ledger kept at its Midvale store, in which a clerk who has since left the company wrote by hand on October 1: "On hand: 212 chainsaws." The ledger is offered to prove that the store had 212 chainsaws on October 1.''')

T(2, 1, 9,
  '''At the retrial of a securities case after a hung jury, the government reads the transcript of testimony that analyst Pete Varga gave at the first trial, where the same defense lawyer cross-examined him. Varga has since died. The testimony is offered to prove that the defendant ordered Varga to inflate the quarterly numbers.''')

T(2, 1, 11,
  '''In a products-liability trial, the plaintiff plays for the jury the videotaped deposition, taken in this case last year, of a former plant engineer who now lives in Japan and will not travel for trial. In it he says that the plant skipped the final pressure test on the valve that failed. The deposition is offered to prove that the pressure test was skipped.''')

T(2, 1, "Leaving aside Rule 801(d), is Pryor's text hearsay?",
  '''Cyclist Anika Berg sues driver Lucas Pryor, who struck her at an intersection. Berg offers a text message Pryor sent his brother an hour after the crash: "I shouldn't have run that light. I feel sick about it." It is conceded that Pryor sent the text. The text is offered to prove that Pryor ran the red light.''')

T(1, 1, 0,
  '''Warehouse worker Ben Soto was struck by a forklift and sues the operator's employer. Soto's co-worker testifies that ten minutes after the accident, another employee, who has since moved away, told her, "The forklift driver was texting when he hit Ben." The co-worker's testimony is offered to prove that the driver was texting.''')

T(1, 1, 7,
  '''In a disability-benefits dispute, claimant Leon Frey offers a letter from his orthopedic surgeon to the insurer: "Mr. Frey cannot lift more than ten pounds or stand longer than twenty minutes and is unable to return to his warehouse job." The surgeon is not called. The letter is offered to prove Frey's physical limits.''')

T(1, 1, 4,
  '''In a civil suit against a daycare, a teacher testifies that four-year-old Owen, who is not called as a witness, told her at pickup, "Miss Tara locked me in the closet at nap time." The testimony is offered to prove that Owen was locked in a closet.''')

T(1, 1, 6,
  '''Five customers sue Pina's Grill for food poisoning. They offer a printout of an online review posted on June 3 by an unknown user: "Got food poisoning from the chicken at Pina's on June 2. Half our table was sick." The review is offered to prove that Pina's chicken made people sick on June 2.''')

T(1, 1, 1,
  '''In an insurance dispute over a barn fire, the insurer claims the owner, Ada Tilden, set the fire herself. A neighbor testifies, "Everyone in town says Ada set that fire for the insurance money." The insurer offers the testimony to prove that Tilden set the fire.''')

T(1, 1, 10,
  '''At a manslaughter trial, the prosecution offers the typed transcript of a police interview with a witness who died before trial. In the interview, the witness said, "I saw the defendant push him down the stairs." The transcript is offered to prove that the defendant pushed the victim.''')

T(2, 1, 3,
  '''In a boundary dispute between neighbors, one side offers a 1998 surveyor's report, prepared for a previous owner, stating that the property line runs three feet east of the current fence. The surveyor has retired and is not called. The report is offered to prove where the property line is.''')

T(2, 1, 0,
  '''A city bus struck a pedestrian at Market and Fifth. A shop clerk testifies that seconds after the crash, a woman standing next to him screamed, "Oh my God, the bus ran the red!" The woman was never identified. The pedestrian's family offers the clerk's testimony to prove that the bus ran the red light.''')

T(2, 1, 9,
  '''In a class action over a defective laptop battery, the plaintiffs offer a press release issued by the battery's supplier, which is not a party, stating that "approximately 60,000 battery cells from the 2023 production run were found to have a separator flaw that can cause overheating." The release is offered to prove that the cells had that flaw.''')

T(1, 1, 2,
  '''Driver Nate Cole sues cyclist Ivy Marsh after a collision at Fourth and Main. Cole offers a post that an unknown user published on social media four minutes after the collision: "Just watched a cyclist blow straight through the stop sign at 4th & Main and get clipped. She's OK." The post is offered to prove that Marsh ran the stop sign.''')

T(1, 0, 0,
  '''At a shoplifting trial, store detective Maria Olin takes the stand and testifies, "I was watching the live camera feed when the defendant slipped two phone chargers into her coat and walked past the registers." Her testimony is offered to prove that the defendant took the chargers.''')

T(1, 0, 8,
  '''In a paternity case, geneticist Dr. Farid Anwar, who personally ran the DNA analysis, testifies from the witness stand that the test showed a 99.97% probability that Carl Dunne is the child's father. His testimony is offered to prove paternity.''')

T(1, 0, 11,
  '''At an arson trial, a neighbor testifies: "Around midnight I heard glass break, looked out my window, and saw the defendant running from the side of the house with a red gas can." Her testimony is offered to prove that the defendant was at the house with a gas can.''')

T(2, 0, 4,
  '''At a carjacking trial, the victim testifies about the incident and is asked whether the man who took her car is in the courtroom. She points to the defendant and says, "That's him, at the end of the table." The prosecution offers her identification to prove that the defendant was the carjacker.''')


# ---------------------------------------------------------------- build
def cid(instr, state, options):
    h = hashlib.sha1(json.dumps([instr, state, options], ensure_ascii=False).encode()).hexdigest()
    return "c_" + h[:12]


def apply_edits(state, edits):
    s = state
    for old, new in edits:
        n = s.count(old)
        assert n == 1, f"edit target must occur exactly once (found {n}): {old[:70]!r}"
        s = s.replace(old, new)
    return s


def qtext(q):
    return Q[q] if isinstance(q, int) else q


def purpose_verbs(key):
    """Pick one wording per item for purpose clauses ("offers X to prove/show that ..."),
    shared by an item and its twin, so the verb carries no signal about the answer."""
    rng = random.Random(f"{SEED}:verbs:{key}")
    v_that = rng.choice(["to prove", "to show", "to establish", "to demonstrate"])
    v_wh = rng.choice(["to prove", "to show", "to establish"])
    v_why = rng.choice(["to show", "to establish"])
    v_plain = rng.choice(["to prove", "to show", "to establish"])

    def norm(text):
        text = re.sub(r"\bto (?:prove|show) that\b", v_that + " that", text)
        text = re.sub(r"\bto (?:prove|show) (what|how|where|when)\b", lambda m: f"{v_wh} {m.group(1)}", text)
        text = re.sub(r"\bto (?:show|explain) why\b", v_why + " why", text)
        text = re.sub(r"\bto (?:prove|show)\b(?! that| what| how| where| when| why)", v_plain, text)
        return text
    return norm


def build():
    rows, n = [], 0
    for i, it in enumerate(ITEMS, 1):
        key = f"h{i:03d}"
        hdr = HEADERS[random.Random(f"{SEED}:{key}").randrange(len(HEADERS))]
        raw = hdr + it["state"].strip()
        norm = purpose_verbs(key)
        state = norm(raw)
        ins = qtext(it["q"])
        n += 1
        base_id = f"r_{SRC}_{n}"
        base = {
            "id": base_id, "group_id": f"g:{SRC}:{key}", "call_id": cid(ins, state, None),
            "split": "train", "track": "STD", "source": SRC, "state": state,
            "qtype": "noul", "instructions": ins, "options": None, "gold": it["gold"],
            "role": "aff", "card": CARD,
            "meta": {"domain": DOMAIN, "difficulty": it["d"], "item": key},
        }
        rows.append(base)
        if it["twin"]:
            edits, tgold, tq = it["twin"]
            st = norm(apply_edits(raw, edits))
            tins = qtext(tq) if tq is not None else ins
            n += 1
            rows.append({**base, "id": f"r_{SRC}_{n}", "call_id": cid(tins, st, None),
                         "state": st, "instructions": tins, "gold": tgold,
                         "meta": {"domain": DOMAIN, "difficulty": it["d"], "item": key,
                                  "twin_of": base_id}})
    return rows


def validate(rows):
    errs = []
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    byid = {r["id"]: r for r in rows}
    text2cid = {}
    for r in rows:
        k = json.dumps([r["instructions"], r["state"], r["options"]], ensure_ascii=False)
        if k in text2cid and text2cid[k] != r["call_id"]:
            errs.append(f"{r['id']}: same text, different call_id")
        text2cid.setdefault(k, r["call_id"])
    if len(set(text2cid.values())) != len(text2cid):
        errs.append("call_id collision across different texts")
    if len(text2cid) != len(rows):
        errs.append("duplicate row texts")
    need = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
            "instructions", "options", "gold", "role", "card", "meta"}
    for r in rows:
        rid = r["id"]
        if set(r) != need:
            errs.append(f"{rid}: keys {sorted(set(r) ^ need)}")
        if (r["split"], r["track"], r["source"], r["qtype"], r["role"]) != \
                ("train", "STD", SRC, "noul", "aff"):
            errs.append(f"{rid}: split/track/source/qtype/role")
        if r["options"] is not None or r["gold"] not in (0, 1) or isinstance(r["gold"], bool):
            errs.append(f"{rid}: noul fields")
        if not r["id"].startswith(f"r_{SRC}_"):
            errs.append(f"{rid}: id prefix")
        wc = len(r["state"].split())
        if not 35 <= wc <= 200:
            errs.append(f"{rid}: state words {wc}")
        if any(not ln.startswith("- ") or ": " not in ln for ln in r["card"].split("\n")):
            errs.append(f"{rid}: card format")
        low = (r["state"] + " " + r["instructions"]).lower()
        for leak in ("hearsay", "truth of the matter", "not offered for its truth",
                     "verbal act", "non-assertive", "nonassertive", "implied assertion"):
            if leak in r["state"].lower() or (leak != "hearsay" and leak in low):
                errs.append(f"{rid}: leak term {leak!r}")
        m = r["meta"]
        if m.get("domain") != DOMAIN or m.get("difficulty") not in (1, 2, 3):
            errs.append(f"{rid}: meta")
        if "twin_of" in m:
            b = byid.get(m["twin_of"])
            if not b or b["group_id"] != r["group_id"] or b["gold"] == r["gold"] \
                    or b["call_id"] == r["call_id"] or "twin_of" in b["meta"]:
                errs.append(f"{rid}: bad twin")
    y = sum(r["gold"] for r in rows) / len(rows)
    if not 0.48 <= y <= 0.52:
        errs.append(f"yes share {y:.3f}")
    if len({r["instructions"] for r in rows}) < 6:
        errs.append("fewer than 6 phrasings")
    return errs


def main():
    rows = build()
    errs = validate(rows)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  ", e)
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{DOMAIN}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / f"{DOMAIN}.blind.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    wc = [len(r["state"].split()) for r in rows]
    print(json.dumps({
        "rows": len(rows), "base_items": len(base), "twin_rows": len(twins),
        "twin_share_of_rows": round(len(twins) / len(rows), 3),
        "rows_in_twin_pairs": 2 * len(twins),
        "yes": sum(r["gold"] for r in rows), "no": sum(1 - r["gold"] for r in rows),
        "base_yes": sum(r["gold"] for r in base), "base_no": sum(1 - r["gold"] for r in base),
        "difficulty_rows": dict(sorted(Counter(r["meta"]["difficulty"] for r in rows).items())),
        "distinct_instructions": len({r["instructions"] for r in rows}),
        "state_words": [min(wc), round(sum(wc) / len(wc)), max(wc)],
    }, indent=1))


if __name__ == "__main__":
    main()
