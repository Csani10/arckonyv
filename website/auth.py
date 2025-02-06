from flask import request, redirect, url_for, render_template, Blueprint, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import *

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.user"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:
            user_password = user.password

            if check_password_hash(user_password, password):
                login_user(user, remember=True)
                flash("Sikeres Bejelentkezés!", "success")
                return redirect(url_for("views.user"))
            else:
                flash("Hibás jelszó!", "error")
        else:
            flash("Felhasználó nem létezik!", "error")
    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.user"))

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        user2 = User.query.filter_by(email=email).first()
        if user:
            flash("A felhasználónév már létezik!", "error")
        elif user2:
            flash("Az email már létezik!", "error")
        elif len(first_name) < 2:
            flash("Keresztnév túl rövid!", "error")
        elif len(last_name) < 2:
            flash("Vezetéknév túl rövid!", "error")
        elif len(password) < 6:
            flash("A jelszónak minimum 6 karakternek kell lennie!", "error")
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash("Sikeres regisztráció!", "success")

            login_user(new_user, remember=True)

            return redirect(url_for("views.user"))
    return render_template("register.html")