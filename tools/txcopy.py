"""Copy for passyourtexascontractorexam.com: what each license covers and the facts per license group.

Edit freely, then run python3 build.py. Figures here were checked against the TDLR, TSBPE, PSI, Pearson VUE,
ICC, City of San Antonio, City of Dallas and Texas Secretary of State pages listed in SOURCES on 2026-10-28.
Re-check them when the boards change their rules. Things to watch:
  - Texas electrical exams use the 2026 NEC since September 1, 2026; products for older code years stay listed
    but their pages say so.
  - TSBPE proposed moving plumbing exams from the 2018 to the 2021 codes in July 2026; not adopted as of 2026-10-28.
"""

STATE = "Texas"

TDLR_ELEC = "https://www.tdlr.texas.gov/electricians/elecexam.htm"
TDLR_ELEC_CE = "https://www.tdlr.texas.gov/electricians/elecce.htm"
TDLR_ELEC_CONTRACTOR = "https://www.tdlr.texas.gov/electricians/apply/businesses/contractor-elec.htm"
NEC_2026 = "https://content.govdelivery.com/accounts/TXDLR/bulletins/422bc69"
PSI_ELEC = "https://test-takers.psiexams.com/api/content/bulletin/1682"
TDLR_ACR = "https://www.tdlr.texas.gov/acr/contractor-apply.htm"
TDLR_ACR_EXAM = "https://www.tdlr.texas.gov/acr/acrexam.htm"
PSI_ACR = "https://test-takers.psiexams.com/api/content/bulletin/554"
TSBPE = "https://tsbpe.texas.gov/license-types/journeyman"
TSBPE_MASTER = "https://tsbpe.texas.gov/licensing/master/"
PEARSON_TSBPE = "https://www.pearsonvue.com/us/en/tsbpe.html"
TDLR_CEO = "https://www.tdlr.texas.gov/ceo/ceoapply.htm"
PSI_CEO = "https://test-takers.psiexams.com/api/content/bulletin/5636"
ICC_SAN_ANTONIO = "https://cdn-web.iccsafe.org/wp-content/uploads/CO_TX-SanAntonio.pdf"
SA_SIGNS = "https://www.sa.gov/Directory/Departments/DSD/Contractor/Sign-Contractors-Operators"
DALLAS_GREEN = "https://dallascityhall.com/departments/sustainabledevelopment/buildinginspection/Pages/dallas_third_party.aspx"
SUNSET_TRCC = "https://www.sunset.texas.gov/reviews-and-reports/agencies/texas-residential-construction-commission"
SOS_FEES = "https://www.sos.texas.gov/corp/forms/806_boc.pdf"
ICC_EXAMS = "https://www.iccsafe.org/professional-development/certification/"
NASCLA = "https://www.nascla.org/page/AccreditedExam"

# the three links named on the home page, FAQ and blog
MAIN_SOURCES = [("TDLR electrician exams", TDLR_ELEC), ("TDLR air conditioning and refrigeration contractors", TDLR_ACR), ("Texas State Board of Plumbing Examiners", TSBPE)]

SOURCES = {
    "electrical": [("TDLR electrician exams", TDLR_ELEC), ("PSI Texas electrician candidate bulletin", PSI_ELEC), ("TDLR: 2026 NEC adopted for September 1, 2026", NEC_2026), ("TDLR electrician continuing education", TDLR_ELEC_CE)],
    "plumbing": [("Texas State Board of Plumbing Examiners", TSBPE), ("TSBPE master plumber license", TSBPE_MASTER), ("Pearson VUE: Texas plumbing exams", PEARSON_TSBPE)],
    "acr": [("TDLR air conditioning and refrigeration contractors", TDLR_ACR), ("TDLR ACR exams", TDLR_ACR_EXAM), ("PSI Texas ACR candidate bulletin", PSI_ACR)],
    "local": [("ICC: City of San Antonio exams", ICC_SAN_ANTONIO), ("San Antonio sign contractors and operators", SA_SIGNS), ("Dallas third-party green providers", DALLAS_GREEN), ("TDLR code enforcement officers", TDLR_CEO)],
    "business": [("TDLR electrical contractor license", TDLR_ELEC_CONTRACTOR), ("TDLR ACR contractor license", TDLR_ACR), ("Texas Secretary of State fee schedule (Form 806)", SOS_FEES)],
    "national": [("ICC certification exams", ICC_EXAMS), ("NASCLA accredited examinations", NASCLA), ("TDLR electrician exams", TDLR_ELEC)],
    "codes": [("TDLR: 2026 NEC adopted for September 1, 2026", NEC_2026), ("PSI Texas electrician candidate bulletin", PSI_ELEC), ("Texas State Board of Plumbing Examiners", TSBPE)],
}

# One or two plain sentences on what each license covers.
SCOPE = {
    "journeyman-electrician": "A Texas Journeyman Electrician holds the core TDLR electrical license. TDLR lets you apply and test after 7,000 hours of on-the-job training and issues the license at 8,000 hours.",
    "master-electrician": "A Texas Master Electrician can serve as the master of record for an electrical contractor. It takes 12,000 hours of on-the-job training and at least 2 years holding a journeyman license.",
    "master-electrician-contractor": "Texas has no separate Master Electrical Contractor exam. An Electrical Contractor license from TDLR needs a Master Electrician on the payroll, and the master's PSI exam is the test these packages prepare for.",
    "residential-wireman": "A Texas Residential Wireman is licensed for residential electrical work. The license needs 4,000 hours of on-the-job training under a Master Electrician or Residential Wireman, or an approved career and technology program.",
    "maintenance-electrician": "A Texas Maintenance Electrician is licensed for electrical maintenance and repair work. The license needs 8,000 hours of on-the-job training under a Master Electrician or Maintenance Electrician.",
    "journeyman-sign-electrician": "A Texas Journeyman Sign Electrician is licensed for electric sign work. The license needs 8,000 hours of on-the-job training under a Master Electrician or Master Sign Electrician.",
    "journeyman-lineman": "A Texas Journeyman Lineman works on overhead and underground power lines for utilities, co-ops, municipal utilities and electrical contractors. The license needs 7,000 apprenticeship hours or 3.5 years as a lineman in Texas.",
    "journeyman-industrial-electrician": "A Texas Journeyman Industrial Electrician is licensed for industrial electrical work; time on this license does not count toward a master license. The license needs 8,000 hours as a licensed apprentice under a Texas Master Electrician.",
    "residential-appliance-installer": "A Texas Residential Appliance Installer is licensed to install residential appliances. No experience is needed to apply, only the PSI exam, and the license needs no continuing education.",
    "journeyman-plumber": "A Texas Journeyman Plumber is licensed for plumbing work. The Texas State Board of Plumbing Examiners requires 8,000 hours in the trade and a 48-hour approved course.",
    "master-plumber": "A Texas Master Plumber holds the top plumbing license. Since September 1, 2025 it takes 2 years as a licensed journeyman, or 1 year plus an approved apprenticeship.",
    "tradesman-limited-plumber": "The Texas Tradesman Plumber-Limited license is the first plumbing license above apprentice. It needs 4,000 hours in the trade and a 24-hour approved course.",
    "plumbing-inspector": "A Texas Plumbing Inspector inspects plumbing for a city or other political subdivision. The license needs 500 hours of plumbing training and experience plus a high school diploma or GED, or a qualifying plumbing license.",
    "environmental-air-class-a": "The Environmental Air Conditioning endorsement on a Class A contractor license covers comfort heating and cooling systems of any size. Class A has no tonnage limit and needs 48 months of practical experience.",
    "environmental-air-class-b": "The Environmental Air Conditioning endorsement on a Class B contractor license covers comfort systems of 25 tons cooling and 1.5 million BTU per hour heating or less. It needs 48 months of practical experience.",
    "commercial-refrigeration-class-a": "The Commercial Refrigeration endorsement on a Class A contractor license covers commercial refrigeration work with no size limit, and needs the same 48 months of practical experience.",
    "commercial-refrigeration-class-b": "The Commercial Refrigeration endorsement on a Class B contractor license covers refrigeration systems of 25 tons and under, the same size limit as a Class B comfort license.",
    "acr-certified-technician": "The TDLR Certified Technician is the step above a registered technician. It needs 24 months of experience under a licensed contractor, or a 2,000-hour approved program, plus the PSI exam.",
    "code-enforcement-officer": "Texas code enforcement officers register with TDLR. The path is the one-week TEEX Basic Code Enforcement course, a closed-book PSI exam, and a year of full-time code enforcement experience for full registration.",
    "san-antonio-commercial-sign-operator": "San Antonio requires an on-premises sign operator to pass an approved ICC exam, post a $45,000 bond and pay a $100 yearly fee. ICC lists the exam as 974, Texas (San Antonio) Commercial Sign Operator.",
    "san-antonio-billboard-operator": "San Antonio requires an off-premises (billboard) sign operator to pass an approved ICC exam, post a $45,000 bond and pay a $375 yearly fee. ICC lists the exam as 975, Texas (San Antonio) Billboard Operator.",
    "san-antonio-structural-masonry": "The San Antonio Structural Masonry Code Module book package has the references for the ICC structural masonry module sold under that name. Confirm the exam number with ICC or the city before ordering, since we could not find it in a current bulletin.",
    "dallas-green-construction-professional": "Dallas lets third-party Commercial Green Providers review and inspect green building work. A provider needs the ICC Commercial Green Construction Professional (GCP) certification or another listed one, plus City of Dallas training.",
    "licensing-services": "Licensing services handle the paperwork: the TDLR license application and the Texas Secretary of State filing for the LLC or corporation, which costs $300 in state fees for a certificate of formation.",
    "icc-general-building-contractor-a": "The ICC National Standard General Building Contractor (A) exam is used by cities, counties and other states for commercial general contractor licenses. Texas has no state general contractor license, so check whether your city asks for it.",
    "icc-building-contractor-b": "The ICC National Standard Building Contractor (B) exam covers buildings up to three stories. Cities, counties and some states use it for contractor registration, and Texas has no state version.",
    "icc-residential-building-contractor-c": "The ICC National Standard Residential Building Contractor (C) exam covers one- and two-family homes and townhouses. San Antonio accepts an ICC residential certification for its residential contractor registration.",
    "nascla-commercial-general-building": "The NASCLA Commercial General Building exam is a national contractor exam accepted by a group of states, so one pass can count in more than one place. Texas itself has no state general contractor exam.",
    "icc-master-electrician": "The ICC National Standard Master Electrician exam is used by cities, counties and states outside the TDLR system. A Texas master electrician license comes from TDLR and its PSI exam instead.",
    "icc-journeyman-electrician": "The ICC National Standard Journeyman Electrician exam is used outside the TDLR system. Electricians licensed in Texas take the TDLR exam through PSI.",
    "icc-residential-electrician": "The ICC National Standard Residential Electrician exam is used by jurisdictions outside Texas. In Texas the matching license is the TDLR Residential Wireman.",
    "nascla-electrical": "The NASCLA electrical exams are national exams accepted by a group of states for journeyman, residential and master unlimited electrical contractor licenses. Texas licenses electricians through TDLR instead.",
    "icc-master-plumber": "The ICC National Standard Master Plumber exam is used by cities, counties and states that test plumbers through ICC. Texas plumbers test through TSBPE and Pearson VUE.",
    "icc-journeyman-plumber": "The ICC National Standard Journeyman Plumber exam is used outside Texas. Texas journeymen take the TSBPE written and practical exams.",
    "icc-master-plumber-gas": "The ICC Master Plumber with Gas exam adds fuel gas piping to the master plumber exam, for jurisdictions that license both together.",
    "icc-journeyman-plumber-gas": "The ICC Journeyman Plumber with Gas exam adds fuel gas piping to the journeyman plumber exam, for jurisdictions that license both together.",
    "icc-master-mechanical": "The ICC National Standard Master Mechanical exam covers heating, ventilation and air conditioning for jurisdictions that license mechanical contractors through ICC.",
    "icc-master-gas-pipe-fitter": "The ICC Master Gas Pipe Fitter exam covers fuel gas piping for jurisdictions that license gas fitters through ICC.",
    "icc-journeyman-gas-pipe-fitter": "The ICC Journeyman Gas Pipe Fitter exam covers fuel gas piping work for jurisdictions that license journeyman gas fitters through ICC.",
    "code-books-and-courses": "Code books and short courses cover the National Electrical Code, the International Building and Plumbing Codes, electrical calculations and OSHA construction rules.",
    "other": "Other exam prep collects products that do not fit a single license.",
}

# extra facts for one license, shown before the group facts. Keep each one a plain sentence with a number in it.
CLASS_FACTS = {
    "journeyman-electrician": ["The PSI exam has two portions: 59 NEC knowledge items in 130 minutes and 26 calculation items in 110 minutes.", "The exam fee is $78 for both portions and the TDLR application fee is $30."],
    "master-electrician": ["The PSI exam has two portions: 75 NEC knowledge items in 150 minutes and 33 calculation items in 170 minutes.", "The exam fee is $78 for both portions and the TDLR application fee is $45."],
    "master-electrician-contractor": ["The Electrical Contractor license costs $110 a year and needs liability insurance of $300,000 per occurrence and $600,000 aggregate.", "There is no business or law exam for a Texas electrical contractor; the master electrician's PSI exam is the test."],
    "residential-wireman": ["The PSI exam has 80 scored items in 240 minutes and costs $64.", "The TDLR application fee is $20."],
    "maintenance-electrician": ["The PSI exam has 60 scored items in 180 minutes and costs $64.", "The TDLR application fee is $20."],
    "journeyman-sign-electrician": ["The PSI exam has 80 scored items in 240 minutes and costs $64.", "The TDLR application fee is $30."],
    "journeyman-lineman": ["The PSI exam has 40 scored items in 120 minutes and costs $61.", "The TDLR application fee is $30."],
    "journeyman-industrial-electrician": ["The PSI exam has 60 scored items in 180 minutes and costs $64.", "The TDLR application fee is $30."],
    "residential-appliance-installer": ["The PSI exam has 80 scored items in 240 minutes and costs $64.", "The license needs no continuing education, and the TDLR application fee is $30."],
    "journeyman-plumber": ["The written exam has 100 items in 120 minutes and costs $68.50 at Pearson VUE; the practical has 6 items in 240 minutes.", "TSBPE charges $40 to apply for the exam and $40 for the license."],
    "master-plumber": ["The master exam is written only, 360 minutes plus a 30-minute break, and costs $128.50 at Pearson VUE.", "TSBPE charges a $25 processing fee and $75 for the license."],
    "tradesman-limited-plumber": ["The written exam has 85 items in 120 minutes and costs $68.50; the practical has 6 items in 240 minutes.", "TSBPE charges $36 to apply for the exam and $35 for the license."],
    "plumbing-inspector": ["The exam fee, the license fee and the renewal fee are each $55.", "Pearson VUE lists the computer-based plumbing inspector exam as coming soon, so check with TSBPE how it is given now."],
    "environmental-air-class-a": ["The PSI exam has 120 items in 230 minutes and costs $74.", "References include the 2024 IMC, UMC and IFGC, ACCA Manuals J, D and S, and Modern Refrigeration and Air Conditioning, 22nd edition."],
    "environmental-air-class-b": ["The PSI exam has 100 items in 170 minutes and costs $60.", "References include the 2024 IMC, UMC and IFGC, ACCA Manuals J, D and S, and Modern Refrigeration and Air Conditioning, 22nd edition."],
    "commercial-refrigeration-class-a": ["The PSI exam has 120 items in 230 minutes and costs $74.", "Class A insurance minimums are $300,000 per occurrence and $600,000 aggregate."],
    "commercial-refrigeration-class-b": ["The PSI exam has 100 items in 170 minutes and costs $60.", "Class B insurance minimums are $100,000 per occurrence and $200,000 aggregate."],
    "acr-certified-technician": ["The PSI exam has 60 scored items in 112 minutes and costs $60.", "The TDLR application fee is $50 and the applicant must be at least 18."],
    "code-enforcement-officer": ["The PSI exam has 70 scored items in 105 minutes, costs $50 and is closed book.", "Registration costs $100 and lasts 2 years, with 12 hours of continuing education before each renewal."],
    "san-antonio-commercial-sign-operator": ["ICC exam 974 has 70 questions in 3 hours, is open book and costs $115.", "It is written to the City of San Antonio sign code, Chapter 28."],
    "san-antonio-billboard-operator": ["ICC exam 975 has 70 questions in 3 hours, is open book and costs $115.", "It is written to the San Antonio sign code and billboard ordinance, plus Chapter 10 building-related codes."],
}

OFFICIAL_SCOPE = "The {name} exam is used by Texas cities and code officials."

# facts per group, used in the "How does the exam work" section and the FAQ
GROUP_FACTS = {
    "electrical": [
        "TDLR licenses Texas electricians, and PSI gives every exam with a 70 percent passing score on each portion.",
        "Since September 1, 2026, the exams are written to the 2026 National Electrical Code, the edition Texas adopted on July 28, 2026.",
        "The exams are open book: bring a soft-bound NEC, highlighted and noted before the exam, with only the publisher's permanent index tabs. Homemade and other tabs are not allowed.",
        "Licenses renew every year with 4 hours of continuing education covering the NEC, Texas electrician law and rules, and NFPA 70E.",
    ],
    "plumbing": [
        "The Texas State Board of Plumbing Examiners (TSBPE) licenses plumbers, not TDLR, and Pearson VUE gives the computer exams.",
        "The written exams are closed book: no books, papers or references are allowed in the room, so what you study is what you have.",
        "Journeyman and tradesman candidates also take a hands-on practical, held only in Austin and Waco.",
        "The current handbook points to the 2018 IPC with the 2018 IFGC, or the 2018 UPC; a move to the 2021 codes was proposed in July 2026.",
    ],
    "acr": [
        "TDLR licenses air conditioning and refrigeration contractors in two classes: Class B up to 25 tons cooling and 1.5 million BTU per hour heating, and Class A with no limit.",
        "A contractor needs 48 months of practical experience in the last 72 months, and the application fee is $115.",
        "PSI gives the exams, and they are open book; since September 1, 2026 they reference the 2024 IMC, UMC and IFGC.",
        "Contractors complete 8 hours of continuing education each year, including 1 hour of Texas law and rules.",
    ],
    "local": [
        "Texas does not license general contractors at the state level; the Texas Residential Construction Commission was abolished in 2009.",
        "Cities set their own registration rules, and some, such as San Antonio, require an ICC exam for certain trades.",
        "San Antonio sign operators need a passing ICC exam, a $45,000 bond and $1,000,000 in general liability insurance.",
        "Texas code enforcement officers register with TDLR after the TEEX course and a closed-book PSI exam that costs $50.",
    ],
    "business": [
        "A Texas LLC or corporation is formed with a certificate of formation at the Secretary of State, which costs $300.",
        "An Electrical Contractor license costs $110 and needs a Master Electrician plus $300,000 per occurrence liability insurance.",
        "An ACR contractor license costs $115, with insurance of $300,000 per occurrence for Class A and $100,000 for Class B.",
        "Neither license has a business and law exam in Texas; the trade exam is the only test.",
    ],
    "national": [
        "ICC National Standard and NASCLA exams are national exams, used by cities, counties and other states that do not write their own.",
        "Texas licenses electricians and air conditioning contractors through TDLR and plumbers through TSBPE, so these exams are mainly for work outside the state system.",
        "ICC exams are open book for most categories, and the ICC bulletin for the exam lists the references allowed.",
        "Check with the city or state that issues your license which exam and code edition it accepts before you order.",
    ],
    "codes": [
        "Texas electrical exams have used the 2026 NEC since September 1, 2026, so buy the 2026 edition for a Texas electrical exam.",
        "PSI allows the publisher's permanent index tabs in the NEC, plus highlighting and notes made before the exam.",
        "Texas plumbing exams are closed book, so plumbing code books are for studying, not for the exam room.",
        "Books ship from the fulfillment center; online courses arrive by email after purchase.",
    ],
}
GROUP_HOW = {
    "electrical": "The {name} exam is a TDLR license exam given by PSI. TDLR approves your application first, then you schedule with PSI and have one year from the application date to pass.",
    "plumbing": "The {name} license comes from the Texas State Board of Plumbing Examiners. You apply to TSBPE, then take the written exam at Pearson VUE and, where required, the practical in Austin or Waco.",
    "acr": "The {name} exam is a TDLR license exam given by PSI. You apply to TDLR with proof of experience, then schedule the open-book exam with PSI.",
    "local": "The {name} exam is set by a Texas city or by TDLR rather than by a statewide contractor board. The city or agency approves you, then the exam is scheduled with ICC or PSI.",
    "business": "The {name} help covers the paperwork side of a Texas license, which every new contracting business goes through whatever its trade.",
    "national": "The {name} exam is a national exam. It is listed here for jurisdictions that use it; Texas state trade licenses have their own exams.",
    "codes": "The {name} items are references and short courses that sit beside the exam prep for any license on this site.",
}

OPEN_BOOK = {
    "electrical": "Yes. Texas electrician exams are open book with your own soft-bound 2026 NEC. Highlighting, underlining and notes made before the exam are fine, but only the publisher's permanent index tabs are allowed; homemade and other tabs are not.",
    "plumbing": "No. The Texas plumbing written exams are closed book. Pearson VUE does not allow books, papers or reference material in the room, so the study guide and practice exams are how you prepare.",
    "acr": "Yes. The PSI exams for Texas air conditioning and refrigeration licenses are open book, with the code books and references listed in the PSI bulletin.",
    "local": "It depends on the exam. The San Antonio ICC sign exams are open book, while the Texas Code Enforcement Officer exam is closed book. The bulletin for your exam has the rule.",
    "business": "There is no exam for the paperwork itself. The trade exam that goes with the license has its own rule: open book for electrical and A/C, closed book for plumbing.",
    "national": "ICC and NASCLA exams are open book for most categories. The bulletin for your exam lists the references allowed and the editions.",
    "codes": "Texas electrical and A/C exams are open book, and plumbing exams are closed book. Code books here are for the open-book exams and for studying.",
}
WHO_ISSUES = {
    "electrical": "the Texas Department of Licensing and Regulation (TDLR)",
    "plumbing": "the Texas State Board of Plumbing Examiners (TSBPE)",
    "acr": "the Texas Department of Licensing and Regulation (TDLR)",
    "local": "the city that requires it, or TDLR for code enforcement officers",
    "business": "TDLR for the trade license and the Texas Secretary of State for the business entity",
    "national": "the city, county or state that uses the exam",
    "codes": "the board for the license you are testing for",
}
# two extra FAQ entries per group: (question template with {name}, answer)
GROUP_FAQ = {
    "electrical": [("What does the {name} exam cost?", "PSI charges $78 for the journeyman and master exams, $61 for journeyman lineman and $64 for the other electrician exams, paid to PSI after TDLR approves your application."),
                   ("Do I need the 2023 or the 2026 NEC?", "The 2026 NEC. Texas adopted it on July 28, 2026, and PSI exams have been written to it since September 1, 2026. Packages built on the 2023 NEC are still listed for anyone finishing up, but the 2026 editions match the current exam.")],
    "plumbing": [("Is there a practical exam?", "Yes, for journeyman and tradesman candidates. The practical is held only at the TSBPE testing centers in Austin and Waco. A tradesman moving up to journeyman takes the written exam only."),
                 ("How long do I wait to retake a failed exam?", "Pearson VUE lists 30 days after a first failure, 60 days after a second and 90 days after each later one.")],
    "acr": [("What is the difference between Class A and Class B?", "Class B covers cooling systems of 25 tons and under and heating systems of 1.5 million BTU per hour and under. Class A has no size limit and a longer exam: 120 items in 230 minutes for $74, against 100 items in 170 minutes for $60."),
            ("Which books are allowed in the A/C exam?", "The PSI bulletin lists the 2024 IMC, UMC and IFGC, ACCA Manuals J, D and S for Environmental Air, Modern Refrigeration and Air Conditioning (22nd edition) and the ADI Duct Size Calculator, plus the Texas ACR law and rules.")],
    "local": [("Does Texas have a state general contractor license?", "No. Texas has no statewide general contractor license, and the residential construction commission that registered builders was abolished in 2009. Cities such as San Antonio and Dallas set their own registration rules."),
              ("What does a San Antonio sign operator need besides the exam?", "A $45,000 bond, a yearly city fee of $100 for on-premises signs or $375 for billboards, $500,000 in workers' compensation and employer's liability and $1,000,000 in general liability insurance.")],
    "business": [("How much does it cost to form a Texas LLC?", "The Texas Secretary of State charges $300 to file a certificate of formation for an LLC or a for-profit corporation. Our service fee is separate and shown at checkout."),
                 ("What does a Texas electrical contractor license need?", "A Master Electrician on staff, who can also be the owner, liability insurance of $300,000 per occurrence and $600,000 aggregate, workers' compensation or a filed election, and a $110 TDLR fee.")],
    "national": [("Can I use an ICC or NASCLA exam for a Texas state license?", "Not for the TDLR electrician or A/C licenses or the TSBPE plumbing licenses, which have their own exams. These national exams are for cities, counties and other states that accept them."),
                 ("Which code edition is the exam on?", "Each ICC and NASCLA bulletin names the edition. Check it before ordering, since jurisdictions adopt new codes on their own schedules.")],
    "codes": [("Which edition of a code book should I buy?", "The edition named in the candidate bulletin for your exam. For Texas electrical exams that is the 2026 NEC since September 1, 2026."),
              ("Can I bring a tabbed NEC into a Texas electrical exam?", "Only with the publisher's permanent index tabs. PSI does not allow homemade or other tabs, and nothing may be added or marked during the exam.")],
}

# what each package type is, in one line
TYPE_BLURB = {
    "online-practice-exams": "timed practice questions online, with explanations",
    "online-course": "an online course with practice exams you can take on a phone or laptop",
    "tabs": "pre-printed tabs for the reference books",
    "study-guide-online-course": "the study guide plus the online course",
    "study-guide-flash-cards": "the study guide with practice exams plus flash cards",
    "study-guide": "the printed study guide with practice exams",
    "code-book": "the printed code book",
    "book-package": "the reference books the exam is written to, new and unmarked",
    "study-guide-nec-tabs": "the study guide, the National Electrical Code and tabs",
    "study-guide-calculations-nec": "the study guide, the calculations guide and the National Electrical Code",
    "super-combo": "study guide, calculations guide, flash cards, the NEC and tabs",
    "jump-start-package": "a starter set of books and online practice",
    "complete-package": "the books, tabs and course together",
    "electrician-package": "the books and online practice for an earlier code cycle",
    "ultimate-combo": "the full study set plus the online test kit",
    "highlighted-tabbed": "the reference books already highlighted and tabbed",
    "nec-course-package": "the study package plus an instructor-led NEC course",
    "live-training": "live virtual classes with an instructor plus self-study material",
    "rental-package": "the reference books on rental plus the online course, returned after your exam",
    "ultimate-rental": "highlighted and tabbed rental books, the online course and live training",
    "licensing-service": "help preparing and filing the license application or business setup",
    "the-1-package": "everything: exam prep, books, licensing paperwork and business setup",
    "ultimate-package": "the complete exam prep package",
    "exam-prep-package": "an exam prep package",
    "other": "exam prep",
}

# home page
HOME_H1 = "Texas contractor exam prep for every license"
HOME_LEAD = ("Exam prep for {n} Texas licenses: TDLR electrician licenses from residential wireman to master, plumbing licenses, "
             "air conditioning and refrigeration contractor exams, and the city exams Texas leaves to local government. "
             "Pick your license to compare its packages, then check out in one click.")
HOME_TITLE = "Texas Contractor Exam Prep for Every License"
HOME_DESC = "Texas exam prep for {n} licenses: TDLR electrician and A/C contractor exams, TSBPE plumbing, and San Antonio and Dallas city exams. Books, courses and The 1 Package."
HOME_TAKEAWAYS = [
    "Texas electrical exams have used the 2026 NEC since September 1, 2026; journeyman and master exams cost $78 at PSI.",
    "Electrical and A/C exams are open book; Texas plumbing exams are closed book with a hands-on practical.",
    "Texas has no state general contractor license, so trade licenses and city registrations are what you test for.",
]
HOME_SEARCH_PLACEHOLDER = "Try journeyman, residential wireman or Class B"
LICENSES_COVERED = "Texas licenses covered"
# the table on the home page: (heading, sub, header row, rows, note)
HOME_TABLE = {
    "h2": "Which Texas license needs which exam?",
    "sub": "Texas splits trade licensing between TDLR and the plumbing board, and leaves general contracting to the cities. Here is who tests what.",
    "head": ["License", "Experience", "Exam", "Book rules"],
    "rows": [
        ["Journeyman Electrician (TDLR)", "8,000 hours (test at 7,000)", "PSI, 2 portions, $78", "Open book, 2026 NEC"],
        ["Master Electrician (TDLR)", "12,000 hours and 2 years as journeyman", "PSI, 2 portions, $78", "Open book, 2026 NEC"],
        ["Residential Wireman (TDLR)", "4,000 hours", "PSI, 80 items, $64", "Open book, 2026 NEC"],
        ["ACR Contractor Class B (TDLR)", "48 months in the last 72", "PSI, 100 items, $60", "Open book, 2024 IMC, UMC, IFGC"],
        ["ACR Contractor Class A (TDLR)", "48 months in the last 72", "PSI, 120 items, $74", "Open book, 2024 IMC, UMC, IFGC"],
        ["Journeyman Plumber (TSBPE)", "8,000 hours and a 48-hour course", "Pearson VUE, 100 items, $68.50, plus practical", "Closed book"],
        ["Master Plumber (TSBPE)", "2 years as journeyman", "Pearson VUE, written, $128.50", "Closed book"],
    ],
    "hot": 1,
    "note": "Figures from TDLR, TSBPE, PSI and Pearson VUE, checked October 28, 2026. Confirm with the board before you apply, since fees and rules change.",
}
HOME_FAQ = [
    ("Which Texas license do I need?", "The right license depends on your trade. Electricians are licensed by TDLR, from residential wireman to master; air conditioning and refrigeration contractors by TDLR in Class A or B; plumbers by the Texas State Board of Plumbing Examiners. General contractors have no state license, but some cities register them."),
    ("Are the Texas exams open book?", "Electrical and air conditioning exams are open book. Electricians bring a soft-bound 2026 NEC with only the publisher's permanent tabs. Plumbing written exams are closed book, with no references allowed in the room."),
    ("Which NEC edition is the Texas electrical exam on?", "The 2026 NEC. Texas adopted it on July 28, 2026 and PSI exams switched on September 1, 2026. Packages built on the 2023 NEC stay listed, marked with their code year."),
    ("What do the exams cost?", "PSI charges $78 for the journeyman and master electrician exams, $60 to $74 for the A/C contractor exams and $64 for most other electrician exams. Plumbing written exams are $68.50 at Pearson VUE, or $128.50 for master. Board application fees are separate."),
    ("Are these the real exam questions?", "No. Licensing exam questions are confidential. The courses and practice exams here are original material written to the same subjects and format, with explanations."),
    ("Does buying a package register me for the exam?", "No. TDLR or TSBPE approves your application first, then PSI or Pearson VUE schedules the exam. A package gets you ready for the test itself."),
    ("How do orders arrive?", "Books ship from our fulfillment center, {ful}; online courses and practice exams arrive by email after purchase. Rental books go back after your exam."),
    ("What is The 1 Package?", "The 1 Package is the all-inclusive option for a Texas electrical license: the exam prep, the reference books, help with the TDLR application and the business setup, in one order."),
]
GENERAL_FAQ_LEAD = "{n} answers about Texas electrician, plumbing, air conditioning and city exams: which board licenses what, the 2026 NEC switch, exam fees, open and closed book rules, studying and ordering. Each of the {k} license pages adds questions of its own."
FAQ_TAKEAWAYS = [
    "TDLR licenses electricians and A/C contractors; TSBPE licenses plumbers; cities handle general contractors.",
    "Electrician exams cost $61 to $78 at PSI and use the 2026 NEC since September 1, 2026.",
    "Electrical and A/C exams are open book; plumbing written exams are closed book.",
]
BLOG_FAQ = [
    ("How long should I study for a Texas electrician exam?", "Most candidates do well with six to eight weeks at about 90 minutes a day, split between finding answers fast in the 2026 NEC, the calculations, and full-length timed practice exams. The journeyman exam alone runs 240 minutes across two portions."),
    ("Is the exam open book, and which books do I bring?", "Texas electrical and A/C exams are open book; bring the editions named in the PSI bulletin. Texas plumbing exams are closed book. For the NEC, only the publisher's permanent tabs are allowed."),
    ("Does Texas have a general contractor license?", "No. Texas licenses trades, not general contractors. Some cities, such as San Antonio and Dallas, have their own registration and may ask for an ICC exam."),
    ("Are the practice questions the real exam questions?", "No. Licensing exam questions are confidential. Our courses and practice exams are original material written to the same subjects and format."),
    ("Does buying a package register me for the exam?", "No. TDLR or TSBPE approves you first, then PSI or Pearson VUE schedules the exam."),
    ("How do orders arrive?", "Books ship from our fulfillment center, {ful}; online courses arrive by email after purchase."),
]
FAQ_GROUP_INTRO = {"contractor": "Texas licensing", "trades": "Trade licenses"}
LLM_SUMMARY = "Exam prep for {n} Texas licenses: TDLR electrician licenses (journeyman, master, residential wireman, maintenance, sign, lineman, industrial, residential appliance installer), TSBPE plumbing licenses, TDLR air conditioning and refrigeration contractor and technician exams, San Antonio and Dallas city exams, the TDLR code enforcement officer exam, and ICC and NASCLA national exams."
LLM_FACTS = [
    "- Texas electricians are licensed by TDLR and tested by PSI. Exams have used the 2026 NEC since September 1, 2026. Journeyman and master exams are 2 portions for $78; most other electrician exams are $64.",
    "- Journeyman electrician: 8,000 hours (may test at 7,000). Master: 12,000 hours and 2 years as journeyman. Residential wireman: 4,000 hours. Electricians renew yearly with 4 hours of CE.",
    "- Electrical exams are open book with a soft-bound NEC; only the publisher's permanent index tabs are allowed.",
    "- Plumbers are licensed by the Texas State Board of Plumbing Examiners and tested by Pearson VUE. Written exams are closed book; journeyman and tradesman candidates also take a practical in Austin or Waco.",
    "- ACR contractors (TDLR): Class B up to 25 tons cooling and 1.5 million BTU/hr heating, Class A no limit; 48 months experience; PSI exams $60 (B) and $74 (A), open book, 2024 IMC/UMC/IFGC.",
    "- Texas has no state general contractor license. Cities such as San Antonio and Dallas set their own rules.",
]
BLOG_LEAD = "Study plans, Texas licensing rules and exam strategy for electrician, plumbing, air conditioning and city exams, written for people who work full days and study at night. Each post links to the license it covers, and every rule we quote, from the 2026 NEC switch to the PSI tab rules, links to the board that sets it."

# short labels for the Quick facts box on license pages
ISSUER_SHORT = {"electrical": "TDLR, exams by PSI", "plumbing": "TSBPE, exams by Pearson VUE", "acr": "TDLR, exams by PSI", "local": "The city, or TDLR", "business": "TDLR and the Secretary of State", "national": "ICC or NASCLA", "codes": "Depends on the license"}
BOOK_SHORT = {"electrical": "Open book, 2026 NEC", "plumbing": "Closed book", "acr": "Open book, 2024 IMC, UMC, IFGC", "local": "Depends on the exam", "business": "No exam for the paperwork", "national": "Open book, most categories", "codes": "Open book for electrical and A/C"}
# the line across the top of every page in designs that show it
PROMO = "Texas electrical exams use the 2026 NEC since September 1, 2026"
# product pages pictured in the home page collage (license/package paths)
COLLAGE = ["journeyman-electrician/ultimate-combo-2026/", "master-electrician/super-combo-2026/", "journeyman-plumber/complete-package-2026/", "residential-wireman/highlighted-tabbed/"]

# the words people use for each license, so the exam advisor (Max) can tell which one they mean
MAX_ALIASES = {
    "journeyman-electrician": ["journeyman electrician", "journeyman electric", "jman electrician", "electrical journeyman"],
    "master-electrician": ["master electrician", "electrical master", "master electric"],
    "master-electrician-contractor": ["electrical contractor", "master electrical contractor", "ec license", "contractor license electric"],
    "residential-wireman": ["residential wireman", "wireman", "residential electrician", "residential electric"],
    "maintenance-electrician": ["maintenance electrician", "maintenance electric"],
    "journeyman-sign-electrician": ["sign electrician", "journeyman sign", "neon"],
    "journeyman-lineman": ["lineman", "linemen", "line worker", "power line"],
    "journeyman-industrial-electrician": ["industrial electrician", "journeyman industrial", "refinery electrician", "plant electrician"],
    "residential-appliance-installer": ["appliance installer", "residential appliance", "water heater install"],
    "journeyman-plumber": ["journeyman plumber", "journeyman plumbing", "plumber journeyman"],
    "master-plumber": ["master plumber", "master plumbing", "rmp"],
    "tradesman-limited-plumber": ["tradesman plumber", "tradesman limited", "plumber limited", "tradesman"],
    "plumbing-inspector": ["plumbing inspector"],
    "environmental-air-class-a": ["class a hvac", "hvac class a", "ac class a", "a/c class a", "environmental air a", "class a environmental"],
    "environmental-air-class-b": ["class b hvac", "hvac class b", "ac class b", "a/c class b", "environmental air b", "class b environmental", "hvac license", "ac license"],
    "commercial-refrigeration-class-a": ["refrigeration class a", "class a refrigeration", "commercial refrigeration a"],
    "commercial-refrigeration-class-b": ["refrigeration class b", "class b refrigeration", "commercial refrigeration b", "refrigeration license"],
    "acr-certified-technician": ["certified technician", "hvac technician", "ac technician", "acr technician", "hvac tech", "ac tech"],
    "code-enforcement-officer": ["code enforcement", "code officer", "ceo"],
    "san-antonio-commercial-sign-operator": ["sign operator", "974", "on premises sign", "commercial sign"],
    "san-antonio-billboard-operator": ["billboard", "975", "off premises sign"],
    "san-antonio-structural-masonry": ["masonry", "84cy", "structural masonry"],
    "dallas-green-construction-professional": ["green construction", "gcp", "green building", "dallas green"],
    "licensing-services": ["llc", "application help", "business setup", "form a company", "corporation", "apply for my license"],
    "icc-general-building-contractor-a": ["general contractor", "general building", "building contractor a", "f11", "g11"],
    "icc-building-contractor-b": ["building contractor b", "f12", "g12"],
    "icc-residential-building-contractor-c": ["residential contractor", "home builder", "residential building", "f13", "g13"],
    "nascla-commercial-general-building": ["nascla", "commercial general"],
    "nascla-electrical": ["nascla electrical", "nascla journeyman", "nascla master"],
    "code-books-and-courses": ["code book", "osha", "nec webinar", "ibc", "ipc", "calculations book"],
}
