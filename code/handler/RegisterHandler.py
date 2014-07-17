# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json,base64,os

class RegisterHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>RegisterHandler</p><form action='/api/register' method='post'><input type='submit' value='submit'></form>")	

	def post(self):
		content =self.request.body
		#content = '{"username": "test","password": "1","kind": 1, "cardid":"test" ,"realname":"1","sex":1,"age":1, "address":"1","illness":"1","file":"1"}'
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
		#avatar=open(os.path.abspath('./static/avatar/test.png'),"rb");
		#ilestring=base64.standard_b64encode(avatar.read())
		#self.application.util.setAvatar(j['username'],filestring,self.application.dbapi)
		
		#self.application.util.setAvatar(j['username'],j['file'],self.application.dbapi)
		self.write("{'state':3}")
		print("Register success")
		return