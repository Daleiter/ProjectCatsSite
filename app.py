from flask import Flask, request, render_template, make_response,send_file,redirect, url_for
from service.dbSite import execute_query as execute_querySite
from service.dbRage import execute_query as execute_queryRage
from service.dbMine import execute_query as execute_queryMine
from service.syncmoney import AddMoney
import hashlib
import uuid
import os
import json
import bcrypt
from flask_restful import Api
# from service.login import Login
# from your_login_module import Login
# from service.register import Register
from service.skins import Skins
from service.cloaks import Cloaks

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    changelog = execute_querySite('SELECT * FROM ChangeLog ORDER BY version DESC')
    user_cookie = request.cookies.get('user', 'Not set')
    if user_cookie:
        money = execute_querySite(f"SELECT money  FROM data WHERE name = '{user_cookie}'")
    else:
        money = None
    return render_template('index.html', changelog=changelog, money=money)


@app.route('/setskin', methods=['POST'])
def setskin():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    if file.filename.split('.')[1] != 'png':
        return 'No png file'
    user_cookie = request.cookies.get('user', 'Not set')
    # Тут ви можете визначити шлях для збереження файлу на сервері
    # Наприклад, якщо ви хочете зберегти його в папці "uploads" на рівні проекту:
    file.save(os.path.join('pack_skins', f'{user_cookie}.png'))

    return redirect(url_for('home'))
@app.route('/setcloaks', methods=['POST'])
def setcloaks():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    if file.filename.split('.')[1] != 'png':
        return 'No png file'
    user_cookie = request.cookies.get('user', 'Not set')
    # Тут ви можете визначити шлях для збереження файлу на сервері
    # Наприклад, якщо ви хочете зберегти його в папці "uploads" на рівні проекту:
    file.save(os.path.join('pack_cloaks', f'{user_cookie}.png'))

    return redirect(url_for('home'))

@app.route('/logining', methods=['POST'])
def logining():
    data = request.form.to_dict()
    passw_hash = hashlib.md5(data['passw'].encode()).hexdigest()
    passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
    print(passw_hash)
    query = f"SELECT name FROM data WHERE name='{data['user']}' AND password='{passw_hash}'"
    result = execute_querySite(query)
    if result:
        print(result)
        response = make_response(home())
        response.set_cookie('user', data['user'])
        response.set_cookie('badlogin', '', expires=0)
        return response
        # user_cookie = request.cookies.get('usera')
        # print(user_cookie)
    else:
        response = make_response(home())
        response.set_cookie('badlogin', "True")
        return response
    return "good"

@app.route('/registering', methods=['POST'])
def registering():
    data = request.form.to_dict()
    passw_hash = hashlib.md5(data['passw'].encode()).hexdigest()
    passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
    try:
        print(data)
        print('pass',data['passw'],'copy', data['passw_copy'])
        if data['passw'] == data['passw_copy']:
            query = f"SELECT name FROM data WHERE name='{data['user']}'"
            result = execute_querySite(query)
            if result:
                print(result)
                return 'name'
            query = f"SELECT name FROM data WHERE email='{data['email']}'"
            result = execute_querySite(query)
            if result:
                print(result)
                return 'email'
            passw_hash = hashlib.md5(data['passw'].encode()).hexdigest()
            passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
            execute_querySite(f"INSERT INTO data (name, password, email, money) VALUES ('{data['user']}', '{passw_hash}', '{data['email']}', '50000');")
            #Mine
            execute_queryMine(f"INSERT INTO dle_users (name, password, email) VALUES ('{data['user']}', '{passw_hash}', '{data['email']}');")
            execute_queryMine(f"INSERT INTO uuid_user (uuid, username) VALUES ('{str(uuid.uuid4())}', '{data['user']}');")
            #Rage
            promocod = ["noref"]
            promocod_json = json.dumps(promocod)
            rage_pass_hash = bcrypt.hashpw(data['passw'].encode(), bcrypt.gensalt(11)).decode('utf-8')
            execute_queryRage(f"INSERT INTO accounts (socialclub, login, hwid, redbucks, ip, character1, character2, character3, email, password, viplvl, vipdate, promocodes, present) VALUES ('Site','{data['user']}','Site','0','192.168.1.1','-1','-1','-2', '{data['email']}','{rage_pass_hash}', '0', '2024-02-01 21:35:03', '{promocod_json}', '0');")
            
            return 'user'
        else:
            return 'password'
    except:
        return 'eror'
@app.route('/addmoney', methods=['POST'])
def addmoneys():
    # data = request.form.to_dict()
    # print(data['user'])
    user_cookie = request.cookies.get('user', 'Not set')
    print(user_cookie)
    AddMoney.get(user_cookie)
    return '200'
@app.route('/changepassword', methods=['POST'])
def changepassword():
    data = request.form.to_dict()
    passw_hash = hashlib.md5(data['passw'].encode()).hexdigest()
    passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
    user_cookie = request.cookies.get('user', 'Not set')
    execute_querySite(f"UPDATE data SET password = '{passw_hash}' WHERE name = '{user_cookie}';")
    #Mine
    execute_queryMine(f"UPDATE dle_users SET password = '{passw_hash}' WHERE name = '{user_cookie}';")
    #Rage
    promocod = ["noref"]
    promocod_json = json.dumps(promocod)
    rage_pass_hash = bcrypt.hashpw(data['passw'].encode(), bcrypt.gensalt(11)).decode('utf-8')
    execute_queryRage(f"UPDATE accounts SET password = '{rage_pass_hash}' WHERE login = '{user_cookie}';")
            
    print(data['passw'], user_cookie)
    
    return 'good'

@app.route('/download_launcher')
def download_launcher():
    launcher_path = '../../sashok/Launcher.jar'
    return send_file(launcher_path, as_attachment=True)

@app.route('/download_java')
def download_java():
    launcher_path = 'java-8u311.exe'
    return send_file(launcher_path, as_attachment=True)

@app.route('/download_rage')
def download_rage():
    launcher_path = 'RAGEMultiplayer_Setup.exe'
    return send_file(launcher_path, as_attachment=True)

@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('index.html'))
    response.set_cookie('user', '', expires=0)
    return response

@app.route('/get_cookie')
def get_cookie():
    user_cookie = request.cookies.get('user', 'Not set')
    print(f'Value of "user" cookie: {user_cookie}')
    return render_template('index.html')

# api.add_resource(Login, '/login')
# api.add_resource(Login, '/api/login/<string:user>&<string:passw>')
# api.add_resource(Register, '/api/register/<string:user>&<string:passw>&<string:passw_copy>&<string:email>')
# api.add_resource(AddMoney, '/api/syncmoney/<string:user>')
api.add_resource(Skins, '/api/MinecraftSkins/<string:user>')
api.add_resource(Cloaks, '/api/MinecraftCloaks/<string:user>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')
