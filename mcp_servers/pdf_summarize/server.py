import os
import requests
import tempfile
import pymupdf
import litellm
import traceback
from typing import Dict
from fastmcp import FastMCP

mcp = FastMCP("pdf-summarize")

@mcp.tool()
def pdf_summarize(pdf_url: str) -> Dict[str, str]:
    try:
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return "Could not download PDF"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        os.remove(tmp_path)

        if not text.strip():
            return "No text found in PDF"

        summary = generate_summary(text)
        return summary

    except Exception as e:
        return str(e)


def extract_text_from_pdf(path) -> str:
    """Extract text from PDFs using PyMuPDF"""

    doc = PyMuPDF.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_summary(text: str) -> str:
    """Generates summary from PDF text"""
    try:
        messages = [
            {"role": "system", "content": "You are an expert at summarizing PDFs, return a short summary for the following content. Don't generate markdown!"},
            {"role": "user", "content": text}
        ]
        response = litellm.completion(
            model=os.getenv("MODEL_NAME"),
            messages=messages,
            stream=True,
        )
        return response

    except:
        print("❌ LLM call failed!")
        traceback.print_exc()