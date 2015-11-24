"""Python bindings to Odoo's user interface (UI) driven by Selenium."""
import contextlib
import urlparse

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import ui

from odooselenium import wait


class OdooUI(object):
    """Encapsulate DOM elements of Odoo user interface."""
    def __init__(self, webdriver, base_url='http://localhost:8069'):
        #: Selenium WebDriver instance.
        self.webdriver = webdriver
        #: Base URL of Odoo web service.
        self.base_url = base_url

    @property
    def create_button(self):
        return self.webdriver.find_element(
            By.XPATH,
            "//button["
            "@data-bt-testing-model_name='stock.move' and "
            "@data-bt-testing-name='oe_list_add']")

    def install_module_web_selenium(self):
        """Install module web_selenium using original Odoo's UI.

        Other methods of OdooUI take advantage of features provided by
        web_selenium.

        """

    @contextlib.contextmanager
    def wait_for_page_load(self):
        """Wait for full page load and assert new page has been loaded."""
        # Inspect initial state.
        try:
            initial_body = self.webdriver.find_element(By.XPATH, '//body')
        except NoSuchElementException:  # First load.
            initial_body = None

        # Yield (back to 'with' block, where user triggers page load).
        yield

        # Wait for body to change.
        ui.WebDriverWait(self.webdriver, 10).until(
            expected_conditions.staleness_of(initial_body)
        )

    @contextlib.contextmanager
    def wait_for_ajax_load(self):
        """Wait for AJAX-style load and assert new page has been loaded."""
        # Inspect initial state.
        initial_jquery_active = not wait.jquery_inactive(self.webdriver)

        # Yield (back to 'with' block where user clicks or whatever)
        yield

        # Check state changed.
        def page_loaded(webdriver):
            # jQuery should be inactive (no AJAX pending).
            if not initial_jquery_active:
                if not wait.jquery_inactive(webdriver):
                    return False
            # Body element doesn't have class 'oe_wait'.
            try:
                webdriver.find_element(By.CSS_SELECTOR, 'body.oe_wait')
            except:
                pass
            else:
                return False
            return True

        ui.WebDriverWait(self.webdriver, 10).until(page_loaded)

    def login(self, username, password, dbname=None):
        """Log in Odoo.

        If ``dbname`` is None and there are several databases, then the first
        one is automatically selected.

        """
        # Display the first page
        self.webdriver.get(self.url())

        # Fill in database selection form.
        try:
            db_field = self.webdriver.find_element(By.ID, u'db')
        except NoSuchElementException:
            pass
        else:
            with self.wait_for_page_load():
                if dbname:  # Select database by name.
                    ui.Select(db_field).select_by_value(dbname)
                else:  # Select first database available.
                    db_field.send_keys(Keys.DOWN)
                    db_field.send_keys(Keys.TAB)

        # Fill in login form.
        login_field = self.webdriver.find_element(By.ID, u'login')
        login_field.send_keys(username)
        password_field = self.webdriver.find_element(By.ID, u'password')
        password_field.send_keys(password)
        login_button = self.webdriver.find_element(
            By.CSS_SELECTOR,
            '.btn-primary')
        with self.wait_for_page_load():
            login_button.click()

    def url(self, path=''):
        """Return complete URL."""
        return u'{base:s}/{path:s}'.format(
            base=self.base_url,
            path=path.lstrip('/'),
        )

    def go_to_module(self, module_name):
        """Click on the module in menu."""
        modules = self.webdriver.find_elements(
            By.CSS_SELECTOR,
            ".navbar-nav .oe_menu_text"
        )
        module_link = None
        for module in modules:
            if module.text == module_name:
                module_link = module
                break
        assert module_link is not None, \
            "Couldn't find module menu '{0}'".format(module_name)
        with self.wait_for_ajax_load():
            module.click()
        # Wait for application view to be loaded.
        ui.WebDriverWait(self.webdriver, 10).until(
            expected_conditions.presence_of_element_located((
                By.CSS_SELECTOR,
                '.oe_application .oe_view_manager'
            ))
        )

    def go_to_view(self, view_name):
        """Click on the view in menu."""
        # Select all the secondary menus
        secondary_menus = self.webdriver.find_elements_by_css_selector(
            '.oe_secondary_menu')
        menu_parts = view_name.split(u'/')
        searched_menu = menu_parts.pop(0)
        # Click on the view requested
        view_link = None
        for sec_menu in secondary_menus:
            if sec_menu.is_displayed():
                menus = sec_menu.find_elements(
                    By.CSS_SELECTOR,
                    ".oe_secondary_submenu .oe_menu_text"
                )
                for menu in menus:
                    if menu.text == searched_menu:
                        if menu_parts:
                            menu.click()
                            searched_menu = menu_parts.pop(0)
                        else:
                            view_link = menu
                            break
                break
        assert view_link is not None, \
            "Couldn't find view menu '{0}'".format(view_name)
        with self.wait_for_ajax_load():
            view_link.click()
        # Wait for application view to be loaded.
        ui.WebDriverWait(self.webdriver, 10).until(
            expected_conditions.presence_of_element_located((
                By.CSS_SELECTOR,
                '.oe_application .oe_view_manager'
            ))
        )

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
        with self.wait_for_ajax_load():
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
