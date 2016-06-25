# vim:ts=4:sw=4:

from mako.template import Template
from mako.lookup import TemplateLookup

class Page(object):
	lookup=None

	def __init__(self, config, menus):
		self.config=config

		if not Page.lookup:
			Page.lookup=TemplateLookup(directories=[config.get('global', 'theme')], default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8')

		# set metadata defaults
		self.metadata={
			'base': config.get('global', 'base'),		# meta base path
			'theme': config.get('global', 'theme'),		# default theme directory
			'template': 'page',							# default page template
			'menus': menus								# expose menus to template engine
		}

	def render(self, args, kwargs):
		self.metadata['content']=Template(text=self.metadata['content']).render(**self.metadata)

		return self.lookup.get_template(self.metadata['template']).render(**self.metadata)
