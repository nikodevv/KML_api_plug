import requests
from lxml.html import fromstring

URL = ("https://api.findmespot.com/spot-main-web/consumer/" + 
	"rest-api/2.0/public/feed/0i9SOoPmAWhrgM15Yl41McqjrEbERSGiD/message.xml")

for x in messages:
	print(x)

class ScrapeData():
	"""Downloads data from API and manipulates it into a list of locations"""
	def main():
		raw_data = requests.get(URL).content # Downloads data from API
		root = fromstring(raw_data)
		messages = root[0].xpath('//message')
	