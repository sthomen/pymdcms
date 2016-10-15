# vim:ts=4:sw=4:

import os.path
import signal

import cherrypy

from pages.md import Markdown
from pages.apps import Apps
from menus.menu import Menus

class Dispatcher(object):
	menus=None

	def __init__(self, config):
		self.config=config

		self.pages={}

		self.menus=Menus(config)

		self.handlers=[
			Markdown(config, self.menus),
			Apps(config, self.menus)
		]

		for handler in self.handlers:
			self.pages.update(handler.pages)

		signal.signal(signal.SIGHUP, self.refresh_content)
		signal.signal(signal.SIGUSR1, self.refresh_content)

	def refresh_content(self, signal, frame):
		self.menus.reload()
		for handler in self.handlers:
			handler.reload()

	@cherrypy.expose
	def default(self, *args, **kwargs):
		if len(args) > 0:
			if args[0] in self.pages.keys():
				output=self.pages[args[0]].render(args, kwargs)

				if hasattr(self.pages[args[0]], "metadata") and 'content-type' in self.pages[args[0]].metadata:
					cherrypy.response.headers['Content-Type']=self.pages[args[0]].metadata['content-type']

				return output
			else:
				raise cherrypy.HTTPError(404)

		else:
			if 'index' in self.pages.keys():
				return self.pages['index'].render(args, kwargs)
