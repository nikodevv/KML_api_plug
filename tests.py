import unittest
from lxml.etree import fromstring
from data_gen import ScrapeData
from simplekml import Kml, Coordinates, LineString

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
		self.sample_row1 = self.convert_list_to_etree(['913691903', '0-2440482', 
			'Lima', '1517941403', 'UNLIMITED-TRACK', '-8.38843', '-74.63849', 
			'SPOT3', 'Y', '2018-02-06T18:23:23+0000', 'GOOD', '0', '644'])
		
	def test_gets_raw_xml_as_binary(self):
		self.assertIsInstance(self.scraper.get_xml(self.URL), bytes)

	def test_xml_contains_coordinates(self):
		"""
		Checks that API call did not return an error;
		Checks that messages with coordinate attributes exist.
		"""
		self.assertIn('<latitude>', str(self.scraper.get_xml(self.URL)))

	def test_gets_right_amount_of_messages(self):
		# Tested against static file
		with open('example_xml.xml','r') as f:
			num_msgs = len(self.scraper.get_list_of_msgs(str(f.read())))
			self.assertEqual( num_msgs, 50)

	def test_returns_list_of_coordinates(self):
		with open('example_xml.xml','r') as f:
			XML = str(f.read())
			self.assertIsInstance(self.scraper.get_list_of_msgs(XML), list)

	def test_gets_time(self):
		sample_row2 = self.convert_list_to_etree(
			['913686008', '0-2440482', 'Lima', '1517940807', 
			'UNLIMITED-TRACK', '-8.74288', '-74.43631', 'SPOT3', 'Y', 
			'2018-02-06T18:13:27+0000', 'GOOD', '0', '2027'])
		self.assertEqual(self.scraper.get_time(self.sample_row1), '18:23')
		self.assertEqual(self.scraper.get_time(sample_row2, position_num=3), 
			'Position 3 at 18:13')

	def test_correct_pt_time(self):
		kml = Kml()
		point = self.scraper.create_point(kml, self.sample_row1)
		self.assertEqual(point.name, '18:23')

	def test_sets_altitudemode(self):
		kml = Kml()
		point = self.scraper.create_point(kml, self.sample_row1)
		self.assertEqual(point.altitudemode, 'clampedToGround')

	def test_sets_coords(self):
		""" 
		The coords are private variables, so they can't be 
		tested directly. Instead this test just checks they exist
		"""
		kml = Kml()
		point = self.scraper.create_point(kml, self.sample_row1)
		self.assertIsInstance(point.coords, Coordinates)
	
	def test_set_description(self):
		date = self.sample_row1[self.indx['dtime']].text[:10]
		description_str= ("<![CDATA[Date: %s]]><br/><![CDATA[Time: UTC]]>" % date)
		self.assertEqual(self.scraper.get_description(self.sample_row1),
			description_str)

	def test_line_sgmnt(self):
		""" 
		The segment specs are private variables. This tests whetehr line
		segments can be made.
		"""
		sample_row2 = self.convert_list_to_etree(
			['913686008', '0-2440482', 'Lima', '1517940807', 
			'UNLIMITED-TRACK', '-8.74288', '-74.43631', 'SPOT3', 'Y', 
			'2018-02-06T18:13:27+0000', 'GOOD', '0', '2027'])
		kml = Kml()
		line = self.scraper.create_line_sgmnt(kml, self.sample_row1,
			sample_row2)
		self.assertIsInstance(line, LineString)

	def test_is_ascii(self):
		"""
		Tests are done without http requests; static files are used instead.
		This test makes sure that static files are valid (simplekml doesn't
		like higher order characters).
		"""
		with open('example_xml.xml','r') as f:
			XML = fromstring(f.read())
			self.assertTrue(all(ord(c) < 128 for c in str(XML)))
	def convert_list_to_etree(self, list_):
		"""
		used to conert test strings to the type of 
		data returned by api.findmespot
		"""
		return [fromstring(self.to_xml(item)) for item in list_]

	def to_xml(self,value):
		"""wraps values in XML tags"""
		return'<Element>' + str(value) +'</Element>'
