import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
from sets import Set
import json

class HelpmessageHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>HelpmessageHandler</p><form action='/api/helpmessage' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"username":"test1","video":"TestAssist","audeo":"dsds","message":{"kind":1,"content":"TestContent", "videosign":1,,"audiosign":1,"latitude":23.000000,"longitude":23.000000}}'
		jobj=json.loads(content)
		result = self.application.dbapi.addEventByUserName(jobj["username"],jobj["message"])
		#add push message,make all distance 5km

		if(jobj['message']['videosign'] == "1"):
			self.application.util.setVideobyEid(result['eventid'],jobj['video'])

		if(jobj['message']['audiosign'] == "1"):
			self.application.util.setAudiobyEid(result['eventid'],jobj['audio'])

		if(result["state"] == 1):
			eventinfo = self.application.dbapi.getEventandUserByEventId(result['eventid'])
			#eventinfo['audio'] = jobj['message']['videosign']
			#eventinfo['video'] = jobj['message']['audiosign']
			print '{"type":"help","data":'+json_encode(eventinfo)+'}'
			info = self.application.dbapi.getUserInfobyName(jobj["username"])
			cidlist = self.application.dbapi.getUserCidAround(info["longitude"],info["latitude"],5)
			cidlist =  list(Set(cidlist))
			cid = self.application.dbapi.getUserByUserName(jobj['username'])['cid']
			cidlist.remove(cid)
			self.application.push.pushToList(cidlist,'{"type":"help","data":'+json_encode(eventinfo)+'}')
		
		self.write(json_encode(result))
		return

class EventHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>eventHandler</p><form action='/api/event' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content=self.request.body
		#content='{"username":"test4","eventid":1}'
		jobj=json.loads(content)
		uid = self.application.dbapi.getUserByUserName(jobj['username'])["id"]
		helpevent=self.application.dbapi.getEventandUserByEventId(jobj['eventid'])
		result={}
		if(helpevent):
			helpevent['follows'] = self.application.dbapi.getFollowsByEventId(jobj['eventid'])['count']
			helpevent['helpers'] = len(self.application.dbapi.getHelpersCidbyEid(jobj['eventid']))
			result['event']=helpevent
			ishelper = self.application.dbapi.checkifUseraddHelper(uid,jobj['eventid'])
			if(ishelper is None):
				if(helpevent['username'] == jobj['username']):
					result['ishelper'] = 1
				else:
					result['ishelper'] = 0
			else:
				result['ishelper'] = 1
			rNamelist = self.application.dbapi.getAllRelativeNamebyUid(helpevent['userid'])
			print rNamelist
			if(uid in rNamelist):
				result['canend'] = 1
			else:
				result['canend'] = 0
			if(self.application.dbapi.getFollow(uid,jobj['eventid']) is None):
				result['isfollow'] = 0
			else:
				result['isfollow'] = 1
			result['support']=self.application.dbapi.getSupportsByEventId(jobj['eventid'])
			for support in result['support']:
				user=self.application.dbapi.getUserByUserId(support['usrid'])
				if(user):
					support['username']=user['name'];
					#avatar=self.application.util.getAvatar(user['name'],self.application.dbapi)
					#support['avatar']=avatar
		print json_encode(result)
		self.write(json_encode(result))

'''Yeqin Zheng, 09/07/2014'''
''' Add a helper to an event. Succeed with "1" returned, else with "0". '''
class AddaidHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AddaidHandler</p><form action='/api/addaid' method='post'><input type='submit' value='submit'></form>")
	def post(self):
		content = self.request.body
		#content = '{"username":"test1","eventid":"4"}'
		j = json.loads(content)

		result = self.application.dbapi.addaidhelper(j['username'], j['eventid'])
		self.write("{'state': " + result + "}")


class FinishHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>FinishHandler</p><form action='/api/finish' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"test1","eventid":1}'
		j = json.loads(content)
		uid = self.application.dbapi.getUserByUserName(j['username'])["id"]
		event = self.application.dbapi.getEventByEventId(j['eventid'])
		if(event is None):
			self.write("{'state':1}")
			print "event not exist"
			return
		rNamelist = self.application.dbapi.getAllRelativeNamebyUid(event["usrid"])
		print rNamelist
		if(uid not in rNamelist):
			self.write("{'state':2}")
			print "user not relative or itself,can not update sate"
			return
		currenttime = self.application.dbapi.changeEventState(j['eventid'])
		helpers =  self.application.dbapi.getHelperInfoByEid(j['eventid'])
		data = []
		for item in helpers:
			info = {}
			info['username'] = item['username']
			info['uid'] = item['uid']
			data.append(info)
			#data.append("{'username':" + str(item['username']) + ",'uid':"+ str(item['uid'])+"}")
		print data
		writedata = {}
		writedata['state'] = 3
		writedata['helpers'] = data
		print writedata
		#push
		"""pushlist = self.application.dbapi.getFollowerCidByEid(jobj['eid'])
		helperlist = self.application.dbapi.getHelpersCidbyEid(jobj['eid'])
		pushlist.extend(helperlist)
		relativelist = self.application.dbapi.getRelativesCidbyUid(uid)
		pushlist.extend(relativelist)
		pushlist =  list(Set(pushlist))
		cid = self.application.dbapi.getUserByUserName(j['username'])['cid']
		cidlist.remove(cid)
		pushdata = {}
		data = {}
		pushdata['type'] = "endhelp"
		data['eventid'] = j['eventid']
		data['time'] = currenttime.strftime('%Y-%m-%d %H:%M:%S')
		pushdata['data'] = data
		self.application.push.pushToList(pushlist,pushdata)"""
		self.write(json_encode(writedata))
		print "finsh an event"
		return


class GivecreditHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>GivecreditHandler</p><form action='/api/givecredit' method='post'><input type='submit' value='submit'></form>")
	def post(self):
		content =self.request.body
		#content='{"eventid":4,"helpername":"test2","credit":3}'
		#content='{"eventid":1,"credits":[{"username":"test2","cridit":5},{"username":"test6","cridit":1}]}'
		jobj=json.loads(content)
		result=[]
		for issue in jobj["credits"]:
			temp=self.application.dbapi.setCreditByEventIdAndUserName(jobj["eventid"],issue["username"],issue["cridit"])
			result.append({"helpername":issue["username"],"result":temp});
		self.write(str(result))

class QuitaidHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>QuitaidHandler</p><form action='/api/quitaid' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"oo11o","eventid":5}'
		j = json.loads(content)
		uid = self.application.dbapi.getUserByUserName(j['username'])['id']
		if(self.application.dbapi.getEventByEventId(j['eventid'])['state'] == 1):
			print "current had been end,you can not quit"
			self.write("{'state':3}")
			return

		if(self.application.dbapi.checkifUseraddHelper(uid,j['eventid']) is None):
			print "user " + j['username'] +" do not add the aid first"
			self.write("{'state':2}")
			return
		self.application.dbapi.deleteHelperbyUidEid(uid,j['eventid'])
		print "quit success"
		self.write("{'state':1}") 
		return

class SendsupportHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>SendsupportHandler</p><form action='/api/sendsupport' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"username":"test1","eid":4,"message":{"content":"TestssCofffntent"}}'
		jobj=json.loads(content)
		result=self.application.dbapi.addSupportByEventIdAndUserName(jobj["eid"],jobj["username"],jobj["message"])
		"""if(result['errorCode'] == 200):
			pushlist = self.application.dbapi.getFollowerCidByEid(jobj['eid'])
			datatemp = self.application.dbapi.getSupportBySid(result['supportid'])
			pushdata = {}
			data = {}
			pushdata['type'] = 'aid'
			data['user'] = jobj['username']
			data['content'] = datatemp['content']
			data['time'] = datatemp['time'].strftime('%Y-%m-%d %H:%M:%S')
			data['eventid'] = jobj['eid']
			pushdata['data'] = data
			self.application.push.pushToList(pushlist,pushdata)"""
		self.write(json_encode(result))


class SupportmessageHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>SupportmessageHandler</p><form action='/api/supportmessage' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		content = '{"eventid": 3,"video": "ssssssssssssssss","audio":"ddddd"}'
		"""#content = '{"username": "ooo","eventid": 3,"video": "ssssssssssssssss","audio":""}'
		j = json.loads(content)
		us = self.application.dbapi.getUserByUserName(j['username'])
		if(us is None):
			self.write("{'state':1}")
			print "username not exist"
			return
		print us["id"]
		
		event = self.application.dbapi.getEventByEventId(j['eventid'])
		if(event is None):
			self.write("{'state':2}")
			print "event not exist"
			return
		if (event['state']==1):
			self.write("{'state':3}")
			print "event is end"
			return
		if(us["id"]==event["usrid"]):
			self.application.dbapi.supportmessageinsert(j)
			self.write("{'state':4}")
			print "insert success"
			return
		return"""
		j = json.loads(content)
		if('video' in j):
			self.application.util.setVideobyEid(j['eid'],j['video'])
		if('audio' in j):
			self.application.util.setAudiobyEid(j['eid'],j['video']) 