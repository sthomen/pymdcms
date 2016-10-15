# vim:ts=4:sw=4:

import sys
import os.path
import glob

import time

from markdown import markdown

from page import Page

class Markdown(object):
	def __init__(self, config, menus):
		self.config=config
		self.menus=menus

		self.pages = {}

		self.reload()

	def reload(self):
		path = self.config.get('pages', 'path')

		for fn in glob.glob(os.path.join(path, '*')):
			self.pages.update(((os.path.basename(fn), MarkdownPage(self.config, self.menus, fn)),))

class MarkdownPage(Page):
	def __init__(self, config, menus, fn=None):
		Page.__init__(self, config, menus)
		self.filename=fn

	def render(self, args, kwargs):
		self._load()

		self.metadata['content']=markdown(self.markdown, ['markdown.extensions.extra'])

		return super(MarkdownPage,self).render(args, kwargs)

	def _load(self):
		with open(self.filename) as fp:
			rollback=0;

			while True:
				rollback=fp.tell()
				line=fp.readline().strip()

				if not line:
					break

				try:
					key,value=[x.strip() for x in line.split(':', 1)]
					self.metadata.update({key.lower(): value})
				except ValueError:
					break

			fp.seek(rollback)

			self.markdown=fp.read()
