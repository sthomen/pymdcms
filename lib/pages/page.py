# vim:ts=4:sw=4:

from mako.template import Template
from mako.lookup import TemplateLookup

class Page(object):
	def __init__(self, config):
		self.config=config

		self.metadata={
			'template': 'page'
		}

		self.lookup=TemplateLookup(directories=[config.get('global', 'theme')], default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8')

	def render(self, args, kwargs):
		self.metadata.update({
			'base': self.config.get('global', 'base'),
			'theme': self.config.get('global', 'theme')
		})

		self.metadata['content']=Template(text=self.metadata['content']).render(**self.metadata)

		return self.lookup.get_template(self.metadata['template']).render(**self.metadata)
