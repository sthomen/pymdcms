Title: PyMDCMS
Date: Wed Jun 15 14:20:32 EEST 2016

# Super simple CMS with python and markdown

> As with most software I write, I had a need for something and this is no
> different.

This time, I wanted to host webpages and the occasional form (although this
code is much more powerful than just form receiving) on my "ancient" Alpha
system (ev5.6 at 500MHz with a whopping 1GB of RAM)

The primary requirements for this program was minimalism, flexibility and speed.

Apart from python itself, there are only a few dependencies, all of which are
platform independent. This was important because anyone who've ever tried to
port an application to anything other than middle class caucasian male
software / hardware (I'm looking at you, GNU/Linux and i386) will know that
problems multiply with dependencies.

PyMDCMS currently requires:

	CherryPy>=6.0.1
	flup6>=1.1.1
	Mako>=1.0.4
	Markdown>=2.6.6

There is (as yet) no administration UI, and the page structure is flat (unless
you extend it using an applet in which you can do what you please).

To set up, install the above modules (there's a requirements.txt for pip
convenience) and hook it up to your webserver like any other FastCGI
application.

You will also need to create a configuration file named `cms.conf` in the
program root directory, an example is provided in `./examples/`.

Documents served are by default located in `./pages/` and the url to them is
simply the filename.

There is a special document `index` that will be used for when no file was
requested. If both a file an app binds to `index`, then the app will be used.

The markdown is according to the python markdown module with a small twist, you
can specify metadata at the beginning of the file to set variables and change
the page title and display template from within the page, so if you wish to 
use a completely different template for just one markdown page, this is
possible through setting the `template` header.

Per-page css and javascript embedding is also possible through the header
variables (this is then executed in the theme template file,
see `theme/default/base` for an example)

Variables set in the header can also be used in the contents, like the date
at the bottom of this page.

## Applets

If you'd like to perform an action with a form, you'll need to build an applet.
There's a small demo-applet in the `apps/test.py` file, and it should be enough
to get you started.

Applets are required to implement the `dispatch` method accepting one parameter
which is the request.
Other than that you're free to do what you like.

There is also a convenience superclass `applet.Applet` that you may use if
you like (but it is not mandatory), which defines mako template rendering
methods (for now).

Use `Applet.add_template_dir()` to add a template directory where you want
to store your app-specific templates to the lookup, and then just return
`self.render("template_file", dict)` where dict is a dictionary of template
variables.

If an applet sets an object property named `metadata` to be a dictionary, it
will be merged with the page metadata and you are able to override variables
just like the markdown pages. You can even override your own "content" variable
which actually is where the value retuned from the `dispatch` method is set.

<small>Last updated: ${date}</small>
