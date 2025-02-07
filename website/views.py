from flask import request, redirect, url_for, render_template, Blueprint, flash
from flask_login import current_user, logout_user
from .models import *
import json

views = Blueprint("views", __name__)

@views.route("/")
def index():
    posts = Post.query.order_by(Post.date).all()
    posts.reverse()

    for post in posts:
        print(post.data)

    return render_template("index.html", user=current_user, posts=posts, users=User)

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
        elif request.form.get("addasrelative") == "":
            id = request.form.get("id")

            relative_add = RelativeAdd(user1_id=current_user.id, user2_id=int(id))
            db.session.add(relative_add)
            db.session.commit()
            return redirect(url_for("views.user") + f"?id={str(id)}")
        elif request.form.get("acceptasrelative") == "":
            id = request.form.get("id")
            relative_add = RelativeAdd.query.filter_by(user1_id=int(id), user2_id=current_user.id).first()
            db.session.delete(relative_add)

            relatives1 = Relatives.query.filter_by(user_id=current_user.id).first()
            json_text = json.loads(relatives1.relatives)
            json_text["relatives"].append(User.query.filter_by(id=int(id)).first().username)
            relatives1.relatives = json.dumps(json_text)

            relatives2 = Relatives.query.filter_by(user_id=int(id)).first()
            json_text = json.loads(relatives2.relatives)
            json_text["relatives"].append(User.query.filter_by(id=int(current_user.id)).first().username)
            relatives2.relatives = json.dumps(json_text)

            db.session.commit()

    if not current_user.is_authenticated and not id:
        return redirect(url_for("views.index"))

    posts = Post.query.filter_by(user_id=user.id).all()
    posts.reverse()

    relative_adds = RelativeAdd.query.filter_by(user2_id=current_user.id)

    return render_template("user.html", user=user, posts=posts, local_user=local_user, current_user=current_user, relative_add=RelativeAdd, relatives=Relatives, json=json)