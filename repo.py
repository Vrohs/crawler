import os
def analyze_repository(repo_url, output_path):
    from git import Repo
    import tempfile
    import shutil
    import patterns
    import doc_analysis
    import report
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(repo_url, temp_dir)
        repo_name = os.path.basename(repo_url.rstrip('/').replace('.git',''))
        file_list = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, temp_dir)
                file_list.append(rel_path)
        lang_stats, tech_stack = patterns.detect_languages_and_stack(temp_dir, file_list)
        code_patterns = patterns.analyze_code_patterns(temp_dir, file_list, lang_stats)
        doc_info = doc_analysis.extract_docs(temp_dir, file_list)
        report_content = report.generate_report(repo_name, lang_stats, tech_stack, code_patterns, doc_info)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
    finally:
        shutil.rmtree(temp_dir)
