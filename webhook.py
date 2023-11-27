# Ignore this, its just for the Linux container
from flask import Flask, request
import subprocess
import psutil

MAIN_APP_PORT = 1739

app = Flask(__name__)

def restart_main_server():
    main_server_process = False
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'python' in process.info['name'].lower() and str(MAIN_APP_PORT) in process.info['cmdline']:
            main_server_process = process
    if main_server_process:
        main_server_process.terminate()
        main_server_process.wait()
    subprocess.run(['python', 'main.py'])

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        subprocess.run(['git', '-C', '.', 'pull'])
        restart_main_server()
        return 'Webhook received and processed.', 200

if __name__ == '__main__':
    restart_main_server()
    app.run(host='0.0.0.0', port=8069)