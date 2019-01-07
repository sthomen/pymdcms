# vim:ts=4:sw=4:

import sys
import os.path
import glob

from datetime import datetime, timedelta
from ConfigParser import ConfigParser
from collections import OrderedDict

from config import Config

class Menus(object):
	menus = {}
	cacheinterval=timedelta(seconds=60)
	updated = 0

	def __init__(self):
		Menus.load()

	@classmethod
	def load(cls):
		path = Config.get('menus', 'path')

		for fn in glob.glob(os.path.join(path, '*')):
			cls.menus.update({fn: Menu(fn)})

		cls.updated = datetime.now()

	@classmethod
	def has(cls, menu):
		if menu in cls.find(menu):
			return True

		return False

	@classmethod
	def get(cls, menu):
		return cls.find(menu)

	@classmethod
	def find(cls, name):
		if cls.updated + cls.cacheinterval < datetime.now():
			cls.load()
        
		for id,menu in cls.menus.items():
			if menu.name == name:
				return menu

		return None

class Menu(object):
	def __init__(self, path):
		self._items = OrderedDict()

		cp=ConfigParser()
		# override optionxform to preserve case
		cp.optionxform=str
		cp.read(path)

		self.name = cp.get('menu', 'name')

		for title in cp.options('links'):
			self._items.update({ title: cp.get('links', title) })

	def items(self):
		return self._items.items()

	def __repr__(self):
		return repr(self._items)

	def render(self):
		return self._items
