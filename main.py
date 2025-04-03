from fetch_code import fetch_github_repo, fetch_local_code
from bug_finder import detect_bugs
from fix_generator import generate_fixes
from github_actions import create_pull_request

USE_GITHUB = True
REPO_NAME = "user/repository-name"
LOCAL_DIRECTORY = "/path/to/local/code"

if USE_GITHUB:
    code_files = fetch_github_repo(REPO_NAME)
else:
    code_files = fetch_local_code(LOCAL_DIRECTORY)

bug_reports = detect_bugs(code_files)
fixed_code = generate_fixes(bug_reports, code_files)

if USE_GITHUB:
    create_pull_request(REPO_NAME, fixed_code)
else:
    for filename, code in fixed_code.items():
        with open(f"fixed_{filename}", "w", encoding="utf-8") as f:
            f.write(code)

print("Bug detection & fixing complete!")
