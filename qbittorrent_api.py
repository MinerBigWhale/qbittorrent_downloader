import requests
from requests.auth import HTTPBasicAuth
from .const import CATEGORIES
from flask import Flask, request, jsonify
import json

class QBittorrentAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.username, self.password)

    def login(self):
        response = self.session.post(f"{self.base_url}/api/v2/auth/login", data={
            'username': self.username,
            'password': self.password
        })
        return response.status_code == 200

    def add_torrent(self, torrent_url, category):
        if category not in CATEGORIES:
            raise ValueError("Invalid category provided.")
        
        response = self.session.post(f"{self.base_url}/api/v2/torrents/add", data={
            'urls': torrent_url,
            'category': category
        })
        return response.status_code == 200

    def logout(self):
        self.session.post(f"{self.base_url}/api/v2/auth/logout")
        self.session.close()

app = Flask(__name__)

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(config['categories'])

@app.route('/api/add_torrent', methods=['POST'])
def add_torrent():
    data = request.json
    torrent_url = data.get('torrentUrl')
    category_name = data.get('category')

    # Find the folder for the selected category
    category = next((cat for cat in config['categories'] if cat['name'] == category_name), None)
    if not category:
        return jsonify({'message': 'Invalid category'}), 400

    # Add logic to interact with qBittorrent API here
    # Example: qbittorrent_client.add_torrent(torrent_url, save_path=category['folder'])

    return jsonify({'message': 'Torrent added successfully'})