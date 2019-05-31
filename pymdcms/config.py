from functools import wraps
from configparser import ConfigParser

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
	@checkinit
	def set(cls, section, option, value):
		try:
			cls.config.set(section, option, value)
		except:
			pass

	@classmethod
	def load(cls, fn):
		cls.fn = fn
		cls.config = ConfigParser()
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
	def options(cls, section):
		return cls.config.options(section)

	@classmethod
	@checkinit
	def items(cls, section):
		return cls.config.items(section)

	@classmethod
	@checkinit
	def has_section(cls, section):
		return cls.config.has_section(section)

	@classmethod
	@checkinit
	def has_option(cls, section, option):
		return cls.config.has_option(section, option)
