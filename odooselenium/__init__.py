"""odooselenium provides tools to interact with Odoo using Selenium."""
import pkg_resources

# API shortcuts.
from odooselenium.api import *  # NoQA


#: Module version, as defined in :pep:`396`.
__version__ = pkg_resources.get_distribution(__package__).version
