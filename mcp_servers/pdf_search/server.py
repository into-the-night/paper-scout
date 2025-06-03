from typing import Dict
import httpx
import xml.etree.ElementTree as ET
from fastmcp import FastMCP

ARXIV_API_URL = "http://export.arxiv.org/api/query"
mcp = FastMCP("paper-search")

@mcp.tool()
async def paper_search(query: str, max_results: int) -> Dict[str, str]:
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(ARXIV_API_URL, params=params)
        papers = parse_arxiv_response(response.text)
    return {"results": papers}


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

if __name__ == "__main__":
    mcp.run()


