# Arabic Document Assistant

An Arabic PDF assistant built with Python and local AI models. It can extract a text-based PDF, create a detailed Arabic summary, and answer questions using only the selected document.

The project runs locally with Ollama, Chroma, Hugging Face embeddings, LangChain, and PyMuPDF. No paid API is required.

## What it can do

- Accept a local PDF path through the command line.
- Extract selectable text page by page with PyMuPDF.
- Create a whole-document Arabic summary from page summaries.
- Split pages into token-aware chunks.
- Create a separate Chroma database for each processed document.
- Answer questions in Arabic with a source page reference.
- Reject questions when the closest retrieved chunk is below the current relevance threshold.

## Current pipeline

```text
PDF path
  -> extract pages
  -> choose summary or question answering

Summary
  -> summarize each page
  -> create a final document summary

Question answering
  -> create chunks
  -> build a Chroma database
  -> retrieve the closest chunk
  -> check relevance score
  -> generate an Arabic answer
```

## Project structure

```text
Arabic-doc-assistant/
├── data/                          # Local PDFs and generated data (ignored by Git)
├── src/
│   ├── main.py                    # Command-line entry point
│   ├── extract_document.py        # PDF page extraction
│   ├── summerize_document.py      # Page-by-page summaries
│   ├── final_summarize.py         # Whole-document summary
│   ├── build_documents_chunks.py  # Chunk generation
│   ├── build_document_database.py # Per-document Chroma database
│   └── rag_document.py            # Retrieval and answer generation
├── requirements.txt
└── README.md
```

Some older files in `src/` are experiments from the first version, which focused on an Arabic university-law document.

## Requirements

- Windows
- Python 3
- [Ollama](https://ollama.com/)
- A text-based PDF with selectable text

The current local model is:

```text
llama3.2:3b
```

The embedding model is:

```text
intfloat/multilingual-e5-small
```

## Setup

```powershell
git clone https://github.com/omar44-00/Arabic-doc-assistant.git
cd Arabic-doc-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.2:3b
```

Then run:

```powershell
python src\main.py
```

Paste the full path of a PDF when prompted, then choose:

```text
1. Summarize the document
2. Ask a question about the document
```

## Generated files

For a PDF named `student_handbook.pdf`, the program generates local files such as:

```text
student_handbook_pages.json
student_handbook_pages_summaries.json
student_handbook_pages_summaries_final_summarize.json
student_handbook_pages_chunks.json
student_handbook_pages_chunks_chroma_db/
```

These are generated locally and are excluded from Git.

## Limitations

- The current extractor works with PDFs that contain selectable text. Scanned PDFs need OCR support.
- Table layouts and complex multi-column PDFs can produce imperfect extracted text.
- The `0.36` relevance threshold was tested on the student-handbook example and may need adjustment for another document collection.
- The local language model can omit or rephrase details. Check important answers against the cited source page.
- The extraction script currently saves generated files under the local `data/` folder. Update the path configuration if your project is stored elsewhere.

## Next steps

- Add OCR for scanned Arabic PDFs.
- Allow multiple questions without rebuilding the database.
- Improve citation verification and answer fidelity.
- Support more document formats, such as DOCX.
- Build a graphical interface for file selection and chat.

## Learning goals

This project is part of a practical AI-engineering learning journey. It explores PDF extraction, Arabic text handling, embeddings, vector databases, retrieval-augmented generation, local LLMs, and prompt design.
