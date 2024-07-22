from flask_restful import Resource
from db.db import db, User, BLOB,Data
from flask import make_response,request,redirect,url_for,flash
from werkzeug.utils import secure_filename
import base64
from werkzeug.security import generate_password_hash 
import time
from datetime import datetime, timedelta

class CreateUser(Resource):
    def post(self):
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        user_type = request.form["user_type"]
        phone = request.form["phone"]
        photo = request.files["photo"]
        filename = secure_filename(photo.filename)
        mimetype = photo.mimetype
        photo_data = photo.read()
        user = User(
            name=name,
            email=email,
            password=password,
            user_type=user_type,
            phone=phone,
            photo=photo_data,
            file=filename,
            mimetype=mimetype
        )
        db.session.add(user)
        db.session.commit()
        if user_type == "Admin":
            flash("User Has Been Created, Now you are redirected to login page")
            time.sleep(5)
            return redirect(url_for('login.return_admin_login_page'))
        else:
            return redirect(url_for('login.return_user_login_page'))


class RemoveUser(Resource):
    def post(self):
        user = User.query.filter_by(id=id).first()
        if user.user_type == 'User':
            db.session.delete(user)
            db.session.commit()
class PostData(Resource):
    def post(self):
        time = datetime.now()
        date = datetime.today()
        current = request.json["current"]
        voltage = request.json["voltage"]
        frequency = request.json["frequency"]
        power = request.json["power"]
        energy = request.json["energy"]
        d = Data(time=time, date=date, current=current, voltage=voltage, frequency=frequency, power=power, energy=energy)
        db.session.add(d)
        db.session.commit()
        return {"message": "Data Transmitted Successfully"}


    
        
        