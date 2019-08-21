"""
Default conftl configurations.
The changes here will reflect globally conftl.
Example:

delimiters = {% %}

will change default delimiters for the command line tool and also
for the Python API.
"""
# Needed for getting home path
import os

# Default delimiters
DELIMITERS = "{{ }}"

# Default search path for templates
TEMPLATE_PATH = ["%s/templates" % os.environ["HOME"]]
