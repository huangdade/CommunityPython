import json,os,base64

class util:
	def __init__(self):
		pass

	def setAvatar(self,username,filestring,dbapi):
		print "Start set Avatar"
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"wb");
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()
		print "End set Avatar"

	def getAvatar(self,username,dbapi):
		print "Start get Avatar"
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"rb");
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		print "End get Avatar"
		return result

	def setAvatarbyUid(self,uid,filestring):
		print "Start set Avatar"
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"wb");
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()
		print "End set Avatar"

	def getAvatarbyUid(self,uid):
		print "Start get Avatar"
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"rb");
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		print "End get Avatar"
		return result

	def setVideobyEid(self,uid,videostring):
		newdir = raw_input('./static/Video/'+str(uid))
		os.mkdir(newdir)
		video=open(os.path.abspath('./static/Video/'+str(uid)+'/'+str(uid)+'.3gp'),"wb");
		video.write(base64.standard_b64decode(videostring))
		video.close()
		print "set Video success"

	def setAudiobyEid(self,uid,videostring):
		newdir = raw_input('./static/Audio/'+str(uid))
		os.mkdir(newdir)
		audio=open(os.path.abspath('./static/Audio/'+str(uid)+'/'+str(uid)+'.amr'),"wb");
		audio.write(base64.standard_b64decode(videostring))
		audio.close()
		print "set Audio success"
