![](conftl_tl_dr.png)
# Configuration Templating Language

Simple to learn but yet powerful language for templating your configuration files. It is a 'slang' of the [web2py](http://www.web2py.com)'s templating language, written from scratch and optimized for textual non-html data.

## Features

* Simple to learn - a person who has some idea of the Python syntax could dive into conftl for 15 min.

* Powerful - Python code in templating.

* Command line tool for rendering.

* Different methods for trigerring rendering from Python code.

* Suitable for system administration, devops and similar roles.

* Performance - minimal code base optimized for performance.

* Platform independent - tested under Linux and Windows, should work on other Unix platforms as well, Python 2.7 compatible, Python 3.x compatible.

## Getting Started

Install conftl using pip:

```
pip install conftl
```

Alternatively download the source code:

```
git clone https://github.com/ttt-fifo/conftl
cd conftl
python setup.py install
```

Hello world from the command line:

```bash
$ render -c "name='John Smith'"
Hello, {{=name}}
Hello, John Smith
```

NOTE: Write ```Hello, {{=name}}``` on stdin, followed by Enter, Ctr+D

Hello world from the Python REPL:

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

Python 2.7 or Python 3.x

Please place an [issue](https://github.com/ttt-fifo/conftl/issues) in case the current implementation is not working with your platform and I will help.

Python Modules: future

## Template Syntax Quickstart

As conftl embeds Python syntax in template, the prerequisite is to know the basic Python syntax.
After accomplishing this prerequisite, the one must remember only the following three rules:

**Rule 1)** Python code must be enclosed in tags ```{{...}}```

```python
TEMPLATE                    | WILL OUTPUT
------------------------------------------
{{                          |
import sys                  |
def one():                  |
    return 1                |
i = 3                       |
}}                          |
------------------------------------------
```

NOTE: this Python code does not output anything, just imports, defines function, assigns variable.

**Rule 2)** Python blocks must end with the keyword ```{{pass}}```

```python
TEMPLATE                    | WILL OUTPUT
------------------------------------------
{{for i in range(0, 10):}}  | Hi, there!
Hi, there!                  | Hi, there!
{{pass}}                    | Hi, there!
------------------------------------------
```

**Rule 3)** Variables are printed to output enclosed in tags and prepended with = like ```{{=i}}```

```python
TEMPLATE                    | WILL OUTPUT
------------------------------------------
{{for i in range(0, 10):}}  | 0 Hi, there!
{{=i}} Hi, there!           | 1 Hi, there!
{{pass}}                    | 2 Hi, there!
------------------------------------------
```

For advanced syntax description see [TEMPLATE_SYNTAX.md](https://github.com/ttt-fifo/blob/master/docs/TEMPLATE_SYNTAX.md)

## Examples

There is no better knowledge than the real code. Take a look at the [examples folder](https://github.com/ttt-fifo/conftl/blob/master/examples)

## Command Line Tool for Rendering (render)

conftl comes with a command line tool for quick and easy templating. It works like this:

```bash
$ render -i templatename.tmpl - o filename.conf

-i input template
-o output configuration file
```

Full description could be found in [COMMAND_LINE.md](https://github.com/ttt-fifo/conftl/blob/master/docs/COMMAND_LINE.md)

## Python API

There are three interfaces for rendering a template from Python: the function ```render(...)```, the class ```Render``` and the decorator ```@template(...)``` .

The API description could be found here: [PYTHON_API.md](https://github.com/ttt-fifo/conftl/blob/master/docs/PYTHON_API.md)

## Known Limitations

* Arbitrary Python code is possible to be executed by the current templating language. I would advice against giving opportunity to the end-users to write template code, unless you know what you are doing. Multiple attack vectors could be used by a malicious end-user who has the possibility to execute arbitrary Python code. See [security_considerations.txt](https://github.com/ttt-fifo/conftl/blob/master/docs/security_considerations.txt)

* In case you want to template a HTML output, you would be better off using other templating languages:

web2py's templating language called [yatl](https://github.com/web2py/yatl).

jinja

cheetah

The templating languages above have HTML escaping switched on by default, helper functions and other features suitable for web services.
## Contributing

Testing implementation on different platforms.

Place [issue](https://github.com/ttt-fifo/conftl/issues) if you spot issues with this code.

Do not hesitate to fork me on github.

## Versioning

See [HISTORY.txt](https://github.com/ttt-fifo/conftl/blob/master/HISTORY.txt)

Also see the [tags](https://github.com/ttt-fifo/conftl/tags) on the [conftl repositiory](https://github.com/ttt-fifo/conftl).

## Authors

**Todor Todorov** - [ttt-fifo](https://github.com/ttt-fifo)

## License

This is open source software, free for personal and commercial use, licensed under:

BSD + other copyright credits

See [LICENSE](https://github.com/ttt-fifo/conftl/blob/master/LICENSE) for details.

## Acknowledgments

Thanks to [Massimo Di Pierro](https://github.com/mdipierro) and the [web2py](https://github.com/web2py) team for the inspiration.

Logo: [server](https://www.vrt.com.au/downloads/vrt-network-equipment), [icons](http://hawcons.com/), [arrow](https://longfordpc.com/)

## See Also

Differences between conftl and yatl from the document [differences_yatl.txt](https://github.com/ttt-fifo/conftl/blob/master/docs/differences_yatl.txt)

[web2py on github](https://github.com/web2py/web2py)

web2py templating language [yatl](https://github.com/web2py/yatl)

Another implementation of the same templating language may be found at the [weppy](https://github.com/gi0baro/weppy) project.
