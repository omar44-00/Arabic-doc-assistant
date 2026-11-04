import json
from pathlib import Path
import ollama

def sumarrarize_doc(link):
    link = Path(link)

    save_path = link.parent / f"{link.stem}_summaries.json"

    with open(link, "r", encoding= "utf-8") as file:
        pages = json.load(file)

    summaries = {}

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        prompt = f"""PERSONA:
    Act as a professional Arabic document analyst. Your job is to summarize documents accurately without changing their meaning.

    CONTEXT:
    You will receive all pages from one Arabic document. The document text is your only source of information.

    DOCUMENT PAGES:
    {page_text}

    TASK:
    Create a concise summary of the most important information in the complete document.

    RULES:
    1. Use only facts explicitly written in the document pages. Never add information from general knowledge.
    2. Before writing, analyze the document internally to identify its main subject, important rules, dates, numbers, conditions, deadlines, procedures, and restrictions.
    3. Preserve important names, numbers, dates, durations, percentages, and conditions exactly as written.
    4. Do not guess missing information. If an important detail is unclear because of extracted text, write: النص غير واضح في المصدر.
    5. Combine related information only when it comes from the document and does not change its meaning.
    6. Give priority to information that affects the reader's actions, rights, responsibilities, deadlines, or requirements.
    7. Do not include greetings, introductions, opinions, explanations of your reasoning, or repeated information.
    8. Write in Modern Standard Arabic and use no more than 8 concise bullet points. End every bullet with its source page number in this format:
    (المصدر: صفحة رقم X)

    OUTPUT REQUIREMENTS:
    - Start directly with: ملخص المستند:
    - Use concise bullet points only.
    - Return only the final summary.
    """

        respond = ollama.chat(
            model= "llama3.2:3b",
            messages= [{"role": "user", "content": prompt}],
            options= {
                "temperature": 0,
                "num_ctx": 8192
            }
        )

        summary = respond["message"]["content"]
        summaries[page_number] = summary

    with open(save_path, "w", encoding= "utf-8") as f:
        json.dump(summaries, f, ensure_ascii= False, indent= 4)

        print(f"Page {page_number} has been summarized and saved")

    return save_path