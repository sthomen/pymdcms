# vim:ts=4:sw=4:

import cherrypy
from pymdcms.renderer import Renderer

class Applet(object):
	def __init__(self):
		self.renderer = Renderer()
		
	def dispatch(self, method, *args, **kwargs):
		self._body=''
		if method in cherrypy.request.methods_with_bodies:
			self._body=cherrypy.request.body.read()

	def add_template_dir(self, path):
		self.renderer.add_path(path)

	def render(self, template, data={}):
		return self.renderer.raw(template, data)

	def redirect(self, path):
		raise cherrypy.HTTPRedirect(path)
