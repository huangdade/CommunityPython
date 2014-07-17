import json,os,base64

class util:
	def __init__(self):
		pass

	def setAvatar(self,username,filestring,dbapi):
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"wb");
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()

	def getAvatar(self,username,dbapi):
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"rb");
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		return result