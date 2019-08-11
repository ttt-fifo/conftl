#!/bin/env python
"""
Example rendering template using @template(..) decorator
"""
from conftl import template


@template('iptables.conf.tmpl')
def open_ports(*arg):
    interface = 'eth0'
    protocol = 'tcp'
    return dict(interface=interface, protocol=protocol, dports=arg)


out = open_ports(80, 8080, 443)

print(out)
