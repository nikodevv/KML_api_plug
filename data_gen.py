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

	def make_kml_object(self): # Temporary function to be deleted
		kml = Kml()
		kml.document.name = "Test"
		kml_points = map(self.create_one_point())

	def create_one_point(self, kml, msg_data):
		"""
		returns a kml.newpoint object of the form
		"""
		point = kml.newpoint(name=self.get_date(msg_data[INDEX]))
		return point


	def get_time(self, msg_data):
		""" currently missing 'position #' format """
		# -13 and -8 indexes are consistent across all formats 
		# I've seen. If this causes issues
		# then regex should be used
		time = msg_data[self.indx['dtime']][-13:-8]
		return time