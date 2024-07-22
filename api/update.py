from flask_restful import Resource
from flask import request, make_response
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask import flash,redirect, url_for
from flask_login import current_user
class ChangePassword(Resource):
    def post(self):
        email = current_user.email
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, old_password):
            flash("Password has been changed successfully")
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return redirect(url_for('base.changePassword'))
        else:
            flash("Entered password is incorrect. Please enter the correct password.")
            return redirect(url_for('base.changePassword'))
