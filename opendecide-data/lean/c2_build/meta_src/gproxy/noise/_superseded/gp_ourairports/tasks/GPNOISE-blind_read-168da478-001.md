# G-proxy noise check (flag-only blind read) GPNOISE-blind_read-168da478-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/meta_src/gproxy/noise/gp_ourairports/answers/GPNOISE-blind_read-168da478-001.json

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
  "qid": "qaae3e99475",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Ballyjamesduff Airstrip\nIdent: IE-0019\nType: small_airport\nMunicipality: Ballyjamesduff; country: IE; region: IE-CN; continent: EU\nLatitude: 53.8644; longitude: -7.21496\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is this record located in Europe?",
  "definitions": "- yes: The continent field is EU.\n- no: The continent field is NA, AS, AF, SA, OC or AN."
 },
 {
  "qid": "qeff900afb7",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Caddo Mills Municipal Airport\nIdent: K7F3\nType: small_airport\nMunicipality: Caddo Mills; country: US; region: US-TX; continent: NA\nLatitude: 33.0362; longitude: -96.2431\nField elevation (ft): 542\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation above 5000 ft?"
 },
 {
  "qid": "q27df49639b",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Las Salinas Heliport\nIdent: SHLS\nType: heliport\nMunicipality: Viña Del Mar; country: CL; region: CL-VS; continent: SA\nLatitude: -32.9958; longitude: -71.5472\nField elevation (ft): 10\nScheduled service: no\nIATA code: none",
  "question": "Is this airport in the Northern Hemisphere?"
 },
 {
  "qid": "q4f52e90e4f",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Volare Balloon Field\nIdent: MX-2222\nType: balloonport\nMunicipality: Teotihuacán; country: MX; region: MX-MEX; continent: NA\nLatitude: 19.692; longitude: -98.8275\nField elevation (ft): 7500\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 7000 ft.\n- no: The field elevation is 7000 ft or lower."
 },
 {
  "qid": "q566b43e4c2",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: San Francisco Naciff Airport\nIdent: SLZF\nType: small_airport\nMunicipality: Nacif; country: BO; region: BO-B; continent: SA\nLatitude: -13.7486; longitude: -64.4537\nField elevation (ft): 482\nScheduled service: no\nIATA code: none",
  "question": "Is this airport a southern airport?",
  "definitions": "- yes: The latitude is below 0 degrees.\n- no: The latitude is above 0 degrees."
 },
 {
  "qid": "q6c0a2e6cb8",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Memorial Hermann The Woodlands Medical Center Heliport\nIdent: 26TS\nType: heliport\nMunicipality: Shenandoah; country: US; region: US-TX; continent: NA\nLatitude: 30.1745; longitude: -95.4532\nField elevation (ft): 150\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 2000 ft.\n- no: The field elevation is 2000 ft or lower."
 },
 {
  "qid": "q856b80b8ec",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Leziria Aerodrome\nIdent: PT-0041\nType: small_airport\nMunicipality: Vila Franca de Xira; country: PT; region: PT-11; continent: EU\nLatitude: 38.9023; longitude: -8.93682\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Does this record show a field elevation?",
  "definitions": "- yes: The field elevation is given.\n- no: The field elevation is unknown."
 },
 {
  "qid": "qbdc5752089",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Gilbert Aviation Heliport\nIdent: CA83\nType: heliport\nMunicipality: Visalia; country: US; region: US-CA; continent: NA\nLatitude: 36.4427; longitude: -119.316\nField elevation (ft): 310\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 2000 ft or lower.\n- no: The field elevation is above 2000 ft."
 },
 {
  "qid": "q6f4dbe5920",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Helfrick Heliport\nIdent: 8PN5\nType: heliport\nMunicipality: Elysburg; country: US; region: US-PA; continent: NA\nLatitude: 40.8334; longitude: -76.5497\nField elevation (ft): 1000\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in Asia?"
 },
 {
  "qid": "q649d9e168d",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Westberg-Rosling Farms Airport\nIdent: 74CO\nType: small_airport\nMunicipality: Roggen; country: US; region: US-CO; continent: NA\nLatitude: 40.0472; longitude: -104.209\nField elevation (ft): 4857\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 5000 ft.\n- no: The field elevation is 5000 ft or lower."
 },
 {
  "qid": "q56a76c03e9",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Prince Rupert/Seal Cove Seaplane Base\nIdent: CZSW\nType: seaplane_base\nMunicipality: Prince Rupert; country: CA; region: CA-BC; continent: NA\nLatitude: 54.3333; longitude: -130.283\nField elevation (ft): unknown\nScheduled service: no\nIATA code: ZSW",
  "question": "Is this airport in the Western Hemisphere?"
 },
 {
  "qid": "qa28b84cc32",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Elk Meadow Airstrip\nIdent: 55MT\nType: small_airport\nMunicipality: Hamilton; country: US; region: US-MT; continent: NA\nLatitude: 46.2311; longitude: -114.199\nField elevation (ft): 3720\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 2000 ft.\n- no: The field elevation is 2000 ft or lower."
 },
 {
  "qid": "q8a3b261553",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Orlando Bezerra de Menezes Airport\nIdent: SBJU\nType: small_airport\nMunicipality: Juazeiro do Norte; country: BR; region: BR-CE; continent: SA\nLatitude: -7.21932; longitude: -39.2691\nField elevation (ft): 1342\nScheduled service: yes\nIATA code: JDO",
  "question": "Can this airport handle scheduled flights?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "qa97f62511f",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Fazenda Pouso Alegre Airport\nIdent: SIXG\nType: small_airport\nMunicipality: Catalão; country: BR; region: BR-GO; continent: SA\nLatitude: -18.0323; longitude: -47.4639\nField elevation (ft): 2812\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 3000 ft.\n- no: The field elevation is 3000 ft or lower."
 },
 {
  "qid": "qafca154f3a",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Raroia Airport\nIdent: NTKO\nType: small_airport\nMunicipality: Raroia; country: PF; region: PF-U-A; continent: OC\nLatitude: -16.0505; longitude: -142.477\nField elevation (ft): 18\nScheduled service: yes\nIATA code: RRR",
  "question": "Is this airport in the Southern Hemisphere?"
 },
 {
  "qid": "q9911d1fe22",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Kure Airport\nIdent: US-9351\nType: closed\nMunicipality: Kure Atoll; country: US; region: US-HI; continent: OC\nLatitude: 28.3893; longitude: -178.297\nField elevation (ft): 12\nScheduled service: no\nIATA code: none",
  "question": "Is this airport record marked as closed?"
 },
 {
  "qid": "q5a403dff34",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Mabalacat West Airfield (Kamikaze West)\nIdent: PH-0114\nType: closed\nMunicipality: Mabalacat; country: PH; region: PH-PAM; continent: AS\nLatitude: 15.2173; longitude: 120.549\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in South America?"
 },
 {
  "qid": "q56bb3d902c",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Sarnoff Princeton Heliport\nIdent: 3NJ4\nType: heliport\nMunicipality: Princeton; country: US; region: US-NJ; continent: NA\nLatitude: 40.3334; longitude: -74.6329\nField elevation (ft): 90\nScheduled service: no\nIATA code: none",
  "question": "Can this airport handle scheduled flights?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "q4628ff38e9",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Cape Pole Seaplane Base\nIdent: Z71\nType: seaplane_base\nMunicipality: Cape Pole; country: US; region: US-AK; continent: NA\nLatitude: 55.9663; longitude: -133.797\nField elevation (ft): 0\nScheduled service: no\nIATA code: CZP",
  "question": "Is this airport in the Eastern Hemisphere?"
 },
 {
  "qid": "q932d77cb40",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: N 305 Helipad\nIdent: RK8T\nType: heliport\nMunicipality: Port Hamilton; country: KR; region: KR-46; continent: AS\nLatitude: 34.0289; longitude: 127.305\nField elevation (ft): 3\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation above 500 ft?"
 },
 {
  "qid": "qd223b91bcb",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Kuini Lavenia Airport\nIdent: NFTP\nType: small_airport\nMunicipality: Niuatoputapu; country: TO; region: TO-03; continent: OC\nLatitude: -15.9773; longitude: -173.791\nField elevation (ft): 30\nScheduled service: yes\nIATA code: NTT",
  "question": "Does this airport have regular airline service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "qd6ee06499c",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Mwadingusha Airport\nIdent: FZQJ\nType: small_airport\nMunicipality: Mwadingusha; country: CD; region: CD-HK; continent: AF\nLatitude: -10.7566; longitude: 27.2155\nField elevation (ft): 3707\nScheduled service: no\nIATA code: none",
  "question": "Is this a large or medium airport in Europe?"
 },
 {
  "qid": "q0b2c6e9b63",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Antelope Airpark\nIdent: 93CO\nType: small_airport\nMunicipality: Lake George; country: US; region: US-CO; continent: NA\nLatitude: 39.0253; longitude: -105.61\nField elevation (ft): 8700\nScheduled service: no\nIATA code: none",
  "question": "Is this airport record marked as closed?"
 },
 {
  "qid": "qcca2cd9e75",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Privolzhskiy Air Base\nIdent: RU-0303\nType: medium_airport\nMunicipality: Astrakhan; country: RU; region: RU-AST; continent: EU\nLatitude: 46.3957; longitude: 47.8877\nField elevation (ft): -66\nScheduled service: no\nIATA code: none",
  "question": "Is this a large or medium airport in Europe?"
 },
 {
  "qid": "q9b899d764e",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Valcourt Airport\nIdent: CSQ3\nType: small_airport\nMunicipality: Valcourt; country: CA; region: CA-QC; continent: NA\nLatitude: 45.4811; longitude: -72.3103\nField elevation (ft): 740\nScheduled service: no\nIATA code: none",
  "question": "Is this record a heliport?"
 },
 {
  "qid": "q67e28189f7",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Ifunda Farm Airstrip\nIdent: TZ-0068\nType: small_airport\nMunicipality: Ifunda; country: TZ; region: TZ-04; continent: AF\nLatitude: -8.06545; longitude: 35.4307\nField elevation (ft): 5744\nScheduled service: no\nIATA code: none",
  "question": "Does this airport provide scheduled service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "qe807153684",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Yahk Aerodrome\nIdent: CA-0659\nType: closed\nMunicipality: Yahk; country: CA; region: CA-BC; continent: NA\nLatitude: 49.109; longitude: -116.06\nField elevation (ft): 2870\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in South America?"
 },
 {
  "qid": "q5393959237",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Southwest Florida International Airport\nIdent: KRSW\nType: large_airport\nMunicipality: Fort Myers; country: US; region: US-FL; continent: NA\nLatitude: 26.5347; longitude: -81.7528\nField elevation (ft): 30\nScheduled service: yes\nIATA code: RSW",
  "question": "Is this airport located in North America?"
 },
 {
  "qid": "q760ed33791",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Lewis Airport\nIdent: US-9338\nType: small_airport\nMunicipality: Fleming; country: US; region: US-GA; continent: NA\nLatitude: 31.8497; longitude: -81.435\nField elevation (ft): 16\nScheduled service: no\nIATA code: none",
  "question": "Does this airport have an airline code?",
  "definitions": "- yes: The IATA code field is filled.\n- no: The IATA code field is empty."
 },
 {
  "qid": "q33c9d8a852",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Rosalia Municipal Airport\nIdent: 72S\nType: small_airport\nMunicipality: Rosalia; country: US; region: US-WA; continent: NA\nLatitude: 47.2366; longitude: -117.421\nField elevation (ft): 2169\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 2000 ft or lower.\n- no: The field elevation is above 2000 ft."
 },
 {
  "qid": "q2ebebcc0a9",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Eliporto le dune\nIdent: IT-0604\nType: heliport\nMunicipality: Ostuni; country: IT; region: IT-75; continent: EU\nLatitude: 40.7713; longitude: 17.6377\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in Europe?"
 },
 {
  "qid": "q3aeb8f59a6",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Balkhash Airport\nIdent: UAAH\nType: medium_airport\nMunicipality: Balkhash; country: KZ; region: KZ-KAR; continent: AS\nLatitude: 46.8942; longitude: 75.0045\nField elevation (ft): 1446\nScheduled service: yes\nIATA code: BXH",
  "question": "Is this airport a minor airport?",
  "definitions": "- yes: The airport type is small_airport, heliport, seaplane_base, balloonport or closed.\n- no: The airport type is large_airport or medium_airport."
 },
 {
  "qid": "qd9d01c0d30",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Pretzer Strip\nIdent: US-2940\nType: small_airport\nMunicipality: Eloy; country: US; region: US-AZ; continent: NA\nLatitude: 32.6687; longitude: -111.543\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Does this record show a field elevation?",
  "definitions": "- yes: The field elevation is given.\n- no: The field elevation is unknown."
 },
 {
  "qid": "qc23faf547b",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Serenje Airport\nIdent: FLSE\nType: small_airport\nMunicipality: Serenje; country: ZM; region: ZM-02; continent: AF\nLatitude: -13.198; longitude: 30.2398\nField elevation (ft): 4650\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation above 3000 ft?"
 },
 {
  "qid": "qdc7498111e",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Natuashish Airport\nIdent: CNH2\nType: small_airport\nMunicipality: Natuashish; country: CA; region: CA-NL; continent: NA\nLatitude: 55.9139; longitude: -61.1844\nField elevation (ft): 30\nScheduled service: yes\nIATA code: YNP",
  "question": "Is this airport in the Western Hemisphere?"
 },
 {
  "qid": "q4ad5014eca",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Noumérat - Moufdi Zakaria Airport\nIdent: DAUG\nType: medium_airport\nMunicipality: El Atteuf; country: DZ; region: DZ-47; continent: AF\nLatitude: 32.3841; longitude: 3.79411\nField elevation (ft): 1512\nScheduled service: yes\nIATA code: GHA",
  "question": "Does this airport have regular airline service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "q6f816dab92",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Bowron Lake Airport\nIdent: CA-0674\nType: closed\nMunicipality: Wells; country: CA; region: CA-BC; continent: NA\nLatitude: 53.2557; longitude: -121.42\nField elevation (ft): 3000\nScheduled service: no\nIATA code: none",
  "question": "Is this record closed?",
  "definitions": "- yes: The airport type is closed.\n- no: The airport type is large_airport, medium_airport, small_airport, heliport, seaplane_base or balloonport."
 },
 {
  "qid": "q484aa95959",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Bauhinia Downs Airport\nIdent: YBAH\nType: small_airport\nMunicipality: unknown; country: AU; region: AU-NT; continent: OC\nLatitude: -16.1333; longitude: 135.467\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Does this record name a municipality?",
  "definitions": "- yes: The municipality field is filled.\n- no: The municipality field is unknown."
 },
 {
  "qid": "q53542626dd",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Military Helipads (2x)\nIdent: IR-0088\nType: heliport\nMunicipality: unknown; country: IR; region: IR-23; continent: AS\nLatitude: 35.5293; longitude: 51.0043\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Can this airport handle scheduled flights?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "qcbaaa7f2b8",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Uzhhorod International Airport\nIdent: UKLU\nType: medium_airport\nMunicipality: Uzhhorod; country: UA; region: UA-21; continent: EU\nLatitude: 48.6343; longitude: 22.2634\nField elevation (ft): 383\nScheduled service: no\nIATA code: UDJ",
  "question": "Is this a large or medium airport in Europe?"
 },
 {
  "qid": "q0bf8eee01e",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Rhines Roost Airport\nIdent: 91TA\nType: small_airport\nMunicipality: Canton; country: US; region: US-TX; continent: NA\nLatitude: 32.446; longitude: -95.9189\nField elevation (ft): 540\nScheduled service: no\nIATA code: none",
  "question": "Does this airport have scheduled service and a field elevation above 1000 ft?"
 },
 {
  "qid": "q5fc1ab9579",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Varys Field\nIdent: CA-0524\nType: small_airport\nMunicipality: Owen Sound; country: CA; region: CA-ON; continent: NA\nLatitude: 44.5881; longitude: -80.7632\nField elevation (ft): 1200\nScheduled service: no\nIATA code: none",
  "question": "Is the field elevation above 500 ft?"
 },
 {
  "qid": "q1f3b46c965",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Muli Airport\nIdent: MV-0013\nType: small_airport\nMunicipality: Muli; country: MV; region: MV-12; continent: AS\nLatitude: 2.91139; longitude: 73.5836\nField elevation (ft): unknown\nScheduled service: no\nIATA code: MUM",
  "question": "Does this airport have an airline code?",
  "definitions": "- yes: The IATA code field is filled.\n- no: The IATA code field is empty."
 },
 {
  "qid": "q987e9e0be0",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Dhalinbuy Airport\nIdent: YDHL\nType: small_airport\nMunicipality: unknown; country: AU; region: AU-NT; continent: OC\nLatitude: -12.413; longitude: 136.387\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Does this airport have regular airline service?",
  "definitions": "- yes: The record lists scheduled service as yes.\n- no: The record lists scheduled service as no."
 },
 {
  "qid": "q15fca6d976",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Ōkaihau South Airstrip\nIdent: NZ-0067\nType: closed\nMunicipality: Ōkaihau; country: NZ; region: NZ-NTL; continent: OC\nLatitude: -35.3464; longitude: 173.736\nField elevation (ft): unknown\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in Oceania?"
 },
 {
  "qid": "qf2535b55f6",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Mabuiag Island Airport\nIdent: YMAA\nType: small_airport\nMunicipality: Mabuiag Island; country: AU; region: AU-QLD; continent: OC\nLatitude: -9.95017; longitude: 142.195\nField elevation (ft): unknown\nScheduled service: yes\nIATA code: UBB",
  "question": "Is this airport located in Oceania?"
 },
 {
  "qid": "q8d1ec07c8f",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Marshfield Emergency Heliport\nIdent: US-9044\nType: heliport\nMunicipality: Marshfield; country: US; region: US-MO; continent: NA\nLatitude: 37.3462; longitude: -92.9254\nField elevation (ft): 1475\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in North America?"
 },
 {
  "qid": "qc1916d6d92",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Šumperk Hospital Heliport\nIdent: CZ-0020\nType: heliport\nMunicipality: Šumperk; country: CZ; region: CZ-OL; continent: EU\nLatitude: 49.9576; longitude: 16.963\nField elevation (ft): 1023\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a high altitude?",
  "definitions": "- yes: The field elevation is above 1000 ft.\n- no: The field elevation is 1000 ft or lower."
 },
 {
  "qid": "q2743b5fe14",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Destilaria Veredas Airport\nIdent: BR-1161\nType: small_airport\nMunicipality: João Pinheiro; country: BR; region: BR-MG; continent: SA\nLatitude: -17.7158; longitude: -45.8174\nField elevation (ft): 2631\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located at a low altitude?",
  "definitions": "- yes: The field elevation is 3000 ft or lower.\n- no: The field elevation is above 3000 ft."
 },
 {
  "qid": "q63fb23e6f2",
  "kind": "yes/no",
  "text": "Airport record (OurAirports registry).\nName: Los Morros Airport\nIdent: SCQR\nType: small_airport\nMunicipality: Cobquecura; country: CL; region: CL-NB; continent: SA\nLatitude: -36.1226; longitude: -72.8049\nField elevation (ft): 7\nScheduled service: no\nIATA code: none",
  "question": "Is this airport located in Asia?"
 }
]
