# vim:ts=4:sw=4:

import sys
import os.path
import glob

import time

from ..config import Config
from ..mdrenderer import MDRenderer
from page import Page

class Md(object):
	def __init__(self):
		self.pages = {}

		self.reload()

	def reload(self):
		path = Config.get('pages', 'path')

		for fn in glob.glob(os.path.join(path, '*')):
			self.pages.update(((os.path.basename(fn), MarkdownPage(fn)),))

class MarkdownPage(Page):
	def __init__(self, fn=None):
		Page.__init__(self)
		self.filename=fn

	def render(self, method, args, kwargs):
		self.metadata=self.metadata_defaults.copy()

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

		self.metadata['content']=MDRenderer.render(self.markdown)

		return super(MarkdownPage,self).render(method, args, kwargs)

