import json

from flask import Flask, render_template, request
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
import numpy as np


app = Flask(__name__)
global ml_model
ml_model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/retrieve_data')
def generate_data():
    url = 'http://127.0.0.1:5001/get_sensors'
    ret = requests.get(url)
    return ret.json()

@app.route('/create_data', methods=["GET", "POST"])
def create_data():
    d_quantity = request.form['dataQuantity']
    anomalous_probability = request.form['anomalousProbability']

    url = 'http://127.0.0.1:5001/generate_data'
    params = {'d_quantity':d_quantity, 'anomalous_probability':anomalous_probability}
    ret = requests.post(url, params=params)

    with open('static/data/data.json', 'w+') as fp:
        json.dump(ret.json(), fp, indent=4)

    create_img(data = ret.json())

    return render_template('visualization.html')

@app.route('/detect_anomalies', methods=["GET", "POST"])
def detect_anomalies():

    with open('static/data/data.json', 'r') as fp:
        data = json.load(fp)

    df_creator = {'hour' : data['x_values']}
    for sensor in data['sensors']:
        df_creator[sensor] = data['sensors'][sensor]
    df_creator['label'] = data['labels']

    df = pd.DataFrame(df_creator)

    data_t = df[['hour','lightsensor']]
    model = IsolationForest(contamination='auto')
    model.fit(data_t)

    global ml_model
    ml_model = model

    preds = model.predict(data_t)

    for i, pred in enumerate(preds):
        if pred == -1:
            plt.plot(data_t.iloc[i,0],data_t.iloc[i,1],'ro')
    plt.plot(data_t.hour, data_t.lightsensor, '.')

    plt.savefig('static/imgs/prediction.png')


    return render_template('predictions.html')

@app.route('/get_real_data')
def get_real_data():
    url = 'http://127.0.0.1:5001/sense_real_data'
    ret = requests.get(url)

    ret_json = ret.json()
    hour = ret_json['hour_transformed']
    X_pred = [[hour, ret_json['lightsensor']]]

    global ml_model
    prediction = ml_model.predict(X_pred)
    prediction_result = "REAL DATA" if prediction[0] == 1 else "ANOMALOUS DATA"
    text = "    Sent: REAL DATA, Validator result: {}".format(prediction_result)
    values ="    Value sent: {}".format(X_pred[0])
    return render_template('predictions.html', text= text, values = values)

@app.route('/get_anomalous_data')
def get_anomalous_data():
    url = 'http://127.0.0.1:5001/sense_anomalous_data'
    ret = requests.get(url)
    ret_json = ret.json()
    hour = ret_json['hour_transformed']
    X_pred = [[hour, ret_json['lightsensor']]]

    global ml_model
    prediction = ml_model.predict(X_pred)
    prediction_result = "REAL DATA" if prediction[0] == 1 else "ANOMALOUS DATA"
    text = "    Sent: ANOMALOUS DATA, Validator result: {}".format(prediction_result)
    values = "    Value sent: {}".format(X_pred[0])
    return render_template('predictions.html', text= text, values = values)

def create_img(data, preds = None):
    x_values = data['x_values']
    for sensor in data['sensors']:
        plt.plot(x_values, data['sensors'][sensor],'o', label = sensor)

    plt.legend(loc='best')
    plt.xlabel("Hour")
    plt.ylabel("Value sensed")
    plt.xlim([0,24])
    plt.savefig('static/imgs/visualization.png')

    return

if __name__ == "__main__":
    app.run(debug = True)