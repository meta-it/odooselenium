"""Python bindings to Odoo's user interface (UI) driven by Selenium."""
import contextlib
import urlparse

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
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
    def wait_for_page_load(self, timeout=10):
        """Wait for full page load and assert new page has been loaded."""
        # Inspect initial state.
        try:
            initial_body = self.webdriver.find_element(By.XPATH, '//body')
        except NoSuchElementException:  # First load.
            initial_body = None

        # Yield (back to 'with' block, where user triggers page load).
        yield

        # Wait for body to change.
        ui.WebDriverWait(self.webdriver, timeout).until(
            expected_conditions.staleness_of(initial_body)
        )

    @contextlib.contextmanager
    def wait_for_ajax_load(self, timeout=10):
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

        ui.WebDriverWait(self.webdriver, timeout).until(page_loaded)

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

    def list_modules(self):
        modules = self.webdriver.find_elements(
            By.CSS_SELECTOR,
            ".navbar-nav .oe_menu_text"
        )
        return modules

    def go_to_module(self, module_name, timeout=10):
        """Click on the module in menu."""
        modules = self.list_modules()
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
        ui.WebDriverWait(self.webdriver, timeout).until(
            expected_conditions.presence_of_element_located((
                By.CSS_SELECTOR,
                '.oe_application .oe_view_manager'
            ))
        )

    def go_to_view(self, view_name, timeout=10):
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
        ui.WebDriverWait(self.webdriver, timeout).until(
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

    def click_edit(self, timeout=10):
        self.click_ajax_load_button('oe_form_button_edit', timeout)

    def click_apply(self, timeout=10):
        self.click_ajax_load_button('execute', timeout)

    def click_ajax_load_button(self, data_bt_testing_name, timeout=10):
        xpath = '//button[@data-bt-testing-name="{}"]'.format(
            data_bt_testing_name)
        buttons = self.webdriver.find_elements_by_xpath(xpath)
        visible_buttons = [b for b in buttons if b.is_displayed()]
        if len(visible_buttons) != 1:
            raise RuntimeError("Couldn't find exactly one Apply button")
        with self.wait_for_ajax_load(timeout):
            visible_buttons[0].click()

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

    def delete_from_list(self):
        """Delete items selected with select_list_items"""
        self.click_more_item('Delete')
        alert = self.webdriver.switch_to_alert()
        alert.accept()

    def get_rows_from_list(self, data_field=None, column_value=None):
        """Get the values of all rows having a specific column value.
        If data_field and column_value are not specified, get all rows."""

        headers_xpath = ('//table[@class="oe_list_content"]/thead/tr['
                         '@class="oe_list_header_columns"]/th[starts-with('
                         '@class, "oe_list_header_")]/div')

        header_values = [elem.text for elem in
                         self.webdriver.find_elements_by_xpath(headers_xpath)
                         if elem.is_displayed()]

        if data_field and column_value:
            xpath = ('//table[@class="oe_list_content"]/tbody/tr/td['
                     '@data-field="{}" and text()="{}"]/../td'.format(
                         data_field, column_value))
        else:
            xpath = '//table[@class="oe_list_content"]/tbody/tr/td'

        values = []

        all_values = self.webdriver.find_elements_by_xpath(xpath)
        chunk_size = len(header_values)
        lines = [all_values[i:i + chunk_size] for i in xrange(0,
                                                              len(all_values),
                                                              chunk_size)]
        for line in lines:
            line_values = [elem.text for elem in line]
            values.append(dict(zip(header_values, line_values)))

        return values

    def click_more_item(self, menu_item):
        """Click an item in the More menu that appears when selecting list
        items"""

        more_button = self.wait_for_visible_element_by_xpath(
            '//button[normalize-space(text())="More"]')
        more_button.click()
        item_link = self.wait_for_visible_element_by_xpath(
            '//ul[@class="oe_dropdown_menu oe_opened"]/li/a['
            'normalize-space(text())="{}"]'.format(menu_item))
        item_link.click()

    def clear_search_facets(self):
        xpath = '//div[@class="oe_searchview_clear"]'
        clear_searchview_button = self.wait_for_visible_element_by_xpath(xpath)
        with self.wait_for_ajax_load():
            clear_searchview_button.click()

    def search_for(self, search_string):
        xpath = ('//div[@class="oe_searchview_facets"]/'
                 'div[@class="oe_searchview_input"]')
        input_fields = self.webdriver.find_elements_by_xpath(xpath)
        input_field = next(field for field in input_fields
                           if field.is_displayed())
        with self.wait_for_ajax_load():
            input_field.click()
            input_field.send_keys(search_string)
            input_field.send_keys(Keys.ENTER)

    def click_list_column(self, data_field, value):
        """Click the first item with the specified value in the specified
        column in a list. Cycle through multiple pages if they're available and
        it is necessary."""

        rows = []
        while not rows:
            rows = self.get_rows_from_list(data_field, value)

            next_button_xpath = ('//div[@class="oe_list_pager"]/'
                                 'ul[@class="oe_pager_group"]/li/'
                                 'a[@data-pager-action="next"]')
            next_buttons = self.webdriver.find_elements_by_xpath(
                next_button_xpath)

            if rows:
                break
            elif not next_buttons:
                raise RuntimeError('Could not find row with {}'.format(value))
            else:
                next_buttons[0].click()

        xpath = ('//table[@class="oe_list_content"]/tbody/tr/'
                 'td[@data-field="{}" and text()="{}"]'.format(
                     data_field, value))
        elem = self.wait_for_visible_element_by_xpath(xpath)
        with self.wait_for_ajax_load():
            elem.click()

    def install_module(self, module_name, timeout=60, upgrade=False):
        """ Install the specified module. You need to be on the Settings page.
        This will NOT go through the setup wizard.
        If upgrade is True, will click the Upgrade button if the module is
        already installed."""

        with self.wait_for_ajax_load():
            self.switch_to_view('list')

        self.clear_search_facets()
        self.search_for(module_name)
        row_data = self.get_rows_from_list('shortdesc', module_name)
        if row_data[0]['Status'] == 'Installed' and upgrade is False:
            return

        self.click_list_column('shortdesc', module_name)
        btn = self.wait_for_visible_element_by_xpath(
            '//button[@class="oe_button oe_form_button oe_highlight"]')
        with self.wait_for_ajax_load(timeout):
            btn.click()

    def select_list_items(self, data_field, column_value):
        """Select items in a list view where the specified data_field has the
        specified column_value"""

        xpath = ('//table[@class="oe_list_content"]/tbody/tr/'
                 'td[@data-field="{}" and text()="{}"]/../'
                 'th[@class="oe_list_record_selector"]/input'.format(
                     data_field, column_value))
        checkboxes = self.webdriver.find_elements_by_xpath(xpath)
        for checkbox in checkboxes:
            checkbox.click()

    def switch_to_view(self, view_name):
        """Switch to list, form or kanban view

        @param view_name: should be list, form or kanban"""

        xpath = ('//ul[@class="oe_view_manager_switch oe_button_group '
                 'oe_right"]/li/a[@data-view-type="{}"]'.format(view_name))
        button = self.wait_for_visible_element_by_xpath(xpath)
        button.click()

    def _get_bt_testing_element(self, field_name):
        xpath = '//*[@data-bt-testing-name="{}"]'.format(field_name)

        return self.wait_for_visible_element_by_xpath(xpath)

    def write_in_element(self, field_name, text, clear=True):
        """Writes text to an element
        @param field_name: data-bt-testing-name on the element
        @param text: text to enter into the field
        @clear: whether to clear the field first
        @param clear: whether to clear the field first
        @param in_dialog: whether the text field is part of a modal dialog
        """
        elem = self._get_bt_testing_element(field_name)

        if clear:
            elem.clear()

        elem.send_keys(text)

    def toggle_checkbox(self, field_name):
        """Toggles a checkbox"""
        elem = self._get_bt_testing_element(field_name)
        elem.click()

    def open_text_dropdown(self, field_name, in_dialog):
        """Open a dropdown list on a text field"""

        if in_dialog:
            xpath = '//div[@class="modal-content openerp"]'
        else:
            xpath = ''

        xpath += ('//input[@data-bt-testing-name="{}"]/../'
                  'span[@class="oe_m2o_drop_down_button"]'.format(field_name))
        elem = self.wait_for_visible_element_by_xpath(xpath)
        elem.click()

    def get_edit_field_from_label_text(self, label_text):
        """Get the editable field which belongs to a label.
        CAUTION: some labels have more than one field, but only one of them
        will be linked by ID."""

        xpath = '//tr/td/label[normalize-space(text())="{}"]'.format(
            label_text)
        label = self.webdriver.find_element_by_xpath(xpath)
        field_id = label.get_attribute('for')
        field = self.webdriver.find_element_by_id(field_id)
        return field

    def enter_data(self, field, data, search_column=None, in_dialog=False):
        """Enter data into a field. The type of field will be determined.

        @param field: the data-bt-testing-name attribute for the field
        @param data: the data to enter
        @param search_column: the column title to search in the Search form in
                              case of an autocomplete text field
        """
        input_field = self._get_bt_testing_element(field)

        if input_field.tag_name == 'select':
            dropdown_xpath = ('//div[@class="modal-content openerp"]//'
                              'select[@data-bt-testing-name="{}"]/'
                              'option[normalize-space('
                              'text())="{}"]'.format(field, data))
            input_field = self.webdriver.find_element_by_xpath(dropdown_xpath)
            input_field.click()
        elif input_field.tag_name == 'input':
            elem_class = input_field.get_attribute('class')
            elem_type = input_field.get_attribute('type')
            if (elem_type == 'text' and
                    elem_class in ['', 'oe_datepicker_master']):
                self.write_in_element(field, data)
            elif (elem_type == 'text'
                    and elem_class == 'ui-autocomplete-input'):
                self.search_text_dropdown(field, search_column, data,
                                          in_dialog)
            elif elem_type == 'checkbox':
                if input_field.is_selected() != data:
                    self.toggle_checkbox(field)
            else:
                raise NotImplementedError(
                    "I don't know how to handle {}".format(field))

    def wizard_screen(self, config_data, timeout=30):
        """Enter the specified config data in the wizard screen.
        config_data is a list of dicts. Each dict needs:
            * field: the data-bt-testing-name attribute for the field
            * value: the value to enter
            * search_column: the column title to search in the Search form in
                             case of an autocomplete text field
        """
        for config_item in config_data:
            self.enter_data(config_item['field'], config_item['value'],
                            config_item.get('search_column'), True)

        button_xpath = ('//div[@class="modal-content openerp"]//footer/'
                        'button[@data-bt-testing-name="action_next"]')
        button = self.wait_for_visible_element_by_xpath(button_xpath)
        with self.wait_for_ajax_load(timeout):
            button.click()

    def _get_data_id_from_column_title(self, column_title):
        """Get the data-id attribute based on a column title"""

        xpath = ('//table[@class="oe_list_content"]/thead/tr'
                 '[@class="oe_list_header_columns"]/th/div[normalize-space('
                 'text())="{}"]/..'.format(column_title))

        elem = self.webdriver.find_element_by_xpath(xpath)
        return elem.get_attribute('data-id')

    def search_text_dropdown(self, field_name, column_title, value, in_dialog):
        """Search through a text dropdown. If the value is already in the
        dropdown, click it. If not, go to the search form via the Search
        More... item."""

        self.open_text_dropdown(field_name, in_dialog)
        menu_items_xpath = ('//ul[contains(@class, "ui-autocomplete")]/'
                            'li[contains(@class, "ui-menu-item")]/a')
        menu_items = self.webdriver.find_elements_by_xpath(menu_items_xpath)
        try:
            elem = next(e for e in menu_items if e.text == value)
            elem.click()
            return
        except StopIteration:
            elem = next(e for e in menu_items if e.text == 'Search More...')
            with self.wait_for_ajax_load():
                elem.click()

        search_field = self._get_data_id_from_column_title(column_title)
        with self.wait_for_ajax_load():
            self.click_list_column(search_field, value)

    def wait_for_visible_element_by_xpath(self, xpath, timeout=10, attempts=2):
        """Find an element by XPath and wait until it is visible. Will try up
        to <attempts> times with a timeout of <timeout> seconds each time."""

        tries = 0
        elem = None

        while tries < attempts and elem is None:
            try:
                condition = expected_conditions.visibility_of_element_located(
                    (By.XPATH, xpath))
                elem = ui.WebDriverWait(self.webdriver,
                                        timeout).until(condition)
            except TimeoutException:
                tries += 1
                if tries == attempts:
                    raise

        return elem
