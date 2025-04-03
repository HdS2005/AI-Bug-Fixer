from github3 import GitHub
from config import GITHUB_TOKEN

def create_pull_request(repo_name, fixed_code, branch="bug-fix-ai"):
    gh = GitHub(token=GITHUB_TOKEN)
    repo = gh.repository(*repo_name.split("/"))
    
    # Create a new branch
    main_branch = repo.branch("main")
    repo.create_ref(f"refs/heads/{branch}", main_branch.commit.sha)

    # Commit changes
    for filename, new_code in fixed_code.items():
        repo.file_contents(filename).update(
            f"AI-generated fix for {filename}",
            new_code,
            branch=branch,
        )
    
    # Create PR
    repo.create_pull(
        title="AI-generated Bug Fixes",
        base="main",
        head=branch,
        body="This PR contains automatic bug fixes detected and corrected by AI."
    )
