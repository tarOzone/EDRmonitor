from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

# init Flask instance
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    if request.method == 'GET':
        return jsonify({'method': 'get'})
    if request.method == 'POST':
        return jsonify({'method': 'post'})


if __name__ == "__main__":
    app.run('192.168.0.105', 8080, debug=True)