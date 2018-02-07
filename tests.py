import unittest
from lxml.html import fromstring
from data_gen import ScrapeData

class TestScraper(unittest.TestCase):

	def setUp(self):
		self.scraper = ScrapeData()

	def test_gets_raw_xml_as_binary(self):
		self.assertIsInstance(self.scraper.get_xml(), bytes)

	def test_xml_contains_coordinates(self):
		"""
		Checks that API call did not return an error;
		Non-error responses contain coordinates for latitude
		"""
		self.assertIn('<latitude>', str(self.scraper.get_xml()))

	def test_gets_right_amount_of_messages(self):
		"""
		Tested against static file
		"""
		# Overriding ScrapeData function for testing purposes.
		# The base function get_coord_list cannot be unit tested
		# due to compositionality
		def override_get_xml(self):
			# f is unassigined until with statement
			return fromstring(f.read())
		self.scraper.get_xml = override_get_xml

		with open('example_xml.xml','r') as f:
			self.assertEqual(len(self.scraper.get_coord_list()), 50)

	def test_returns_list_of_coordinates(self):
		self.assertIsInstance(self.scraper.get_coord_list(), list)