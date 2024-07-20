from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from tqdm import tqdm
import time
import os
import json

load_dotenv()
access_token = os.environ.get("ACCESS_TOKEN")

SEPARATORS = [
    "\n\n",
    "\n",
    " ",
    "",
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    add_start_index=True,
    strip_whitespace=True,
    separators=SEPARATORS,
)

template = """
You are a factual language model trained to convert bodies of text into a single, well-formed question and its corresponding answer.
When processing the text, prioritize factual information and avoid making claims of sentience or consciousness.
Present the question and answer in a single JSON object. 
context: {context}
"""
prompt = PromptTemplate.from_template(template)

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    model_kwargs={"max_length": 128},
    temperature=0.5,
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
    files = []
    if os.path.exists(path):
        files.extend(os.listdir(path))
    return files


def get_text(pdf_path):
    path = "./pdfs/A_Random_Walk_Down_Wall_Street.pdf"
    reader_obj = open(path, "rb")
    pdf = PdfReader(reader_obj)
    book = [Document(page_content=page.extract_text()) for page in pdf.pages]
    reader_obj.close()
    return book


outputs = []
files = get_pdf_list("./pdfs")

for pdf in tqdm(files, desc="total pdfs"):
    pdf_path = "./pdfs/" + pdf
    book = get_text(pdf_path)
    proccessed_docs = []
    for page in book:
        proccessed_docs += text_splitter.split_documents([page])
    for chunk in tqdm(proccessed_docs, desc="total chunks"):
        output = llm_chain.invoke({"context": chunk})
        if is_json(output):
            outputs.append(output)
        time.sleep(12)

with open("outputs.json", "w") as f:
    json.dump(outputs, f)
