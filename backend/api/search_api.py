from fastapi import FastAPI, Query
from backend.search.hybrid_search import hybrid_search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Allow Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

search_history = set()

@app.get("/search/")
def search(q: str = Query(..., description="Search query"), top_k: int = 5):
    """API endpoint for hybrid search"""
    results = hybrid_search(q, top_k=top_k)
    
    if results:
        search_history.add(q.lower())
    
    return {"query": q, "results": results}

@app.get("/suggest/")
def suggest(q: str = Query("", description="Partial search query")):
    """Suggest search queries based on the search history"""
    suggestions = [query for query in search_history if query.startswith(q.lower())]
    return {"suggestions": suggestions[:5]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
