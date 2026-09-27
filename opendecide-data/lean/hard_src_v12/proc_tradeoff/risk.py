"""proc_tradeoff / risk-limited and compliance-constrained choices (backup
designs, treasury placements, hosting regions, staffing levels, hedging,
incident containment, supplier allocation, payment controls). All
organisations, people, products and places are invented."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ rk01
# why: tier-1: RPO <= 4 h, RTO <= 8 h; every tier: copy in a separate region; budget
# <= $1,500/month; cheapest meeting all. Nightly RPO 24 fails; hourly same-region fails
# region rule; continuous $2,400 > budget; 4-hourly cross-region (RPO 4, RTO 6, $900) ok.
# Twin: tier-2 (RPO/RTO <= 24 h) -> nightly offsite ($300) cheapest.
C("rk01", "Which backup design should be implemented for the system?",
"""
Backup Design Review — system: Sales CRM (Harlow Instruments)
Classification in the service catalogue: tier-1.

Resilience Standard RS-2
- Tier-1: recovery point objective (RPO) of 4 hours or less; recovery time objective (RTO) of 8 hours or less.
- Tier-2: RPO and RTO of 24 hours or less.
- All tiers: at least one backup copy must be held in a different cloud region from production.
- Monthly cost must not exceed $1,500. Choose the cheapest design meeting all rules for the system's tier.

Designs proposed by the platform team
| Design | RPO | RTO | Copy in another region | Monthly cost |
| Nightly offsite backup | 24 h | 12 h | yes | $300 |
| 4-hourly snapshots, copied cross-region | 4 h | 6 h | yes | $900 |
| Hourly snapshots, same region | 1 h | 2 h | no | $700 |
| Continuous replication | 5 min | 1 h | yes | $2,400 |

Architect's note: "Region separation is best practice, but hourly same-region snapshots give far better recovery for less money."
""",
[("nightly_offsite", "As a tier-2 system its 24-hour targets are met by nightly offsite backups, the cheapest compliant design."),
 ("snapshots_4h_cross_region", "4-hourly cross-region snapshots meet the tier-1 targets and the region rule within budget, at the lowest cost that does."),
 ("hourly_same_region", "Hourly snapshots beat both targets at lower cost, and region separation is only best practice."),
 ("continuous_replication", "Tier-1 systems need continuous replication to be safe, so the monthly budget should be raised to cover the $2,400 design instead.")],
"snapshots_4h_cross_region", 2,
twin=T([("Classification in the service catalogue: tier-1.", "Classification in the service catalogue: tier-2.")], "nightly_offsite")),

# ------------------------------------------------------------------ rk02
# why: portfolio after purchase $10.0M; issuer cap 25% = $2.5M; rating >= A; maturity
# <= 12 months; highest yield. Harlan A- fails; Vesper 18 m fails; Linden 2.0+1.0 =
# 3.0M = 30% fails; Corran 0.5+1.0 = 1.5M ok 4.5%; Ostmark 4.2%. -> Corran.
# Twin: Linden existing $1.0M -> 2.0M = 20% ok -> 4.6% > 4.5% -> Linden.
C("rk02", "Which instrument should the $1 million surplus be invested in?",
"""
Surplus Cash Investment Request — Tollgate Housing Association
Amount: $1.0M. Portfolio after this purchase: $10.0M.

Investment Policy (Board-approved)
IP-1. Maximum maturity 12 months.
IP-2. Minimum credit rating A. (A-, BBB+ and lower do not qualify.)
IP-3. After the purchase, no single issuer may exceed 25% of the portfolio.
IP-4. Among instruments meeting IP-1 to IP-3, choose the highest yield.

Existing holdings by issuer: Linden Bank $2.0M; Corran Bank $0.5M; others below $1M each.

Instruments offered by the broker
| Instrument | Maturity | Rating | Yield |
| Harlan Motors commercial paper | 6 months | A- | 5.1% |
| Vesper Utility bond | 18 months | AA | 4.9% |
| Linden Bank deposit certificate | 9 months | A | 4.6% |
| Corran Bank deposit certificate | 6 months | AA- | 4.5% |
| Ostmark Treasury bill | 3 months | AAA | 4.2% |

Broker's note: "Harlan's A- is basically an A. Great yield for a six-month paper."
""",
[("harlan_cp", "Harlan has the highest yield, and an A- rating is part of the A band."),
 ("vesper_bond", "Vesper's AA rating is strong enough to justify going beyond 12 months."),
 ("linden_cd", "Linden meets the rating and maturity limits, stays within 25% per issuer after the purchase, and yields more than Corran."),
 ("corran_cd", "With Linden pushed over the issuer limit, Corran has the highest yield among compliant instruments."),
 ("ostmark_tbill", "Only AAA paper is safe enough for a housing association's surplus cash.")],
"corran_cd", 3,
twin=T([("Existing holdings by issuer: Linden Bank $2.0M;", "Existing holdings by issuer: Linden Bank $1.0M;")], "linden_cd")),

# ------------------------------------------------------------------ rk03
# why: EU/EEA residency + p95 latency to EU users <= 50 ms; cheapest. Hesselt 28 ms
# $4,300; Varby 46 ms $3,700; Marra 58 ms fails; Carlow (US) fails residency.
# -> Varby. Twin: Varby 57 ms -> Hesselt only compliant.
C("rk03", "Which hosting region should the customer portal be deployed in?",
"""
Deployment decision — Vantor Energy customer portal (EU customers only)

Requirements
H1. Customer data must be stored and processed in an EU or EEA region.
H2. 95th-percentile latency to EU users must be 50 ms or less (measured by the synthetic test in ticket PERF-221).
H3. Choose the cheapest region meeting H1 and H2.

Measured results and prices (Stratacloud)
| Region | Location | p95 latency to EU users | Monthly cost |
| eu-central | Hesselt | 28 ms | $4,300 |
| eu-north | Varby | 46 ms | $3,700 |
| eu-south | Marra | 58 ms | $3,500 |
| us-east | Carlow (USA) | 92 ms | $3,100 |

Vendor note: "Our latency tests have a 10 ms margin of error, so Marra is effectively within 50 ms."
Sales note: "Carlow is covered by our EU-standard contract clauses."
""",
[("eu_central_hesselt", "Hesselt is the only EU region within the 50 ms latency limit."),
 ("eu_north_varby", "Varby is the cheapest EU region within the 50 ms latency limit."),
 ("eu_south_marra", "Marra is within 50 ms once the 10 ms margin of error is allowed for, and it is cheaper than Varby."),
 ("us_east_carlow", "EU-standard contract clauses satisfy the residency rule, and Carlow is the cheapest region.")],
"eu_north_varby", 1,
twin=T([("| eu-north | Varby | 46 ms | $3,700 |", "| eu-north | Varby | 57 ms | $3,700 |")], "eu_central_hesselt")),

# ------------------------------------------------------------------ rk04
# why: general areas 1 per 100; licensed bar area 1 per 50 of its capacity (instead of
# 1 per 100). Capacity 2,400 incl. bar 600 -> general 1,800/100 = 18 + 600/50 = 12 = 30.
# Smallest plan >= 30 -> plan_30. Twin: bar 900 -> 1,500/100 = 15 + 900/50 = 18 = 33 ->
# plan_36.
C("rk04", "Which stewarding plan should the event organiser adopt?",
"""
Event Safety Plan — Harbourside Summer Late, 2026
Licensed capacity: 2,400 people in total, of which the licensed bar area holds 600.

Licensing condition 14 (stewarding)
14.1 One steward for every 100 people of capacity in general areas.
14.2 In the licensed bar area, one steward for every 50 people of that area's capacity, instead of 14.1.
14.3 Adopt the smallest stewarding plan that meets 14.1 and 14.2.

Plans quoted by Castleguard Events
| Plan | Stewards | Cost |
| plan_24 | 24 | $4,800 |
| plan_30 | 30 | $6,000 |
| plan_36 | 36 | $7,200 |
| plan_40 | 40 | $8,000 |

Organiser's note: "Last year we used 40 stewards and there were no incidents, so let's just repeat that."
First-aid cover is arranged separately with Tarn Valley Ambulance Volunteers.
""",
[("plan_24", "One steward per 100 across the full 2,400 capacity gives 24, which covers the whole site."),
 ("plan_30", "Counting the bar area at one per 50 and the remaining capacity at one per 100 gives 30 stewards, so plan_30 is the smallest compliant plan."),
 ("plan_36", "Counting the bar area at one per 50 and the remaining capacity at one per 100, plan_36 is the smallest plan that meets the requirement."),
 ("plan_40", "Forty stewards worked last year without incident, so the same level should be kept.")],
"plan_30", 2,
twin=T([("of which the licensed bar area holds 600.", "of which the licensed bar area holds 900.")], "plan_36")),

# ------------------------------------------------------------------ rk05
# why: payable EUR 400k due in 5 months -> within 12-month horizon, over $50k -> hedge
# 75-100% with forwards; options not permitted. forward 80% in band.
# Twin: due in 14 months -> outside horizon -> no hedge yet.
C("rk05", "How should treasury hedge the euro payable?",
"""
Treasury Risk Policy — Foreign Exchange (Brannock Instruments)
FX-1. Committed foreign-currency payables above $50,000 equivalent that fall due within the next 12 months must be hedged at 75% to 100% of their value.
FX-2. Hedges are made with forward contracts only. Currency options are not permitted.
FX-3. Payables due more than 12 months ahead are not hedged until they come within the 12-month horizon.

Exposure report, 25 September 2026
Payable: EUR 400,000 to Kessel Maschinenbau for a moulding press (about $436,000).
Due date: in 5 months.
Budget rate: 1.09. Current forward rate for the due date: 1.1012.

Options presented
- No hedge.
- Forward contract for 50% (EUR 200,000).
- Forward contract for 80% (EUR 320,000).
- Currency option for 100% (EUR 400,000).

Bank relationship manager: "An option gives you full protection and keeps the upside. Most clients your size use them."
""",
[("no_hedge", "The payable falls outside the 12-month horizon, so no hedge is required yet."),
 ("forward_50pct", "Hedging half the exposure balances protection and flexibility, which is the policy's intent."),
 ("forward_80pct", "The payable is within the 12-month horizon, and an 80% forward sits inside the required 75-100% band."),
 ("option_100pct", "An option covers the full amount, and full cover satisfies the 75-100% band.")],
"forward_80pct", 2,
twin=T([("Due date: in 5 months.", "Due date: in 14 months.")], "no_hedge")),

# ------------------------------------------------------------------ rk06
# why: containment rule: isolate at once; do not power off unless encryption is
# spreading AND isolation is impossible; take forensic image before any rebuild.
# Switch-port isolation is available -> isolate and image. Ransom note instruction not
# to disconnect is attacker text, not a rule.
C("rk06", "Which containment action should the incident commander order?",
"""
Incident INC-9031 — Ransomware on file server FS-02 (tier-2), Pellbrook Paper Mills
Time: 07:42. Detected by endpoint alert: files on the shared "Projects" volume being renamed to *.lokd.
Status: the network team confirms FS-02's switch port can be shut down remotely. Backups of FS-02 from 02:00 are verified clean.

Incident Response Playbook, ransomware section
IR-1. Isolate the affected host from the network immediately.
IR-2. Do not power off the host (memory evidence would be lost) unless encryption is actively spreading to other systems and network isolation is impossible.
IR-3. Take a forensic disk and memory image before any rebuild or reimage.
IR-4. Restore from verified backups only after IR-3.

Text of the ransom note found on the server: "Do NOT disconnect this server from the network or all your files will be deleted immediately. Contact us within 24 hours."

Service desk note: "Users are asking when Projects will be back; the fastest fix is to reimage from the 02:00 backup now."
""",
[("isolate_and_image", "Isolation is available, so the server is cut off from the network and imaged before any rebuild."),
 ("power_off_now", "Shutting the server down is the fastest way to stop the encryption."),
 ("reimage_immediately", "Verified clean backups exist, so reimaging now restores service fastest."),
 ("monitor_only", "The ransom note warns that disconnecting will delete the files, so the server stays online while the team watches.")],
"isolate_and_image", 1),

# ------------------------------------------------------------------ rk07
# why: no supplier > 60% of the quarter's units (incl. this order). Quarter so far A
# 5,000 + B 2,000 + new 3,000 = 10,000 -> A max 6,000 -> at most 1,000 more to A.
# A $4.00, B $4.60 -> cheapest compliant: 1,000 A / 2,000 B ($13,200) vs all B ($13,800).
# Twin: A 4,000, B 3,000 -> A max 6,000 -> 2,000 A / 1,000 B ($12,600) now allowed.
C("rk07", "How should the new order for housings be split between suppliers?",
"""
Purchasing — Q4 2026 orders for die-cast housings (part DH-440), Orrin Controls

Supply Risk Rule SR-3: no single supplier may provide more than 60% of the units of a critical part ordered in a quarter, counting all orders placed in that quarter including the new one.
Commercial rule: among allocations meeting SR-3, choose the lowest cost.

Units already ordered this quarter
- Supplier A (Kessel Castings): 5,000 units.
- Supplier B (Tarn Diecast): 2,000 units.

New order to place: 3,000 units.
Prices: Kessel $4.00 per unit; Tarn $4.60 per unit.

Allocations under consideration
- All 3,000 to Kessel.
- 2,000 to Kessel, 1,000 to Tarn.
- 1,000 to Kessel, 2,000 to Tarn.
- All 3,000 to Tarn.

Buyer's note: "SR-3 is about each order, surely? This order on its own is 100% Kessel either way if we send it all there."
""",
[("all_to_kessel", "The 60% limit applies to each order on its own, and Kessel is cheapest."),
 ("kessel_2000_tarn_1000", "Sending 2,000 units to Kessel keeps it at or below 60% of the quarter and is the cheapest allocation that does."),
 ("kessel_1000_tarn_2000", "Only 1,000 more units can go to Kessel before it passes 60% of the quarter, so this is the cheapest compliant split."),
 ("all_to_tarn", "Diversification means a new order should go to the smaller supplier.")],
"kessel_1000_tarn_2000", 3,
twin=T([("- Supplier A (Kessel Castings): 5,000 units.", "- Supplier A (Kessel Castings): 4,000 units."),
        ("- Supplier B (Tarn Diecast): 2,000 units.", "- Supplier B (Tarn Diecast): 3,000 units.")], "kessel_2000_tarn_1000")),

# ------------------------------------------------------------------ rk08
# why: bank detail changes must be verified by call-back to the number already on
# file; until verified, no payment to either account. AP called the number in the
# email -> not valid. -> hold. Email's "do not call" is the requester's instruction.
# Twin: call-back to number on file confirmed -> pay new account.
C("rk08", "What should accounts payable do with the Tamsin Packaging payment?",
"""
Accounts Payable — payment run 25 September 2026
Invoice TP-7720, Tamsin Packaging, $38,400, due today.

Payment Controls Standard PC-4
PC-4.1 Any request to change a supplier's bank details must be verified by a call-back to the phone number already held on the vendor master file, not a number supplied with the request.
PC-4.2 Until the change is verified or rejected, no payment is released to either the old or the new account.
PC-4.3 Late-payment fees are accepted as a cost of this control.

Change request received 21 September by email from "accounts@tamsin-packaging.example":
"Our bank has changed. Please pay all invoices to the new account below from today. This is urgent and approved by our CFO — please do not call, our phones are being moved. If needed, call +44 7700 900 412."
Call-back status: AP called the number given in the email; the person who answered confirmed the change.

Supplier contract: late-payment fee 1% per month.
""",
[("pay_new_account", "The change has been confirmed by a call-back to the number on file, so the invoice is paid to the new account."),
 ("pay_old_account", "The invoice is due today, so paying the old account avoids a late fee while the change is checked."),
 ("hold_and_call_back", "The change has not been verified through the number on file, so payment is held until it is.")],
"hold_and_call_back", 2,
twin=T([("Call-back status: AP called the number given in the email; the person who answered confirmed the change.",
         "Call-back status: AP called the number on the vendor master file (Tamsin head office, on file since 2019) on 24 September; the finance director confirmed the change (reference CB-2231).")], "pay_new_account")),

# ------------------------------------------------------------------ rk09
# why: access method depends on employment status: third-party contractors -> VDI;
# employees -> VPN. Marek is an agency contractor (company laptop does not change
# status). Direct RDP and shared admin prohibited. -> VDI.
C("rk09", "Which remote access method should be provisioned for Marek?",
"""
Access request AR-6619 — Marek Olsen, database contractor via Selwood Talent (agency), 3-month engagement
Needs: read access to reporting databases from home, weekdays.
Equipment: company laptop issued for the engagement.

Remote Access Standard RA-2
RA-2.1 Employees connect through the corporate VPN.
RA-2.2 Third parties (contractors, agency workers, suppliers) connect only through a VDI session, whatever device they use.
RA-2.3 Direct RDP from the internet is prohibited.
RA-2.4 Shared or generic admin accounts are prohibited.

Team lead's note: "He's on a company laptop, so treat him like staff and give him VPN; VDI is slow for SQL work."
Firewall history: a direct RDP rule for the old reporting server was opened in 2023 and never closed.
""",
[("corporate_vpn", "Marek uses a company laptop, so he is treated as an employee and gets VPN."),
 ("vdi_session", "Marek is an agency contractor, and third parties may connect only through VDI."),
 ("direct_rdp", "The 2023 firewall rule is still open, so direct RDP is already available and quickest."),
 ("shared_admin_account", "A shared reporting login avoids creating an account for a short engagement.")],
"vdi_session", 1),

# ------------------------------------------------------------------ rk10
# why: appetite: retained loss per event <= $50,000 (deductible is the per-event
# retention). Expected annual cost = premium + expected retained losses (0.5 claims x
# min(deductible, 80k)). 25k: 90,000 + 12,500 = 102,500. 50k: 70,000 + 25,000 = 95,000.
# 100k: 45,000 + 40,000 = 85,000 but per-event retention 100k > 50k -> excluded.
# -> 50k deductible.
C("rk10", "Which deductible should be chosen at the property insurance renewal?",
"""
Insurance Renewal Paper — Carrick Foods, property damage policy, renewal 1 December 2026

Risk Appetite Statement RA-5: the company will retain no more than $50,000 of loss on any single event.
Selection rule: among options within RA-5, choose the lowest expected annual cost, where expected annual cost = premium + expected retained losses.
Claims history basis (broker's model): 0.5 claims a year on average, average claim size $80,000. Each claim is retained up to the deductible.

Options quoted by Halden Re
| Deductible per event | Annual premium |
| $25,000 | $90,000 |
| $50,000 | $70,000 |
| $100,000 | $45,000 |

Finance director's note: "The $100k option is clearly cheapest, and our expected retained loss would only be $40k a year, which is under the $50k appetite."
""",
[("deductible_25k", "The smallest deductible keeps the most risk with the insurer, which is always the safest choice."),
 ("deductible_50k", "The $50,000 deductible respects the per-event limit and has the lowest expected cost of the options that do."),
 ("deductible_100k", "The $100,000 option has the lowest expected cost, and its $40,000 expected annual retention is within the $50,000 appetite.")],
"deductible_50k", 2),

# ------------------------------------------------------------------ rk11
# why: customer payment keys need Level 3 HSM; must be live by go-live (6 weeks).
# Cloud KMS Level 2 fails. On-prem Level 3 but 12-week lead time > 6 -> fails.
# Cloud HSM Level 3, available -> only option. 3-yr: cloud HSM 4,800*36 = 172,800;
# on-prem 95,000 + 1,500*36 = 149,000. Twin: go-live in 16 weeks -> on-prem available
# and cheaper -> on-prem.
C("rk11", "Which key-management option should the payments team adopt?",
"""
Architecture Board paper — Key management for the Kestrel Pay card-tokenisation service
Go-live date: in 6 weeks (fixed by the scheme certification slot).

Security requirement SEC-14: keys protecting customer payment data must be held in a hardware security module certified to SecStore Level 3 or higher.
Selection rule: among options meeting SEC-14 that can be in service by go-live, choose the lowest three-year cost.

Options
| Option | Certification | Lead time | Three-year cost |
| Cloud KMS (standard) | SecStore Level 2 | immediate | $21,600 |
| Cloud HSM (dedicated) | SecStore Level 3 | 1 week | $172,800 ($4,800 a month) |
| On-premises HSM pair | SecStore Level 3 | 12 weeks | $149,000 ($95,000 + $1,500 a month) |

Engineering lead's note: "Level 2 is fine for keys used by internal services." (These keys protect customer card data.)
""",
[("cloud_kms_standard", "Level 2 is enough for keys used by internal services, and Cloud KMS is by far the cheapest."),
 ("cloud_hsm_dedicated", "Cloud HSM is the only Level 3 option that can be in service before go-live."),
 ("on_prem_hsm", "The on-premises HSM meets Level 3, can be delivered before go-live and has the lower three-year cost.")],
"cloud_hsm_dedicated", 2,
twin=T([("Go-live date: in 6 weeks (fixed by the scheme certification slot).", "Go-live date: in 16 weeks (fixed by the scheme certification slot).")], "on_prem_hsm")),

# ------------------------------------------------------------------ rk12
# why: alternate site >= 30 km from primary, outside the primary's flood zone, travel
# <= 90 min; cheapest. P 18 km fails; Q same flood zone (River Tarn zone 3) fails;
# S 150 min fails; R 55 km, 85 min, different zone -> R.
C("rk12", "Which site should be contracted as the business continuity location?",
"""
Business Continuity Plan review — Selby Mutual Building Society
Primary office: Tarnside House, Selby (River Tarn flood zone 3).

Continuity Standard BC-6
- The alternate site must be at least 30 km from the primary office.
- It must not lie in the same flood zone as the primary office.
- Staff travel time from the primary office must be 90 minutes or less.
- Choose the cheapest site meeting all three.

Candidate sites (work-area recovery providers)
| Site | Distance | Flood zone | Travel time | Monthly fee |
| Brook Park | 18 km | none | 30 min | $2,000 |
| Hollin Gate | 42 km | River Tarn zone 3 | 70 min | $2,400 |
| Carden Works | 55 km | none | 85 min | $3,100 |
| Vellan Hub | 120 km | none | 150 min | $1,900 |

Operations manager's note: "Brook Park is closest and staff will actually go there; that matters more than a distance rule."
""",
[("brook_park", "Staff are most likely to reach Brook Park, which matters more than the distance rule."),
 ("hollin_gate", "Hollin Gate is far enough away and within travel time, and the shared flood-zone risk is managed by the provider's own defences."),
 ("carden_works", "Carden Works is the only site that is far enough away, outside the primary's flood zone and within travel time."),
 ("vellan_hub", "Vellan Hub is the cheapest and the furthest from any shared local risk.")],
"carden_works", 1),

# ------------------------------------------------------------------ rk13
# why: standard change only for pre-approved templates (FW-ALLOW-443 covers port 443 to
# approved SaaS list only; this is port 8443 to a new partner -> not covered). Emergency
# change only with an open Severity 1 incident (none). -> normal change via CAB.
C("rk13", "Which change type should be raised for the firewall rule?",
"""
Change request draft — allow outbound traffic from app server APP-17 to Norland Logistics API (partner.norland.example), TCP port 8443.
Business driver: new partner integration, launch planned in 3 days.

Change Policy (Brisk Bank IT)
CP-1. Standard change: only for changes that exactly match a pre-approved template. Template FW-ALLOW-443 covers outbound TCP 443 to destinations on the approved SaaS list.
CP-2. Normal change: needs Change Advisory Board approval; the next CAB meets in 6 days.
CP-3. Emergency change: only to restore service or contain a security incident under an open Severity 1 incident.
Currently open incidents: none of Severity 1.

Email from the Sales VP: "Mark this as an emergency change. The launch is critical and the CAB can't hold us up."
Network engineer: "It's basically the same as FW-ALLOW-443, just a different port."
""",
[("standard_change", "The request is close enough to template FW-ALLOW-443 to count as pre-approved."),
 ("normal_change", "The request matches no template and there is no Severity 1 incident, so it goes to CAB as a normal change."),
 ("emergency_change", "The launch is business-critical and a senior leader has asked for it, which justifies an emergency change.")],
"normal_change", 1),

# ------------------------------------------------------------------ rk14
# why: Port Selim is level 4 now; level 5 applies from 1 Nov 2026. Trip 12-15 Oct ->
# level 4 -> approve with security conditions. City rating governs (country rating 3
# irrelevant). Twin: trip 12-15 Nov -> level 5 -> not permitted -> reject.
C("rk14", "What decision should the travel risk desk make on this trip request?",
"""
Travel Risk Policy (Castell Engineering)
TR-1. Risk levels are set per city by our security adviser; where a city has its own rating, it overrides the country rating.
TR-2. Levels 1-3: approve normally. Level 4: approve only with security conditions (pre-travel briefing, approved itinerary, tracking app). Level 5: travel not permitted.
TR-3. Ratings apply to the dates of travel.

Adviser bulletin, 20 September 2026
Country: Ostral — level 3.
City: Port Selim — currently level 4. Raised to level 5 with effect from 1 November 2026 (expected unrest around the election).

Trip request TRQ-8841
Traveller: Amara Quist, site engineer. Destination: Port Selim desalination plant. Dates: 12-15 October 2026.
Purpose: commissioning inspection (cannot be done remotely).

Line manager's comment: "The bulletin says level 5, so surely we just say no?"
""",
[("approve_normally", "Ostral as a country is rated level 3, which covers all its cities, so the trip can be approved normally without extra conditions."),
 ("approve_with_conditions", "Port Selim is level 4 on the travel dates, so the trip is approved with the security conditions."),
 ("reject_trip", "Port Selim is level 5 on the travel dates, so the trip is not permitted.")],
"approve_with_conditions", 2,
twin=T([("Dates: 12-15 October 2026.", "Dates: 12-15 November 2026.")], "reject_trip")),

# ------------------------------------------------------------------ rk15
# why: rating B -> credit allowed; limit = min(10% of net worth, $50,000) = min(20,000,
# 50,000) = $20,000. LC only for export customers (domestic). -> net 30, $20k limit.
C("rk15", "Which credit terms should be offered to the new customer?",
"""
Credit Policy (Aldermoor Aggregates), new trade accounts
CR-1. Customers rated A or B by Credora may be given 30-day terms. Customers rated C or below must prepay.
CR-2. Credit limit = the lower of 10% of the customer's net worth or $50,000.
CR-3. Letters of credit are used only for export customers.

Application CA-3170 — Hendry Landscapes Ltd (domestic)
Credora rating: B. Net worth (latest filed accounts): $200,000.
First order: $18,000 of paving stone, delivery in October.

Sales rep's note: "Standard new-account limit is $50k, isn't it? They'll want room for spring orders."
Credit controller's note: "Some firms make new customers prepay the first order; we have no such rule."
""",
[("net30_limit_50k", "$50,000 is the policy's limit for new accounts, which leaves room for later orders."),
 ("net30_limit_20k", "A B rating allows 30-day terms, and 10% of net worth caps the limit at $20,000."),
 ("prepayment_only", "New customers should prepay their first order until they build a history."),
 ("letter_of_credit", "A letter of credit gives the strongest security for a new customer.")],
"net30_limit_20k", 1),

# ------------------------------------------------------------------ rk16
# why: product is distributed -> AGPL banned; LGPL allowed only when dynamically
# linked; target <= 200 ms; fastest compliant. Quillparse AGPL out. Swiftcsv LGPL,
# static only -> out. Tallyread Apache 150 ms ok. Minirow 260 ms fails target.
# -> Tallyread. Twin: Swiftcsv supports dynamic linking -> 95 ms fastest compliant.
C("rk16", "Which CSV parsing library should be used in the field app?",
"""
Engineering decision — CSV import for the Harbour Inspect field app (installed on customers' tablets)
Performance target: parse a 10,000-row file in 200 ms or less on the reference tablet.

Open Source Policy OSP-3
3.1 In any product distributed to customers, AGPL and GPL libraries are not allowed.
3.2 LGPL libraries are allowed only when dynamically linked.
3.3 MIT, BSD and Apache 2.0 libraries are allowed.
3.4 Choose the fastest allowed library that meets the performance target.

Benchmarks
| Library | Licence | Linking | Time for 10,000 rows |
| Quillparse | AGPL-3.0 | any | 80 ms |
| Swiftcsv | LGPL-3.0 | static linking only | 95 ms |
| Tallyread | Apache 2.0 | any | 150 ms |
| Minirow | MIT | any | 260 ms |

Developer's note: "AGPL only bites on servers, and this runs on tablets, so Quillparse should be fine."
""",
[("quillparse", "AGPL only matters for server software, so the fastest library can be used on tablets."),
 ("swiftcsv", "Swiftcsv is LGPL used through dynamic linking, and it is the fastest allowed library within target."),
 ("tallyread", "Tallyread is the fastest library whose licence and linking are allowed and that meets the 200 ms target."),
 ("minirow", "MIT is the most permissive licence, so Minirow carries the least risk.")],
"tallyread", 2,
twin=T([("| Swiftcsv | LGPL-3.0 | static linking only | 95 ms |", "| Swiftcsv | LGPL-3.0 | dynamic linking (shared library) | 95 ms |")], "swiftcsv")),

# ------------------------------------------------------------------ rk17
# why: replace if repair > 70% of replacement value (amended from 60% for policies
# renewed on/after 1 Apr 2026; this policy renewed 1 May 2026). Repair 26,000 /
# 40,000 = 65% -> not over 70% -> repair. Cash settlement only if insured does not
# reinstate (it does).
C("rk17", "How should the loss adjuster settle the server-room claim?",
"""
Claim CL-50231 — Pennant Print Ltd, escape of water into the server room, 2 September 2026
Policy: commercial property, renewed 1 May 2026.

Settlement basis (policy wording, section 9)
9.1 Where the cost of repair is more than 60% of the replacement value, the insurer replaces the damaged equipment; otherwise it pays for repair.
9.2 A cash settlement is made only if the insured chooses not to reinstate the equipment.
Endorsement 9A (policies renewed on or after 1 April 2026): in 9.1, "60%" is replaced by "70%".

Adjuster's findings
Damaged equipment: storage array and two switches.
Repair quote (Vantor Technical Services): $26,000.
Replacement value (like for like): $40,000.
Insured's position: wishes to reinstate and keep the equipment in use.

Insured's IT manager: "We'd much prefer brand-new kit after this."
""",
[("repair", "Repair at 65% of replacement value is below the 70% threshold that applies to this policy, so the insurer pays for repair."),
 ("replace", "The repair cost is over 60% of the replacement value under section 9.1, so the insurer must replace the damaged equipment."),
 ("cash_settlement", "A cash settlement lets the insured choose between repair and new kit, which is simplest for both parties.")],
"repair", 2),

# ------------------------------------------------------------------ rk18
# why: margin = (net revenue - unit cost - any company-paid shipping) / net revenue;
# floor 35%. Unit cost $55. flat 15%: (85-55)/85 = 35.3% ok, saving $15. 10% + free
# shipping: (90-55-4)/90 = 34.4% fails. rebate 12%: (88-55)/88 = 37.5% ok, saving $12.
# Largest saving among compliant = flat 15%.
# Twin: unit cost $56 -> flat 29/85 = 34.1% fails; 10%+ship 30/90 = 33.3% fails;
# rebate 32/88 = 36.4% ok -> rebate.
C("rk18", "Which discount structure should be offered to the distributor?",
"""
Deal desk — Vellan Garden Wholesale, annual order of 1,000 irrigation controllers
List price: $100 per unit. Unit cost: $55. Normal shipping: $4 per unit, charged to the customer.

Pricing Policy PP-2
PP-2.1 Deal margin = (net revenue per unit - unit cost - any shipping cost the company pays) / net revenue per unit.
PP-2.2 Deal margin must be at least 35%.
PP-2.3 Among structures meeting PP-2.2, offer the one that gives the customer the largest saving per unit.

Structures proposed by the account manager
- Flat discount of 15%.
- 10% discount plus free shipping (the company pays the $4 carrier charge).
- 12% year-end volume rebate.

Account manager's note: "Free shipping costs us nothing really — it's just a pass-through."
""",
[("flat_15pct", "A flat 15% keeps margin at or above 35% and gives the largest saving of the structures that do."),
 ("discount_10pct_free_shipping", "Free shipping is a pass-through, so this gives a $14 saving while keeping the margin above 35%."),
 ("rebate_12pct", "The 12% rebate is the only structure that keeps the deal margin at or above 35%.")],
"flat_15pct", 3,
twin=T([("Unit cost: $55.", "Unit cost: $56.")], "rebate_12pct")),

# ------------------------------------------------------------------ rk19
# why: 320 extra hours over 4 weeks. Overtime only: 320/8/4 = 10 h/week each -> 50 h >
# 48 h weekly cap -> fails. Outsource: handles customer personal data, no signed DPA ->
# fails. Temps: 320 x 38 = 12,160. Mix: 8 staff x 8 h x 4 wk = 256 h x 45 = 11,520 +
# 64 h x 38 = 2,432 -> 13,952. Cheapest compliant = temps.
C("rk19", "How should the claims backlog be resourced?",
"""
Resourcing decision — claims backlog, Brightwater Mutual (October 2026)
Extra work: 320 hours over the next 4 weeks. Team: 8 claims handlers, each contracted for 40 hours a week.

Rules
W1. No employee may work more than 48 hours in any single week.
W2. Any outside firm handling customer personal data must have a signed Data Processing Agreement (DPA) before work starts.
W3. Choose the cheapest option meeting W1 and W2.

Options
- Overtime only: the 8 handlers share all 320 hours equally. Overtime rate $45 per hour.
- Agency temps (Selwood Talent): $38 per hour for all 320 hours.
- Outsource to Datacove Claims Services: fixed price $11,500. Datacove has not signed our DPA; it says it can sign "within a month or two".
- Mix: each handler works 8 overtime hours a week at $45, and temps cover the remaining hours at $38.

Team leader's note: "Ten extra hours a week is fine — the 48-hour limit is averaged over 17 weeks anyway."
""",
[("overtime_only", "Ten extra hours a week stays within the 48-hour limit once hours are averaged over 17 weeks, and it keeps the work in-house."),
 ("agency_temps", "Overtime alone breaks the weekly hours cap and Datacove has no DPA, so temps are the cheapest option that complies."),
 ("outsource_datacove", "Datacove is cheapest, and the DPA can be signed after the work starts."),
 ("overtime_temp_mix", "Keeping most hours in-house through capped overtime is the cheapest option that complies.")],
"agency_temps", 3),

# ------------------------------------------------------------------ rk20
# why: projects must pay back within 3 years; budget $250k; maximise total NPV.
# P2 payback 3.5 y fails. P1 (200k, NPV 90k) + P3 (100k, NPV 50k) = 300k > 250k.
# Best within budget: P1 alone (90k) > P3 alone (50k). -> fund P1.
# Twin: budget $300k -> P1 + P3 fits, NPV 140k -> fund both.
C("rk20", "Which projects should the investment committee fund this year?",
"""
Capital Allocation Paper — Harrowgate Builders Merchants, FY2027
Capital budget available: $250,000.

Capital Rules
CA-1. A project may be funded only if its simple payback period is 3 years or less.
CA-2. The combined cost of funded projects must not exceed the capital budget.
CA-3. Among combinations meeting CA-1 and CA-2, fund the one with the highest total net present value (NPV).

Proposals
| Project | Cost | NPV | Payback |
| P1 — racking automation, Ferris Lane | $200,000 | $90,000 | 2.5 years |
| P2 — solar canopy, Tanfield yard | $150,000 | $70,000 | 3.5 years |
| P3 — telematics for delivery fleet | $100,000 | $50,000 | 2.0 years |

Sustainability lead's note: "P2 and P3 together use the budget exactly and give $120k of NPV."
""",
[("fund_p1", "P1 alone gives the highest total NPV of the combinations that pass the payback rule and fit the budget."),
 ("fund_p3", "P3 has the quickest payback, which makes it the least risky use of capital and the project the committee should prefer."),
 ("fund_p1_and_p3", "P1 and P3 both pass the payback rule and together fit the budget, giving the highest total NPV."),
 ("fund_p2_and_p3", "P2 and P3 together use exactly the budget and deliver $120,000 of NPV.")],
"fund_p1", 2,
twin=T([("Capital budget available: $250,000.", "Capital budget available: $300,000.")], "fund_p1_and_p3")),

# ------------------------------------------------------------------ rk21
# why: store >= 10 m from occupied buildings, bund >= 110% of largest container,
# inside security fence; choose compliant shed nearest the loading bay. A 8 m fails;
# B bund 100% fails; D outside fence fails; C 12 m, 115%, inside -> C.
C("rk21", "Which shed should be used to store the new solvent delivery?",
"""
Hazardous Substances Storage Rules (Ellery Coatings, site standard HS-4)
HS-4.1 Flammable solvent stores must be at least 10 m from any occupied building.
HS-4.2 The store's bund must hold at least 110% of the largest single container stored.
HS-4.3 The store must be inside the site security fence.
HS-4.4 Among stores meeting HS-4.1 to HS-4.3, use the one nearest the loading bay.

Delivery: 8 drums of xylene, 205 litres each (largest container 205 litres).

Candidate sheds
| Shed | Distance to nearest occupied building | Bund capacity (% of largest container) | Inside fence | Distance to loading bay |
| A | 8 m (site office) | 120% | yes | 15 m |
| B | 15 m | 100% | yes | 20 m |
| C | 12 m | 115% | yes | 45 m |
| D | 25 m | 150% | no | 60 m |

Yard supervisor's note: "Shed A is right by the bay and it's only 2 metres short; we used it for paints last year."
""",
[("shed_a", "Shed A is nearest the loading bay, and being 2 m short of the distance rule is a minor gap."),
 ("shed_b", "Shed B is far enough from buildings and close to the bay, and a full-size bund is enough for drums."),
 ("shed_c", "Shed C is the only shed meeting the distance, bund and fence rules, so it is used despite the longer walk."),
 ("shed_d", "Shed D has the largest bund and the most distance from buildings, which makes it the safest store for flammable solvents.")],
"shed_c", 1),
]
