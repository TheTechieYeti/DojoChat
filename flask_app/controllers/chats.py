from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.model import user

app.route('/chat/review/<int:id>')
def review_chat():
    pass