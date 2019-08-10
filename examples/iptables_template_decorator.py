#!/bin/env python
"""
Example rendering template using @template(..) decorator
"""
from conftl import template

@template('iptables_template.conf.tmpl')
def iptables(*arg):
    interface = 'eth0'
    protocol = 'tcp'
    dports = arg
    return dict(interface=interface, protocol=protocol, dports=dports)


out = iptables(80, 8080, 443)

print(out)
