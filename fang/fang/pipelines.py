# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exporters import JsonLinesItemExporter
import pymysql
import scapy
from scrapy.pipelines.images import ImagesPipeline
from .db import DBHelper
import os
from scrapy.utils.project import get_project_settings  #导入seetings配置

class FangPipeline(object):
    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        self.db.insert(item)
        return item

    def close_spider(self, spider):
        pass
