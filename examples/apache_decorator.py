#!/bin/env python
"""
Example rendering template using @template(..) decorator
"""
from conftl import template


@template('apache.conf.tmpl')
def add_domains():
    domain = 'foo.com'
    plusdomain_map = {"fooa.com": "192.168.34.14",
                      "foob.com": "192.168.34.17"}
    return dict(domain=domain, plusdomain_map=plusdomain_map)


out = add_domains()

print(out)
