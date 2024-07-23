from flask_restful import Resource
from db.db import *
from flask import request,Response,jsonify,flash,redirect,url_for, render_template_string, send_file
import requests
import os
import tempfile
import subprocess
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
            print(q)
            lst.append({
                "time": q.time.strftime("%Y-%m-%d %H:%M:%S"),
                "date": q.date,  # No need to convert to string
                "current": q.current,
                "voltage": q.voltage,
                "frequency": q.frequency,
                "power": q.power,
                "energy": q.energy,
                "device_id": q.device_id
            })
        return {"data": lst}

class ListDevice(Resource):
    def get(self):
        query = Devices.query.filter_by(user_id=current_user.id).all()
        device_list = []
        for device in query:
            device_list.append(
                {
                    "owner":device.user_id,
                    "device_id":device.device_id,
                    "device_name":device.device_name,
                    "device_location":device.device_location,
                    "package": "/api/package/download",
                    "wifi_name": device.wifi_name,
                    "password": device.password
                }
            )
        return {"DeviceList":device_list}
    
class GetBinary(Resource):
    def post(self):
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
        print(sketch_content)
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