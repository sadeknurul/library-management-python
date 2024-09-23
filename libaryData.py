#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:11:18 2022

@author: Stish
"""

from book import Book
import json
import sqlite3
from dbcon import dbCon

class LibaryData(dbCon):
    d_books = {}
    def __init__(self):
        super().__init__()

        self.create_books_table()
        self.create_account_table()
        self.create_borrowed_table()
        self.create_reserved_table()
        self.create_lost_books_table()
        self.create_return_books_table()
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #print(self.c.fetchall())




    def create_account_table(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS accounts(
                uid integer PRIMARY KEY AUTOINCREMENT,
                username text NOT NULL,
                password text NOT NULL,
                f_name text NOT NULL,
                l_name text NOT NULL,
                u_type text NOT NULL,
                class text NULL,
                dept text NULL,
                verified text,
                fine text
                )""")
        except BaseException as e:
            print(e)
            print("Table already exist")
    def create_borrowed_table(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS borrow_books(
                id integer PRIMARY KEY,
                user_id integer,
                book_id integer,
                create_date text,
                return_date text,
                is_return text DEFAULT false
                )""")
        except BaseException as e :
            print(e)
            print("Borrow Books Table already exist")

    def create_return_books_table(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS return_books(
                id integer PRIMARY KEY,
                user_id integer,
                book_id integer,
                create_date text
                )""")
        except BaseException as e :
            print(e)
            print("Borrow Books Table already exist")
    def create_reserved_table(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS reserve_books(
                id integer PRIMARY KEY,
                user_id integer,
                book_id,
                create_date text
                )""")
        except BaseException as e :
            print(e)
            print("Reserve Book")

    def create_lost_books_table(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS lost_books(
                id integer PRIMARY KEY,
                user_id integer,
                book_id integer,
                create_date text
                )""")
        except BaseException as e :
            print(e)
            print("Reserve Book")

    def create_Fee_collection_table(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS fee_collection(
                id integer PRIMARY KEY,
                user_id integer,
                fee_paid integer,
                fee_due integer,
                create_date text
                )""")
        except BaseException as e :
            print(e)
            print("Borrow Books Table already exist")



    def create_books_table(self):
        try:
            # self.c.execute("DROP TABLE  books;")
            # self.conn.commit()
            self.c.execute("""CREATE TABLE IF NOT EXISTS books(
                bookID integer PRIMARY KEY,
                title text,
                authors text,
                isbn text,
                isbn13 text,
                language_code text,
                num_pages integer,
                publication_date text,
                publisher text,
                available integer
                )""")
        except BaseException as e :
            print(e)
            print("books Table already exist")
        # else:
        #     self.loadBooks_JsonToDb()
    def loadBooks_JsonToDb(self):
        with open('./book2.json') as fd:
            books= json.load(fd)
            for b in books:
                self.insertBook(
                    Book(
                        b['bookID'],
                        b['title'],
                        b['authors'],
                        b['isbn'],
                        b['isbn13'],
                        b['language_code'],
                        b['num_pages'],
                        b['publication_date'],
                        b['publisher'],
                        '5'
                    )
                )

    def insertBook(self,b):
        with self.conn:
            self.c.execute("INSERT INTO books VALUES(:bookID,:title,:authors,:isbn,:isbn13,:language_code,:num_pages,:publication_date,:publisher,:available)",
                           {
                               'bookID':b.bookID,
                               'title':b.title,
                               'authors':b.authors,
                               'isbn':b.isbn,
                               'isbn13':b.isbn13,
                               'language_code':b.language_code,
                               'num_pages':b.num_pages,
                               'publication_date':b.publication_date,
                               'publisher':b.publisher,
                               'available':b.available
                            }
                        )



