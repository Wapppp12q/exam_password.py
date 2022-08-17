import requests
from flask import Flask, render_template, redirect, request
from flask_restful import Api
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import database

from code_sender import send_mail

from photo_editing import editing_photo

from backend import Registration_Api, Verirfication_Api, Registartion_data_Api, Entrance_Api, Recovery_Api, Recovery_Data_Api, Page_Api

from forms import RegistrationForm, VerificationForm, DataForm, EntranceForm, RecoveryForm, RecoveryDataForm, PageForm, SearchForm, PeopleForm

load_dotenv()

UPLOAD_FOLDER = 'C:\\Users\\artur\\PycharmProjects\\Project\\Проект\\static\\image'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
DATABASE_NAME = 'db/users.sqlite'

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'fdgjj54569*FJ$84jgf@#_fdsgf8958ea52588d4b518^%jh546c20f38c5e50cbd3ca067fe9d08dc259167c63a33bb267435hj89wq8*SRF89dsgkjs8g7*(&*(&%giodsg5ten0&r(9Br37h8'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api()
api.add_resource(Registration_Api, '/api/registration/')
api.add_resource(Verirfication_Api, '/api/verification/')
api.add_resource(Registartion_data_Api, '/api/registration_data/')
api.add_resource(Entrance_Api, '/api/entrance/')
api.add_resource(Recovery_Api, '/api/recovery/')
api.add_resource(Recovery_Data_Api, '/api/recovery_data/')
api.add_resource(Page_Api, '/api/page/')
api.init_app(app)


# def entr_ex(email, password):
#     exam_email = False
#     db_sess = database.create_session()
#     for em in db_sess.query(Reg.email).all():
#         em = replacce(str(*em))
#         if str(email) == em:
#             exam_email = True
#             break
#
#     if exam_email:
#         pas = replacce(str(*db_sess.query(Data.hashed_password).filter(Reg.email == email)))
#         db_sess.close()
#         return check_password(pas, password)
#     else:
#         db_sess.close()
#         return False
#
#
# def allowed_file(filename):
#     if '.' in filename:
#         fname = filename.rsplit('.', 1)[1].lower()
#         if fname in ALLOWED_EXTENSIONS:
#             return True
#
#     return False
#
#
# @app.route('/upload/<id_ver>', methods=['GET', 'POST'])
# def upload_file(id_ver):
#     error = ''
#     path_im = ''
#     id_ver = int(id_ver)
#     db_sess = database.create_session()
#     email = replacce(str(*db_sess.query(Reg.email).filter(Reg.id == id_ver)))
#     page_data = db_sess.query(PData).filter(PData.page_id == id_ver).first()
#
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             error = "Нет файловой части"
#         else:
#             file = request.files['file']
#         if file.filename == '':
#             error = "Файл не выбран"
#
#         if file and allowed_file(file.filename):
#             for photo in os.walk(f'static/image/{email}'):
#                 for elem in photo[2]:
#                     if elem.split('.')[0] == 'avatar':
#                         os.remove(f'static/image/{email}/{elem}')
#                         break
#                 break
#             file.filename = 'avatar.' + file.filename.split('.')[-1]
#             filename = secure_filename(file.filename)
#             path_im = '/static/image/' + email + '/' + filename
#             page_data.avatar = path_im
#             db_sess.commit()
#             db_sess.close()
#
#             file.save(os.path.join(UPLOAD_FOLDER + '/' + email, filename))
#             file = editing_photo(path_im.lstrip('/'))
#             file.save(os.path.join(UPLOAD_FOLDER + '/' + email, filename))
#
#             return redirect(f'/page/{id_ver}')
#
#         else:
#             db_sess.close()
#             error = 'Неверный формат фотографии'
#
#     return render_template('upload.html', title='Загрузка фото', error=error, src=path_im)


# Пароль, чтобы не придумывать YUGDsdf12#%fdg
@app.route('/')
def registration():
    response = ''
    form = RegistrationForm()

    if form.entrance.data:
        return redirect('/entrance')

    if form.validate_on_submit():
        registration_json = {'address': form.address.data}
        response = requests.post(f'http://127.0.0.1:8000/api/registration/', json=registration_json)
        if response['status'] == 'ok':
            return redirect(f'/verification?id={response["id_ver"]}&recovery=False')
    elif form.submit.data:
        response = 'Введите данные'

    return render_template('registration.html', title='Регистрация', form=form, response=response)


@app.route('/verification/')
def verification():
    id_ver = request.args.get('id_ver')
    recovery = request.args.get('recovery')
    response = ''
    form = VerificationForm()

    if form.validate_on_submit():
        verification_json = {'code_verification': form.code.data, 'id_ver': id_ver}
        response = requests.post(f'http://127.0.0.1:8000/api/verification/', json=verification_json)
        if response['status'] == 'ok':
            if recovery:
                return redirect(f'/registration_data?id_ver={id_ver}')
            else:
                return redirect(f'/recovery_data?id_ver={id_ver}')
    elif form.submit.data:
        response = 'Введите код'

    return render_template('verification.html', title='Подтверждение почты', form=form, response=response)


@app.route('/registration_data/', methods=['GET', 'POST'])
def registration_data():
    response = ''
    id_ver = request.args.get('id_ver')
    form = DataForm()

    if form.validate_on_submit():
        registration_data_json = {'password': form.password.data, 'password_exam': form.password_exam.data, 'name': form.name.data, 'surname': form.surname.data, 'id_ver': id_ver}
        response = requests.post('http://127.0.0.1:8000/api/registration_data/', json=registration_data_json)
        if response['status'] == 'ok':
            return redirect(f'/page/')
    elif form.submit.data:
        response = 'Введите данные'

    return render_template('registration_data.html', title='Регистраци данных', form=form, response=response)


@app.route('/entrance', methods=['GET', 'POST'])
def entrance():
    response = ''
    form = EntranceForm()

    if form.registration_submit.data:
        return redirect('/registration/')

    if form.recovery_submit.data:
        return redirect('/recovery/')

    if form.validate_on_submit():
        entrance_json = {'address': form.address.data.strip(), 'password': form.password.data.strip()}
        response = requests.post('http://127.0.0.1:8000/api/entrance/', json=entrance_json)
        if response.json()['status'] == 'ok':
            return redirect('/page/')

    elif form.submit.data:
        response = 'Введите данные'

    return render_template('entrance.html', title='Вход', form=form, response=response)


@app.route('/recovery/', methods=['GET', 'POST'])
def recovery():
    response = ''
    form = RecoveryForm()

    if form.validate_on_submit():
        recovery_json = {'address': form.address.data}
        response = requests.post(f'http://127.0.0.1:8000/api/recovery/', json=recovery_json)
        if response['status'] == 'ok':
            return redirect(f'/verification?id={response["id_ver"]}&recovery=True')
    elif form.submit.data:
        response = 'Введите данные'

    return render_template('recovery.html', form=form, title='Восстановление пароля', response=response)


@app.route('/recovery_data/', methods=['GET', 'POST'])
def recovery_data():
    form = RecoveryDataForm()
    response = ''
    id = request.args.get('id_ver')

    if form.validate_on_submit():
        recovery_data_json = {'password': form.password.data, 'password_exam': form.password_exam.data, 'id': id}
        response = requests.post('http://127.0.0.1:8000/api/recovery_data/', json=recovery_data_json)
        if response['status'] == 'ok':
            return redirect('/page/')
    elif form.submit.data:
        response = 'Введите пароли'

    return render_template('recovery_data.html', form=form, title='Новый пароль', response=response)


@app.route("/page/", methods=['POST', 'GET'])
def page():
    id_ver = int(id_ver)
    form = PageForm()
    db_sess = database.create_session()
    src_res = str(*db_sess.query(PData.avatar).filter(PData.page_id == id_ver))
    src = replacce(src_res)
    name = str(*db_sess.query(Data.name).filter(Data.user_id == id_ver))
    surname = str(*db_sess.query(Data.surname).filter(Data.user_id == id_ver))
    name = replacce(name)
    surname = replacce(surname)


    if form.submit.data:
        return redirect(f'/upload/{id_ver}')

    return render_template('page.html', title='Boot', form=form, src=src, name=name, surname=surname)


# @app.route('/search_people', methods=['GET', 'POST'])
# def search_people():
#     form = SearchForm()
#
#
# @app.route('/people_page', methods=['GET', 'POST'])
# def people_page():
#     form = PeopleForm()


if __name__ == '__main__':
    database.global_init(DATABASE_NAME)
    app.run(host="127.0.0.1", port='8000', debug=True)
