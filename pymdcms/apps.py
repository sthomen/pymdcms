# vim:ts=4:sw=4:

import sys
import os.path
import glob

from config import Config
from page import Page
from handler import Handler
from renderer import Renderer

class Apps(Handler):
	def __init__(self):
		self.pages = {}

		if Config.has_section('apps'):
			for name in Config.options('apps'):
				self.pages.update({
					name: AppPage(Config.get('apps', name))
				})

		self.renderer = Renderer()

	def getpage(self, route):
		if route[0] in self.pages.keys():
			return self.pages[route[0]]

class AppPage(Page):
	def __init__(self, path):
		Page.__init__(self)

		module,name=path.rsplit('.', 1)

		app=__import__(module, fromlist=[ name ])

		self.app=getattr(app, name)()

	def render(self, method, *args, **kwargs):
		# Use a dummy Page here so that we don't clobber the defaults
		# we set in __init__ when changing something in the actual app.
		data = Page()

		data.content=self.app.dispatch(method, *args, **kwargs)

		# Add page-level metadata, this is currently only for the base
		# template variable.
		data.update(self)

		if hasattr(self.app, 'metadata'):
			data.update(self.app.metadata)

		return self.renderer.render(data)
