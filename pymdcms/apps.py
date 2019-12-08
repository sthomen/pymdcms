# vim:ts=4:sw=4:

import sys
import os.path
import glob

from .config import Config
from .page import Page
from .handler import Handler
from .renderer import Renderer

class Apps(Handler):
	def __init__(self):
		self.pages = {}

		if Config.has_section('apps'):
			for name in Config.options('apps'):
				self.pages.update({
					name: AppPage(Config.get('apps', name))
				})

		self.renderer = Renderer()

	def getpage(self, request):
		if request.route[0] in self.pages.keys():
			return self.pages[request.route[0]]

class AppPage(Page):
	def __init__(self, path):
		Page.__init__(self)

		module,name=path.rsplit('.', 1)

		app=__import__(module, fromlist=[ name ])

		self.app=getattr(app, name)()

	########################################################################
	# XXX This hack handles the content-type metadata for app pages, since
	# they need to be set in the AppPage to act like a regular Page that has
	# a static content-type (if any)
	#

	APP_META=('content-type', 'headers')

	def __contains__(self, name):
		if name in self.APP_META and name in self.app.metadata:
			return True

		return Page.__contains__(self, name)

	def __getitem__(self, name):
		result = None

		if name in self.APP_META:
			try:
				result = self.app.metadata.get(name)
			except:
				pass

		if result:
			return result

		return Page.__getitem__(self, name)

	#
	# XXX
	########################################################################

	def render(self, request):
		# Use a dummy Page here so that we don't clobber the defaults
		# we set in __init__ when changing something in the actual app.
		data = Page()

		data.content=self.app.dispatch(request)

		# Add page-level metadata, this is currently only for the base
		# template variable.
		data.update(self)

		if hasattr(self.app, 'metadata'):
			data.update(self.app.metadata)

		return self.renderer.render(data)
