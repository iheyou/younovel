import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from items import BooksItem, DocumentItem
from books.mysqlpipelines.sql import Sql

class Myspider(scrapy.Spider):
    name = 'books'
    chapter_order = 'http://www.booktxt.net/'
    allowed_domains = ('booktxt.net',)
    start_urls = (
        'http://www.booktxt.net/xiaoshuodaquan/',
    )
    # def start_requests(self):
    #     yield Request(books_web, self.parse)

    ## 爬取所有小说
    def parse(self, response):

        links = BeautifulSoup(response.text, 'lxml').find('div', id='main').find_all('li')

        for num in links:
            bookName = num.find('a').get_text()
            bookUrl = num.find('a')['href']

            yield scrapy.Request(bookUrl, callback=self.get_chapterurl, meta={'book_name': bookName, 'book_url': bookUrl})

    ##处理每本小说的信息，然后爬取每个章节
    def get_chapterurl(self, response):

        ## 处理获取到的小说信息
        item = BooksItem()
        item['book_name'] = str(response.meta['book_name']).replace('\xa0', '')

        item["book_url"] = response.url

        book_category = BeautifulSoup(response.text, 'lxml').find('div',id='bdshare').findNext(text='顶点小说').findNext('a').get_text()
        item['book_category'] = str(book_category).replace('/', '')

        tag_author = BeautifulSoup(response.text, 'lxml').find('div', id='info').find('p')
        book_author = tag_author.get_text()
        item['book_author'] = str(book_author).replace('\xa0', '')

        item['book_lastupdate'] = tag_author.findNextSibling('p').findNextSibling('p').get_text()

        book_id = str(response.url)[-8 : -1].replace('/', '')
        item['book_id'] = book_id

        ## 返回小说的信息给pipelines处理存储
        yield item

        ##处理每本小说的所有章节信息
        urls = re.findall(r'<dd><a href="(.*)">(.*)</a></dd>', response.text)
        num = 0
        for url in urls:
            url_last = re.match(r'^(\/\d+\_\d+)/(\d+\.html)', url[0]).group(2)
            num = num + 1
            book_chapterurl = response.url + url_last
            book_chaptertitle = url[1]
            rets = Sql.sclect_chapter(book_chapterurl)
            if rets[0] == 1:
                pass
            else:
                yield scrapy.Request(url=book_chapterurl, callback=self.get_chaptercontent, meta={
                    'book_order': num,
                    'book_id': book_id,
                    'book_chaptertitle': book_chaptertitle,
                    'book_chapterurl': book_chapterurl
                })

    ##爬取章节内容然后存入数据库
    def get_chaptercontent(self, response):
        item = DocumentItem()
        item['book_order'] = response.meta['book_order']
        item['book_id'] = response.meta['book_id']
        item['book_chaptertitle'] = str(response.meta['book_chaptertitle']).replace('\xa0', '')
        item['book_chapterurl'] = response.meta['book_chapterurl']
        book_chaptercontent = BeautifulSoup(response.text, 'lxml').find('div', id='content').get_text()
        item['book_chaptercontent'] = str(book_chaptercontent).replace('\xa0', ' ')

        yield item
