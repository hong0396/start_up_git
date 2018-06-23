# -*- coding: utf-8 -*-
import scrapy


class ZhihuspdSpider(scrapy.Spider):
    name = "zhihuspd"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass
