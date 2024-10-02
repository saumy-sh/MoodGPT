from marshmallow import Schema, fields
from datetime import datetime



class userSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
    loginedAt = fields.DateTime(missing=datetime.now())
    sessionDuration = fields.Float(missing=0)
    userMood = fields.String(missing="happy")
    activities = fields.List(fields.String, missing=[])
    badges = fields.List(fields.String, missing=[])
    total_points = fields.Integer(missing=0)
    chat_history = fields.List(fields.Dict, missing=[])


# class userSchema(UserMixin):
#     def __init__(self, user_data):
#         self._id = str(user_data.get("_id"))
#         self.username = user_data.get("username")
#         self.password = user_data.get("password")
#         self.email = user_data.get("email")
#         self.loginedAt = user_data.get("loginedAt")
#         self.sessionDuration = user_data.get("sessionDuration")
#         self.userMood = user_data.get("userMood")
#         self.activities = user_data.get("activities")
#         self.badges = user_data.get("badges")
#         self.total_points = user_data.get("total_points")
    
#     def get_id(self):
#         return self._id

#     def is_authenticated(self):
#         return True

#     def is_active(self):
#         return self.is_active

#     def is_anonymous(self):
#         return False
