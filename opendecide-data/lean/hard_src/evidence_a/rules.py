"""Invented evidence codes for the HARD evidence_a domain (all jurisdictions fictional).

Each jurisdiction deliberately differs from real-world rules in places (time limits, party statements,
implied assertions, unavailability, business-record conditions), so items must be answered from the text.
"""

JNAME = {
    "A": "Arvell Rules of Evidence",
    "M": "Morrow Vale Evidence Code",
    "H": "Evidence Act of Halvard Reach",
    "V": "Vane Islands Evidence Ordinance",
    "C": "Coldmere Code of Evidence",
    "T": "Tessary Evidence Code",
}

RULES = {
    # ---------------- Arvell (A) ----------------
    "A801": 'Rule 801 (Definitions). (a) "Statement" means a person\'s oral assertion, written assertion, or nonverbal conduct, if the person intended it as an assertion. (b) "Hearsay" means a statement that the declarant does not make while testifying at the current trial or hearing and that a party offers in evidence to prove the truth of the matter asserted in the statement. (c) A statement is not hearsay if it is offered against an opposing party and was made by that party.',
    "A802": "Rule 802. Hearsay is not admissible unless these Rules provide otherwise.",
    "A803_1": "Rule 803(1) (Present sense impression). A statement describing or explaining an event or condition, made while or immediately after the declarant perceived it, is not excluded by Rule 802, whether or not the declarant is available.",
    "A803_2": "Rule 803(2) (Excited utterance). A statement relating to a startling event or condition, made while the declarant was under the stress of excitement that it caused, is not excluded by Rule 802, whether or not the declarant is available.",
    "A803_6": "Rule 803(6) (Records of a regularly conducted activity). A record of an act, event, condition, opinion, or diagnosis is not excluded by Rule 802 if: (A) it was made at or near the time by, or from information transmitted by, someone with knowledge who was acting in the course of the activity; (B) it was kept in the course of a regularly conducted activity of a business or organisation; (C) making the record was a regular practice of that activity; (D) these conditions are shown by the testimony of the custodian or another qualified witness, or by a certification of the custodian; and (E) the opponent does not show that the source of information or the method or circumstances of preparation indicate a lack of trustworthiness.",
    "A804a": "Rule 804(a) (Unavailability). A declarant is unavailable if the declarant: is exempted from testifying by a court ruling on privilege; refuses to testify despite a court order; testifies to not remembering the subject matter; cannot be present because of death or a then-existing infirmity or illness; or is absent and the proponent has been unable, by process or other reasonable means, to procure attendance.",
    "A804b3": "Rule 804(b)(3) (Statement against interest). If the declarant is unavailable, the following is not excluded by Rule 802: a statement that a reasonable person in the declarant's position would have made only if the person believed it to be true because, when made, it was so contrary to the declarant's proprietary or pecuniary interest or had so great a tendency to expose the declarant to civil or criminal liability; if offered in a criminal case as one that tends to expose the declarant to criminal liability, it must also be supported by corroborating circumstances that clearly indicate its trustworthiness.",
    "MENU_A": (
        "R.801: Hearsay is a statement (an oral or written assertion, or conduct intended as an assertion) that the declarant did not make while testifying at the current trial or hearing, offered to prove the truth of the matter asserted. A statement offered against an opposing party and made by that party is not hearsay. R.802: Hearsay is inadmissible unless an exception applies.\n"
        "R.803(1) Present sense impression: a statement describing or explaining an event or condition, made while or immediately after the declarant perceived it.\n"
        "R.803(2) Excited utterance: a statement relating to a startling event or condition, made while the declarant was under the stress of excitement it caused.\n"
        "R.803(6) Business record: a record made at or near the time by, or from information transmitted by, someone with knowledge acting in the course of a regularly conducted activity, where making the record was a regular practice, shown by the custodian's testimony or certification, unless the source or circumstances indicate a lack of trustworthiness.\n"
        "R.804(b)(3) Statement against interest: if the declarant is unavailable (privilege ruling, refusal despite court order, lack of memory, death or illness, or absence despite reasonable efforts), a statement so contrary to the declarant's pecuniary or proprietary interest, or so exposing the declarant to civil or criminal liability, that a reasonable person would have made it only if true; in a criminal case, a statement exposing the declarant to criminal liability also needs corroborating circumstances clearly indicating trustworthiness."
    ),
    # ---------------- Morrow Vale (M) ----------------
    "M801": "Section 801 (Hearsay). (1) Hearsay is an assertion made by a person otherwise than while testifying in the present proceeding, offered to prove that the matter asserted is true. (2) Conduct is an assertion only if the person intended it to communicate a fact. (3) There is no exclusion for statements of a party: a party's own out-of-court assertion is hearsay if it meets subsection (1).",
    "M802": "Section 802. Hearsay is inadmissible except as provided in sections 803 and 804.",
    "M803_1": "Section 803(1) (Present sense impression). An assertion describing an event, made while the declarant was perceiving the event or not more than two minutes afterwards, is admissible, but only if the declarant, or another person who perceived the same event, testifies in the proceeding.",
    "M803_2": "Section 803(2) (Excited utterance). An assertion relating to a startling event, made while the declarant was under the stress of excitement caused by it and not more than thirty minutes after the event ended, is admissible. An assertion made in answer to a question put by a law-enforcement officer does not qualify.",
    "M803_6": "Section 803(6) (Business records). A record made in the ordinary course of a business, within seven days after the act or event recorded, by a person with personal knowledge of it or from information supplied by an employee of the same business who had personal knowledge, and authenticated by a written certificate of the records custodian, is admissible. A record prepared in contemplation of litigation is excluded.",
    "M804_3": "Section 804(3) (Statement against interest). An assertion that, when made, was so far contrary to the declarant's financial or property interest (such as an acknowledgment of a debt owed, or a surrender of a claim or of property) that a reasonable person would not have made it unless believing it true, is admissible. The declarant's availability is immaterial. Exposure to criminal or civil liability for wrongdoing is not by itself a financial or property interest.",
    "MENU_M": (
        "s.801: Hearsay is an assertion made by a person otherwise than while testifying in the present proceeding, offered to prove that the matter asserted is true; conduct is an assertion only if intended to communicate a fact. There is no exclusion for a party's own statements. s.802: Hearsay is inadmissible except under ss.803-804.\n"
        "s.803(1) Present sense impression: an assertion describing an event, made while perceiving it or not more than two minutes afterwards, if the declarant or another person who perceived the event testifies.\n"
        "s.803(2) Excited utterance: an assertion relating to a startling event, made under the stress of excitement it caused and not more than thirty minutes after the event ended; not an assertion made in answer to a law-enforcement officer's question.\n"
        "s.803(6) Business record: a record made in the ordinary course of business within seven days after the event, by a person with personal knowledge or from information supplied by an employee of the same business with personal knowledge, authenticated by the custodian's written certificate; not a record prepared in contemplation of litigation.\n"
        "s.804(3) Statement against interest: an assertion so far contrary to the declarant's financial or property interest when made (e.g. acknowledging a debt) that a reasonable person would not have made it unless true; availability immaterial; exposure to criminal or civil liability for wrongdoing is not by itself enough."
    ),
    # ---------------- Halvard Reach (H) ----------------
    "H4": "Section 4 (Hearsay). (1) Hearsay is evidence of a previous representation made by a person, tendered to prove a fact that the person intended to assert by the representation or that the representation implies the person believed. (2) Words are not hearsay if they are tendered only because they were uttered, such as words of offer, acceptance, gift, threat, or defamation. (3) A representation includes conduct, whether or not the conduct was intended as an assertion. (4) Output generated by a device or process without human input is not a representation of a person.",
    "H5": "Section 5. Hearsay is inadmissible unless an exception in Part 2 applies.",
    "H9": "Section 9 (Spontaneous statements). A representation about a startling occurrence, made by a person who perceived it, while that person was still so dominated by the occurrence that there was no real opportunity for reflection, is admissible. Elapsed time is relevant but not decisive.",
    "H11": "Section 11 (Business records). A document forming part of the records of a business, made in the course of that business by a person who had personal knowledge of the matter, or from information supplied directly or indirectly by such a person, is admissible if the person who had the personal knowledge (i) is dead, (ii) cannot be found after reasonable inquiry, or (iii) cannot reasonably be expected to recollect the matter, having regard to the time elapsed and the routine nature of the entry.",
    "H13": "Section 13 (Declarations against interest). A representation made by a person who is dead, or who is mentally incapable of giving evidence, at the time of trial is admissible if, when it was made, it was against that person's pecuniary, proprietary, or penal interest and the person knew it to be so.",
    "MENU_H": (
        "s.4: Hearsay is evidence of a previous representation made by a person, tendered to prove a fact the person intended to assert or that the representation implies the person believed. Words tendered only because they were uttered (offer, acceptance, gift, threat, defamation) are not hearsay. Representations include conduct, whether or not intended as an assertion. Device output generated without human input is not a representation of a person. s.5: Hearsay is inadmissible unless Part 2 applies.\n"
        "s.9 Spontaneous statement: a representation about a startling occurrence by a person who perceived it, made while still so dominated by the occurrence that there was no real opportunity for reflection; elapsed time is relevant but not decisive.\n"
        "s.11 Business record: a document in the records of a business, made in the course of the business by, or from information supplied directly or indirectly by, a person with personal knowledge, if that person is dead, cannot be found after reasonable inquiry, or cannot reasonably be expected to recollect the matter.\n"
        "s.13 Declaration against interest: a representation by a person who is dead or mentally incapable of giving evidence at the time of trial, which when made was against that person's pecuniary, proprietary, or penal interest, and which the person knew to be so."
    ),
    # ---------------- Vane Islands (V) ----------------
    "V601": "Rule 601 (Competence). (a) Every person is competent to be a witness unless this Rule provides otherwise. (b) A person is not competent to testify about a matter if the person is incapable of expressing himself or herself about it so as to be understood, directly or through an interpreter, or is incapable of understanding the duty of a witness to tell the truth. (c) A child under eight years of age may testify only after the presiding judge has questioned the child outside the presence of the jury and found that the child understands the difference between truth and falsehood. (d) The presiding judge and any member of the jury may not testify in that trial. (e) A person convicted of perjury within the ten years preceding the proceeding is not competent to testify in it.",
    "V602": "Rule 602 (Personal knowledge). A lay witness may testify to a matter only if evidence is introduced sufficient to support a finding that the witness has personal knowledge of it. The witness's own testimony may be that evidence.",
    "V801": "Rule 801 (Hearsay). An out-of-court assertion offered to prove the truth of the matter asserted is inadmissible unless an exception in Part 8 applies.",
    "V901c": "Rule 901(c) (Chain of custody). For an item that is fungible or readily altered, including drugs, powders, liquids, biological samples, and digital storage media, the proponent must account for custody from seizure to analysis: each person who had custody must be identified and must either testify or have signed a contemporaneous log entry. A period during which custody is not so accounted for is excused only if the item was in a tamper-evident container whose seal number was recorded at sealing and was found intact and matching when opened. A discrepancy in recorded weight of not more than 5 percent goes to weight only; a larger unexplained discrepancy makes the item inadmissible.",
    "V901d": "Rule 901(d) (Unique items). An item bearing a serial number or other distinctive marking may be authenticated by a witness who recognises it, without proof of an unbroken chain of custody.",
    # ---------------- Coldmere (C) ----------------
    "C20": "Article 20. Hearsay is an out-of-court statement (oral, written, or conduct intended as an assertion) offered to prove the truth of what it asserts. It is inadmissible unless Article 30 or 31 applies. Article 21. The following are not hearsay: (a) a statement of an opposing party offered against that party; (b) a prior statement of a witness who testifies and is subject to cross-examination about it, if the prior statement is inconsistent with the testimony and was given under penalty of perjury at a trial, hearing, or deposition.",
    "C30a": "Article 30(a) (Contemporaneous description). A statement describing an event, made while the declarant was actually perceiving it, is admissible. A statement made after the event has ended does not qualify, however soon afterwards it is made.",
    "C30b": "Article 30(b) (Excited utterance). A statement relating to a startling event, made under the stress of excitement caused by it and within ten minutes after the event, is admissible.",
    "C30c": "Article 30(c) (Business records). A record made within 72 hours after the recorded act or event, as a regular practice of a regularly conducted activity, by or from a person with knowledge, and proved by a custodian's testimony or certificate, is admissible. A record whose preparation was prompted by an anticipated claim or prosecution is excluded.",
    "C31": "Article 31 (Statement against interest). If the declarant is unavailable (dead, too ill to attend, beyond the court's process despite diligent effort, or refusing to testify despite a court order), a statement that when made was so contrary to the declarant's pecuniary, proprietary, or penal interest that a reasonable person would have made it only if true is admissible. No corroboration is required.",
    "MENU_C": (
        "Art. 20: Hearsay is an out-of-court statement (oral, written, or conduct intended as an assertion) offered to prove the truth of what it asserts; it is inadmissible unless Article 30 or 31 applies. Art. 21: Not hearsay are (a) an opposing party's statement offered against it, and (b) a testifying witness's prior inconsistent statement given under penalty of perjury at a trial, hearing, or deposition.\n"
        "Art. 30(a) Contemporaneous description: a statement describing an event, made while the declarant was actually perceiving it; not one made after the event ended, however soon.\n"
        "Art. 30(b) Excited utterance: a statement relating to a startling event, made under the stress of excitement it caused and within ten minutes after the event.\n"
        "Art. 30(c) Business record: a record made within 72 hours after the recorded act or event, as a regular practice of a regularly conducted activity, by or from a person with knowledge, proved by a custodian's testimony or certificate; not a record prompted by an anticipated claim or prosecution.\n"
        "Art. 31 Statement against interest: if the declarant is unavailable (dead, too ill to attend, beyond process despite diligent effort, or refusing to testify despite a court order), a statement so contrary to the declarant's pecuniary, proprietary, or penal interest that a reasonable person would have made it only if true; no corroboration required."
    ),
    # ---------------- Tessary (T) ----------------
    "T60": 'Section 60. "Hearsay" is a statement, other than one the declarant makes while testifying at the current trial or hearing, that a party offers to prove the truth of the matter asserted; "statement" means an oral or written assertion, or nonverbal conduct intended as an assertion. Section 61. Hearsay is inadmissible unless a provision of Part 6 admits it. Section 62 lists statements that are not hearsay, and sections 63 and 64 list exceptions. The provisions named in the answer options are set out in the card.',
}

LABEL = {
    "A801": "hearsay (Arvell Rule 801)",
    "A802": "hearsay rule (Arvell Rule 802)",
    "A803_1": "present sense impression (Arvell Rule 803(1))",
    "A803_2": "excited utterance (Arvell Rule 803(2))",
    "A803_6": "business records (Arvell Rule 803(6))",
    "A804a": "unavailability (Arvell Rule 804(a))",
    "A804b3": "statement against interest (Arvell Rule 804(b)(3))",
    "M801": "hearsay (Morrow Vale s.801)",
    "M802": "hearsay rule (Morrow Vale s.802)",
    "M803_1": "present sense impression (Morrow Vale s.803(1))",
    "M803_2": "excited utterance (Morrow Vale s.803(2))",
    "M803_6": "business records (Morrow Vale s.803(6))",
    "M804_3": "statement against interest (Morrow Vale s.804(3))",
    "H4": "hearsay (Halvard Reach s.4)",
    "H5": "hearsay rule (Halvard Reach s.5)",
    "H9": "spontaneous statements (Halvard Reach s.9)",
    "H11": "business records (Halvard Reach s.11)",
    "H13": "declarations against interest (Halvard Reach s.13)",
    "V601": "competence (Vane Islands Rule 601)",
    "V602": "personal knowledge (Vane Islands Rule 602)",
    "V801": "hearsay (Vane Islands Rule 801)",
    "V901c": "chain of custody (Vane Islands Rule 901(c))",
    "V901d": "unique items (Vane Islands Rule 901(d))",
    "C20": "hearsay and exclusions (Coldmere Arts. 20-21)",
    "C30a": "contemporaneous description (Coldmere Art. 30(a))",
    "C30b": "excited utterance (Coldmere Art. 30(b))",
    "C30c": "business records (Coldmere Art. 30(c))",
    "C31": "statement against interest (Coldmere Art. 31)",
}

# ---------------- option definitions for choice items ----------------
NONE_DEF = "The statement is hearsay and none of the listed provisions admits it, so it is inadmissible."

DEFS_EXC = {
    "A": {
        "present sense impression": "Arvell Rule 803(1): a statement describing or explaining an event or condition, made while or immediately after the declarant perceived it.",
        "excited utterance": "Arvell Rule 803(2): a statement relating to a startling event or condition, made while the declarant was under the stress of excitement that it caused.",
        "business record": "Arvell Rule 803(6): a record made at or near the time by, or from information transmitted by, someone with knowledge acting in the course of a regularly conducted activity, where making the record was a regular practice, shown by the custodian or a certification, absent a showing of untrustworthiness.",
        "statement against interest": "Arvell Rule 804(b)(3): a statement by an unavailable declarant so contrary to pecuniary or proprietary interest, or so exposing the declarant to civil or criminal liability, that a reasonable person would have made it only if true; in a criminal case, a statement exposing the declarant to criminal liability also needs clear corroboration.",
        "not hearsay": "The statement falls outside Rule 801 (it is not offered for the truth of what it asserts, it is not an intended assertion, or it is an opposing party's own statement offered against that party), so no exception is needed.",
        "none of these": NONE_DEF,
    },
    "M": {
        "present sense impression": "Morrow Vale s.803(1): an assertion describing an event, made while perceiving it or within two minutes afterwards, provided the declarant or another person who perceived the event testifies.",
        "excited utterance": "Morrow Vale s.803(2): an assertion relating to a startling event, made under the stress of excitement it caused and within thirty minutes after the event ended; answers to a law-enforcement officer's questions do not qualify.",
        "business record": "Morrow Vale s.803(6): a record made in the ordinary course of business within seven days of the event, by a person with personal knowledge or from an employee of the same business with personal knowledge, with the custodian's written certificate; records prepared in contemplation of litigation are excluded.",
        "statement against interest": "Morrow Vale s.804(3): an assertion so far contrary to the declarant's financial or property interest when made (e.g. acknowledging a debt) that a reasonable person would not have made it unless true; availability immaterial; exposure to criminal or civil liability for wrongdoing is not by itself enough.",
        "not hearsay": "The evidence falls outside s.801: it is not an assertion by a person (conduct counts only if intended to communicate a fact), or it is not offered to prove that what it asserts is true. A party's own assertions are not excluded from the definition.",
        "none of these": NONE_DEF,
    },
    "C": {
        "contemporaneous description": "Coldmere Art. 30(a): a statement describing an event, made while the declarant was actually perceiving it; statements made after the event ended do not qualify.",
        "excited utterance": "Coldmere Art. 30(b): a statement relating to a startling event, made under the stress of excitement it caused and within ten minutes after the event.",
        "business record": "Coldmere Art. 30(c): a record made within 72 hours of the event as a regular practice of a regularly conducted activity, by or from a person with knowledge, proved by a custodian; records prompted by an anticipated claim or prosecution are excluded.",
        "statement against interest": "Coldmere Art. 31: a statement by an unavailable declarant so contrary to pecuniary, proprietary, or penal interest that a reasonable person would have made it only if true; no corroboration required.",
        "not hearsay": "The statement is outside Article 20 or excluded by Article 21 (an opposing party's statement offered against it, or a testifying witness's prior inconsistent sworn statement).",
        "none of these": NONE_DEF,
    },
    "H": {
        "spontaneous statement": "Halvard Reach s.9: a representation about a startling occurrence by a person who perceived it, made while still so dominated by the occurrence that there was no real opportunity for reflection.",
        "business record": "Halvard Reach s.11: a business document made in the course of the business by or from a person with personal knowledge, if that person is dead, cannot be found after reasonable inquiry, or cannot reasonably be expected to recollect the matter.",
        "declaration against interest": "Halvard Reach s.13: a representation by a person now dead or mentally incapable of giving evidence, which when made was against that person's pecuniary, proprietary, or penal interest, known to be so.",
        "not hearsay": "The evidence is not hearsay under s.4 (for example, words tendered only because they were uttered, such as an offer, gift, threat, or defamation, or device output generated without human input).",
        "none of these": NONE_DEF,
    },
}

EXC_OPTS = {
    "A": ["present sense impression", "excited utterance", "business record", "statement against interest", "not hearsay", "none of these"],
    "M": ["present sense impression", "excited utterance", "business record", "statement against interest", "not hearsay", "none of these"],
    "C": ["contemporaneous description", "excited utterance", "business record", "statement against interest", "not hearsay", "none of these"],
    "H": ["spontaneous statement", "business record", "declaration against interest", "not hearsay", "none of these"],
}

P_TRUTH = "to prove the truth of the matter asserted"
P_EFFECT = "to show its effect on the listener"
P_VERBAL = "as a verbal act with independent legal significance"
P_IMPEACH = "to impeach a witness's credibility"
P_MIND = "as circumstantial evidence of the declarant's state of mind"
PURPOSE_OPTS = [P_TRUTH, P_EFFECT, P_VERBAL, P_IMPEACH, P_MIND]
DEFS_PURPOSE = {
    P_TRUTH: "The proponent needs the fact-finder to believe that what the declarant asserted is true.",
    P_EFFECT: "The statement is used to show that someone heard or read it (notice, warning, the listener's knowledge, or the listener's reason for acting), whether or not it was true.",
    P_VERBAL: "The words themselves have legal effect or are the conduct in issue, e.g. an offer, acceptance, contract term, threat, defamatory publication, or a misrepresentation that is sued on.",
    P_IMPEACH: "The statement is used only to show that a witness has said something inconsistent, so the witness's testimony is less believable; it is not used as proof of what it says.",
    P_MIND: "The statement is used to infer the declarant's own mental state, sanity, or knowledge from the fact that it was made, not to prove the fact it asserts.",
}

BRA_OPTS = [
    "made at or near the time",
    "made by or from someone with knowledge acting in the activity",
    "kept in the course of a regularly conducted activity",
    "making the record was a regular practice",
    "foundation by custodian or certification",
    "no indication of untrustworthiness",
    "every requirement is satisfied",
]
DEFS_BRA = {
    "made at or near the time": "Rule 803(6)(A), timing: the record was made at or near the time of the act or event.",
    "made by or from someone with knowledge acting in the activity": "Rule 803(6)(A), source: the maker, or whoever transmitted the information, had knowledge and was acting in the course of the regularly conducted activity.",
    "kept in the course of a regularly conducted activity": "Rule 803(6)(B): the record was kept in the course of a regularly conducted activity of a business or organisation.",
    "making the record was a regular practice": "Rule 803(6)(C): making this kind of record was a regular practice of that activity.",
    "foundation by custodian or certification": "Rule 803(6)(D): the conditions are shown by the custodian or another qualified witness, or by the custodian's certification.",
    "no indication of untrustworthiness": "Rule 803(6)(E): the opponent has not shown that the source of information or the method or circumstances of preparation indicate a lack of trustworthiness.",
    "every requirement is satisfied": "All conditions of Rule 803(6) are met, so the record is admissible under it.",
}

BRM_OPTS = [
    "made in the ordinary course of business",
    "made within seven days",
    "personal knowledge or employee source",
    "custodian's written certificate",
    "not prepared in contemplation of litigation",
    "every requirement is satisfied",
]
DEFS_BRM = {
    "made in the ordinary course of business": "s.803(6): the record was made in the ordinary course of a business.",
    "made within seven days": "s.803(6): the record was made within seven days after the act or event recorded.",
    "personal knowledge or employee source": "s.803(6): the maker had personal knowledge, or the information came from an employee of the same business with personal knowledge.",
    "custodian's written certificate": "s.803(6): the record is authenticated by a written certificate of the records custodian.",
    "not prepared in contemplation of litigation": "s.803(6): the record was not prepared in contemplation of litigation.",
    "every requirement is satisfied": "All conditions of s.803(6) are met, so the record is admissible under it.",
}

R_SUST_H = "sustain: inadmissible hearsay"
R_OVER_NH = "overrule: not hearsay"
R_OVER_EX = "overrule: hearsay admissible under an exception"
R_SUST_COMP = "sustain: witness not competent"
R_OVER_COMP = "overrule: witness competent"
R_SUST_CHAIN = "sustain: chain of custody not established"
DEFS_RULING = {
    R_SUST_H: "The evidence is hearsay and no quoted exception admits it.",
    R_OVER_NH: "The evidence falls outside the quoted definition of hearsay.",
    R_OVER_EX: "The evidence is hearsay, but a quoted exception admits it.",
    R_SUST_COMP: "The quoted competence rules bar the witness from testifying.",
    R_OVER_COMP: "Nothing in the quoted competence rules prevents the witness from testifying.",
    R_SUST_CHAIN: "The proponent has not accounted for custody of the item as the quoted rules require.",
}

# Tessary: 28-option menu (27 provisions + none of these)
T_DEFS = {
    "present sense impression": "s.63(1): a statement describing or explaining an event or condition, made while or immediately after the declarant perceived it.",
    "excited utterance": "s.63(2): a statement relating to a startling event or condition, made while the declarant was under the stress of excitement that it caused.",
    "then-existing state of mind or condition": "s.63(3): a statement of the declarant's then-existing state of mind (such as motive, intent, or plan) or emotional, sensory, or physical condition, but not a statement of memory or belief offered to prove the fact remembered or believed.",
    "statement for medical diagnosis or treatment": "s.63(4): a statement made for, and reasonably pertinent to, medical diagnosis or treatment, describing medical history, past or present symptoms, their inception, or their general cause; any part identifying who caused the condition is excluded.",
    "recorded recollection": "s.63(5): a record on a matter the witness once knew but now cannot recall well enough to testify fully and accurately, made or adopted by the witness when the matter was fresh in memory, and shown to reflect the witness's knowledge accurately; it may be read into evidence.",
    "business record": "s.63(6): a record made at or near the time by, or from information transmitted by, someone with knowledge acting in a regularly conducted activity, where making the record was a regular practice, shown by a custodian or certification, absent indications of untrustworthiness.",
    "absence of a business record": "s.63(7): evidence that a matter is not included in records kept under s.63(6), offered to prove that the matter did not occur or exist, if a record was regularly kept for a matter of that kind.",
    "public record": "s.63(8): a record of a public office setting out the office's activities, or a matter observed under a legal duty to report, excluding in a criminal case a matter observed by law-enforcement personnel.",
    "record of vital statistics": "s.63(9): a record of a birth, death, or marriage, if reported to a public office in accordance with a legal duty.",
    "family record": "s.63(13): a statement of fact about personal or family history contained in a family record, such as a Bible, genealogy, chart, engraving on a ring, inscription on a portrait, or engraving on an urn or burial marker.",
    "statement in a document affecting an interest in property": "s.63(15): a statement in a document that purports to establish or affect an interest in property, if the matter stated was relevant to the document's purpose, unless later dealings with the property are inconsistent with it.",
    "ancient document": "s.63(16): a statement in a document prepared at least 30 years before the current proceeding, whose authenticity is established.",
    "market report or commercial publication": "s.63(17): market quotations, lists, directories, or other compilations generally relied on by the public or by persons in particular occupations.",
    "learned treatise": "s.63(18): a statement in a treatise, periodical, or pamphlet established as a reliable authority by expert testimony or judicial notice, called to an expert's attention or relied on by the expert; it may be read but not received as an exhibit.",
    "reputation concerning boundaries": "s.63(20): a reputation in a community, arising before the controversy, concerning boundaries of land in the community or customs affecting that land.",
    "judgment of a previous conviction": "s.63(22): evidence of a final judgment of conviction for a crime punishable by more than one year's imprisonment, offered to prove a fact essential to the judgment.",
    "former testimony": "s.64(1): testimony given as a witness at a trial, hearing, or deposition, if the declarant is now unavailable and the party against whom it is offered had an opportunity and similar motive to develop it by examination.",
    "dying declaration": "s.64(2): in any civil or criminal case, a statement by a declarant who has since died, made while the declarant believed death to be imminent, about its cause or circumstances.",
    "statement against interest": "s.64(3): a statement by an unavailable declarant that was, when made, so contrary to the declarant's pecuniary, proprietary, or penal interest that a reasonable person would have made it only if true.",
    "statement of personal or family history": "s.64(4): a statement by an unavailable declarant about the declarant's own birth, adoption, marriage, divorce, relationship by blood or marriage, or similar fact of the declarant's own personal or family history.",
    "forfeiture by wrongdoing": "s.64(6): a statement offered against a party that wrongfully caused, or acquiesced in wrongfully causing, the declarant's unavailability as a witness, and did so intending that result.",
    "opposing party's statement": "s.62(2): a statement offered against a party that was made by that party in an individual or representative capacity; excluded from the definition of hearsay.",
    "co-conspirator's statement": "s.62(2)(e): a statement offered against a party, made by the party's co-conspirator during and in furtherance of the conspiracy; excluded from the definition of hearsay.",
    "prior inconsistent statement under oath": "s.62(1)(a): a statement of a declarant who testifies and is subject to cross-examination, inconsistent with the testimony, and given under penalty of perjury at a trial, hearing, or deposition; excluded from the definition of hearsay.",
    "prior consistent statement": "s.62(1)(b): a statement of a testifying declarant consistent with the testimony, offered to rebut an express or implied charge of recent fabrication or improper motive; excluded from the definition of hearsay.",
    "prior identification": "s.62(1)(c): a statement of a declarant who testifies and is subject to cross-examination, identifying a person as someone the declarant perceived earlier; excluded from the definition of hearsay.",
    "not offered for its truth": "The statement is offered for a purpose other than proving the truth of the matter asserted, so it is not hearsay under s.60.",
    "none of these": NONE_DEF,
}
T_OPTS = list(T_DEFS.keys())
assert len(T_OPTS) == 28
