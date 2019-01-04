# vim:ts=4:sw=4:

from mako.template import Template
from mako.lookup import TemplateLookup

from ..config import Config
from ..menus import Menus

class Page(object):
	lookup=None

	def __init__(self):
		if not Page.lookup:
			Page.lookup=TemplateLookup(directories=[Config.get('global', 'theme')], default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8')

		# set metadata defaults
		self.metadata={
			'base': Config.get('global', 'base'),
			'theme': Config.get('global', 'theme'),
			'template': 'page',
			'menus': Menus
		}

		self.metadata_defaults=self.metadata.copy()

	def reload(self):
		pass

	def render(self, method, args, kwargs):
		content=self.metadata['content'] or ''

		self.metadata['content']=Template(text=content).render(**self.metadata)

		return self.lookup.get_template(self.metadata['template']).render(**self.metadata)
