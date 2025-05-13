# Home Assistant qBittorrent Plugin

This plugin integrates qBittorrent with Home Assistant, allowing users to manage torrent downloads directly from the Home Assistant interface. Users can input torrent URLs and categorize them into films, series, audio, or apps, which will then be downloaded to the appropriate folders.

## Features

- Add torrents via a web interface.
- Categorize torrents into films, series, audio, or apps.
- Utilizes the qBittorrent remote interface for managing downloads.

## Installation

1. Clone this repository to your Home Assistant `custom_components` directory:
   ```
   git clone https://github.com/yourusername/home-assistant-qbittorrent-plugin.git
   ```

2. Ensure that the `custom_components/qbittorrent_plugin` directory is created.

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Restart Home Assistant.

## Configuration

To configure the plugin, navigate to the Home Assistant UI and follow these steps:

1. Go to **Configuration** > **Integrations**.
2. Click on **Add Integration** and search for `qBittorrent`.
3. Enter your qBittorrent URL, username, and password.
4. Save the configuration.

## Usage

Once configured, you can access the qBittorrent web UI from the Home Assistant dashboard. Here, you can input torrent URLs and select the appropriate category for downloading.

## Categories

- **Film**: Downloads will be saved in the designated film folder.
- **Series**: Downloads will be saved in the designated series folder.
- **Audio**: Downloads will be saved in the designated audio folder.
- **App**: Downloads will be saved in the designated app folder.

## Development

If you wish to contribute to the development of this plugin, please follow these guidelines:

- Ensure that your code adheres to the existing style and conventions.
- Write unit tests for any new features or changes.
- Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.