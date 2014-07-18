import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json

class EventHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>eventHandler</p><form action='/api/event' method='post'><input type='submit' value='submit'></form>")

	#return format
	#{event:{},support:{0:{},1:{}}}
	def post(self):
		#content=self.request.body
		content='{"eventid":1}'
		jobj=json.loads(content)
		helpevent=self.application.dbapi.getEventandUserByEventId(jobj['eventid'])
		result={}
		if(helpevent):
			result['event']=helpevent
			result['support']=self.application.dbapi.getSupportsByEventId(jobj['eventid'])

			for support in result['support']:
				user=self.application.dbapi.getUserByUserId(support['usrid'])
				if(user):
					support['username']=user['name'];
					#avatar=self.application.util.getAvatar(user['name'],self.application.dbapi)
					#support['avatar']=avatar
		print json_encode(result)
		self.write(json_encode(result));