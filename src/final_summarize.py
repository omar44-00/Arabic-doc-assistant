import json
import ollama
from pathlib import Path

def last_summary(link):
    link = Path(link)

    save_path = link.parent/ f"{link.stem}_final_summarize.json"

    with open(link, "r", encoding= "utf-8") as file:
        summary = json.load(file)

    combined_summaries = ""

    for page_number, summary_text in summary.items():
        combined_summaries += f""" 
ملخص الصفحة رقم {page_number}:
{summary_text}

---
"""
    prompt = f"""PERSONA:
Act as a professional Arabic document analyst.

CONTEXT:
You will receive summaries from all pages of one Arabic document.
The page summaries are your only source of information.

PAGE SUMMARIES:
{combined_summaries}

TASK:
Create one final summary of the complete document.

RULES:
1. Use only information explicitly written in the page summaries.
2. Select the most important rules, dates, numbers, requirements, procedures, and restrictions.
3. Preserve important names, numbers, dates, durations, percentages, and conditions.
4. Do not guess missing information.
5. Do not repeat information.
6. Do not include greetings, introductions, opinions, or explanations of your reasoning.
7. Write in Modern Standard Arabic.
8. Use as much bullets as you can as you explain everything important

OUTPUT REQUIREMENTS:
- Start directly with: ملخص المستند:
- Use bullet points only.
- Return only the final summary.
"""

    respond = ollama.chat(
            model= "llama3.2:3b",
            messages=[{"role":"user", "content": prompt}],
            options= {
                "temperature": 0,
                "num_ctx": 8192
            }
        )

    final_summary = respond["message"]["content"]

    with open(save_path, "w", encoding= "utf-8") as f:
        json.dump({"document_summary": final_summary}, f, ensure_ascii= False, indent= 4)

    return save_path