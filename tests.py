import unittest
from lxml.etree import fromstring
from data_gen import ScrapeData
from simplekml import Kml, Coordinates

class TestScraper(unittest.TestCase):

	def setUp(self):
		self.scraper = ScrapeData()
		self.URL = ("https://api.findmespot.com/spot-main-web/consumer/" + 
			"rest-api/2.0/public/feed/0i9SOoPmAWhrgM15Yl41McqjrEbERSGiD/message.xml")
		self.indx = {
		'id': 0, 'msngr_id': 1,'msngr_name': 2,'unixTime': 3,
		'msg_typ': 4, 'lat': 5,'long': 6,'model_id': 7,
		'custm_msg': 8,'dtime': 9, 'bat': 10,'hidden': 11,
		'alt': 12
		}
		self.sample_row1 = ['913691903', '0-2440482', 'Lima', '1517941403', 
		'UNLIMITED-TRACK', '-8.38843', '-74.63849', 'SPOT3', 'Y', 
		'2018-02-06T18:23:23+0000', 'GOOD', '0', '644']
		
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

	def test_intentional_fail(self):
		self.fail()

	def test_gets_time(self):
		# Need 2 samples for 'Position #' check - not currently in code
		sample_row2 = ['913686008', '0-2440482', 'Lima', '1517940807', 
		'UNLIMITED-TRACK', '-8.74288', '-74.43631', 'SPOT3', 'Y', 
		'2018-02-06T18:13:27+0000', 'GOOD', '0', '2027']
		self.assertEqual(self.scraper.get_time(self.sample_row1), '18:23')
		self.assertEqual(self.scraper.get_time(sample_row2), '18:13')

	def test_correct_pt_time(self):
		kml = Kml()
		point = self.scraper.create_point(kml, self.sample_row1)
		self.assertEqual(point.name, '18:23')

	def test_sets_altitudemode(self):
		# Not sure if working as intended -- Check later ------------------------------------
		kml = Kml()
		point = self.scraper.create_point(kml, self.sample_row1)
		self.assertEqual(point.altitudemode, 'clamptoground')

	def test_sets_coords(self):
		""" 
		The coords are private variables, so they can't be 
		tested directly. Instead this test just checks they exist
		"""
		kml = Kml()
		point = self.scraper.create_point(kml, self.sample_row1)
		self.assertIsInstance(point.coords, Coordinates)
