import schedule
import time
from parse_news import extract_full_article
from arxiv_fetcher import fetch_arxiv_papers
from utils.db import save_article

def daily_scrape():
    print("Fetching AI news...")
    ai_news = extract_full_article("https://venturebeat.com/category/ai/")
    print("Fetching AI research papers...")
    ai_papers = fetch_arxiv_papers()

    # Save to database
    for article in ai_news:
        save_article(article['title'], article['url'], article['content'], "News")
    
    for paper in ai_papers:
        save_article(paper['title'], paper['url'], paper['abstract'], "ArXiv")

# Run daily
schedule.every().day.at("06:00").do(daily_scrape)

while True:
    schedule.run_pending()
    time.sleep(60)
