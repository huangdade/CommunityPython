# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class cancelFollowHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>cancelFollowHandler</p><form action='/api/cancelfollow' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content='{"id":2,"name":"ooo"}'
		jobj=json.loads(content)
		pass
		"""
		传入格式{username:,eid:}
		先判断user是否存在，不存在返回状态2
		取消前用getFollow判断是否已经关注
		没关注过直接返回状态3，
		否则取消关注delectFollow，返回状态1
		返回格式{state：x}
		"""