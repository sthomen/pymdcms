import unittest
from ..util import DefaultDict

class MockDict(DefaultDict):
	defaults = {
		'foo': 'bar'
	}

class TestDefaultDict(unittest.TestCase):
	def test_unset_items_without_default_are_None(self):
		d = MockDict()
		self.assertEqual(None, d.bar)

	def test_item_assignment(self):
		d = MockDict()

		d['bar'] = 'baz'
		self.assertEqual('baz', d['bar'])

	def test_attribute_assignment(self):
		d = MockDict()

		d.bar = 'baz'
		self.assertEqual('baz', d.bar)

	def test_setting_with_set(self):
		d = MockDict()

		d.set('bar', 'baz')
		self.assertEqual('baz', d.get('bar'))

	def test_defaulting_when_value_is_none(self):
		d = MockDict()

		d.foo = None
		self.assertEqual('bar', d.foo)

	def test_overwriting_default_values(self):
		d = MockDict()

		d.foo = 'baz'
		self.assertEqual('baz', d.foo)
