from .sql import Sql
from items import BooksItem, DocumentItem

class BooksPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BooksItem):
            book_id = item['book_id']
            ret = Sql.select_name(book_id)
            if ret[0] == 1:
                pass
            else:
                book_name = item['book_name']
                book_author = item['book_author']
                book_category = item['book_category']
                book_lastupdate = item['book_lastupdate']
                Sql.insert_book_name(book_name, book_author, book_category, book_id, book_lastupdate)

        if isinstance(item, DocumentItem):
            book_chapterurl = item['book_chapterurl']
            book_id = item['book_id']
            book_order = item['book_order']
            book_chaptertitle = item['book_chaptertitle']
            book_chaptercontent = item['book_chaptercontent']
            Sql.insert_book_chapter(book_chaptertitle, book_chaptercontent, book_id, book_order, book_chapterurl)