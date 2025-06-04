import os
import requests
import tempfile
import pymupdf
import openai
import traceback
from typing import Dict
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
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
        return {"result": summary}

    except Exception as e:
        return {"error": "An error has occurred"}
    

def extract_text_from_pdf(path) -> str:
    """Extract text from PDFs using PyMuPDF"""

    doc = pymupdf.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_summary(text: str) -> str:
    """Generates summary from PDF text"""
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        api_base = "https://openrouter.ai/api/v1"
        model = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")

        messages = [
            {"role": "system", "content": "You are an expert at summarizing PDFs, return a short summary for the following content. Don't generate markdown!"},
            {"role": "user", "content": text}
        ]
        client = openai.OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        # Extract the summary text
        return response.choices[0].message.content

    except Exception as e:
        traceback.print_exc()
        return str(e)