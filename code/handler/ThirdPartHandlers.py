# coding: utf-8
# Filename: handlers.py
__author__ = 'Administrator'

import tornado.web
import json
import urllib

# 2014-07-17
#
# post: access_token, platform
# return: result
# actions:
# visit get_token_info
#     check for binding
#     create new user
#     bind user
#     update user state
# 我需要与前后台协商，除了本地登录之外，在增加第三方专用的返回值。这里就将就一下

class ThirdPartyLoginHandler(tornado.web.RequestHandler):
    platformapi = { "sinaweibo": "https://api.weibo.com/oauth2/get_token_info" }

    def post(self):
        # 获取参数access_token和platform
        access_token = self.get_argument("access_token")
        platform = self.get_argument("platform")
        # 根据platform获取对应的api地址
        url = ThirdPartyLoginHandler.platformapi.get(platform)
        # 生成api参数。这里只考虑了sinaweibo的参数格式。需要改进。
        # urllib的post参数为字符串
        data = "access_token=" + access_token
        try:
            # 访问授权服务器，获取返回值
            result = urllib.urlopen(url, data).read()
            print(result)
        except IOError:
            # 有可能出错，这时我们认为用户使用的是虚假令牌，认为登录失败
            print("IOError: fake access_token")
            # 登录失败返回state：1
            self.write("{\"state\":1}")
            return
        # 解析返回值，这里依旧只考虑了新浪微博
        j = json.loads(result)
        expire_in = j["expire_in"]
        # 如果令牌超时，则驳回请求
        if expire_in <= 0:
            # 返回state：1
            self.write("{\"state\":1}")
            return
        # 第三方不需要在本系统中设置用户名，因此自动生成一个作为第三方用户的唯一标识
        username = "*" + platform + ("%i" % j["uid"])
        # 这里做简单处理：直接将星号+platform+uid作为用户名，不设密码
        # 其他用户不允许第一个符号是星号。一般的用户名只允许出现字母，数字，空格，和下划线。
        # 首先检查是否已经注册过
        record = self.application.dbapi.getUserByUserName(username)
        isNewUser = "false"
        if record == None:
            # 如果用户不存在，则新建用户并且插入数据库
            # 新建用户时的参数参考dbapi的代码
            # content是字典格式
            # username：用户名；kind：分三种，这里可以设为1-普通用户；password：第三方用户不需密码
            # kind：int整数
            newUser = {"username": username,
                       "kind": 1,
                       "password": "",
                       "cardid": 0,
                       "realname": "",
                       "sex": 0,
                       "age": 0,
                       "address": "",
                       "illness": ""}
            self.application.dbapi.register(newUser)
            # 再次取用户记录，因为需要获取uid，而uid是系统自动分配的
            record = self.application.dbapi.getUserByUserName(username)
            isNewUser = "true"
        # 现在新用户与老用户到了同一状态
        # 现在我们认为用户已经登录成功了，需要更新用户的状态为已登录
        # 这一部分可以参考正常的loginhandler
        uid = record["id"]
        self.application.dbapi.updateUserstate(uid, 1) # 登录状态为数字1
        # 返回登录成功的返回值
        returnValue = "{'state':3," + "'isNewUser':" + isNewUser + "}";
        self.write(returnValue) # 3表示登录成功
        print("third party login succeed")
        print("return: " + returnValue)
        return

# 在第三方登录成功之后，第三方用户状态就与本地用户相同了。这里的登出过程也几乎没有区别
class ThirdPartyLogoutHandler(tornado.web.RequestHandler):
    # 数据库的所有操作都没有进行用户是否已经登录的检查。
    # 鉴于这种检查时普遍操作，可能会作为任何一项需要特权的操作的前置操作，仅仅需要修改少数类，因此这里不做检查，等待小组长修复该bug
    # 这里需要将访问方式改为post。之前考虑失误。显然应该是post
    def post(self):
        # 这与正常的登出一模一样。直接copy代码。
        # 这里用到了username。按照我的预想，是不需要username的。但是第一版可以简单设计。
        # 这需要我修改几处anroid代码
        # 其他人采用json格式传输数据。我这里并没有采用，而是直接使用参数传递。
        username = "*" + self.get_argument("platform") + self.get_argument("uid")
        print("username: " + username)
        # 因为假设所有的特权操作都经过了检查，因此不必考虑用户不存在的情况
        record = self.application.dbapi.getUserByUserName(username)
        uid = record["id"]
        self.application.dbapi.updateUserstate(uid, 0)
        self.write("{'state':1}")
        self.write("Third Party Logout Test")

class ThirdPartyRemoveAccountHandler(tornado.web.RequestHandler):
    # 与前面一个一样，这里的get也是不对的，需要改为post
    def post(self):
        # 这里也与正常注销几乎一样
        # 一般情况下，注销用户需要第二次检查，要求用户再次登录
        # 对于我们，就是再次传输了access_token
        access_token = self.get_argument("access_token")
        # 下面的一段是直接复制的，这与thirdpartylogin是一样的操作
        platform = self.get_argument("platform")
        url = ThirdPartyLoginHandler.platformapi.get(platform)
        data = "access_token=" + access_token
        try:
            result = urllib.urlopen(url, data).read()
            print(result)
        except IOError:
            print("IOError: fake access_token")
            self.write("{\"state\":1}")
            return
        j = json.loads(result)
        expire_in = j["expire_in"]
        if expire_in <= 0:
            # 返回state：1
            self.write("{\"state\":1}")
            return
        # 至此，认为用户的第二次认证成功
        # 获取用户id，删除用户
        username = "*" + platform + ("%i" % j["uid"])
        record = self.application.dbapi.getUserByUserName(username)
        uid = record["id"]
        self.application.dbapi.cancelUser(uid)
        # 用户已删除，这是返回登录成功的返回值，暗示了用户已删除
        self.write("{\"state\":3}")

class ThirdPartyFillUserInfoHandler(tornado.web.RequestHandler):
    def post(self):
        username = "*" + self.get_argument("platform") + self.get_argument("uid")
        newUserInfo = {
            "sex": self.get_argument("sex"),
            "address": self.get_argument("address")
        }
        user = self.application.dbapi.getUserByUserName(username)
        if(user is None):
            self.write("{'state':1}")
            print "username not exist"
            return
        print("username: " + username)
        print("sex: " + newUserInfo["sex"])
        print("address: " + newUserInfo["address"])
        result = self.application.dbapi.updateUserinfo(user['id'], newUserInfo)
        self.write("{'result':"+ str(result)+"}")
        print("UpdateUserInfo success")