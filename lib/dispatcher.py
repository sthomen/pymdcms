# vim:ts=4:sw=4:

import os.path

import cherrypy

from pages.md import Markdown
from pages.apps import Apps
from menus.menu import Menus

class Dispatcher(object):
	def __init__(self, config):
		self.config=config

		self.pages={}

		menus=Menus(config)

		self.handlers=[
			Markdown(config, menus),
			Apps(config, menus)
		]

		for handler in self.handlers:
			self.pages.update(handler.pages)

	@cherrypy.expose
	def default(self, *args, **kwargs):
		if len(args) > 0:
			if args[0] in self.pages.keys():
				return self.pages[args[0]].render(args, kwargs)
			else:
				raise cherrypy.HTTPError(404)

		else:
			if 'index' in self.pages.keys():
				return self.pages['index'].render(args, kwargs)
