# vim:ts=4:sw=4:

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup

class Applet(object):
	def __init__(self, config, menus):
		self.lookup=TemplateLookup(
			default_filters=['decode.utf8'],
			input_encoding='utf-8',
			output_encoding='utf-8')
		
		self.config=config
		self.menus=menus

	def add_template_dir(self, path):
		self.lookup.directories.append(path)

	def render(self, template, data={}):
		return self.lookup.get_template(template).render(**data)

	def redirect(self, path):
		raise cherrypy.HTTPRedirect(path)
