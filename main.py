from flask import Flask, render_template, request
import json
from bot import next_move, opp_move
from env import COLAB_URL

current_colab_url = COLAB_URL

app = Flask(__name__)

@app.route('/')
def send_html():
    return render_template('index.html')

def is_valid_url(url):
    allowed_characters = set("0123456789abcdef-")
    return all(char in allowed_characters for char in url)

@app.route('/update_colab_url', methods=['GET'])
def update_url():
    new_url = request.args.get('new_url')
    if new_url is None:
        return 'Missing new_url parameter', 400
    if not is_valid_url(new_url):
        return 'Invalid characters in new_url', 400
    current_colab_url = f"https://{new_url}.ngrok-free.app"
    print("Colab URL updated:", new_url, current_colab_url)
    return f'URL successfully updated to: {new_url}'

@app.route('/v3')
def send_v3():
    return render_template('v3.html')

@app.route('/v5')
def send_v5():
    return render_template('v5.html')

@app.route('/v7')
def send_v7():
    return render_template('v7.html')

@app.route('/v9')
def send_v9():
    return render_template('v9.html')

@app.route('/v11')
def send_v11():
    return render_template('v11.html')

@app.route('/botmode')
def send_botmode():
    return render_template('bot-vs-bot.html')

@app.route('/move', methods=['POST'])
def bot_move():
    data_str = request.data.decode()
    data = json.loads(data_str)
    return json.dumps(next_move(data["state"], data["move"], current_colab_url))

@app.route('/rit-move', methods=['POST'])
def rit_move():
    data_str = request.data.decode()
    data = json.loads(data_str)
    return json.dumps(opp_move(data["state"], current_colab_url))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1739)