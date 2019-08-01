"""
Python Dynamic Load Recipe
for Python >= 3.7
See https://github.com/ttt-fifo/python-dynamicload for details
"""
import importlib.resources

# Change your dynamic imports here --------------------------------------------
#     - As you would normally import your modules, functions, classes, etc.
#     - But you should end every import with '... as somename'
IMPORTS = """
from .template import render
from .helpers import A as A
from .helpers import BEAUTIFY as BEAUTIFY
from .helpers import BODY as BODY
from .helpers import CAT as CAT
from .helpers import CODE as CODE
from .helpers import DIV as DIV
from .helpers import EM as EM
from .helpers import FORM as FORM
from .helpers import H1 as H1
from .helpers import H2 as H2
from .helpers import H3 as H3
from .helpers import H4 as H4
from .helpers import H5 as H5
from .helpers import H6 as H6
from .helpers import HEAD as HEAD
from .helpers import HTML as HTML
from .helpers import IMG as IMG
from .helpers import INPUT as INPUT
from .helpers import LABEL as LABEL
from .helpers import LI as LI
from .helpers import METATAG as METATAG
from .helpers import OL as OL
from .helpers import OPTION as OPTION
from .helpers import P as P
from .helpers import PRE as PRE
from .helpers import SELECT as SELECT
from .helpers import SPAN as SPAN
from .helpers import STRONG as STRONG
from .helpers import TABLE as TABLE
from .helpers import TAG as TAG
from .helpers import TAGGER as TAGGER
from .helpers import TBODY as TBODY
from .helpers import TD as TD
from .helpers import TEXTAREA as TEXTAREA
from .helpers import TH as TH
from .helpers import THAED as THAED
from .helpers import TR as TR
from .helpers import UL as UL
from .helpers import XML as XML
from .helpers import I as I
from .helpers import META as META
from .helpers import LINK as LINK
from .helpers import TITLE as TITLE
"""
# End dynamic imports ---------------------------------------------------------

# Parse the import registry
REGISTRY = {}
for i in IMPORTS.split('\n'):
    if i == '':
        continue
    REGISTRY[i.split(' ')[-1]] = i
del IMPORTS
del i

# Needed for 'from mypackage import *'
__all__ = list(REGISTRY.keys())


def __getattr__(name):
    """
    Executed whenever attribute is not found
    Attempts to dynamically load attribute and return it
    """
    if REGISTRY.get(name):
        # Attempts to load dynamically from REGISTRY
        try:
            exec(REGISTRY[name], globals(), globals())
            REGISTRY[name] = eval(name)
            return REGISTRY[name]
        except Exception:
            print(f'ERROR while attempting to dynamically load {name}:')
            raise
    elif importlib.resources.is_resource(__name__, name):
        # This is a module into the package directory, attempt to load it
        exec(f'import {__name__}.{name}', globals(), globals())
        return eval(f'{__name__}.{name}')
    else:
        # No such attribute, raise the proper exception
        raise AttributeError(f'module {__name__} has no attribute {name}')


def __dir__():
    """
    Give a hint to the end user what they could import, even the attributes
    which are still not loaded in memory.
    """
    return list(__all__)
