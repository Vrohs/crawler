import argparse
from repo import analyze_repository

def main():
    parser = argparse.ArgumentParser(description="Project Analysis Tool")
    parser.add_argument("repo_url", help="GitHub or GitLab repository URL")
    parser.add_argument("--output", default="report.md", help="Output markdown report file")
    args = parser.parse_args()
    analyze_repository(args.repo_url, args.output)
