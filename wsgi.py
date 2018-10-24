#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json

from backend.facebook.parser import FBParser
from backend.daily.parser import DailyParser

app = Flask(__name__)
app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}
api = Api(app)
fbparser = FBParser()
dailyparser = DailyParser()

# http://preview.risevision.com/Viewer.html?type=presentation&id=269cbe4e-4b35-4e4e-9f39-8cac09f29202
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# Parse Bitstop info from facebook and post it to db/redis
class BitStop(Resource):
    def get(self):
        response = fbparser.get_fb_post(sub_url="/bitstopkohvik/posts/")
        return {"bitstop": response}
        
    def post(self):
        pass

class Rahvatoit(Resource):
    def get(self):
        response = fbparser.get_fb_post(sub_url="/rahvatoitttu/posts/", numberOfPosts=1)
        return {"rahvatoit": response}
        
    def post(self):
        pass

class ITDaily(Resource):
    def get(self):
        response = dailyparser.get_daily_menu("https://päevapakkumised.ee/tallinn/ttü-it-maja-daily")
        return {"IT maja daily" : response}
    def post(self):
        pass

class VIKorpusDaily(Resource):
    def get(self):
        response = dailyparser.get_pdfalt_menu("http://www.daily.ee/files/dn_daily_nadalamenuu_ttu_6_korpus.pdf")
        return {"VI korpuse daily" : response}
    def post(self):
        pass

api.add_resource(BitStop, "/bitstop")
api.add_resource(Rahvatoit, "/rahvatoit")
api.add_resource(ITDaily, "/itdaily")
api.add_resource(VIKorpusDaily, "/vidaily")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
