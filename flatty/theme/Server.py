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

#Create second page with chosen products
class secondPageHandler(tornado.web.RequestHandler):

    def post(self):
        #extract json sent from client
        data = self.request.body
        print(type(data))
        data = data.decode()
        data = ast.literal_eval(data)
        # print (type(data))
        print(data)

        #Run data through DB
        filter = []
        sort_by = "mt"
        if '_vegetarian' in data: filter.append('vegetarian')
        if '_vegan' in data: filter.append('vegan')
        if '_gluten' in data: filter.append('gluten_safe')
        if '_sort_mt' in data: sort_by += "t"

        #db_answer = alg.return_recipes(db, data, sort_by,filter,AMOUNT)
        #todo add vegan
        # the database answer
        # proccesed_data = json.dumps({"recepies":[{"title":"hamburger",
        #                                           "image":"http://www.mediterran-leben.com/wp-content/uploads/2012/09/Spaghetti-Bolognese-1.jpg",
        #                                           "link":"https://www.yahoo.com/"},{"title":"pizza","image":"http://i.imgur.com/MwBKTI8.jpg","link":"https://www.facebook.com/"}]})
        #Send answer to client
        #print(alg.df_to_format(db_answer))
        #self.write(alg.df_to_format(db_answer))
        #self.finish



# Update Second page with new chosen products
class secondUpdateHandler(tornado.web.RequestHandler):

    def post(self):
        #extract json sent from client
        test = self.get_argument("chicken")

        #Run data jason through db
        #Todo

        #DB answer
        proccessed_data = "{\\\"recepies\\\":[{\\\"title\\\": " \
                          "\\\"hamburger\\\", \\\"image\\\": \\\"imgurl\\\", \\\"url\\\":\\\"link\\\" " \
                          "}]}"

        #Send answer to client
        self.write(proccessed_data)
        self.finish()
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


        # if pitot in alg.basic_ing_beverage+alg.basic_ing_dairy+alg.basic_ing_fruit+alg.basic_ing_grains+alg.basic_ing_grains+\
        #     alg.basic_ing_meat_fish+alg.basic_ing_meat_fish+alg.basic_ing_murder+alg.basic_ing_pastry+alg.basic_ing_sauce+\
        #     alg.basic_ing_seasoning+alg.basic_ing_sweet+alg.basic_ing_vegetable:
        #     self.write("true")
        # else:
        #     self.write("false")
        #     self.finish()

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"))

def make_app():
    return tornado.web.Application([
        (r"/", HomePageHandler),
        (r"/secondPage", secondPageHandler),
        (r"/secondPageUpdate", secondUpdateHandler),
        (r"/search", searchHandler)
        ], **settings)

# static_path=os.path.join(PATH2, 'theme')

if __name__ == "__main__":
    #db = pickle.load(open('full_dump.p','rb'))
    G, seekingList, offeringList = graph.parse_and_init('final DB.csv')
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()



