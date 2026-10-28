"""Sort the Texas catalog into license classes and package types.

build.py imports this and works it out from each product's title and Shopify product type, so the
catalog can come from the dashboard sync or from tools/sync_shopify.py without any special fields.

To add a class: put a row in CLASSES (the first pattern that matches a title wins, so specific
rows go above general ones). To add a package type: add a row to TYPES. Run python3 build.py and
check the "unclassified" line it prints; anything listed there lands under "Other exam prep".
"""
import re

STATE = "Texas"

GROUPS = [
    ("electrical", "Texas electrician licenses", "TDLR electrical licenses, from residential wireman and journeyman to master and the sign, lineman, industrial and maintenance licenses. Every one of them has its own PSI exam."),
    ("plumbing", "Texas plumbing licenses", "Tradesman limited, journeyman and master plumber and plumbing inspector, licensed through the Texas plumbing program."),
    ("acr", "Air conditioning and refrigeration", "TDLR air conditioning and refrigeration contractor licenses, Class A and Class B, with the Environmental Air and Commercial Refrigeration endorsements, and the certified technician exam."),
    ("local", "City exams and code officials", "Texas has no statewide general contractor license, so some cities test certain trades themselves. These are the city exams and the Code Enforcement Officer exam."),
    ("business", "Licensing and business setup", "Help with the TDLR license application and with forming the Texas LLC or corporation the license goes under."),
    ("national", "ICC National Standard and NASCLA exams", "National exams for building, electrical, plumbing, gas and mechanical licenses. They are used by cities, counties and other states, so they are listed as any-state editions."),
    ("codes", "Code books, courses and practice tests", "Reference books, calculations practice and short code courses that sit beside the exam prep for any license on this site."),
]

# (slug, display name, group, regex on the title)
CLASSES = [
    # paperwork first: its titles name the license too
    ("licensing-services", "License Application and Business Setup Services", "business", r"Application (Processing|Service)|LLC Filing|Corporation or LLC"),
    # national exams before the Texas trades, since their titles name the same trades
    ("icc-general-building-contractor-a", "ICC General Building Contractor (A)", "national", r"ICC [FG]11\b"),
    ("icc-building-contractor-b", "ICC Building Contractor (B)", "national", r"ICC [FG]12\b"),
    ("icc-residential-building-contractor-c", "ICC Residential Building Contractor (C)", "national", r"ICC [FG]13\b"),
    ("nascla-commercial-general-building", "NASCLA Commercial General Building Contractor", "national", r"NASCLA Commercial General Building"),
    ("icc-master-electrician", "ICC National Standard Master Electrician", "national", r"ICC [FG]16\b"),
    ("icc-journeyman-electrician", "ICC National Standard Journeyman Electrician", "national", r"ICC [FG]17\b"),
    ("icc-residential-electrician", "ICC National Standard Residential Electrician", "national", r"ICC [FG]18\b"),
    ("nascla-electrical", "NASCLA Electrical Exams", "national", r"NASCLA (Master Unlimited Electrical|Residential Electrical|Journeyman Electrician)"),
    ("icc-master-plumber", "ICC National Standard Master Plumber", "national", r"ICC [FG]24\b"),
    ("icc-journeyman-plumber", "ICC National Standard Journeyman Plumber", "national", r"ICC [FG]25\b"),
    ("icc-master-plumber-gas", "ICC Master Plumber with Gas", "national", r"ICC [FG]27\b"),
    ("icc-journeyman-plumber-gas", "ICC Journeyman Plumber with Gas", "national", r"ICC [FG]28\b"),
    ("icc-master-mechanical", "ICC National Standard Master Mechanical", "national", r"ICC [FG]29\b"),
    ("icc-master-gas-pipe-fitter", "ICC Master Gas Pipe Fitter", "national", r"ICC [FG]33\b"),
    ("icc-journeyman-gas-pipe-fitter", "ICC Journeyman Gas Pipe Fitter", "national", r"ICC [FG]34\b"),
    # city exams and code officials
    ("code-enforcement-officer", "Code Enforcement Officer", "local", r"Code Enforcement Officer"),
    ("san-antonio-commercial-sign-operator", "San Antonio Commercial Sign Operator (974Y)", "local", r"Commercial Sign Operator"),
    ("san-antonio-billboard-operator", "San Antonio Billboard Operator (975Y)", "local", r"Billboard Operator"),
    ("san-antonio-structural-masonry", "San Antonio Structural Masonry (84CY)", "local", r"Structural Masonry"),
    ("dallas-green-construction-professional", "Dallas Commercial Green Construction Professional", "local", r"Green Construction Professional"),
    # air conditioning and refrigeration
    ("environmental-air-class-a", "ACR Contractor Class A, Environmental Air", "acr", r"Environmental Air Class A"),
    ("environmental-air-class-b", "ACR Contractor Class B, Environmental Air", "acr", r"Environmental Air Class B"),
    ("commercial-refrigeration-class-a", "ACR Contractor Class A, Commercial Refrigeration", "acr", r"Commercial Refrigeration Class A"),
    ("commercial-refrigeration-class-b", "ACR Contractor Class B, Commercial Refrigeration", "acr", r"Commercial Refrigeration Class B"),
    ("acr-certified-technician", "Certified Air Conditioning and Refrigeration Technician", "acr", r"Certified Air Conditioning"),
    # plumbing
    ("plumbing-inspector", "Plumbing Inspector", "plumbing", r"Plumbing Inspector"),
    ("tradesman-limited-plumber", "Tradesman Plumber-Limited", "plumbing", r"Tradesman Limited Plumber"),
    ("master-plumber", "Master Plumber", "plumbing", r"Master Plumber"),
    ("journeyman-plumber", "Journeyman Plumber", "plumbing", r"Journeyman Plumber"),
    # electrical: the specialty licenses first, since their titles also say journeyman
    ("journeyman-sign-electrician", "Journeyman Sign Electrician", "electrical", r"Sign Electrician"),
    ("journeyman-lineman", "Journeyman Lineman", "electrical", r"Lineman"),
    ("journeyman-industrial-electrician", "Journeyman Industrial Electrician", "electrical", r"Industrial Electrician"),
    ("maintenance-electrician", "Maintenance Electrician", "electrical", r"Maintenance Electrician"),
    ("residential-wireman", "Residential Wireman", "electrical", r"Residential Wireman"),
    ("residential-appliance-installer", "Residential Appliance Installer", "electrical", r"Residential Appliance Installer"),
    ("master-electrician-contractor", "Master Electrician and Electrical Contractor", "electrical", r"Master Electrical Contractor"),
    ("journeyman-electrician", "Journeyman Electrician", "electrical", r"Journeyman'?s? Electrician"),
    ("master-electrician", "Master Electrician", "electrical", r"Master Electrician"),
    # codes and references
    ("code-books-and-courses", "Code Books, Courses and Practice Tests", "codes", r"International (Building|Plumbing) Code|OSHA|National Electrical Code Webinar|Calculations for Electrical"),
]
OTHER = ("other", "Other Exam Prep", "codes")

# package types, lowest rank first: (slug, name, test(title, productType))
def _t(rx): return lambda t, ty: re.search(rx, t, re.I) is not None
TYPES = [
    ("online-practice-exams", "Online Practice Exams", lambda t, ty: ty in ("Online Course", "Practice Course") and re.search(r"Practice (Questions|Exam|Tests)|Code Review|Course Review", t, re.I) is not None),
    ("online-course", "Online Exam Prep Course", lambda t, ty: ty in ("Online Course", "Practice Course")),
    ("tabs", "Pre-Printed Tabs", lambda t, ty: ty == "Tabs"),
    ("study-guide-online-course", "Study Guide and Online Course", _t(r"Study Guide & Online Course")),
    ("study-guide-flash-cards", "Study Guide and Flash Cards", _t(r"Flash Card Combo")),
    ("study-guide", "Study Guide", lambda t, ty: ty in ("Book", "Plumber Package") and re.search(r"Study Guide", t, re.I) is not None and not re.search(r"Books, Tabs", t, re.I)),
    ("code-book", "Code Book", lambda t, ty: ty == "Book"),
    ("book-package", "Book Package", lambda t, ty: ty == "Book Package"),
    ("study-guide-nec-tabs", "Study Guide + NEC with Tabs", _t(r"National Electrical Code Combo with Tabs")),
    ("study-guide-calculations-nec", "Study Guide + Calculations + NEC", _t(r"Calculations Study Guides & National Electrical Code Combo")),
    ("super-combo", "Super Combo", _t(r"Super Combo")),
    ("jump-start-package", "Jump Start Package", _t(r"Jump Start")),
    ("complete-package", "Complete Package", _t(r"Complete (Journeyman|Master) Electrician|Books, Tabs & Course")),
    ("ultimate-combo", "Ultimate Combo", _t(r"Ultimate Combo")),
    ("highlighted-tabbed", "Highlighted and Tabbed Books", lambda t, ty: ty == "Book Package H/T" or re.search(r"Highlighted", t, re.I) is not None),
    ("nec-course-package", "Study Package with NEC Course", _t(r"Instructor Led NEC Course")),
    ("live-training", "Live Virtual Training", lambda t, ty: ty == "Live Training"),
    ("rental-package", "Books and Courses Rental", lambda t, ty: ty == "Book Rental"),
    ("ultimate-rental", "Ultimate Rental Package", lambda t, ty: ty == "Ultimate Package"),
    ("licensing-service", "Licensing Service", lambda t, ty: ty in ("Application", "Business Complete Package")),
    ("the-1-package", "The 1 Package (all-inclusive)", lambda t, ty: ty == "1 Package"),
    ("ultimate-package", "Ultimate Exam Prep Package", _t(r"Ultimate Exam Prep Package")),
    ("exam-prep-package", "Exam Prep Package", _t(r"Exam Prep Package")),
    ("electrician-package", "Electrician Package", _t(r"(Journeyman|Master) Electrician Package$")),
]
TYPE_RANK = {s: i for i, (s, _, _) in enumerate(TYPES)}

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def region(title):
    return "Texas" if re.search(r"\bTexas\b", title) else "Nationwide"

def classify(title, ptype):
    cls = next((c for c in CLASSES if re.search(c[3], title, re.I)), None) or OTHER
    typ = next(((s, n) for s, n, f in TYPES if f(title, ptype or "")), ("other", ptype or "Exam Prep"))
    m = re.search(r"\b(20\d\d)\b", title)
    return {"cls": cls[0], "clsName": cls[1], "group": cls[2], "type": typ[0], "typeName": typ[1], "rank": TYPE_RANK.get(typ[0], 99),
            "region": region(title), "year": m.group(1) if m else ""}

def clean_title(t):
    t = re.sub(r"\s*\(Based on (the )?\d{4} [A-Z]+\)\s*", " ", t)
    t = re.sub(r":\s*Trusted by 50k Electricians", "", t)
    return re.sub(r"\s+", " ", t).strip()

def assign(products):
    """Give every product its class, package type and a short URL slug that is unique inside its class."""
    used = {}
    out = []
    for p in sorted(products, key=lambda p: (p["title"], p["id"])):
        c = classify(p["title"], p.get("type", ""))
        base = c["type"] if c["type"] != "other" else slugify(clean_title(p["title"]))[:50].rstrip("-")
        extra = [c["year"]] if c["year"] else []
        if c["region"] not in (STATE, "Nationwide"): extra.append(slugify(c["region"]))
        if c["region"] == "Nationwide" and c["group"] in ("electrical", "plumbing"): extra.append("any-state")
        sl = "-".join([base] + extra)
        key = (c["cls"], sl); n = used.get(key, 0) + 1; used[key] = n
        if n > 1: sl = "%s-%d" % (sl, n)
        out.append(dict(p, **c, slug=sl, path="%s/%s/" % (c["cls"], sl), short=clean_title(p["title"])))
    return out

# order the licenses are listed in on the home page and in menus (the matching order above is for titles only)
DISPLAY_ORDER = ["journeyman-electrician", "master-electrician", "master-electrician-contractor", "residential-wireman", "maintenance-electrician",
                 "journeyman-sign-electrician", "journeyman-lineman", "journeyman-industrial-electrician", "residential-appliance-installer",
                 "journeyman-plumber", "master-plumber", "tradesman-limited-plumber", "plumbing-inspector",
                 "environmental-air-class-b", "environmental-air-class-a", "commercial-refrigeration-class-b", "commercial-refrigeration-class-a", "acr-certified-technician"]
