# 🧊 Refrigerator Service RAG Chatbot  
### (Ollama + SQLite + ChromaDB)

An **end-to-end Retrieval-Augmented Generation (RAG) chatbot** designed for **refrigerator service and repair workflows**.  
The system combines **structured customer data (SQL)** with **unstructured troubleshooting manuals (PDFs)** and uses **Ollama (local LLM)** to generate **accurate, model-specific, explainable troubleshooting responses with source citations**.

---

## 📌 Problem Statement

In appliance service and repair workflows, technicians and support agents must manually verify customer details, warranty status, and search through lengthy product manuals to diagnose issues. This process is time-consuming, error-prone, and highly dependent on individual experience.

This project aims to build an **intelligent, accurate, and auditable RAG-based chatbot** that:
- Uses a **serial number** to retrieve customer and product details
- Fetches **model-specific troubleshooting steps** from product manuals
- Generates **step-by-step repair guidance**
- Provides **source citations** for trust and auditability
- Prevents hallucinations using strict prompts and confidence gating

---

## 🎯 Key Features

- 🔢 Serial number–based customer lookup
- 🗄️ SQLite database for purchase, warranty, and service history
- 📄 Troubleshooting PDFs as knowledge base
- 🧠 Semantic search using Chroma vector database
- 🤖 Local LLM reasoning using Ollama
- 📚 Source citations with every answer
- 🚫 Hallucination control with strict prompts
- 🛠️ Technician-focused troubleshooting responses

---

## 🏗️ High-Level Architecture

User
└─► Enter Serial Number
└─► SQLite Database (Customer & Product Data)
└─► Product Model
└─► Enter Issue Description
└─► Chroma Vector DB (PDF Chunks)
└─► Ollama LLM
└─► Answer + Source Citations

---

## 📂 Project Structure

project/
│
├── product_pdfs/ # Troubleshooting manuals (PDF)
│├── LG_FrostFree_260L.pdf
│├── Samsung_Digital_Inverter_275L.pdf
│
├── extracted_chunks/
│└── troubleshooting_chunks.json
│
├── chroma_db/ # Persistent vector database
│
├── refrigerator_service.db # SQLite database
│
├── create_db.py # Create SQL tables
├── insert_dummy_data.py # Insert sample data
│
├── generate_troubleshooting_pdfs.py
├── extract_and_chunk.py
├── create_chroma_index.py
│
├── rag_engine.py # SQL + Chroma + Ollama logic
├── chatbot.py # CLI chatbot
│
└── README.md


---

## 🧰 Prerequisites

### System Requirements
- Python **3.9+**
- 8 GB RAM recommended
- Local disk for vector DB

---

## 🤖 Install & Setup Ollama

Download Ollama:
pip install pdfplumber tiktoken chromadb ollama reportlab

python sat_main.py
