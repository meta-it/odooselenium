"""Testing libraries."""
import unittest

from selenium import webdriver

from odooselenium.ui import OdooUI


class TestCase(unittest.TestCase):
    def setUp(self):
        """Setup Selenium driver, log in."""
        self.configure()
        self.setup_webdriver()
        #: Bindings to Odoo user interface.
        self.ui = OdooUI(self.webdriver, base_url=self.cfg['url'])
        self.ui.login(self.cfg['username'],
                      self.cfg['password'],
                      self.cfg['dbname'])

    def tearDown(self):
        """Close the webdriver's session."""
        self.webdriver.quit()

    def configure(self, **kwargs):
        """Set :attr:`cfg`."""
        self.cfg = {
            'url': 'http://localhost:8069',
            'username': 'admin',
            'password': 'admin',
            'dbname': 'test',
        }
        self.cfg.update(kwargs)

    def setup_webdriver(self):
        """Set :attr:`webdriver`."""
        self.webdriver = webdriver.Chrome()
