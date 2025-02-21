from store import embed_text


def search_similar_documents(query, top_k=5):
    query_vector = embed_text(query)
    results = index.query(query_vector, top_k=top_k, include_metadata=True)
    return results["matches"]

query = "How is AI used in healthcare?"
print(search_similar_documents(query))
