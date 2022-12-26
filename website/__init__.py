from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sqlite3

db=SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fdskjhfaskheasiu'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    fd=open('script_creare.sql','r')
    script_creare=fd.read()
    fd.close()
    sqlCommands=script_creare.split(';')
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    for command in sqlCommands:
        try:
            cursor.execute(command)
        except sqlite3.OperationalError:
            print("Eroare in scriptul de creare a tabelelor!")
    connection.commit()
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

