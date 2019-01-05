from config import Config
from menus import Menus
from renderer import Renderer

class Page(dict):
	def __init__(self):
		self.update({
			'base': Config.get('global', 'base'),
			'theme': Config.get('global', 'theme'),
			'template': 'page',
			'menus': Menus
		})

		self.renderer = Renderer()

	def __getattr__(self, key):
		try:
			return self[key]
		except IndexError:
			return None

	def __setattr__(self, key, value):
		self[key]=value

	def render(self, method, *args, **kwargs):
		return self.renderer.render(self)
