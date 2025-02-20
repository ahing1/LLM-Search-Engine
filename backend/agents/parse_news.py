from newspaper import Article

def extract_full_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return {"title": article.title, "content": article.text, "authors": article.authors}
