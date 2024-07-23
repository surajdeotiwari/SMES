from flask import Blueprint,render_template,request,Response,flash,redirect,url_for,send_file, render_template_string
from jinja2 import TemplateNotFound
import requests
from flask_login import login_required, logout_user, current_user
import os
import subprocess
import tempfile
import time
page = Blueprint("base",__name__,template_folder="templates",url_prefix="/")
@page.route('/')
def home_render():
    return render_template("base.html",title="SMES - Home")

@page.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", title="SMES - Book Upload")

@page.route('/changepassword', methods=['GET','POST'])
@login_required
def changePassword():
    return render_template("changePassword.html", title="SMES - Change Password")


@page.route('data', methods=['GET','POST'])
@login_required
def userdashboard():
    return render_template("dashboard.html",title="SMES - User Dashboard")

@page.route('logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("Logout Successully")
    return redirect(url_for('login.return_user_login_page'))

@page.route('graph', methods=['GET','POST'])
@login_required
def graph():
    return render_template('graph.html',title="Dashboard")



@page.route('compile', methods=['GET', 'POST'])
@login_required
def compile_sketch():
    baud_rate = 9600
    led_pin = 2
    delay_time = 1000
    wifi_name = request.form["wifi_name"]
    password = request.form["password"]
    device_id = request.form["device_id"]
    print(wifi_name, password, device_id)
    sketch_content = render_template_string(
        open('templates/sketch_template.ino.jinja').read(),
        baud_rate=baud_rate,
        led_pin=led_pin,
        delay_time=delay_time,
        wifi_name = wifi_name,
        password = password,
        device_id=device_id
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        sketch_path = os.path.join(temp_dir, f'{temp_dir[5:]}.ino')
        with open(sketch_path, 'w') as f:
            f.write(sketch_content)
        with tempfile.TemporaryDirectory() as build_path:
            compile_command = [
                'arduino-cli', 'compile', '--fqbn', 'esp8266:esp8266:nodemcuv2',
                '--build-path', build_path, sketch_path
            ]
        result = subprocess.run(compile_command, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Compilation failed: {result.stderr}", 400
        bin_file_path = None
        for file_name in os.listdir(build_path):
            if file_name.endswith('.bin'):
                bin_file_path = os.path.join(build_path, file_name)
                break
        if not bin_file_path:
            return "Hex file not found", 500
        return send_file(bin_file_path, as_attachment=True, download_name='sketch.bin')
    
@page.route('addDevice', methods=['GET'])
@login_required
def add_device():
    # This will redirect adding the device in the database
    return render_template("add_device.html")

@page.route('manageDevice', methods=['GET'])
@login_required
def manage_device():
    return render_template("manage_device.html")