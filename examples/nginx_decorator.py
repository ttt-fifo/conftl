#!/bin/env python
"""
Example rendering template using @template(..) decorator
"""
from conftl import template


@template('nginx.conf.tmpl', delimiters="<% %>")
def add_locations():
    locations = dict(blog="192.168.43.15:8081",
                     mail="192.168.43.15:8082")
    return dict(locations=locations)


out = add_locations()

print(out)
