from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import rooms
from flask_app.controllers import chats

if __name__=="__main__":   
    app.run(debug=True) 