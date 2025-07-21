import json
import yaml
import os

with open("bertopic_config.yaml", "r") as f:
    config = yaml.safe_load(f)

output_topics_file = config.get("output_topics_file", "topics_output.json")
output_docs_file = config.get("output_docs_file", "docs_output.json")

topic_labels = {}

# Try loading human-readable topic labels from YAML
try:
    if os.path.exists("topic_labels.yaml"):
        with open("topic_labels.yaml", "r") as f:
            label_config = yaml.safe_load(f)
            topic_labels = label_config.get("topic_labels", {})
    else:
        print("No topic_labels.yaml found — using default topic names.")
except Exception as e:
    print(f"Error loading topic_labels.yaml: {e} — using default topic names.")
    topic_labels = {}

# Load and label topics_output.json
with open(output_topics_file, "r") as f:
    topics = json.load(f)

for topic in topics:
    topic_num = topic["Topic"]
    topic["Label"] = topic_labels.get(topic_num, f"Topic {topic_num}")

with open("topics_labeled.json", "w") as f:
    json.dump(topics, f, indent=2)

# Load and label docs_output.json
with open(output_docs_file, "r") as f:
    docs = json.load(f)

for doc in docs:
    topic_num = doc["topic"]
    doc["topic_label"] = topic_labels.get(topic_num, f"Topic {topic_num}")

with open("docs_labeled.json", "w") as f:
    json.dump(docs, f, indent=2)

print("Labeled topics saved to topics_labeled.json")
print("Labeled document assignments saved to docs_labeled.json")