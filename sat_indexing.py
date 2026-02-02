import pdfplumber
import tiktoken
from pathlib import Path
import json

PDF_DIR = Path("product_pdfs")
OUTPUT_DIR = Path("extracted_chunks")
OUTPUT_DIR.mkdir(exist_ok=True)

CHUNK_SIZE = 500
OVERLAP = 50

tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    return len(tokenizer.encode(text))


def chunk_text(text, chunk_size=500, overlap=50):
    tokens = tokenizer.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)

        chunks.append(chunk_text)

        start = end - overlap

    return chunks


def extract_text_from_pdf(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                pages.append({
                    "page": page_num,
                    "text": text.strip()
                })
    return pages


all_chunks = []

for pdf_file in PDF_DIR.glob("*.pdf"):
    product_name = pdf_file.stem.replace("_", " ")

    pages = extract_text_from_pdf(pdf_file)

    full_text = "\n".join([p["text"] for p in pages])

    chunks = chunk_text(full_text)

    for idx, chunk in enumerate(chunks):
        chunk_data = {
            "id": f"{pdf_file.stem}_chunk_{idx}",
            "product_model": product_name,
            "source_pdf": pdf_file.name,
            "chunk_index": idx,
            "token_count": count_tokens(chunk),
            "content": chunk
        }
        all_chunks.append(chunk_data)

# Save chunks as JSON (easy for next step)
output_file = OUTPUT_DIR / "troubleshooting_chunks.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

print(f"✅ Extracted & chunked {len(all_chunks)} chunks")
print(f"📁 Saved to {output_file}")
