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
        # wil need this to be populated so - changed .user to .member
        member_data = {
            'user_id': self.user_id
        }
        self.member = Message.get_member(member_data)

    @classmethod
    def post(cls, data):
        query = "INSERT INTO messages (text, user_id, room_id) VALUES "\
                "(%(text)s, %(user_id)s, %(room_id)s);"
        return MySQLConnection(db).query_db(query, data)

    @classmethod
    def get(cls, data):
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        return MySQLConnection(db).query_db(query, data)

    @classmethod
    def get_member(cls, data):
        query = "SELECT id, first_name, last_name, username FROM users WHERE id = %(user_id)s;"
        results = MySQLConnection(db).query_db(query, data)
        if (results != False):
            return Member(results[0])
        else:
            # wil - this is messy but we need this not to error out, need to have
            # something in the message user field
            member_data = {
                'first-name': "unknown",
                'last-name': "user"
            }
            return Member(member_data)

    @classmethod
    def get_all_by_room(cls, data):
        query = "SELECT * FROM messages WHERE room_id = %(room_id)s;"
        results = MySQLConnection(db).query_db(query, data)
        messages = []
        for result in results:
            message = Message(result)
            messages.append(message)
        return messages
