## Conftl Template Syntax


## Three General Rules

Detailed explanation of the three general rules, mentioned in the "Templating Syntax Quickstart":

**Rule 1)** Python code should be enclosed in tags ```{{...}}```

All types of Python code could be embedded by enclosing in ```{{...}}```. Python one liner assigning value to a variable is:

```python
{{myvar = 3}}
```

Multiline code is possible:

```python
{{
if i == 1:
    j = 3
else:
    j = 0
}}

The multiline code must comply to the python indentation rules. Althoug this will be valid code:

```python
{{If True:
    i = 1
else:
    i = 2}}
```

, the suggested design for better visibility of the multiline code is:

```python
{{
if True:
    i = 1
else:
    i = 2
}}
```

Python code blocks are useful for writing comments, which will be ignored in the output:

```python
{{
# This is my comment block
# with explanation what this template does.
}}
```

Arbitrary code could be incuded in ```{{...}}```. 

```python
{{
import os
import sys

def myfunct(*arg):
    return arg[1:]

class MyClass:
    pass
}}
```

NOTE: the above examples does not print anything to the output. For code blocks which print to the output see the next rule.

**Rule 2)** Python blocks must end with the keyword ```{{pass}}```

If you have code block, which should print something to the output it cannot be indented like the original Python. Take as an example this original Python code:

```python
for i in range(0, 3):
    print('X')
```

The above code may be interpreted in template syntax like this:

```python
{{for i in range(0, 3):}}
X
{{pass}}
```

You see that in template it is not possible to have an indented block, so we need to tell the interpreter where our block ends. We mark the block end with the special keyword {{pass}}

Here are some examples of Python blocks, printing to the output:

```python
TEMPLATE                   | WILL OUTPUT
------------------------------------------
{{for i in range(0, 3):}}  | Hi, there!
Hi, there!                 | Hi, there!
{{pass}}                   | Hi, there!
------------------------------------------
{{i = 0}}                  | X
{{while i <= 3:}}          | X
X                          | X
{{i += 1}}                 | X
{{pass}}                   |
----------------------------------------
{{i = None}}               | Z
{{if i == True:}}          |
X                          |
{{elif i == False:}}       |
Y                          |
{{else:}}                  |
Z                          |
{{pass}}                   |
----------------------------------------
```

Relaxed syntax. Of course, we should aim to write strictly the Python code, but sometimes we put some more spaces in front of / or trailing the expression. For this reason these patterns are **valid syntax**:

```python
{{   for i in mylist :   }}
X
{{ pass}}

{{ if j =   4  : }}
Z
{{   pass   }}
```

Here are some examples of **invalid python blocks**:

```python
INVALID           | EXPLANATION
-----------------------------------------
{{i = 0           | Block start should be
while i <= 3:}}   | always one liner.
...               |
-----------------------------------------
{{if True:}}      | No need for {{pass}}
X                 | in front of
{{pass}}          | {{else:}}
{{else:}}         | {{elif ...:}}
Y                 | {{except ...:}}
{{pass}}          | {{finally:}}
-----------------------------------------
```

**Rule 3)** Variables are printed to output enclosed in tags and prepended with = like ```{{=i}}```

What to expect when printing a variable to the output? Here are some examples:

```python
TEMPLATE                    | WILL OUTPUT
------------------------------------------
{{i = 3}}                   | 3
{{=i}}                      |
------------------------------------------
{{name = 'John'}}           | Hello, John!
Hello, {{=name}}!           |
------------------------------------------
{{                          | 2
def two():                  |
    return 2                |
}}                          |
{{=two()}}                  |
------------------------------------------
{{list = [1, 2]}}           | [1, 2]
{{=list}}                   |
------------------------------------------
```


## Puting All Together

```python
TEMPLATE                       | WILL OUTPUT
---------------------------------------------------------------
{{                             | Hello, Friend!
try:                           |
    name                       | I would like to invite you to:
Except NameError:              |   * party
    name = 'Friend'            |   * birthday
                               |   * presentation
events = [                     |
    'party',                   | Bye!
    'birthday',                |
    'presentation']            |
}}                             |
Hello, {{=name}}!              |
                               |
I would like to invite you to: |
{{for e in events:}}           |
  * {{=e}}                     |
{{pass}}                       |
                               |
Bye!                           |
---------------------------------------------------------------
```

Giving context to template - e.g. giving values to variables is possible via the command line tool or Python API. In case context is not given, the variable 'name' will have default value 'Friend'.

## Template Context

Variable values could be assigned outside of template by giving context to template via [command line](https://github.com/ttt-fifo/conftl/blob/master/docs/COMMAND_LINE.md) or via [Python API](https://github.com/ttt-fifo/conftl/blob/master/docs/PYTHON_API.md).

## Template Inheritance

One valuable feature for the web templating engines is Template Inheritance. As conftl is ment to be simple it does not implement this feature. However, similar behaviour may be implemented using Python language. See the following example:

test.tmpl:

```python
{{from conftl import render}}
I am master template.
{{=render('child_template.tmpl')}}
```

child_template.tmpl:

```
I am child template.
```

Python REPL:

```python
>>> from conftl import render
>>> render('test.tmpl')
'I am master template.\nI am child template.\n\n'
>>>
```
