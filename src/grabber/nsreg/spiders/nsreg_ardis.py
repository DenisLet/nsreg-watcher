# -*- coding: utf-8 -*-
import scrapy
from nsreg.items import NsregItem

from ..utils import find_price
# работает

REGEX_PATTERN = r".*(([0-9]*[.,])?[0-9]{3}).*"
EMPTY_PRICE = {
    'price_reg': None,
    'price_prolong': None,
    'price_change': None,
}


class NsregArdisSpider(scrapy.Spider):
    name = 'nsreg_ardis'
    allowed_domains = ['ardis.ru']
    start_urls = ['https://ardis.ru/domains/']

    def parse(self, response):
        price_reg = response.xpath(
            '//*[@id="show_domain"]/div/div/table/tbody/tr[1]/td[3]/a/text()').get()
        price_reg = find_price(REGEX_PATTERN, price_reg)

        price_prolong = response.xpath(
            '//*[@id="show_domain"]/div/div/table/tbody/tr[1]/td[4]/a/text()').get()
        price_prolong = find_price(REGEX_PATTERN, price_prolong)

        price_change = response.xpath(
            '//*[@id="show_domain"]/div/div/table/tbody/tr[1]/td[5]/a/text()').get()
        price_change = find_price(REGEX_PATTERN, price_change)

        item = NsregItem()
        item['name'] = "ООО «Ардис»"
        price = item.get('price', EMPTY_PRICE)
        price['price_reg'] = price_reg
        price['price_prolong'] = price_prolong
        price['price_change'] = price_change
        item['price'] = price

        yield item
