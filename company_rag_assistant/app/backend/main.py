# =============================================================================
# Standard Library Imports
# =============================================================================
import json
import os
import re
from pathlib import Path
from typing import Iterator
from uuid import uuid4

# =============================================================================
# Third-Party Imports
# =============================================================================
import chromadb
import requests
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pypdf import PdfReader
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

# =============================================================================
# Environment & Application Setup
# =============================================================================

load_dotenv()

app = FastAPI(title="Company Knowledge RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion auf erlaubte Domains einschränken.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Storage Configuration
# =============================================================================

RAW_DATA_DIR = Path("app/data/raw")
CHROMA_DIR = Path("app/data/chroma")

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Model & Retrieval Configuration
# =============================================================================

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "company_knowledge")

RERANK_CANDIDATES = int(os.getenv("RERANK_CANDIDATES", 10))
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", 5))
DISTANCE_THRESHOLD = float(os.getenv("DISTANCE_THRESHOLD", 1.5))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", 3000))
BM25_CANDIDATES = int(os.getenv("BM25_CANDIDATES", 10))
HYBRID_CANDIDATES = int(os.getenv("HYBRID_CANDIDATES", 20))


# =============================================================================
# Embedding, Reranking & Vector Database Setup
# =============================================================================

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=embedding_function,
)


# =============================================================================
# Document Loading & Chunking
# =============================================================================

def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extrahiert Text aus einer PDF-Datei.

    Leere oder nicht lesbare Seiten werden übersprungen.

    Args:
        file_path (Path): Pfad zur PDF-Datei.

    Returns:
        str: Extrahierter Text aller lesbaren PDF-Seiten, getrennt durch
        doppelte Zeilenumbrüche.
    """
    reader = PdfReader(str(file_path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n\n".join(pages)


def load_document_text(file_path: Path) -> str:
    """
    Lädt den Textinhalt eines Dokuments.

    Unterstützt PDF-Dateien sowie textbasierte Dateien wie .txt und .md.

    Args:
        file_path (Path): Pfad zur Datei, deren Inhalt geladen werden soll.

    Returns:
        str: Textinhalt der Datei.
    """
    if file_path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)

    return file_path.read_text(encoding="utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 900) -> list[str]:
    """
    Zerlegt Text in semantisch sinnvolle Abschnitte auf Paragraph-Basis.

    Diese Methode vermeidet harte Schnitte mitten im Text und verbessert dadurch
    die Qualität der späteren Retrieval-Ergebnisse.

    Args:
        text (str): Vollständiger Eingabetext, der in kleinere Chunks
            zerlegt werden soll.
        chunk_size (int, optional): Maximale Länge eines Chunks in Zeichen.
            Standard ist 900.

    Returns:
        list[str]: Liste bereinigter Text-Chunks.
    """
    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# =============================================================================
# Vector Retrieval Helpers
# =============================================================================

def parse_chroma_results(results: dict) -> list[dict]:
    """
    Normalisiert ChromaDB-Ergebnisse in ein einheitliches internes Format.

    Args:
        results (dict): Rohes Ergebnisobjekt aus einer ChromaDB-Query.

    Returns:
        list[dict]: Liste normalisierter Treffer mit Text, Metadaten,
        Distanzscore und Retrieval-Quelle.
    """
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    return [
        {
            "id": chunk_id,
            "text": doc,
            "metadata": meta,
            "score": float(dist),
            "retrieval_source": "vector",
        }
        for chunk_id, doc, meta, dist in zip(ids, documents, metadatas, distances)
    ]


def filter_retrieved_chunks(retrieved_chunks: list[dict]) -> list[dict]:
    """
    Filtert semantische Treffer anhand eines Distanz-Schwellwerts.

    Falls alle Treffer herausgefiltert würden, wird aus Fallback-Gründen die
    ursprüngliche Trefferliste zurückgegeben.

    Args:
        retrieved_chunks (list[dict]): Liste gefundener Chunks aus der
            Vektorsuche.

    Returns:
        list[dict]: Gefilterte oder ursprüngliche Liste von Chunks.
    """
    filtered = [
        chunk for chunk in retrieved_chunks if chunk["score"] < DISTANCE_THRESHOLD
    ]

    return filtered if filtered else retrieved_chunks


def rerank_results(query: str, results: list[dict], top_k: int) -> list[dict]:
    """
    Bewertet Retrieval-Ergebnisse mit einem CrossEncoder neu.

    Der CrossEncoder vergleicht Query und Chunk direkt und liefert dadurch meist
    präzisere Relevanzbewertungen als reine Embedding-Distanzen.

    Args:
        query (str): Benutzerfrage oder Suchanfrage.
        results (list[dict]): Liste initial gefundener Dokument-Chunks.
        top_k (int): Anzahl der relevantesten Ergebnisse, die zurückgegeben
            werden sollen.

    Returns:
        list[dict]: Nach Relevanz sortierte Trefferliste inklusive
        `rerank_score`.
    """
    if not results:
        return []

    pairs = [(query, result["text"]) for result in results]
    scores = reranker.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):
        item = result.copy()
        item["rerank_score"] = float(score)
        reranked.append(item)

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

    return reranked[:top_k]


# =============================================================================
# BM25 Keyword Retrieval
# =============================================================================

def tokenize(text: str) -> list[str]:
    """
    Tokenisiert Text für die BM25-Suche.

    Args:
        text (str): Eingabetext, der tokenisiert werden soll.

    Returns:
        list[str]: Liste kleingeschriebener Wort-Tokens.
    """
    return re.findall(r"\b\w+\b", text.lower())


def get_all_indexed_chunks() -> list[dict]:
    """
    Lädt alle bereits indexierten Chunks aus ChromaDB.

    Diese Funktion wird benötigt, um darauf eine BM25-Suche auszuführen.

    Args:
        Keine.

    Returns:
        list[dict]: Liste aller gespeicherten Dokument-Chunks inklusive
        Metadaten.
    """
    data = collection.get()

    documents = data.get("documents", [])
    metadatas = data.get("metadatas", [])
    ids = data.get("ids", [])

    chunks = []

    for doc_id, doc, meta in zip(ids, documents, metadatas):
        chunks.append(
            {
                "id": doc_id,
                "text": doc,
                "metadata": meta,
                "score": None,
                "retrieval_source": "bm25",
            }
        )

    return chunks


def bm25_search(query: str, top_k: int = BM25_CANDIDATES) -> list[dict]:
    """
    Führt eine keyword-basierte BM25-Suche über alle indexierten Chunks aus.

    BM25 ergänzt die semantische Suche, da exakte Begriffe, Abkürzungen oder
    Eigennamen häufig besser gefunden werden.

    Args:
        query (str): Suchanfrage des Benutzers.
        top_k (int, optional): Anzahl der besten BM25-Treffer.
            Standard ist BM25_CANDIDATES.

    Returns:
        list[dict]: Liste der besten BM25-Treffer inklusive `bm25_score`.
    """
    chunks = get_all_indexed_chunks()

    if not chunks:
        return []

    tokenized_corpus = [tokenize(chunk["text"]) for chunk in chunks]
    tokenized_query = tokenize(query)

    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(tokenized_query)

    ranked = []

    for chunk, score in zip(chunks, scores):
        item = chunk.copy()
        item["bm25_score"] = float(score)
        ranked.append(item)

    ranked.sort(key=lambda x: x["bm25_score"], reverse=True)

    return ranked[:top_k]


# =============================================================================
# Hybrid Retrieval Pipeline
# =============================================================================

def merge_hybrid_results(
    vector_results: list[dict],
    bm25_results: list[dict],
    max_candidates: int = HYBRID_CANDIDATES,
) -> list[dict]:
    """
    Kombiniert Ergebnisse aus Vektorsuche und BM25-Suche.

    Doppelte Treffer werden anhand ihrer Chunk-ID zusammengeführt. Treffer, die
    aus beiden Methoden stammen, werden als `hybrid` markiert.

    Args:
        vector_results (list[dict]): Treffer aus der semantischen Vektorsuche.
        bm25_results (list[dict]): Treffer aus der keyword-basierten BM25-Suche.
        max_candidates (int, optional): Maximale Anzahl kombinierter Kandidaten.
            Standard ist HYBRID_CANDIDATES.

    Returns:
        list[dict]: Zusammengeführte Trefferliste aus beiden Retrieval-Methoden.
    """
    merged = {}

    for result in vector_results:
        key = result["id"]
        merged[key] = result.copy()
        merged[key]["retrieval_source"] = "vector"

    for result in bm25_results:
        key = result["id"]

        if key in merged:
            merged[key]["retrieval_source"] = "hybrid"
            merged[key]["bm25_score"] = result.get("bm25_score")
        else:
            merged[key] = result.copy()

    return list(merged.values())[:max_candidates]


def retrieve_chunks(query: str) -> list[dict]:
    """
    Führt die vollständige Retrieval-Pipeline aus.

    Ablauf:
    1. Semantische Vektorsuche in ChromaDB
    2. Filterung nach Distanz
    3. BM25-Keyword-Suche
    4. Zusammenführung zu Hybrid-Ergebnissen
    5. Re-Ranking mit CrossEncoder

    Args:
        query (str): Benutzerfrage oder Suchanfrage.

    Returns:
        list[dict]: Final sortierte Liste der relevantesten Dokument-Chunks.
    """
    vector_raw = collection.query(
        query_texts=[query],
        n_results=RERANK_CANDIDATES,
    )

    vector_results = parse_chroma_results(vector_raw)
    vector_results = filter_retrieved_chunks(vector_results)

    bm25_results = bm25_search(
        query=query,
        top_k=BM25_CANDIDATES,
    )

    hybrid_results = merge_hybrid_results(
        vector_results=vector_results,
        bm25_results=bm25_results,
        max_candidates=HYBRID_CANDIDATES,
    )

    return rerank_results(
        query=query,
        results=hybrid_results,
        top_k=RETRIEVAL_TOP_K,
    )


# =============================================================================
# Prompt & Context Building
# =============================================================================

def build_context(results: list[dict]) -> str:
    """
    Erstellt den Kontext für das LLM aus den besten Retrieval-Ergebnissen.

    Die Kontextlänge wird begrenzt, damit der Prompt nicht zu groß wird.

    Args:
        results (list[dict]): Liste relevanter Dokument-Chunks inklusive
            Text und Metadaten.

    Returns:
        str: Formatierter Kontext mit Quellen- und Chunk-Angaben.
    """
    context_parts = []
    total_length = 0

    for result in results:
        text = result["text"]

        if total_length + len(text) > MAX_CONTEXT_CHARS:
            break

        source = result["metadata"]["filename"]
        chunk_index = result["metadata"]["chunk_index"]

        context_parts.append(f"[Source: {source}, Chunk: {chunk_index}]\n{text}")
        total_length += len(text)

    return "\n\n".join(context_parts)


def build_prompt(question: str, context: str) -> str:
    """
    Erstellt den finalen Prompt für das lokale LLM.

    Der Prompt zwingt das Modell dazu, ausschließlich auf Basis des gegebenen
    Kontexts zu antworten.

    Args:
        question (str): Benutzerfrage.
        context (str): Aus Dokumenten zusammengestellter Kontext.

    Returns:
        str: Vollständiger Prompt für das LLM.
    """
    return f"""
You are an AI assistant for company internal knowledge.

Answer the question ONLY based on the provided context.

Rules:
- Be concise and factual.
- If the answer is not contained in the context, say:
  "I don't know based on the provided documents."
- Cite the document names you used.
- Do not invent policies, numbers, names, or procedures.

Context:
{context}

Question:
{question}

Answer:
"""


# =============================================================================
# Local LLM Communication
# =============================================================================

def ask_local_llm(question: str, context: str) -> str:
    """
    Sendet eine nicht-streamende Anfrage an das lokale LLM.

    Args:
        question (str): Benutzerfrage.
        context (str): Relevanter Dokumentenkontext.

    Returns:
        str: Generierte Antwort des lokalen LLM.

    Raises:
        requests.HTTPError: Wenn der Ollama-Endpunkt einen Fehlerstatus liefert.
    """
    prompt = build_prompt(question, context)

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    response.raise_for_status()

    return response.json()["message"]["content"]


def stream_local_llm(question: str, context: str) -> Iterator[str]:
    """
    Sendet eine streamende Anfrage an das lokale LLM.

    Die Antwort wird als NDJSON-kompatibler Token-Stream zurückgegeben.

    Args:
        question (str): Benutzerfrage.
        context (str): Relevanter Dokumentenkontext.

    Yields:
        Iterator[str]: JSON-Zeilen mit Token-Inhalten oder Done-Signal.

    Raises:
        requests.HTTPError: Wenn der Ollama-Endpunkt einen Fehlerstatus liefert.
    """
    prompt = build_prompt(question, context)

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    with requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True,
        timeout=300,
    ) as response:
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            token = data.get("message", {}).get("content", "")
            done = data.get("done", False)

            if token:
                yield json.dumps({"type": "token", "content": token}) + "\n"

            if done:
                yield json.dumps({"type": "done"}) + "\n"
                break


# =============================================================================
# Response Formatting
# =============================================================================

def format_sources(retrieved_chunks: list[dict]) -> list[dict]:
    """
    Formatiert Retrieval-Treffer als Quellenangaben für API-Antworten.

    Args:
        retrieved_chunks (list[dict]): Liste der abgerufenen Dokument-Chunks.

    Returns:
        list[dict]: Quellenliste mit Dateiname, Chunk, Scores und
        Retrieval-Methode.
    """
    return [
        {
            "filename": chunk["metadata"]["filename"],
            "chunk_index": chunk["metadata"]["chunk_index"],
            "chunk": chunk["text"],
            "score": chunk.get("score"),
            "bm25_score": chunk.get("bm25_score"),
            "rerank_score": chunk.get("rerank_score"),
            "retrieval_source": chunk.get("retrieval_source"),
        }
        for chunk in retrieved_chunks
    ]


# =============================================================================
# Indexing
# =============================================================================

def index_document(file_path: Path, filename: str) -> dict:
    """
    Lädt, chunked und indexiert ein Dokument in ChromaDB.

    Für jedes Dokument wird eine eindeutige Dokument-ID erzeugt. Jeder Chunk
    erhält zusätzlich eine eigene Chunk-ID.

    Args:
        file_path (Path): Lokaler Pfad zur gespeicherten Datei.
        filename (str): Ursprünglicher Dateiname für Metadaten und Anzeige.

    Returns:
        dict: Statistik über das indexierte Dokument, inklusive Dateiname,
        Zeichenanzahl und Anzahl erzeugter Chunks.
    """
    text = load_document_text(file_path)
    chunks = chunk_text(text)

    doc_id = str(uuid4())

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        ids.append(f"{doc_id}_{index}")
        documents.append(chunk)
        metadatas.append(
            {
                "filename": filename,
                "doc_id": doc_id,
                "chunk_index": index,
            }
        )

    if chunks:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

    return {
        "filename": filename,
        "characters": len(text),
        "chunks_created": len(chunks),
    }


# =============================================================================
# API Routes
# =============================================================================

@app.get("/health")
def health():
    """
    Prüft, ob die API erreichbar ist.

    Args:
        Keine.

    Returns:
        dict: Statusmeldung der API.
    """
    return {"status": "ok"}


@app.get("/")
def root():
    """
    Gibt eine einfache Willkommensnachricht zurück.

    Args:
        Keine.

    Returns:
        dict: Basisinformation zur API.
    """
    return {"message": "Company Knowledge RAG API"}


@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    """
    Nimmt eine Datei entgegen, speichert sie lokal und indexiert sie.

    Unterstützt werden .txt, .md und .pdf Dateien.

    Args:
        file (UploadFile): Hochgeladene Datei aus dem Multipart-Request.

    Returns:
        dict: Erfolgs- oder Fehlermeldung inklusive Indexierungsstatistik.
    """
    supported_extensions = (".txt", ".md", ".pdf")

    if not file.filename.endswith(supported_extensions):
        return {
            "status": "error",
            "message": "Only .txt, .md and .pdf files are supported.",
        }

    file_path = RAW_DATA_DIR / file.filename
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    result = index_document(file_path, file.filename)

    return {
        "status": "success",
        **result,
        "saved_to": str(file_path),
    }


@app.get("/documents")
def list_documents():
    """
    Listet alle aktuell indexierten Dokumente auf.

    Args:
        Keine.

    Returns:
        dict: Liste eindeutiger Dateinamen und Anzahl der Dokumente.
    """
    data = collection.get()

    metadatas = data.get("metadatas", [])

    filenames = sorted(
        set(metadata["filename"] for metadata in metadatas if metadata)
    )

    return {
        "documents": filenames,
        "count": len(filenames),
    }


@app.delete("/documents/{filename}")
def delete_document(filename: str):
    """
    Löscht ein Dokument aus ChromaDB und entfernt die lokale Datei.

    Args:
        filename (str): Name der zu löschenden Datei.

    Returns:
        dict: Statusmeldung zur Löschoperation.
    """
    collection.delete(where={"filename": filename})

    file_path = RAW_DATA_DIR / filename
    if file_path.exists():
        file_path.unlink()

    return {
        "status": "success",
        "message": f"Deleted document: {filename}",
    }


@app.post("/documents/{filename}/reindex")
def reindex_document(filename: str):
    """
    Löscht vorhandene Chunks eines Dokuments und indexiert die Datei erneut.

    Args:
        filename (str): Name der Datei, die neu indexiert werden soll.

    Returns:
        dict: Erfolgs- oder Fehlermeldung inklusive neuer Indexierungsstatistik.
    """
    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        return {
            "status": "error",
            "message": f"File not found: {filename}",
        }

    collection.delete(where={"filename": filename})
    result = index_document(file_path, filename)

    return {
        "status": "success",
        "message": f"Reindexed document: {filename}",
        **result,
    }


@app.post("/search")
def search(query: str):
    """
    Führt eine reine Retrieval-Suche aus, ohne das LLM aufzurufen.

    Args:
        query (str): Suchanfrage des Benutzers.

    Returns:
        dict: Suchanfrage und relevante Retrieval-Ergebnisse.
    """
    retrieved_chunks = retrieve_chunks(query)

    return {
        "query": query,
        "results": retrieved_chunks,
    }


@app.post("/chat")
def chat(query: str):
    """
    Beantwortet eine Benutzerfrage anhand der indexierten Dokumente.

    Ablauf:
    1. Relevante Chunks abrufen
    2. Kontext bauen
    3. Lokales LLM abfragen
    4. Antwort inklusive Quellen zurückgeben

    Args:
        query (str): Frage des Benutzers.

    Returns:
        dict: Antwort des LLM sowie verwendete Quellen.
    """
    retrieved_chunks = retrieve_chunks(query)
    context = build_context(retrieved_chunks)

    if not context.strip():
        return {
            "query": query,
            "answer": "I don't know based on the provided documents.",
            "sources": [],
        }

    answer = ask_local_llm(query, context)

    return {
        "query": query,
        "answer": answer,
        "sources": format_sources(retrieved_chunks),
    }


@app.post("/chat/stream")
def chat_stream(query: str):
    """
    Beantwortet eine Benutzerfrage als Streaming-Antwort.

    Zuerst werden die Quellen gesendet, anschließend die generierten Tokens
    des lokalen LLMs.

    Args:
        query (str): Frage des Benutzers.

    Returns:
        StreamingResponse: NDJSON-Stream mit Quellen, Tokens und Done-Signal.
    """
    retrieved_chunks = retrieve_chunks(query)
    context = build_context(retrieved_chunks)

    def event_generator() -> Iterator[str]:
        """
        Erzeugt den NDJSON-Stream für Quellen und Antworttokens.

        Args:
            Keine.

        Yields:
            Iterator[str]: JSON-Zeilen mit Quellen, Tokens oder Done-Signal.
        """
        sources = format_sources(retrieved_chunks)

        yield json.dumps(
            {
                "type": "sources",
                "sources": sources,
            }
        ) + "\n"

        if not context.strip():
            yield json.dumps(
                {
                    "type": "token",
                    "content": "I don't know based on the provided documents.",
                }
            ) + "\n"
            yield json.dumps({"type": "done"}) + "\n"
            return

        yield from stream_local_llm(query, context)

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson",
    )