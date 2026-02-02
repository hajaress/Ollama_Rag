import sqlite3
import chromadb
import ollama

# -------------------------------
# CONFIG
# -------------------------------
DB_PATH = "IFB_refrigerator_service.db"
CHROMA_DIR = "chroma_db_1"
COLLECTION_NAME = "refrigerator_troubleshooting"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:latest"

# -------------------------------
# SQL
# -------------------------------
def get_customer_by_serial(serial_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT serial_number, customer_name, product_model,
           purchase_date, warranty_status, address
    FROM customer_products
    WHERE serial_number = ?
    """, (serial_number,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "serial_number": row[0],
        "customer_name": row[1],
        "product_model": row[2],
        "purchase_date": row[3],
        "warranty_status": row[4],
        "address": row[5]
    }

# -------------------------------
# CHROMA SEARCH
# -------------------------------
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(COLLECTION_NAME)

def get_embedding(text):
    return ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )["embedding"]

# def search_troubleshooting(product_model, issue, top_k=3):
#     query = f"{product_model} issue {issue}"
#     embedding = get_embedding(query)

#     results = collection.query(
#         query_embeddings=[embedding],
#         n_results=top_k,
#         where={"product_model": product_model}
#     )

#     return results["documents"][0] if results["documents"] else []
def search_troubleshooting(product_model, issue, top_k=3):
    query = f"{product_model} issue {issue}"
    embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        where={"product_model": product_model},
        include=["documents", "metadatas", "distances"]
    )

    return results  # ✅ return full dict

# -------------------------------
# PROMPT BUILDER
# -------------------------------
def build_prompt(customer, issue, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    return f"""
You are a refrigerator service assistant.

RULES:
- Use ONLY the troubleshooting context.
- Do not guess or hallucinate.
- If steps are insufficient, recommend service visit.

Customer:
- Name: {customer['customer_name']}
- Product: {customer['product_model']}
- Warranty: {customer['warranty_status']}

Issue:
{issue}

Troubleshooting Context:
{context}

Provide step-by-step guidance with safety instructions.
"""

# -------------------------------
# FINAL RAG RESPONSE
# -------------------------------
# def generate_response(serial_number, issue):
#     customer = get_customer_by_serial(serial_number)

#     if not customer:
#         return "❌ Invalid serial number. Please check and try again."

#     chunks = search_troubleshooting(customer["product_model"], issue)

#     if not chunks:
#         return "⚠️ No troubleshooting steps found. Please schedule a service visit."

#     prompt = build_prompt(customer, issue, chunks)

#     response = ollama.generate(
#         model=LLM_MODEL,
#         prompt=prompt
#     )

#     return response["response"]


# def extract_context_and_citations(results):
#     docs = results["documents"][0]
#     metas = results["metadatas"][0]
#     distances = results["distances"][0]

#     citations = []
#     context_chunks = []

#     for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
#         context_chunks.append(doc)
#         citations.append({
#             "source_pdf": meta["source_pdf"],
#             "product_model": meta["product_model"],
#             "chunk_index": meta["chunk_index"],
#             "distance": round(dist, 4)
#         })

#     return context_chunks, citations

def extract_context_and_citations(results):
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    context_chunks = []
    citations = []

    for doc, meta, dist in zip(docs, metas, dists):
        context_chunks.append(doc)
        citations.append({
            "source_pdf": meta["source_pdf"],
            "product_model": meta["product_model"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4)
        })

    return context_chunks, citations


def generate_response(serial_number, issue):
    customer = get_customer_by_serial(serial_number)

    if not customer:
        return {
            "answer": "Invalid serial number.",
            "citations": []
        }

    results = search_troubleshooting(customer["product_model"], issue)

    # if not results["documents"]:
    #     return {
    #         "answer": "No troubleshooting steps found. Please schedule service.",
    #         "citations": []
    #     }
    # results = search_troubleshooting(customer["product_model"], issue)

    if not results or not results.get("documents") or not results["documents"][0]:
        return {
            "answer": "No troubleshooting steps found. Please schedule service.",
            "citations": []
        }


    context_chunks, citations = extract_context_and_citations(results)

    prompt = build_prompt(customer, issue, context_chunks)

    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt
    )

    return {
        "answer": response["response"],
        "citations": citations
    }

