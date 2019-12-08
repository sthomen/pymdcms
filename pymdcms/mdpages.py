# vim:ts=4:sw=4:

import os
import glob

from datetime import datetime, timedelta

from .config import Config
from .mdpage import MDPage
from .handler import Handler

class MDPages(Handler):
	cacheinterval=timedelta(seconds=60)

	def __init__(self):
		self.pages = {}
		self.reload()

	def getpage(self, request):
		if self.updated + self.cacheinterval < datetime.now():
			self.reload()

		if request.route[0] in self.pages:
			return self.pages[request.route[0]]

	def reload(self):
		path = Config.get('pages', 'path')

		for fn in os.listdir(path):
			self.pages.update({fn: MDPage().from_file(os.path.join(path, fn))})

		self.updated = datetime.now()
