from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date

db="DojoChat_schema"
class Room:
    def __call__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.administrator_id = data['administrator_id']
        self.administrator = None
        self.members = []

    @classmethod
    def get(cls,data):
        query = "SELECT rooms WHERE id = %(id)s;"
        results = MySQLConnection(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def create(cls, data):
        # administrator id should be set in data by calling method
        query = "INSERT INTO rooms (name, administrator_id) VALUES "\
                "(%(name)s, %(administrator_id)s);" 
        new_room_id = MySQLConnection(db).query_db( query, data )
        # admin should automatically be member of the room??
        user_id = data['administrator_id']
        data = {
            'room_id': new_room_id,
            'user_id': user_id 
        }
        query = "INSERT INTO members (room_id, user_id) VALUES "\
                "(%(room_id)s, %(user_id)s);"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def update(cls, data):
        query = "UPDATE rooms SET name = %(name)s WHERE id = %(id)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def delete(cls, data):
        # DELETE members from the room first
        query = "DELETE FROM members WHERE room_id = %(id)s;"
        deleted = MySQLConnection(db).query_db( query, data )
        # now can delete the room... but do we want to do this?? if we store
        # message logs by room we can't do this??
        query = "DELETE FROM rooms WHERE id = %(id)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def join(cls, data):
        query = "INSERT INTO members (room_id, user_id) VALUES "\
                "(%(id)s, %(user_id)s);"
        return MySQLConnection(db).query_db( query, data )
