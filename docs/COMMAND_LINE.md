# Configuration Templating Language Command Line Tool

While out there many configuration management tools exist (Ansible, Salt, Chef), there are not many simple means of taking one template and converting it to a configuration file. Aiming to have a simple command line tool for templating, the ```$ render``` command line tool was created.

## Help

Running ```$ render -h``` will give the command usage and help:

```bash
$ render -h

Configuration Templating Language Renderer

Usage:

render -h
render [-i infile.tmpl] [-o outfile.conf] [-d "<% %>"] [-j context.json] [-p "search/path1, search/path2"] [-c i=3] [-c j=4] ...

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
```

## Template Debug

A template output can be seen by omiting -o option, then the output will be printed out to stdout:

```bash
$ render -i test.tmpl -c "ports=[80, 8080]"
Listen 80
Listen 8080
```

A template can be written on stdin, instead of file:

NOTE: after the last {{pass}} the template should be terminated with:

* Ctrl-D for Unix

* Ctrl-Z + Enter for Windows

```bash
$ render -c "ports=[80, 8080]"
{{for p in ports:}}
Listen {{=p}}
{{pass}}
Listen 80
Listen 80
```

## Context

Context is a dictionary, containing the variable data passed to the template.

* Giving context variables on the command line via -c

```bash
render -i template.tmpl -o configfile.conf -c i=1 -c j=2 -c k=3
```

As you can see, the -c option may be placed multiple times to give multiple variable values.

Complex datatypes must be enclosed with ""

```bash
$ render -c "mylist=[0, 1, 2]"
$ render -c "mystr='John Smith'"
```

* Context from json file

Json file example:

```bash
$ cat template.ctx
{"name": "John",
 "surname": "Smith"}
```

Passing json file data via -j option

```bash
$ render -i template.tmpl -j template.ctx
```

* Shell environment in context for convenience

The command line tool always passes the shell environment, because this is convenient to use in conjunction with shell scripts.

Example shell script:

```bash
#!/bin/bash

export DEV_ENV = 'ci_cd'
render -i template.tmpl
```

Accessing shell environment in the template via ENV dictionary like this:

```
{{
if ENV['DEV_ENVIRONMENT'] = 'ci_cd':
    port = 8080
elif ENV['DEV_ENVIRONMENT'] = 'development':
    port = 8081
elif ENV['DEV_ENVIRONMENT'] = 'production':
    port = 80
else:
    raise RuntimeError('Bad DEV_ENVIRONMENT %s' % ENV['DEV_ENVIRONMENT']) 
}}
Listen {{=port}}
```

* Context precedence

Command line option -c has precedence over the json file (-j). If you have i=3 in json file and -c i=2 on the command line, the resulting value of i will be i=2.

ENV dictionary is always included in the context, do not try to assign it from command line or json file.

## Delimiters Change

The delimiters may be changed on the command line by using -d option:

```bash
$ render -i ... -o ... -d "<% %>"
```

The default delimiters may be also changed globally by editing conftl/defaults.py

## Search Path for Templates

Adding multiple search paths using -p option:

```bash
$ render -p "/home/john/templates, /var/templates"
```

The default search path is $HOME/templates.

The default search path may be changed globally by editing conftl/defaults.py
