import unittest
from lxml.html import fromstring
from data_gen import ScrapeData

class TestScraper(unittest.TestCase):

	def setUp(self):
		self.scraper = ScrapeData()
		self.URL = ("https://api.findmespot.com/spot-main-web/consumer/" + 
			"rest-api/2.0/public/feed/0i9SOoPmAWhrgM15Yl41McqjrEbERSGiD/message.xml")

	def test_gets_raw_xml_as_binary(self):
		self.assertIsInstance(self.scraper.get_xml(self.URL), bytes)

	def test_xml_contains_coordinates(self):
		"""
		Checks that API call did not return an error;
		Non-error responses contain coordinates for latitude
		"""
		self.assertIn('<latitude>', str(self.scraper.get_xml(self.URL)))

	def test_gets_right_amount_of_messages(self):
		"""
		Tested against static file
		"""
		with open('example_xml.xml','r') as f:
			num_msgs = len(self.scraper.get_coord_list(fromstring(f.read())))
			self.assertEqual( num_msgs, 50)

	def test_returns_list_of_coordinates(self):
		with open('example_xml.xml','r') as f:
			XML = fromstring(f.read())
			self.assertIsInstance(self.scraper.get_coord_list(XML), list)