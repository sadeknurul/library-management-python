#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:22:50 2022

@author: Stish
"""
from datetime import datetime


class Book:
    def __init__(self,bookID,title,authors,isbn,isbn13,
            language_code,num_pages,publication_date,publisher,available):
        self.bookID=bookID
        self.title=title
        self.authors=authors
        self.isbn=isbn
        self.isbn13=isbn13
        self.language_code=language_code
        self.num_pages=num_pages
        self.publication_date=publication_date
        self.publisher=publisher
        self.available = available


    def __repr__(self):
        return f'''
                    Book ID:  {self.bookID}
                  Book ISBN:  {self.isbn}
                 Book Title:  {self.title}
                Book Auther:  {self.authors}
             Book Publisher:  {self.publisher}
      Book Publication Date:  {self.publication_date}
             Book Available:  {self.check_available()}
        '''
    def check_available(self):
        if self.available>0:
            return 'Available'
        else:
            return 'Not Available'
class BorrowBook:
    def __init__(self,user_id,book_id,create_date,retuen_date):
        self.user_id=user_id
        self.book_id=book_id
        self.create_date=create_date
        self.return_date=retuen_date



    def delayed_book_days(self):

        # convert string to date object
        d1 = datetime.strptime(self.create_date, "%Y-%m-%d")
        d2 = datetime.strptime(datetime.now().date(), "%Y-%m=%d")

        # difference between dates in timedelta
        delta = d2 - d1
        return delta.days