import mysql.connector
from books import settings

MYSQL_HOST = settings.MYSQL_HOST
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER, password = MYSQL_PASSWORD, host=MYSQL_HOST, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:

    @classmethod
    def insert_book_name(cls, book_name, book_author, book_category, book_id, book_lastupdate):
        sql = "INSERT INTO books_list(`book_name`, `book_author`, `book_category`, `book_id`, `book_lastupdate`) VALUES (%(book_name)s, %(book_author)s, %(book_category)s, %(book_id)s, %(book_lastupdate)s)"
        value = {
            'book_name': book_name,
            'book_author': book_author,
            'book_category': book_category,
            'book_id': book_id,
            'book_lastupdate': book_lastupdate
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_name(cls, book_id):
        sql = "SELECT EXISTS(SELECT 1 FROM books_list WHERE book_id=%(book_id)s)"
        value = {
            'book_id': book_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def insert_book_chapter(cls,book_chaptertitle, book_chaptercontent, book_id, book_order, book_chapterurl):
        sql = 'INSERT INTO book_content(`book_chaptertitle`, `book_chaptercontent`, `book_id`, `book_order`,`book_chapterurl`)\
                VALUES (%(book_chaptertitle)s,%(book_chaptercontent)s,%(book_id)s,%(book_order)s,%(book_chapterurl)s)'
        value = {
            'book_chaptertitle': book_chaptertitle,
            'book_chaptercontent': book_chaptercontent,
            'book_id': book_id,
            'book_order': book_order,
            'book_chapterurl': book_chapterurl
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def sclect_chapter(cls, book_chapterurl):
        sql = "SELECT EXISTS(SELECT 1 FROM book_content WHERE book_chapterurl=%(book_chapterurl)s)"
        value = {
            'book_chapterurl': book_chapterurl
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]
