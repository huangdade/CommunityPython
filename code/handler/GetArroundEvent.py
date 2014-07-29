import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json

class GetArroundEvent(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>GetArroundEvent</p><form action='/api/getAround' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		j=json.loads(content)
		user = self.application.dbapi.getUserInfobyName(j['username'])
		if(user is None):
			self.write("{'state':2}")
			print "username not exist"
			return
		result = self.application.dbapi.getEventAround(user['longitude'],user['latitude'],5)
		self.write("{'state':1,aids:"+json_encode(result)+"}")
		return
