# vim:ts=4:sw=4:

import sys
import os.path
import glob

from page import Page

class Apps(object):
	def __init__(self, config, menus):
		self.config=config
		self.menus=menus

		self.pages = {}
		for name in self.config.options('apps'):
			self.pages.update({
				name: AppPage(config, menus, self.config.get('apps', name))
			})

class AppPage(Page):
	def __init__(self, config, menus, path):
		Page.__init__(self, config, menus)

		module,name=path.rsplit('.', 1)

		app=__import__(module, fromlist=[ name ])

		self.app=getattr(app, name)(config, menus)

	def render(self, args, kwargs):
		if hasattr(self.app, 'metadata'):
			self.metadata.update(self.app.metadata)

		self.metadata['content']=self.app.dispatch(*args, **kwargs)

		return super(AppPage,self).render(args, kwargs)
