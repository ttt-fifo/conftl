# Coming from Jinja

Jinja is multi purpose and powerful templating language. It implements multiple features for web templating, but it is also used for templating any kind of documents, including text. Conftl has but one purpose - to template configuration files and for this purpose it uses the power of the embedded Python syntax. This makes it easier to lern for Python coders and the abilities are equal to the abilities of the multipurpose Python language.

## Delimiters

Jinja has four types of delimiters, conftl uses one type of delimiters and one addition (placing = after the first delimiter) for printing variables.

```python
PURPOSE             | JINJA        | CONFTL
------------------------------------------------------------------------------------
Statements          | {% ... %}    | {{ ... }}
Print to output     | {{ ... }}    | {{= ... }}
Comments            | {# ... #}    | {{ ... }}   (arbitrary comments in Python code)
Line Statements     | # ... ##     | {{ ... }}
------------------------------------------------------------------------------------
```

The different block statements in Jinja end differently. Conftl uses only one {{pass}} keyword:

```python
JINJA                               | CONFTL
--------------------------------------------------------------
{% for user in users %}             | {{for user in users:}}
{{ user }}                          | {{=user}}
{% endfor %}                        | {{pass}}
--------------------------------------------------------------
{% if variable is sameas true %}    | {{if variable == True:}}
X                                   | X
{% endif %}                         | {{pass}}
```

## Variables

The variable values are given by the context in both templating engines.

In Jinja you can use dot notation or getitem syntax interchargeably, in conftl you should use exactly the Python syntax depending on the variable type.

```python
JINJA                               | CONFTL
--------------------------------------------------------------
{{ foo.bar }}                       | {{# only python syntax possible}}
{# is the same as #}                | {{=foo['bar']}}
{{ foo['bar'] }}                    | 
--------------------------------------------------------------
```

## Jinja Filters

Jinja implements filters as a syntax feature and has numerous builtin filters. Conftl does not implement filters, but arbitrary filtering can be accomplished via the embeded Python syntax. As an example:

```python
JINJA                               | CONFTL
--------------------------------------------------------------
{{ listx | join(',') }}             | {{=','.join(listx)}}
--------------------------------------------------------------
```

## Jinja Tests

The above is valid also for Jinja tests - Jinja defines a list of builtin tests to test a variable against. Conftl can use Python syntax for testing a variable.

## Comments

Jinja has a special syntax for comments, Conftl can include arbitrary Python comments.

```python
JINJA                               | CONFTL
--------------------------------------------------------------
{# comment #}                       | {{# python comment}}
--------------------------------------------------------------
{# commenting a block in Jinja      | {{# block comment
    {% for user in users %}         | # {{for user in users:}}
    ...                             | # ...
    {% endfor %}                    | # {{pass}}
#}                                  | }}
--------------------------------------------------------------
{# commenting a block in Jinja      | {{"""
    {% for user in users %}         | {{for user in users:}}
    ...                             | ...
    {% endfor %}                    | {{pass}}
#}                                  | """}}
--------------------------------------------------------------
```

## Jinja Whitespace Control, Escaping, Line Statements

For symplicity conftl does not implement these features.

## Template Inheritance

A core and very useful feature in web templating engines is the Templating Inheritance. It is supposed that Template Inheritance is not much needed while templating configuration files, so conftl does not implement special Template Inheritance. However, it is possible via Python Syntax and it is described in [TEMPLATE_SYNTAX.md](https://github.com/ttt-fifo/conftl/blob/master/docs/TEMPLATE_SYNTAX.md)

## HTML Escaping

HTML Escaping is unneded behavior while templating configuration files. Therefore conftl does not have HTML escaping features by default. However, in case needed, it can be implemented via Python syntax inside the template. See [here](https://wiki.python.org/moin/EscapingHtml) for Python recipes.

## Other Junja Features, Not Mentioned Here

As Jinja has it own templating syntax, it implements multiple features, not mentioned here. Due to the philosophy of conftl to embed Python code in template, it can implement arbitrary features. 

## Security Considerations

Jinja implements it's own syntax and many of the features for a reason. By embeding full Python interpreter in the template, conftl has some [security considerations](https://github.com/ttt-fifo/conftl/blob/master/docs/security_considerations.txt) need to be mentioned.
