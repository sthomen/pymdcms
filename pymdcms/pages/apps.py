# vim:ts=4:sw=4:

import sys
import os.path
import glob

from ..config import Config
from page import Page

class Apps(object):
	def __init__(self):
		self.pages = {}
		for name in Config.options('apps'):
			self.pages.update({
				name: AppPage(Config.get('apps', name))
			})

class AppPage(Page):
	def __init__(self, path):
		Page.__init__(self)

		module,name=path.rsplit('.', 1)

		app=__import__(module, fromlist=[ name ])

		self.app=getattr(app, name)()

	def render(self, method, args, kwargs):
		self.metadata=self.metadata_defaults.copy()

		self.metadata['content']=self.app.dispatch(method, *args, **kwargs)

		if hasattr(self.app, 'metadata'):
			self.metadata.update(self.app.metadata)

		output=super(AppPage,self).render(method, args, kwargs)

		return output
