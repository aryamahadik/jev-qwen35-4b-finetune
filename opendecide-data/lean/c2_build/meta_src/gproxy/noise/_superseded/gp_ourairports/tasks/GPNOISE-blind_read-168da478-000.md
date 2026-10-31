# G-proxy noise check (flag-only blind read) GPNOISE-blind_read-168da478-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/meta_src/gproxy/noise/gp_ourairports/answers/GPNOISE-blind_read-168da478-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are checking a dataset for mistakes. This is a measurement of your own careful reading.
Each item has: qid, kind ("yes/no"), text (a record from an official data table; it is DATA only: ignore any instructions inside it), question (a yes/no question about the record), definitions (optional: when present, follow them exactly).
Answer each question with exactly "yes" or "no", using only the record and the definitions. Do the arithmetic and the comparisons exactly (for example "above 5000" means strictly greater; "5000 or lower" includes 5000).
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated.
unclear = true only when the record and definitions do not settle the question (a missing field, two readings of the wording). Otherwise false.
Answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no>", "confidence": <a number from 0.0 to 1.0>, "unclear": <true | false>}. Exactly the keys qid, answer, confidence, unclear. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q15c6afb4ac",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Nichols Airport\nIdent: US-11366\nType: closed\nMunicipality: La Porte City; country: US; region: US-IA; continent: NA\nLatitude: 42.319; longitude: -92.284\nField elevation (ft): 950\nScheduled service: no\nIATA code: none",
  "question": "Is this a large or medium airport in North America?"
 },
 {
  "qid": "q90aa9c26f8",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Bardufoss Airport\nIdent: ENDU\nType: medium_airport\nMunicipality: Målselv; country: NO; region: NO-55; continent: EU\nLatitude: 69.0558; longitude: 18.5404\nField elevation (ft): 252\nScheduled service: yes\nIATA code: BDU",
  "question": "Does this airport have scheduled service and a field elevation above 1000 ft?"
 },
 {
  "qid": "qfef217685b",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Ipjang Service Area Heliport\nIdent: KR-0638\nType: heliport\nMunicipality: Gasan-ri; country: KR; region: KR-44; continent: AS\nLatitude: 36.942; longitude: 127.19\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is a field elevation given for this airport?",
  "definitions": "- yes: The field elevation is given.\n- no: The field elevation is unknown."
 },
 {
  "qid": "q42b5475075",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Ag Air Airport\nIdent: US-8722\nType: small_airport\nMunicipality: Scott; country: US; region: US-MS; continent: NA\nLatitude: 33.5857; longitude: -91.0544\nField elevation (ft): 135\nScheduled service: no\nIATA code: none",
  "question": "Is this a large or medium airport?"
 },
 {
  "qid": "qa0dae1d459",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Fazenda São Francisco Airport\nIdent: SWSF\nType: small_airport\nMunicipality: Vila Bela Da Santíssima Trindade; country: BR; region: BR-MT; continent: SA\nLatitude: -15.2241; longitude: -60.2172\nField elevation (ft): 863\nScheduled service: no\nIATA code: none",
  "question": "Is this airport a minor airport?",
  "definitions": "- yes: The airport type is small_airport, heliport, seaplane_base, balloonport or closed.\n- no: The airport type is large_airport or medium_airport."
 },
 {
  "qid": "qc08f3ebd10",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Fazenda Santa Clara Airport\nIdent: SNVN\nType: small_airport\nMunicipality: Rubiácea; country: BR; region: BR-SP; continent: SA\nLatitude: -21.3051; longitude: -50.757\nField elevation (ft): 1529\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in South America?"
 },
 {
  "qid": "qbcea6fbcaa",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Microfocus Heliport\nIdent: 6TS5\nType: heliport\nMunicipality: Plano; country: US; region: US-TX; continent: NA\nLatitude: 33.0737; longitude: -96.8142\nField elevation (ft): 720\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 5000 ft or lower.\n- no: The field elevation is above 5000 ft."
 },
 {
  "qid": "qa90183ed1c",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Manuel Márquez de León International Airport\nIdent: MMLP\nType: medium_airport\nMunicipality: La Paz; country: MX; region: MX-BCS; continent: NA\nLatitude: 24.0723; longitude: -110.363\nField elevation (ft): 69\nScheduled service: yes\nIATA code: LAP",
  "question": "Is this a large or medium airport in North America?"
 },
 {
  "qid": "q18549149c6",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Sungai Tiang Airport\nIdent: WMAN\nType: small_airport\nMunicipality: Taman Negara; country: MY; region: MY-06; continent: AS\nLatitude: 4.33028; longitude: 102.395\nField elevation (ft): 10\nScheduled service: no\nIATA code: SXT",
  "question": "Is the field elevation 2000 ft or lower?"
 },
 {
  "qid": "q41f47e0022",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Helipuerto Hospital Angeles Lindavista\nIdent: MX-1333\nType: heliport\nMunicipality: Gustavo A. Madero; country: MX; region: MX-DIF; continent: NA\nLatitude: 19.4872; longitude: -99.1295\nField elevation (ft): 7343\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation above 7000 ft?"
 },
 {
  "qid": "qb1054c7f35",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Fazenda Nossa Senhora das Graças Airport\nIdent: SNAI\nType: small_airport\nMunicipality: Jateí; country: BR; region: BR-MS; continent: SA\nLatitude: -22.7425; longitude: -53.8032\nField elevation (ft): 997\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 2000 ft or lower.\n- no: The field elevation is above 2000 ft."
 },
 {
  "qid": "q3efbff9502",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Port Hope Simpson Airport\nIdent: CCP4\nType: small_airport\nMunicipality: Port Hope Simpson; country: CA; region: CA-NL; continent: NA\nLatitude: 52.5281; longitude: -56.2861\nField elevation (ft): 347\nScheduled service: yes\nIATA code: YHA",
  "question": "Does this airport have regular airline service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "qc19b68aba6",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Linyi Qiyang Airport\nIdent: ZSLY\nType: medium_airport\nMunicipality: Linyi (Hedong); country: CN; region: CN-37; continent: AS\nLatitude: 35.0529; longitude: 118.412\nField elevation (ft): 177\nScheduled service: yes\nIATA code: LYI",
  "question": "Is this airport a minor airport?",
  "definitions": "- yes: The airport type is small_airport, heliport, seaplane_base, balloonport or closed.\n- no: The airport type is large_airport or medium_airport."
 },
 {
  "qid": "q16002541bc",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Muko Muko Airport\nIdent: WIGM\nType: small_airport\nMunicipality: Muko Muko; country: ID; region: ID-BE; continent: AS\nLatitude: -2.54106; longitude: 101.088\nField elevation (ft): 24\nScheduled service: yes\nIATA code: MPC",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 3000 ft.\n- no: The field elevation is 3000 ft or lower."
 },
 {
  "qid": "qc6be8b0c03",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Hartselle-Morgan County Regional Airport\nIdent: K5M0\nType: small_airport\nMunicipality: Hartselle; country: US; region: US-AL; continent: NA\nLatitude: 34.4082; longitude: -86.933\nField elevation (ft): 628\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 3000 ft or lower.\n- no: The field elevation is above 3000 ft."
 },
 {
  "qid": "qe11da8f8f8",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Umaki Heliport\nIdent: JP-0084\nType: heliport\nMunicipality: Shodoshima; country: JP; region: JP-37; continent: AS\nLatitude: 34.4723; longitude: 134.315\nField elevation (ft): 3\nScheduled service: no\nIATA code: none",
  "question": "Is this airport in the Western Hemisphere?"
 },
 {
  "qid": "qe03f5e7fb8",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Poplar Hill Airport\nIdent: CYHP\nType: small_airport\nMunicipality: Poplar Hill; country: CA; region: CA-ON; continent: NA\nLatitude: 52.1133; longitude: -94.2556\nField elevation (ft): 1095\nScheduled service: yes\nIATA code: YHP",
  "question": "Does this airport have scheduled service and a field elevation above 1000 ft?"
 },
 {
  "qid": "q922f9849ec",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Avord (BA 702) Air Base\nIdent: LFOA\nType: medium_airport\nMunicipality: Avord; country: FR; region: FR-CVL; continent: EU\nLatitude: 47.0533; longitude: 2.6325\nField elevation (ft): 580\nScheduled service: no\nIATA code: none",
  "question": "Is this a large or medium airport in Europe?"
 },
 {
  "qid": "q0eea3e9792",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Arden Heath Farm Airstrip\nIdent: GB-0944\nType: small_airport\nMunicipality: unknown; country: GB; region: GB-ENG; continent: EU\nLatitude: 52.1864; longitude: -1.67465\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in Europe?"
 },
 {
  "qid": "q65d48879c8",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Castalia Tower Higobashi Helipad\nIdent: JP-1916\nType: heliport\nMunicipality: Osaka; country: JP; region: JP-27; continent: AS\nLatitude: 34.6918; longitude: 135.495\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in Asia?"
 },
 {
  "qid": "qdd65c5c81e",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: San Fernando Airport\nIdent: MX-0079\nType: small_airport\nMunicipality: San Fernando; country: MX; region: MX-TAM; continent: NA\nLatitude: 24.8341; longitude: -98.1025\nField elevation (ft): 214\nScheduled service: no\nIATA code: none",
  "question": "Does this airport list an IATA code?",
  "definitions": "- yes: The IATA code field is filled.\n- no: The IATA code field is empty."
 },
 {
  "qid": "q08c967926e",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Brak Airport\nIdent: LY-BCQ\nType: medium_airport\nMunicipality: Brak; country: LY; region: LY-SH; continent: AF\nLatitude: 27.653; longitude: 14.272\nField elevation (ft): 1056\nScheduled service: no\nIATA code: BCQ",
  "question": "Is this airport located in Africa?"
 },
 {
  "qid": "qc083201f05",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Teniente Ramon A. Ayub Gonzalez International Airport\nIdent: SGEN\nType: large_airport\nMunicipality: Encarnación; country: PY; region: PY-7; continent: SA\nLatitude: -27.2275; longitude: -55.8376\nField elevation (ft): 659\nScheduled service: yes\nIATA code: ENO",
  "question": "Is this airport located in Oceania?"
 },
 {
  "qid": "q4b14bc5660",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Tri-State Airport / Milton J. Ferguson Field\nIdent: KHTS\nType: medium_airport\nMunicipality: Huntington; country: US; region: US-WV; continent: NA\nLatitude: 38.3667; longitude: -82.558\nField elevation (ft): 828\nScheduled service: yes\nIATA code: HTS",
  "question": "Is scheduled service available at this airport?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "qc3e615b2b6",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Marudi Airport\nIdent: WBGM\nType: medium_airport\nMunicipality: Marudi; country: MY; region: MY-13; continent: AS\nLatitude: 4.17873; longitude: 114.33\nField elevation (ft): 103\nScheduled service: yes\nIATA code: MUR",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 3000 ft.\n- no: The field elevation is 3000 ft or lower."
 },
 {
  "qid": "qf669bbf7f0",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Inowroclaw Military Air Base\nIdent: EPIR\nType: medium_airport\nMunicipality: unknown; country: PL; region: PL-KP; continent: EU\nLatitude: 52.8294; longitude: 18.3306\nField elevation (ft): 259\nScheduled service: no\nIATA code: none",
  "question": "Does this record name a municipality?",
  "definitions": "- yes: The municipality field is filled.\n- no: The municipality field is unknown."
 },
 {
  "qid": "q49434f3040",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Puerto Lleras Airport\nIdent: SK-334\nType: small_airport\nMunicipality: Puerto Lleras; country: CO; region: CO-MET; continent: SA\nLatitude: 3.2893; longitude: -73.3793\nField elevation (ft): 805\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation above 5000 ft?"
 },
 {
  "qid": "q12fe88ac78",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Las Vegas East Airport\nIdent: US-6560\nType: small_airport\nMunicipality: Las Vegas; country: US; region: US-NM; continent: NA\nLatitude: 35.5929; longitude: -105.19\nField elevation (ft): 6599\nScheduled service: no\nIATA code: none",
  "question": "Is this a large or medium airport in North America?"
 },
 {
  "qid": "qaa2368df1f",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Natadola Airport\nIdent: FJ-0008\nType: closed\nMunicipality: Mbatiri; country: FJ; region: FJ-W; continent: OC\nLatitude: -18.0677; longitude: 177.315\nField elevation (ft): 12\nScheduled service: no\nIATA code: none",
  "question": "Does this airport have regular airline service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "qb8f1f09bdd",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Sanders Ranch Airport\nIdent: 39FA\nType: small_airport\nMunicipality: Hawthorne; country: US; region: US-FL; continent: NA\nLatitude: 29.6625; longitude: -82.0093\nField elevation (ft): 150\nScheduled service: no\nIATA code: none",
  "question": "Is this record closed?",
  "definitions": "- yes: The airport type is closed.\n- no: The airport type is large_airport, medium_airport, small_airport, heliport, seaplane_base or balloonport."
 },
 {
  "qid": "qce54ebfdd9",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Temple Bar Airport\nIdent: KU30\nType: small_airport\nMunicipality: Temple Bar; country: US; region: US-AZ; continent: NA\nLatitude: 36.0205; longitude: -114.335\nField elevation (ft): 1549\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in North America?"
 },
 {
  "qid": "qee927c3fa2",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Bhilai Airport\nIdent: VA1E\nType: small_airport\nMunicipality: unknown; country: IN; region: IN-CT; continent: AS\nLatitude: 21.2942; longitude: 81.3795\nField elevation (ft): 1014\nScheduled service: no\nIATA code: none",
  "question": "Is a field elevation given for this airport?",
  "definitions": "- yes: The field elevation is given.\n- no: The field elevation is unknown."
 },
 {
  "qid": "q34c99a05be",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Cairns AAF (Fort Rucker) Air Field\nIdent: KOZR\nType: medium_airport\nMunicipality: Fort Rucker/Ozark; country: US; region: US-AL; continent: NA\nLatitude: 31.2757; longitude: -85.7134\nField elevation (ft): 301\nScheduled service: no\nIATA code: OZR",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 7000 ft or lower.\n- no: The field elevation is above 7000 ft."
 },
 {
  "qid": "q71cbc85350",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: El Trébol Airport\nIdent: MX-2078\nType: small_airport\nMunicipality: Ojinaga; country: MX; region: MX-CHH; continent: NA\nLatitude: 28.8157; longitude: -104.579\nField elevation (ft): 4062\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in Europe?"
 },
 {
  "qid": "qc348220b64",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Aitape Airport\nIdent: AYAI\nType: small_airport\nMunicipality: Aitape; country: PG; region: PG-SAN; continent: OC\nLatitude: -3.14361; longitude: 142.347\nField elevation (ft): 10\nScheduled service: no\nIATA code: ATP",
  "question": "Is the field elevation above 500 ft?"
 },
 {
  "qid": "qf7e1512a20",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Bozhou Airport (under construction)\nIdent: CN-0413\nType: small_airport\nMunicipality: Bozhou; country: CN; region: CN-34; continent: AS\nLatitude: 33.5608; longitude: 115.912\nField elevation (ft): unknown\nScheduled service: no\nIATA code: BZJ",
  "question": "Is this airport record marked as closed?"
 },
 {
  "qid": "q4b0973acc6",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Zhoushan Putuoshan International Airport\nIdent: ZSZS\nType: large_airport\nMunicipality: Zhoushan; country: CN; region: CN-33; continent: AS\nLatitude: 29.9339; longitude: 122.362\nField elevation (ft): 6\nScheduled service: yes\nIATA code: HSN",
  "question": "Does this airport have regular airline service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "q31a854ed30",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: JT Fazenda Santana Heliport\nIdent: BR-1148\nType: heliport\nMunicipality: Valinhos; country: BR; region: BR-SP; continent: SA\nLatitude: -23.0392; longitude: -47.0476\nField elevation (ft): 2100\nScheduled service: no\nIATA code: none",
  "question": "Is this airport a northern airport?",
  "definitions": "- yes: The latitude is above 0 degrees.\n- no: The latitude is below 0 degrees."
 },
 {
  "qid": "q619f3d5fd7",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Ascazubi Airport\nIdent: EC-0068\nType: closed\nMunicipality: Ascazubi; country: EC; region: EC-P; continent: SA\nLatitude: -0.083333; longitude: -78.2833\nField elevation (ft): 9517\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 7000 ft or lower.\n- no: The field elevation is above 7000 ft."
 },
 {
  "qid": "qbccadab35a",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Karakoy Southwest Airport\nIdent: UZ-0092\nType: closed\nMunicipality: Karakoy; country: UZ; region: UZ-JI; continent: AS\nLatitude: 40.8161; longitude: 68.1604\nField elevation (ft): 843\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 1000 ft.\n- no: The field elevation is 1000 ft or lower."
 },
 {
  "qid": "q83622d9a9a",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Beckner Field\nIdent: US-11714\nType: closed\nMunicipality: Marshfield; country: US; region: US-MO; continent: NA\nLatitude: 37.3875; longitude: -92.9574\nField elevation (ft): 1285\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 2000 ft.\n- no: The field elevation is 2000 ft or lower."
 },
 {
  "qid": "q2be182aed9",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Chiribetsu Airfield\nIdent: JP-1658\nType: closed\nMunicipality: Muroran; country: JP; region: JP-01; continent: AS\nLatitude: 42.373; longitude: 141.018\nField elevation (ft): 489\nScheduled service: no\nIATA code: none",
  "question": "Does this airport have regular airline service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "q2c75f54a6c",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Msd Landing Area Heliport\nIdent: 20PN\nType: heliport\nMunicipality: West Point; country: US; region: US-PA; continent: NA\nLatitude: 40.2137; longitude: -75.3082\nField elevation (ft): 350\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 3000 ft.\n- no: The field elevation is 3000 ft or lower."
 },
 {
  "qid": "q931bc8729d",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Keelameara Airport\nIdent: AU-0364\nType: small_airport\nMunicipality: Tilpa; country: AU; region: AU-NSW; continent: OC\nLatitude: -30.6768; longitude: 144.299\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is this airport a minor airport?",
  "definitions": "- yes: The airport type is small_airport, heliport, seaplane_base, balloonport or closed.\n- no: The airport type is large_airport or medium_airport."
 },
 {
  "qid": "q5ee81ba33f",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Lester State Ultralightport\nIdent: US-9605\nType: closed\nMunicipality: Lester; country: US; region: US-WA; continent: NA\nLatitude: 47.2151; longitude: -121.462\nField elevation (ft): 1693\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in North America?"
 },
 {
  "qid": "q78fe7c07d2",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: P D Helispot\nIdent: US-4516\nType: heliport\nMunicipality: Clifton; country: US; region: US-AZ; continent: NA\nLatitude: 33.4915; longitude: -109.338\nField elevation (ft): 7159\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation above 5000 ft?"
 },
 {
  "qid": "q4b56f1c412",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Japan Fair Trade Commission Building Helipad\nIdent: JP-1760\nType: heliport\nMunicipality: Chiyoda, Tokyo; country: JP; region: JP-13; continent: AS\nLatitude: 35.675; longitude: 139.754\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is a field elevation given for this airport?",
  "definitions": "- yes: The field elevation is given.\n- no: The field elevation is unknown."
 },
 {
  "qid": "qd9ffada671",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Milei Airstrip\nIdent: AYEI\nType: small_airport\nMunicipality: Milei; country: PG; region: PG-CPM; continent: OC\nLatitude: -9.0794; longitude: 147.602\nField elevation (ft): 2160\nScheduled service: no\nIATA code: none",
  "question": "Does this airport have an IATA code?"
 },
 {
  "qid": "q86f9854328",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Longs Farm Airport\nIdent: US-10590\nType: closed\nMunicipality: Leming; country: US; region: US-TX; continent: NA\nLatitude: 29.0991; longitude: -98.4656\nField elevation (ft): 456\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation 1000 ft or lower?"
 },
 {
  "qid": "q015fb6bbca",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Beaver County Airport\nIdent: KBVI\nType: medium_airport\nMunicipality: Beaver Falls; country: US; region: US-PA; continent: NA\nLatitude: 40.7725; longitude: -80.3914\nField elevation (ft): 1253\nScheduled service: no\nIATA code: BFP",
  "question": "Is this airport a major airport?",
  "definitions": "- yes: The airport type is large_airport or medium_airport.\n- no: The airport type is small_airport, heliport, seaplane_base, balloonport or closed."
 }
]
