"""Knowledge for the exam advisor (Max): shared/kb/products.json and shared/kb/texas.json.

build.py calls write() on every build, so Max always matches the catalog and the copy in tools/txcopy.py.

products.json  every product Max can recommend (id, checkout variant, license, package type, price, page)
               plus the license list with the words people use for each license (aliases).
texas.json     short fact pieces Max answers questions from: what each license is, exam facts, book rules,
               the FAQs, and the sections of each product description. Each piece carries the license
               slug (c) and group (g) it belongs to, and pre-split search words (k, kh) so the worker does
               almost no work per question.
"""
import html
import json
import os
import re

STOP = set("a an the and or of to in on for is are am be do does did i im my me we you your it its this that what "
           "which who how when where why can could would should will with from at by as about if so get need want "
           "exam test license licence texas".split())
MAX_CHARS = 900

# product types, grouped the way people ask for them
WANT_TYPES = {
    "online": ["online-course", "online-practice-exams", "study-guide-online-course"],
    "books": ["study-guide", "study-guide-flash-cards", "book-package", "highlighted-tabbed", "study-guide-nec-tabs",
              "study-guide-calculations-nec", "code-book", "super-combo", "complete-package", "rental-package"],
    "everything": ["ultimate-combo", "ultimate-rental", "the-1-package", "nec-course-package", "complete-package", "ultimate-package"],
}


# what Max leads with when someone says "help me choose": the best value complete option, in this order
BEST_VALUE = ["ultimate-combo", "complete-package", "super-combo", "highlighted-tabbed", "ultimate-package", "the-1-package", "book-package", "exam-prep-package"]


def words(text):
    return [w for w in re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).split() if len(w) > 1 and w not in STOP]


def text_of(fragment):
    t = re.sub(r"<(br|/p|/li|/h\d)[^>]*>", "\n", fragment or "", flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    return re.sub(r"\s*\n\s*", "\n", t).strip()


def cut(text, limit=MAX_CHARS):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return [text]
    out, cur = [], ""
    for s in re.split(r"(?<=[.!?])\s+", text):
        if cur and len(cur) + len(s) > limit:
            out.append(cur.strip()); cur = ""
        cur += s + " "
    if cur.strip():
        out.append(cur.strip())
    return out


def piece(h, t, c="", g=""):
    return {"h": h, "t": t, "c": c, "g": g, "kh": " ".join(sorted(set(words(h)))), "k": " ".join(sorted(set(words(h + " " + t))))}


def description_pieces(hx, cls, grp, title):
    """Split one product description into its sections (h3 headings) and keep the useful ones."""
    out = []
    parts = re.split(r"<h3[^>]*>(.*?)</h3>", hx or "", flags=re.S | re.I)
    chunks = [("About " + title, parts[0])] + [(text_of(parts[i]), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]
    for head, body in chunks:
        body = text_of(body)
        if len(body) < 60 or re.search(r"how 1 exam prep helps", head, re.I):
            continue
        for i, t in enumerate(cut(body)):
            out.append(piece(head if i == 0 else head + " (continued)", t, cls, grp))
    return out


def write(root, products, classes, order, copy, cls_mod, full, faq_general, is_old_code, cart_tag=""):
    kb = os.path.join(root, "shared", "kb")
    os.makedirs(kb, exist_ok=True)
    groups = {g: n for g, n, _ in cls_mod.GROUPS}

    # ---- products.json ----
    items = []
    for p in products:
        live = [v for v in p["variants"] if v.get("available", True)] or p["variants"]
        items.append({"id": str(p["id"]), "v": str(live[0]["id"]), "t": p["short"], "c": p["cls"], "cn": p["clsName"], "g": p["group"],
                      "ty": p["type"], "tn": p["typeName"], "r": p["rank"], "p": float(p["price"]), "y": p["year"], "rg": p["region"],
                      "u": p["path"], "i": p.get("image", ""), "cur": not is_old_code(classes[p["cls"]], p),
                      "a": any(v.get("available", True) for v in p["variants"])})
    alias = getattr(copy, "MAX_ALIASES", {})
    lic = [{"s": s, "n": classes[s]["name"], "g": classes[s]["group"], "gn": groups.get(classes[s]["group"], ""), "k": len(classes[s]["products"]),
            "lo": classes[s]["lo"], "a": alias.get(s, []) + [classes[s]["name"].lower()]} for s in order if s in classes]
    with open(os.path.join(kb, "products.json"), "w", encoding="utf-8") as f:
        json.dump({"items": items, "licenses": lic, "groups": [{"g": g, "n": n} for g, n, _ in cls_mod.GROUPS], "want": WANT_TYPES, "best": BEST_VALUE}, f, separators=(",", ":"))

    # ---- texas.json ----
    pcs = []
    for s in order:
        if s not in classes:
            continue
        c = classes[s]; g = c["group"]; n = c["name"]
        pcs.append(piece("What is the %s license?" % n, copy.SCOPE.get(s, ""), s, g))
        cf = copy.CLASS_FACTS.get(s)
        if cf:
            pcs.append(piece("%s exam: questions, time and fees" % n, " ".join(cf), s, g))
        pcs.append(piece("%s prep prices" % n, "%s exam prep runs from $%s to $%s across %d options on this site." % (n, format(c["lo"], ",.2f"), format(c["hi"], ",.2f"), len(c["products"])), s, g))
    for g, gname, blurb in cls_mod.GROUPS:
        pcs.append(piece(gname, blurb, "", g))
        pcs.append(piece("How the %s exams work" % gname.lower(), " ".join(copy.GROUP_FACTS.get(g, [])), "", g))
        pcs.append(piece("Is the exam open book? (%s)" % gname.lower(), copy.OPEN_BOOK.get(g, ""), "", g))
        pcs.append(piece("Who issues the license? (%s)" % gname.lower(), "It comes from %s." % copy.WHO_ISSUES.get(g, "the board"), "", g))
        for q, a in copy.GROUP_FAQ.get(g, []):
            pcs.append(piece("Q: " + q.replace("{name}", gname.lower()), a, "", g))
    for q, a in copy.HOME_FAQ:
        pcs.append(piece("Q: " + q, a.replace("{ful}", "1 Exam Prep")))
    for cat in faq_general.get("categories", []):
        for q, a in cat["items"]:
            pcs.append(piece("Q: " + q, a))
    seen = set()
    for p in products:
        if is_old_code(classes[p["cls"]], p):
            continue  # descriptions written for an older code year would mislead
        hx = (full.get(p["id"]) or {}).get("html", "")
        for x in description_pieces(hx, p["cls"], p["group"], p["short"]):
            key = re.sub(r"\W+", "", x["t"].lower())[:400]
            if key in seen:
                continue
            seen.add(key); pcs.append(x)
    heads, uniq = set(), []
    for x in pcs:  # the same question can be in two FAQs; keep the first
        if not x["t"].strip() or (x["h"].startswith("Q:") and x["h"].lower() in heads):
            continue
        heads.add(x["h"].lower()); uniq.append(x)
    pcs = uniq
    with open(os.path.join(kb, "texas.json"), "w", encoding="utf-8") as f:
        json.dump({"pieces": pcs}, f, separators=(",", ":"))
    return len(items), len(pcs)
