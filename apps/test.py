# vim:ts=4:sw=4:

class Test(object):
	def __init__(self):
		self.metadata={}

	def dispatch(self, *args, **kwargs):
		return self.render(args, kwargs)

	def render(self, args, kwargs):
		self.metadata['title']='Applet'

		return '''<p>This is an applet!, the arguments given to it were:
                  <pre>(PATH_INFO) {}</pre>
                  and:
                  <pre>(QUERY_STRING) {}</pre></p>'''.format(', '.join(args), ', '.join(["{} = {}".format(k,w) for k,w in kwargs.items()]))
