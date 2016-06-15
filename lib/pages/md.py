# vim:ts=4:sw=4:

import sys
import os.path
import glob

import time

from markdown import markdown

from page import Page

class Markdown(object):
	def __init__(self, config):
		self.config=config

		self.pages = {}
		path = self.config.get('pages', 'path')

		for fn in glob.glob(os.path.join(path, '*')):
			self.pages.update(((os.path.basename(fn), MarkdownPage(self.config, fn)),))

class MarkdownPage(Page):
	def __init__(self, config, fn=None):
		super(MarkdownPage,self).__init__(config)
		self.filename=fn

	def render(self, args, kwargs):
		self._load()

		self.metadata['content']=markdown(self.markdown)

		return super(MarkdownPage,self).render(args, kwargs)

	def _load(self):
		with open(self.filename) as fp:
			while True:
				line=fp.readline().strip()

				if not line:
					break

				try:
					key,value=[x.strip() for x in line.split(':')]
					self.metadata.update({key.lower(): value})
				except ValueError:
					break

			self.markdown=fp.read()
