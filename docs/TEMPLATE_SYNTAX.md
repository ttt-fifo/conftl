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

* **Printing a variable value to the output** is done by tagging it and placing = sign in front of the variable like this ```{{=myvar}}```

For example if ```i``` has the value of ```3``` and you put in template:

```{{=i}}```

you will receive in the output:

```3```

* **Combining a Python code block with clear text and variable outputs** - you should not indent the code block as you normally do with Python, but you should determine it with ```{{pass}}``` special keyword instead.

Whenever you write a code block into the original Python interpreter you indent the code. Lets take the following example of original Python code block:

```python
for i in range(0, 2):
    print('X', i)
```

The equivalent of the above code would be:

```
{{for i in range(0, 2):}}
X {{=i}}
{{pass}}
```

* **You are able to pass values to template variables from outside of the template** - there are multiple methods to give 'context' to the template, e.g. assigning variable values outside of the template. Look the follow up sections.

* **Advanced templating topics** could be found at [TEMPLATING.md](https://github.com/ttt-fifo/conftl/blob/master/TEMPLATING.md)


