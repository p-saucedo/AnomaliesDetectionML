from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt

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

    create_img(data = ret.json())

    return ret.json()

def create_img(data):
    print(data)
    x_values = data['x_values']
    for sensor in data:
        if sensor != 'x_values':
            plt.plot(x_values, data[sensor],'o', label = sensor)
    plt.legend(loc='best')
    plt.savefig('static/imgs/visualization.png')
    return

if __name__ == "__main__":
    app.run(debug = True)