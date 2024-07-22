from flask_restful import Resource
from db.db import User,Data
from flask import request,Response,jsonify,flash,redirect,url_for
import requests
from flask_login import login_required,current_user
class GetUserList(Resource):
    # API endpoint /getUsers
    def get(self):
        users = User.query.all()
        user_list = list()
        for user in users:
            user_list.append({
                "id": user.id,
                "name": user.name
            })
        return {"users": user_list}


class GetData(Resource):
    def get(self):
        query = Data.query.all()
        lst = []
        for q in query:
            lst.append({
                "time": q.time.strftime("%Y-%m-%d %H:%M:%S"),
                "date": q.date,  # No need to convert to string
                "current": q.current,
                "voltage": q.voltage,
                "frequency": q.frequency,
                "power": q.power,
                "energy": q.energy
            })
        return {"data": lst}
