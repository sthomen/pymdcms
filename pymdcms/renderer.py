from mako.template import Template
from mako.lookup import TemplateLookup

from .config import Config

class Renderer(object):
	lookup = None

	def __init__(self):
		if not Renderer.lookup:
			Renderer.lookup = TemplateLookup(
				directories=Config.get('global', 'theme'),
				default_filters=['decode.utf8'],
				input_encoding='utf-8', 
				output_encoding='utf-8')

	def add_path(self, path):
		self.lookup.directories.append(path)
		return self

	def render(self, page):
		# render into a copy
		values = dict(page)
		values['content'] = page.content

		return self.raw(page.template, values)

	def raw(self, template, data={}):
		return self.lookup.get_template(template).render(**data)
