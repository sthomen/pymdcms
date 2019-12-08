import unittest
from ..util import DefaultDict

class MockDict(DefaultDict):
	defaults = {
		'foo': 'bar'
	}

class TestDefaultDict(unittest.TestCase):
	def test_defaulting_when_value_is_none(self):
		d = MockDict()

		d.bar = None
		self.assertEqual('bar', d.foo)

		d['bar'] = None
		self.assertEqual('bar', d.foo)

		d.set('bar', None)
		self.assertEqual('bar', d.foo)

	def test_not_defaulting_when_value_is_an_empty_string(self):
		d = MockDict()

		d.foo = ''
		self.assertEqual('', d.foo)

		d['foo'] = ''
		self.assertEqual('', d.foo)

		d.set('foo', '')
		self.assertEqual('', d.foo)
