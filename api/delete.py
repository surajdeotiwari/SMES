from flask_restful import Resource
from db.db import db, User
from flask import make_response,request,flash,redirect,url_for

class DeleteUser(Resource):
    def post(self):
        user_name = request.form["username"]
        user = db.get_or_404(User,user_name)
        db.session.delete(user)
        db.session.commit()
        return make_response("User has been deleted",200)
