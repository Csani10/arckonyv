from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "arckonyv.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "NIGANGIANGIANIGNIANI"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin
    from .messenger import messenger

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(messenger, url_prefix="/messenger")

    from .models import User, Post, Relatives, RelativeAdd, Message

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Database created")
