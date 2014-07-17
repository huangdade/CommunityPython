# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>LoginHandler</p><form action='/api/login' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#content =self.request.body
		content = '{"username":"12","password":"1"}'
		j = json.loads(content)
		if(j['username'].strip()=='' or j['password'].strip()==''):
			self.write("{'state':1}")
			print "username or password is null"
			return
		user = self.application.dbapi.getUserByUserName(j['username'])
		if(user is None):
			self.write("{'state':1}")
			print "username not exist"
			return
		if(user["password"]!= j['password']):
			self.write("{'state':2}")
			print "passwd incorrect"
			return
		self.application.dbapi.updateUserstate(user['id'],1)
		self.write("{'state':3}")
		print("Login success")
		print self.application.util.getAvatar("12",self.application.dbapi)
		return
