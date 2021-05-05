from flask import Flask, jsonify, request
from rPi import RPi
import numpy as np
from utils import *

app = Flask(__name__)
STARTING_TIME = "00:00"

def create_rpi():
    rpi = RPi()
    rpi.add_sensor("LIGHT_SENSOR", "lightsensor", 2)
    #rpi.add_sensor("TEMPERATURE_SENSOR", "temperaturesensor", 2)
    return rpi

global rpi
rpi = create_rpi()

@app.route('/')
def index():
    return 'done'

@app.route('/get_value')
def get_single_value():
    global rpi
    ret = rpi.sense()
    return jsonify(ret)

@app.route('/get_sensors')
def get_sensors():
    global rpi
    ret = rpi.get_sensors()
    l_sensors = [s.name for s in ret]
    return jsonify({'sensors': l_sensors})

@app.route('/generate_data', methods = ["POST"])
def generate_data():
    d_quantity = int(request.args['d_quantity'])
    anomalous_probability = float(request.args['anomalous_probability'])

    global rpi
    l_sensors = [s.name for s in rpi.get_sensors()]
    data = {}
    x_values = []
    labels = []

    data['sensors'] = {}
    for sensor in l_sensors:
        time = STARTING_TIME
        values = []

        probs = np.random.rand(d_quantity) * 100
        for i in range(d_quantity):
            if probs[i] < anomalous_probability:
                s = rpi.hacked_sense(hour=time)
                values.append(s[sensor])
                if sensor == l_sensors[0]:
                    x_values.append(s['hour_transformed'])
                    labels.append(1)
            else:
                s = rpi.sense(hour=time)
                values.append(s[sensor])
                if sensor == l_sensors[0]:
                    x_values.append(s['hour_transformed'])
                    labels.append(0)

            time = add_minutes_to_time(time,minutes_to_add=5)
        data['sensors'][sensor] = values

    data['x_values'] = x_values
    data['labels'] = labels

    return jsonify(data)

@app.route('/sense_real_data')
def sense_real_data():
    global rpi
    ret = rpi.sense()
    return ret

@app.route('/sense_anomalous_data')
def sense_anomalous_data():
    global rpi
    ret = rpi.hacked_sense()
    return ret

if __name__ == "__main__":
    app.run(debug=True, port=5001)