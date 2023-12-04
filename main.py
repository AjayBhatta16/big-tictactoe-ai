from flask import Flask, render_template, request
import json
from bot import next_move

app = Flask(__name__)

@app.route('/')
def send_html():
    return render_template('index.html')

@app.route('/v7')
def send_v7():
    return render_template('v7.html')

@app.route('/v9')
def send_v9():
    return render_template('v9.html')

@app.route('/v11')
def send_v11():
    return render_template('v11.html')

@app.route('/move', methods=['POST'])
def bot_move():
    data_str = request.data.decode()
    data = json.loads(data_str)
    return json.dumps(next_move(data["state"], data["move"]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1739)