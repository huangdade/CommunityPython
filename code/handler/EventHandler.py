import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class EventHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>eventHandler</p><form action='/api/event' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#conteng=self.request.body
		content='{"eventid":1}'
		jobj=json.loads(content)
		helpevent=self.application.dbapi.getEventByEventId(jobj['eventid'])
		result={}
		if(helpevent):
			result['event']=(helpevent)
			result['support']=self.application.dbapi.getSupportsByEventId(jobj['eventid'])
		return result