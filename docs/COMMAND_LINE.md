* **The render command line tool works as follows:**

```
render -i templatename.tmpl -o filename.conf
```

will take the template from file ```templatename.tmpl``` and write the output to ```filename.conf```

WARNING: filename.conf will be overwriten!!!

In case input template is not given by -i, you would be expected to place template code on stdin.

NOTE: For Linux and other Unix systems write template code and finish it with Ctr + D

NOTE: For Windows finish template code with with Ctr + Z and then hit ENTER

In case the output filename (-o) is not given, the output will be written to stdout.

* **Giving context variables on the command line**

You want to give ```i``` value of ```4``` and use it in your template. Use -c flag:

```
render -i templatename.tmpl -o filename.conf -c i=4
```

For assigning values to multiple variables, just repeat -c flag multiple times:

```
render -i templatename.tmpl -o filename.conf -c i=4 -c j=8 -c x=2
```

For assigning complex variable datatypes, wrap assignment in double quote like this:

```
render -i templatename.tmpl -o filename.conf -c "mydict={'a': 1, 'b': 'string'}"
```

* **Context from json file**

The json file format should be similar to:

```json
{"myvar": 4,
 "otherthing": [1, 3, 5],
 "stringsomething": "hello world"
}
```

You can invoke render by giving the -j option like this:

```
render -i mytemplate.tmpl -j mycontext.ctx
```

NOTE: the command line variables have precedence over json file, e.g. if you assign i=2 in json file and i=3 on command line, the final value of i will be i=3.

* **Environment in context for convenience**

For convenience the ENV dictionary is automatically included in the context and it contains the OS environment variables. The following example prints them on the screen:

```
render
{{for e in ENV:}}
{{=e}} : {{=ENV[e]}}
{{pass}}
..................................
... environment will come here ...
..................................
```

NOTE: the ENV is included automatically in context only with the command line tool, rendering from Python (the next section) does not have ENV automatically in context.

*How to use ENV in templates?*

Many devops / sysadmin systems pass data to their underlying scripts via environment variables. As an example the following shell commands:

```
$ export SYSTEM=production
$
$ render
{{if ENV['SYSTEM'] == 'production':}}
Listen 80
{{elif ENV['SYSTEM'] == 'ci_cd':}}
Listen 8080
{{elif ENV['SYSTEM'] == 'devel':}}
Listen 8081
{{else:}}
{{raise RuntimeError('wrong SYSTEM')}}
{{pass}}
```
(Ctr+D at the end)

will give you the output based on the SYSTEM environment variable:

```
Listen 80
```

* **Command line tool help**

See ```render -h```


