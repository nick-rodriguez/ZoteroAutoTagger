import os
import subprocess

def run_step(name, script_path):
    print(f"\n=== Running: {name} ===")
    result = subprocess.run(["python", script_path])
    if result.returncode != 0:
        print(f"{name} failed.")
        exit(1)
    print(f"{name} completed.\n")

def main():
    steps = [
        ("Run BERTopic Topic Modeling", "autotag_bert.py"),
        ("Label Topics with Descriptive Names", "label_topics.py"),
        ("Apply Tags to Zotero Library", "apply_zotero_tags.py")
    ]

    for name, script in steps:
        run_step(name, script)

    print("All steps completed successfully.")

if __name__ == "__main__":
    main()