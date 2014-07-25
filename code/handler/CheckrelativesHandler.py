# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import os,json
class CheckrelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>CheckrelativesHandler</p><form action='/api/checkrelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#content =self.request.body
		content = '{"username":"test1"}'
		j = json.loads(content)
		userid=self.application.dbapi.getUserByUserName(j['username'])["id"]
		re=self.application.dbapi.CheckRelationbyId(userid)
		if re!=():
			relatives=[]
			for row in re:
				info=self.application.dbapi.getUsermassegeByUserId(row["cid"])
				#relatives.append('{"info":'+str(info)+',"avatar":'+self.application.util.getAvatarbyUid(info['id'])+'}')
				relatives.append(json_encode(info))
			data={'state':1,'ralatives':json_encode(relatives)}
		else:
			data={'state':1,'relatives':'[]'}
		self.write(data)
