import arxiv
from backend.utils.db import save_article

def fetch_arxiv_papers(query="artificial intelligence", max_results=10):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    client = arxiv.Client()
    papers = []
    for paper in client.results(search):
        paper_data = {
            "title": paper.title,
            "abstract": paper.summary,
            "url": paper.entry_id,
            "authors": [author.name for author in paper.authors],
            "published": paper.published.strftime("%Y-%m-%d")
        }
        papers.append(paper_data)
        save_article(paper_data["title"], paper_data["url"], paper_data["abstract"], "arXiv")
    
    return papers

fetch_arxiv_papers()