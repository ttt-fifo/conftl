#!/bin/env python
"""
render command line script for conftl rendering
"""
from __future__ import print_function
from conftl import Render
from conftl._open_infile import _open_infile
from conftl.defaults import TEMPLATE_PATH
from collections import deque
import sys
import os
import json

helpstr = """
Configuration Templating Language Renderer

Usage:

render -h
render [-i infile.tmpl] [-o outfile.conf] [-d "{% %}"] [-j context.json] \
[-p "search/path1, search/path2"] [-c i=3] [-c j=4] ...

Options:

-i or --infile
Input template, if not given you should provide the template code on stdin.

-o or --outfile
Output file, if not given the result will go to stdout.
WARNING: the contents of outfile will be overwritten.

-d or --delimiters
Template delimiters, defaults are "{{ }}".

-c or --context
Context variable. You can repeat this option to give multiple context
variables. Wrap complex datatypes with double quotes like this:
render -c "i=['complex', 'data', 'type']"

-j or --json-context
Get the context from a json file.

-p or --template-path
Search path for templates. Coma separated paths.

-h or --help
Prints current help screen.
"""

usage = """
For usage see:
render -h
"""


def parse_arg(sys_argv):
    """
    Parses sys.argv
    """

    sys_argv = deque(sys_argv)
    sys_argv.popleft()
    kwarg = {}
    while True:
        try:
            a = sys_argv.popleft()
        except IndexError:
            break

        if a.startswith('-'):
            if a == '-h' or a == '--help':
                print(helpstr, file=sys.stderr)
                exit(0)

            try:
                val = sys_argv.popleft()
            except IndexError:
                print('ERROR parsing arguments', file=sys.stderr)
                print(usage, file=sys.stderr)
                exit(1)

            if kwarg.get(a):
                kwarg[a].append(val)
            else:
                kwarg[a] = [val]

        else:
            print('ERROR parsing arguments', file=sys.stderr)
            print(usage, file=sys.stderr)
            exit(1)
    return kwarg


def get_arg_context(context):
    cmdcx = {}
    for val in context:
        cxkey, cxval = parse_context(val)
        cmdcx[cxkey] = cxval
    return cmdcx


def get_arg_json(jsonfile):
    with open(jsonfile, 'r') as f:
        cx = f.read()
    try:
        jsoncx = json.loads(cx)
    except Exception as e:
        print('ERROR getting json context from -j', file=sys.stderr)
        print(str(e), file=sys.stderr)
        exit(1)
    return jsoncx


def get_arg_path(pathstring):
    path = []
    for p in pathstring.split(','):
        p = p.strip(' ')
        path.append(p)
    return path


def arg2renderarg(kwarg):
    """
    From given arg, kwarg
    Returns: the arguments dict for Render(**renderarg)
    """

    renderarg = {}

    cmdcx = {}
    jsoncx = {}
    delimiters = None
    infile = None
    outfile = None
    path = TEMPLATE_PATH
    for k in kwarg:
        if k == '-c' or k == '--context':
            cmdcx = get_arg_context(kwarg[k])
        elif k == '-j' or k == '--json-context':
            jsoncx = get_arg_json(kwarg[k][0])
        elif k == '-d' or k == '--delimiters':
            delimiters = kwarg[k][0]
        elif k == '-i' or k == '--infile':
            infile = kwarg[k][0]
        elif k == '-o' or k == '--outfile':
            outfile = kwarg[k][0]
        elif k == '-p' or k == '--template-path':
            path = path + get_arg_path(kwarg[k][0])
        else:
            print('ERROR parsing arguments', file=sys.stderr)
            print(usage, file=sys.stderr)
            exit(1)

    renderarg['context'] = {}
    # command line has precedence over json
    renderarg['context'].update(jsoncx)
    renderarg['context'].update(cmdcx)
    # put environment in context for convenience
    renderarg['context']['ENV'] = os.environ

    renderarg['delimiters'] = delimiters

    if infile:
        renderarg['instream'] = _open_infile(infile, path)
    else:
        renderarg['instream'] = sys.stdin

    if outfile:
        renderarg['outstream'] = open(outfile, 'r')
    else:
        renderarg['outstream'] = sys.stdout

    return renderarg


def parse_context(val):
    """
    Parses one context variable
    val: should be string of type a=3
    Returns: context key, context val
    """
    try:
        cxkey, cxval = val.split('=', 1)
        cxval = eval(cxval)
    except Exception as e:
        print('ERROR parsing context variable %s' % (val), file=sys.stderr)
        print(str(e), file=sys.stderr)
        exit(1)
    return cxkey, cxval


def main():
    # get the arguments from command line
    kwarg = parse_arg(sys.argv)
    renderarg = arg2renderarg(kwarg)

    # render
    try:
        Render(**renderarg)()
    except Exception as e:
        print('ERROR in template', file=sys.stderr)
        print(str(e), file=sys.stderr)
        renderarg['instream'].close()
        renderarg['outstream'].close()
        exit(1)

    # close the streams and exit
    renderarg['instream'].close()
    renderarg['outstream'].close()
    exit(0)


if __name__ == '__main__':
    main()
