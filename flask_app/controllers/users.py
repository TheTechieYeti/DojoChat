from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.config.mysqlconnection import MySQLConnection
from flask_bcrypt import Bcrypt
from flask_app.model import user
from flask_app.model import chat
from flask_app.model import room
bcrypt = Bcrypt(app)


@app.route('/')         
def log_reg():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template("popover.html")

@app.route('/register', methods=["POST"])         
def register():
    if not user.User.validate_user(request.form):
        return redirect ('/')
    #if not user.User.validate_email(request.form):
    #    return redirect ('/')
    if not user.User.validate_password(request.form):
        return redirect ('/')
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "username" : request.form["username"],
        "email" : "",
        "password" : bcrypt.generate_password_hash(request.form["password"]),
    }
    session['user_id'] = user.User.create_user(data)
    session['first_name'] = request.form["first_name"]
    session['last_name'] = request.form["last_name"]
    return redirect("/dashboard", ) 

@app.route('/dashboard')
def dashboard():
    print(session)
    if 'user_id' not in session:
        flash('You must be logged in to view this page')
        return redirect('/')
    
    data = {
        'user_id' : session['user_id']
    }
    return render_template("dashboard.html", rooms = room.Room.get_all_user_rooms(data), chats = chat.Chat.get_all_user_chats(data),user=user.User.get_logged_in_user())

@app.route('/login', methods = ["POST"])
def login():
    data = {
        "username" : request.form["username"],
    }
    print(f'this is my data from my request form {data}')
    #login_user = user.User.get_user_by_email(data)
    login_user = user.User.get_user_by_username(data)
    if not login_user:
        flash("Please check your username. No user found with that username.")
        return redirect ("/")
    if not bcrypt.check_password_hash(login_user.password, request.form["password"]):
        flash("Incorrect Password")
        return redirect ("/")
    session["user_id"] = login_user.id
    return redirect("/dashboard",)

@app.route('/user/<int:user_id>')
def display_account(user_id):
    if 'user_id' not in session:
        flash('You must be logged in to view this page')
        return redirect('/')
    
    return render_template("user.html")

@app.route('/user/<int:user_id>/edit')
def edit_user(user_id):
    if 'user_id' not in session:
        flash('You must be logged in to view this page')
        return redirect('/')
    
    return render_template("user_edit.html")

@app.route('/user/<int:user_id>/edit/process', methods = ["POST"])
def update_user(user_id):
    print(request.form)
    if not user.User.validate_user(request.form):
        return redirect (f'/user/{user_id}/edit')
    if not user.User.validate_email(request.form):
        return redirect (f'/user/{user_id}/edit')
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "username" : request.form["username"],
        "email" : "",
        "id" : user_id
    }
    user.User.update_user(data)
    return redirect(f"/user/{user_id}")

@app.route('/logout')
def logout():
    #session.pop('user_id')
    session.clear()
    return redirect("/") 
    