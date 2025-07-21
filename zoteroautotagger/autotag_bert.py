import yaml
import json
from pathlib import Path
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

from zoteroautotagger.utils import clean_text

# --- Load config ---
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

input_file = Path(config["input_file"])
output_topics_file = Path(config["output_topics_file"])
output_docs_file = Path(config["output_docs_file"])
min_topic_size = config.get("min_topic_size", 5)
n_components = config.get("n_components")
nr_topics = config.get("nr_topics", "auto")
verbose = config.get("verbose", False)

# --- Load data ---
with open(input_file, "r") as f:
    items = json.load(f)

texts = []
doc_ids = []
for item in tqdm(items, desc="Preparing documents"):
    title_clean = clean_text(item.get("title", ""))
    abstract_clean = clean_text(item.get("abstract", ""))
    text = f"{title_clean}. {abstract_clean}".strip()
    if text:
        texts.append(text)
        doc_ids.append(item.get("id", ""))

# --- Run BERTopic ---
vectorizer_model = CountVectorizer(stop_words="english")
topic_model = BERTopic(
    min_topic_size=min_topic_size,
    nr_topics=nr_topics,
    vectorizer_model=vectorizer_model,
    embedding_model="all-MiniLM-L6-v2",
    verbose=verbose
)

topics, probs = topic_model.fit_transform(texts)

# --- Output topics ---
topics_info = topic_model.get_topic_info().to_dict(orient="records")
with open(output_topics_file, "w") as f:
    json.dump(topics_info, f, indent=2)

# --- Output documents ---
doc_results = []
for idx, topic in enumerate(topics):
    doc_results.append({
        "id": doc_ids[idx],
        "topic": int(topic),
        "text": texts[idx],
        "probability": float(probs[idx]) if probs[idx] else None
    })

with open(output_docs_file, "w") as f:
    json.dump(doc_results, f, indent=2)

print(f"Topics saved to {output_topics_file}")
print(f"Document-topic assignments saved to {output_docs_file}")
