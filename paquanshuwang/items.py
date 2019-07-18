# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaquanshuwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_url = scrapy.Field()
    title = scrapy.Field()
    intro = scrapy.Field()
    category = scrapy.Field()
    state = scrapy.Field()
    author = scrapy.Field()

    detail_url = scrapy.Field()
    image_url = scrapy.Field()


class PaquanshuwangDetailItem(scrapy.Item):
    book_id = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_text = scrapy.Field()
    chapter_name = scrapy.Field()


