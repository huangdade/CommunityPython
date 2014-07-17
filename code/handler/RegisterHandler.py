# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json,base64,os

class RegisterHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>RegisterHandler</p><form action='/api/register' method='post'><input type='submit' value='submit'></form>")	

	def post(self):
		#content = self.get_argument("content")
		content = '{"username": "12","password": "1","kind": 1, "cardid":"12" ,"realname":"1","sex":1,"age":1, "address":"1","illness":"1","file":"1"}'
		j = json.loads(content)
		if(self.application.dbapi.getUserByUserName(j['username']) is not None):
			self.write("{'state':1}")
			print "username exist"
			return
		if(self.application.dbapi.getInfoBycardid(j['cardid']) is not None):
			self.write("{'state':2}")
			print "cardid exist"
			return
		self.application.dbapi.register(j)

		#test
		avatar=open(os.path.abspath('./static/avatar/test.png'),"rb");
		filestring=base64.standard_b64encode(avatar.read())
		self.application.util.setAvatar(j['username'],filestring,self.application.dbapi)
		
		u = self.application.dbapi.getUserByUserName(j['username']);
		self.write("{'state':3}")
		print("Register")
		return

	