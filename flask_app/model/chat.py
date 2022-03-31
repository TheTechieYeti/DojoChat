from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date
from flask_app.model.room import Room
from flask_app.model.message import Message

db="dojochat_schema"
class Chat:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.room_id = data['room_id']
        self.room = None
        self.messages = []
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO chats room_id = %(room_id);"
        return MySQLConnection(db).query_db(query, data)

    @classmethod
    def get_all_messages_in_chat(cls, data):
        query = "SELECT * FROM messages WHERE chat_id = %(id)s;"
        results = MySQLConnection(db).query_db(query, data)
        messages = []
        for result in results:
            messages.append(Message(result))
    
    @classmethod
    def get_all_user_chats(cls, data):
        query = "SELECT * FROM chats WHERE id = %(user_id)s;"
        results = MySQLConnection(db).query_db(query, data)
        my_chats = []
        for result in results:
            my_chat = cls(result)
            my_chats.append(my_chat)
        return my_chats