# Configuration Templating Language

Simple to learn but yet powerful language for templating your configuration files. It is a 'slang' of the [web2py](http://www.web2py.com)'s templating language, written from scratch and optimized for textual non-html data.

## Features

* Simple to learn - a person who has some idea of the Python syntax could dive into conftl for 15 min.

* Powerful - interpretation of python code is embedded into the templating language.

* Platform independent - tested under Linux and Windows, should work on other Unix platforms as well, Python 2.17 compatible, Python 3.x compatible. Please place an [issue](https://github.com/ttt-fifo/conftl/issues) in case you find problems with your platform of choice and I will try to help.

* Performance - minimal code base optimized for performance.

* Command line tool for rendering.

* Different methods for trigerring rendering from Python code.

* Suitable for system administration, devops and similar roles.

## Templating Kickstart

* **Clear text from the template is printed to the output as is**

```
lorem ipsum dolor sim amet
text clear lorem ipsum
```

will go exactly the same into the output

```
lorem ipsum dolor sim amet
text clear lorem ipsum
```

* **Python code in template should be written using tags** ```{{ ...code... }}```

For example if you would like to assign a value ```3``` to ```i```, you can do it using the following syntax:

```{{i = 3}}```

You could also write multiline Python code as well - like the following example:

```
{{
import sys

def one():
    return 1

i = 3
}}
```

* **Printing a variable value to the output** is done by wrapping the variable in tags and placing = sign in front of the variable like this ```{{=myvar}}```

For example if ```i``` has the value of ```3``` and you put in template:

```{{=i}}```

you will receive in the output:

```3```

* **Combining a Python code block with clear text and variable value outputs** - you should not indent the code block as you normaly do with Python, but you should determine it with ```{{pass}}``` special keyword.

Whenever you write a code block into the original Python interpreter you indent the code. Lets take the following example of original Python code block:

```
for i in range(0, 2):
    print('X', i)
```

The equivalent of the above code block using the template language would be:

```
{{for i in range(0, 2):}}
X {{=i}}
{{pass}}
```

* **You are able to pass values to template variables from outside of the template** - this is just a reminder for you to know that there are multiple methods to give 'context' to the template, e.g. assigning variable values outside of the template. About this - look the follow up sections.

## Command Line Tool for Rendering

* **The render command line tool works as follows:**

```
render -i templatename.tmpl -o filename.conf
```

will take the template from file ```templatename.tmpl``` and write the output to ```filename.conf```

WARNING: filename.conf will be overwriten!!!

In case input template is not given with -i, you would be expected to place template code on stdin.

NOTE: For Linux and other Unix systems write template code and finish it with Ctr + D
      For Windows finish it with Ctr + z and then hit ENTER

In case output filename is not given, the output will be written to stdout.

* **Giving context variables on the command line**

For example if you want to give ```i``` value of ```4``` and to use it into your template, use -c flag:

```
render -i templatename.tmpl -o filename.conf -c i=4
```

For assigning values to multiple variables, just repeat -c flag multiple times:

```
render -i templatename.tmpl -o filename.conf -c i=4 -c j=8 -c x=2
```

* **See render -h for the full set of options***

```
$ bin/render -h

Usage:

render -h
render [-i infile.tmpl] [-o outfile.conf] [-d "{% %}"] [-c i=3] [-c j=4] ...

Options:

-i or --infile
Input template, if not given you should provide the template code on stdin.

-o or --outfile
Output file, if not given the result will go to stdout.
WARNING: the contents of outfile will be overwritten.

-d or --delimiters
Template delimiters, defaults are "{{ }}"

-c or --context
Context variable. You can repeat this option to give
multiple context variables.

-h or --help
Prints current help screen.
```
