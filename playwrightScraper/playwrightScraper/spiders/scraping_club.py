import scrapy
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
                        # PageMethod("click", ".post"),
                        PageMethod(
                            "screenshot",
                            path="others/screen_shots/infinit_scroll_page.jpg",
                            full_page=True,
                            omit_background=True),
                        ],
                    })

    def parse(self, response):
        products = response.css(".post")
        scraping_club_item = ScrapingClubItem()

        for product in products:
            # scrape product data
            url = product.css("a").attrib["href"]
            image = product.css(".card-img-top").attrib["src"]
            name = product.css("h4 a::text").get()
            price = product.css("h5::text").get()

            # add the data to the list of scraped items
            scraping_club_item['url'] = url
            scraping_club_item['image'] = image
            scraping_club_item['name'] = name
            scraping_club_item['price'] = price

            yield scraping_club_item
