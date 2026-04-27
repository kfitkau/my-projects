import pandas as pd
import requests


# =============================================================================
# Evaluation Configuration
# =============================================================================

BACKEND_URL = "http://localhost:8000"


# =============================================================================
# Load Evaluation Dataset
# =============================================================================

# Erwartet eine CSV-Datei mit mindestens den Spalten:
# - question: Testfrage
# - expected_source: erwartetes Quelldokument
df = pd.read_csv("eval/questions.csv")


# =============================================================================
# Retrieval Evaluation
# =============================================================================

hits = 0

for _, row in df.iterrows():
    question = row["question"]
    expected_source = row["expected_source"]

    response = requests.post(
        f"{BACKEND_URL}/search",
        params={"query": question},
        timeout=120,
    )

    data = response.json()

    retrieved_sources = [
        item["metadata"]["filename"]
        for item in data["results"]
    ]

    hit = expected_source in retrieved_sources
    hits += int(hit)

    print(f"Question: {question}")
    print(f"Expected: {expected_source}")
    print(f"Retrieved: {retrieved_sources}")
    print(f"Hit: {hit}")
    print("-" * 50)


# =============================================================================
# Evaluation Result
# =============================================================================

print(f"Hit Rate: {hits / len(df):.2f}")