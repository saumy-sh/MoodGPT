from flask import Blueprint,render_template,session
from backend.auth import login_required


routes = Blueprint("routes", __name__)

@routes.route('/dashboard')
@login_required
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
                           total_points = session["total_points"])

@routes.route("/todo")
@login_required
def todo():
    return render_template("todo.html")