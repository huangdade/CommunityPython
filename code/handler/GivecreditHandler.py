import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class GivecreditHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>GivecreditHandler</p><form action='/api/givecredit' method='post'><input type='submit' value='submit'></form>")
	def post(self):
		#content='{"eventid":4,"helpername":"test2","credit":3}'
		content='{"eventid":1,"credits":[{"username":"test2","cridit":5},{"username":"test6","cridit":1}]}'
		jobj=json.loads(content)
		result=[]
		for issue in jobj["credits"]:
			temp=self.application.dbapi.setCreditByEventIdAndUserName(jobj["eventid"],issue["username"],issue["cridit"])
			result.append({"helpername":issue["username"],"result":temp});
		self.write(str(result))
		