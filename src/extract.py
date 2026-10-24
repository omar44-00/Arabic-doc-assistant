#from langchain_community.document_loaders import PyPDFLoader -> This isn't good for arabic
import unicodedata
import pymupdf #so we used this   <-
import re

#reader = PyPDFLoader("D:/Python_projects/Arabic-doc-assistant/data/bylaw_0.pdf")
#loader = reader.load()


#for page in loader:
#    page.page_content = unicodedata.normalize("NFKC", page.page_content)

#print(loader[0].page_content[:500])

TO_WEASTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

def fix_digit(text):
    text = re.sub("[٠-٩]+", lambda m: m.group()[::-1], text)
    return text.translate(TO_WEASTERN)


pdf_path = "D:/Python_projects/Arabic-doc-assistant/data/bylaw_0.pdf"

pages = []

with pymupdf.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf, 1):
        text = page.get_text()
        #print(page_number)
        #print(text[:500])

        text = unicodedata.normalize('NFKC', text)
        text = fix_digit(text= text)
        pages.append(text)

#print(len(pages)) -> 71 and that is correct
#print(pages[:1])

all_text = "\n".join(pages)

found = re.findall(r"^\s*م\s*ا\s*د\s*ة\s*:?\s*(\d+)", all_text, flags=re.MULTILINE)

article_numbers = [int(n) for n in found]

#print(f"Article found: {article_numbers}")
#print(article_numbers[:20])

law_numbers = article_numbers[2:]
missing = [n for n in range(1, 214) if n not in law_numbers]
print(f"Missing: {missing}")