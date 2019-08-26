# Configuration Templating Language Python API

Conftl is a pure Python implementation, it embeds Python syntax in the template and of course it has an Python API to trigger templating from Python scripts. There are three ways of interaction:

* Using ```render(...)``` function to render a template

* Using an object of the ```Render``` class

* Using ```@template(...)``` decorator to decorate a function

## render(...) function

An example from a python REPL would be:

```python
>>> from conftl import render
>>> render(content='{{=i}}', context=dict(i=8))
'8'
>>>
```

The signature of the function follows:

```python
render(infile=None,
       outfile=None,
       context=None,
       content=None,
       delimiters=None,
       path=None)
```

You can use the function by giving infile= as argument (this is the template file). If not given, you should give the content= value - this would be a string with the template content.

Output file could be given by outfile= argument. If given, the output will be written to this file. On outfile= absence, the output is returned as string.

In case you need to use other delimiters than the default ```{{ }}```, you can change the delimiters like this:

```python
>>>
>>> render(content='[[=i]]', context=dict(i=7), delimiters='[[ ]]')
'7'
>>>
```

The default delimiters may be changed globally by editing conftl/defaults.py

The path= argument is a list of template search paths. They will be added to the default search path.

The default search path is $HOME/templates, but this may be changed by editing conftl/defaults.py.

## Object from Class Render

An object from Render class could be used in a long running processes. Load the object in memory once and use it multiple times for templating multiple files:


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


## Template Decorator

The template decorator may be used to develop set of functions as a framework for templating your configuration files. The idea is well known for the web2py users, because this is how web2py's controller works.

Define a function which returns the context as a dict. Decorate your function with template decorator:

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

The possible arguments for template decorator are

```python
@template(infile=None,
          outfile=None,
          content=None,
          delimiters=None,
          path=None)
```

You must give eihter infile= or content= as input. You can omit outfile= and in this case the decorated function will return the output as a string. Changing delimiters= and template search path= is also possible. The function, decorated with template(...) must return dict, otherwise exception is raised.

The default delimiters and template search path may be changed globally by editing conftl/defaults.py
