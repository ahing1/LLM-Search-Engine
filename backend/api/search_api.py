from fastapi import FastAPI, Query
from backend.search.hybrid_search import hybrid_search

app = FastAPI()

@app.get("/search/")
def search(q: str = Query(..., description="Search query"), top_k: int = 5):
    """API endpoint for hybrid search"""
    results = hybrid_search(q, top_k=top_k)
    return {"query": q, "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
