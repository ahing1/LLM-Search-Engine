import scrapy

class AINewsSpider(scrapy.Spider):
    name = "ai_news"
    start_urls = [
        "https://www.technologyreview.com/topic/artificial-intelligence/",
        "https://venturebeat.com/category/ai/",
    ]

    def parse(self, response):
        for article in response.css("article"):
            yield {
                "title": article.css("h2 a::text").get(),
                "url": response.urljoin(article.css("h2 a::attr(href)").get()),
                "content": article.css("p::text").get(),
                "date": article.css("time::attr(datetime)").get(),
            }
