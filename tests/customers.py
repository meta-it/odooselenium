from selenium.webdriver.common.by import By

import odooselenium


class CustomerTestCase(odooselenium.TestCase):
    def test_customer(self):
        """Create then delete sample customer."""
        self.ui.go_to_module('Accounting')
        self.ui.go_to_view('Customers')

        # Toggle list view.
        assert self.ui.get_url_fragments()['view_type'] == u'kanban'
        list_view_button = self.webdriver.find_element(
            By.CSS_SELECTOR,
            ".oe_vm_switch_list")
        with self.ui.wait_for_ajax_load():
            list_view_button.click()
        assert self.ui.get_url_fragments()['view_type'] == u'list'

        # Create a customer.
        create_button = self.webdriver.find_element(
            By.XPATH,
            "//button["
            "@data-bt-testing-model_name='res.partner' and "
            "@data-bt-testing-name='oe_list_add']")
        with self.ui.wait_for_ajax_load():
            create_button.click()
        # Fill in form.
        name_field = self.webdriver.find_element(
            By.XPATH,
            "//input["
            "@data-bt-testing-model_name='res.partner' and "
            "@data-bt-testing-name='name']")
        name_field.send_keys('Sample customer')

        save_button = self.webdriver.find_element(
            By.XPATH,
            "//button["
            "@data-bt-testing-model_name='res.partner' and "
            "@data-bt-testing-name='oe_form_button_save']"
        )
        with self.ui.wait_for_ajax_load():
            save_button.click()

        # Delete customer.
        sidebar_buttons = self.webdriver.find_elements(
            By.CSS_SELECTOR,
            '.oe_sidebar button')
        more_button = [bt for bt in sidebar_buttons if bt.text == u'More'][0]
        more_button.click()  # "Delete" link appears in drop-down menu.
        delete_button = self.webdriver.find_element(
            By.LINK_TEXT,
            u'Delete')
        with self.ui.wait_for_ajax_load():
            delete_button.click()
            alert = self.webdriver.switch_to_alert()
            alert.accept()
