import unittest
from ..version import Version

class TestVersion(unittest.TestCase):
	def test_loading_from_string(self):
		version = Version()
		version.fromString('1.0.0')
		self.assertEqual([1,0,0], version)

	def test_overwriting_version_from_string_that_is_longer_than_existing(self):
		version = Version(1,2,3)
		version.fromString('2.3.4.5')

		self.assertEqual([2,3,4,5], version)

	def test_overwriting_version_from_string_that_is_shorter_than_existing(self):
		version = Version(1,2,3)
		version.fromString('4.5')

		self.assertEqual([4,5], version)

	def test_loading_from_non_numeric_string(self):
		version = Version()
		with self.assertRaises(ValueError):
			version.fromString('a.b.c')

	def test_creating_version_with_non_numeric_values(self):
		with self.assertRaises(ValueError):
			version = Version('a', 'b', 'c')

	def test_creating_version_with_single_string_value(self):
		version = Version('1.0.0')
		self.assertEqual([1,0,0], version)

	def test_creating_version_with_single_int_value(self):
		version = Version(1)
		self.assertEqual([1], version)

	def test_float_conversion(self):
		version = Version(0,0,1)
		self.assertEqual(0.01, float(version))

		version = Version(1)
		self.assertEqual(1.0, float(version))

		version = Version(1,2,3)
		self.assertEqual(1.23, float(version))
