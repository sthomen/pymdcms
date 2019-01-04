from functools import wraps
from ConfigParser import SafeConfigParser

def checkinit(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if not args[0].config:
			raise RuntimeError("Config wasn't initialized")

		return f(*args, **kwargs)

	return wrapper

class Config(object):
	config = None
	fn = None

	def __init__(self, fn):
		Config.load(fn)

	@classmethod
	def load(cls, fn):
		cls.fn = fn
		cls.config = SafeConfigParser()
		cls.config.read(cls.fn)

	@classmethod
	@checkinit
	def get(cls, section, option):
		try:
			return cls.config.get(section, option)
		except:
			return None

	@classmethod
	@checkinit
	def set(cls, section, option, value):
		cls.config.set(section, option, value)

	@classmethod
	@checkinit
	def options(cls, section):
		return cls.config.options(section)

	@classmethod
	@checkinit
	def save(cls):
		with open(cls.fn, 'wb') as fp:
			cls.config.write(fp)
