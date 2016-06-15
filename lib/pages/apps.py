# vim:ts=4:sw=4:

import sys
import os.path
import glob

from page import Page

class Apps(object):
	def __init__(self, config):
		self.config=config

		self.pages = {}
		for name in self.config.options('apps'):
			self.pages.update({
				name: AppPage(config, self.config.get('apps', name))
			})

class AppPage(Page):
	def __init__(self, config, path):
		super(AppPage,self).__init__(config)

		module,name=path.rsplit('.', 1)

		app=__import__(module, fromlist=[ name ])

		self.app=getattr(app, name)()

	def render(self, args, kwargs):
		if hasattr(self.app, 'metadata'):
			self.metadata.update(self.app.metadata)

		self.metadata['content']=self.app.dispatch(*args, **kwargs)

		return super(AppPage,self).render(args, kwargs)
