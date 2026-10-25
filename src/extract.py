import unicodedata
import pymupdf #so we used this   <-
import re
import json

TO_WESTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
pdf_path = "D:/Python_projects/Arabic-doc-assistant/data/bylaw_0.pdf"


def fix_digit(text):
    text = re.sub("[٠-٩]+", lambda m: m.group()[::-1], text)
    return text.translate(TO_WESTERN)

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

pages = []

with pymupdf.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf, 1):
        text = page.get_text()

        text = unicodedata.normalize('NFKC', text)
        text = fix_digit(text= text)
        pages.append(text)

all_text = "\n".join(pages)


matches = list(re.finditer(r"^\s*م\s*ا\s*د\s*ة\s*:?\s*(\d+)" , all_text, flags= re.MULTILINE))
law_matches = matches[2:] 

articles = []

for i, match in enumerate(law_matches):
    start = match.start()
    if i + 1 < len(law_matches):
        end = law_matches[i + 1].start()
    else:
        end = len(all_text)

    articles.append({"number": int(match.group(1)), "text": all_text[start:end].strip()})


#print(f"Articles: {len(articles)}")

#for article in articles:
#    article["text"] = clean_text(article= article["text"])
#    if article["number"] == 213:
#        print("End of 213 article")
#        print(article["text"][-300:])
#        print(len(article["text"]))
#
#    elif article["number"] == 117:
#        print("Start of article 117")
#        print(article["text"][:300])

SIGNATURE = "صدر برياسة الجمهورية"
ARTICLES_PATH = "D:/Python_projects/Arabic-doc-assistant/data/articles.json"

for article in articles:
    if article["number"] == 213:
        position = article["text"].find(SIGNATURE)
        if position != -1:
            annex = {"number": "annex", "text": article["text"][position:].strip()}
            article["text"] = article["text"][:position].strip()
            articles.append(annex)
        break

print("Items:", len(articles))
for article in articles:
    if article["number"] == 213:
        print("New length of article 213:", len(article["text"]))

with open(ARTICLES_PATH, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

with open(ARTICLES_PATH, "r", encoding="utf-8") as f:
    loaded = json.load(f)
print("Saved and reloaded:", len(loaded))