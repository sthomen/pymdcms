from .page import Page

class Handler(object):
	def getpage(self, route):
		return Page()

	def reload(self):
		pass
