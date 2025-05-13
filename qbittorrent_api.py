import os
import json
from flask import Flask, request, jsonify, send_from_directory, redirect
import requests

app = Flask(__name__)

# Load configuration from environment variables
QB_URL = os.getenv("QB_URL", "http://localhost:8080")
QB_USERNAME = os.getenv("QB_USERNAME", "admin")
QB_PASSWORD = os.getenv("QB_PASSWORD", "adminadmin")
CATEGORIES = json.loads(os.getenv("CATEGORIES", '{}'))

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(CATEGORIES)

@app.route('/api/add_torrent', methods=['POST'])
def add_torrent():
    data = request.json
    torrent_url = data.get('torrentUrl')
    category = data.get('category')

    if category not in CATEGORIES:
        return jsonify({'message': 'Invalid category'}), 400

    response = requests.post(
        f"{QB_URL}/api/v2/torrents/add",
        data={'urls': torrent_url, 'category': category},
        auth=(QB_USERNAME, QB_PASSWORD)
    )

    if response.status_code == 200:
        return jsonify({'message': 'Torrent added successfully'})
    else:
        return jsonify({'message': 'Failed to add torrent'}), 500

@app.route('/api/active_torrents', methods=['GET'])
def list_torrents():
    response = requests.get(
        f"{QB_URL}/api/v2/torrents/info",
        auth=(QB_USERNAME, QB_PASSWORD)
    )

    if response.status_code == 200:
        torrents = response.json()
        formatted_torrents = [
            {
                'name': torrent['name'],
                'progress': torrent['progress'],
                'state': torrent['state']
            }
            for torrent in torrents
        ]
        return jsonify(formatted_torrents)
    else:
        return jsonify({'message': 'Failed to fetch torrents'}), 500

@app.route('/web_ui/<path:filename>')
def serve_static(filename):
    return send_from_directory('web_ui', filename)

@app.route('/')
def home():
    return redirect('/web_ui/index.html')


@app.before_request
def set_script_root():
    x_ingress_path = request.headers.get('X-Ingress-Path')
    if x_ingress_path:
        app.config['APPLICATION_ROOT'] = x_ingress_path
        request.environ['SCRIPT_NAME'] = x_ingress_path
        if not request.path.startswith(x_ingress_path):
            request.environ['PATH_INFO'] = x_ingress_path + request.path


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099)

