from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date
from flask_app.model.member import Member

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
        # NOTE: Do we allow change of admin?
        query = "UPDATE rooms SET name = %(name)s WHERE id = %(id)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def delete(cls, data):
        # DELETE members from the room first
        query = "DELETE FROM members WHERE room_id = %(id)s;"
        deleted = MySQLConnection(db).query_db( query, data )
        # NOTE: commented this out for the moment - should we keep the room
        # and keep the messages related to it??
        #query = "DELETE FROM rooms WHERE id = %(id)s;"
        #return MySQLConnection(db).query_db( query, data )

    @classmethod
    def join(cls, data):
        query = "INSERT INTO members (room_id, user_id) VALUES "\
                "(%(id)s, %(user_id)s);"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def leave(cls, data):
        query = "DELETE FROM members WHERE room_id = %(id)s AND "\
                "user_id = %(user_id)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def get_members(cls, data):
        query = "SELECT u.id, u.first_name, u.last_name "\
                "LEFT JOIN members ON u.id = members.user_id "\
                "LEFT JOIN rooms ON rooms.id = members.room_id "\
                "FROM users as u WHERE u.id = %(id)s;"
        results = MySQLConnection(db).query_db( query, data )
        members = []
        for result in results:
            members.append(cls(result))
        return members

    @classmethod
    def clear_members(cls, data):
        # NOTE: don't know if you would want to do this but...
        query = "DELETE FROM members WHERE room_id = %(room_id)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def get_administrator(cls, data):
        query = "SELECT users.id as id, users.first_name as first_name, users.last_name as last_name "\
                "FROM users LEFT JOIN rooms WHERE rooms.administrator_id = %(administrator_id)s;"
        results = MySQLConnection(db).query_db( query, data )
        return Member(results[0])

    @classmethod
    def get_all_user_rooms(cls, data):
        query = "SELECT * FROM rooms LEFT JOIN members ON rooms.id = members.room_id "\
                "WHERE members.user_id = %(user_id)s;"
        results = MySQLConnection(db).query_db( query, data )
        my_rooms = []
        for result in results:
            my_room = cls(result)
            data = {
                'administrator_id' : my_room.administrator_id
            }
            my_room.administrator = Room.get_administrator(data)
            my_rooms.append(my_room)
        return my_rooms
