from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.model import user

@app.route('/room/create')
def create_room():
    pass

@app.route('/room/join/<int:id>')
def join_room(id):
    pass

@app.route('/room/leave/<int:id>')
def leave_room(id):
    pass