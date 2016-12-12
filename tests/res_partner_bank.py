"""Test suite around model 'res.partner.bank' form addon 'base'."""
from selenium.webdriver.common.by import By
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
        self.ui.enter_data('state', 'res.partner.bank', 'Normal Bank Account')
        self.ui.enter_data('acc_number', 'res.partner.bank', '200')
        self.ui.enter_data('bank_name', 'res.partner.bank', 'TestBank')

        save_button = self.webdriver.find_element(
            By.XPATH,
            "//button["
            "@data-bt-testing-model_name='res.partner.bank' and "
            "@data-bt-testing-name='oe_form_button_save']"
        )
        with self.ui.wait_for_ajax_load():
            save_button.click()

        # Delete customer.
        with self.ui.wait_for_ajax_load():
            self.ui.click_more_item('Delete')
            alert = self.webdriver.switch_to_alert()
            alert.accept()
