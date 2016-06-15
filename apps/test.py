# vim:ts=4:sw=4:

class Test(object):
	def dispatch(self, *args, **kwargs):
		return self.render(args, kwargs)

	def render(self, args, kwargs):
		return '''This is an applet!, the arguments given to it were:
(args) {} and:
(kwargs) {}'''.format(','.join(args), ','.join(["{}={}".format(k,w) for k,w in kwargs.items()]))
