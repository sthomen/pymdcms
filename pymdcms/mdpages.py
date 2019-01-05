# vim:ts=4:sw=4:

import sys
import os.path
import glob

import time

from config import Config
from mdpage import MDPage
from handler import Handler

class MDPages(Handler):
	def __init__(self):
		self.pages = {}

		self.reload()

	def getpage(self, route):
		# XXX the structure here is flat so far, make it work with depth?
		if route[0] in self.pages:
			return self.pages[route[0]]

	def reload(self):
		path = Config.get('pages', 'path')

		for fn in glob.glob(os.path.join(path, '*')):
			self.pages.update({os.path.basename(fn): MDPage().from_file(fn)})
