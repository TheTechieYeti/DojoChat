from contextlib import nullcontext
from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date
from flask_app.model.member import Member
from flask_app.model.user import User
from flask_app.model.room_att import Room_att


db="DojoChat_schema"
class Room:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.number = data['number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.administrator_id = data['administrator_id']
        self.subject = data['subject']
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
        query = "INSERT INTO rooms (name, administrator_id, number, passkey, subject) VALUES "\
                "(%(name)s, %(administrator_id)s, %(number)s, %(passkey)s, %(subject)s);" 
        new_room_id = MySQLConnection(db).query_db( query, data )
        # admin should automatically be member of the room??
        query = "INSERT INTO room_att (user_id, rnumber) VALUES "\
                "(%(administrator_id)s, %(number)s);" 
        room_att_q = MySQLConnection(db).query_db( query, data )

        user_id = data['administrator_id']
        number = data['number']
        new_data = {
            'room_id': number,
            'user_id': user_id,
        }
        query = "INSERT INTO members (room_id, user_id) VALUES "\
        "(%(room_id)s, %(user_id)s);"
        return MySQLConnection(db).query_db( query, new_data )

    @classmethod
    def update(cls, data):
        # NOTE: Do we allow change of admin?
        query = "UPDATE rooms SET name = %(name)s WHERE id = %(id)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def check_passkey(cls, data):
        # NOTE: Do we allow change of admin?
        query = "SELECT * FROM rooms where number = %(number)s;"
        results = MySQLConnection(db).query_db( query, data )
        check = 1
        print ('Check passkey')
        check = len(results)
        print (check)
        if id == 0:
            return -1
        else :
            return (results[0]['passkey'])
        # NOTE: commented this out - we never get here
        #return MySQLConnection(db).query_db( query, data )
    
    @classmethod
    def check_room(cls, data):
        # NOTE: Do we allow change of admin?
        query = "SELECT * FROM rooms where number = %(number)s;"
        results = MySQLConnection(db).query_db( query, data )
        check = 0
        print ('Check room in db')
        check = len(results)
        print (check)
        if check == 0:
            return -1
        else :
            return 1
        # NOTE: commented this out - we never get here
        #return MySQLConnection(db).query_db( query, data )
    
    @classmethod
    def remove_admin(cls, data):
        # NOTE: Do we allow change of admin?
        #User.update_user_info(data)
        query = "UPDATE rooms SET administrator_id = %(administrator_id)s where administrator_id = %(id)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def delete(cls, data):
        # DELETE members from the room first
        query = "DELETE FROM rooms WHERE administrator_id = %(id)s;"
        #query = "INSERT INTO rooms (administrator_id) VALUES "\
        #        "(%(administrator_id)s);"
        deleted = MySQLConnection(db).query_db( query, data )
        # NOTE: commented this out for the moment - should we keep the room
        # and keep the messages related to it??
        #query = "DELETE FROM rooms WHERE id = %(id)s;"
        #return MySQLConnection(db).query_db( query, data )
    
    @classmethod
    def delete_room(cls, data):
        # DELETE members from the room first
        query = "DELETE FROM rooms WHERE number = %(number)s;"
        #query = "INSERT INTO rooms (administrator_id) VALUES "\
        #        "(%(administrator_id)s);"
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
    def get_members_in_room (cls,data):
        query = "SELECT * FROM members where room_id = %(number)s;"
        results = MySQLConnection(db).query_db( query, data )
        check = 0
        print ('Check members in room')
        check = len(results)
        print (check)
        if check == 0:
            return -1
        else :
            return 1
        return 0

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
        if results != False:
            return Member(results[0])
        else:
            # query errored out - we don't have a good administrator
            return None
            
    @classmethod
    def get_administrator_from_room_number(cls, data):
        query = "SELECT administrator_id FROM rooms where number = %(number)s and administrator_id = %(id)s;"
        results = MySQLConnection(db).query_db( query, data )
        id = 1
        print ('#############')
        id = len(results)
        print (id)
        if id == 0:
            return -1
        else :
            return (results[0]['administrator_id'])


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

    @classmethod
    def get_all_rooms(cls):
        query = "SELECT * FROM rooms"
        results = MySQLConnection(db).query_db( query)
        my_rooms = []
        for row in results:
            print(row['number'])
            my_rooms.append( cls(row) )
        return my_rooms
        
    @classmethod
    def get_last_ten_rooms(cls):
        query = "SELECT * FROM rooms ORDER BY id DESC LIMIT 10;"
        results = MySQLConnection(db).query_db( query)
        my_rooms = []
        for row in results:
            print(row['number'])
            my_rooms.append( cls(row) )
        return my_rooms
