from contextlib import nullcontext
from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date
from flask_app.model.member import Member
from flask_app.model.user import User

db="dojochat_schema"
class Room_att:
    def __init__(self, data):
        self.id = data['id']
        self.person = data['person']
        self.rnumber = data['rnumber']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def join(cls, data):
        print ("Run join room_att query")
        query = "INSERT INTO room_att (user_id, rnumber) VALUES "\
                "(%(administrator_id)s, %(number)s);" 
        return MySQLConnection(db).query_db( query, data )
    
    @classmethod
    def remove_user(cls, data):
        query = "DELETE FROM room_att WHERE user_id = %(id)s and rnumber = %(number)s;"
        return MySQLConnection(db).query_db( query, data )

    @classmethod
    def check_room_users(cls, data):
        print ("Run join room_att query") 
        query = "SELECT * FROM room_att where rnumber = %(number)s;"
        results = MySQLConnection(db).query_db( query, data )
        #check = 0
        print ('Check users in db')
        #check = len(results)
        return (len(results))
        #if check == 0:
        #    return 0
        #else :
        #    return 1