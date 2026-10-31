"""W8 routing cards (PREREG_FINAL Ruling A40 addendum, W8: complaint and ticket routing).

24 hand-written routing cards over 10 industries (2-3 cards each). A card = a company description, 4-8 routes (a team or
product, each with a one-sentence definition and a few "typical words" that people use when writing to it), always ending
in "general / other", and ONE precedence rule for complaints that touch more than one route:
  order  the earliest team in a stated order wins (deterministic);
  ask    the team that can fix what the customer most wants done wins (side remarks do not decide);
  top    one named team wins whenever a stated matter is raised, otherwise "ask".
Everything here is invented wording: no public complaint corpus, no CFPB product list or text, no real company.
The cards are data for w8_complaint_routing.py; nothing here is a label for any particular complaint.
"""
from __future__ import annotations

GENERAL = "general / other"
K_BY_N = {4: 18, 5: 14, 6: 12, 7: 10, 8: 9}          # complaints per route, by number of routes (incl. general)


def R(label: str, definition: str, words: str) -> dict:
    return {"label": label, "definition": definition, "words": [w.strip() for w in words.split(",")]}


def G(definition: str) -> dict:
    return {"label": GENERAL, "definition": definition, "words": []}


CATEGORY_ASK = ("Route a complaint by the kind of {thing} it is about, whatever the problem is; if it mentions more than "
                "one kind, use the one the customer mainly wants put right.")

CARDS = [
    # ------------------------------------------------------------------------------------------------- telecom
    {"card_id": "tel_a", "industry": "telecom", "company": "a mobile phone and home-internet provider",
     "who": "customers", "audience": "consumer",
     "routes": [
         R("billing & payments", "Charges, invoices, failed or duplicate payments, refunds, credits and unexpected price "
           "changes on a bill.", "bill, charged, invoice, refund, direct debit"),
         R("network & coverage", "Dropped calls, no signal, slow mobile data or home internet speeds, and outages in an "
           "area.", "no signal, dropped calls, slow data, outage, coverage"),
         R("devices & SIM", "Faulty, damaged or late phones, routers and SIM cards, plus repairs and warranty swaps.",
           "handset, router, SIM card, cracked screen, replacement"),
         R("plans & contracts", "Choosing, changing or upgrading a plan or contract, what the contract terms say, and "
           "offers that were described wrongly at sign-up.", "plan, contract, upgrade, promotion, sign-up offer"),
         R("cancellations & number transfers", "Requests to end a service or move a number to another provider, "
           "including fees or obstacles when leaving.", "cancel, port my number, leave, switch provider, exit fee"),
         R("fraud & security", "Someone else using the account or a SIM, unauthorised lines or purchases, and scam calls "
           "or texts pretending to be from the company.", "SIM swap, hacked, scam text, unauthorised, identity stolen"),
         G("Anything that fits none of the teams above, such as feedback about adverts or staff manners, requests "
           "unrelated to the services, or a complaint too vague to place.")],
     "other_hints": ["feedback about a TV advert or sponsorship", "a request for a job or work experience",
                     "a complaint about another company's service sent here by mistake",
                     "an opinion about a government phone tax or regulation"],
     "rule": {"type": "top", "top": "fraud & security",
              "phrase": "a suspected SIM swap, someone else using the account, or an unauthorised line or purchase"}},

    {"card_id": "tel_b", "industry": "telecom", "company": "a mobile phone and home-internet provider",
     "who": "customers", "audience": "consumer",
     "routes": [
         R("postpaid mobile", "Monthly-contract mobile lines billed after use, with their calls, data, texts and "
           "handsets paid by instalments.", "monthly contract, handset instalments, data allowance, roaming"),
         R("prepaid mobile", "Pay-as-you-go lines and top-ups, including credit that disappears, expired bundles and "
           "top-up vouchers.", "top-up, pay as you go, credit vanished, voucher, bundle expired"),
         R("home internet", "Home broadband and wifi, including routers, installation visits, line speed and faults.",
           "broadband, router, installer, wifi, fibre"),
         R("tv & streaming", "The TV box, channel packages and streaming add-ons, and picture or app faults on them.",
           "TV box, channels, sports package, streaming app, remote"),
         R("business accounts", "Company accounts with several lines, business fibre, fleet SIMs and dedicated account "
           "managers.", "company account, fleet, account manager, staff phones, business fibre"),
         G("Anything that fits none of the products above, or a complaint too vague to place.")],
     "other_hints": ["a suggestion to open a store in another town", "feedback about the company's charity work",
                     "a question about a competitor's offer",
                     "a complaint about a shop assistant's manner that names no service"],
     "rule": {"type": "ask", "sentence": CATEGORY_ASK.format(thing="product")}},

    {"card_id": "tel_c", "industry": "telecom", "company": "a mobile phone and home-internet provider",
     "who": "customers", "audience": "consumer",
     "routes": [
         R("technical repair", "A fault, outage or slow service that needs an engineer visit or a remote fix.",
           "engineer, fault, no connection, outage, reset"),
         R("billing dispute", "The customer says an amount charged is wrong and wants it checked, removed or refunded.",
           "overcharged, wrong amount, dispute, refund, double charge"),
         R("account changes", "Updating personal details, moving the service to a new address, adding or removing "
           "account users, and name changes.", "change address, new surname, add my husband, update email, moving house"),
         R("goodwill & compensation", "Asking for an apology, goodwill credit or compensation for poor service when no "
           "specific charge is being disputed.", "compensation, apology, goodwill credit, inconvenience, poor service"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a general opinion about the company's marketing emails",
                     "praise mixed with a vague wish that things were better", "a request for a job",
                     "a complaint that a competitor's advert is misleading"],
     "rule": {"type": "order", "order": ["technical repair", "billing dispute", "account changes",
                                          "goodwill & compensation"]}},

    # ------------------------------------------------------------------------------------------------- utilities
    {"card_id": "util_a", "industry": "utilities", "company": "an electricity and gas supplier", "who": "customers",
     "audience": "consumer",
     "routes": [
         R("billing & payments", "Questions about bills, estimated charges, direct debit amounts, payments and refunds "
           "of credit balances.", "bill, estimated, direct debit, credit balance, overcharged"),
         R("meter & readings", "Smart or standard meters that are faulty, missing or being installed, and wrong or "
           "missing readings.", "meter, reading, smart meter, installation, display"),
         R("supply & outages", "Power or gas supply that is cut off, keeps failing or is restored late.",
           "power cut, blackout, no gas, flickering, restored"),
         R("moving & switching", "Opening or closing an account when moving home, and switching to or from this "
           "supplier.", "moving out, final reading, switching, new tenant, closing account"),
         R("hardship & arrears", "Customers struggling to pay, debt on the account, payment plans, prepayment meter "
           "debt and disconnection warnings.", "arrears, cannot pay, payment plan, debt, disconnection notice"),
         R("safety & emergencies", "Reports of danger such as a gas smell, sparking sockets, exposed wires or a damaged "
           "supply cable.", "gas smell, sparks, burning smell, exposed wire, cable down"),
         G("Anything that fits none of the teams above, such as opinions about energy policy or advertising, or a "
           "complaint too vague to place.")],
     "other_hints": ["feedback about the company's green-energy advertising",
                     "worry about wind turbines planned near the customer's town",
                     "an opinion on national energy prices or government policy", "a suggestion to redesign the website"],
     "rule": {"type": "top", "top": "safety & emergencies",
              "phrase": "a gas smell, sparking, exposed wiring or another danger"}},

    {"card_id": "util_b", "industry": "utilities", "company": "an electricity and gas supplier", "who": "customers",
     "audience": "consumer",
     "routes": [
         R("home electricity", "Electricity for a private home, including its tariff, bills, meter and supply.",
           "electricity bill, tariff, standing charge, kWh, power"),
         R("home gas & boilers", "Gas for a private home and the boiler or heating cover plans sold with it.",
           "gas bill, boiler, heating cover, engineer visit, radiators"),
         R("solar & batteries", "Rooftop solar panels, home batteries, and payments for electricity sent back to the "
           "grid.", "solar panels, battery, export payment, inverter, generation"),
         R("business energy", "Electricity or gas for a shop, office or other business, including business contracts "
           "and renewals.", "shop, office, business contract, renewal, commercial"),
         G("Anything that fits none of the products above, or a complaint too vague to place.")],
     "other_hints": ["a complaint about the water company, a different company", "feedback about a sponsorship deal",
                     "a request for a job", "a suggestion for the customer magazine"],
     "rule": {"type": "ask", "sentence": CATEGORY_ASK.format(thing="product")}},

    # ------------------------------------------------------------------------------------------------- airlines
    {"card_id": "air_a", "industry": "airlines", "company": "an airline", "who": "passengers", "audience": "consumer",
     "routes": [
         R("booking & changes", "Buying a ticket, fare differences, seat selection, name corrections, and changing or "
           "rebooking a flight by choice.", "booking, fare, seat selection, change the date, rebook"),
         R("refunds & compensation", "Money back for cancelled or unused tickets, and compensation claims for delays, "
           "cancellations or denied boarding.", "refund, compensation, voucher, reimbursement, delay claim"),
         R("baggage", "Lost, delayed or damaged luggage, baggage fees and allowance disputes.",
           "suitcase, lost luggage, baggage fee, damaged bag, carry-on"),
         R("check-in & boarding", "Trouble with online or airport check-in, boarding passes and gate procedures on the "
           "day of travel.", "check-in, boarding pass, gate, kiosk, boarding group"),
         R("loyalty programme", "Points or miles that are missing or expired, status tiers, and reward flights.",
           "miles, points, tier status, reward flight, frequent flyer"),
         R("special assistance", "Help a passenger needs because of a disability, a medical condition, reduced mobility "
           "or travelling with a baby, such as wheelchairs, medical equipment and priority seating.",
           "wheelchair, mobility, infant, medical, assistance"),
         R("in-flight experience", "Crew behaviour, seats, food and drink, entertainment, cleanliness and temperature "
           "on board.", "cabin crew, meal, broken seat, entertainment, cold cabin"),
         G("Anything that fits none of the teams above, such as opinions about airports, taxes or advertising, or a "
           "complaint too vague to place.")],
     "other_hints": ["feedback about the airline's uniforms or livery",
                     "a complaint about airport shops or security queues run by the airport, not the airline",
                     "an opinion about aviation taxes", "a request to sponsor a charity event"],
     "rule": {"type": "top", "top": "special assistance",
              "phrase": "a need for special help because of a disability, a medical condition or an infant"}},

    {"card_id": "air_b", "industry": "airlines", "company": "an airline", "who": "passengers", "audience": "consumer",
     "routes": [
         R("flight disruption", "Delays, cancellations, diversions and missed connections, and the rebooking or "
           "information given during them.", "delayed, cancelled, stranded, missed connection, rebooked"),
         R("baggage claims", "Lost, delayed or damaged bags and the claim that follows.",
           "lost bag, claim form, damaged suitcase, delayed baggage, compensation for bag"),
         R("refunds & vouchers", "Money or vouchers owed for cancelled, changed or unused tickets and extras.",
           "refund, voucher, credit, unused ticket, money back"),
         R("website & app problems", "Errors or confusing steps on the airline's website or app, including failed "
           "payments and login trouble.", "app crashed, error message, website, login, payment page"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a complaint about a hotel booked separately", "feedback about an advert", "a job enquiry",
                     "an opinion about airport security rules"],
     "rule": {"type": "order", "order": ["flight disruption", "baggage claims", "refunds & vouchers",
                                          "website & app problems"]}},

    {"card_id": "air_c", "industry": "airlines", "company": "a low-cost airline", "who": "passengers",
     "audience": "consumer",
     "routes": [
         R("fees & extras", "Paid add-ons and surcharges such as seat fees, cabin bag fees, priority boarding and card "
           "fees.", "fee, surcharge, cabin bag, priority boarding, extra charge"),
         R("booking errors", "Mistakes made when booking, such as wrong dates, misspelled names, duplicate bookings or "
           "tickets that never arrived.", "wrong date, misspelled name, duplicate booking, no confirmation, typo"),
         R("payment & card issues", "Failed, double or suspicious-looking card payments and currency conversion on "
           "payments.", "card declined, charged twice, payment failed, exchange rate, bank blocked"),
         R("flight changes", "Schedule changes, cancellations by the airline and the options offered afterwards.",
           "flight time changed, cancelled by the airline, new option, retimed"),
         R("staff conduct", "Rude, unhelpful or unfair treatment by airport or cabin staff.",
           "rude, shouted at, unhelpful agent, attitude, unfair treatment"),
         R("accessibility & assistance", "Support for passengers with disabilities, reduced mobility or special needs, "
           "including pre-booked help.", "wheelchair, mobility assistance, hearing, special seat, assistance booking"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a complaint about taxi prices outside the airport", "feedback about the airline's slogan",
                     "a request to sponsor an event", "a general opinion about budget airlines"],
     "rule": {"type": "ask"}},

    # ------------------------------------------------------------------------------------------------- retail
    {"card_id": "ret_a", "industry": "retail", "company": "an online and high-street retailer", "who": "shoppers",
     "audience": "consumer",
     "routes": [
         R("returns & refunds", "Sending items back, return labels, refund delays and refusals to accept a return.",
           "return, refund, money back, return label, exchange"),
         R("payments & promo codes", "Card or wallet payments that fail or double charge, and discount codes, gift "
           "cards or loyalty offers that do not work.", "promo code, gift card, charged twice, payment declined, coupon"),
         R("orders & delivery", "Late, lost, misdelivered or wrongly packed orders, and tracking problems.",
           "parcel, delivery, tracking, wrong item sent, courier"),
         R("product quality & damage", "Items that arrived broken, faulty, worn out early or not as described.",
           "broken, faulty, not as described, stopped working, defective"),
         R("account & website", "Login, password and account details, website or app errors, and unwanted emails.",
           "login, password, app crashed, website error, unsubscribe"),
         R("store experience", "Behaviour of shop staff, queues, cleanliness, opening hours and store layout.",
           "cashier, queue, store, rude assistant, closed early"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a suggestion to open a store in another town", "feedback about the company's advertising",
                     "a complaint about a different retailer", "a request for a job"],
     "rule": {"type": "order", "order": ["returns & refunds", "payments & promo codes", "orders & delivery",
                                          "product quality & damage", "account & website", "store experience"]}},

    {"card_id": "ret_b", "industry": "retail", "company": "a department-store retailer", "who": "shoppers",
     "audience": "consumer",
     "routes": [
         R("electronics & appliances", "Phones, computers, TVs, headphones, cameras, and kitchen or laundry appliances.",
           "laptop, TV, headphones, washing machine, charger"),
         R("furniture & home", "Sofas, beds, tables, rugs, lighting, curtains and other home decor.",
           "sofa, mattress, table, rug, curtains"),
         R("clothing & shoes", "Clothes, shoes, bags and fashion accessories, including sizing and fit.",
           "jacket, trainers, size, dress, handbag"),
         R("grocery & household", "Food, drink, cleaning products, toiletries and pet supplies.",
           "food, cleaning spray, shampoo, dog food, coffee"),
         G("Any other product such as toys, sports gear or garden items, or a complaint that is about no product at "
           "all.")],
     "other_hints": ["a toy that broke after a week", "a garden hose that leaks",
                     "a complaint about noise from the store's building works", "a request to open a store elsewhere"],
     "rule": {"type": "ask", "sentence": CATEGORY_ASK.format(thing="item")}},

    {"card_id": "ret_c", "industry": "retail", "company": "an online marketplace", "who": "sellers on the marketplace",
     "audience": "seller",
     "routes": [
         R("seller payouts", "Payments owed to sellers, delayed or short payouts, and funds held back.",
           "payout, payment delayed, funds on hold, short paid, bank transfer"),
         R("fees & commissions", "Questions or disputes about listing fees, commission rates and charges deducted from "
           "sales.", "commission, listing fee, deducted, fee increase, charged for"),
         R("listing & account suspension", "Listings taken down, rejected photos or categories, and suspended or "
           "restricted seller accounts.", "listing removed, suspended, restricted, rejected photo, banned"),
         R("buyer disputes & claims", "Buyers' refund requests, chargebacks, return disputes and unfair ratings that "
           "affect the seller.", "buyer claim, chargeback, refund request, bad rating, return dispute"),
         R("shipping labels & logistics", "Printing shipping labels, carrier pickups, tracking uploads and parcels lost "
           "on the way to buyers.", "shipping label, pickup, tracking number, lost parcel, carrier"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a request for a job at the marketplace", "feedback about the marketplace's logo or adverts",
                     "an opinion about tax rules for online sellers",
                     "a complaint about a different marketplace the seller also uses"],
     "rule": {"type": "ask"}},

    # ------------------------------------------------------------------------------------------------- insurance
    {"card_id": "ins_a", "industry": "insurance", "company": "a home, motor and travel insurer",
     "who": "policyholders", "audience": "consumer",
     "routes": [
         R("claim decisions & appeals", "A claim has been refused, reduced or valued too low and the customer wants the "
           "decision reviewed.", "claim rejected, settlement offer, appeal, undervalued, reassess"),
         R("claims filing & status", "Starting a claim, sending documents, repair or replacement arrangements and "
           "chasing the progress of an open claim.", "file a claim, uploaded photos, claim number, status, repair garage"),
         R("premiums & billing", "The price of cover, payment dates, double or failed premium payments and refunds of "
           "premium.", "premium, monthly payment, direct debit, price rise, refund"),
         R("policy changes & renewals", "Changing cover, adding drivers or items, renewal terms and ending a policy.",
           "renewal, add a driver, change address, cancel my policy, cover change"),
         R("new quotes & sales", "Getting a quote, buying cover, and complaints that a sales agent gave misleading "
           "advice.", "quote, mis-sold, salesperson, comparison site, new policy"),
         R("documents & portal", "Policy documents, insurance certificates, ID cards, and the online account or app.",
           "certificate, policy document, login, app, proof of insurance"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a general opinion about insurance companies", "feedback about an advert",
                     "a request for a job", "a complaint about a different insurer"],
     "rule": {"type": "order", "order": ["claim decisions & appeals", "claims filing & status", "premiums & billing",
                                          "policy changes & renewals", "new quotes & sales", "documents & portal"]}},

    {"card_id": "ins_b", "industry": "insurance", "company": "an insurance company", "who": "policyholders",
     "audience": "consumer",
     "routes": [
         R("motor insurance", "Cover for cars, vans and motorbikes.", "car, van, motorbike, no-claims bonus, windscreen"),
         R("home & contents", "Cover for a house, flat, its fixtures and belongings.",
           "house, flat, contents, burst pipe, burglary"),
         R("pet insurance", "Vet-fee cover for dogs, cats and other pets.", "vet bill, dog, cat, pre-existing, treatment"),
         R("travel insurance", "Trip cancellation, medical and baggage cover for journeys.",
           "holiday, trip, cancelled flight, lost luggage, abroad"),
         R("life & health cover", "Life cover, income protection and private health plans.",
           "life cover, income protection, health plan, beneficiary, waiting period"),
         G("Any other product, or a complaint that is about no product at all.")],
     "other_hints": ["a general opinion about how expensive insurance is", "a request for a job",
                     "feedback about a sponsorship", "a complaint about an unrelated bank"],
     "rule": {"type": "ask", "sentence": CATEGORY_ASK.format(thing="cover")}},

    # ------------------------------------------------------------------------------------------------- software
    {"card_id": "sw_a", "industry": "software", "company": "a project-management software company",
     "who": "users and admins of the software", "audience": "user",
     "routes": [
         R("bugs & errors", "Features that crash, show error messages or behave differently from how they are meant "
           "to.", "bug, error message, crashes, glitch, not saving"),
         R("login & account access", "Locked accounts, forgotten passwords, two-step codes, single sign-on trouble and "
           "invites that do not work.", "locked out, password reset, 2FA code, SSO, invite link"),
         R("billing & subscriptions", "Invoices, plan prices, seat charges, failed payments, renewals and refunds.",
           "invoice, charged, seats, renewal, refund"),
         R("feature requests", "Asking for a feature that does not exist or a change to how a feature is designed.",
           "please add, wish it could, missing feature, would be great if, roadmap"),
         R("integrations & API", "Connections to other tools, webhooks, import tools and the public API.",
           "connector, webhook, API key, import from spreadsheet, sync"),
         R("performance & outages", "The service being slow, unavailable or down for many users.",
           "slow, timeout, down, cannot load, outage"),
         R("security & privacy", "Suspected unauthorised access, leaked data, requests to delete or export personal "
           "data, and other security worries.", "hacked, data leak, delete my data, privacy, suspicious login"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["feedback about the company's marketing emails", "a complaint about a competitor's software",
                     "a question about a job opening", "an opinion on the content of the company blog"],
     "rule": {"type": "top", "top": "security & privacy",
              "phrase": "suspected unauthorised access, a data leak or another security or privacy worry"}},

    {"card_id": "sw_b", "industry": "software", "company": "a project-management software company",
     "who": "users and admins of the software", "audience": "user",
     "routes": [
         R("boards & tasks", "Creating, assigning, moving and commenting on tasks and boards.",
           "task, board, assign, comment, drag"),
         R("time tracking", "Timers, timesheets, billable hours and time reports.",
           "timer, timesheet, billable hours, hours logged, clock"),
         R("reports & dashboards", "Charts, dashboards, exports and scheduled reports.",
           "dashboard, chart, export, report, scheduled report"),
         R("mobile app", "Problems that happen only in the phone or tablet app.",
           "phone app, tablet, push notification, iOS, Android"),
         R("admin & permissions", "Roles, user management, sharing settings, workspace settings and audit logs.",
           "roles, permissions, admin, sharing settings, audit log"),
         G("Anything that fits none of the parts above, such as billing or sales questions handled elsewhere, or a "
           "complaint too vague to place.")],
     "other_hints": ["a billing or subscription question that belongs to no part of the product",
                     "feedback about the company's pricing page wording", "a complaint about the company's marketing emails",
                     "a question about a job opening"],
     "rule": {"type": "ask", "sentence": "Route a complaint by the part of the product the problem is in; if it mentions "
              "more than one part, use the part the customer mainly wants fixed."}},

    {"card_id": "sw_c", "industry": "software", "company": "an accounting software company for small businesses",
     "who": "small-business owners using the software", "audience": "business",
     "routes": [
         R("payroll", "Paying employees, payslips, pay runs, pension contributions and payroll tax filings.",
           "payslip, pay run, employee wages, pension, payroll tax"),
         R("tax filing", "Sales tax or VAT returns, year-end tax forms and tax rates inside the software.",
           "VAT return, sales tax, year-end form, tax rate, filing deadline"),
         R("bank feeds & reconciliation", "Bank connections, imported transactions, duplicates and matching payments to "
           "invoices.", "bank feed, imported transactions, duplicate, reconcile, matching"),
         R("invoicing", "Creating, sending and tracking invoices, quotes and customer payment reminders.",
           "invoice template, send invoice, quote, payment reminder, overdue"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a complaint about the customer's own accountant", "feedback about the company's adverts",
                     "a question about a different product from another company", "a request for a job"],
     "rule": {"type": "order", "order": ["payroll", "tax filing", "bank feeds & reconciliation", "invoicing"]}},

    # ------------------------------------------------------------------------------------------------- healthcare billing admin
    {"card_id": "hb_a", "industry": "healthcare billing", "company": "a hospital billing office",
     "who": "patients and their families", "audience": "patient",
     "routes": [
         R("statements & amounts", "A hospital or clinic bill that is wrong, unclear, duplicated or lists services the "
           "patient did not receive.", "wrong amount, unclear statement, charged for, duplicate bill, itemised"),
         R("insurance claims & coverage", "The billing office's handling of the patient's insurer, such as claims sent "
           "late, to the wrong insurer or left unpaid.", "insurer, claim sent late, coverage, wrong insurer, not paid"),
         R("payment plans & collections", "Paying a bill in instalments, due dates, late fees and letters from a "
           "collections agency.", "instalments, due date, late fee, collections, payment plan"),
         R("refunds & credits", "Money owed back to a patient for overpayments, duplicate charges or insurer payments "
           "received late.", "overpaid, refund cheque, credit balance, paid twice, money owed"),
         R("financial assistance", "Applications for discounts, charity care or hardship help with a bill.",
           "discount, charity care, hardship, cannot afford, assistance form"),
         R("records & privacy", "Billing records that show the wrong person or details, and bills or letters sent to the "
           "wrong address or seen by someone else.", "wrong name, wrong address, sent to my neighbour, privacy, record"),
         G("Anything that fits none of the teams above, such as complaints about clinical care, or a complaint too "
           "vague to place.")],
     "other_hints": ["a complaint about a doctor's manner or waiting times", "feedback about hospital parking or the cafe",
                     "a request for medical advice", "an opinion about national health policy"],
     "rule": {"type": "top", "top": "records & privacy",
              "phrase": "billing details sent to, or seen by, the wrong person"}},

    {"card_id": "hb_b", "industry": "healthcare billing", "company": "a health clinic's billing office",
     "who": "patients and their families", "audience": "patient",
     "routes": [
         R("hospital stays", "Bills for nights on a ward, surgery, childbirth or other inpatient care.",
           "overnight stay, ward, surgery, inpatient, room charge"),
         R("emergency visits", "Bills for emergency department and urgent care visits, including ambulance charges "
           "added to them.", "emergency room, urgent care, ambulance, A&E visit, triage"),
         R("clinic visits & tests", "Bills for outpatient appointments, scans, X-rays and lab tests.",
           "appointment, scan, X-ray, blood test, outpatient"),
         R("pharmacy & supplies", "Bills for medicines, dressings, braces and other equipment from the clinic pharmacy "
           "or supplier.", "prescription, pharmacy, dressings, brace, supplies"),
         G("Anything that fits none of the kinds of care above, or a complaint too vague to place.")],
     "other_hints": ["a complaint about a doctor's manner or waiting times", "feedback about clinic food or parking",
                     "a request for medical advice", "a request for a job"],
     "rule": {"type": "ask", "sentence": CATEGORY_ASK.format(thing="care or item on the bill")}},

    # ------------------------------------------------------------------------------------------------- banking
    {"card_id": "bank_a", "industry": "banking", "company": "a retail bank", "who": "customers", "audience": "consumer",
     "routes": [
         R("card disputes & fraud", "Card payments the customer did not make, scams, disputed merchant charges and "
           "blocked or stolen cards.", "did not make this payment, scam, stolen card, disputed charge, card blocked"),
         R("payments & transfers", "Money that did not arrive, went to the wrong account or is held or delayed, and "
           "standing orders or direct debits that went wrong.", "transfer, payment missing, wrong account, standing order, delayed"),
         R("online & mobile banking", "Logging in, app errors, security codes and website problems.",
           "login, app error, security code, website, locked out"),
         R("loans & mortgages", "Interest, repayments, fees, offers and servicing of loans and mortgages.",
           "mortgage, loan repayment, interest rate, offer, remortgage"),
         R("account fees & statements", "Monthly fees, overdraft charges, interest on accounts and statement mistakes.",
           "monthly fee, overdraft charge, statement, account interest, charged a fee"),
         R("branch & ATM service", "Branch staff, queues, opening times, and cash machines that fail or keep the card.",
           "branch, queue, cashier, cash machine, ATM swallowed my card"),
         G("Anything that fits none of the teams above, such as opinions about the bank's advertising or pay, or a "
           "complaint too vague to place.")],
     "other_hints": ["feedback about the bank's adverts or sponsorship",
                     "a complaint about the bank's bonus pay or executive salaries",
                     "an opinion on interest rates set by the central bank", "a request for a job"],
     "rule": {"type": "order", "order": ["card disputes & fraud", "payments & transfers", "online & mobile banking",
                                          "loans & mortgages", "account fees & statements", "branch & ATM service"]}},

    {"card_id": "bank_b", "industry": "banking", "company": "a bank's business-banking arm",
     "who": "small-business owners and their finance staff", "audience": "business",
     "routes": [
         R("business current accounts", "Day-to-day business accounts, including their fees, statements, limits, opening and closing.",
           "business account, monthly fee, statement, account limit, closing"),
         R("card payments & terminals", "Card machines, settlement of card sales and chargebacks on a business's sales.",
           "card machine, settlement, terminal, chargeback, card sales"),
         R("business loans & overdrafts", "Loans, overdrafts and credit lines for a business, including approval, interest and "
           "repayments.", "business loan, overdraft limit, credit line, approval, repayments"),
         R("payroll & bulk payments", "Paying staff or many suppliers at once, bulk files and scheduled payments.",
           "pay staff, bulk file, supplier payments, scheduled payment, batch"),
         R("foreign payments & FX", "Sending or receiving money abroad, exchange rates and international fees.",
           "international transfer, exchange rate, swift fee, euros, abroad"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["feedback about a networking event the bank hosted", "an opinion on business taxes",
                     "a complaint about a different bank", "a request for a job"],
     "rule": {"type": "ask"}},

    # ------------------------------------------------------------------------------------------------- hospitality
    {"card_id": "hot_a", "industry": "hospitality", "company": "a hotel group", "who": "guests", "audience": "guest",
     "routes": [
         R("reservations & rates", "Booking mistakes, price differences, deposits, and fees for changing or cancelling a "
           "stay before arrival.", "booking, rate, deposit, cancellation fee, price difference"),
         R("room condition", "Dirty, broken, damaged or wrongly equipped rooms, pests, smells, and heating or cooling "
           "that does not work in the room.", "dirty room, broken, smell, air conditioning, bed bugs"),
         R("front desk & staff", "How reception, housekeeping and other staff treated the guest, check-in and "
           "check-out delays, and lost property.", "reception, rude staff, waited to check in, housekeeping, lost property"),
         R("facilities & noise", "Shared spaces and amenities such as the pool, gym, restaurant, wifi and parking, and "
           "disturbance from noise.", "pool, gym, wifi, parking, noisy neighbours"),
         R("charges at checkout", "Charges made during or after the stay, such as incidentals, minibar, restaurant "
           "tabs, holds and deposit refunds.", "minibar, incidentals, double charged, hold on my card, deposit refund"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a complaint about the local council's tourist tax", "feedback about the hotel group's adverts",
                     "a complaint about an unrelated travel agent", "a request for a job"],
     "rule": {"type": "ask"}},

    {"card_id": "hot_b", "industry": "hospitality", "company": "a holiday-rental booking platform", "who": "guests",
     "audience": "guest",
     "routes": [
         R("listing accuracy", "The place, its photos, amenities or location are not as the listing described.",
           "photos, not as described, location, missing amenities, misleading listing"),
         R("booking & payments", "Payment, deposit, cancellation and refund problems with the booking.",
           "payment, deposit, cancellation, refund, charged"),
         R("host communication & check-in", "The host not replying, keys or entry codes not working, and arrival or "
           "checkout arrangements.", "host not replying, key, entry code, arrival, checkout"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a complaint about local council rules for short-term rentals",
                     "a neighbour's complaint about guests at a listing", "feedback about the platform's adverts",
                     "a request for a job"],
     "rule": {"type": "order", "order": ["listing accuracy", "booking & payments", "host communication & check-in"]}},

    # ------------------------------------------------------------------------------------------------- delivery
    {"card_id": "del_a", "industry": "delivery", "company": "a parcel courier", "who": "senders and receivers of parcels",
     "audience": "consumer",
     "routes": [
         R("late or missing parcels", "Parcels that are late, lost, marked delivered but not received, or stuck in "
           "transit, including parcels left at the wrong address.", "late, lost, marked delivered, stuck in transit, wrong address"),
         R("damaged contents & claims", "Parcels that arrive broken or open, and the claim for their value.",
           "broken, crushed box, open parcel, claim form, insured value"),
         R("pickups & drop-off points", "Collections that did not happen, missed driver visits, and locker or drop-off "
           "point trouble.", "pickup, driver did not come, locker, drop-off point, collection"),
         R("customs & duties", "Import charges, customs delays and paperwork on international parcels.",
           "customs, import duty, paperwork, held at customs, international"),
         R("address changes & redirects", "Changing or correcting a delivery address before delivery, and redirecting a "
           "parcel.", "change address, redirect, new address, hold at depot, reroute"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["feedback about the courier's advertising", "a complaint about the retailer's website",
                     "a request for a job as a driver", "a complaint about delivery vans parking on the customer's street"],
     "rule": {"type": "ask"}},

    {"card_id": "del_b", "industry": "delivery", "company": "a food-delivery app", "who": "customers",
     "audience": "consumer",
     "routes": [
         R("order & delivery problems", "Anything wrong with the food order or its delivery, including missing or wrong "
           "items, cold or spilled food, late orders, drivers who never arrived and requests for a refund for them.",
           "missing item, cold food, late, driver, wrong order"),
         R("payments & refunds", "Money problems unrelated to what arrived, such as charges, double payments, promo credit "
           "not applied and subscription fees.", "charged twice, promo credit, subscription fee, payment, card"),
         R("app & account", "Login, app errors, and address and profile settings.",
           "login, app error, address, profile, notifications"),
         G("Anything that fits none of the teams above, or a complaint too vague to place.")],
     "other_hints": ["a restaurant owner complaining about commission rates", "feedback about the company's adverts",
                     "a request for a job as a courier", "an opinion about couriers' working conditions"],
     "rule": {"type": "order", "order": ["payments & refunds", "order & delivery problems", "app & account"]}},
]

# ------------------------------------------------------------------------------------------------- style pools

PERSONAS = {
    "consumer": ["a retired customer who is not confident with technology", "a busy parent", "a university student",
                 "a self-employed person writing as a private customer", "a non-native English speaker with imperfect "
                 "grammar", "a customer of many years", "a first-time customer", "someone typing quickly on a phone",
                 "a customer writing on behalf of an elderly relative", "a detail-oriented customer who lists facts"],
    "seller": ["a part-time hobby seller", "a full-time seller with a small team", "a seller in their first month",
               "a seller who sells handmade items", "a seller who resells second-hand goods",
               "a non-native English speaker with imperfect grammar", "a seller who has used the site for years"],
    "business": ["a shop owner", "an office manager", "the finance lead of a ten-person firm", "a sole trader",
                 "a restaurant owner", "a freelance consultant", "a bookkeeper working for several clients",
                 "a non-native English speaker with imperfect grammar"],
    "user": ["a team lead", "a freelance consultant", "an IT administrator", "a student-group organiser",
             "a non-technical manager", "a developer", "a project coordinator at a charity",
             "a non-native English speaker with imperfect grammar"],
    "patient": ["a patient", "an adult child handling a parent's bills", "a parent paying for a child's care",
                "an older patient who is worried about money", "a patient writing from work in a hurry",
                "a non-native English speaker with imperfect grammar", "a spouse handling the household paperwork"],
    "guest": ["a business traveller", "a family on holiday", "a couple on an anniversary trip", "a solo traveller",
              "a group organiser for a wedding party", "a retired traveller", "a student on a budget",
              "a non-native English speaker with imperfect grammar"],
}
CHANNELS = ["web contact form", "email", "live chat message", "letter", "public social media post",
            "voicemail transcription", "text message", "app store or review-site review"]
TONES = ["calm and factual", "polite but firm", "worried", "confused", "tired and resigned", "terse",
         "chatty and rambling", "disappointed", "dry and sarcastic but not abusive"]
ANGRY_STYLES = ["furious, with some words in capital letters", "cold, sarcastic fury",
                "threatening to leave and write a bad review", "threatening to go to the regulator or an ombudsman",
                "demanding a manager and saying they have been ignored", "ranting, with insults aimed at the company "
                "(no slurs)"]
LENGTHS = [("very short", "8-20"), ("short", "20-45"), ("medium", "45-90"), ("long", "90-150")]
LENGTH_WEIGHTS = [3, 4, 4, 1]


def route_labels(card: dict) -> list:
    return [r["label"] for r in card["routes"]]


def route_by_label(card: dict) -> dict:
    return {r["label"]: r for r in card["routes"]}


def card_problems(card: dict) -> list:
    """Structural problems of one card (empty = fine); used by the tests and before tasks are written."""
    p = []
    routes = card["routes"]
    labels = route_labels(card)
    if not 4 <= len(routes) <= 8:
        p.append(f"{card['card_id']}: {len(routes)} routes (4-8)")
    if len(set(labels)) != len(labels):
        p.append("duplicate labels")
    if labels[-1] != GENERAL or labels.count(GENERAL) != 1:
        p.append("general / other must be present once, and last")
    for r in routes:
        lab, d = r["label"], r["definition"]
        if ": " in lab or "\n" in lab or lab != lab.strip() or lab.startswith("- ") or not lab:
            p.append(f"bad label {lab!r}")
        if ": " in d or "\n" in d or not d.endswith(".") or d.count(". ") > 0:
            p.append(f"definition of {lab!r} is not one sentence without ': '")
        if lab != GENERAL and len(r["words"]) < 3:
            p.append(f"{lab!r}: fewer than 3 typical words")
    if len(card["other_hints"]) < 4:
        p.append("fewer than 4 other_hints")
    if card["audience"] not in PERSONAS:
        p.append("audience")
    rule = card["rule"]
    if rule["type"] == "order":
        if sorted(rule["order"]) != sorted(x for x in labels if x != GENERAL):
            p.append("order must list every team except general / other, once")
    elif rule["type"] == "top":
        if rule["top"] not in labels or rule["top"] == GENERAL or not rule.get("phrase"):
            p.append("top rule: top team / phrase")
    elif rule["type"] != "ask":
        p.append(f"rule type {rule['type']!r}")
    return p
