import unittest
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