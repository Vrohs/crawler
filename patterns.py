import collections
import os
import re

def detect_languages_and_stack(repo_path, file_list):
    ext_lang = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.java': 'Java', '.rb': 'Ruby', '.go': 'Go',
        '.cpp': 'C++', '.c': 'C', '.cs': 'C#', '.php': 'PHP', '.rs': 'Rust', '.swift': 'Swift', '.kt': 'Kotlin',
        '.m': 'Objective-C', '.scala': 'Scala', '.sh': 'Shell', '.pl': 'Perl', '.r': 'R', '.dart': 'Dart',
        '.html': 'HTML', '.css': 'CSS', '.json': 'JSON', '.yml': 'YAML', '.yaml': 'YAML', '.xml': 'XML',
    }
    lang_count = collections.Counter()
    for f in file_list:
        ext = os.path.splitext(f)[1].lower()
        if ext in ext_lang:
            lang_count[ext_lang[ext]] += 1
    main_langs = lang_count.most_common()
    tech_stack = set()
    for f in file_list:
        if 'requirements.txt' in f or 'Pipfile' in f:
            tech_stack.add('Python')
        if 'package.json' in f:
            tech_stack.add('Node.js')
        if 'pom.xml' in f or 'build.gradle' in f:
            tech_stack.add('Java')
        if 'Gemfile' in f:
            tech_stack.add('Ruby')
        if 'go.mod' in f:
            tech_stack.add('Go')
    return main_langs, list(tech_stack)

def analyze_code_patterns(repo_path, file_list, lang_stats):
    patterns = {}
    for lang, _ in lang_stats:
        if lang == 'Python':
            patterns['Python'] = analyze_python_patterns(repo_path, file_list)
        if lang == 'JavaScript':
            patterns['JavaScript'] = analyze_js_patterns(repo_path, file_list)
    patterns['File Organization'] = analyze_file_organization(repo_path, file_list)
    return patterns

def analyze_python_patterns(repo_path, file_list):
    import ast
    naming = collections.Counter()
    var_naming = collections.Counter()
    param_naming = collections.Counter()
    docstrings = 0
    comments = 0
    total_defs = 0
    indent_style = collections.Counter()
    line_lengths = []
    for f in file_list:
        if f.endswith('.py'):
            with open(os.path.join(repo_path, f), 'r', encoding='utf-8', errors='ignore') as src:
                lines = src.readlines()
                for line in lines:
                    if line.strip().startswith('#'):
                        comments += 1
                    if line.startswith(' '):
                        indent_style['spaces'] += 1
                    if line.startswith('\t'):
                        indent_style['tabs'] += 1
                    line_lengths.append(len(line.rstrip('\n')))
                src.seek(0)
                try:
                    tree = ast.parse(''.join(lines))
                except Exception:
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        total_defs += 1
                        if node.name.islower() and '_' in node.name:
                            naming['snake_case'] += 1
                        elif node.name[0].isupper():
                            naming['PascalCase'] += 1
                        elif '_' not in node.name:
                            naming['camelCase'] += 1
                        if ast.get_docstring(node):
                            docstrings += 1
                        for arg in node.args.args:
                            if arg.arg.islower() and '_' in arg.arg:
                                param_naming['snake_case'] += 1
                            elif arg.arg[0].isupper():
                                param_naming['PascalCase'] += 1
                            elif '_' not in arg.arg:
                                param_naming['camelCase'] += 1
                    if isinstance(node, ast.ClassDef):
                        if node.name[0].isupper():
                            naming['PascalCase'] += 1
                        else:
                            naming['other'] += 1
                        if ast.get_docstring(node):
                            docstrings += 1
                    if isinstance(node, ast.Assign):
                        for t in node.targets:
                            if hasattr(t, 'id'):
                                v = t.id
                                if v.islower() and '_' in v:
                                    var_naming['snake_case'] += 1
                                elif v[0].isupper():
                                    var_naming['PascalCase'] += 1
                                elif '_' not in v:
                                    var_naming['camelCase'] += 1
    avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
    return {
        'naming': dict(naming),
        'variable_naming': dict(var_naming),
        'parameter_naming': dict(param_naming),
        'docstrings': docstrings,
        'comments': comments,
        'total_defs': total_defs,
        'indent_style': dict(indent_style),
        'avg_line_length': avg_line_length
    }

def analyze_js_patterns(repo_path, file_list):
    naming = collections.Counter()
    var_naming = collections.Counter()
    comments = 0
    total_funcs = 0
    indent_style = collections.Counter()
    line_lengths = []
    for f in file_list:
        if f.endswith('.js'):
            with open(os.path.join(repo_path, f), 'r', encoding='utf-8', errors='ignore') as src:
                for line in src:
                    if re.match(r'function [a-zA-Z_][a-zA-Z0-9_]*', line):
                        total_funcs += 1
                        name = line.split()[1].split('(')[0]
                        if name[0].isupper():
                            naming['PascalCase'] += 1
                        elif '_' in name:
                            naming['snake_case'] += 1
                        else:
                            naming['camelCase'] += 1
                    var_match = re.match(r'(let|var|const) ([a-zA-Z_][a-zA-Z0-9_]*)', line)
                    if var_match:
                        v = var_match.group(2)
                        if v[0].isupper():
                            var_naming['PascalCase'] += 1
                        elif '_' in v:
                            var_naming['snake_case'] += 1
                        else:
                            var_naming['camelCase'] += 1
                    if '//' in line or line.strip().startswith('/*'):
                        comments += 1
                    if line.startswith(' '):
                        indent_style['spaces'] += 1
                    if line.startswith('\t'):
                        indent_style['tabs'] += 1
                    line_lengths.append(len(line.rstrip('\n')))
    avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
    return {
        'naming': dict(naming),
        'variable_naming': dict(var_naming),
        'comments': comments,
        'total_funcs': total_funcs,
        'indent_style': dict(indent_style),
        'avg_line_length': avg_line_length
    }

def analyze_file_organization(repo_path, file_list):
    ext_count = collections.Counter()
    dir_count = collections.Counter()
    file_sizes = []
    for f in file_list:
        ext = os.path.splitext(f)[1].lower()
        ext_count[ext] += 1
        dir_name = os.path.dirname(f).split(os.sep)[0] if os.path.dirname(f) else '.'
        dir_count[dir_name] += 1
        try:
            file_sizes.append(os.path.getsize(os.path.join(repo_path, f)))
        except Exception:
            continue
    return {
        'file_types': dict(ext_count),
        'top_dirs': dict(dir_count),
        'avg_file_size': sum(file_sizes) / len(file_sizes) if file_sizes else 0,
        'total_files': len(file_list)
    }
