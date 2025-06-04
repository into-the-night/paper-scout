from typing import Dict
from fastmcp import FastMCP
import arxiv

arxiv_client = arxiv.Client()
mcp = FastMCP("pdf_search")

@mcp.tool()
async def pdf_search(query: str, max_results: int) -> Dict[str, str]:
    try:
        search = arxiv.Search(
            query = query,
            max_results = int(max_results),
            sort_by = arxiv.SortCriterion.SubmittedDate
        )
        results = arxiv_client.results(search)
        papers = parse_arxiv_response(results)
        return {"results": papers}
    
    except Exception as e:
        return {"error": "An error occured while searching papers"}


def parse_arxiv_response(results):
    """Parse arXiv responses to required format"""
    results = list(results)
    formatted_results = []

    for result in results:
        formatted_results.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.pdf_url if hasattr(result, "pdf_url") else result.entry_id,
            "authors": result.authors
        })

    return formatted_results

if __name__ == "__main__":
    mcp.run(transport="stdio")