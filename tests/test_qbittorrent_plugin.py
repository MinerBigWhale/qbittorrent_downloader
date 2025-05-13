import unittest
from custom_components.qbittorrent_plugin.qbittorrent_api import add_torrent

class TestQbittorrentPlugin(unittest.TestCase):

    def setUp(self):
        self.valid_url = "http://example.com/torrent"
        self.valid_category = "film"
        self.invalid_url = "invalid_url"
        self.invalid_category = "invalid_category"

    def test_add_torrent_valid(self):
        result = add_torrent(self.valid_url, self.valid_category)
        self.assertTrue(result)

    def test_add_torrent_invalid_url(self):
        result = add_torrent(self.invalid_url, self.valid_category)
        self.assertFalse(result)

    def test_add_torrent_invalid_category(self):
        result = add_torrent(self.valid_url, self.invalid_category)
        self.assertFalse(result)

    def test_add_torrent_empty_url(self):
        result = add_torrent("", self.valid_category)
        self.assertFalse(result)

    def test_add_torrent_empty_category(self):
        result = add_torrent(self.valid_url, "")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()