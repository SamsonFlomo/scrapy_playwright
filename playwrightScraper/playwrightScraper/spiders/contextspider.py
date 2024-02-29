import scrapy
import os
from scrapy_playwright.page import PageMethod
from PyPDF2 import PdfMerger
from playwrightScraper.items import ContextNewsItem


class ContextspiderSpider(scrapy.Spider):
    name = "contextspider"
    allowed_domains = ["www.context.news"]

    def __init__(self, *args, **kwargs):
        super(ContextspiderSpider, self).__init__(*args, **kwargs)
        self.pdfs = []
        self.pdf_directory = "others/files_json_csv_txt_pdf/contextspider/"
        os.makedirs(self.pdf_directory, exist_ok=True)

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
                        path=f"{self.pdf_directory}contextspider_home_page.pdf",
                        scale=1
                    ),
                ],
            }
        )

    def parse(self, response):
        latest_news = response.xpath(
            "//main/section[contains(@class, 'Hero')]/div[last()]/div/div")

        for index, news in enumerate(latest_news, start=1):
            relative_url = news.xpath("article/div[last()]/a/@href").get()
            news_url = response.urljoin(relative_url)

            # Save the page as PDF and add it to the list
            pdf_path = f"../{self.pdf_directory}ContextNews_{index}.pdf"
            self.pdfs.append(pdf_path)

            yield scrapy.Request(
                news_url,
                callback=self.parse_news_page,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod(
                            "wait_for_selector",
                            ".row",
                            timeout=60000
                        ),
                        PageMethod(
                            "pdf",
                            path=pdf_path,
                            scale=1
                        ),
                    ]
                }
            )

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

    def closed(self, reason):
        # Combine all PDFs into a single file
        combined_pdf_path = f"../{self.pdf_directory}Combined_ContextNews.pdf"
        pdf_merger = PdfMerger()
        for pdf_path in self.pdfs:
            if pdf_path:
                pdf_merger.append(pdf_path)
            else:
                print("##### Invalid file or folder. #####")
        pdf_merger.write(combined_pdf_path)
        pdf_merger.close()
