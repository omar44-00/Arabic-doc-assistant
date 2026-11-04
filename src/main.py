from pathlib import Path
import json
from extract_document import extract_document
from summerize_document import sumarrarize_doc
from final_summarize import last_summary
from build_documents_chunks import building_chunks
from build_document_database import database
from rag_document import ask_document_question

pdf_path = Path(
    input("Enter your pdf path: ").strip().strip('"')
)

if not pdf_path.exists():
    print("Pdf Not found")
    raise SystemExit

elif pdf_path.suffix.lower() != ".pdf":
    print("Please choose a pdf file")
    raise SystemExit

print(f"Your selected document is {pdf_path.name}")

pages_path = extract_document(pdf_path)
print(pages_path)

choice = input(
    "\nChoose an option:\n"
    "1. Summarize the document\n"
    "2. Ask a question about the document\n"
).strip()

if choice == "1":
    print("You selected document summarization.")
    summarize_path = sumarrarize_doc(pages_path)
    final_summary_path = last_summary(summarize_path)
    with open(final_summary_path, "r", encoding= "utf-8") as file:
        text = json.load(file)

    print(f"Here's your Summary")
    print(text["document_summary"])


elif choice == "2":
    print("You selected document question answering")
    chunks_path = building_chunks(pages_path)

    document_collection_name, document_database_path = database(chunks_path)

    question = input("What is your question? ")

    answer = ask_document_question(question, document_collection_name,
                                   document_database_path)

    print(answer)

else:
    print("Invalid choice")