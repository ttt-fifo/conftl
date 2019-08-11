#!/bin/env python
"""
Example rendering template using render() function
"""
from conftl import render

context = dict(locations={"blog": "192.168.43.15:8081",
                          "mail": "192.168.43.15:8082"})

out = render('nginx.conf.tmpl', context=context, delimiters="<% %>")

print(out)
