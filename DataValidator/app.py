import json

from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
import numpy as np


app = Flask(__name__)

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
    model = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
    model.fit(data_t)
    preds = model.predict(data_t)
    print(preds)
    print(df_creator['label'])
    return render_template('visualization.html')

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