
class Version(list):
	"""
	A simple class for comparing version numbers.

	Version values can be created in a number of ways, these are all equal:

	Version(1,0,0)
	Version('1.0.0')
	Version().fromString('1.0.0')
	
	Version objects are derived from list, and can thus be compared like a
	list of integers. Note that because of this, 1.0 and 1.0.0 are not equal,
	and 1.0.0 would be greater than 1.0.

	Implement zero-padding if that seems necessary.
	"""
	def __init__(self, *initial):
		# Allow loading values from the first initial value if it's a string
		if len(initial) == 1 and type(initial[0]) != int:
			self.fromString(initial[0])
			return

		# Test if values are numeric
		for n in initial:
			int(n)
			
		# The list starts out blank, so just extend
		self.extend(initial)

	def __float__(self):
		"""
		Coerce the version number to a float, this is merely intended as
		a method for handling backwards compatibility to when I lazily typed
		version = 1.0 into the pymdcms __init__.py file.

		This turns any version number to a floating point number of the
		major number as the integer value and the fraction being each
		subsequent number; e.g.

		'1.2.3' = 1.23
		'0.0.1' = 0.01

		"""
		output = 0.0

		for index,value in enumerate(self):
			if value > 0:
				output+=float(value) * (10 ** -index)

		return output
			

	def fromString(self, string: str):
		"""
		Load version number into this Version object from a period-separated
		string, replacing the current value.
		"""
		values = string.split('.')

		# This loop is here to convert values to integers, and throw errors
		# if they're not
		for index,value in enumerate(values):
			values[index] = int(value)

		# It should now be safe to update ourself
		self.clear()
		self.extend(values)

		return self
