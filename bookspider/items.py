# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_url = scrapy.Field()
    book_lastupdate = scrapy.Field()
    book_category = scrapy.Field()
    book_id = scrapy.Field()
    pass

class DocumentItem(scrapy.Item):
    book_id = scrapy.Field()
    book_chaptercontent = scrapy.Field()
    book_order = scrapy.Field()
    book_chapterurl = scrapy.Field()
    book_chaptertitle = scrapy.Field()

# class DocomentImageItem(scrapy.Item):
#     image_name = scrapy.Field()
#     image_urls = scrapy.Field()
#     image_url = scrapy.Field()
