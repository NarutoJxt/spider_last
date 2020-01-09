#! /usr/bin/[ython
# -*- coding=utf-8 -*-
import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入seetings配置
import time


class DBHelper():
    '''这个类也是读取settings中的配置，自行修改代码进行操作'''

    def __init__(self):
        settings = get_project_settings()  #获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  #读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  #编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    #创建数据库
    def insert(self, item):
        sql = ""
        params = ()
        if item["status"] ==2:
            sql = """
              insert into esffouseitem (city_name,esf_house_link,house_name,house_detail,house_address
              ,house_total_price,house_per_price,status)
              values({},{},{},{},{},{},{},{})
            """
            params = (repr(item["city_name"]), repr(item['esf_house_link']), repr(item['house_name']),
                      repr(item['house_detail']), repr(item['house_address']),repr(item['house_total_price']),
                      repr(item['house_per_price']), repr(item['status']))
        elif item["status"]==1:
            sql = """
                       insert into newhouseitem (city_name,new_house_name,house_area,address,tel,forsale,house_type,
                       nhouse_price,orgion_url,status)
                       values({},{},{},{},{},{},{},{},{},{})
                     """
            params = (repr(item["city_name"]), repr(item['new_house_name']), repr(item['house_area']),
                      repr(item['address']), repr(item['tel']), repr(item['forsale']), repr(item['house_type']),
                      repr(item['nhouse_price']), repr(item['orgion_url']),repr(item['status']))
        query = self.dbpool.runInteraction(self._conditional_insert,sql,params)
        #调用异常处理方法
        query.addErrback(self._handle_error)
        return item

    #写入数据库中
    def _conditional_insert(self, tx, sql,params):
        print(sql.format(*params))
        tx.execute(sql.format(*params))
    #错误处理方法

    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)