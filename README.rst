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

Let's create a sample test...

.. code:: python

   import odooselenium


   class SampleTestCase(odooselenium.SeleniumTestCase):
       def test_sample(self):
           """User can confirm several invoices at once."""
           self.login()
           view = self.load_view('Account/Invoices')
           view.create_button.click()


****************
Project's status
****************

This project is experimental.


**********
Ressources
**********

* Documentation: https://odooselenium.readthedocs.org
* PyPI: https://pypi.python.org/pypi/odooselenium
* Code repository: https://github.com/meta-it/odooselenium
* Bugtracker: https://github.com/meta-it/odooselenium/issues
* Continuous integration: https://travis-ci.org/meta-it/odooselenium


.. _`Odoo`: https://odoo.com
.. _`Selenium`: https://pypi.python.org/pypi/selenium/
