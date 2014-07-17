# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class startFollowHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>startFollowHandler</p><form action='/api/startfollow' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		pass
		"""
		传入格式{username:,eid:}
		先判断user是否存在，不存在返回状态2
		{username:,eid:}
		关注前用getFollow判断是否已经关注
		关注过则直接返回状态3，
		否则关注insertFollow，返回状态1
		返回格式{state：x}
		"""