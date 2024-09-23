# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:45:18 2022

@author: Sadek
"""
import os

from book import Book
from dbcon import dbCon
from Utils import design
from datetime import datetime


class User(dbCon) :
    def __init__(self,f,s,a=None):
        super().__init__()
        self.f = f
        self.s = s
        self.account = a
    def __rpr__(self):
        return f"""{self.f} {self.s},
{self.a}
"""
    def pending_user_accounts(self):
        with self.conn:
            self.c.execute("""SELECT * from accounts WHERE verified=:verified""",
                      {'verified':'False'})
            users = self.c.fetchall()
            for user in users:
                status = 'Waiting for Approval'
                print(f'''
                      UserID: {user[0]}
                      Name: {user[3]} {user[4]}
                      Status: {status}
                      **********
                      ''')
            while True:
                print(f"""\n\n\n
            ============= Do you want to approved account =============

                        1. Yes
                        q. Return
                """)
                c = input('''\n
                        Select Option (1|q):''')
                choice = {"1" :"Yes",
                      "q" :"q"}.get(c,"invalid")
                if choice == "q":
                    print('Bye..')
                    break
                elif choice == 'Yes':
                    userID = input("Input UserID: ")
                    try:
                        self.c.execute("""UPDATE accounts SET verified=:verified
                              WHERE uid=:uid""",
                              {'verified':'True', 'uid':userID})
                        self.conn.commit()
                        print("User account approved successfull")
                    except:
                        print("Something went wrong!")

                else:
                    print("Try again...")
            return True
            
    def user_details(self):
        uid = input("Input UsesrID: ")
        with self.conn:
            self.c.execute("""SELECT * from accounts WHERE uid=:uid""",
                      {'uid':uid})
            
            rows = self.c.fetchall()
            if len(rows) > 0:
                for row in rows:
                    status = 'Waiting for Approval'
                    if row[8] == 'True':
                        status = 'Approved'
                    print(f'''
                          UserID: {row[0]}
                          Username: {row[1]}
                          Name: {row[3]} {row[4]}
                          User Type: {row[5]}
                          Status: {status}
                          ''')
                    return True
            else:
                print("No reservation for this book.")
                return False
            
    def search(self,opt,s):
        s = '%'+s+'%'
        cmd = f'SELECT * FROM books WHERE {opt} LIKE :s'
        if opt in ['title','authors','isbn','publication_date']:
           # c.execute('SELECT * FROM books WHERE title LIKE :s', {'s':s})
            self.c.execute(cmd, {'s':s})
            # c.execute('SELECT * FROM books WHERE title =:s', {'s':s})
        else:
           print('option not available')
        return self.c.fetchall()

    def getBookInfo(self,opt,s):
        s = '%'+s+'%'
        cmd = f'SELECT * FROM books WHERE {opt} LIKE :s'
        if opt in ['bookID','isbn']:
           # c.execute('SELECT * FROM books WHERE title LIKE :s', {'s':s})
            self.c.execute(cmd, {'s':s})
            # c.execute('SELECT * FROM books WHERE title =:s', {'s':s})
        else:
           print('option not available')
        return self.c.fetchone()

    def reservation_status(self):
        b = input("Input ISBN: ")
        with self.conn:
            self.c.execute("""SELECT * from books WHERE isbn=:isbn""",
                      {'isbn':b})
            row = self.c.fetchone()

            self.c.execute("""SELECT * from reserve_books WHERE book_id=:book_id""",
                      {'book_id':row[0]})
            rows = self.c.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.c.execute("""SELECT * from accounts WHERE uid=:uid""",
                              {'uid':row[1]})
                    user = self.c.fetchone()
                    print("User : {} Reservation Date: {}".format(user[3], row[3]))
                    return True
            else:
                print("No reservation for this book.")
                return False




    def getBooks(self):
        with self.conn:
            self.c.execute('SELECT * FROM books')
        return self.c.fetchall()

    def getBook_by_ID(self,id):
        with self.conn:
            self.c.execute("""SELECT * from books WHERE bookID=:bookID""",
                {   'bookID':id})
        return self.c.fetchone()
    def getBook_by_ISBN(self,isbn):
        with self.conn:
            self.c.execute("""SELECT * from books WHERE isbn=:isbn""",
                {   'isbn':isbn})
        return self.c.fetchone()

    def getBorrowedBooks(self):
        with self.conn:
            self.c.execute("""SELECT * from borrow_books WHERE user_id=:user_id""",
                {'user_id':self.account.a_id})
        return self.c.fetchall()

    def getReservedBooks(self):
        with self.conn:
            self.c.execute("""SELECT * from reserve_books WHERE user_id=:user_id""",
                {'user_id':self.account.a_id})
        return self.c.fetchall()

    def borrow_book(self,b):
        current_availble = b.available-1
        design(f"Availlble book count {current_availble}")
        if current_availble>0:
            with self.conn:
                self.c.execute("INSERT INTO borrow_books(book_id,user_id,create_date,return_date) VALUES(?,?,?,?)",
                (b.bookID,self.account.a_id,datetime.now().date(),None))
                self.conn.commit()
                self.c.execute("""UPDATE books SET available=:available
                      WHERE isbn=:isbn""",
                      {'isbn':b.isbn, 'available':current_availble})
                self.conn.commit()
                design("Your book Borrowed a Book Done.")
            return True
        else:
            design("Book is not available at the moment!")
            return False

    def reserve_book(self,b):
        current_availble = b.available-1
        design(f"Availlble book count {current_availble}")
        if current_availble>0:
            self.c.execute("INSERT INTO reserve_books(book_id,user_id,create_date) VALUES(?,?,?)",
            (b.bookID,self.account.a_id,datetime.now().date()))
            self.conn.commit()
            self.c.execute("""UPDATE books SET available=:available
                  WHERE isbn=:isbn""",
                  {'isbn':b.isbn, 'available':current_availble})
            self.conn.commit()
            design("Your reserved a Book Done.")
            return True
        else:
            design("Book is not available at the moment!")
            return False

    def issue_book(self,b):
        with self.conn:
            self.c.execute("""UPDATE books SET available=:available)",
                      WHERE title=:title AND 'author':author""",
                      {'title':b.title, 'author':b.author, 'available':b.available})

    def return_book(self,isbn):

        r=self.getBook_by_ISBN(isbn)
        b=Book(*r)
        self.c.execute("""UPDATE borrow_books SET return_date=:return_date,is_return=:is_return
                WHERE book_id=:book_id and user_id=:user_id""",
                {'book_id':b.bookID,'user_id':self.account.a_id, 'return_date':datetime.now().date(),'is_return':'True'})
        self.conn.commit()

        self.c.execute("INSERT INTO return_books(book_id,user_id,create_date) VALUES(?,?,?)",
            (b.bookID,self.account.a_id,datetime.now().date()))
        self.conn.commit()

        self.c.execute("""UPDATE books SET available=:available
                WHERE isbn=:isbn""",
                {'isbn':b.isbn, 'available':b.available+1})
        self.conn.commit()
        design("Your Return a Book Done.")
        return True

    def cancel_reservation_book(self,isbn):

        r=self.getBook_by_ISBN(isbn)
        b=Book(*r)
        self.c.execute("""DELETE from reserve_books
                WHERE book_id=:book_id and user_id=:user_id""",
                {'book_id':b.bookID,'user_id':self.account.a_id})
        self.conn.commit()

        self.c.execute("""UPDATE books SET available=:available
                WHERE isbn=:isbn""",
                {'isbn':b.isbn, 'available':b.available+1})
        self.conn.commit()
        design("Your reservation of book is cancelled Done.")
        return True


    def remove_book(self,b):
        with self.conn:
            self.c.execute("""DELETE from books WHERE title=:title AND author=:author""",
                      {'title':b.title, 'author':b.author})



class Student(User):
    b_limit = 2
    def __init__(self,f,s,cls=None,acc=None):
        super().__init__(f,s,acc)
        self.class_name = cls




    def menu(self):
        while True:
            print(f"""\n\n\n
        ============= Welcome to Library  System =============

                            Student Menu
                    1. Books Catalog
                    2. Search Book
                    3. Borrow Book
                    4. Reserve Book
                    5. My Borrowed Books
                    6. Return book
                    7. My Reservations
                    8. Cancel Reservation
                    9. Pay Fine Fee
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-9|q): ''')
            choice = {"1" :self.f_opt1,
                  "2" :self.f_opt2,
                  "3" :self.f_opt3,
                  "4" :self.f_opt4,
                  "5" :self.f_opt5,
                  "6" :self.f_opt6,
                  "7" :self.f_opt7,
                  "8" :self.f_opt8,
                  "9" :self.f_opt9,
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                choice()
            else:
                print("Try again...")

    def f_opt1(self):
        print(f"""\n\n\n
        ============= Books Catalog =============
            """)
        r=self.getBooks()
        for b in r:
            design(Book(*b))
        while True:
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break

    def f_opt2(self):
        while True:
            print(f"""\n\n\n
        ============= Search Book By =============

                    1. ISBN
                    2. Title
                    3. Auther
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-3|q):''')
            choice = {"1" :"isbn",
                  "2" :"title",
                  "3" :"authors",
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')

                break
            elif choice != "invalid":
                s_txt = input('''
                    Search Book: ''')
                result=self.search(choice,s_txt)
                if result:
                    design("Search Book Results")
                    for b in result:
                        design(Book(*b))

            else:
                print("Try again...")

    def f_opt3(self):
        while True:
            print(f"""\n\n\n
        ============= For Borrowing! Find Book by =============

                    1. ISBN
                    2. Book ID
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-2|q):''')
            choice = {"1" :"isbn",
                  "2" :"bookID",
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                s_txt = input(f'''
                    Search Book by {choice}: ''')
                result=self.getBookInfo(choice,s_txt)
                if result:
                    design('''
                        Your Book Info''')

                    design(Book(*result).__repr__())
                    book=Book(*result)
                    while True:
                        design('''
                        ''')
                        print(f"""\n\n\n
                        Are you sure, you want to borrow this book?

                    1. Yes
                    2. No
                    q. Return
            """)
                        c = input('''\n
                        Select Option (1-2|q):''')
                        choice = {"1" :"Yes",
                            "2" :"No",
                            "q" :"q"}.get(c,"invalid")
                        if choice == "q":
                            print('Bye..')
                            break
                        elif choice != "invalid":
                             if choice =="Yes":
                                return self.borrow_book(book)

                        else:
                            print("Try again...")

    def f_opt4(self):
        while True:
            print(f"""\n\n\n
        ============= Find book to reserve =============

                    1. ISBN
                    2. Book ID
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-2|q):''')
            choice = {"1" :"isbn",
                  "2" :"bookID",
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                s_txt = input(f'''
                    Search Book by {choice}: ''')
                result=self.getBookInfo(choice,s_txt)
                if result:
                    design('''
                        Your Book Info''')

                    design(Book(*result).__repr__())
                    book=Book(*result)
                    while True:
                        design('''
                        ''')
                        print(f"""\n\n\n
                        Are you sure to reserve This Book?

                    1. Yes
                    2. No
                    q. Return
            """)
                        c = input('''\n
                        Select Option (1-2|q):''')
                        choice = {"1" :"Yes",
                            "2" :"No",
                            "q" :"q"}.get(c,"invalid")
                        if choice == "q":
                            print('Bye..')
                            break
                        elif choice != "invalid":
                             if choice =="Yes":
                                return self.reserve_book(book)

                        else:
                            print("Try again...")

    def f_opt5(self):
        borrows_data=self.getBorrowedBooks()

        while True:
            print(f"""\n\n\n
        ============= List of borrowed books =============
            """)
            for b in borrows_data:
                get_book=self.getBook_by_ID(b[0])
                design(Book(*get_book))
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break

    def f_opt6(self):
       while True:
            print(f"""\n\n\n
        ============= Retruning Book =============
        
            """)
            isbn = input('''\n
                    Enter book isbn to return:''')
            if isbn:
                self.return_book(isbn)
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break
    def f_opt7(self):
        reserve_data=self.getReservedBooks()

        while True:
            print(f"""\n\n\n
        ============= List of reserved books =============

            """)
            for b in reserve_data:
                get_book=self.getBook_by_ID(b[0])
                design(Book(*get_book))
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break
    def f_opt8(self):
       while True:
            print(f"""\n\n\n
        ============= Cancelling Reservation =============
        
            """)
            isbn = input('''\n
                    Enter book isbn to cancel:''')
            if isbn:
                self.cancel_reservation_book(isbn)
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break
    def f_opt9(self):
       while True:
            print(f"""\n\n\n
        ============= Welcome to Library  System =============

                             Retruning Book
            """)
            isbn = input('''\n
                    Enter book isbn to return:''')
            if isbn:
                self.return_book(isbn)
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break


    def f_ex(self):
        return
    def __repr__(self):
        return f"{self.f}\n {self.account}"


class Staff(User):
    b_limit = 5
    def __init__(self,f,s,dept=None,acc=None):
        super().__init__(f,s,acc)
        self.dept = dept

    def menu(self):
        while True:
            print(f"""\n\n\n
        ============= Welcome to Library  System =============

                            Staff Menu
                    1. Books Catalog
                    2. Search Book
                    3. Borrow Book
                    4. Reserve Book
                    5. My Borrowed Books
                    6. Return book
                    7. My Reservations
                    8. Cancel Reservation
                    9. Pay Fine Fee
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-9|q): ''')
            choice = {"1" :self.f_opt1,
                  "2" :self.f_opt2,
                  "3" :self.f_opt3,
                  "4" :self.f_opt4,
                  "5" :self.f_opt5,
                  "6" :self.f_opt6,
                  "7" :self.f_opt7,
                  "8" :self.f_opt8,
                  "9" :self.f_opt9,
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                choice()
            else:
                print("Try again...")

    def f_opt1(self):
        print(f"""\n\n\n
        ============= Books Catalog =============

            """)
        r=self.getBooks()
        for b in r:
            design(Book(*b))
        while True:
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break

    def f_opt2(self):
        while True:
            print(f"""\n\n\n
        ============= Search Book By =============

                    1. ISBN
                    2. Title
                    3. Auther
                    4. Publication Date(dd/mm/yyyy)
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-4|q):''')
            choice = {"1" :"isbn",
                  "2" :"title",
                  "3" :"authors",
                  "4" :"publication_date",
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')

                break
            elif choice != "invalid":
                s_txt = input('''
                    Search Book: ''')
                result=self.search(choice,s_txt)
                if result:
                    design("Search Book Results")
                    for b in result:
                        design(Book(*b))

            else:
                print("Try again...")

    def f_opt3(self):
        while True:
            print(f"""\n\n\n
        ============= For Borrowing! Find Book by =============

                    1. ISBN
                    2. Book ID
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-2|q):''')
            choice = {"1" :"isbn",
                  "2" :"bookID",
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                s_txt = input(f'''
                    Search Book by {choice}: ''')
                result=self.getBookInfo(choice,s_txt)
                if result:
                    design('''
                        Your Book Info''')

                    design(Book(*result).__repr__())
                    book=Book(*result)
                    while True:
                        design('''
                        ''')
                        print(f"""\n\n\n
                        Are you sure, you want to borrow this book?

                    1. Yes
                    2. No
                    q. Return
            """)
                        c = input('''\n
                        Select Option (1-2|q):''')
                        choice = {"1" :"Yes",
                            "2" :"No",
                            "q" :"q"}.get(c,"invalid")
                        if choice == "q":
                            print('Bye..')
                            break
                        elif choice != "invalid":
                             if choice =="Yes":
                                return self.borrow_book(book)

                        else:
                            print("Try again...")

    def f_opt4(self):
        while True:
            print(f"""\n\n\n
        ============= Find book to reserve =============

                    1. ISBN
                    2. Book ID
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-2|q):''')
            choice = {"1" :"isbn",
                  "2" :"bookID",
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                s_txt = input(f'''
                    Search Book by {choice}: ''')
                result=self.getBookInfo(choice,s_txt)
                if result:
                    design('''
                        Your Book Info''')

                    design(Book(*result).__repr__())
                    book=Book(*result)
                    while True:
                        design('''
                        ''')
                        print(f"""\n\n\n
                        Are you sure to reserve This Book?

                    1. Yes
                    2. No
                    q. Return
            """)
                        c = input('''\n
                        Select Option (1-2|q):''')
                        choice = {"1" :"Yes",
                            "2" :"No",
                            "q" :"q"}.get(c,"invalid")
                        if choice == "q":
                            print('Bye..')
                            break
                        elif choice != "invalid":
                             if choice =="Yes":
                                return self.reserve_book(book)

                        else:
                            print("Try again...")

    def f_opt5(self):
        borrows_data=self.getBorrowedBooks()

        while True:
            print(f"""\n\n\n
        ============= List of borrowed books =============
                      
            """)
            for b in borrows_data:
                get_book=self.getBook_by_ID(b[0])
                design(Book(*get_book))
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break

    def f_opt6(self):
       while True:
            print(f"""\n\n\n
        ============= Retruning Book =============

            """)
            isbn = input('''\n
                    Enter book isbn to return:''')
            if isbn:
                self.return_book(isbn)
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break
    def f_opt7(self):
        reserve_data=self.getReservedBooks()

        while True:
            print(f"""\n\n\n
        ============= List of reserved books =============

            """)
            for b in reserve_data:
                get_book=self.getBook_by_ID(b[0])
                design(Book(*get_book))
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break
    def f_opt8(self):
       while True:
            print(f"""\n\n\n
        ============= Cancelling Reservation =============
                         
            """)
            isbn = input('''\n
                    Enter book isbn to cancel:''')
            if isbn:
                self.cancel_reservation_book(isbn)
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break
    def f_opt9(self):
       while True:
            print(f"""\n\n\n
        ============= Retruning Book =============
            """)
            isbn = input('''\n
                    Enter book isbn to return:''')
            if isbn:
                self.return_book(isbn)
            c = input('''\n
                    Enter q to get back:''')
            choice = {"q" :"q"}.get(c,"invalid")
            if choice == "q":
                break

    def f_ex(self):
        return
    def __repr__(self):
        return f"{self.f}\n {self.account}"

class Librarian(User):
    def __init__(self,f,s,acc=None):
        super().__init__(f,s,acc)

    def menu(self):
        
        while True:
            print(f"""Menu for Librarian
    1. Display Books
    2. Add Book
    3. Update Book
    4. Delete Book
    5. Search Book
    6. Pending User Accounts
    7. View Reservations Details
    8. View Users Details
    q. Return

    """)
            c = input("\nSelect Option (1-8|q): ")
            choice = {"1" :self.f_opt1,
                  "2" :self.f_opt2,
                  "3" :self.f_opt3,
                  "4" :self.f_opt4,
                  "5" :self.f_opt5,
                  "6" :self.f_opt6,
                  "7" :self.f_opt7,
                  "8" :self.f_opt8,
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                choice()
            else:
                print("Try again...")

    
    def f_opt1(self):
        rows = self.getBooks()
        for book in rows:
            print(Book(*book))
        return True
        
    def f_opt2(self):
        print("option-1")
        title = input("Book Title: ")
        authors = input("Book Authors(comma seperated):")
        isbn = input("ISBN number:")
        publisher = input("Publisher: ")
        publication_date = input("Publication Date: ")
        pages = input("Total Pages: ")
        available = input("Available Copies: ")
        with self.conn:
            self.c.execute("SELECT bookID FROM books ORDER BY bookID DESC LIMIT 1")
            id = self.c.fetchone()
            bookID = id[0] + 1
            self.c.execute("INSERT INTO books VALUES(:bookID,:title,:authors,:isbn,:isbn13,:language_code,:num_pages,:publication_date,:publisher,:available)",
                            {
                                'bookID': bookID,
                                'title':title,
                                'authors':authors,
                                'isbn':isbn,
                                'isbn13':isbn,
                                'language_code':"eng",
                                'num_pages':pages,
                                'publication_date':publication_date,
                                'publisher':publisher,
                                'available':available
                            }
                        )
            self.conn.commit()
            design("New book added.")
            return True
    def f_opt3(self):
        while True:
            bookID = input('Enter the BookID you want to Update:" ')
            if bookID is not "":
                b_obj=self.getBook_by_ID(bookID)

                b=Book(*b_obj)
                print(b)
                design("Enter those values you want to change!")
                title = input("Book Title: ")
                if title == '':
                    title = b.title
                authors = input("Book Authors(comma seperated):")
                if authors == '':
                    authors = b.authors
                isbn = input("ISBN number:")
                if isbn == '':
                    isbn = b.isbn
                publisher = input("Publisher: ")
                if publisher == '':
                    publisher = b.publisher
                publication_date = input("Publication Date: ")
                if publication_date == '':
                    publication_date = b.publication_date
                pages = input("Total Pages: ")
                if pages == '':
                    pages = b.num_pages
                available = input("Available Copies: ")
                if available == '':
                    available = b.available
                language_code =input("Language Code: ")
                if language_code == '':
                    language_code = b.language_code
                print(pages if pages is not "" else b.num_pages)
                print(available if available is not "" else b.available)
                try:
                    with self.conn:
                        self.c.execute("""UPDATE books SET title=:title,authors=:authors,isbn=:isbn,language_code=:language_code,num_pages=:num_pages,publication_date=:publication_date,publisher=:publisher,available=:available
                                WHERE bookID=:bookID""",
                                {
                                'title':title,
                                'authors':authors,
                                'isbn':isbn,
                                'language_code':language_code,
                                'num_pages':pages,
                                'publication_date':publication_date,
                                'publisher':publisher,
                                'available':available,
                                'bookID':b.bookID,
                                })
                        self.conn.commit()
                        design("Book Updated successfully")
                except BaseException as e:
                    print(e)
    def f_opt4(self):
        try:
            bookID = int(input('Enter the BookID you want to delete:" '))
        except:
            print('Invalid input')
            return False
        
        try:
            with self.conn:
                self.c.execute("""DELETE from books WHERE bookID=:bookID""",
                          {'bookID':bookID})
                self.conn.commit()
                print('Book has been deleted.')
                return True
        except:
            print("Something went wrong, please try again!")
            return False
    def f_opt5(self):
        while True:
            print(f"""\n\n\n
                          Search Book By

                    1. ISBN
                    2. Title
                    3. Auther
                    q. Return
            """)
            c = input('''\n
                    Select Option (1-3|q):''')
            choice = {"1" :"isbn",
                  "2" :"title",
                  "3" :"authors",
                  "q" :"q"}.get(c,"invalid")
            if choice == "q":
                print('Bye..')

                break
            elif choice != "invalid":
                s_txt = input('''
                    Search Book: ''')
                result=self.search(choice,s_txt)
                if result:
                    design("Search Book Results")
                    for b in result:
                        design(Book(*b).__repr__())

            else:
                print("Try again...")
    def f_opt6(self):
        self.pending_user_accounts()
    def f_opt7(self):
        self.reservation_status()
    def f_opt8(self):
        self.user_details()
    def f_ex(self):
        return
    def __repr__(self):
        return f"{self.f}\n {self.account}"