from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date
from flask_app.model.member import Member

db="DojoChat_schema"
class Message:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO messages text, chat_id, user_id VALUES "\
                "(%(text)s, %(chat_id)s, %(user_id)s);"
        return MySQLConnection(db).query_db(query, data)

    @classmethod
    def get(cls, data):
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        return MySQLConnection(db).query_db(query, data)

    @classmethod
    def get_user(cls, data):
        query = "SELECT id, first_name, last_name FROM users WHERE id = "