# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SenukaiItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    last_updated = scrapy.Field()

class IkeaItem(scrapy.Item):
    name = scrapy.Field()
    name_desc = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    last_updated = scrapy.Field()
