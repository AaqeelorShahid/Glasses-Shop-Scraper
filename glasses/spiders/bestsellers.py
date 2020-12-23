# -*- coding: utf-8 -*-
import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com']
    start_urls =["https://www.glassesshop.com/bestsellers"]

    # def start_requests(self):
    #     yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback= self.parse, headers={
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    #     })

    def get_price(self, selector):
        original_price = selector.xpath(
            ".//del/text()").get()
        if original_price is not None:
            return original_price
        else:
            return selector.xpath(".//div[@class='row']/div[contains(@class, 'pprice')]/span/text()").get()

    def parse(self, response):
        for item in response.xpath("//div[@class='prlist row']/div[@class='col-sm-6 col-md-4 m-p-product']"):
            yield{
                'url': item.xpath("//div[@class='pimg default-image-front']/a/@href").get(),
                'image_url': item.xpath("//div[@class='pimg default-image-front']/a/img[1]/@src").get(),
                'name': item.xpath("//div[@class='row']/p[@class='pname col-sm-12']/a/text()").get(),
                'price': self.get_price(item),
                'next_page': response.xpath("//div[@class='custom-pagination']/ul/li/a[@aria-label='Next »']/@href").get()
            }

        next_page = response.xpath("//div[@class='custom-pagination']/ul/li/a[@aria-label='Next »']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        



