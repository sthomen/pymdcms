# vim:ts=4:sw=4:

import os.path
import signal

import logging

import cherrypy

from pages.md import Markdown
from pages.apps import Apps
from menus.menu import Menus

class Dispatcher(object):
	menus=None

	def __init__(self, config):
		self.config=config

		self.log=logging.getLogger(__name__)

		self.pages={}

		self.log.info("Loading menus")

		self.menus=Menus(config)

		self.log.info("Loading handlers")

		self.handlers=[
			Markdown(config, self.menus),
			Apps(config, self.menus)
		]

		for handler in self.handlers:
			self.pages.update(handler.pages)

		signal.signal(signal.SIGHUP, self.refresh_content)
		signal.signal(signal.SIGUSR1, self.refresh_content)

		self.log.info("CMS started")


	def refresh_content(self, signal, frame):
		self.menus.reload()
		for handler in self.handlers:
			handler.reload()

		self.log.info("Content handlers reloaded")

	@cherrypy.expose
	def default(self, *args, **kwargs):
		method=cherrypy.request.method

		self.log.info("New request: %s", method)

		if len(args) > 0:
			if args[0] in self.pages.keys():
				output=self.pages[args[0]].render(method, args, kwargs)

				if hasattr(self.pages[args[0]], "metadata") and 'content-type' in self.pages[args[0]].metadata:
					cherrypy.response.headers['Content-Type']=self.pages[args[0]].metadata['content-type']

				return output
			else:
				raise cherrypy.HTTPError(404)

		else:
			if 'index' in self.pages.keys():
				return self.pages['index'].render(method, args, kwargs)
