from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import ollama

def ask_document_question(
    question,
    document_collection_name,
    document_database_path
):

    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-small"
    )

    db = Chroma(
        collection_name= document_collection_name,
        embedding_function=embeddings,
        persist_directory= str(document_database_path)
    )

    SCORE_THRESHOLD = 0.36

    results = db.similarity_search_with_score(
        "query: " + question,
        k=1
    )

    if not results:
        return("المعلومة غير متوفرة في المواد المسترجعة.")
        raise SystemExit

    doc, score = results[0]

    if score > SCORE_THRESHOLD:
        return("المعلومة غير متوفرة في المواد المسترجعة.")
        raise SystemExit

    page_number = doc.metadata["page_number"]

    context = f"""
    Page Number: {page_number}
    {doc.page_content}

    ---
    """

    prompt = f"""You are a professional Arabic document inspector assistant.

    RETRIEVED PAGE:
    {context}

    RULES:
    1. Use only information explicitly written in the retrieved page above.
    2. Answer in Arabic only.
    3. First decide silently:
    - Does the retrieved page explicitly contain an answer to the question?
    4. If it does contain the answer:
    - Return only the exact relevant sentence or sentences.
    - Use bullet points.
    - End every bullet with this source reference:
        (المصدر: صفحة رقم {page_number})
    - Preserve the original wording, conditions, names, titles, numbers, dates, and durations.
    - Do not paraphrase.
    - Do not add explanations, conclusions, headings, or information that is not written in the retrieved page.
    5. If the retrieved page does not explicitly contain the answer, return exactly this sentence and nothing else:
    المعلومة غير متوفرة في المواد المسترجعة.
    6. Never write both an answer and the unavailable sentence.
    7. Do not infer an answer from missing information.

    QUESTION:
    {question}

    ANSWER:
    """

    respond = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0,
            "num_ctx": 8192
        }
    )

    answer = respond["message"]["content"]

    return answer