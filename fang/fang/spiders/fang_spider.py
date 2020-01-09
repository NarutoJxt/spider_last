# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
import re
import os
from ..items import NewHouseItem,EsfFouseItem
import requests
from lxml import etree
from scrapy.utils.project import get_project_settings

class FangSpiderSpider(CrawlSpider):
    name = 'fang_spider'
    allowed_domains = ['fang.com']
    start_urls = ["https://www.fang.com/SoufunFamily.html"]

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//table[@class='table01']//tr")
        province_fu = None
        for tr in trs:
            td = tr.xpath(".//td")
            province = td[1].xpath(".//strong/text()").get()
            city = {}
            if province is None or province == '\xa0':
                province = province_fu
            else:
                province_fu = province
            if province == "其他":
                continue
            city_as = td[2].xpath(".//a")
            city_loc = {}
            for a in city_as:
                city_a = a.xpath("./@href").get()
                city_name = a.xpath("./text()").get()
                if city_name != "成都":
                    continue
                if city_name =="北京":
                    new_house = "https://newhouse.fang.com/house/s/"
                    esf_house = "https://esf.fang.com/"
                else:
                    city_list = city_a.split("//")
                    scheme = city_list[0]
                    domain = city_list[1]
                    new_house = scheme + "//newhouse."+domain+"/house/s"
                    esf_house = scheme + "//esf." + domain + "/house/s"

                yield scrapy.Request(url=new_house,callback=self.parse_newhouse,meta={"city_name":city_name,"href":new_house})
                yield scrapy.Request(url=esf_house,callback=self.parse_esfhouse, meta={"city_name":city_name,"href":esf_house})
    def parse_newhouse(self,response):
        new_house_item = NewHouseItem()
        new_house_item['city_name'] = response.meta["city_name"]
        divs = response.xpath("//div[@class='clearfix']")
        for div in divs:
            new_house_name = str(div.xpath(".//div[@class='nlcd_name']/a/text()").get())
            new_house_item["new_house_name"] = new_house_name.strip()
            house_area = div.xpath(".//div[@class='house_type clearfix']//a/text()").getall()
            new_house_item['house_area'] = ",".join(house_area).replace(" ","")
            new_house_item['address'] = div.xpath(".//div[@class='relative_message clearfix']//div[@class='address']/a/text()").get()
            tel = div.xpath(".//div[@class='relative_message clearfix']//div[@class='tel']/p//text()").getall()
            tel = ",".join(tel)
            re.sub(r"\n|\t", "", tel)
            new_house_item['tel'] = tel
            if new_house_item['address'] is not None:
                new_house_item['address'] = new_house_item['address'].strip()
            new_house_item['forsale'] = div.xpath(".//div[@class='nlc_details']//div[@class='fangyuan']//span/text()").get()
            if new_house_item["address"] == None or new_house_item['address'] =="":
                new_house_item['address'] = "空"
            house_types = div.xpath(".//div[@class='nlc_details']//div[@class='fangyuan']//a/text()").getall()
            house_type = ",".join(house_types)
            if house_type:
                house_type = house_type.strip()
            else:
                house_type = None

            new_house_item['house_type'] = house_type

            nhouse_price = div.xpath(".//div[@class='nlc_details']//div[@class='nhouse_price']//text()").getall()
            nhouse_price = ",".join(nhouse_price)
            re.sub(r"\n|\t","",nhouse_price)
            new_house_item['nhouse_price'] = nhouse_price.strip()
            orgion_url = div.xpath(".//div[@class='nlcd_name']/a/@href").get()
            if orgion_url:
                new_house_item['orgion_url'] = "http:"+orgion_url
            new_house_item['status'] = 1
            yield new_house_item
        next_url = response.xpath("//div[@class='page']//li[@class='fr']//a[@class='next']/@href").get()
        next_url = response.urljoin(next_url)
        yield scrapy.Request(url=next_url,callback=self.parse_newhouse,meta={"city_name":response.meta["city_name"],"href":response.meta['href']})
    def parse_esfhouse(self,response):
        esf_house_item = EsfFouseItem()
        esf_house_item['city_name'] = response.meta['city_name']
        dls = response.xpath("//div[contains(@class,'shop_list')]//dl[@class='clearfix']")
        for dl in dls:
            h4 = dl.xpath(".//h4[@class='clearfix']")
            esf_house_link = h4.xpath(".//a/@href").get()
            if esf_house_link:
                esf_house_item['esf_house_link'] = response.urljoin(esf_house_link)
            esf_house_item['house_name'] = h4.xpath(".//a/@title").get()
            house_detail = dl.xpath(".//p[@class='tel_shop']//text()").getall()
            house_detail = list(map(lambda x:re.sub(r"\s","",x),house_detail))
            house_detail = ",".join(house_detail)
            esf_house_item['house_detail'] = house_detail.replace(",","")
            esf_house_item['house_address'] = dl.xpath(".//p[@class='add_shop']//span/text()").get()
            house_total_price =",".join(dl.xpath(".//span[@class='red']//text()").getall())
            esf_house_item['house_total_price'] = house_total_price.replace(",","")
            esf_house_item['house_per_price'] = dl.xpath(".//dd[@class='price_right']//span[not(@class)]//text()").get()
            esf_house_item["status"] = 2
            yield esf_house_item
        next_urls = response.xpath("//div[@class='page_al']//p")
        next_url = next_urls[-3].xpath("./a/@href").get()
        if next_url:
           next_url = response.urljoin(next_url)
           print(next_url)
           yield scrapy.Request(url=next_url,callback=self.parse_esfhouse
                                ,meta={"city_name":esf_house_item['city_name'],"href":response.meta["href"]})
        else:
            print("hahahah")
