import semanticscholar as sch
from semanticscholar import SemanticScholar, SemanticScholarException
from typing import List, Dict, Any

def initialize_client() -> SemanticScholar:
    """Initialize the SemanticScholar client with timeout."""
    return SemanticScholar(timeout=10)

def search_papers(client: SemanticScholar, query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search for papers using a query string."""
    results = client.search_paper(query, limit=limit)
    papers = []
    
    for paper in results:
        try:
            papers.append({
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
            })
        except Exception as e:
            continue
    
    return papers

def get_paper_details(client: SemanticScholar, paper_id: str) -> Any:
    """Get details of a specific paper."""
    return client.get_paper(paper_id)

def get_author_details(client: SemanticScholar, author_id: str) -> Any:
    """Get details of a specific author."""
    return client.get_author(author_id)

def get_citations_and_references(paper: Any) -> Dict[str, Any]:
    """Get citations and references for a paper."""
    return {
        "citations": paper.citations if hasattr(paper, 'citations') else [],
        "references": paper.references if hasattr(paper, 'references') else []
    }

def main():
    try:
        # Initialize the client
        client = initialize_client()

        # Search for papers
        search_results = search_papers(client, "machine learning")
        print(f"Search results: {search_results[:2]}")  # Print first 2 results

        # Get paper details
        if search_results:
            paper_id = search_results[0]['paperId']
            paper = get_paper_details(client, paper_id)
            print(f"Paper details: {paper}")

            # Get citations and references
            citations_refs = get_citations_and_references(paper)
            print(f"Citations: {citations_refs['citations'][:2]}")  # Print first 2 citations
            print(f"References: {citations_refs['references'][:2]}")  # Print first 2 references

        # Get author details
        author_id = "1741101"  # Example author ID
        author = get_author_details(client, author_id)
        print(f"Author details: {author}")

    except SemanticScholarException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()