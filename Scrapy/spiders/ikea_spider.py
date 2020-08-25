# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrape_prices.items import IkeaItem


class CarsSpider(scrapy.Spider):
    name = "ikea"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 200,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    start_urls = [
        'https://www.ikea.lt/lt/products/biuro-baldai/grindys/darbo-kambario-spinteles-ir-lentynos/micke-stalciu-spintele-su-ratukais-balta-art-90213078'
    ]

    def parse(self, response):
        name = response.xpath("//*[@class='display-7']/text()").get()
        name_desc = response.xpath("//*[@class='itemFacts']/text()").get()
        price = response.xpath("//span/@data-price").get()
        url = response.url

        item = IkeaItem()
        item['name'] = name + " " + name_desc
        item['price'] = price
        item['url'] = url
        item['last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d')
        yield item