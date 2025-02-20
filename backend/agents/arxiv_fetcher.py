import arxiv

def fetch_arxiv_papers(query="artificial intelligence", max_results=10):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for paper in search.results():
        papers.append({
            "title": paper.title,
            "abstract": paper.summary,
            "url": paper.entry_id,
            "authors": [author.name for author in paper.authors],
            "published": paper.published.strftime("%Y-%m-%d")
        })
    return papers
