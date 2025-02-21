import schedule
import time
from .parse_news import extract_full_article, get_ai_article_links
from .arxiv_fetcher import fetch_arxiv_papers
from backend.utils.db import save_article

def daily_scrape():
    """Fetches AI news and research papers, then saves them to the database."""
    print("Fetching AI article links...")
    article_links = get_ai_article_links()
    print(f"Found {len(article_links)} articles")

    if not article_links:
        print("No articles found. Skipping news scraping.")
    else:
        for link in article_links:
            try:
                article_data = extract_full_article(link)
                if article_data and article_data["content"].strip():  # Ensure article has content
                    save_article(article_data["title"], article_data["url"], article_data["content"], "News")
                    print(f"✅ Saved article: {article_data['title']}")
                else:
                    print(f"⚠️ Skipping empty article: {link}")
            except Exception as e:
                print(f"❌ Error processing article {link}: {e}")

    print("Fetching AI research papers...")
    try:
        ai_papers = fetch_arxiv_papers()
        if ai_papers:
            for paper in ai_papers:
                save_article(paper['title'], paper['url'], paper['abstract'], "ArXiv")
                print(f"✅ Saved paper: {paper['title']}")
        else:
            print("No AI research papers found.")
    except Exception as e:
        print(f"❌ Error fetching research papers: {e}")

# ✅ Run once immediately for testing
daily_scrape()

# ✅ Schedule future runs
schedule.every().day.at("06:00").do(daily_scrape)

print("✅ Scheduler is running. Next run at 06:00 AM daily.")

while True:
    schedule.run_pending()
    time.sleep(60)
