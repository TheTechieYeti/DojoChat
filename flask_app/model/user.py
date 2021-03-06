from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
import re
from datetime import datetime, date
db="dojochat_schema"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username= data['username']
        self.password = data['password']
        self.logged_in = data['logged_in']
        # self.img = data['img_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    def today_date(self):
        today = date.today()
        return today.strftime("%a %b %d, %Y")
    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name
    @classmethod
    def get_logged_in_user(cls):
        data = {
            "id" : session["user_id"]
        }
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = MySQLConnection(db).query_db(query, data)
        this_user = cls(MySQLConnection(db).query_db(query,data)[0])
        return this_user
    
    @classmethod
    def logon(cls,data):
        query = "UPDATE users SET logged_in = %(on)s where id = %(id)s"
        results = MySQLConnection(db).query_db(query, data)

    @classmethod
    def get_one_user(cls, data):
        data1 = {
            "id" : data
        }
        query = "SELECT * FROM users WHERE id = %(id)s;"
        this_user_data = MySQLConnection(db).query_db(query, data1)
        this_user = cls(this_user_data[0])
        return this_user
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        all_users = []
        for i in MySQLConnection(db).query_db(query):
            print(i['first_name'])
            if i['first_name'] == None :
                print ("empty row")
            else :
                all_users.append(cls(i))
        return all_users
    @classmethod
    def create_user(cls, data): 
        print ("creating user")
        print (data)
        query = "INSERT INTO users (first_name, last_name, username, password) VALUES(%(first_name)s, %(last_name)s, %(username)s, %(password)s);"
        user = MySQLConnection(db).query_db(query, data)
        return user
    @classmethod
    def update_user(cls,data):
        print ("updating user")
        print (data)
        query = '''UPDATE users
        SET first_name = %(first_name)s, 
        last_name = %(last_name)s, 
        username = %(username)s
        WHERE id = %(id)s;'''
        return MySQLConnection(db).query_db(query, data)
    @classmethod
    def update_user_info(cls,data):
        query = '''UPDATE users
        SET first_name = %(first_name)s, 
        last_name = %(last_name)s, 
        username = %(username)s
        WHERE id = %(administrator_id)s;'''
        return MySQLConnection(db).query_db(query, data)
    @classmethod
    def get_user_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        this_user_info = MySQLConnection(db).query_db(query,data)
        if len(this_user_info) < 1:
            return False
        this_user = cls(this_user_info[0])
        return this_user
    @classmethod
    def upload_image(cls,data):
        query = '''UPDATE users 
        SET img_path = %(img_path)s
        WHERE id = %(id)s'''
        return MySQLConnection(db).query_db(query, data)
    @staticmethod
    def validate_user(user):
        is_valid = True
        if not user['first_name']:
            flash("Please enter a first name")
            is_valid = False
        elif len(user['first_name']) < 3:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if not user['last_name']:
            flash("Please enter a last name")
            is_valid = False
        elif len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not user['username']:
            flash("Please enter a first name")
            is_valid = False
        elif len(user['username']) < 3:
            flash("Username must be at least 3 characters")
        #query = "SELECT * FROM users WHERE email = %(email)s;"
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = MySQLConnection(db).query_db(query, user)
        if len(result) >= 1:
            flash("Username Already Taken!")
            is_valid=False
        return is_valid
    @staticmethod
    def validate_password(user):
        is_valid = True
        if not user['password']: #checks to make sure the user input something
            is_valid = False
            flash("Please enter a password that contains one letter, one number, and is a least 8 characters and confirm it.")
        elif len(user['password']) < 8: #checks to make sure the user input at least 8 characters
            is_valid = False
            flash("Please enter a password that is AT LEAST 8 characters and contains one letter and one number.")
        elif re.match('^[a-zA-Z]*$', user['password']): #checks if it is all letters
            is_valid = False
            flash("Please enter a password that contains ONE NUMBER, one letter, and is at least 8 characters long.")
        elif re.match('^[0-9]*$', user['password']): #checks if it is all numbers
            is_valid = False
            flash("Please enter a password that contains ONE LETTER, one number and is at least 8 characters long.")
        elif not user['confirm_password']: #checks to see if user input confirm password
            is_valid = False
            flash("Please confirm your password")
        elif user['confirm_password'] != user['password']: #if user did input confirm password, checks to see if it is the same as password
            is_valid = False
            flash("Passwords do not match. Please re-enter")
        return is_valid
    @staticmethod
    def format_date(date):
        return date.strftime("%a %b %d, %Y")