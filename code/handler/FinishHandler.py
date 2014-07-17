import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class FinishHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>FinishHandler</p><form action='/api/finish' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#content =self.request.body
		content = '{"username":"test1","eventid":1}'
		j = json.loads(content)
		uid = self.application.dbapi.getUserByUserName(j['username'])["id"]
		event = self.application.dbapi.getEventByEventId(j['eventid'])
		if(event is None):
			self.write("{'state':1}")
			print "event not exist"
			return
		rNamelist = self.application.dbapi.getAllRelativeNamebyUid(event["usrid"])
		print rNamelist
		if(uid not in rNamelist):
			self.write("{'state':2}")
			print "user not relative or itself,can not update sate"
			return
		self.application.dbapi.changeEventState(j['eventid']);
		self.write("{'state':3}")
		print "finsh an event"
		return
