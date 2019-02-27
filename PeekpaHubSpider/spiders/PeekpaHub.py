# -*- coding: utf-8 -*-
import scrapy


class PeekpahubSpider(scrapy.Spider):
    name = 'PeekpaHub'
    allowed_domains = ['peekpahub.com']
    # start_urls = ['http://peekpahub.com/']
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        pass
