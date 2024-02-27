import scrapy
from scrapy_playwright.page import PageMethod
from playwrightScraper.items import ContextNewsItem


class ContextspiderSpider(scrapy.Spider):
    name = "contextspider"
    allowed_domains = ["www.context.news"]

    def start_requests(self):
        url = "https://www.context.news"

        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod(
                        "wait_for_selector",
                        "article div:last-child a",
                        timeout=60000
                    ),
                    PageMethod(
                        "screenshot",
                        path="others/screen_shots/ContextNews_page.jpg",
                        full_page=True,
                        omit_background=True
                    ),
                    PageMethod(
                        "pdf",
                        path="others/files_json_csv_txt_pdf/scraping_club/output.pdf",
                        scale=1
                    ),

                ],
            }
        )

    def parse(self, response):
        latestNews = response.xpath(
                "//main/section[contains(@class, 'Hero')]/div[last()]/div/div")

        for news in latestNews:
            relative_url = news.xpath("article/div[last()]/a/@href").get()
            news_url = response.urljoin(relative_url)

            yield scrapy.Request(
                    news_url,
                    callback=self.parse_news_page,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod(
                            "click", "article div:last-child a"
                            ),
                            PageMethod(
                                "wait_for_selector",
                                "article div:last-child a",
                                timeout=60000
                                ),

                            ]})

    def parse_news_page(self, response):
        news_item = ContextNewsItem()

        news_item['explainer'] = response.xpath(
                "//div[contains(@class, 'author')]/@title"
                ).get()
        news_item['published'] = response.xpath(
                "//div[contains(@class, 'author__info')]/p[last()]/text()"
                ).get()
        news_item['category'] = response.xpath(
                "//a[contains(@class, 'spacer__tab')]/text()"
                ).get()
        news_item['title'] = response.xpath(
                "//div[contains(@class, 'article__header')]/h1/text()"
                ).get()
        news_item['context'] = response.xpath(
                "//div[contains(@class, 'ArticleSummary')]/p/text()"
                ).get()
        news_item['content'] = response.xpath(
                "//div[contains(@class, 'ArticleText')]/p/text()"
                ).getall()
        news_item['url'] = response.url

        yield news_item
