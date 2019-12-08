class DefaultDict(dict):
	"""
	A dictionary that lets you specify defaults for values.
	Subclasses should define a defaults class variable, and
	values set (using any of the four methods) will have the
	value loaded from the defaults, if there is one.
	"""
	defaults = {}

	def __init__(self, **values):
		"""
		Initialize the object, with a shorthand definition
		to set the values at once. Note that update respects
		the defaults.
		"""
		self.update(**values)

	def __getattr__(self, name):
		"""
		I perfer foo.bar instead of foo['bar'], so here is
		an override that does this. If the value isn't found
		an attempt is made to load it from the defaults;
		if no value is found then then just return None
		"""
		if name in self:
			return self[name]

		return self.__class__.defaults.get(name)

	def __setattr__(self, name, value):
		"""
		Enable setting values like attributes, this also
		invokes the defaults, so that if a value is empty
		the default value vill be stored (if there is one)
		"""
		self[name] = value

	def __setitem__(self, name, value):
		"""
		Set items, but use the defaults if the value is None
		"""
		if not value and name in self.__class__.defaults.keys():
			self[name] = self.__class__.defaults.get(name)
			return

		dict.__setitem__(self, name, value)

	def update(self, **kwargs):
		"""
		Override for the dict update method, to invoke our
		__setitem__ method.
		"""
		for k,v in kwargs.items():
			self[k]=v

	def set(self, key, value = None):
		"""
		Chainable setting method
		"""
		self[key] = value
		return self
