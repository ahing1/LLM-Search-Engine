from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_ai_article_links():
    """Extracts AI article URLs from VentureBeat"""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://venturebeat.com/category/ai/")
    time.sleep(5)  # Allow JavaScript to load

    try:
        articles = driver.find_elements(By.CSS_SELECTOR, "article a")
        links = [article.get_attribute("href") for article in articles if article.get_attribute("href")]
    except Exception as e:
        print(f"Error extracting article links: {e}")
        links = []

    driver.quit()
    return links[:5]  # Limit to first 5 articles for testing

def extract_full_article(url):
    """Extracts the full content of an article"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)

    try:
        title = driver.find_element(By.TAG_NAME, "h1").text
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        content = "\n".join([p.text for p in paragraphs if p.text.strip()])
    except Exception as e:
        print(f"Error extracting article: {e}")
        title, content = "No title", "No content"

    driver.quit()
    return {"title": title, "content": content, "url": url}

