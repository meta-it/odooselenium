import time

from selenium.webdriver.support.ui import WebDriverWait


def loading_displayed(driver):
    """Return True if jQuery is enabled and inactive in web driver."""
    return driver.find_element_by_css_selector('.oe_loading').is_displayed()


def loading_hidden(driver):
    """Return True if jQuery is enabled and inactive in web driver."""
    return not loading_displayed(driver)


def jquery_inactive(driver):
    """Return True if jQuery is enabled and inactive in web driver.

    Use this method in jQuery-powered websites to make sure there is no pending
    AJAX call.

    .. code:: python

       from selenium import webdriver
       from selenium.webdriver.support.ui import WebDriverWait

       driver = webdriver.Firefox()
       WebDriverWait(driver, 10).until(jquery_inactive)

    Tip from book "Mastering Selenium WebDriver" by Mark Collin.

    """
    return driver.execute_script(
        "return (window.jQuery != null) && (jQuery.active === 0);"
    )


def wait_for(condition_function, timeout=10):
    """Wait until condition_function returns True or raise timeout exception.

    The ``condition_function`` must return a boolean.

    """
    start_time = time.time()
    while time.time() < start_time + timeout:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


class wait_for_new_page_load(object):
    """Wait for browser to load new HTML page.

    Works for body change in HTML; doesn't work with AJAX.

    """
    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        """Remember the HTML page body."""
        self.old_body = self.browser.find_element_by_tag_name('body')

    def new_page_has_loaded(self):
        """Return True if the new body was loaded."""
        if(len(self.browser.find_elements_by_tag_name('body')) == 0):
            return False
        else:
            new_body = self.browser.find_element_by_tag_name('body')
            return new_body.id != self.old_body.id

    def __exit__(self, *args):
        """Wait for new body to be loaded."""
        wait_for(self.new_page_has_loaded, 60)


class wait_for_body_odoo_load(object):
    """Wait for Odoo page loading."""
    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        """Do nothing."""

    def __exit__(self, *args):
        """Wait for the page to be loaded after doing the web action..."""
        WebDriverWait(self.browser, 10).until(jquery_inactive)
