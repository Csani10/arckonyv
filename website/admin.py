from flask import request, redirect, url_for, render_template, Blueprint, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text, CursorResult
from .models import *
import json

admin = Blueprint("admin", __name__)

def edituser(form):
    id = form.get("id")
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")
    admin = request.form.get("admin")

    user = User.query.get(int(id))

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if username:
        user.username = username
    if password:
        user.password = generate_password_hash(password)
    if admin:
        user.admin = admin
    
    db.session.commit()

def editpost(form):
    id = form.get("id")
    data = request.form.get("data")

    print(data)

    post = Post.query.get(int(id))

    if data:
        post.data = data

    db.session.commit()

def editrelatives(form):
    id = form.get("id")
    relatives = request.form.get("relatives")
    user_id = request.form.get("user_id")

    relatives_object = Relatives.query.get(int(id))

    if relatives:
        relatives_object.relatives = relatives
    if user_id:
        relatives_object.user_id = int(user_id)

    db.session.commit()

def editrelative_add(form):
    id = form.get("id")
    user1_id = request.form.get("user1_id")
    user2_id = request.form.get("user2_id")

    relative_add = RelativeAdd.query.get(int(id))

    if user1_id:
        relative_add.user1_id = int(user1_id)
    if user2_id:
        relative_add.user2_id = int(user2_id)
    
    db.session.commit()

def editmessage(form):
    id = form.get("id")
    user1_id = request.form.get("user1_id")
    user2_id = request.form.get("user2_id")
    data = request.form.get("data")

    message = Message.query.get(int(id))

    if user1_id:
        message.user1_id = int(user1_id)
    if user2_id:
        message.user2_id = int(user2_id)
    if data:
        message.data = data
    
    db.session.commit()

@admin.route("/editrow", methods=["GET", "POST"])
def editrow():
    if not current_user.admin or not current_user.is_authenticated:
        return redirect(url_for("views.index"))

    table = request.args.get("table")
    id = request.args.get("id")

    if not table:
        return redirect(url_for("admin.index"))

    if not id:
        return request(url_for("admin.index"))    

    if request.method == "POST":
        match table:
            case "user":
                edituser(request.form)
            case "post":
                editpost(request.form)
            case "relatives":
                editrelatives(request.form)
            case "relative_add":
                editrelative_add(request.form)
            case "message":
                editmessage(request.form)

    return render_template("/admin/editrow.html", table=table, id=int(id), post=Post, user=User, relative_add=RelativeAdd, relatives=Relatives, message=Message)

@admin.route("/addrow", methods=["GET", "POST"])
def addrow():
    if not current_user.admin or not current_user.is_authenticated:
        return redirect(url_for("views.index"))
    
    table = request.args.get("table")

    if not table:
        return redirect(url_for("admin.index"))

    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        admin = request.form.get("admin")
        user_id = request.form.get("user_id")
        user1_id = request.form.get("user1_id")
        user2_id = request.form.get("user2_id")
        data = request.form.get("data")
        relatives = request.form.get("relatives")

        match table:
            case "user":
                newrow = User(email=email, last_name=last_name, first_name=first_name, username=username, password=generate_password_hash(password), admin=admin)
                db.session.add(newrow)
                db.session.commit()
            case "post":
                newrow = Post(data=data, user_id=int(user_id))
                db.session.add(newrow)
                db.session.commit()
            case "relatives":
                newrow = Relatives(relatives=relatives, user_id=int(user_id))
                db.session.add(newrow)
                db.session.commit()
            case "relative_add":
                newrow = RelativeAdd(user1_id=int(user1_id), user2_id=int(user2_id))
                db.session.add(newrow)
                db.session.commit()
            case "message":
                newrow = Message(user1_id=int(user1_id), user2_id=int(user2_id), data=data)
                db.session.add(newrow)
                db.session.commit()

    return render_template("admin/addrow.html", table=table)

@admin.route("/", methods=["GET", "POST"])
def index():
    if not current_user.admin or not current_user.is_authenticated:
        return redirect(url_for("views.index"))
    
    if request.method == "POST":
        print("POST")
        print(request.form)
        if request.form.get("deleterow") == "":
            print("DELETEROW")
            table = request.form.get("table")
            id = request.form.get("id")

            match table:
                case "user":
                    row = User.query.get(int(id))
                    db.session.delete(row)
                    db.session.commit()
                case "post":
                    row = Post.query.get(int(id))
                    db.session.delete(row)
                    db.session.commit()
                case "relatives":
                    row = Relatives.query.get(int(id))
                    db.session.delete(row)
                    db.session.commit()
                case "relative_add":
                    row = RelativeAdd.query.get(int(id))
                    db.session.delete(row)
                    db.session.commit()
                case "message":
                    row = Message.query.get(int(id))
                    db.session.delete(row)
                    db.session.commit()

    rows: CursorResult = []
    table = ""

    if "table" in request.args.keys():
        table = request.args.get("table")
        rows = []
        with db.engine.connect() as conn:
            rows = conn.execute(text(f"select * from {table}"))

    return render_template("admin/index.html", rows=rows, table=table)