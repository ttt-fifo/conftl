#!/bin/env python
"""
Example rendering template using @template(..) decorator
"""
from conftl import template


@template('apache.conf.tmpl')
def add_domains(**kwarg):
    domain = 'foo.com'
    return dict(domain=domain, plusdomain_map=kwarg)


domain_map = {"fooa.com": "192.168.34.14",
              "foob.com": "192.168.34.17"}
out = add_domains(**domain_map)

print(out)
