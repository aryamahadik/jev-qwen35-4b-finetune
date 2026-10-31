"""packs-2 sector ed: education administration (Claude-written pack sources; invented schools and entities)."""

PACKS = [
dict(slot="ed-01", slug="pd-credits", sector="education_admin",
     sub="professional development credit approvals for a school district's teachers",
     org="Wexmoor Unified School District", desk="professional learning office",
     setting="A school district awards professional development credits that count toward teacher salary steps. "
             "The professional learning office checks each credit claim against the district's credit rules "
             "before the credits post to a teacher's record.",
     decider="instructional coordinator",
     roles="credit registrar; curriculum director; building principal; union representative; payroll liaison; "
           "workshop facilitator",
     docs="credit claim form; certificate of completion; workshop agenda; salary step table; transcript extract; "
          "credit policy handbook",
     scope=("school level", "Elementary; Middle; High; Alternative Program"),
     money="dollars",
     ents=[
        dict(key="claim", singular="credit claim", plural="credit claims", id="CC", aka="PD claim",
             attrs="""
             contact_hours | dec1 | 1.0..90.0 hours | aka=seat time
             credits_claimed | dec1 | 0.5..6.0 credits | aka=credits sought
             course_fee | money | 0.00..1800.00 | aka=registration cost
             days_since_completion | int | 0..400 days | aka=time since the course ended
             provider_type | cat | district workshop; university course; online module; conference; peer observation
             subject_link | cat | literacy; mathematics; science; special education; technology; leadership
             relevance_level | ord | general; related; core subject | aka=link to teaching duties
             certificate_attached | state | bad=0 | aka=completion certificate on file | grp=proof
             principal_endorsed | event | bad=0 | aka=principal signed the claim
             district_paid_fee | event | bad=0 | aka=district covered the fee
             hours_verified | event | bad=0 | aka=attendance hours confirmed | grp=proof
             counted_elsewhere | state | bad=1 | aka=hours already used for another credit
             completed_on | date
             submitted_on | date
             claim_tags | tag | summer session; evening course; mentor credit; graduate level; repeat topic
             """),
        dict(key="teacher", singular="teacher", plural="teachers", id="TC", names="person", role="person",
             attrs="""
             credits_this_cycle | dec1 | 0.0..30.0 credits | aka=credits earned this cycle
             salary_step | int | 1..15 units | aka=pay step
             tenure_status | ord | probationary; continuing; tenured | aka=employment status
             """),
        dict(key="provider", singular="course provider", plural="course providers", id="CP",
             names="org: Institute, College, Academy, Learning Center",
             attrs="""
             district_approved | state | bad=0 | aka=an approved provider
             courses_run | int | 1..200 items | aka=courses offered
             """),
     ],
     outcomes=["post credits; post partial credits; send to curriculum director; return for certificate*; "
               "reject claim*",
               "count toward salary step; count toward license renewal; count for both; void the credits*"],
     levels=["general; related; core subject", "low; moderate; high"],
     words="""
     intensive: contact_hours >= 30
     brief: contact_hours < 3
     ambitious: credits_claimed >= 3
     lavish: course_fee >= 600
     stale: days_since_completion >= 180
     certified: certificate_attached
     blessed: principal_endorsed
     sponsored: district_paid_fee
     attested: hours_verified
     accredited: district_approved
     prolific: credits_this_cycle >= 15
     veteran: salary_step >= 10
     technical: subject_link == technology
     academic: provider_type == university course
     pertinent: relevance_level == core subject
     redundant: counted_elsewhere
     """,
     cues="lacks a completion certificate => certificate_attached=false; was never endorsed by the principal => "
          "principal_endorsed=false; is not an approved provider => district_approved=false",
     links="claim > teacher: credits / credited by; claim > provider: cites / cited by",
     actions="post = record; verify = confirm hours; endorse = sign; return = send back",
     sources="credit registrar log; principal email; provider transcript; payroll report; teacher portal; "
             "workshop sign-in sheet",
     inert="""
     lanyard_colour | cat | navy; lime; grey
     parking_spot | cat | spot 4; spot 9; spot 12
     staffroom_kettle | cat | electric; stovetop
     bulletin_board_theme | cat | autumn; reading; space
     hallway_bench | cat | oak; pine
     """,
     affix="unendorsed => principal_endorsed; unverified => hours_verified"),

dict(slot="ed-02", slug="student-teaching", sector="education_admin",
     sub="placement office matching student teachers to host classrooms",
     org="Halvorsen College of Education", desk="field placement office",
     setting="A college of education places its student teachers in partner school classrooms for a semester. "
             "The field placement office applies the program's placement and clearance rules to each candidate.",
     decider="education professor",
     roles="placement coordinator; university supervisor; host teacher; school principal; program chair; "
           "clearance clerk",
     docs="placement application; clearance record; host teacher agreement; supervision log; evaluation form; "
          "partnership agreement",
     scope=("partner district", "Brookhollow; Carrick Falls; Dunlevy; Elmstead; Foxmere"),
     money="dollars",
     ents=[
        dict(key="placement", singular="placement application", plural="placement applications", id="PA",
             aka="placement",
             attrs="""
             gpa | dec2 | 2.00..4.00 points | aka=grade point average
             field_hours_completed | int | 0..200 hours | aka=practicum hours
             commute_minutes | int | 5..90 minutes | aka=travel time to school
             program_fee | money | 0.00..900.00 | aka=placement fee
             certification_area | cat | early childhood; elementary; secondary math; secondary English; special education; music
             grade_band | cat | pre-K to 2; grades 3 to 5; grades 6 to 8; grades 9 to 12
             readiness_rating | ord | developing; proficient; distinguished | aka=readiness
             background_check_cleared | event | bad=0 | aka=background check passed | grp=clearance
             tb_test_on_file | state | bad=0 | aka=health screening on file | grp=clearance
             licensure_exam_passed | event | bad=0 | aka=content exam passed
             has_own_transport | state | bad=0 | aka=can drive to the school
             relative_at_school | state | bad=1 | aka=family member works at the school
             applied_on | date
             term_starts_on | date
             placement_tags | tag | bilingual; rural; urban; co-teaching; second placement; career changer
             """),
        dict(key="candidate", singular="student teacher", plural="student teachers", id="SK", names="person",
             role="person",
             attrs="""
             earlier_placements | int | 0..2 items | aka=past placements
             credits_completed | int | 60..140 credits | aka=credit hours earned
             """),
        dict(key="host", singular="host teacher", plural="host teachers", id="HT", names="person", role="person",
             attrs="""
             years_teaching | int | 3..35 years | aka=teaching experience
             mentor_trained | event | bad=0 | aka=mentor course finished
             """),
     ],
     outcomes=["place with host teacher; place at second choice school; send to program chair; "
               "defer to next term*; hold for clearance*",
               "full-time placement; split placement; observation only*"],
     levels=["developing; proficient; distinguished", "low; medium; high"],
     words="""
     strong: gpa >= 3.50
     marginal: gpa < 2.75
     seasoned: field_hours_completed >= 100
     distant: commute_minutes >= 60
     vetted: background_check_cleared
     fit: tb_test_on_file
     qualified: licensure_exam_passed
     mobile: has_own_transport
     conflicted: relative_at_school
     veteran: years_teaching >= 15
     coached: mentor_trained
     advanced: credits_completed >= 120
     adaptive: certification_area == special education
     nursery: grade_band == pre-K to 2
     polished: readiness_rating == distinguished
     dear: program_fee >= 500
     """,
     cues="lacks a cleared background check => background_check_cleared=false; has no health screening on file => "
          "tb_test_on_file=false; was never trained as a mentor => mentor_trained=false",
     links="placement > candidate: names / named by; placement > host: assigns / assigned by",
     actions="place = assign school; defer = postpone; clear = approve checks; pair = match up",
     sources="clearance record; principal email; host teacher survey; candidate portfolio; supervisor note; "
             "registrar report",
     inert="""
     portfolio_binder | cat | blue binder; black binder
     campus_shuttle_stop | cat | north stop; south stop
     cafeteria_day | cat | taco day; pasta day; soup day
     classroom_door_colour | cat | red door; green door
     orientation_room | cat | hall A; hall B
     """,
     affix="uncleared => background_check_cleared; untrained => mentor_trained"),

dict(slot="ed-03", slug="substitute-dispatch", sector="education_admin",
     sub="substitute teacher dispatch for daily absences across a district",
     org="Coldharbour Public Schools", desk="substitute dispatch office",
     setting="When teachers are absent, a district's dispatch office fills each absence with a short-term "
             "substitute. The office applies the district's assignment order, pay and qualification rules to every "
             "absence.",
     decider="substitute teacher",
     roles="dispatch clerk; building secretary; human resources partner; principal; payroll clerk; "
           "lead substitute",
     docs="absence record; substitute roster; assignment log; daily pay sheet; lesson plan note; "
          "qualification list",
     scope=("building", "Ashby Elementary; Birchmont Middle; Calder High; Dunmore Academy; Elgin Center"),
     money="dollars",
     ents=[
        dict(key="absence", singular="absence", plural="absences", id="AB", aka="vacancy",
             attrs="""
             hours_notice | int | 0..240 hours | aka=notice given
             days_long | int | 1..60 days | aka=length of the absence
             periods_to_cover | int | 1..8 items | aka=class periods
             daily_rate | money | 90.00..260.00 | aka=pay per day
             subject_area | cat | general classroom; mathematics; science; languages; physical education; special education
             absence_reason | cat | illness; training; family leave; jury duty; personal day
             coverage_urgency | ord | routine; same day; immediate | aka=urgency
             lesson_materials_left | state | bad=0 | aka=materials left by the teacher | grp=handover
             license_required | state | bad=1 | aka=certified cover needed
             filled_by_noon | event | bad=0 | aka=covered by midday
             internal_cover_offered | event | bad=0 | aka=staff member offered to cover
             posted_on | date
             starts_on | date
             absence_tags | tag | long term; half day; field trip; exam day; testing week; new teacher
             """),
        dict(key="substitute", singular="substitute", plural="substitutes", id="SB", names="person", role="person",
             attrs="""
             days_worked_this_year | int | 0..180 days | aka=days worked
             rating_average | dec1 | 1.0..5.0 points | aka=principal rating
             certified_teacher | state | bad=0 | aka=holds a teaching license
             """),
        dict(key="school", singular="school", plural="schools", id="SC",
             names="org: Elementary, Middle School, High School, Academy",
             attrs="""
             vacancies_today | int | 0..20 items | aka=open absences today
             priority_band | ord | standard; hard to staff; critical | aka=staffing band
             """),
     ],
     outcomes=["assign first available; assign preferred substitute; use internal cover; "
               "send to principal; leave vacant*",
               "pay daily rate; pay long-term rate; pay half day; pay after review*"],
     levels=["routine; same day; immediate", "standard; hard to staff; critical"],
     words="""
     last-minute: hours_notice < 12
     forewarned: hours_notice >= 72
     extended: days_long >= 10
     heavy: periods_to_cover >= 6
     generous: daily_rate >= 200
     prepared: lesson_materials_left
     settled: filled_by_noon
     regular: days_worked_this_year >= 100
     admired: rating_average >= 4.5
     credentialed: certified_teacher
     strained: vacancies_today >= 8
     athletic: subject_area == physical education
     urgent: coverage_urgency == immediate
     ailing: absence_reason == illness
     specialized: license_required
     collegial: internal_cover_offered
     """,
     cues="left no lesson materials => lesson_materials_left=false; holds no teaching license => certified_teacher=false; "
          "was never covered by midday => filled_by_noon=false",
     links="absence > substitute: assigns / assigned by; absence > school: occurs at / chosen by",
     actions="dispatch = send out; fill = cover; post = list; confirm = verify",
     sources="dispatch system; building secretary call; substitute text reply; principal email; payroll sheet; "
             "absence hotline",
     inert="""
     sign_in_pen | cat | blue pen; black pen
     visitor_sticker | cat | round sticker; square sticker
     car_park_side | cat | front lot; rear lot
     bell_tone | cat | chime; buzzer
     mailbox_row | cat | top row; bottom row
     """,
     affix="unlicensed => certified_teacher; unfilled => filled_by_noon"),

dict(slot="ed-04", slug="registration-overrides", sector="education_admin",
     sub="registrar's petition desk for course overrides and late add or drop",
     org="Tidewater State University", desk="registrar's petition desk",
     setting="A university registrar reviews student petitions to add courses after the deadline, exceed credit "
             "limits or skip prerequisites. The petition desk applies the academic calendar and override rules "
             "and decides each petition's outcome.",
     decider="postsecondary education administrator",
     roles="petition reviewer; academic advisor; department chair; course instructor; financial aid liaison; "
           "associate registrar",
     docs="petition form; academic calendar; prerequisite map; override authorization; transcript; "
          "fee adjustment notice",
     scope=("college", "Arts and Sciences; Engineering; Business; Nursing; Education"),
     money="dollars",
     ents=[
        dict(key="petition", singular="registration petition", plural="registration petitions", id="RP",
             aka="override petition",
             attrs="""
             days_past_deadline | int | 0..60 days | aka=days late
             credits_after_change | int | 3..24 credits | aka=credit load after the change
             section_seats_left | int | 0..30 seats | aka=open seats
             late_fee | money | 0.00..250.00 | aka=late registration fee
             petition_kind | cat | late add; late drop; credit overload; prerequisite waiver; section swap; time conflict
             class_standing | ord | first year; second year; third year; final year | aka=year in school
             instructor_approved | event | bad=0 | aka=instructor signed | grp=approvals
             advisor_approved | event | bad=0 | aka=advisor signed | grp=approvals
             attended_first_week | event | bad=0 | aka=went to the first week of class
             financial_hold | state | bad=1 | aka=account hold in place
             academic_probation | state | bad=1 | aka=on probation
             filed_on | date
             term_start | date
             petition_tags | tag | athlete; veteran; international; medical; graduating senior; transfer
             """),
        dict(key="student", singular="student", plural="students", id="SN", names="person", role="person",
             attrs="""
             gpa | dec2 | 0.00..4.00 points | aka=cumulative GPA
             petitions_this_year | int | 0..6 items | aka=petitions filed this year
             """),
        dict(key="course", singular="course section", plural="course sections", id="CS",
             names=["Section HIST 210-02", "Section CHEM 101-05", "Section MATH 241-01", "Section ECON 300-03", "Section NURS 220-01", "Section ARTS 115-04", "Section BUSN 330-02", "Section ENGR 205-06"],
             attrs="""
             enrolled_count | int | 5..300 students | aka=students enrolled
             queue_length | int | 0..40 students | aka=students queued
             delivery_mode | cat | in person; online; hybrid | aka=teaching mode
             """),
     ],
     outcomes=["approve petition; approve with late fee*; send to department chair; return for signatures*; "
               "reject petition*",
               "add course; drop course; swap section; keep schedule as is*"],
     levels=["first year; second year; third year; final year", "low; medium; high"],
     words="""
     tardy: days_past_deadline >= 14
     prompt: days_past_deadline <= 2
     swamped: credits_after_change >= 19
     light: credits_after_change <= 9
     full: section_seats_left < 1
     sanctioned: instructor_approved
     advised: advisor_approved
     present: attended_first_week
     frozen: financial_hold
     struggling: gpa < 2.00
     distinguished: gpa >= 3.70
     crowded: queue_length >= 15
     outgoing: class_standing == final year
     precarious: academic_probation
     penalized: late_fee >= 100
     ambitious: petition_kind == credit overload
     """,
     cues="lacks the instructor's signature => instructor_approved=false; never attended the first week => "
          "attended_first_week=false; has no account hold in place => financial_hold=false",
     links="petition > student: names / named by; petition > course: targets / targeted by",
     actions="approve = grant; override = force add; adjust = change fees; route = send on",
     sources="petition form; student portal; instructor email; advisor note; bursar report; class roster",
     inert="""
     counter_ticket_number | cat | ticket 12; ticket 40; ticket 77
     campus_flag | cat | blue flag; gold flag
     registrar_plant | cat | fern; succulent
     wall_poster | cat | campus map; library hours
     counter_mat | cat | rubber mat; carpet mat
     """,
     affix="unsigned => instructor_approved; unadvised => advisor_approved"),

dict(slot="ed-05", slug="interlibrary-loans", sector="education_admin",
     sub="interlibrary loan desk at a college library",
     org="Kettering Hill College Library", desk="interlibrary loan desk",
     setting="A college library borrows books and article copies from other libraries for its students and staff. "
             "The interlibrary loan desk applies the lending network's rules, fees and limits to each borrowing "
             "slip.",
     decider="library technician",
     roles="loan clerk; access services librarian; lending partner contact; mail room clerk; copyright officer; "
           "student worker",
     docs="borrowing slip; lending partner policy; copyright log; shipping label; overdue notice; invoice",
     scope=("lending network", "State Consortium; Regional Network; National Network; International Partner"),
     money="dollars",
     ents=[
        dict(key="loan", singular="borrowing slip", plural="borrowing slips", id="BS", aka="loan file",
             attrs="""
             lending_fee | money | 0.00..60.00 | aka=partner fee
             pages_to_copy | int | 0..400 pages | aka=pages for scanning
             days_needed_by | int | 1..60 days | aka=time until needed
             renewals_used | int | 0..3 entries | aka=renewals so far
             item_format | cat | book; article copy; thesis; media disc; book chapter
             patron_class | cat | undergraduate; graduate; faculty; staff; alumni
             delivery_speed | ord | standard; express; rush | aka=delivery level
             owned_locally | state | bad=1 | aka=already held by the library
             copyright_limit_reached | state | bad=1 | aka=copy limit for the journal used up
             partner_confirmed | event | bad=0 | aka=lender accepted | grp=lender
             item_returned_late_before | event | bad=1 | aka=patron returned a loan late before
             submitted_on | date
             due_back_on | date
             loan_tags | tag | thesis research; course reserve; rare item; oversize; foreign language
             """),
        dict(key="patron", singular="patron", plural="patrons", id="PN", names="person", role="person",
             attrs="""
             open_loans | int | 0..20 items | aka=loans out now
             fines_owed | money | 0.00..120.00 | aka=fines balance
             """),
        dict(key="lender", singular="lending library", plural="lending libraries", id="RB",
             names="org: University Library, Public Library, College Library",
             attrs="""
             fill_rate | dec1 | 40.0..99.0 percent | aka=share of loans filled
             reciprocal_agreement | state | bad=0 | aka=fee-free agreement in place
             """),
     ],
     outcomes=["send to lender; buy a copy instead; point to local holding; send to access librarian; "
               "cancel borrowing slip*",
               "ship by mail; send by courier; deliver electronically; pay rush fee*"],
     levels=["standard; express; rush", "low; medium; high"],
     words="""
     pricey: lending_fee >= 25
     bulky: pages_to_copy >= 100
     urgent: days_needed_by <= 3
     relaxed: days_needed_by >= 21
     extended: renewals_used >= 1
     duplicate: owned_locally
     exhausted: copyright_limit_reached
     secured: partner_confirmed
     busy: open_loans >= 10
     indebted: fines_owed >= 20
     reliable: fill_rate >= 90
     scholarly: patron_class == faculty
     digital: item_format == article copy
     hasty: delivery_speed == rush
     slack: item_returned_late_before
     """,
     cues="was never accepted by the lender => partner_confirmed=false; lacks an agreement on fees => "
          "reciprocal_agreement=false; holds no local copy => owned_locally=false",
     links="loan > patron: serves / served by; loan > lender: borrows from / lent to",
     actions="borrow = obtain; renew = extend; ship = mail; scan = digitize",
     sources="loan system; lender email; patron account; mail room log; copyright log; catalog search",
     inert="""
     bookmark_design | cat | owl bookmark; star bookmark
     carrel_number | cat | carrel 3; carrel 8; carrel 15
     book_drop_side | cat | east bin; west bin
     reading_lamp | cat | green shade; white shade
     tote_bag_colour | cat | canvas; black
     """,
     affix="unconfirmed => partner_confirmed; unreturned => item_returned_late_before"),

dict(slot="ed-06", slug="regrade-extensions", sector="education_admin",
     sub="teaching assistant desk handling regrade and assignment extension petitions",
     org="Ostrander Institute of Technology", desk="course operations desk",
     setting="A large university course runs a course operations desk staffed by teaching assistants. The desk "
             "applies the syllabus rules to each regrade or extension petition and decides when the instructor "
             "must rule.",
     decider="postsecondary teaching assistant",
     roles="head teaching assistant; course instructor; accessibility services liaison; grader; "
           "academic integrity officer; section leader",
     docs="syllabus; petition form; grading rubric; extension log; gradebook export; accommodation letter",
     scope=("course", "Intro Statistics; Organic Chemistry; Data Structures; Microeconomics"),
     money="dollars",
     ents=[
        dict(key="petition", singular="student petition", plural="student petitions", id="SP",
             aka="regrade or extension petition",
             attrs="""
             points_contested | dec1 | 0.5..30.0 points | aka=points disputed
             days_extension_sought | int | 0..14 days | aka=extra days sought
             hours_before_due | int | 0..168 hours | aka=time before the due date
             assignment_weight | dec1 | 1.0..40.0 percent | aka=share of the final grade
             makeup_exam_fee | money | 0.00..60.00 | aka=fee for a makeup sitting
             petition_kind | cat | regrade; extension; makeup exam; excused absence
             evidence_kind | cat | medical note; travel letter; family notice; accommodation letter; written statement only
             grade_band | ord | failing; passing; good; excellent | aka=current grade band
             rubric_error_found | state | bad=0 | aka=grader used the wrong rubric line
             accommodation_on_file | state | bad=0 | aka=formal accommodation on file
             submitted_on_time | event | bad=0 | aka=filed before the deadline
             earlier_extension_granted | event | bad=1 | aka=extension already given this term
             filed_on | date
             assignment_due | date
             petition_tags | tag | group project; final exam; lab report; quiz; take-home
             """),
        dict(key="student", singular="student", plural="students", id="ST", names="person", role="person",
             attrs="""
             petitions_this_term | int | 0..6 items | aka=petitions this term
             course_average | dec1 | 0.0..100.0 percent | aka=running average
             """),
        dict(key="grader", singular="grader", plural="graders", id="GR", names="person", role="person",
             attrs="""
             papers_graded | int | 0..400 items | aka=papers marked
             calibration_done | event | bad=0 | aka=grader calibration finished
             """),
     ],
     outcomes=["grant petition; grant in part; send to instructor; return for evidence*; "
               "reject petition*",
               "adjust score up; leave score; adjust score down*"],
     levels=["failing; passing; good; excellent", "low; medium; high"],
     words="""
     sizable: points_contested >= 10
     trivial: points_contested < 2
     lengthy: days_extension_sought >= 7
     eager: hours_before_due >= 48
     weighty: assignment_weight >= 20
     faulty: rubric_error_found
     entitled: accommodation_on_file
     punctual: submitted_on_time
     repeat: earlier_extension_granted
     frequent: petitions_this_term >= 3
     strong: course_average >= 90
     aligned: calibration_done
     clinical: evidence_kind == medical note
     floundering: grade_band == failing
     absentee: petition_kind == excused absence
     """,
     cues="was never filed before the deadline => submitted_on_time=false; lacks a formal accommodation => "
          "accommodation_on_file=false; has no rubric mistake in it => rubric_error_found=false",
     links="petition > student: names / named by; petition > grader: cites / cited by",
     actions="regrade = remark; extend = grant time; excuse = clear absence; refer = pass on",
     sources="petition form; gradebook export; instructor email; accommodation letter; grader note; "
             "course forum post",
     inert="""
     lecture_hall_row | cat | row C; row K; row P
     whiteboard_colour | cat | green board; white board
     help_room_number | cat | room 101; room 214
     laptop_sticker | cat | rocket; cat; planet
     backpack_brand | cat | brand U; brand V
     """,
     affix="unaccommodated => accommodation_on_file; untimely => submitted_on_time"),

dict(slot="ed-07", slug="esl-placement", sector="education_admin",
     sub="adult English language program placement and enrolment",
     org="Riverside Adult Learning Center", desk="adult program enrolment desk",
     setting="An adult learning center places new learners into English language classes by test score and "
             "goals. The enrolment desk applies the program's placement and seat rules and decides each learner's "
             "class.",
     decider="adult language instructor",
     roles="enrolment clerk; testing proctor; program coordinator; childcare aide; volunteer tutor; "
           "outreach worker",
     docs="intake form; placement test report; class roster; attendance record; learner goals sheet; "
          "funding report",
     scope=("site", "Main Center; Library Branch; Community Hall; Evening Annex"),
     money="dollars",
     ents=[
        dict(key="enrolment", singular="enrolment file", plural="enrolment files", id="ER", aka="intake file",
             attrs="""
             placement_score | int | 150..260 points | aka=placement test score
             weeks_waiting | int | 0..26 weeks | aka=wait so far
             free_hours_weekly | int | 2..20 hours | aka=study hours per week
             materials_fee | money | 0.00..80.00 | aka=book fee
             preferred_time | cat | morning; afternoon; evening; weekend
             learner_goal | cat | work; citizenship; family literacy; further study; daily life
             placement_level | ord | beginning; low intermediate; high intermediate; advanced | aka=class level
             test_completed | event | bad=0 | aka=placement test taken | grp=testing
             childcare_needed | state | bad=1 | aka=needs childcare to attend
             residency_proof_seen | event | bad=0 | aka=proof of local address shown
             returning_learner | state | bad=0 | aka=studied here before
             employer_sponsored | state | bad=0 | aka=employer pays
             intake_on | date
             class_starts_on | date
             enrolment_tags | tag | refugee; evening shift; youth; senior; online only; job training
             """),
        dict(key="learner", singular="learner", plural="learners", id="KR", names="person", role="person",
             attrs="""
             years_schooling | int | 0..20 years | aka=years of schooling
             attendance_rate | dec1 | 0.0..100.0 percent | aka=past attendance
             """),
        dict(key="class", singular="class section", plural="class sections", id="CX",
             names=["Section Heron", "Section Kestrel", "Section Plover", "Section Wren", "Section Finch", "Section Swift", "Section Tern", "Section Martin"],
             attrs="""
             seats_open | int | 0..25 seats | aka=free seats
             class_hours_weekly | int | 3..12 hours | aka=class hours per week
             """),
     ],
     outcomes=["enrol in matched level; enrol one level down; place on waitlist*; send to coordinator; "
               "retest learner*",
               "charge materials fee*; waive materials fee; lend books"],
     levels=["beginning; low intermediate; high intermediate; advanced", "low; medium; high"],
     words="""
     strong: placement_score >= 236
     emerging: placement_score < 180
     patient: weeks_waiting >= 8
     busy: free_hours_weekly <= 4
     assessed: test_completed
     resident: residency_proof_seen
     veteran: returning_learner
     backed: employer_sponsored
     educated: years_schooling >= 12
     faithful: attendance_rate >= 90
     full: seats_open < 1
     intensive: class_hours_weekly >= 9
     nocturnal: preferred_time == evening
     vocational: learner_goal == work
     fluent: placement_level == advanced
     parental: childcare_needed
     """,
     cues="never took the placement test => test_completed=false; has no proof of local address => "
          "residency_proof_seen=false; lacks employer sponsorship => employer_sponsored=false",
     links="enrolment > learner: registers / registered by; enrolment > class: targets / targeted by",
     actions="enrol = register; retest = test again; waitlist = queue; transfer = move up",
     sources="intake form; placement test report; coordinator email; learner phone call; class roster; "
             "funding report",
     inert="""
     badge_shape | cat | oval; rectangle
     tea_urn | cat | full urn; half urn
     classroom_map | cat | world map; city map
     door_mat | cat | welcome mat; plain mat
     clock_face | cat | roman numerals; arabic numerals
     """,
     affix="untested => test_completed; unsponsored => employer_sponsored"),

dict(slot="ed-08", slug="preschool-enrolment", sector="education_admin",
     sub="preschool enrolment, tuition subsidy and waitlist decisions",
     org="Little Lantern Early Learning Centers", desk="family enrolment office",
     setting="A network of preschool centers enrols children by age group and offers tuition subsidies by family "
             "income. The family enrolment office applies the center's enrolment, subsidy and ratio rules to each "
             "application.",
     decider="preschool administrator",
     roles="enrolment coordinator; center director; subsidy specialist; lead teacher; family advocate; "
           "billing clerk",
     docs="enrolment application; immunization record; subsidy worksheet; waitlist report; parent handbook; "
          "tuition agreement",
     scope=("center", "Maple Street Center; Harbour Center; Hillcrest Center; Parkside Center"),
     money="dollars",
     ents=[
        dict(key="application", singular="enrolment application", plural="enrolment applications", id="EA",
             aka="family application",
             attrs="""
             child_age_months | int | 6..66 months | aka=age in months
             family_income | money | 0.00..200000.00 | aka=household income
             days_in_queue | int | 0..400 days | aka=time in the queue
             days_per_week | int | 2..5 days | aka=days of care
             monthly_tuition | money | 300.00..2200.00 | aka=tuition per month
             age_group | cat | infant room; toddler room; preschool room; pre-K room
             subsidy_band | ord | full pay; partial subsidy; full subsidy | aka=subsidy level
             immunizations_current | state | bad=0 | aka=shots up to date | grp=health
             sibling_enrolled | state | bad=0 | aka=brother or sister already attends
             staff_child | state | bad=0 | aka=parent works at the center
             deposit_paid | event | bad=0 | aka=enrolment deposit paid
             tour_completed | event | bad=0 | aka=family toured the center
             applied_on | date
             start_wanted_on | date
             application_tags | tag | special diet; therapy services; twins; mid-year start; transfer in
             """),
        dict(key="family", singular="family", plural="families", id="FM", names="person", role="person",
             attrs="""
             children_in_care | int | 1..4 people | aka=children in care
             balance_due | money | 0.00..5000.00 | aka=past balance
             home_language | cat | English; Spanish; Arabic; Mandarin; Polish | aka=language spoken at home
             """),
        dict(key="room", singular="classroom", plural="classrooms", id="RM",
             names=["Room Sunflower", "Room Bluebird", "Room Acorn", "Room Pebble", "Room Willow", "Room Comet", "Room Lark", "Room Clover"],
             attrs="""
             open_spots | int | 0..12 seats | aka=spaces open
             ratio_children_per_adult | int | 3..12 people | aka=children per adult
             """),
     ],
     outcomes=["enrol now; enrol next month; offer another center; keep on waitlist*; send to center director; "
               "close application*",
               "charge full tuition*; apply partial subsidy; apply full subsidy"],
     levels=["full pay; partial subsidy; full subsidy", "low; medium; high"],
     words="""
     tiny: child_age_months < 18
     mature: child_age_months >= 48
     modest: family_income < 40000
     affluent: family_income >= 150000
     patient: days_in_queue >= 180
     steady: days_per_week > 4
     pricey: monthly_tuition >= 1500
     protected: immunizations_current
     kindred: sibling_enrolled
     committed: deposit_paid
     acquainted: tour_completed
     indebted: balance_due > 200
     packed: open_spots < 1
     assisted: subsidy_band == full subsidy
     """,
     cues="lacks current immunizations => immunizations_current=false; never toured the center => "
          "tour_completed=false; has no deposit paid => deposit_paid=false",
     links="application > family: names / named by; application > room: targets / targeted by",
     actions="enrol = register; subsidize = apply aid; waitlist = queue; transfer = move center",
     sources="enrolment application; health form; subsidy worksheet; director email; parent phone call; "
             "billing ledger",
     inert="""
     cubby_colour | cat | yellow cubby; purple cubby
     storybook_theme | cat | farm story; ocean story
     playground_slide | cat | straight slide; spiral slide
     nap_mat_pattern | cat | stars; stripes
     snack_fruit | cat | apples; bananas; grapes
     """,
     affix="unvaccinated => immunizations_current; unpaid => deposit_paid"),

dict(slot="ed-09", slug="circulation-blocks", sector="education_admin",
     sub="library circulation desk handling holds, overdue fines and account blocks",
     org="Wyndham County Public Library", desk="circulation desk",
     setting="A county library lends books, media and equipment. The circulation desk applies loan periods, "
             "fines, holds and account block rules to each patron account.",
     decider="library clerical assistant",
     roles="circulation clerk; branch manager; collections clerk; youth services librarian; volunteer shelver; "
           "outreach driver",
     docs="patron account summary; overdue notice; hold slip; fine schedule; lost item bill; "
          "library card application",
     scope=("branch", "Central Branch; Eastgate Branch; Lakeview Branch; Bookmobile"),
     money="dollars",
     ents=[
        dict(key="account", singular="patron account", plural="patron accounts", id="PC", aka="library account",
             attrs="""
             fines_balance | money | 0.00..250.00 | aka=fines owed
             items_overdue | int | 0..15 items | aka=overdue items
             days_most_overdue | int | 0..180 days | aka=longest overdue
             holds_waiting | int | 0..12 items | aka=holds on the shelf
             card_type | cat | adult card; teen card; child card; teacher card; visitor card
             contact_method | cat | email; text; phone; mail
             account_tier | ord | basic; standard; premium | aka=borrowing tier
             address_updated | event | bad=0 | aka=address refreshed this year | grp=contact
             lost_item_billed | event | bad=1 | aka=bill sent for a lost item
             guardian_signed | state | bad=0 | aka=guardian signature on file
             collections_referral | state | bad=1 | aka=sent to the collection agency
             card_renewed | event | bad=0 | aka=card renewed on time
             last_visit_on | date
             card_expires_on | date
             account_tags | tag | homebound; school class; reading challenge; accessible formats; new resident
             """),
        dict(key="patron", singular="patron", plural="patrons", id="PT", names="person", role="person",
             attrs="""
             patron_age | int | 3..99 years | aka=age
             items_borrowed_this_year | int | 0..400 items | aka=loans this year
             """),
        dict(key="item", singular="library item", plural="library items", id="ME",
             names=["Item Lighthouse Atlas", "Item River Songs Album", "Item Telescope Kit", "Item Bread Baking Guide", "Item Chess Set", "Item Garden Almanac", "Item Ukulele", "Item Bird Field Guide"],
             attrs="""
             replacement_cost | money | 5.00..400.00 | aka=cost to replace
             loan_period_days | int | 3..28 days | aka=loan length
             """),
     ],
     outcomes=["clear account; block borrowing*; allow limited borrowing; send to branch manager; "
               "refer to collections*",
               "waive fines; reduce fines; keep fines*"],
     levels=["basic; standard; premium", "low; medium; high"],
     words="""
     indebted: fines_balance >= 10
     clean: fines_balance < 1
     forgetful: items_overdue >= 3
     delinquent: days_most_overdue >= 60
     eager: holds_waiting >= 4
     current: address_updated
     sanctioned: guardian_signed
     maintained: card_renewed
     young: patron_age < 13
     avid: items_borrowed_this_year >= 100
     valuable: replacement_cost >= 100
     brisk: loan_period_days <= 7
     adolescent: card_type == teen card
     digital: contact_method in {email, text}
     privileged: account_tier == premium
     pursued: collections_referral
     """,
     cues="lacks a guardian signature => guardian_signed=false; was never renewed on time => "
          "card_renewed=false; has no address refresh this year => address_updated=false",
     links="account > patron: belongs to / owned by; account > item: borrows / borrowed by",
     actions="check out = lend; check in = receive back; renew = extend; block = freeze",
     sources="patron account summary; overdue notice log; branch manager email; phone message; "
             "self-checkout log; collection agency report",
     inert="""
     book_cart_colour | cat | red cart; blue cart
     display_theme | cat | mysteries; gardening; poetry
     returns_slot | cat | slot A; slot B
     reading_room_chair | cat | armchair; stool
     window_seat | cat | sunny seat; shady seat
     """,
     affix="unsigned => guardian_signed; unrenewed => card_renewed"),

dict(slot="ed-10", slug="graduation-audit", sector="education_admin",
     sub="graduation requirement audit at a high school counseling office",
     org="Pinecrest Regional High School", desk="counseling office",
     setting="A high school counseling office audits each senior's record before graduation. Counselors apply "
             "the credit, testing and service requirements and decide each senior's graduation status.",
     decider="school counselor",
     roles="graduation auditor; registrar; assistant principal; parent liaison; career center advisor; "
           "credit recovery teacher",
     docs="graduation audit sheet; transcript; credit recovery contract; service hours log; test score report; "
          "diploma order",
     scope=("cohort", "Class of A; Class of B; Early Graduates; Fifth-Year Seniors"),
     money="dollars",
     ents=[
        dict(key="audit", singular="graduation audit", plural="graduation audits", id="GA", aka="senior audit",
             attrs="""
             credits_earned | dec1 | 10.0..30.0 credits | aka=total credits
             credits_required | dec1 | 22.0..26.0 credits | aka=credits needed
             service_hours | int | 0..120 hours | aka=community service hours
             math_credits | dec1 | 0.0..5.0 credits | aka=math credits
             cap_and_gown_fee | money | 0.00..90.00 | aka=ceremony fee
             diploma_track | cat | standard diploma; honors diploma; career diploma; alternative certificate
             exit_exam_result | ord | below basic; basic; proficient; advanced | aka=exit exam band
             senior_project_done | event | bad=0 | aka=capstone project finished | grp=capstone
             recovery_course_active | state | bad=1 | aka=credit recovery course in progress
             transcript_from_transfer_received | event | bad=0 | aka=transfer transcript arrived
             fees_cleared | state | bad=0 | aka=school fees settled
             parent_meeting_held | event | bad=0 | aka=family conference held
             audited_on | date
             ceremony_on | date
             audit_tags | tag | transfer student; athlete; English learner; early graduate; dual enrollment
             """),
        dict(key="student", singular="senior", plural="seniors", id="SR", names="person", role="person",
             attrs="""
             attendance_rate | dec1 | 50.0..100.0 percent | aka=attendance this year
             gpa | dec2 | 0.50..4.00 points | aka=grade point average
             post_graduation_path | cat | college; trade school; military; workforce; gap year | aka=next step
             """),
        dict(key="counselor", singular="counselor", plural="counselors", id="CW", names="person", role="person",
             attrs="""
             caseload | int | 100..500 students | aka=students assigned
             years_in_role | int | 0..30 years | aka=years as counselor
             """),
     ],
     outcomes=["clear to graduate; graduate pending summer course; graduate with alternative certificate; "
               "send to assistant principal; withhold diploma*",
               "walk in ceremony; walk and finish in summer; skip ceremony*"],
     levels=["below basic; basic; proficient; advanced", "low; medium; high"],
     words="""
     ahead: credits_earned >= 27
     behind: credits_earned < 20
     generous: service_hours >= 80
     numerate: math_credits >= 4
     accomplished: senior_project_done
     recovering: recovery_course_active
     solvent: fees_cleared
     consulted: parent_meeting_held
     punctual: attendance_rate >= 95
     stellar: gpa >= 3.50
     overloaded: caseload >= 400
     seasoned: years_in_role >= 10
     competent: exit_exam_result >= proficient
     elite: diploma_track == honors diploma
     relocated: transcript_from_transfer_received
     demanding: credits_required >= 25
     """,
     cues="never finished the capstone project => senior_project_done=false; has no settled school fees => "
          "fees_cleared=false; lacks the transfer transcript => transcript_from_transfer_received=false",
     links="audit > student: concerns / concerned by; audit > counselor: assigns / assigned by",
     actions="audit = review record; clear = approve; enroll = sign up; order = buy diploma",
     sources="transcript; counselor note; registrar email; parent phone call; service hours log; "
             "test score report",
     inert="""
     yearbook_cover | cat | blue cover; silver cover
     tassel_colour | cat | gold tassel; white tassel
     locker_row | cat | upper locker; lower locker
     mascot_costume | cat | eagle; bear
     hallway_trophy | cat | chess trophy; band trophy
     """,
     affix="unfinished => senior_project_done; unsettled => fees_cleared"),
]
