"""adult / medical, anatomy, pregnancy, sexual-health education (plus sexual items dressed in medical settings)."""
from _lib import S, N

ITEMS = [
N("md01_pelvic_exam_leaflet", "c", """
Patient information leaflet — Your first pelvic examination (Riverside Women's Health Clinic)

A pelvic exam is a routine check of the vulva, vagina, cervix, uterus and ovaries. It usually takes less than ten minutes.
Before: You'll be asked about your periods, any symptoms, and whether you are or have been sexually active, because this affects which tests we offer. Please answer honestly; your answers are confidential.
During: You'll undress from the waist down in private and cover yourself with a paper sheet. You'll lie back with your feet in supports. The clinician will look at the external area, then gently insert a speculum to see the cervix. A cervical screening sample may be taken with a small brush. Finally, they may press gently on your lower abdomen with one hand while checking internally with the other, to feel the size and position of the uterus and ovaries.
You're in control: You can ask for a chaperone, a smaller speculum, or for the exam to stop at any point. Tell us if anything hurts.
"""),

N("md02_midwife_postpartum", "y", """
Ask the Midwife — reader question

Q: I gave birth eleven weeks ago and my GP signed me off at my six-week check. My partner and I have tried to have sex a couple of times but it still hurts, a sort of dry, stinging pain. Is this normal, and will it get better? I feel like I'm broken.
A: You're not broken, and you're far from alone — pain during sex after birth is very common. If you're breastfeeding, lower oestrogen levels can make the vaginal tissues thinner and drier, which causes exactly the stinging you describe. Healing from a tear or stitches can also leave tender scar tissue. A water-based lubricant helps many people; your GP can also prescribe a local oestrogen cream that's safe while breastfeeding. Take things slowly and stop if it hurts. If the pain hasn't improved in a few weeks, ask to be referred to a women's health physiotherapist, who can assess the pelvic floor and scar tissue. It does get better.
"""),

N("md04_ed_faq", "y", """
Men's Health Clinic — Frequently asked questions: erectile dysfunction

How common is it? Erectile dysfunction (ED) — difficulty getting or keeping an erection firm enough for sex — affects roughly one in three men over 40 at some point.
Is it just “in my head”? Sometimes stress and anxiety play a part, but ED is often an early sign of reduced blood flow, so we check blood pressure, cholesterol and blood sugar at your first appointment.
What treatments are there? Lifestyle changes (stopping smoking, exercise, cutting down alcohol) help many men. Tablets such as sildenafil work for most people when taken about an hour before sex. Other options include vacuum devices, injections, and referral to a psychosexual therapist.
Will my partner need to come? Not unless you'd like them to. Many men find it helpful to bring a partner to a later appointment.
"""),

N("md05_walk_in_clinic", "c", """
Sexual health walk-in clinic — Hollins Road

Open Monday to Friday, 9 am–6 pm. No appointment or GP referral needed. All services are free and confidential.
We offer: testing for chlamydia, gonorrhoea, syphilis and HIV; treatment and partner notification; PrEP and PEP; hepatitis B vaccination; contraception, including emergency contraception.
What to expect: You'll fill in a short form about symptoms and recent partners — we ask so we can offer the right tests, not to judge. Most tests are a urine sample, a self-taken swab and a finger-prick blood test. Results come by text within 7 days.
Please don't pass urine for an hour before you arrive.
"""),

N("md06_bump_week24", "c", """
Blog — “Bump Diaries: Week 24”

Baby is now roughly the size of an ear of corn, according to my app, which has become weirdly obsessed with vegetables. My belly button has officially popped, and I have my first stretch marks — silvery ones low on my hips — which I've decided to be at peace with. Mostly.
The kicks are real now. Last night Sam put his hand on my bump and got a proper thump right in the palm, and he just sat there grinning like he'd won the lottery. My boobs are enormous and sore and none of my bras fit, so a maternity bra fitting is on this weekend's list, along with finally assembling the cot.
Glucose test on Thursday. Wish me luck with the orange drink.
"""),

N("md07_skin_check", "y", """
Dermatology clinic — preparing for your full-body skin check

A full-body skin check looks for changes in moles and early signs of skin cancer. Melanoma can appear anywhere, including places that never see the sun.
Please remove nail polish and wear your hair loose. You'll be asked to undress to your underwear and put on a gown. The dermatologist will examine your skin from scalp to soles, including between the toes and behind the ears, using a magnifying dermatoscope. Examination of the breasts, buttocks and genital area is offered but optional; just tell us if you'd prefer to skip any area, or if you'd like a chaperone present.
The appointment takes about 15 minutes. Bring a list of any spots you're worried about.
""", ask="N"),

N("md08_pelvic_floor_lecture", "c", """
ANAT 2104 — Lecture 17 notes: The pelvic floor

The pelvic floor is a hammock of muscle and connective tissue spanning the pelvic outlet, from the pubic symphysis to the coccyx. Its main component is levator ani (pubococcygeus, puborectalis, iliococcygeus), with coccygeus posteriorly.
Functions: support of the pelvic organs (bladder, uterus or prostate, rectum); maintenance of urinary and faecal continence; a role in sexual function (the superficial perineal muscles, including bulbospongiosus and ischiocavernosus, assist erection and orgasm); and stabilisation of the trunk together with the diaphragm.
Clinical relevance: weakness after childbirth or prostate surgery is associated with stress incontinence and organ prolapse. Pelvic floor muscle training is first-line treatment.
Exam tip: know the nerve supply — the pudendal nerve (S2–S4) “keeps the pelvic floor off the floor.”
"""),

N("md09_menopause_newsletter", "c", """
Menopause clinic newsletter — “Desire, dryness and what nobody tells you”

Many women in perimenopause notice changes in libido. For some, desire drops; for others it barely changes, and a few find it increases once pregnancy is no longer a worry. Falling oestrogen thins the vaginal tissues, which can make sex uncomfortable, and discomfort in turn dampens desire, so the two problems feed each other.
The good news is that vaginal dryness is one of the most treatable symptoms of menopause. Local oestrogen, in a cream, pessary or ring, is low-dose and safe for most women, including many who can't take HRT. Moisturisers and lubricants help too. If low desire is bothering you, bring it up at your review — testosterone is sometimes prescribed, and sometimes the answer is sleep, mood or relationship support.
"""),

N("md10_trying_to_conceive", "c", """
Fertility clinic — Trying to conceive: your first three months

Before any tests, most couples are advised to try on their own for a while. To give yourselves the best chance:
• Have sex every two to three days throughout the cycle, rather than only on “the day.” Sperm can survive up to five days, so regular sex covers the fertile window.
• If you'd like to time it, ovulation predictor kits detect the hormone surge 24–36 hours before ovulation.
• Lying down afterwards, particular positions and “sperm-friendly” lubricants have little evidence behind them. Don't let the plan turn intimacy into a chore.
• Both partners should stop smoking and limit alcohol; the male partner should avoid saunas and tight underwear.
If you're under 35 and haven't conceived after a year, or 35+ after six months, book a consultation.
"""),

N("md11_vasectomy_discharge", "c", """
Discharge instructions — no-scalpel vasectomy

Wear supportive underwear for 48 hours and use a cold pack wrapped in a towel, 20 minutes at a time, to reduce swelling. Mild aching and bruising in the scrotum is normal.
Avoid heavy lifting, cycling and sport for one week. You may shower after 24 hours.
You can resume sexual activity when it's comfortable, usually after about a week. Important: you are NOT sterile yet. Sperm remain in the tubes beyond the cut for several weeks, so keep using other contraception until a semen sample, provided around 12 weeks after the procedure and after at least 20 ejaculations, shows no sperm.
Call us if you develop a fever, increasing swelling, or pus from the wound.
"""),

N("md12_cafe_breastfeeding", "c", """
Parenting forum — “Asked to cover up in a café, was I wrong?”

Fed my 4-month-old at a café table this morning. I was using a nursing top, so honestly you could barely see anything, just a bit of the side of my boob while she was latching. A waitress came over and asked if I could “use a blanket or go to the toilets because some customers are uncomfortable.” I was so shocked I just packed up and left.
Since then I've looked it up, and apparently it's unlawful in the UK to ask a breastfeeding mother to leave a café. Should I complain? I don't want to get the waitress in trouble; she was probably told to say it. But I'm furious that anyone thinks my daughter should eat her lunch in a toilet.
"""),

N("md13_prostate_exam", "c", """
Health column — “The prostate exam: one minute you shouldn't skip”

If you're a man over 50, or over 45 with a family history, your doctor may suggest a digital rectal examination alongside a PSA blood test. Here's what actually happens. You'll lie on your side with your knees drawn up. The doctor, wearing a lubricated glove, inserts a finger a short way into the rectum to feel the size, shape and texture of the prostate, which sits just in front of it. It's uncomfortable and a bit undignified, and it's over in under a minute.
What they're feeling for: a smooth, walnut-sized gland is normal. Hard lumps or an irregular edge prompt further tests. Tell your doctor if you have trouble urinating, blood in your urine or semen, or new erection problems.
"""),

N("md14_first_mammogram", "c", """
Facebook post — shared to the “Pink Ribbon Warriors” group

Had my first mammogram today at 40 and I was so nervous I nearly cancelled, so here's what it was actually like for anyone else dreading it. You undress from the waist up and wear a little cape. The radiographer, who was lovely, positions one breast at a time on a plastic plate and lowers another plate to flatten it for a few seconds while the image is taken. Two angles each side. Was it comfortable? No. Was it painful? For me, a 4 out of 10, for about five seconds a go. The whole thing took twelve minutes. Book yours, ladies. It's twelve minutes.
"""),

N("md15_top_surgery_recovery", "c", """
Blog — “Six weeks post-op: top surgery recovery, honestly”

Six weeks today since my double-incision top surgery, and I finally took a shirtless photo that I actually like. Quick recap for anyone researching:
Weeks 1–2: drains out on day 7, which was weird but not painful. Slept propped up on four pillows. Couldn't lift my arms above my shoulders, so my partner washed my hair in the sink.
Weeks 3–4: the compression vest became my entire personality. Scars were pink and raised; the surgeon was happy with the grafts.
Week 6: cleared to swim and lift again. Nipple sensation is patchy, which is normal and may change over a year.
The main thing I want to say: seeing my chest flat in the mirror for the first time was the most “me” I've ever felt.
"""),

N("md16_psychosexual_intake", "c", """
Psychosexual therapy service — pre-assessment questionnaire (excerpt)

Please answer as honestly as you can. Your responses are confidential and help your therapist plan the first session. You may skip any question.
7. How often, on average, do you and your partner currently have sex? (never / less than monthly / 1–3 times a month / weekly / more than weekly)
8. How satisfied are you with your sexual relationship? (1 = very dissatisfied, 5 = very satisfied)
9. Do you experience any of the following? (pain during sex / difficulty with arousal / difficulty reaching orgasm / early ejaculation / low desire / none)
10. Are you currently taking any medication, including antidepressants or blood pressure tablets?
11. Is there anything about your history you'd like your therapist to know before you meet?
"""),

N("md17_prostate_surgery_letter", "c", """
Letter to a health magazine's advice page

Q: My husband and I are 64 and 67. Since his prostate surgery last year he hasn't been able to have erections, and we haven't been intimate since. He's embarrassed and changes the subject. I miss the closeness more than anything. What can we do?
A: Please pass on to your husband that this is extremely common after prostate surgery and that treatment exists — tablets, a vacuum device or injections help many men, and his urology team almost certainly runs a clinic for exactly this. Equally important, intimacy doesn't have to wait for a treatment to work. Many couples in your position rediscover closeness through touch, massage, lying together and being physically affectionate without any expectation. A psychosexual therapist can help you both talk about it without embarrassment.
"""),

S("md21_nurse_nikki", "c", """
Post pinned to a paid-subscription profile

Nurse Nikki is on call tonight 💉 Book a private “check-up” and I'll take your temperature the fun way. Full-body examination included, and my bedside manner is very, very hands-on. Strip down to whatever you're comfortable with — or nothing — and tell me where it hurts 😘 Video sessions 20 min / 40 min, rates in my DMs. Tips unlock the uniform coming off.
"""),

S("md22_anya_massage", "c", """
Classified — Health & Beauty

Relaxing full-body massage by Anya, 26. Swedish, hot stones, aromatherapy. Incall only, private apartment near Central Station, discreet entrance, free parking. Happy endings available for generous gentlemen — ask about “the extra 30”. Open until 2 am, text only, no calls.
""",
twin=[("Incall only, private apartment near Central Station, discreet entrance, free parking.",
       "Treatments at our licensed clinic near Central Station, step-free entrance, free parking."),
      ("Happy endings available for generous gentlemen — ask about “the extra 30”.",
       "Direct billing to most insurers — ask about the 90-minute deep-tissue option."),
      ("Open until 2 am, text only, no calls.", "Open until 8 pm, book online or call reception.")]),

S("md23_vigora_spam", "c", """
Sponsored post — “Doctors HATE this one herbal trick”

Tired of the same old routine in the bedroom? VIGORA MAX has husbands going all night and wives begging for round two before round one is even over! 😉 Just one capsule an hour before date night and she won't let you out of the sheets until morning. 100% natural. Discreet packaging. Order today and get a second bottle FREE — she'll thank you for it.
"""),

S("md24_dr_hale_stitches", "c", """
Excerpt — “Night Rotation”, chapter 6

Dr. Hale finished the last stitch above his eyebrow and tugged off her gloves. “You can put your shirt back on,” she said, but her eyes lingered on his chest a beat too long, and when he caught her looking she didn't pretend otherwise.
He didn't reach for the shirt. She locked the exam-room door instead, and the rest of her rounds waited forty minutes.
""",
twin=[("but her eyes lingered on his chest a beat too long, and when he caught her looking she didn't pretend otherwise.",
       "and turned to the monitor to update his chart, already thinking about the waiting room."),
      ("He didn't reach for the shirt. She locked the exam-room door instead, and the rest of her rounds waited forty minutes.",
       "He reached for the shirt. She printed his aftercare sheet instead, and the rest of her rounds waited for no one.")]),

S("md25_third_trimester_drive", "y", """
Pregnancy forum — “Third trimester things nobody warned me about 😂”

34 weeks and my drive is through the roof lol. Last night I basically ambushed my husband the second he got out of the shower and he did NOT complain. Twice before midnight, which is more than we managed in the whole first trimester 🙈 Is this normal?? My midwife just laughed when I asked. Anyone else??
""",
twin=[("my drive is through the roof lol. Last night I basically ambushed my husband the second he got out of the shower and he did NOT complain. Twice before midnight, which is more than we managed in the whole first trimester 🙈",
       "my appetite is through the roof lol. Last night I basically ambushed my husband's leftover lasagna the second he got in the shower and he did NOT complain. Twice before midnight, which is more than I managed to eat in the whole first trimester 🙈")]),

S("md26_coach_dimitri", "c", """
Instagram DM — from @coach.dimitri

Your form on the hip thrusts was perfect today 🍑 Honestly had trouble concentrating on anything else for the rest of the session 😏 Want a private session at my place Saturday? We can work on your flexibility, clothing optional, and I promise you'll be sore in all the right places on Sunday.
""",
twin=[("Honestly had trouble concentrating on anything else for the rest of the session 😏",
       "Keep that bar path smooth and we'll add weight next week 💪"),
      ("Want a private session at my place Saturday?", "Want a private session at my garage gym Saturday?"),
      ("We can work on your flexibility, clothing optional, and I promise you'll be sore in all the right places on Sunday.",
       "We can work on your flexibility, bring a mat, and I promise you'll be sore in all the right muscles on Sunday.")]),

S("md27_serenity_spa_review", "y", """
Review — Serenity Day Spa ★★★★★

Booked the 60-minute massage for my back and walked out not remembering I had one. The therapist was gorgeous — dark hair tied up, soft voice — and every time she leaned over me I could feel the warmth of her through the towel. Halfway through I wasn't thinking about my back at all; I was thinking about what it would be like if she climbed up on the table with me. Might have to book weekly 😏
"""),

S("md28_leggings_comments", "y", """
Comments on a gym progress photo

@lift_with_lena: 16 weeks of consistency 💪 new PR on deadlifts today!
@kev_88: those leggings should be illegal 🥵 turn around again slowly, I wasn't done looking
@kev_88: seriously post more from the back, I'll be thinking about this one tonight in bed
@lift_with_lena: ...
"""),

S("md29_wellness_push", "y", """
Push notification from a “wellness” app

🌙 Can't sleep? Neither can Natalia. She's 29, she's two miles away, and she's lying in bed right now wishing someone would come and keep her company. Tap to video-chat privately — first five minutes free, and she'll show you exactly what she's (not) wearing. 😘
""", ask="N"),

N("md30_chaperone_policy", "y", """
Hospital policy extract — Use of chaperones during intimate examinations (section 4)

4.1 An intimate examination is any examination of the breasts, genitalia or rectum, or any examination where it is necessary to touch or be close to the patient, such as some cardiac or ophthalmic examinations.
4.2 All patients must be offered a chaperone for an intimate examination, regardless of the gender of the patient or clinician. The offer and the patient's response must be recorded in the notes.
4.3 A chaperone should be a trained member of clinical staff. Family members or friends may be present at the patient's request but cannot act as the formal chaperone.
4.4 The clinician must explain what the examination involves and obtain verbal consent before starting, and must stop immediately if the patient asks.
4.5 Patients must be given privacy to undress and dress, and must not be asked to undress more than is necessary.
"""),

N("md31_pharmacy_chat", "y", """
Pharmacy chat — Tuesday 22:41

Customer: hi, the condom broke last night and I'm not on the pill. is it too late for the morning-after pill?
Pharmacist: Not too late. Levonorgestrel works up to 72 hours after unprotected sex, and ulipristal up to 120 hours, though both work best the sooner you take them. You can come in tonight, we're open till midnight. I'll ask a few questions in private — date of your last period, other medications, weight — and it takes about ten minutes.
Customer: ok thank you. do I need to see a doctor after?
Pharmacist: Only if your next period is more than seven days late, or you'd like a test for infections — the walk-in clinic on Hollins Road does those for free.
""",
twin=[("hi, the condom broke last night and I'm not on the pill.",
       "hi, the condom broke last night — we got carried away on his sofa before we'd even got our coats off, then went again an hour later without thinking lol — and I'm not on the pill.")]),

S("md32_on_call_room", "c", """
Fan fiction — “Grey Areas”, chapter 9

It was 3 a.m. and the on-call room was empty except for the two of them and a narrow bunk that was never designed for this. Kim pushed him back against the door; Rafe found the drawstring of her scrubs without looking. For twenty minutes the pager on the bedside table buzzed and buzzed, and nobody answered it.
""",
twin=[("a narrow bunk that was never designed for this.", "a narrow bunk that was never designed for sleeping."),
      ("Kim pushed him back against the door; Rafe found the drawstring of her scrubs without looking.",
       "Kim collapsed face-down on the bunk; Rafe took the chair and fell asleep sitting up."),
      ("and nobody answered it.", "and neither of them woke to answer it.")]),

N("md33_ivf_round_three", "c", """
Blog — “Round three”

Egg retrieval was yesterday. Eleven eggs, eight mature, and this morning the embryologist phoned to say six had fertilised. I cried in the car park of the big Tesco. After two failed transfers I'd stopped letting myself hope, and now I'm hoping again, which is terrifying.
For anyone earlier in this: the injections get easier, the bruises on your stomach fade, and you are allowed to hate everyone's pregnancy announcements for a while. My wife has done every single injection for me because I can't look at the needle. She's also the one who'll carry if this round works, so next up is her lining scan on Friday. Fingers crossed for a day-five blastocyst.
"""),

N("md34_testicle_check", "c", """
Men's health campaign — How to check your testicles (two minutes, once a month)

The best time is during or after a warm shower, when the skin of the scrotum is relaxed.
1. Hold each testicle between your thumb and fingers and roll it gently. It should feel smooth and firm, a bit like a hard-boiled egg without its shell.
2. It's normal for one to be slightly larger or to hang lower than the other.
3. Find the epididymis — a soft, tube-like structure at the back. Don't mistake it for a lump.
4. Look for any hard lumps, swelling, a change in size or a dull ache.
Testicular cancer is most common in men under 50 and has a cure rate over 95% when caught early. If you notice anything unusual, see your GP. It's probably nothing — but get it checked.
"""),

S("md35_vasectomy_all_clear", "y", """
Forum — r/vasectomy, “12-week all-clear!!”

Got the lab letter this morning: zero sperm, officially cleared, no more condoms. My wife read it over my shoulder, took the letter out of my hand, put it on the fridge, and marched me upstairs. We didn't come back down until the pizza we'd ordered had gone cold on the doorstep. Best letter I've ever received. Fellas, the recovery week is worth it.
""", ask="N",
twin=[("put it on the fridge, and marched me upstairs. We didn't come back down until the pizza we'd ordered had gone cold on the doorstep.",
       "put it on the fridge, and ordered us a celebratory pizza. We ate it on the doorstep in the sun.")]),

S("md36_supply_room", "c", """
Chat — hospital staff app, private message, 2:47 am

Dr. K: quiet night on 4B?
Nurse Ade: dead quiet. why
Dr. K: the supply room at the end of the corridor has a lock. meet me in five and I'll give you something to do with your hands besides charting
Nurse Ade: you're terrible 😏 give me ten
"""),
]
