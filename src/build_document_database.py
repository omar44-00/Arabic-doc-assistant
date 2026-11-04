from langchain_chroma import Chroma
import json
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

def database(chunks):

    chunks = Path(chunks)

    collection_name = f"document_{chunks.stem}"
    persist_directory = chunks.parent / f"{chunks.stem}_chroma_db"

    with open(chunks, "r", encoding= "utf-8") as file:
        all_pages = json.load(file)

    embeddings = HuggingFaceEmbeddings(model_name= "intfloat/multilingual-e5-small")

    db = Chroma(collection_name= collection_name,
                embedding_function= embeddings,
                persist_directory= str(persist_directory))

    db.reset_collection()

    texts = [chunk["text"] for chunk in all_pages]

    metadatas = [
        {
            "page_number": str(chunk["page_number"]),
            "chunk_index": chunk["chunk_index"]
        }
        for chunk in all_pages
    ]

    ids = [f"chunk_{i}" for i in range(len(all_pages))]

    db.add_texts(
        texts= texts,
        metadatas= metadatas,
        ids= ids
    )

    return collection_name, persist_directory