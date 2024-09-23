# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:37:25 2022

@author: Sadek
"""

from libaryData import LibaryData
from User import User,Student,Staff,Librarian
from Utils import design
from account import Account
from dbcon import dbCon
import os
from sys import exit

class LibManSystem():
    def __init__(self):
        data=LibaryData()
        # data.loadBooks_JsonToDb()
        LibManSystem.main()


    @staticmethod
    def main():
        # os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            welcomeMsg = '''\n\n\n
        ============= Welcome to Library  System =============

                    Please choose an option:
                    1. Login
                    2. Sign Up
                    3. Exit the Library System
                '''
            design(welcomeMsg,1)
            choice = input('''
                    Enter your choice: ''')
            if choice == '1':
                LibManSystem.login()
            elif choice == '2':
                LibManSystem.Register()

            elif choice == '3':
                design("Thank You.",1)
                exit()
            else:
                design("Invalid Choice!",1)

    @staticmethod
    def authenticate(username,password):
        try:
            a = Account.load_account(username)
        except BaseException as e:
            print(e)
            design("Please Check your username!",1)
            return False, None
        else:
            if a.password==password:
                return True, a
            else:
                design("Please Check your password!",1)
                return False, None
    @staticmethod
    def login():
        uid,password='',''
        while uid == '':
            uid = input('''
                    Enter your Username: ''')
        while password =='':
            password = input('''
                    Enter your Password: ''')
        valid, a = LibManSystem.authenticate(uid,password)
        if valid:
            if a.u_type=="Student":
                u = Student(a.f_name,a.l_name,None,a)
                u.menu()
            elif a.u_type=="Staff":
                u=Staff(a.f_name,a.l_name,None,a)
                u.menu()
            else:
                u=Librarian(a.f_name,a.l_name,a)
                u.menu()
            design("back to login",1)
        else:
            design("Login failure..",1)
    @staticmethod
    def Register():
        while True:
            f_name = input("\t\tEnter your First Name: ")
            l_name = input("\t\tEnter your Last Name: ")
            username = input("\t\tEnter your Username: ")
            password = input("\t\tEnter your Password: ")
            print('''
                Please choose an option:
                    1. Student
                    2. Staff
                    3. Librarian
                ''')
            user_type = input("\t\tEnter Your Choice(1-2): ")

            if user_type=="1":
                user_type="Student"
                class_name = input("\t\tEnter your Class Name: ")
                creation=Account.create_account(username,password,user_type,Student(f_name,l_name,class_name))
            elif user_type=="2":
                user_type="Staff"
                dept_name = input("\t\tEnter your department Name: ")
                creation=Account.create_account(username,password,user_type,Staff(f_name,l_name,dept_name))
            else:
                user_type="Librarian "
                creation=Account.create_account(username,password,user_type,Librarian(f_name,l_name))
            if creation:
                design("\n\t\tYour account created successfully!\n\t\t     And awaiting for approve")
                LibManSystem.main()






if __name__=="__main__":
    s = LibManSystem()