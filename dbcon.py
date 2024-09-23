
import sqlite3
from book import Book
class dbCon():
    def __init__(self) :
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()


