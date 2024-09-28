from . import mongo
from flask import Blueprint,request,jsonify,flash,session
from datetime import datetime
from backend.models import userSchema
from marshmallow import ValidationError
# from flask_login import login_user,login_required,logout_user,current_user
import bcrypt
from functools import wraps

user_schema = userSchema()
auth = Blueprint("auth", __name__)




# Login checker decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return jsonify({"message":"User is not logged in!"})
    return wrap



#user login route
@auth.route("/login",methods=['GET','PATCH'])
def login():
    login_data = request.json
    username = login_data.get("username")
    password = login_data.get("password")
    user = mongo.db.userinfo.find_one({"username":username})
    login_at = None
    if user and bcrypt.checkpw(password.encode('utf-8'),user["password"]):
        # mongo.db.userinfo.update_one(
        #     {"username":username},
        #     {"$set":{"signedIn":True}})
        # login_user(user,remember=True)
        login_at = datetime.now()
        session["logged_in"] = True
        session["username"] = username
        if request.method == 'PATCH':
            duration = user["loginedAt"] - login_at
            duration_in_days = duration.days
            if duration_in_days > 5:
                flash('You signed in after a long break, is everything ok',category="check")
            mongo.db.userinfo.update_one(
                {"username":username},
                {"$set":{"loginedAt":login_at}}
            )
        return jsonify({"message":"Login succcessful","category":"success"}),200
    else:
        return jsonify({"message":"Wrong credentials...Try again.","category":"error"}),401

        



#user signup route
@auth.route("/signup",methods=['GET','POST'])
def signup():
    try:
        user_data = request.json
        password = user_data.get("password")
        if request.method == 'POST':
            checkUser = mongo.db.userinfo.find_one({"username":user_data["username"]})
            if checkUser:
                return jsonify({"message":"Username in use!","category":"error"})
            user = user_schema.load(user_data)
            # user = userSchema(user_data)
            mongo.db.userinfo.insert_one(user)
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)
            mongo.db.userinfo.update_one(
                {"username":user_data.get("username")},
                {"$set":{"password":hashed_password}}
            )
            session["logged_in"] = True
            session["username"] = user_data["username"]
            # login_user(checkUser,remember=True)

            return jsonify({"message":"User created successfully!","category":"success"}),200
    except ValidationError as err:
        return jsonify(err.messages),400





#user logout route
@auth.route("/logout",methods=["PATCH"])
@login_required
def logout():
    user_data = request.json
    username = user_data.get("username")
    
    user = mongo.db.userinfo.find_one({"username":username})
    duration = datetime.now() - user["loginedAt"]
    print(duration)
    duration = duration.total_seconds()/60
    
    mongo.db.userinfo.update_one(
        {"username":username},
        {"$set":{"sessionDuration":duration}})
    if duration < 15:
        flash("leaving so soon",category="check")
    session.clear()
    
    return jsonify({"message":"Logged out successfully","category":"success"}),200