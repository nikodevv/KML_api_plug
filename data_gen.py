import requests
from lxml.html import fromstring
from simplekml import Kml

class ScrapeData():
	"""Downloads data from API and manipulates it into a list of locations"""
	def __init__(self):
		URL = ("https://api.findmespot.com/spot-main-web/consumer/" + 
			"rest-api/2.0/public/feed/0i9SOoPmAWhrgM15Yl41McqjrEbERSGiD/message.xml")
		# consider refactoring so indexes are passed as arguments
		self.indx = {
		'id': 0, 'msngr_id': 1,'msngr_name': 2,'unixTime': 3,
		'msg_typ': 4, 'lat': 5,'long': 6,'model_id': 7,
		'custm_msg': 8,'dtime': 9, 'bat': 10,'hidden': 11,
		'alt': 12
		}
		# Not necessary: included because it was in the old file
		self.description_str = "<![CDATA[Date: ]]><br/><![CDATA[Time: UTC]]>"


	def get_xml(self, URL):
		"""
		Makes an API Call and returns data as binary
		"""
		return requests.get(URL).content

	def get_coord_list(self, XML):
		"""
		Gives list of tree branches represneting <message> tags
		"""
		return XML.xpath('//message')

	def create_point(self, kml, msg_data):
		"""
		returns a kml.newpoint object of the form
		"""
		# name, altitude mode have to be set in initialization 
		point = kml.newpoint(name=self.get_time(msg_data), 
			altitudemode='clamptoground') 
		# original file coords also set height, but since every point
		# had a height of 0, I don't bother with it.
		point.coords = self.get_coords(msg_data)
		point.description = self.description_str
		return point

	def get_coords(self,msg_data):
		return (msg_data[self.indx['lat']].text,msg_data[self.indx['long']].text)

	def get_time(self, msg_data):
		""" currently missing 'position #' format """
		# -13 and -8 indexes are consistent across all formats 
		# I've seen. If this causes issues
		# then regex should be used
		return msg_data[self.indx['dtime']].text[-13:-8]

	def give_kml_obj(self, msg_list):
		kml = Kml()
		for msg_data in msg_list:
			self.create_point(kml, msg_data)
		return kml
