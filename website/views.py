from flask import request, redirect, url_for, render_template, Blueprint, flash
from flask_login import current_user, logout_user
from .models import *

views = Blueprint("views", __name__)

@views.route("/")
def index():
    posts = Post.query.order_by(Post.date).all()
    users = User.query.all()

    return render_template("index.html", user=current_user, posts=posts, users=users)

@views.route("/user", methods=["GET", "POST"])
def user():
    id = request.args.get("id")
    local_user = True
    posts = []
    user = current_user
    if request.method == "GET":
        if id:
            user = User.query.get(int(id))

            if not user:
                return redirect(url_for("views.user"))
            
            if user.id == current_user.id:
                local_user = True
            else:
                local_user = False

    elif request.method == "POST":
        if request.form.get("postbtn") == "":
            post = request.form.get("post")

            new_post = Post(data=post, user_id=user.id)
            db.session.add(new_post)
            db.session.commit()
        elif request.form.get("logout") == "":
            logout_user()
            return redirect(url_for("views.index"))
        elif request.form.get("delete") == "":
            post_id = request.form.get("id")
            post = Post.query.get(int(post_id))

            db.session.delete(post)
            db.session.commit()
    
    if not current_user.is_authenticated and not id:
        return redirect(url_for("views.index"))

    posts = Post.query.filter_by(user_id=user.id).all()
    posts.reverse()

    return render_template("user.html", user=user, posts=posts, local_user=local_user)