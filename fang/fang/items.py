# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class NewHouseItem(scrapy.Item):
    city_name = scrapy.Field()
    new_house_name = scrapy.Field()
    house_area = scrapy.Field()
    address = scrapy.Field()
    tel = scrapy.Field()
    forsale = scrapy.Field()
    house_type = scrapy.Field()
    nhouse_price = scrapy.Field()
    orgion_url = scrapy.Field()
    status = scrapy.Field()
class EsfFouseItem(scrapy.Item):
    city_name = scrapy.Field()
    esf_house_link = scrapy.Field()
    house_name = scrapy.Field()
    house_detail = scrapy.Field()
    house_address = scrapy.Field()
    house_total_price = scrapy.Field()
    house_per_price = scrapy.Field()
    status = scrapy.Field()
