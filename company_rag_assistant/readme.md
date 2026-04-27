<a name="readme-top"></a>

<br />
<div align="center">
<h3 align="center">Company Knowledge RAG Assistant</h3>

  <p align="center">
    A fully local Retrieval-Augmented Generation (RAG) system with Hybrid Search and Streaming using open-weight models
  </p>
</div>

---

## About The Project

The **Company Knowledge RAG Assistant** is a local AI system that allows you to query internal documents such as handbooks, policies, or onboarding guides.

It combines:
- semantic vector search
- keyword search (BM25)
- reranking
- local LLMs

to provide accurate, source-grounded answers without relying on external APIs.

---

## Features

- Upload `.txt`, `.md`, `.pdf`
- Hybrid Search (BM25 + Vector Search)
- Cross-Encoder reranking
- Local LLM via Ollama
- Streaming responses
- Chat interface with history
- Source-grounded answers
- Document deletion & reindexing
- Fully Dockerized

---

## Architecture

```text
Query
 ├── Vector Search (ChromaDB)
 ├── Keyword Search (BM25)
 └── Merge
        ↓
   CrossEncoder Reranker
        ↓
     Context Builder
        ↓
     Ollama (LLM)
        ↓
   Streaming Answer
```

---

## Built With

- Python
- FastAPI
- Streamlit
- ChromaDB
- sentence-transformers
- rank-bm25
- Ollama
- Docker

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Git
- At least ~8GB RAM recommended
- ⚠️ Ollama is required (runs inside Docker)

```diff
@@ No external APIs required - Ollama is used locally @@
```

---

### Ollama

This project uses **Ollama** to run local open-weight models.

- Ollama is automatically started via Docker Compose
- The model is automatically pulled on first run
- No manual installation is required

Default model:

```env
OLLAMA_MODEL=mistral
```

You can change the model in `.env`.

---

### Installation

1. Clone the repository:

```sh
git clone https://github.com/kfitkau/my-projects.git
```

2. Navigate into the project:

```sh
cd company_rag_assistant
```

3. Setup environment:
linux:
```sh
cp .env.example .env
```
or 
windows:
```sh
copy .env.example .env
```

4. Start the system:

```sh
docker compose up --build
```

> ⚠️ First startup may take several minutes because the Ollama model will be downloaded.

---

### Usage

1. Open UI:

```
http://localhost:8501
```

2. Upload documents

3. Ask questions:
- "Do employees need VPN?"
- "How long is onboarding?"
- "Remote work policy?"

4. Watch streaming answers and inspect sources

---

## Evaluation

This project includes a simple evaluation script to measure the
retrieval quality of the RAG system.

The evaluation focuses on **retrieval accuracy**, specifically: -
Whether the correct document is retrieved for a given question -
Measured via **Hit Rate**

---

###  Evaluation Dataset

The evaluation uses a CSV file:

eval/questions.csv

Expected format:

question,expected_source "What is the vacation
policy?","employee_handbook.pdf" "Do employees need VPN?","it_policy.md"

---

### Setup (Python Virtual Environment)

It is recommended to run the evaluation in a separate Python
environment.

#### 1. Create virtual environment

Linux / macOS: python3 -m venv .venv source .venv/bin/activate

Windows: python -m venv .venv .venv`\Scripts`{=tex}`\activate`{=tex}

---

#### 2. Install dependencies

pip install pandas requests

Optional: pip install -r requirements.txt

---

### Run Evaluation

Make sure your backend is running:

docker compose up

Then execute:

python eval/evaluate_retrieval.py

---

### Output Example

Question: Do employees need VPN? Expected: it_policy.md Retrieved:
\['it_policy.md', 'onboarding.md'\] Hit: True
-------------------------------------------------- Hit Rate: 0.80

---

### Metrics

-   Hit (True/False): Whether the expected document appears in results
-   Hit Rate: correct_hits / total_questions

---

### Interpretation

-   High Hit Rate (≥ 0.8): good retrieval
-   Medium (0.5 -- 0.8): can be improved
-   Low (\< 0.5): needs tuning

---

### Possible Improvements

-   Adjust chunk size
-   Tune retrieval parameters
-   Improve documents
-   Add more queries
-   Add semantic evaluation

---

### Notes

-   Only retrieval is evaluated
-   LLM answer quality is not measured

---

## Limitations

- No authentication
- Single-user setup
- No OCR for scanned PDFs
- No distributed scaling

---

## License

MIT License
