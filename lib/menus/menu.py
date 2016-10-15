# vim:ts=4:sw=4:

import sys
import os.path
import glob

from ConfigParser import ConfigParser
from collections import OrderedDict

class Menus(object):
	def __init__(self, config):
		self.config=config

		self.menus = {}

		self.reload()

	def reload(self):
		path = self.config.get('menus', 'path')

		for fn in glob.glob(os.path.join(path, '*')):
			self.menus.update({fn: Menu(fn)})

	def has(self, menu):
		if menu in self.find(menu):
			return True

		return False

	def get(self, menu):
		return self.find(menu)

	def find(self, name):
		for id,menu in self.menus.items():
			if menu.name == name:
				return menu

		return None
			

	def __repr__(self):
		return repr(self.menus)

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
