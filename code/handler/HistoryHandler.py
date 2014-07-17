# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class HistoryHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>historyHandler</p><form action='/api/history' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#content =self.request.body
		content='{"name":"test3"}'
		jobj=json.loads(content)
		user = self.application.dbapi.getUserByUserName(jobj['name'])
		if(user is None):
			self.write('{"state":2,"decs":"User not exist"}')
			return
		uid = user['id']
		events=self.application.dbapi.getEventsByUserId(uid)
		#result=self.application.dbapi.getEventsByUserName(jobj['name'])
		supports = self.application.dbapi.getSupportsbyUid(uid)

		self.write('{"state":1,"events":'+str(events)+',"supports":'+str(supports))
		return