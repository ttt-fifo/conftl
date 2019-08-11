#!/bin/env python
"""
Example rendering template using render() function
"""
from conftl import render

context = dict(interface='eth1', protocol='tcp',
               dports=[80, 8080, 443])

out = render('iptables.conf.tmpl', context=context)

print(out)
