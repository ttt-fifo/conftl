#!/bin/env python
"""
Example rendering template using render() function
"""
from conftl import render

context = dict(domain="foo.com",
               plusdomain_map={"fooa.com": "192.168.34.14",
                               "foob.com": "192.168.34.17"})

out = render('apache.conf.tmpl', context=context)

print(out)
