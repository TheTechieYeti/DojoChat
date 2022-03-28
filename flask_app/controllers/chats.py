from flask_app import app
from flask import render_template, redirect, session, flash, request, url_for
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.model.user import User
from flask_app.model.room import Room
from flask_app.model.member import Member


import random

app.route('/chat/review/<int:id>')
def review_chat():
    pass

@app.route('/chat/<usr>')
def chat(usr):
        
    username = usr;
    room = request.args.get('room')
    chat_type = request.args['radio-choice']
    #print("##############") 
    #print (chat_type)
    
    x = random.randint(1,50)
    print("Random NUmber Generator")
    print(x)
    data = {
        "name" : chat_type,
        "administrator_id" : session['user_id'],
        "number" : x,
    }
    #member.Member.insert_room_id(data)
    Room.create(data)
    if username and room:
        return render_template('chat.html', username=username, room=x, chat_type=chat_type)
    else:
        return redirect(url_for('dashboard.html'))

@app.route('/join_room/<usr>/<int:room>/<chat_type>')
def join(usr,room,chat_type):
        
    username = usr;
    room = room
    chat_type = chat_type
    #print("##############") 
    #print (chat_type)
    
    if username and room:
        return render_template('chat.html', username=username, room=room, chat_type=chat_type)
    else:
        return redirect(url_for('dashboard.html'))

@app.route('/exit_room/<int:room>')
def exit_room(room):
    admin_data = []
    data = {
        'id' : session['user_id'],
        'number' : room,
    }
    admin_data = Room.get_administrator_from_room_number(data)
    if admin_data == session['user_id']:
        print('removing admin privlage for user_id',admin_data)
        new_data = {
            'id' : session['user_id'],
            'administrator_id' : 0,
        }
        Room.remove_admin(new_data)
    else:
        print('user not admin')
    #if (admin == session['user_id']):
    #    print(admin,session['user_id'])
    #else:
    #    print(admin)
    
    #Room.delete(data)
    return redirect("/dashboard", )