from setuptools import setup

setup(
    name='project-analyze',
    version='0.1.0',
    py_modules=['cli', 'repo', 'patterns', 'doc_analysis', 'report'],
    install_requires=[
        'gitpython',
        'PyGithub',
        'python-gitlab',
        'pandas',
        'jinja2',
        'markdown',
        'ruff',
        'pylint',
        'matplotlib',
        'seaborn',
        'beautifulsoup4',
        'lxml',
    ],
    entry_points={
        'console_scripts': [
            'project-analyze=cli:main',
        ],
    },
    author='Your Name',
    description='Project Analysis Tool for code standards and documentation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
