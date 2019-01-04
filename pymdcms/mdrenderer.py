from markdown import markdown

class MDRenderer(object):
	"""
	A wrapper for markdown, mostly to add the extras for the python
	markdown.
	"""
	@staticmethod
	def render(md):
		return markdown(md, extensions=['markdown.extensions.extra'])
