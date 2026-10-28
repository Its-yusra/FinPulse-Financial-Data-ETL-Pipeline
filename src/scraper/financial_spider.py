
import scrapy


class FinancialSpider(scrapy.Spider):
    name = "financial_spider"

    # Public sample page for practicing web scraping.
    start_urls = [
        "https://books.toscrape.com/"
    ]

    def parse(self, response):
        for item in response.css("article.product_pod"):
            title = item.css("h3 a::attr(title)").get()
            price = item.css(".price_color::text").get()
            availability = item.css(
                ".availability::text"
            ).getall()

            yield {
                "title": title,
                "price": price,
                "availability": " ".join(
                    text.strip() for text in availability
                ).strip(),
                "source_url": response.url,
            }

        next_page = response.css(
            "li.next a::attr(href)"
        ).get()

        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse
            )
