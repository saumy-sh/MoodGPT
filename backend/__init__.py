from flask import Flask
from dotenv import load_dotenv
from  flask_pymongo import PyMongo
from backend.models import userSchema
import os 
# from flask_login import LoginManager



user_schema = userSchema()

mongo = PyMongo()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
URI = os.getenv("URI")

print("secret",SECRET_KEY)
print("uri",URI)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    # app.secret_key = SECRET_KEY
    app.config["MONGO_URI"] = URI
    from  .routes import routes
    from .auth import auth
    
    app.register_blueprint(routes,url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")

    mongo.init_app(app)
    
    # login_manager = LoginManager()
    # login_manager.login_view = "auth.login"
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    #     if user_data:
    #         # Instead of user_schema.load(), use the User class directly
    #         return userSchema(user_data)  # Return an instance of the User class
    #     return None

    return app

