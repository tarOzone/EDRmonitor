import socket

from flask import Flask
from flask import jsonify
from flask import request

from edrmonitor.esp8266.data_reader import get_data

# init Flask instance
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    # timestamp, latitude, longitude, temp, mode, speed, distance, elapsed_time = get_data()
    # print(timestamp, latitude, longitude, temp, mode, speed, distance)

    # return render_template('index.html')
    if request.method == 'GET':
        return jsonify({'method': 'get'})
    if request.method == 'POST':
        return jsonify({'method': 'post'})


# if __name__ == "__main__":
#     hostname = socket.gethostname()
#     IPAddr = socket.gethostbyname(hostname)
#     app.run(IPAddr, 5000)
