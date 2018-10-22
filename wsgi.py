#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json

from backend.facebook.parser import FBParser

app = Flask(__name__)
app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}
api = Api(app)

# http://preview.risevision.com/Viewer.html?type=presentation&id=269cbe4e-4b35-4e4e-9f39-8cac09f29202
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# Parse Bitstop info from facebook and post it to db/redis
class BitStop(Resource):
    def get(self):
        parser = FBParser()
        response = parser.get_fb_post(sub_url="/bitstopkohvik/posts/")
        return {"bitstop": response}
        
    def post(self):
        pass

class Rahvatoit(Resource):
    def get(self):
        parser = FBParser()
        response = parser.get_fb_post(sub_url="/rahvatoitttu/posts/")
        return {"rahvatoit": response}
        
    def post(self):
        pass

api.add_resource(BitStop, "/bitstop")
api.add_resource(Rahvatoit, "/rahvatoit")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
