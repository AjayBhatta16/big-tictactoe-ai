from flask import Flask, render_template, request
import json
from bot import next_move

app = Flask(__name__)

@app.route('/')
def send_html():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def bot_move():
    data_str = request.data.decode()
    data = json.loads(data_str)
    return json.dumps(next_move(data["state"]))

if __name__ == '__main__':
    app.run()