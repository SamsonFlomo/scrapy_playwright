import scrapy
import os
from scrapy_playwright.page import PageMethod
from playwrightScraper.items import ScrapingClubItem

scrolling_script = """
    const numscrolls = 8
    let scrollCount = 0

    // scroll down and then wait for 0.5s
    const scrollInterval = setInterval(() => {
      window.scrollTo(0, document.body.scrollHeight)
      scrollCount++

      if (scrollCount === numScrolls) {
        clearInterval(scrollInterval)
      }
    }, 600)
"""

class ScrapingClubSpider(scrapy.Spider):
    name = "scraping_club"
    allowed_domains = ["scrapingclub.com"]

    def __init__(self, *args, **kwargs):
        super(ScrapingClubSpider, self).__init__(*args, **kwargs)
        self.pdfs = []
        self.pdf_directory = "others/files_json_csv_txt_pdf/scraping_club/"
        os.makedirs(self.pdf_directory, exist_ok=True)

    def start_requests(self):
        url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("evaluate", scrolling_script),
                    PageMethod(
                        "wait_for_selector",
                        ".post:nth-child(60)",
                        timeout=60000),
                    PageMethod(
                        "screenshot",
                        path="others/screen_shots/infinit_scroll_page.jpg",
                        full_page=True,
                        omit_background=True),
                    PageMethod(
                        "pdf",
                        path=f"{self.pdf_directory}scraping_club_home_page.pdf",
                        scale=1
                    ),
                ],
            })

    def parse(self, response):
        products = response.css(".post")

        for product in products:
            url = product.css("a").attrib["href"]
            product_url = response.urljoin(url)

            # Save the page as PDF and add it to the list
            pdf_path = f"../{self.pdf_directory}scraping_club_{len(self.pdfs) + 1}.pdf"
            self.pdfs.append(pdf_path)

            yield scrapy.Request(
                product_url,
                callback=self.parse_products_page,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod(
                            "wait_for_selector",
                            ".card-description",
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

    def parse_products_page(self, response):
        scraping_club_item = ScrapingClubItem()

        relative_img_url = response.xpath("//div/img/@src").get()
        image = response.urljoin(relative_img_url)

        # add the data to the list of scraped items
        scraping_club_item['image'] = image
        scraping_club_item['name'] = response.xpath(
            "//div/h3[contains(@class, 'card')]/text()"
        ).get()
        scraping_club_item['price'] = response.xpath(
            "//div/h4/text()"
        ).get()
        scraping_club_item['description'] = response.xpath(
            "//div/p[contains(@class, 'card')]/text()"
        ).get()

        yield scraping_club_item

