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

## Getting Started

Install conftl using pip:

```
pip install conftl
```

Alternatively download the source code:

```
git clone https://github.com/ttt-fifo/conftl
```

Make your first templating test in your Python REPL:

```python
>>>
>>> from conftl import render
>>>
>>> render(content='Hello, {{=name}}', context=dict(name='John Smith'))
'Hello, John Smith'
>>>
```

## Prerequisites

Linux or other Unix distribution or Windows.

Please place an [issue](https://github.com/ttt-fifo/conftl/issues) in case the current implementation is not working with your platform and I will try to help.

Python 2.7 or Python 3.x

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

* **Combining a Python code block with clear text and variable outputs** - you should not indent the code block as you normaly do with Python, but you should determine it with ```{{pass}}``` special keyword instead.

Whenever you write a code block into the original Python interpreter you indent the code. Lets take the following example of original Python code block:

```python
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

## Command Line Tool for Rendering (render)

* **The render command line tool works as follows:**

```
render -i templatename.tmpl -o filename.conf
```

will take the template from file ```templatename.tmpl``` and write the output to ```filename.conf```

WARNING: filename.conf will be overwriten!!!

In case input template is not given with -i, you would be expected to place template code on stdin.

NOTE: For Linux and other Unix systems write template code and finish it with Ctr + D

NOTE: For Windows finish template code with with Ctr + z and then hit ENTER

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

- *You can assign integer values*

```
render -c i=4
```

- *You can assign string values*, but please follow strictly this layout:

```
render -c "i='my string here'"
```

, so please quote the string with single quote and quote the whole value with double quotes.

- *Other python types cannot be assigned* from command line, please invoke render from python script if you need to use complex python types in the context.

* **See render -h for the full set of options**

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

## Rendering Template from Python

There are three interfaces for rendering a template from Python: the function ```render(...)```, the class ```Render``` and the decorator ```@template(...)``` . Please see the explanation below:

* **render(...) function**

The signature of the function follows:

```python
render(infile=None,
       outfile=None,
       context=None,
       content=None,
       delimiters=None)
```

You can use the function by giving infile= as argument (this is the template file). If not given, you should give the content= value - this would be a string with the template content.

Output file could be given by outfile= argument. If given, the output will be written to this file. On outfile= absence, the output is returned as string.

Consider the following example:

```python
>>>
>>> from conftl import render
>>> render(content='{{=i}}', context=dict(i=8))
'8'
>>>
```

As you see, you can give the context= value, which is a dict, containing your variable data.

In case you need to use other delimiters than the default ```{{ }}```, you can change the delimiters like this:

```python
>>>
>>> render(content='[[=i]]', context=dict(i=7), delimiters='[[ ]]')
'7'
>>>
```

* **template decorator**

If you have complex computations, which give you the context output, more convenient helper would be the template decorator. Here is an example how to use it:

```python
from conftl import template

# Define your function, which should output a dict
# with the template context and decorate it with
# template decorator

@template(infile='mytemplate.tmpl', outfile='myconf.conf')
def template_myconf(*arg, **kwarg):

    # ...here your complex computations...
    i = ....
    j = ....
    x = '.....'

    return dict(i=i, j=j, templ_var=x)

if __name__ == '__main__':

    # Here invoke your function and it should create
    # the needed myconf.conf

    template_myconf(... some args...)
```

The possible arguments for template are

```python
@template(infile=None,
          outfile=None,
          content=None,
          delimiters=None)
```

You must give eighter infile= or content= as input. You can ommit outfile= and in this case the decorated function will return the output as a string. Changing delimiters= is also possible. The function, decorated with template(...) must return dict, otherwise exception is raised.

This type of complex context computation is well know by the web2py users, because this is the layout of the web2py controller.

* **Render object**

An object from Render class could be used in long running processes, where you can load the object in memory and use it multiple times for templating multiple files:


```python
from conftl import Render

rndr = Render()

# ... use it multiple times like this
rndr.instream = open('filename.tmpl', 'r')
rndr.outstream = open('otherfile.conf', 'w')
rndr.context = dict(i=..., j=..., somevar='...')

rndr()

rndr.instream.close()
rndr.outstream.close()
# ....
```

The ```instream``` and ```outstream``` should be file handles or StringIO objects.

## Examples

Take a look at the [examples](https://github.com/ttt-fifo/conftl/examples] directory.

## Known Limitations

* The opening code for a code block which prints clear text and vars cannot be multiline. Please **do not write this**:

```
{{i = 0
while i <= 10:}}
...
{{pass}}
```

The code **should be**:

```
{{i = 0}}
{{while i <= 10:}}
...
{{pass}}
```

* The command line tool render cannot get complex datatypes as context variables.

This is **not possible**:

```
render -c myvar={'a': 10, 'b': 12}
```

Possible context variables are **numbers and strings only**:

```
render -c i=3 -c j=4.2 -c "s='my string here'"
```

In case you need complex data structures, please invoke the templating from Python.

* Arbitrary Python code is possible to be executed by the current templating language. I would advice against giving opportunity to the end-users to write template code, unless you know what you are doing. Multiple attack vectors could be used by an malicious end-user who has the possibility to execute arbitrary Python code.

* In case you want to template a HTML output, you would be better off using the web2py's templating language (called [yatl](https://github.com/web2py/yatl)). Yatl has XML escaping switched on by default and also multiple HTML helper functions.

## Contributing

Testing implementation on different platforms.

Do not hesitate to fork me on github.

Place [issue](https://github.com/ttt-fifo/conftl/issues) if you spot issues with this code.

## Versioning

See the [tags](https://github.com/ttt-fifo/conftl/tags) on this repository.

## Authors

**Todor Todorov** - [ttt-fifo](https://github.com/ttt-fifo)

## License

See [LICENSE](https://github.com/ttt-fifo/conftl/blob/master/LICENSE) for details.

## Acknowledgments

Thanks to [Massimo Di Pierro](https://github.com/mdipierro) and the [web2py](https://github.com/web2py) team for the inspiration.

## See Also

[web2py on github](https://github.com/web2py/web2py)

web2py templating language [yatl](https://github.com/web2py/yatl)

Another implementation of the same templating language may be found at the [weppy](https://github.com/gi0baro/weppy) project.
