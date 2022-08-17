import datetime
import http
import os
import shutil

from flask import jsonify, redirect, session, request
from flask_restful import Resource
from validate_email import validate_email
from models import database
from models.users_reg import Registration
from models.users_data import Data
from models.page_data import PageData
from create_secret_email import create_secret_email_or_number
from create_code import create_code
from replace import replacce
from phonenumbers import is_valid_number

from code_sender import send_mail, send_sms
from hashed_password import set_password
from exams.exam_password import exam_password


PATH_DIC = r'C:\Users\artur\PycharmProjects\Project\Проект\static\image'


class Registration_Api(Resource):
    def post(self):
        code = create_code()
        address = request.get_json()['address']
        if validate_email(address):
            db_sess = database.create_session()
            email_exist = db_sess.query(Registration.email).filter(Registration.email == address)
            send_mail(address, code, False)
        else:
            return 'Такой почты не существует'

        if is_valid_number(address):
            db_sess = database.create_session()
            number_exist = db_sess.query(Registration.email).filter(Registration.email == address)
            send_sms(address, f"Здравствуйте! Код подтверждения регистрации {address} - {code}.")
        else:
            return 'Такого номера не существует'

        if number_exist or email_exist:

            # conn = http.client.HTTPConnection("ifconfig.me")
            # conn.request("GET", "/ip")
            # session['logged'] = '0'
            # session['IP'] = str(conn.getresponse().read()).replace('b', '').replace("'", '').strip()
            # conn.close()

            user_reg = Registration(code_ver=code, address=address)
            db_sess.add(user_reg)
            db_sess.commit()
            id_ver = int(replacce(*db_sess.query(Registration.id).filter(Registration.email == address)))
            db_sess.close()
            return jsonify({'status': 'ok', 'id_ver': id_ver})
        else:
            return redirect('/')
        db_sess.close()


class Verirfication_Api(Resource):
    def post(self):
        code_verification = request.get_json()['code_verification']
        id_ver = request.get_json()['id_ver']
        db_sess = database.create_session()
        code_db = replacce(*db_sess.query(Registration.code_ver).filter(id == id_ver))
        if code_verification == int(code_db):
            return jsonify({'status': 'ok'})
        else:
            return 'Неверный код'


class Registartion_data_Api(Resource):
    def post(self):
        # conn = http.client.HTTPConnection("ifconfig.me")
        # conn.request("GET", "/ip")
        # if session['IP'] == str(conn.getresponse().read()).replace('b', '').replace("'", '').strip():
        password = request.get_json()['password']
        password_exam = request.get_json()['password_exam']
        name = request.get_json()['name']
        surname = request.get_json()['surname']
        id_ver = request.get_json()['id_ver']

        error = exam_password(password, password_exam)
        if type(error) == bool:
            hashed_password = set_password(password)
            created_data = datetime.datetime.now()
            db_sess = database.create_session()
            email = replacce(str(*db_sess.query(Registration.email).filter(Registration.id == id_ver)))
            user_data = Data(name=name, surname=surname, created_date=created_data, user_id=id_ver,
                             hashed_password=hashed_password)
            avatar = f'/static/image/{email}/avatar.jpeg'
            status = 'Я пользуюсь Boot'
            page_data = PageData(status=status, avatar=avatar, page_id=id_ver)
            direc = PATH_DIC + '/' + email
            os.mkdir(direc)
            shutil.copy('/static/image/avatar.jpeg', f'/static/image/{email}')
            db_sess.add(user_data)
            db_sess.add(page_data)
            db_sess.commit()
            db_sess.close()
            return jsonify({'status': 'ok'})
        else:
            return error


class Entrance_Api(Resource):
    def post(self):
        address = request.get_json()['address']
        password = request.get_json()['password']
        db_sess = database.create_session()
        id_db = db_sess.query(Registration.id).filter(Registration.address == address)
        if id_db:
            truthful_user = db_sess.query(Data.id).filter(Data.hashed_password == str(set_password(password)))
            if truthful_user:
                return jsonify({'status': 'ok'})
            else:
                return 'Неверный пароль'
        else:
            return 'Аккаунта с таким логином не существует'


class Recovery_Api(Resource):
    def post(self):
        code = create_code()
        address = request.get_json()['address']

        db_sess = database.create_session()
        if address == replacce(*db_sess.query(Registration.address).filter(Registration.address == address)):
            id_ver = int(replacce(*db_sess.query(Registration.id).filter(Registration.address == address)))
            send_mail(address, code, True)
            user_reg = db_sess.query(Registration).filter(Registration.id == id_ver).first()
            user_reg.code_ver = code
            db_sess.commit()
            db_sess.close()
            return jsonify({'status': 'ok'})
        else:
            return 'Аккаунта с таким логином не существует'


class Recovery_Data_Api(Resource):
    def post(self):
        id = request.get_json()['id']
        password = request.get_json()['password']
        password_exam = request.get_json()['password_exam']
        error = exam_password(password, password_exam)
        if type(error) == bool:
            db_sess = database.create_session()
            user_data = db_sess.query(Data).filter(Data.user_id == id).first()
            new_password = set_password(password)
            user_data.hashed_password = new_password
            db_sess.commit()
            db_sess.close()
            return jsonify({'status': 'ok'})
        else:
            return error


class Page_Api(Resource):
    def get(self):
        pass