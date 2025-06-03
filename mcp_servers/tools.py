import xml.etree.ElementTree as ET
import PyMuPDF
import traceback
from llm.llm_client import LLM

def parse_arxiv_response(xml_text: str):
    """Parse arXiv responses to required format"""

    root = ET.fromstring(xml_text)
    ns = {'arxiv': 'http://arxiv.org/schemas/atom'}
    results = []

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text
                   for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        results.append({
            "title": title,
            "summary": summary,
            "url": url,
            "authors": authors
        })

    return results


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
        llm = LLM()
        response = llm.generate_response(messages, stream=True)
        return response

    except:
        print("❌ LLM call failed!")
        traceback.print_exc()
