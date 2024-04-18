from flask import Flask, send_from_directory
from flask_restful import Resource, reqparse
import os

class Cloaks(Resource):
    def get(self, user):
        list = os.listdir("pack_cloaks")
        for name in list:
            if name.split('.')[0] == user:
                return send_from_directory("pack_cloaks", name)
        
