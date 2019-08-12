#!/bin/env python
"""
Example rendering template using @template(..) decorator
"""
from conftl import template


@template('nginx.conf.tmpl', delimiters="<% %>")
def add_locations(**kwarg):
    return dict(locations=kwarg)


out = add_locations(blog="192.168.43.15:8081", mail="192.168.43.15:8082")

print(out)
