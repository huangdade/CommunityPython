'''Yeqin Zheng, 09/07/2014'''
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os, json, sys
sys.path.append("..")
import  dbapi

''' Add a relation between two users. Succeed with "1" returned, else with "0". '''

class AddrelativesHandler(tornado.web.RequestHandler):
    def post(self):
        u_name = self.get_argument('u_name')
        r_name = self.get_argument('r_name')

        row = self.application.dbapi.getRelationByUsername(u_name, r_name)
        if row == 0:
            self.application.dbapi.addRelationByUsername(u_name, r_name)
            self.application.dbapi.addtempRelationByUsername(u_name, r_name)
            add_message = {'state': 1}
        else:
            add_message = {'state': 0}

        self.write(add_message)
