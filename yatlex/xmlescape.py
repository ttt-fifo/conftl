#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
xmlescape function
migrated from yaml/sanitizer.py
"""
from html import escape


def xmlescape(text, quote=True, colon=True):
    if not isinstance(text, str):
        text = str(text)
    data = escape(text, quote)
    if quote:
        data = data.replace("'", "&#x27;")
        data = data.replace('"', "&quot;")
    if colon:
        data = data.replace(':', '&#58;')
    return data
