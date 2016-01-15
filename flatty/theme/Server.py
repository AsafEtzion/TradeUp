__author__ = 'GN3'
import tornado.ioloop
import tornado.web
import random
import json
import os
import re
import ast
import graph

# import DataBase as alg
import pickle

sample_size = 16 # number of chosen products from common products list
AMOUNT = 6
PATH = os.path.abspath(os.path.dirname(__file__))
PATH2 = os.path.abspath(os.path.dirname(__file__))
global G
global seekingList
global offeringList

#Create homepage, and send list of common items
class HomePageHandler(tornado.web.RequestHandler):
    def get(self):
        #common_products = str(alg.list_to_format(random.sample(alg.open_screen_products, sample_size)))
        self.render("index.html",
                    title="UpTrade!")
                    #items=common_products)





class searchHandler(tornado.web.RequestHandler):

    def post(self):
        # pitot = self.get_argument
        seek = self.get_argument("seek")
        have = self.get_argument("have")
        print(seek)
        print(have)

        #if the item the client has doesnt exist - send him Have
        result = graph.search_match(G,seekingList,offeringList,seek,have)
        if type(result) == str:
            if result == "noHave":
                self.write("noHave")
            if result == "noSeek":
                self.write("noSeek")
            if result == "noPath":
                self.write("noPath")
        #if both items are ok - create path
        else:
            # jsonResult = {"items": ["bike", "iphone"], "link": ["http://www.bikemag.com/", "http://www.apple.com/shop/buy-iphone/iphone6"]}
            # self.write(jsonResult)
            self.write(result)
        #Send json of items to client
        self.finish()


settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"))

def make_app():
    return tornado.web.Application([
        (r"/", HomePageHandler),
        (r"/search", searchHandler)
        ], **settings)


if __name__ == "__main__":
    G, seekingList, offeringList = graph.parse_and_init('final DB.csv')
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()



