import requests
from lxml.html import fromstring
from simplekml import Kml, Style
from os.path import dirname, realpath, join

class ScrapeData():
	"""Downloads data from API and manipulates it into a list of locations"""
	def __init__(self):
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

	def get_list_of_msgs(self, XML):
		"""
		Gives list of tree branches represneting <message> tags
		"""
		return fromstring(XML).xpath('//message')

	def create_point(self, kml, msg_data, position_num=None, style=Style()):
		"""
		returns a kml.newpoint object of the form
		"""
		# name, altitude mode have to be set in initialization 
		point = kml.newpoint(name=self.get_time(msg_data, 
			position_num=position_num), altitudemode='clampedToGround') 
		point.coords = self.get_coords(msg_data)
		point.style = style
		point.description = self.get_description(msg_data)
		return point

	def get_coords(self,msg_data):
		return [(msg_data[self.indx['lat']].text, msg_data[self.indx['long']].text)]

	def get_time(self, msg_data, position_num = None):
		"""Sets the time and of a point and enumerates it via position #"""
		# -13 and -8 indexes are consistent across all formats 
		prefix = ''
		if position_num != None:
			prefix = "Position %s at " % position_num
		return prefix + msg_data[self.indx['dtime']].text[-13:-8]

	def create_lines_and_base_obj(self, msg_list):
		"""
		Returns KML object with a chain of lines representing the order
		in which msg_list items are indexed.
		"""
		kml = Kml()
		for i in range(1, len(msg_list)):
			self.create_line_sgmnt(kml, msg_list[i-1], msg_list[i])	
		return kml

	def get_line_link_coords(self, msg_data1, msg_data2):
		"""
		Extracts coordinates for creating a LineString and returns
		a list of two coordinate tuples.  i.e. 'links' a pair of 
		messages' coordinates so they can be made into a LineString
		"""
		return [(
			msg_data1[self.indx['lat']].text, 
			msg_data1[self.indx['long']].text), (
			msg_data2[self.indx['lat']].text, 
			msg_data2[self.indx['long']].text)]

	def create_line_sgmnt(self, kml, msg_list1, msg_list2):
		"""
		Given full data represnting two distinct messages, returns a line 
		segment drawn between the two.
		"""
		line = kml.newlinestring(name='line segment', 
			altitudemode='clampedToGround')
		line.coords = self.get_line_link_coords(msg_list1, msg_list2)
		line.extrude = 1 # connects point to ground
		return line

	def give_kml_obj(self, msg_list):
		"""
		Initializes Kml file by calling another class function, creates
		balloon style, and plots points. Line segments are created on
		initialization. Returns a Kml object ready to be saved.
		"""
		kml = self.create_lines_and_base_obj(msg_list)
		style = Style()
		position_num = 50
		for msg_data in msg_list:
			style = self.get_point_style(style, position_num)
			self.create_point(kml, msg_data, position_num, style=style)
			position_num = position_num - 1 
		return kml

	def save_kml_obj(self, URL, DIR):
		msg_list = self.get_list_of_msgs(self.get_xml(URL))
		self.give_kml_obj(msg_list).save(DIR)

	def get_description(self,msg_data):
		"""Description string on point focus"""
		description_str= ("<![CDATA[Date: %s]]><br/><![CDATA[Time: UTC]]>" 
			%msg_data[self.indx['dtime']].text[:10])
		return description_str
	def get_point_style(self, style, position_num):
		"""sets the last icon as a plane, all others as simple dots"""
		style.iconstyle.icon.href = ('http://maps.google.com/' + 
			'mapfiles/kml/shapes/placemark_circle.png')
		if position_num == 1:
			style = Style()
			style.iconstyle.icon.href = (
				'http://maps.google.com/mapfiles/kml/pal2/icon48.png')
		return style
		
DIR = join(dirname(realpath(__file__)), 'coordinates.kml')
URL = ("https://api.findmespot.com/spot-main-web/consumer/" + 
		"rest-api/2.0/public/feed/0i9SOoPmAWhrgM15Yl41McqjrEbERSGiD/" + 
		"message.xml")
kml = ScrapeData()
kml.save_kml_obj(URL, DIR)