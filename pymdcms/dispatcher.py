# vim:ts=4:sw=4:

import sys
import os.path
import signal

import cherrypy

from .config import Config

from .mdpages import MDPages
from .apps import Apps
from .menus import Menus
from .renderer import Renderer
from .request import Request

class Dispatcher(object):
	def __init__(self):
		# initialize menus
		Menus()

		# set up MD and app handlers
		self.handlers=[
			MDPages(),
			Apps()
		]

		signal.signal(signal.SIGHUP, self.refresh_content)
		signal.signal(signal.SIGUSR1, self.refresh_content)

	def refresh_content(self, signal, frame):
		Menus.load()
		for handler in self.handlers:
			handler.reload()

	@cherrypy.expose
	def default(self, *args, **kwargs):
		request = Request(route=args, query=kwargs, headers=cherrypy.request.headers)

		base = '{}/'.format(cherrypy.request.base)

		Config.set('global', 'base', base)

		for handler in self.handlers:
			page = handler.getpage(request)

			if page:
				page.base = base
				output = page.render(request)

				if 'content-type' in page:
					cherrypy.response.headers['Content-Type']=page['content-type']

				if 'headers' in page:
					headers = self.parse_header_string(page.headers)

					for header, value in headers.items():
						cherrypy.response.headers[header]=value

				return output

		raise cherrypy.HTTPError(404)

	def parse_header_string(self, string):
		output={}
		for header in string.split(';'):
			key,value = header.split('=')
			output[str(key).lower()]=value

		return output
