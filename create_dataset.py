import json
import os
import time

from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub.utils._errors import HfHubHTTPError
from PyPDF2 import PdfReader
from PyPDF2.errors import EmptyFileError, PdfReadError


load_dotenv()
access_token = os.environ.get("ACCESS_TOKEN")

template = """
Extract a key concept from the provided text and convert it into a well-formed question and its corresponding detailed answer. 
Ensure the question is directly related to finance or cryptocurrency.
The answer should be factual, concise, and provide a clear explanation of the concept. 
Avoid making claims of sentience or consciousness.
Present question and answer in a single JSON object.

context: {context} 
"""
prompt = PromptTemplate.from_template(template)
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=4096,
    temperature=0.4,
    huggingfacehub_api_token=access_token,
)
llm_chain = prompt | llm


def is_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


def get_pdf_list(path):
    if os.path.exists(path):
        return [f for f in os.listdir(path) if f.endswith(".pdf")]
    return FileNotFoundError


def get_text(pdf_path):
    with open(pdf_path, "rb") as reader_obj:
        try:
            pdf = PdfReader(reader_obj)
            book = [Document(page_content=page.extract_text()) for page in pdf.pages]
            return book
        except EmptyFileError as e:
            print(f"[ERROR] {e}")
            return None
        except PdfReadError as e:
            print(f"[ERROR] {e}")
            return None


def get_checkpoint():
    if os.path.exists("checkpoint.json"):
        with open("checkpoint.json", "r") as chkpoint:
            checkpoint = json.load(chkpoint)
            print("Loading last checkpoint")
    else:
        checkpoint = {"file": 0, "page": 0}
    return checkpoint


def save_checkpoint(output, i, j):
    if is_json(output):
        with open("outputs.jsonl", "a") as f:
            f.write(output + ",\n")
    checkpoint = {"file": i, "page": j}
    with open("checkpoint.json", "w") as f:
        json.dump(checkpoint, f)


files = get_pdf_list("./pdfs")
checkpoint = get_checkpoint()
flag = False

for i in range(checkpoint["file"], len(files)):
    pdf_path = os.path.join("./pdfs", files[i])
    book = get_text(pdf_path)
    if not book:
        continue
    for j in range(checkpoint["page"], len(book)):
        print(f"[INFO] file num: {i}, page num: {j}")
        try:
            output = llm_chain.invoke({"context": book[j]})
            save_checkpoint(output, i, j)
            time.sleep(5.5)
        except HfHubHTTPError as e:
            print(f"[ERROR] {e}")
            flag = True
            break
    if flag:
        break
    checkpoint["page"] = 0

# TODO: use a different prompt template
