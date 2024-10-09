from flask import Blueprint,render_template,session,request,flash,url_for,current_app,jsonify,redirect
from backend.auth import login_required
from . import mongo
import pandas as pd
import os


routes = Blueprint("routes", __name__)

# todos = Blueprint("todos", __name__,template_folder="templates/activities")

@routes.route('/dashboard')
# @login_required
def dashboard():

    # for debugging purpose


    # if session :
    #     print(session)
    # else:
    #     print("no one logged in!!")
    
    return render_template("dashboard.html",
                           username = session["username"],
                           last_login = session["loginedAt"],
                           userMood = session["userMood"],
                           activities = session["activities"],
                           badges = session["badges"],
                           total_points = session["total_points"],
                           chat_history = session["chat_history"])

@routes.route("/todo",methods=['GET','POST'])
@login_required
def todo():
    username = session["username"]
    user = mongo.db.userinfo.find_one({"username" : username})
    file_path = os.path.join(current_app.root_path, 'static', 'database', 'activities.xlsx')
    df = pd.read_excel(file_path)
    todos = df.to_dict(orient='records')
    # session["todos"] = todos
    return render_template("todo.html",
                            username = username,
                            activities = user["activities"],
                            todos = todos
                           )

@routes.route("/todos",methods=['POST','GET'])
@login_required
def todos():
    # Initialize variables to handle cases where id_no is not found
    if 'title' in session:
        del session["title"]
        del session["activity_data"]
        del session["reflection_data"]
        del session["duration"]
        del session["points"]

    print(request.get_json())
    id_no = request.get_json().get('id_no')
    file_path = os.path.join(current_app.root_path, 'static', 'database', 'activities.xlsx')
    df = pd.read_excel(file_path)
    todos = df.to_dict(orient='records')
    for todo in todos:
        if todo.get("id_no") == int(id_no):
            session['title'] = todo["name"]
            session['activity_data'] = todo["activity_data"]
            session['reflection_data'] = todo["reflection_data"]
            session['points'] = todo["points"]
            session['duration'] = todo["duration"]
            break
    return jsonify({
        "message":"redirecting to new activity"})
    
# id_no = id_no,
#                            title = title,
#                            activity_data = activity_data,
#                            reflection_data = reflection_data,
#                            points = points,
#                            duration = duration


@routes.route("/activity",methods=['POST','GET'])
def activity():
    return render_template('activity.html')

@routes.route("/")
def main_page():
    return render_template("main_page.html")

@routes.route("/update_points",methods=['POST','GET'])
@login_required
def update_points():
    print(session)
    # Logic to update completed activities
    session["activities"].append(session["title"])
    
    # Logic to update the user's points in the database
    total_points = session["total_points"] + session["points"]
    session["total_points"] = total_points
    del session["title"]
    del session["activity_data"]
    del session["reflection_data"]
    del session["duration"]
    del session["points"]
    mongo.db.userinfo.update_one(
        {"username":session["username"]},
        {"$set":{
            "total_points":total_points,
            "activities":session["activities"]
        }}
    )
    
    
    flash("Points updated successfully!",category="success")
    return redirect(url_for("todo"))
     