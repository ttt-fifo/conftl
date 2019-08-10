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

* *Clear text from the template is printed to the output as is*

```
lorem ipsum dolor sim amet
text clear lorem ipsum
```

will go exactly the same into the output

```
lorem ipsum dolor sim amet
text clear lorem ipsum
```

* *Python code in template should be written using tags* ```{{ ...code... }}```

For example if you would like to assign a value to i, you can do it using the following syntax:

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

* *Printing a variable value to the output* is done by wrapping the variable in tags and placing = sign in gront of the variable like this ```{{=myvar}}```

For example if i has the value of 3 and you put in template:

```{{=i}}```

you will receive in the output

```3```

* *Combining a Python code block with clear text and variable value outputs* - you should not indent the code block, but you should determine it with ```{{pass}}``` special keyword.

Whenever you write a code block into the original Python interpreter it is indented. Lets take the following example of original Python code block:

```
for i in range(0, 2):
    print('X', i)
```

The equivalent of the above code block into the template language would be:

```
{{for i in range(0, 2):}}
X {{=i}}
{{pass}}
```

* *You are able to pass values to variables from outside of the template* - this is just a reminder for you to know that there are multiple methods to give 'context' to the template, e.g. assigning variable values outside of the template. About this - in the following sections.
