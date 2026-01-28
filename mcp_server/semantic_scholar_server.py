from typing import Any, List, Dict
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from semantic_scholar_search import (
    initialize_client, 
    search_papers, 
    get_paper_details, 
    get_author_details, 
    get_citations_and_references
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server
mcp = FastMCP("semanticscholar")

# Initialize SemanticScholar client
client = initialize_client()

@mcp.tool()
async def search_semantic_scholar(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for papers on Semantic Scholar using a query string.
    
    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)
    
    Returns:
        List of dictionaries containing paper information
    """
    logging.info(f"Searching for papers with query: {query}, num_results: {num_results}")
    try:
        results = await asyncio.to_thread(search_papers, client, query, num_results)
        return results
    
    except Exception as e:
        logging.error(f"Search error: {str(e)}")
        return [{"error": f"An error occurred while searching: {str(e)}"}]

@mcp.tool()
async def get_semantic_scholar_paper_details(paper_id: str) -> Dict[str, Any]:
    """
    Get details of a specific paper on Semantic Scholar.
    
    Args:
        paper_id: ID of the paper (can be Semantic Scholar ID, DOI, or ArXiv ID)
    
    Returns:
        Dictionary containing paper details
    """
    logging.info(f"Fetching paper details for paper ID: {paper_id}")
    try:
        paper = await asyncio.to_thread(get_paper_details, client, paper_id)
        return {
            "paperId": paper.paperId if hasattr(paper, 'paperId') else None,
            "title": paper.title if hasattr(paper, 'title') else "Unknown",
            "abstract": paper.abstract if hasattr(paper, 'abstract') else None,
            "year": paper.year if hasattr(paper, 'year') else None,
            "authors": [
                {"name": author.name, "authorId": author.authorId} 
                for author in (paper.authors if hasattr(paper, 'authors') and paper.authors else [])
            ],
            "url": paper.url if hasattr(paper, 'url') else None,
            "venue": paper.venue if hasattr(paper, 'venue') else None,
            "publicationTypes": paper.publicationTypes if hasattr(paper, 'publicationTypes') else [],
            "citationCount": paper.citationCount if hasattr(paper, 'citationCount') else 0
        }
    except Exception as e:
        logging.error(f"Paper details error: {str(e)}")
        return {"error": f"An error occurred while fetching paper details: {str(e)}"}

@mcp.tool()
async def get_semantic_scholar_author_details(author_id: str) -> Dict[str, Any]:
    """
    Get details of a specific author on Semantic Scholar.
    
    Args:
        author_id: ID of the author
    
    Returns:
        Dictionary containing author details
    """
    logging.info(f"Fetching author details for author ID: {author_id}")
    try:
        author = await asyncio.to_thread(get_author_details, client, author_id)
        return {
            "authorId": author.authorId if hasattr(author, 'authorId') else None,
            "name": author.name if hasattr(author, 'name') else "Unknown",
            "url": author.url if hasattr(author, 'url') else None,
            "affiliations": author.affiliations if hasattr(author, 'affiliations') else [],
            "paperCount": author.paperCount if hasattr(author, 'paperCount') else 0,
            "citationCount": author.citationCount if hasattr(author, 'citationCount') else 0,
            "hIndex": author.hIndex if hasattr(author, 'hIndex') else 0
        }
    except Exception as e:
        logging.error(f"Author details error: {str(e)}")
        return {"error": f"An error occurred while fetching author details: {str(e)}"}

@mcp.tool()
async def get_semantic_scholar_citations_and_references(paper_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get citations and references for a specific paper on Semantic Scholar.
    
    Args:
        paper_id: ID of the paper
    
    Returns:
        Dictionary containing lists of citations and references
    """
    logging.info(f"Fetching citations and references for paper ID: {paper_id}")
    try:
        paper = await asyncio.to_thread(get_paper_details, client, paper_id)
        citations_refs = await asyncio.to_thread(get_citations_and_references, paper)
        
        citations_list = []
        for citation in citations_refs.get("citations", []):
            try:
                citations_list.append({
                    "paperId": citation.paperId if hasattr(citation, 'paperId') else None,
                    "title": citation.title if hasattr(citation, 'title') else "Unknown",
                    "year": citation.year if hasattr(citation, 'year') else None,
                    "authors": [
                        {"name": author.name, "authorId": author.authorId} 
                        for author in (citation.authors if hasattr(citation, 'authors') and citation.authors else [])
                    ]
                })
            except Exception:
                continue
        
        references_list = []
        for reference in citations_refs.get("references", []):
            try:
                references_list.append({
                    "paperId": reference.paperId if hasattr(reference, 'paperId') else None,
                    "title": reference.title if hasattr(reference, 'title') else "Unknown",
                    "year": reference.year if hasattr(reference, 'year') else None,
                    "authors": [
                        {"name": author.name, "authorId": author.authorId} 
                        for author in (reference.authors if hasattr(reference, 'authors') and reference.authors else [])
                    ]
                })
            except Exception:
                continue
        
        return {
            "citations": citations_list,
            "references": references_list
        }
    except Exception as e:
        logging.error(f"Citations/references error: {str(e)}")
        return {
            "citations": [{"error": f"An error occurred while fetching citations and references: {str(e)}"}],
            "references": []
        }

if __name__ == "__main__":
    logging.info("Starting Semantic Scholar MCP server")
    mcp.run(transport='stdio')
