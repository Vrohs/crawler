import jinja2

def generate_report(repo_name, lang_stats, tech_stack, code_patterns, doc_info):
    env = jinja2.Environment()
    template = env.from_string(REPORT_TEMPLATE)
    summary = {
        'repo_name': repo_name,
        'languages': lang_stats,
        'tech_stack': tech_stack,
        'code_patterns': code_patterns,
        'docs': doc_info['docs'],
        'guidelines': doc_info['guidelines'],
        'quick_start': doc_info.get('quick_start', []),
        'build_commands': doc_info.get('build_commands', []),
        'test_commands': doc_info.get('test_commands', []),
        'workflow': doc_info.get('workflow', []),
        'pitfalls': doc_info.get('pitfalls', [])
    }
    return template.render(**summary)

REPORT_TEMPLATE = '''
# Project Analysis Report: {{ repo_name }}

## Quick Start for Contributors
{% if quick_start %}
{% for step in quick_start %}- {{ step }}
{% endfor %}
{% else %}
- No explicit quick start found. See build and test commands below.
{% endif %}

### Build Commands
{% for cmd in build_commands %}- {{ cmd }}
{% endfor %}

### Test Commands
{% for cmd in test_commands %}- {{ cmd }}
{% endfor %}

### Workflow & PR Process
{% for w in workflow %}- {{ w }}
{% endfor %}

### Common Pitfalls & Notes
{% for p in pitfalls %}- {{ p }}
{% endfor %}

## Project Overview
- **Languages Detected:** {% for lang, count in languages %}{{ lang }} ({{ count }}) {% endfor %}
- **Tech Stack:** {{ tech_stack | join(", ") }}

## Coding Standards
{% for lang, patterns in code_patterns.items() %}
### {{ lang }}
- **Naming Conventions:**
    {% for style, count in patterns.get('naming', {}).items() %}
    - {{ style }}: {{ count }}
    {% endfor %}
- **Docstrings/Comments:**
    {% if patterns.get('docstrings') %}Docstrings: {{ patterns['docstrings'] }}{% endif %}
    {% if patterns.get('comments') %}Comments: {{ patterns['comments'] }}{% endif %}
- **Definitions/Functions:**
    {% if patterns.get('total_defs') %}Definitions: {{ patterns['total_defs'] }}{% endif %}
    {% if patterns.get('total_funcs') %}Functions: {{ patterns['total_funcs'] }}{% endif %}
{% endfor %}

## Documentation & Contribution Guidelines
{% for doc, content in docs.items() %}
### {{ doc }}
{{ content[:500] }}{% if content|length > 500 %}...{% endif %}
{% endfor %}

### Contribution Guidelines
- **Setup Instructions:**
    {% for s in guidelines.get('setup', []) %}- {{ s }}{% endfor %}
- **Workflow Requirements:**
    {% for w in guidelines.get('workflow', []) %}- {{ w }}{% endfor %}
- **Testing Procedures:**
    {% for t in guidelines.get('testing', []) %}- {{ t }}{% endfor %}

## Recommendations
- Follow the quick start and build/test steps above for local setup.
- Ensure consistent naming conventions across all files.
- Add or improve docstrings and comments for better maintainability.
- Follow documented setup and workflow instructions for contributions.
- Add more tests or clarify testing procedures if missing.
- Review common pitfalls and notes above before contributing.

---
**Summary View:**
- Languages: {{ languages | map(attribute=0) | join(", ") }}
- Main Tech: {{ tech_stack | join(", ") }}
- Key Docs: {{ docs.keys() | join(", ") }}
'''
