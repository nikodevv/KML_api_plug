import requests
from lxml.html import fromstring
from simplekml import Kml

class ScrapeData():
	"""Downloads data from API and manipulates it into a list of locations"""
	def __init__(self):
		URL = ("https://api.findmespot.com/spot-main-web/consumer/" + 
			"rest-api/2.0/public/feed/0i9SOoPmAWhrgM15Yl41McqjrEbERSGiD/message.xml")

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

	def make_kml_object(self):
		kml = Kml()
		kml.document.name = "Test"
		kml.newpoint()