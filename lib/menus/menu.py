# vim:ts=4:sw=4:

class Menus(object):
	def __init__(self, config):
		self.config=config

		self.menus = {}

		for name in self.config.options('menus'):
			self.menus.update({
				name: Menu(config, name, self.config.get('menus', name))
			})

	def has(self, menu):
		if menu in self.menus.keys():
			return True

		return False

	def get(self, menu):
		return self.menus.get(menu)

	def __repr__(self):
		return repr(self.menus)

class Menu(object):
	def __init__(self, config, name, section):
		self.config = config
		self.name = name

		self._items = {}

		for title in self.config.options(section):
			self._items.update({ title: self.config.get(section, title) })

	def items(self):
		return self._items.items()

	def __repr__(self):
		return repr(self._items)

	def render(self):
		return self._items
