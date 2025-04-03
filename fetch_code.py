import os
import github3
from config import GITHUB_TOKEN

def fetch_github_repo(repo_name, branch="main"):
    gh = github3.login(token=GITHUB_TOKEN)
    repo = gh.repository(*repo_name.split("/"))
    
    files = {}
    for file in repo.directory_contents("", ref=branch):
        if file.name.endswith((".py", ".js")):  
            files[file.name] = file.content()
    
    return files

def fetch_local_code(directory):
    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith((".py", ".js")):
                with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
                    files[filename] = f.read()
    return files
