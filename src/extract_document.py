import unicodedata
import pymupdf
import json

def extract_document(link):

    SAVE_PATH = f"D:/Python_projects/Arabic-doc-assistant/data/{link.stem}_pages.json"
    pages = []

    with pymupdf.open(link) as file:
        for page_number, page in enumerate(file, 1):
            text = page.get_text()
            text = unicodedata.normalize('NFKC', text)
            pages.append({"page_number": page_number, "text": text})


    with open(SAVE_PATH, "w", encoding= "utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    print("Saved succesfully")
    return SAVE_PATH