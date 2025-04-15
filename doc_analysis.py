import os
import re

def extract_docs(repo_path, file_list):
    docs = {}
    for doc_file in [f for f in file_list if os.path.basename(f).lower() in ["readme.md", "contributing.md", "contributing.rst", "readme.rst"]]:
        with open(os.path.join(repo_path, doc_file), 'r', encoding='utf-8', errors='ignore') as f:
            docs[os.path.basename(doc_file).lower()] = f.read()
    guidelines = {}
    if "contributing.md" in docs:
        guidelines = parse_contributing(docs["contributing.md"])
    elif "readme.md" in docs:
        guidelines = parse_contributing(docs["readme.md"])
    return {
        "docs": docs,
        "guidelines": guidelines
    }

def parse_contributing(text):
    setup = extract_section(text, ["setup", "installation", "install"])
    workflow = extract_section(text, ["workflow", "contribute", "pull request", "development"])
    testing = extract_section(text, ["test", "testing", "run tests"])
    return {
        "setup": setup,
        "workflow": workflow,
        "testing": testing
    }

def extract_section(text, keywords):
    pattern = r"(^#+.*(?:{}).*$)(.*?)(?=^#|\Z)".format("|".join(keywords))
    matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    return [m[1].strip() for m in matches] if matches else []
