# # # import json
# # # import ollama
# # # import chromadb
# # # from chromadb.config import Settings
# # # from pathlib import Path

# # # CHUNKS_FILE = Path("extracted_chunks/troubleshooting_chunks.json")
# # # CHROMA_DIR = Path("chroma_db")


# # # EMBED_MODEL = "nomic-embed-text:latest"

# # # def get_embedding(text: str):
# # #     response = ollama.embeddings(
# # #         model=EMBED_MODEL,
# # #         prompt=text
# # #     )
# # #     return response["embedding"]

# # # with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
# # #     chunks = json.load(f)

# # # print(f"🔹 Loaded {len(chunks)} chunks")

# # # client = chromadb.Client(
# # #     Settings(
# # #         persist_directory=str(CHROMA_DIR),
# # #         anonymized_telemetry=False
# # #     )
# # # )

# # # collection = client.get_or_create_collection(
# # #     name="refrigerator_troubleshooting"
# # # )

# # # for i, chunk in enumerate(chunks):
# # #     embedding = get_embedding(chunk["content"])

# # #     collection.add(
# # #         ids=[chunk["id"]],
# # #         documents=[chunk["content"]],
# # #         embeddings=[embedding],
# # #         metadatas=[{
# # #             "product_model": chunk["product_model"],
# # #             "source_pdf": chunk["source_pdf"],
# # #             "chunk_index": chunk["chunk_index"]
# # #         }]
# # #     )

# # #     if i % 5 == 0:
# # #         print(f"✅ Stored {i + 1}/{len(chunks)} chunks")

# # # client.persist()

# # # print("Chroma vector DB created successfully")

# # import json
# # import ollama
# # import chromadb
# # import tiktoken
# # from chromadb.config import Settings
# # from pathlib import Path

# # CHUNKS_FILE = Path("extracted_chunks/troubleshooting_chunks.json")
# # CHROMA_DIR = Path("chroma_db")

# # EMBED_MODEL = "nomic-embed-text"
# # MAX_EMBED_TOKENS = 700

# # tokenizer = tiktoken.get_encoding("cl100k_base")

# # def safe_truncate(text, max_tokens=700):
# #     tokens = tokenizer.encode(text)
# #     if len(tokens) <= max_tokens:
# #         return text
# #     return tokenizer.decode(tokens[:max_tokens])

# # def get_embedding(text: str):
# #     response = ollama.embeddings(
# #         model=EMBED_MODEL,
# #         prompt=text
# #     )
# #     return response["embedding"]

# # # Load chunks
# # with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
# #     chunks = json.load(f)

# # client = chromadb.Client(
# #     Settings(
# #         persist_directory=str(CHROMA_DIR),
# #         anonymized_telemetry=False
# #     )
# # )

# # collection = client.get_or_create_collection(
# #     name="refrigerator_troubleshooting"
# # )

# # success, skipped = 0, 0

# # for chunk in chunks:
# #     try:
# #         safe_text = safe_truncate(chunk["content"], MAX_EMBED_TOKENS)

# #         embedding = get_embedding(safe_text)

# #         collection.add(
# #             ids=[chunk["id"]],
# #             documents=[safe_text],
# #             embeddings=[embedding],
# #             metadatas=[{
# #                 "product_model": chunk["product_model"],
# #                 "source_pdf": chunk["source_pdf"],
# #                 "chunk_index": chunk["chunk_index"]
# #             }]
# #         )

# #         success += 1

# #     except Exception as e:
# #         skipped += 1
# #         print(f"⚠️ Skipped {chunk['id']} → {e}")

# # # client.persist()

# # print(f" Stored {success} chunks")
# # print(f" Skipped {skipped} chunks")
# # print("Chroma vector DB created successfully")


import json
import ollama
import chromadb
import tiktoken
from pathlib import Path

# -------------------------------
# Paths
# -------------------------------
CHUNKS_FILE = Path("extracted_chunks/troubleshooting_chunks.json")
CHROMA_DIR = Path("chroma_db_1")

# -------------------------------
# Models & limits
# -------------------------------
EMBED_MODEL = "nomic-embed-text"
MAX_EMBED_TOKENS = 700

tokenizer = tiktoken.get_encoding("cl100k_base")

def safe_truncate(text, max_tokens=700):
    tokens = tokenizer.encode(text)
    return tokenizer.decode(tokens[:max_tokens])

def get_embedding(text: str):
    return ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )["embedding"]

# -------------------------------
# Load chunks
# -------------------------------
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# -------------------------------
# Persistent Chroma Client
# -------------------------------
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="refrigerator_troubleshooting"
)

success, skipped = 0, 0

for chunk in chunks:
    try:
        safe_text = safe_truncate(chunk["content"], MAX_EMBED_TOKENS)
        embedding = get_embedding(safe_text)

        collection.add(
            ids=[chunk["id"]],
            documents=[safe_text],
            embeddings=[embedding],
            metadatas=[{
                "product_model": chunk["product_model"],
                "source_pdf": chunk["source_pdf"],
                "chunk_index": chunk["chunk_index"]
            }]
        )

        success += 1

    except Exception as e:
        skipped += 1
        print(f" Skipped {chunk['id']} → {e}")

print(f" Stored {success} chunks")
print(f" Skipped {skipped} chunks")
print(" Chroma DB persisted automatically")


import chromadb

client = chromadb.PersistentClient(path="chroma_db_1")
collection = client.get_collection("refrigerator_troubleshooting")

print("Total documents:", collection.count())
