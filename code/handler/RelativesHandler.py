# -*- coding: utf-8 -*-
'''Yeqin Zheng, 09/07/2014'''
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json

''' Add a relation between two users. Succeed with "1" returned, else with "0". '''

class AddrelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AddrelativesHandler</p><form action='/api/addrelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"u_name":"test1","r_name":"test5","info":"i am",'kind':}'
		j = json.loads(content)
		row = self.application.dbapi.getRelationByUsername(j['u_name'], j['r_name'])
		if row == 0:
			#self.application.dbapi.addRelationByUsername(j['u_name'], j['r_name'])
			self.application.dbapi.addtempRelationByUsername(j['u_name'], j['r_name'],j['kind'])
			#push data
			cid = self.application.dbapi.getUserByUserName(j['r_name'])['cid']
			pushdata = {}
			datainside = {}
			pushdata['type'] = "invite"
			datainside['user'] = j['u_name']
			datainside['info'] = j['info']
			pushdata['data'] = datainside
			self.application.push.pushToSingle(cid,pushdata)
			add_message = {'state': 1}
			print "add relative success"
		else:
			add_message = {'state': 0}
			print "two already has relative relation"
		self.write(add_message)
		return

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
				info['kind'] = row['kind']
				#relatives.append('{"info":'+str(info)+',"avatar":'+self.application.util.getAvatarbyUid(info['id'])+'}')
				relatives.append(info)
			data={'state':1,'ralatives':relatives}
			print data
		else:
			data={'state':1,'relatives':'[]'}
		self.write(json_encode(data))

'''Yeqin Zheng, 09/07/2014'''
''' Delete a relation between two users. Succeed with "1" returned, else with "0". '''
class DeleterelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>DeleterelativesHandler</p><form action='/api/deleterelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username1":"ooo","username2":"11oo"}'
		j = json.loads(content)
		row = self.application.dbapi.getRelationByUsername(j['username1'],j['username2'])
		if row == 0 :
			delete_message = {'state': 0}
			print "two has no relations"
		else :
			self.application.dbapi.deleteRelationByUsername(j['username1'],j['username2'])
			print "delete relations success"
			delete_message = {'state': 1}

		self.write(delete_message)
		return

class AgreerelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AgreerelativesHandler</p><form action='/api/agreerelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"u_name":"ooo","c_name":"11oo","kind": ,"agree":1(1同意，0不同意)}'
		j = json.loads(content)
		if(j['agree'] == 1):#删除temprelation，添加relation,返回状态1，推送数据到uid
			self.application.dbapi.deletetemprelation(uid,cid)
			self.application.dbapi.addrelation(uid,cid,j['kind'])
			state = {'state':1}
		else:#删除temprelaiton
			self.application.dbapi.deletetemprelation(uid,cid)
			state = {'state':1}
		self.write(json_encode(state))
		return