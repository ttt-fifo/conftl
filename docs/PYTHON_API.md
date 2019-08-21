* **render(...) function**

Consider the following example:

```python
>>>
>>> from conftl import render
>>> render(content='{{=i}}', context=dict(i=8))
'8'
>>>
```

As you can see, you can give the context= value, which is a dict, containing your variable data.

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

In case you need to use other delimiters than the default ```{{ }}```, you can change the delimiters like this:

```python
>>>
>>> render(content='[[=i]]', context=dict(i=7), delimiters='[[ ]]')
'7'
>>>
```

* **template decorator**

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
          delimiters=None)
```

You must give eihter infile= or content= as input. You can omit outfile= and in this case the decorated function will return the output as a string. Changing delimiters= is also possible. The function, decorated with template(...) must return dict, otherwise exception is raised.

This type of context computation is well know by the web2py users, because this is the layout of the web2py controller.

* **Render object**

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


