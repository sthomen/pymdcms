from .page import Page

class Handler(object):
	def getpage(self, request):
		return Page()

	def reload(self):
		pass
