

# ZoteroAutoTagger

ZoteroAutoTagger is a Python package that uses topic modeling and natural language processing (NLP) to automatically tag items in a Zotero library. It helps researchers organize their libraries by content-based topics without manual tagging.

---

## Features

- Extracts topics from paper abstracts and full-text using BERTopic
- Automatically applies human-readable topic labels
- Integrates with Zotero via its Web API to tag items
- Uses YAML config files for customization and reproducibility
- Works in batch — no manual tagging needed

---

## Installation

```bash
git clone https://github.com/nick-rodriguez/ZoteroAutoTagger.git
cd ZoteroAutoTagger
pip install -e .
```

---

## Input and Configuration




To generate the `library.json` input file, export your Zotero library or a collection:

1. Open Zotero.
2. Right-click on the collection (or your full library) you want to analyze.
3. Choose **Export Collection** (or **Export Library**).
4. Select **Format: Zotero RDF** or **Format: JSON** depending on your setup.
   - This tool expects a JSON export.
5. Uncheck all optional checkboxes unless you want file attachments.
6. Save the file as `library.json` in your project directory or update the `input_file` path in your config.

This package requires two YAML configuration files:

### `config.yaml`

```yaml
input_file: "library.json"
output_topics_file: "topics_output.json"
output_docs_file: "docs_output.json"
topic_labels_yaml: "topic_labels.yaml"
```

### `zotero_config.yaml`

```yaml
api_key: "YOUR_ZOTERO_API_KEY"
user_id: "YOUR_USER_ID"
library_type: "user"  # or "group"
```

Optionally override topic names with `topic_labels.yaml`.

---

## Usage

Run the full pipeline with:

```bash
zoteroautotagger
```

This will:
1. Generate topics with BERTopic
2. Apply readable labels (optional)
3. Push tags to Zotero

Make sure your YAML files are populated and renamed (remove `.example`).

**Note: This will create new tags in your Zotero library. If you want to do a dry run and inspect the results manually before pushing to Zotero, then run the tagging and topic modeling modules separately.** 

---

## 📝 License

MIT License
