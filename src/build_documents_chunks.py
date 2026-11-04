from langchain_huggingface import HuggingFaceEmbeddings
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

def building_chunks(link):
    link = Path(link)
    MAX_WHOLE = 400

    CHUNKS_PATH = link.parent / f"{link.stem}_chunks.json"

    with open(link, "r", encoding="utf-8") as file:
        pages = json.load(file)

    embeddings = HuggingFaceEmbeddings(model_name= "intfloat/multilingual-e5-small")

    tokenizer = embeddings._client.tokenizer

    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 400,
                                                chunk_overlap= 50,
                                                length_function= lambda text: len(tokenizer.encode(text)))

    all_pages = []

    for page in pages:
        text = page["text"]

        page_number = page["page_number"]

        token_count = len(tokenizer.encode(text))

        if token_count <= MAX_WHOLE:
            parts = [text]

        else:
            parts = text_splitter.split_text(text)

        for chunk_index, part in enumerate(parts):
            all_pages.append({"page_number": page_number, "chunk_index": chunk_index, "text": part})

    #max_word_chunk = max(len(tokenizer.encode(chunk["text"])) for chunk in all_pages) to print max chunk

    with open(CHUNKS_PATH, "w", encoding= "utf-8") as f:
        json.dump(all_pages, f, ensure_ascii=False, indent=2)

    return CHUNKS_PATH
