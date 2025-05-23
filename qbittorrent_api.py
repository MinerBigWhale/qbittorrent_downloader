import os
import json
from flask import Flask, request, jsonify, send_from_directory, redirect
import requests

app = Flask(__name__)

# Load configuration from Home Assistant Add-on options
with open('/data/options.json') as options_file:
    options = json.load(options_file)

# Print the content of the options file for debugging purposes
print("Loaded options:", json.dumps(options, indent=4))

QB_URL = options.get("qbittorrent_url", "http://localhost:8080")
QB_USERNAME = options.get("qbittorrent_username", "admin")
QB_PASSWORD = options.get("qbittorrent_password", "adminadmin")
CATEGORIES = options.get("categories", {})


print("Loaded options:", json.dumps(CATEGORIES, indent=4))

@app.route('/api/categories', methods=['GET'])
def get_categories():
    global CATEGORIES
    # Extract only the 'name' attribute from each category
    category_names = [category['name'] for category in CATEGORIES]
    return jsonify(category_names)

@app.route('/api/add_torrent', methods=['POST'])
def add_torrent():
    global CATEGORIES, QB_URL, QB_USERNAME, QB_PASSWORD

    category = request.form.get('category')
    torrent_file = request.files.get('torrentFile')

    if not category:
        return jsonify({'message': 'Category is required'}), 400

    if not torrent_file:
        return jsonify({'message': 'No torrent file provided'}), 400

    # Find the category by name and get its path
    category_item = next((cat for cat in CATEGORIES if cat['name'] == category), None)
    if not category_item:
        return jsonify({'message': 'Invalid category'}), 400

    save_path = category_item['path']
    files = {'torrents': (torrent_file.filename, torrent_file.stream, torrent_file.mimetype)}

    response = requests.post(
        f"{QB_URL}/api/v2/torrents/add",
        data={'category': category, 'savepath': save_path},
        files=files,
        auth=(QB_USERNAME, QB_PASSWORD)
    )

    if response.status_code == 200:
        return jsonify({'message': 'Torrent added successfully'})
    else:
        return jsonify({'message': 'Failed to add torrent'}), 500

@app.route('/api/active_torrents', methods=['GET'])
def list_torrents():
    global QB_URL, QB_USERNAME, QB_PASSWORD
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
    x_ingress_path = request.headers.get('X-Ingress-Path', '')
    return redirect(f'{x_ingress_path}/web_ui/index.html')


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

