from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date

db="dojochat_schema"
class Member:
    def __init__(self, data):
        self.id = data['id']
        self.room_id = data['room_id']
        self.user_id = data['user_id']

        if 'first_name' in data:
            self.first_name = data['first_name']
        else:
            self.first_name = ''

        if 'last_name' in data:
            self.last_name = data['last_name']
        else:
            self.last_name = ''

    @classmethod
    def insert_room_id(cls, data):
        query = "INSERT INTO members (room_id,user_id) VALUES(%(room_id)s,%(user_id)s);"
        user = MySQLConnection(db).query_db(query, data)
        return user