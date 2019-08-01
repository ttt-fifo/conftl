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
from .core import render
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
