from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.model.user import User
from flask_app.model.room import Room
from flask_app.model.message import Message
from flask_app.model.member import Member

@app.route('/rooms')
def list_rooms():
    return render_template('rooms.html', rooms=Room.get_all_rooms())

@app.route('/rooms/history/<int:id>/<int:room_num>')
def room_history(id, room_num):
    data = {
        'room_id': id
    }
    return render_template('chat_history.html', room = room_num, messages = Message.get_all_by_room(data), members = Room.get_members(data))

@app.route('/rooms/members/<int:id>')
def room_members(id):
    pass
