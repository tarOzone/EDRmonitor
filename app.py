import serial
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/toggle')
def toggle():
    return
    return render_template("toggle.html")


if __name__ == '__main__':
    # app.run()
    
    baud_rate = 9600
    port = 'COM8'
    try:
        with serial.Serial(port, baud_rate) as ser:
            while True:
                print(ser.readline())
    except serial.serialutil.SerialException as e:
        print(e)
