import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

# Load API keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GEMINI_API_KEY)

# Define a prompt template for fixing code
fix_prompt = PromptTemplate(
    input_variables=["code", "bugs"],
    template="The following code has these issues:\n{bugs}\n\nFix the code and provide the corrected version:\n\n{code}"
)

fix_chain = LLMChain(llm=llm, prompt=fix_prompt)

def generate_fixes(bug_reports, files):
    fixes = {}
    for filename, bugs in bug_reports.items():
        if bugs.strip():  # Check if there are actual bug reports
            response = fix_chain.invoke({"code": files[filename], "bugs": bugs})
            fixes[filename] = response["text"]  # Gemini returns response as a dictionary
    return fixes
