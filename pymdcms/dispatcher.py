# vim:ts=4:sw=4:

import sys
import os.path
import signal

import cherrypy

from config import Config

from pages.md import Md
from pages.apps import Apps
from menus import Menus

class Dispatcher(object):
	def __init__(self):
		self.pages={}

		Menus()

		self.handlers=[
			Md(),
			Apps()
		]

		for handler in self.handlers:
			self.pages.update(handler.pages)

		signal.signal(signal.SIGHUP, self.refresh_content)
		signal.signal(signal.SIGUSR1, self.refresh_content)


	def refresh_content(self, signal, frame):
		Menus.load()
		for handler in self.handlers:
			handler.reload()

	@cherrypy.expose
	def default(self, *args, **kwargs):
		method=cherrypy.request.method

		if len(args) > 0:
			if args[0] in self.pages.keys():
				output=self.pages[args[0]].render(method, args, kwargs)

				if hasattr(self.pages[args[0]], "metadata"):
					if 'content-type' in self.pages[args[0]].metadata:
						cherrypy.response.headers['Content-Type']=self.pages[args[0]].metadata['content-type']

					if 'headers' in self.pages[args[0]].metadata:
						headers=self.parse_header_string(self.pages[args[0]].metadata['headers'])
						for header,value in headers.items():
							cherrypy.response.headers[header]=value

				return output
			else:
				raise cherrypy.HTTPError(404)

		else:
			if 'index' in self.pages.keys():
				return self.pages['index'].render(method, args, kwargs)

	def parse_header_string(self, string):
		output={}
		for header in string.split(';'):
			key,value = header.split('=')
			output[str(key).lower()]=value

		return output
