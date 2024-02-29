# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    pass


class ScrapingClubItem(BaseItem):
    # define the fields for your item here like:
    image = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()


class ContextNewsItem(BaseItem):
    explainer = scrapy.Field()
    published = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    context = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
