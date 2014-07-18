# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json

class HelpmessageHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>HelpmessageHandler</p><form action='/api/helpmessage' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"username":"test1","message":{"kind":1,"content":"TestContent","assist":"TestAssist","latitude":23.000000,"longitude":23.000000}}'
		jobj=json.loads(content)
		result = self.application.dbapi.addEventByUserName(jobj["username"],jobj["message"])
		#add push message,make all distance 5km
		if(result["state"] == 1):
			eventinfo = self.application.dbapi.getEventandUserByEventId(result['eventid'])
			print '{"type":"help","data":'+json_encode(eventinfo)+'}'
			info = self.application.dbapi.getUserInfobyName(jobj["username"])
			cidlist = self.application.dbapi.getUserCidAround(info["longitude"],info["latitude"],5)
			self.application.push.pushToList(cidlist,'{"type":"help","data":'+json_encode(eventinfo)+'}')
		
		self.write(json_encode(result))
		return