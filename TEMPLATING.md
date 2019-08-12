# Advanced Templating

Here advanced templating topics are represented, together with some tips and tricks.

* **Clear text**

Clear text in template is printed to the output as is.

**Common mistake** is to indent the text like a Python indented block:

```
{{if True:}}
    Indented paragraph.
    Text text
    Lorem ipsum
{{pass}}
```

This will go to the output together with the indentation:

```
    Indented paragraph.
    Text text
    Lorem ipsum
```

If you do not want to have indentation the **template should be**:
```
{{if True:}}
Indented paragraph.
Text text
Lorem ipsum
{{pass}}
```

* **Python code in template**

Python code in template is written in tags ```{{...}}```

This one line code is **valid**:

```{{i = 3}}```

This multiline code is **valid**:

```
{{if i == 3:
    j = 3
else:
    j = 0}}
```

Although the code seams funny, it complies to the indentation rules.

For a better visibility I would propose this **valid** code snippet:

```
{{
if i == 3:
    j = 3
else:
    j = 0
}}
```

Due to some parser limitations this snippet will raise exception, making the code **invalid**:

```{{mydict = {'some': 1, 'other': 2}}}```

(see the three }}} at the end)

This trick will provide you with a **valid** result:

```
{{
mydict = {'some': 1, 'other': 2}
}}
```

All kinds of multiline Python code and indentations are **valid**:

```
{{
# some imports
import sys

# defining my function
def myfunct(i):
    if i == 1:
        return True
    else:
        return False

j = myfunct(1)
k = myfunct(2)

# list definition
x = [j, k, 3]
}}
```

* **Printing a variable value to the output**

Variable is printed in tags and prepending the variable with = like this (**valid**):

```{{=i}}```

Some interesting examples, which are **valid**:

```{{=myfunct(i)}}```

```{{=int(i)}}```

```{{=i+1}}```

Here some examples of **invalid** code:

```{{ = i}}```

```{{=i }}```

```
{{
=i}}
```

```
{{
if True:
    =i
}}
```

* **Python code blocks**

NOTE: whenever you need a Python code blocks, which do not print anything to output, use multiline Python code as explained above.

The following is needed whenever you need to combine Python code blocks with printing clear text and/or variable outputs.

Python code blocks should be ended with the special keyword {{pass}}

Here is one if-else example, which is **valid**:

```
{{if i == 1:}}
X
{{elif i == 2:}}
Y
{{else:}}
Z
{{pass}}
```

This single if statement is also **valid**:

```
{{if i == 3:}}
X
{{pass}}
```

This for loop is **valid**:

```
{{for i in range(0, 2):}}
X: {{=i}}
{{pass}}
```

This for-else loop is **valid**:

```
{{for i in range(0, 2):}}
X: {{=i}}
{{else:}}
Y
{{pass}}
```

Here is one block opening, which is **invalid**:

```
{{i = 0
while i <= 3:}}
...
```

Examples of {{pass}} keyword, which are **invalid**:

```{{ pass}}```

```{{pass }}```

```{{ pass }}}```
