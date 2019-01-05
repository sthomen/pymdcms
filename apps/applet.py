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

	@staticmethod
	def pad(s, l, f=None, fmt=unicode):
		"""
		A simple method for ensuring that input values conforms to the
		expected format of a list of a given length
		"""
		try:
			return [ fmt(s[i]) if i < len(s) else f for i in range(0, l) ]
		except TypeError:
			return [f] * l
