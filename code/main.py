import tornado.ioloop
import tornado.web
import tornado.httpserver
import os,MySQLdb,dbapi,util
from handler import *
from push import *

#login url handler
class IndexHandler(tornado.web.RequestHandler):
				def get(self):
								self.render("index.html")

class app(tornado.web.Application):
	def __init__(self):
		settings = {
			"static_path": os.path.join(os.path.dirname(__file__), "static"),
			"debug": True
		}
		handlers=[(r"/",IndexHandler),
			(r"/api/login",LoginHandler.LoginHandler),
			(r"/api/register",RegisterHandler.RegisterHandler),
			(r"/api/userauthentication",AuthenHandler.AuthenHandler),
			(r"/api/logout",LogoutHandler.LogoutHandler),
			(r"/api/cancel",CancelHandler.CancelHandler),
			(r"/api/checkrelatives",CheckrelativesHandler.CheckrelativesHandler),
			(r"/api/deleterelatives",DeleterelativesHandler.DeleterelativesHandler),
			(r"/api/addrelatives",AddrelativesHandler.AddrelativesHandler),
			(r"/api/history",HistoryHandler.HistoryHandler),
			(r"/api/helpmessage",HelpmessageHandler.HelpmessageHandler),
			(r"/api/supportmessage",SupportmessageHandler.SupportmessageHandler),
			(r"/api/finish",FinishHandler.FinishHandler),
			(r"/api/givecredit",GivecreditHandler.GivecreditHandler),
			(r"/api/addaid",AddaidHandler.AddaidHandler),
			(r"/api/sendsupport",SendsupportHandler.SendsupportHandler),
			(r"/api/quitaid",QuitaidHandler.QuitaidHandler),
			(r"/api/event",EventHandler.EventHandler),
			(r"/api/updatecid",UpdateCid.UpdateCid),
			(r"/api/updateuserinfo",UpdateUserInfoHandler.UpdateUserInfoHandler),
			(r"/api/getAround",GetArroundEvent.GetArroundEvent),
			(r"/api/startfollow",startFollowHandler.startFollowHandler),
			(r"/api/cancelfollow",cancelFollowHandler.cancelFollowHandler),
			(r"/api/thirdpartlogin",ThirdPartHandlers.ThirdPartyLoginHandler),
			(r"/api/thirdpartlogout",ThirdPartHandlers.ThirdPartyLogoutHandler),
			(r"/api/thirdpartremove",ThirdPartHandlers.ThirdPartyRemoveAccountHandler)]
		tornado.web.Application.__init__(self,handlers,**settings)
		self.dbapi=dbapi.dbapi()
		self.util=util.util()
		self.push = Push()
		

if __name__=="__main__":
	server=tornado.httpserver.HTTPServer(app())
	server.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
