# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class UpdateUserInfoHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>UpdateUserInfoHandler</p><form action='/api/updateuserinfo' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#content =self.request.body
		content = '{"username":"dasda1","changemessage":{"age":15,"illness":"我是小啊小苹果"}}'
		j = json.loads(content)
		user = self.application.dbapi.getUserByUserName(j['username'])
		if(user is None):
			self.write("{'state':1}")
			print "username not exist"
			return
		result = self.application.dbapi.updateUserinfo(user['id'],j['changemessage'])
		self.write("{'result':"+ str(result)+"}")
		print("UpdateUserInfo success")
		return