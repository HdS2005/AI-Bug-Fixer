import os
import github3
import google.generativeai as genai
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

"""if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY! Check your .env file.")
if not GITHUB_ACCESS_TOKEN:
    raise ValueError("Missing GITHUB_ACCESS_TOKEN! Check your .env file.")"""

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-pro") 

# Connect to GitHub
try:
    github = github3.login(token=GITHUB_ACCESS_TOKEN)
    if not github:
        raise ValueError("GitHub authentication failed! Invalid token.")
except Exception as e:
    raise RuntimeError(f"GitHub authentication error: {e}")

def get_repo_code(owner, repo_name):
    """Fetch source code files from a GitHub repository."""
    repo = github.repository(owner, repo_name)
    if not repo:
        raise ValueError(f"Repository '{owner}/{repo_name}' not found!")

    files = {}
    valid_extensions = {".py", ".js", ".html", ".css"}

    try:
        try:
            branch = repo.branch("main")
        except github3.exceptions.NotFoundError:
            branch = repo.branch("master")  

        tree = repo.tree(branch.commit.sha, recursive=True)

        for entry in tree.tree:
            if any(entry.path.endswith(ext) for ext in valid_extensions):
                try:
                    file_content = repo.file_contents(entry.path)
                    files[entry.path] = file_content.decoded.decode("utf-8")
                except Exception as e:
                    print(f"Error reading {entry.path}: {e}")

    except Exception as e:
        print(f"Error fetching repo contents: {e}")

    return files

def find_bugs(code, file_extension):
    """Uses Google Gemini AI to find bugs and suggest fixes."""
    language_prompts = {
        ".py": "Find bugs and suggest fixes for this Python code:\n\n",
        ".js": "Find bugs and suggest fixes for this JavaScript code:\n\n",
        ".html": "Check for syntax errors and best practices in this HTML code:\n\n",
        ".css": "Check for syntax errors and best practices in this CSS code:\n\n"
    }

    prompt_prefix = language_prompts.get(file_extension, "Analyze and improve this code:\n\n")
    prompt = prompt_prefix + code

    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else "No response from AI."
    
    except Exception as e:
        print(f"Error analyzing code with Gemini AI: {e}")
        return "Error analyzing code."

def main():
    owner = "HdS2005"
    repo_name = "TREE-APP"

    print("Fetching repository files...")
    files = get_repo_code(owner, repo_name)
    
    if not files:
        print("No supported files found in the repository.")
        return

    for filename, code in files.items():
        file_extension = os.path.splitext(filename)[-1]
        print(f"\nScanning {filename}...")
        bugs = find_bugs(code, file_extension)
        print(f"\nIssues found in {filename}:\n{'-'*40}\n{bugs}\n{'-'*40}")

if __name__ == "__main__":
    main()
