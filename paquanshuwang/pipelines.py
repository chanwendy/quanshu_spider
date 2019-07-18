# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from paquanshuwang.items import PaquanshuwangItem,PaquanshuwangDetailItem


db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'qwe123',
    'db': 'db_quanshu_1',
    "charset": "utf8",
}


class PaquanshuwangPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(**db_config)
        self.cusr = self.conn.cursor()

    def close_spider(self, spider):
        self.cusr.close()
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, PaquanshuwangItem):
            checke_exit_sql = 'SELECT id FROM tb_book_info WHERE title= "{}" AND author="{}"'.format(item['title'], item['author'])
            self.cusr.execute(checke_exit_sql)
            result = self.cusr.fetchone()
            if result:
                pass
            else:

                insert_colum = "title, author,state,category,intro,book_url,image_url,detail_url,date_time"
                insert_value = '"{}","{}","{}","{}","{}","{}","{}","{}",{}'.format(item['title'], item['author'], item['state'], item['category'], item['intro'], item['book_url'], item['image_url'], item['detail_url'], 'NOW()')
                insert_sql = 'INSERT INTO tb_book_info({}) VALUES({})'.format(insert_colum, insert_value)
                try:
                    self.cusr.execute(insert_sql)
                    self.conn.commit()
                    print('[+]{}小说插入成功'.format(item['title']))
                except Exception as e:
                    print('[-]小说插入失败{}'.format(e))
                    self.conn.rollback()
        return item
class PaquanshuwangDetail_Pipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(**db_config)
        self.cusr = self.conn.cursor()
        spider.conn = self.conn
        spider.cusr = self.cusr

    def close_spider(self, spider):
        self.cusr.close()
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, PaquanshuwangDetailItem):
            insert_colum = 'chapter_url, chapter_name, chapter_text, date_time'
            insert_value = "'{}','{}','{}',{}".format(item['chapter_url'], item['chapter_name'], item['chapter_text'], 'NOW()')
            insert_sql = 'INSERT INTO tb_book_detail({}) VALUES({})'
            sql = insert_sql.format(insert_colum, insert_value)
            try:
                self.cusr.execute(sql)
                self.conn.commit()
                print('[+]{}小说章节插入成功'.format(item['chapter_name']))
            except Exception as e :
                print('[-]{}小说章节插入失败'.format(item['chapter_name']))
                self.conn.rollback()

        return item
