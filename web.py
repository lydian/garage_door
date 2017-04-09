# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask
from flask import jsonify

from garage_door import GarageDoorSensor

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({
    'echo_port': 22,
    'trigger_port': 17,
    'threshold': 0.2
})


@app.route('/garage_door', methods=['GET'])
def check_garage_door_status():
    sensor  = GarageDoorSensor(
        echo_port=app.config['echo_port'],
        trigger_port=app.config['trigger_port'],
        threshold=app.config['threshold']
    )
    return jsonify({
        'status': 'opened' if sensor.is_door_opened() else 'closed',
        'time': datetime.now().strftime('%Y-%m-%d')
    })
