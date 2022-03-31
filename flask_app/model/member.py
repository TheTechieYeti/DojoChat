from flask_app import app 
from flask_app.config.mysqlconnection import MySQLConnection
from flask import session, flash
import  pprint
from datetime import datetime, date

# NOTE: this class does not map directly to the members table and should
# not be used to interact directly with the database. this class is intended 
# as a storage area for user/room information when listing room membership 
# or identifying messages.
db="DojoChat_schema"
class Member:
    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']
        else:
            self.id = 0

        if 'room_id' in data:
            self.room_id = data['room_id']
        else:
            self.room_id = 0

        if 'user_id' in data:
            self.user_id = data['user_id']
        else:
            self.user_id = 0

        if 'first_name' in data:
            self.first_name = data['first_name']
        else:
            self.first_name = ''

        if 'last_name' in data:
            self.last_name = data['last_name']
        else:
            self.last_name = ''
