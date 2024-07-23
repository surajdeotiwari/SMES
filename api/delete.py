from flask_restful import Resource
from db.db import *
from flask import make_response,request,flash,redirect,url_for

class DeleteUser(Resource):
    def post(self):
        user_name = request.form["username"]
        user = db.get_or_404(User,user_name)
        db.session.delete(user)
        db.session.commit()
        return make_response("User has been deleted",200)

class RemoveDevice(Resource):
    def get(self):
        try:
            device_id = request.form["device_id"]
            device = Devices.query.filter_by(device_id=device_id).first()
            device_data = Data.query.filter_by(device_id=device_id).all()
            db.session.delete(device)
            db.session.delete(device_data)
            db.session.commit()
            return make_response("Device has been deleted", 200)
        except:
            return {"msg":"There has been an error"}