# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:38:22 2022

@author: Sadek
"""
import json
import sqlite3
from dbcon import dbCon
from Utils import design
from book import BorrowBook

class Account(dbCon):
    def __init__(self,a_id,username, password,f_name,l_name,u_type,l_books_borrowed=[],l_books_reserved=[],
                 history_return=None,l_delayed_book=0,l_lost_Books = None, acc_fine=0):
        super().__init__()
        self.a_id=a_id
        self.username = username,
        self.password = password
        self.u_type = u_type
        self.f_name = f_name
        self.l_name = l_name
        self.l_books_borrowed=l_books_borrowed
        self.l_books_reserved=l_books_reserved
        self.history_return = history_return
        self.l_lost_Books = l_lost_Books
        self.l_delayed_book=l_delayed_book
        self.acc_fine = acc_fine
        self.load_borrows_books()
        self.load_reserved_books()
        self.load_lost_books()
        self.load_returned_books()


        # self.conn = sqlite3.connect(':memory:')





    @classmethod
    def create_account(cls,username,password,type,info):
        if type=="Student":
            values=(username,password,info.f,info.s,type,info.class_name,None,'False')
        elif type=="Staff":
            values=(username,password,info.f,info.s,type,None,info.dept,'False')
        else:
            values=(username,password,info.f,info.s,type,None,None,'False')
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("INSERT INTO accounts(username,password,f_name,l_name,u_type,class,dept,verified) VALUES(?,?,?,?,?,?,?,?)",
        values)
        conn.commit()
        return True
    @classmethod
    def load_account(cls, username):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE username =?',(username,))
        a=c.fetchone()
        return Account(a[0],a[1],a[2],a[3],a[4],a[5])

    def load_borrows_books(self):
        self.c.execute('SELECT * FROM borrow_books WHERE user_id =?',(self.a_id,))
        a=self.c.fetchall()
        if a:
            count=len(a)
            self.l_books_borrowed=count
        else:
            self.l_books_borrowed=0



    def load_reserved_books(self):
        self.c.execute('SELECT * FROM reserve_books WHERE user_id =?',(self.a_id,))
        a=self.c.fetchall()

        if a:
            t_count=len(a)
            print(t_count)
            self.l_books_reserved=a
        else:
            self.l_books_reserved=None


    def load_returned_books(self):
        self.c.execute('SELECT * FROM return_books WHERE user_id =?',(self.a_id,))
        a=self.c.fetchall()
        self.history_return=a


    def load_lost_books(self):
        self.c.execute('SELECT * FROM lost_books WHERE user_id =?',(self.a_id,))
        a=self.c.fetchall()
        self.l_lost_Books=a

    def load_delayed_books(self):
        self.c.execute('SELECT * FROM borrow_books WHERE is_return=false and user_id =?',(self.a_id,))
        a=self.c.fetchall()
        d_count=0
        if a:
            b_obj=BorrowBook(*a)
            for b in b_obj:
                if b.delayed_book_days(self) > 7:
                    d_count+=1
            self.l_delayed_book=d_count
        else:
            self.l_delayed_book=0


    def cal_fine_by_lost_book(self):
        total_lost_books=len(self.l_lost_Books)
        self.acc_fine += total_lost_books*10

    def cal_fine_by_delayed_book(self):
        total_lost_books=len(self.l_delayed_book)
        self.acc_fine += total_lost_books*5

        pass
    def __repr__(self):
        return f"""{'*'*20}
id: {self.a_id}
books_borrowed: {self.l_books_borrowed}
    """
