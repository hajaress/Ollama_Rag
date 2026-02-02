import chromadb
import ollama

# -------------------------------
# Config
# -------------------------------
CHROMA_DIR = "chroma_db_1"
COLLECTION_NAME = "refrigerator_troubleshooting"
EMBED_MODEL = "nomic-embed-text"

# -------------------------------
# Connect to persistent Chroma
# -------------------------------
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(COLLECTION_NAME)

# -------------------------------
# Generate query embedding
# -------------------------------
def get_query_embedding(query: str):
    return ollama.embeddings(
        model=EMBED_MODEL,
        prompt=query
    )["embedding"]

# -------------------------------
# Similarity search (FILTERED)
# -------------------------------
def search_troubleshooting(product_model: str, issue: str, top_k: int = 3):
    query_text = f"{product_model}. Issue: {issue}"

    query_embedding = get_query_embedding(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"product_model": product_model}
    )

    return results

results = search_troubleshooting(
    product_model="B08M643JST",
    issue="Cleaning the Detergent Dispense"
)

for i, doc in enumerate(results["documents"][0]):
    print(f"\n--- Result {i+1} ---")
    print(doc)
    print("\nMetadata:", results["metadatas"][0][i])
    results["distances"]
    print("Distance:", results["distances"][0])