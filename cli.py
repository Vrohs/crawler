import argparse
import os
from repo import analyze_repository

def main():
    parser = argparse.ArgumentParser(description="Project Analysis Tool")
    parser.add_argument("repo_url", help="GitHub or GitLab repository URL")
    args = parser.parse_args()
    cwd = os.getcwd()
    output_path = os.path.join(cwd, "report.md")
    analyze_repository(args.repo_url, output_path)
