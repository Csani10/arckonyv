from flask import request, redirect, url_for, render_template, Blueprint, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text, CursorResult
from .models import *
import json

admin = Blueprint("admin", __name__)

@admin.route("/addrow", methods=["GET", "POST"])
@login_required
def addrow():
    if not current_user.admin or not current_user.is_authenticated:
        return redirect(url_for("views.index"))
    
    table = request.args.get("table")

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
        date = request.form.get("date")
        relatives = request.form.get("relatives")

        match table:
            case "user":
                newrow = User(email=email, last_name=last_name, first_name=first_name, username=username, password=generate_password_hash(password), admin=admin)
                db.session.add(newrow)
                db.session.commit()
            case "post":
                newrow = Post(data=data, user_id=user_id)
                db.session.add(newrow)
                db.session.commit()
            case "relatives":
                newrow = Relatives(relatives=relatives, user_id=user_id)
                db.session.add(newrow)
                db.session.commit()
            case "relative_add":
                newrow = RelativeAdd(user1_id=user1_id, user2_id=user2_id)
                db.session.add(newrow)
                db.session.commit()

    return render_template("admin/addrow.html", table=table)

@admin.route("/", methods=["GET", "POST"])
@login_required
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

    rows: CursorResult = []
    table = ""

    if "table" in request.args.keys():
        table = request.args.get("table")
        rows = []
        with db.engine.connect() as conn:
            rows = conn.execute(text(f"select * from {table}"))

    return render_template("admin/index.html", rows=rows, table=table)