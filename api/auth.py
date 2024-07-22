from flask_restful import Resource
from db.db import db, User, BLOB
from flask import make_response,request
from werkzeug.utils import secure_filename
import base64
from flask_wtf.file import FileField
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import LoginManager
from flask_login import UserMixin,login_user,login_required,current_user,logout_user,LoginManager
from flask import redirect, url_for, flash
from time import sleep
from datetime import datetime, timedelta
import requests
class AuthUser(Resource):
    def post(self):
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.user_type=='User':
            login_user(user)
            flash("User has been authenticated, you are free to use this website.")
            sleep(2)
            return redirect(url_for('base.home_render'))
        else:
            flash("Credential are invalid, try again...")
            return redirect(url_for('login.return_user_login_page'))
class AuthAdmin(Resource):
    def post(self):
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.user_type=='Admin':
            login_user(user)
            flash("User has been authenticated, you are free to use this website.")
            sleep(2)
            return redirect(url_for('base.home_render'))
        else:
            flash("Credential are invalid, try again...")
            return redirect(url_for('login.return_admin_login_page'))
