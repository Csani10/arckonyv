from flask import request, redirect, url_for, render_template, Blueprint, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
import json

messenger = Blueprint("messenger", __name__)

@messenger.route("/", methods=["GET"])
@login_required
def index():
    other_user_id = request.args.get("other_user_id")

    if other_user_id:
        if int(other_user_id) == current_user.id:
            return redirect(url_for("messenger.index"))
        if not User.query.get(int(other_user_id)):
            return redirect(url_for("messenger.index"))
        
        return render_template("messenger/messenger.html", other_user_id=other_user_id, current_user=current_user)
    else:
        users = {}

        relatives_json = Relatives.query.filter_by(user_id=current_user.id).first().relatives

        relatives = json.loads(relatives_json)

        print(relatives)

        for relative in relatives["relatives"]:
            users[relative] = User.query.filter_by(username=relative).first().id
    

    return render_template("messenger/index.html", users=users)

@messenger.route("/api/sendmessage", methods=["POST"])
@login_required
def sendmessage():
    body = request.get_json()
    
    user1 = body["user1_id"]
    user2 = body["user2_id"]
    data = body["data"]

    print(user1)
    print(user2)
    print(data)

    message = Message(user1_id=int(user1), user2_id=int(user2), data=data)
    db.session.add(message)
    db.session.commit()

    return "{}"

@messenger.route("/api/getmessages", methods=["GET"])
@login_required
def getmessages():
    # Validate that user1 and user2 are provided and are integers
    user1 = request.args.get("user1")
    user2 = request.args.get("user2")
    
    if not user1 or not user2 or not user1.isdigit() or not user2.isdigit():
        return jsonify({"error": "Invalid user IDs"}), 400  # Return an error if input is invalid

    user1 = int(user1)
    user2 = int(user2)

    json_ret = {
        "messages": []
    }

    # Get messages in both directions
    message1 = Message.query.filter_by(user1_id=user1, user2_id=user2).order_by(Message.date.desc()).all()
    message2 = Message.query.filter_by(user1_id=user2, user2_id=user1).order_by(Message.date.desc()).all()

    # Combine both message lists
    combined_messages = message1 + message2

    # Sort by the `date` field (newest first)
    combined_messages_sorted = sorted(combined_messages, key=lambda x: x.date, reverse=True)

    # Prepare the messages in the response format
    for msg in combined_messages_sorted:
        json_ret["messages"].append({
            "user1": msg.user1_id,
            "user2": msg.user2_id,
            "data": msg.data,
            "date": msg.date.strftime('%Y-%m-%d %H:%M:%S')  # Format date as a string
        })

    return jsonify(json_ret)  # Return the JSON response