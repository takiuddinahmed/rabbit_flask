from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from threading import Thread

from website.consume import consume_que_msg

db = SQLAlchemy()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth 
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Result 
    create_database(app)
    #consume_thread = Thread(target=consume_que_msg,daemon=True)
    #consume_thread.start()
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)