# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import send_file

from garage_door import GarageDoorSensor

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({
    'echo_port': 22,
    'trigger_port': 17,
    'opener_port': 16,
    'light_port': 20,
    'threshold': 0.5
})

sensor = GarageDoorSensor(
    echo_port=app.config['echo_port'],
    trigger_port=app.config['trigger_port'],
    opener_port=app.config['opener_port'],
    light_port=app.config['light_port'],
    threshold=app.config['threshold']
)

@app.route('/garage_door', methods=['GET'])
def check_garage_door_status():
    return jsonify(0)
    # return jsonify(int(sensor.is_door_opened()) * 100)

@app.route('/open', methods=['GET'])
def open_garage_door():
    sensor.toggle('door')
    return jsonify('ok')

@app.route('/light', methods=['GET'])
def toggle_light():
    sensor.toggle('light')
    return jsonify('ok')

@app.route('/live', methods=['GET'])
def live():
    return send_file(sensor.capture(), mimetype='image/jpeg')
