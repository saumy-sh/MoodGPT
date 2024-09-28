from flask import Blueprint
from backend.auth import login_required

routes = Blueprint("routes", __name__)

@routes.route('/dashboard')
@login_required
def home():
    # mongo.db.userinfo.insert_one({"name":"paamtil bhai"})
    return '<h1>Fuck world!!!</h1>'