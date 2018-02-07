import requests
from lxml.html import fromstring


class ScrapeData():
	"""Downloads data from API and manipulates it into a list of locations"""
	def __init__(self):
		self. URL = ("https://api.findmespot.com/spot-main-web/consumer/" + 
			"rest-api/2.0/public/feed/0i9SOoPmAWhrgM15Yl41McqjrEbERSGiD/message.xml")

	def main(self):
		root = fromstring(raw_data)

	def get_xml(self):
		"""
		Makes an API Call and returns data as binary
		"""
		return requests.get(self.URL).content

	def get_coord_list(self):
		"""
		Gives list of tree branches represneting <message> tags
		"""
		return self.get_xml(self)[0].xpath('//message')
