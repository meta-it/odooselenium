############
odooselenium
############

`odooselenium` provides tools to interact with `Odoo`_ using `Selenium`_:

* base test class;
* helpers to go to module or view, click button, fill in forms...

This project's initial scope is Odoo's core features. Third-party addons can be
supported by additional projects.


*******
Example
*******

Let's write a script that creates then deletes a customer...

.. code:: python

   from selenium.webdriver import Firefox
   from selenium.webdriver.common.by import By

   import odooselenium


   webdriver = Firefox()
   ui = odooselenium.OdooUI(
       webdriver,
       base_url=u'http://localhost:8069',
   )

   # Log in.
   ui.login('myusername', 'mypassword', 'mydatabase')

   # Navigate to "Accounting / Customers".
   ui.go_to_module('Accounting')
   ui.go_to_view('Customers')

   # Toggle list view.
   assert ui.get_url_fragments()['view_type'] == u'kanban'
   list_view_button = webdriver.find_element(
       By.CSS_SELECTOR,
       ".oe_vm_switch_list")
   with ui.wait_for_ajax_load():
       list_view_button.click()
   assert ui.get_url_fragments()['view_type'] == u'list'
   # Click "Create" button.
   create_button = webdriver.find_element(
       By.XPATH,
       "//button["
       "@data-bt-testing-model_name='res.partner' and "
       "@data-bt-testing-name='oe_list_add']")
   with ui.wait_for_ajax_load():
       create_button.click()

   # Fill then submit the form.
   name_field = webdriver.find_element(
       By.XPATH,
       "//input["
       "@data-bt-testing-model_name='res.partner' and "
       "@data-bt-testing-name='name']")
   name_field.send_keys('Sample customer')
   save_button = webdriver.find_element(
       By.XPATH,
       "//button["
       "@data-bt-testing-model_name='res.partner' and "
       "@data-bt-testing-name='oe_form_button_save']"
   )
   with ui.wait_for_ajax_load():
       save_button.click()


And here is a simple test class:

.. code:: python

   import odooselenium


   class SampleTestCase(odooselenium.TestCase):
       def configure(self, **kwargs):
           """Override this method to alter settings... if necessary."""
           kwargs.setdefault('url', 'http://localhost:8069')
           kwargs.setdefault('username', 'admin')
           kwargs.setdefault('password', 'admin')
           kwargs.setdefault('dbname', 'test')
           super(SampleTestCase, self).configure(kwargs)

       def test_ui(self):
           # self.ui is instance of odooselenium.OdooUI.
           self.ui.go_to_module('Accounting')
           # self.webdriver is Selenium's webdriver.
           self.webdriver.find_element_by_css_selector('body')

See also `odooselenium`'s own tests at
https://github.com/meta-it/odooselenium/tree/master/tests


************
Installation
************

See `INSTALL <https://github.com/meta-it/odooselenium/blob/master/INSTALL>`_.


**********
Ressources
**********

* Documentation: only this README for now.
* PyPI: https://pypi.python.org/pypi/odooselenium
* Code repository: https://github.com/meta-it/odooselenium
* Bugtracker: https://github.com/meta-it/odooselenium/issues
* Continuous integration: https://travis-ci.org/meta-it/odooselenium


.. _`Odoo`: https://odoo.com
.. _`Selenium`: https://pypi.python.org/pypi/selenium/
