from flask_app import app
from flask import render_template, redirect, session, flash, request, url_for, jsonify
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.model.user import User
from flask_app.model.room import Room
from flask_app.model.member import Member
from flask_app.model.message import Message

import random

app.route('/chat/review/<int:id>')
def review_chat():
    pass

@app.route('/chat/<usr>')
def chat(usr):
        
    username = usr;
    room = request.args.get('room')
    chat_type = request.args['radio-choice']
    subject = request.args['subject']
    #print("*************") 
    #print (request.args['key'])
    if room == 0 :
        flash("please enter a different room number other than 0")
        return redirect("/dashboard",)
    data = {
        "number" : room,
    }
    check_room = Room.check_room(data)
    if check_room == 1:
        return redirect("/dashboard",)

    #x = random.randint(1,50)
    print("Random NUmber")
    print(room)
    # wil - need to add the user to the members table
    join_data = {
        'room_id': room,
        'user_id': session['user_id']
    }
    Room.join(join_data)
    # wil - i need the room object passed to chat.html so i can log messages
    if chat_type == "public":
        data = {
            "name" : chat_type,
            "administrator_id" : session['user_id'],
            "number" : room,
            "passkey" : "",
            "subject" : request.args['subject'],
        }
        this_room = Room.create(data)
        return render_template('chat.html', username=username, room=room, chat_type=chat_type,subject=subject, chat_room=this_room)
    elif chat_type == "private" :
        if request.args['key'] == "":
            flash("Enter a passkey to create a private chat room")
            return redirect("/dashboard",)
        data = {
            "name" : chat_type,
            "administrator_id" : session['user_id'],
            "number" : room,
            "passkey" : request.args['key'],
            "subject" : request.args['subject'],
        }
        this_room = Room.create(data)
        return render_template('chat.html', username=username, room=room, chat_type=chat_type,subject=subject, chat_room = this_room)
    #member.Member.insert_room_id(data)
    #Room.create(data)
    else:
        return redirect("/dashboard",)

@app.route('/join_room/<usr>/<int:room>/<chat_type>/<subject>')
def join(usr,room,chat_type,subject):
        
    username = usr;
    room = room
    chat_type = chat_type
    subject = subject
    #print("##############") 
    #print (chat_type)
    if chat_type == "private" :
        print("joining private chatroom")
        print(request.args['private_key'])
        key = request.args['private_key']
        if key == "" :
            flash("Wrong passkey, please enter the correct passkey")
            return redirect("/dashboard",)
    if username and room:
        # need to pass the whole room object to the chat page to log messages to the room
        data = {
            'number' : room
        }
        this_room = Room.get_room_by_number(data)
        # wil - need to add the user to the members table
        join_data = {
            'room_id': room,
            'user_id': session['user_id']
        }
        Room.join(join_data)
        if chat_type == "private" :
            data = {
                'number' : room,
            }
            check_key = Room.check_passkey(data)
            if check_key == key :
                print (check_key,key)
                return render_template('chat.html', username=username, room=room, chat_type=chat_type,subject=subject,chat_room=this_room)
            else :
                flash("Incorrect passkey. Please enter the right passkey")
                return redirect("/dashboard",)
        elif chat_type == "public" :
            return render_template('chat.html', username=username, room=room, chat_type=chat_type,subject=subject,chat_room=this_room)
    else:
        return redirect("/dashboard",)

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
    
@app.route('/message/log', methods=['POST'])
def log_message():
    #POST request
    if request.method == 'POST':
        print('Message to log in POST method: ')
        print(request.get_json())
        data = request.get_json()
        Message.post(data)
        return 'OK',200
    #GET request - we shouldn't get here
    else:
        message = {'greeting': 'If you got here you did something wrong!'}
        return 'OK',200
