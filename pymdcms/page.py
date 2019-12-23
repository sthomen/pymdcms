from .config import Config
from .menus import Menus
from .renderer import Renderer
from .util.defaultdict import DefaultDict

class Page(DefaultDict):
	def __init__(self):
		DefaultDict.__init__(self,
			theme=Config.get('global', 'theme'),
			template='page',
			menus=Menus,
			headers={'Content-Type': 'text/plain'})

		self.renderer = Renderer()

	def render(self, request):
		return self.renderer.render(self)
