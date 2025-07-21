import requests
import json
import re
import yaml

# Load Zotero API config
with open("zotero_config.yaml", "r") as f:
    config = yaml.safe_load(f)

ZOTERO_API_KEY = config["api_key"]
ZOTERO_USER_ID = config["user_id"]
LIBRARY_TYPE = config.get("library_type", "user")
HEADERS = {"Zotero-API-Key": ZOTERO_API_KEY}

# Load the labeled documents
with open("docs_labeled.json", "r") as f:
    docs = json.load(f)


# Extract Zotero item key
def extract_key(zotero_id_url):
    match = re.search(r'/items/([A-Z0-9]+)$', zotero_id_url)
    return match.group(1) if match else None


def extract_method_tags(text):
    method_keywords = {
        "rna-seq": "RNA-seq",
        "chip-seq": "ChIP-seq",
        "atac-seq": "ATAC-seq",
        "scrna-seq": "scRNA-seq",
        "bulk rna": "Bulk RNA-seq",
        "single-cell": "Single-cell",
        "ngs": "NGS",
        "deconvolution": "Deconvolution",
        "dimensionality reduction": "Dimensionality Reduction",
        "pca": "PCA",
        "umap": "UMAP",
        "tsne": "t-SNE",
        "harmony": "Harmony",
        "scanpy": "Scanpy",
        "seurat": "Seurat",
        "nextflow": "Nextflow",
        "snakemake": "Snakemake"
    }
    tags = []
    text_lower = text.lower()
    for keyword, tag in method_keywords.items():
        if keyword in text_lower:
            tags.append(tag)
    return tags


# Loop through each document and tag in Zotero
for doc in docs:
    item_url = doc.get("id", "")
    item_key = extract_key(item_url)
    topic_labels = doc.get("topic_label")
    text_content = doc.get("text", "")
    method_labels = extract_method_tags(text_content)

    if isinstance(topic_labels, str):
        topic_labels = [topic_labels]
    elif not isinstance(topic_labels, list):
        topic_labels = []

    if isinstance(method_labels, str):
        method_labels = [method_labels]
    elif not isinstance(method_labels, list):
        method_labels = []

    all_tags = topic_labels + method_labels

    if not item_key or not all_tags:
        continue

    # Get full item to modify tags
    item_url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{ZOTERO_USER_ID}/items/{item_key}"
    item_resp = requests.get(item_url, headers=HEADERS)

    if item_resp.status_code != 200:
        print(f"Failed to retrieve full item {item_key}")
        continue

    item_data = item_resp.json()
    current_version = item_data["version"]
    current_tags = [tag["tag"] for tag in item_data.get("data", {}).get("tags", [])]

    # Append only new tags
    updated_tags = item_data["data"].get("tags", [])
    for tag in all_tags:
        if tag not in current_tags:
            updated_tags.append({"tag": tag})

    item_data["data"]["tags"] = updated_tags

    # PUT updated item back
    put_headers = {
        **HEADERS,
        "If-Unmodified-Since-Version": str(current_version),
        "Content-Type": "application/json"
    }

    put_resp = requests.put(item_url, headers=put_headers, data=json.dumps(item_data["data"]))

    if put_resp.status_code in [200, 204]:
        print(f"Updated tags for item {item_key}")
    else:
        print(f"Failed to update item {item_key}: {put_resp.status_code} - {put_resp.text}")