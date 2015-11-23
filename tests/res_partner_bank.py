"""Test suite around model 'res.partner.bank' form addon 'base'."""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import odooselenium


class ResPartnerBankTestCase(odooselenium.TestCase):
    def test_create(self):
        """Create then delete sample Bank Account."""
        self.ui.go_to_module('Accounting')
        self.ui.go_to_view('Accounts/Setup your Bank Accounts')

        # Create a bank account.
        create_button = self.webdriver.find_element(
            By.XPATH,
            "//button["
            "@data-bt-testing-model_name='res.partner.bank' and "
            "@data-bt-testing-name='oe_list_add']")
        with self.ui.wait_for_ajax_load():
            create_button.click()
        # Fill in form.
        state_field = self.webdriver.find_element(
            By.XPATH,
            "//select["
            "@data-bt-testing-model_name='res.partner.bank' and "
            "@data-bt-testing-name='state']")
        state_field.send_keys(Keys.DOWN)
        state_field.send_keys(Keys.TAB)

        acc_number_field = self.webdriver.find_element(
            By.XPATH,
            "//input["
            "@data-bt-testing-model_name='res.partner.bank' and "
            "@data-bt-testing-name='acc_number']")
        acc_number_field.send_keys('200')

        bank_name_field = self.webdriver.find_element(
            By.XPATH,
            "//input["
            "@data-bt-testing-model_name='res.partner.bank' and "
            "@data-bt-testing-name='bank_name']")
        bank_name_field.send_keys('TestBank')

        save_button = self.webdriver.find_element(
            By.XPATH,
            "//button["
            "@data-bt-testing-model_name='res.partner.bank' and "
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
