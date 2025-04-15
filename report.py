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
        'guidelines': doc_info['guidelines']
    }
    return template.render(**summary)

REPORT_TEMPLATE = '''
# Project Analysis Report: {{ repo_name }}

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
- Ensure consistent naming conventions across all files.
- Add or improve docstrings and comments for better maintainability.
- Follow documented setup and workflow instructions for contributions.
- Add more tests or clarify testing procedures if missing.

---
**Summary View:**
- Languages: {{ languages | map(attribute=0) | join(", ") }}
- Main Tech: {{ tech_stack | join(", ") }}
- Key Docs: {{ docs.keys() | join(", ") }}
'''
