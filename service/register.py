# Файл 2: service/login.py
from flask_restful import Resource, reqparse
from service.db import db, connection
import hashlib
import uuid

class Register(Resource):
    def get(self, user, passw, passw_copy, email):
        try:
            if passw == passw_copy:
                db.execute(f"SELECT name FROM dle_users WHERE name='{user}'")
                result = db.fetchall()
                if result:
                    print(result)
                    return 'name'
                db.execute(f"SELECT name FROM dle_users WHERE email='{email}'")
                result = db.fetchall()
                if result:
                    print(result)
                    return 'email'
                passw_hash = hashlib.md5(passw.encode()).hexdigest()
                passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
                db.execute(f"INSERT INTO dle_users (name, password, email) VALUES ('{user}', '{passw_hash}', '{email}');")
                db.execute(f"INSERT INTO uuid_user (uuid, username) VALUES ('{str(uuid.uuid4())}', '{user}');")
                connection.commit()
                return user
            else:
                return 'password'
        except:
            return 'eror'
        # except Exception as e:
        #     return e