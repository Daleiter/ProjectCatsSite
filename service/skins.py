from flask import Flask, send_from_directory
from flask_restful import Resource, reqparse
import os

class Skins(Resource):
    def get(self, user):
        list = os.listdir("pack_skins")
        for name in list:
            if name == user:
                return send_from_directory("pack_skins", name)
        
