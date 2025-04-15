import os
import re

def extract_docs(repo_path, file_list):
    docs = {}
    for doc_file in [f for f in file_list if os.path.basename(f).lower() in ["readme.md", "contributing.md", "contributing.rst", "readme.rst"] or f.lower().startswith("docs/") or f.lower().startswith("doc/")]:
        try:
            with open(os.path.join(repo_path, doc_file), 'r', encoding='utf-8', errors='ignore') as f:
                docs[os.path.basename(doc_file).lower()] = f.read()
        except Exception:
            continue
    guidelines = extract_guidelines(docs)
    quick_start = extract_quick_start(docs)
    build_commands, test_commands = extract_build_test_commands(repo_path, file_list)
    workflow = extract_workflow(docs)
    pitfalls = extract_pitfalls(docs)
    return {
        "docs": docs,
        "guidelines": guidelines,
        "quick_start": quick_start,
        "build_commands": build_commands,
        "test_commands": test_commands,
        "workflow": workflow,
        "pitfalls": pitfalls
    }

def extract_guidelines(docs):
    for key in ["contributing.md", "readme.md"]:
        if key in docs:
            return parse_contributing(docs[key])
    return {}

def extract_quick_start(docs):
    for key in ["readme.md", "contributing.md"]:
        if key in docs:
            return extract_section(docs[key], ["quick start", "getting started", "usage", "how to run", "how to contribute"])
    return []

def extract_build_test_commands(repo_path, file_list):
    build_cmds = set()
    test_cmds = set()
    for f in file_list:
        path = os.path.join(repo_path, f)
        if os.path.basename(f) == "package.json":
            try:
                import json
                with open(path, 'r', encoding='utf-8', errors='ignore') as pkg:
                    data = json.load(pkg)
                    scripts = data.get("scripts", {})
                    for k, v in scripts.items():
                        if "build" in k:
                            build_cmds.add(f"npm run {k}")
                        if "test" in k:
                            test_cmds.add(f"npm run {k}")
            except Exception:
                continue
        if os.path.basename(f).lower() == "makefile":
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as mk:
                    for line in mk:
                        if re.match(r"^build:", line):
                            build_cmds.add("make build")
                        if re.match(r"^test:", line):
                            test_cmds.add("make test")
            except Exception:
                continue
        if os.path.basename(f) in ["setup.py", "pyproject.toml"]:
            build_cmds.add("python setup.py build")
            test_cmds.add("python setup.py test")
    return list(build_cmds), list(test_cmds)

def extract_workflow(docs):
    for key in docs:
        if "pull request" in docs[key].lower() or "ci" in docs[key].lower() or "workflow" in docs[key].lower():
            return extract_section(docs[key], ["workflow", "pull request", "ci", "review", "branch"])
    return []

def extract_pitfalls(docs):
    pitfalls = []
    for key in docs:
        pitfalls += extract_section(docs[key], ["pitfall", "troubleshoot", "warning", "caution", "gotcha", "note"])
    return pitfalls

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
