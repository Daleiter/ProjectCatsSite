# Файл 2: service/login.py
from flask import Response, redirect
from flask_restful import Resource, reqparse
from service.db import db
import hashlib
import json

class Login(Resource):
    def get(self, user, passw):
        passw_hash = hashlib.md5(passw.encode()).hexdigest()
        passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
        db.execute(f"SELECT name FROM dle_users WHERE name='{user}' AND password='{passw_hash}'")
        result = db.fetchall()
        if result:
            # return Response().set_cookie('user_login', user)
            response = Response().set_cookie('user_login', user)
            # Перенаправляємо користувача на /login
            return redirect('/')
        else:
            return {'login': 'error'}
        # data = {
        #     "user": user,
        #     "passw": passw
        # }
        # return data
    
