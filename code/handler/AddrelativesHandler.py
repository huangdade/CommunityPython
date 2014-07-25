'''Yeqin Zheng, 09/07/2014'''
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

''' Add a relation between two users. Succeed with "1" returned, else with "0". '''

class AddrelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AddrelativesHandler</p><form action='/api/addrelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#content =self.request.body
		content = '{"u_name":"test1","r_name":"test2"}'
		j = json.loads(content)
		row = self.application.dbapi.getRelationByUsername(j['u_name'], j['r_name'])
		if row == 0:
			self.application.dbapi.addRelationByUsername(j['u_name'], j['r_name'])
			self.application.dbapi.addtempRelationByUsername(j['u_name'], j['r_name'])
			add_message = {'state': 1}
			print "add relative success"
		else:
			add_message = {'state': 0}
			print "two already has relative relation"
		self.write(add_message)
		return
