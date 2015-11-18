"""Testing libraries."""
import contextlib
import unittest
import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui

from odooselenium import wait


class OdooPage(object):
    """Encapsulate DOM elements of Odoo user interface."""
    def __init__(self, webdriver):
        # WebDriver instance.
        self.webdriver = webdriver

    @property
    def create_button(self):
        return self.webdriver.find_element(
            By.XPATH,
            "//button["
            "@data-bt-testing-model_name='stock.move' and "
            "@data-bt-testing-name='oe_list_add']")


class TestCase(unittest.TestCase):
    def setUp(self):
        """Setup Selenium driver, log in."""
        self.configure()
        self.setup_webdriver()
        self.log_in()

    def tearDown(self):
        """Close the webdriver's session."""
        self.webdriver.quit()

    def configure(self, **kwargs):
        """Set :attr:`cfg`."""
        self.cfg = {
            'url': 'http://localhost:8069',
            'username': 'admin',
            'password': 'admin',
            'dbname': '',
        }
        self.cfg.update(kwargs)

    def setup_webdriver(self):
        """Set :attr:`webdriver`."""
        self.webdriver = webdriver.Firefox()

    def url(self, path=''):
        """Return complete URL."""
        return u'{base:s}/{path:s}'.format(
            base=self.cfg['url'],
            path=path.lstrip('/'),
        )

    @contextlib.contextmanager
    def assert_page_load(self):
        """Wait for full page load and assert new page has been loaded."""
        yield

    @contextlib.contextmanager
    def assert_ajax_load(self):
        """Wait for AJAX-style load and assert new page has been loaded."""
        yield
        ui.WebDriverWait(self.webdriver, 10).until(wait.jquery_inactive)

    def log_in(self):
        """Log in Odoo."""
        # Display the first page
        with self.assert_page_load():
            self.webdriver.get(self.url())

        # Fill in database selection form.
        db_field = self.webdriver.find_element(By.ID, u'db')
        with self.assert_page_load():
            if self.cfg['dbname']:  # Select database by name.
                ui.Select(db_field).select_by_value(self.cfg['dbname'])
            else:  # Select first database available.
                db_field.send_keys(Keys.DOWN)
                db_field.send_keys(Keys.TAB)

        # Fill in login form.
        login_field = self.webdriver.find_element(By.ID, u'login')
        login_field.send_keys(self.cfg['username'])
        password_field = self.webdriver.find_element(By.ID, u'password')
        password_field.send_keys(self.cfg['password'])
        login_button = self.webdriver.find_element(
            By.CSS_SELECTOR,
            '.btn-primary')
        with self.assert_page_load():
            login_button.click()

    def go_to_module(self, module_name):
        # Click on the module requested and wait until page has loaded.
        modules = self.webdriver.find_elements(
            By.CSS_SELECTOR,
            ".navbar-nav .oe_menu_text"
        )
        for module in modules:
            if module.text == module_name:
                with self.assert_ajax_load():
                    module.click()
                break
        return OdooPage(self.webdriver)

    def go_to_view(self, view_name):
        # Select all the secondary menus
        secondary_menus = self.webdriver.find_elements_by_css_selector(
            '.oe_secondary_menu')
        # Click on the view requested
        view_link = None
        for sec_menu in secondary_menus:
            if sec_menu.is_displayed():
                menus = sec_menu.find_elements(
                    By.CSS_SELECTOR,
                    ".oe_secondary_submenu .oe_menu_text"
                )
                for menu in menus:
                    if menu.text == view_name:
                        view_link = menu
                        break
                break
        assert view_link is not None, \
            "Couldn't find view menu '{0}'".format(view_name)
        with self.assert_ajax_load():
            view_link.click()
        return OdooPage(self.webdriver)

    def click_form_view_tab(self, tab_name):
        tabs = self.webdriver.find_elements(
            By.CSS_SELECTOR,
            ".ui-tabs .ui-corner-top .ui-tabs-anchor"
        )
        requested_tab = None
        for tab in tabs:
            if tab.text == tab_name:
                requested_tab = tab
                break
        assert requested_tab is not None, \
            "Couldn't find form tab '{0}'".format(tab_name)
        with self.assert_ajax_load():
            requested_tab.click()

    def click_button(self, button_name, view_name):
        button_divs = self.webdriver.find_elements_by_css_selector(
            '.oe_view_manager_buttons .oe_{}_buttons'.format(view_name))
        for button_div in button_divs:
            if button_div.is_displayed():
                # Select all the buttons on the div displayed
                buttons = button_div.find_elements_by_tag_name('button')
                # Click on the button requested
                for button in buttons:
                    # Print "Button text: ",button.text
                    if button.text == button_name:
                        with wait.wait_for_body_odoo_load(self.webdriver):
                            button.click()
                        break

    def get_url_fragments(self, url=None):
        """Return dictionary of current URL fragment.

        As an example, on detail page of invoice,
        ``self.get_url_fragments()['id']`` returns ID of current invoice.

        """
        if url is None:
            url = self.webdriver.current_url
        parsed_url = urlparse.urlparse(url)
        fragment_parts = parsed_url.fragment.split('&')
        fragment_values = {}
        for part in fragment_parts:
            key, value = part.split('=')
            fragment_values[key] = value
        return fragment_values
