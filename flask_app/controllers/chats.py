from flask_app import app
from flask import render_template, redirect, session, flash, request, url_for
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.model import user

app.route('/chat/review/<int:id>')
def review_chat():
    pass

@app.route('/chat/<usr>')
def chat(usr):
    username = usr
    room = request.args.get('room')
    chat_type = request.args['radio-choice']
    print(username, room, chat_type)
    #print("##############") 
    #print (chat_type)
    if username and room:
        return render_template('chat.html', username=usr, room=room, chat_type=chat_type)
    else:
        return redirect('/dashboard')