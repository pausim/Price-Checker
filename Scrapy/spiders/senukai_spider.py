# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrape_prices.items import SenukaiItem


class CarsSpider(scrapy.Spider):
    name = "senukai"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 200,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    start_urls = [
        'https://www.senukai.lt/p/juosta-mankstos-spokey-920956-15-23-kg/62iz?mtd=search&pos=regular&src=searchnode',
        'https://www.senukai.lt/p/diskinis-svoris-grifui-ylps18-chromuotas-5-kg/2tx3?mtd=bought&pos=product-bottom&src=bitrec&index=2&prev=128943',
        'https://www.senukai.lt/p/diskinis-svoris-grifui-ylps18-chromuotas-2-5-kg/2rhr?mtd=bought&pos=product-bottom&src=bitrec&index=2&prev=132087',
        'https://www.senukai.lt/p/kingston-a400-240gb-sataiii-2-5-sa400s37-240g/8qiu',
        'https://www.senukai.lt/p/monitorius-hp-elitedisplay-e243/6pzb?mtd=search&pos=regular&src=searchnode',
        'https://www.senukai.lt/p/monitorius-hp-elitedisplay-e233/6pxl?mtd=viewed&pos=product-bottom&src=bitrec&index=5&prev=313607',
        'https://www.senukai.lt/p/monitorius-hp-elitedisplay-e243i/6pxm?mtd=viewed&pos=product-bottom&src=bitrec&index=4&prev=313607'
    ]

    def parse(self, response):
        name = response.xpath("//*[@class='product-righter google-rich-snippet']/h1/text()").get()
        price = response.xpath("//*[@class='price']/span/text()").get()
        url = response.url

        item = SenukaiItem()
        item['name'] = name.replace("\n", "")
        item['price'] = price.replace(",", ".")
        item['url'] = url
        item['last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d')
        yield item