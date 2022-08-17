from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, StringField, PasswordField


class RegistrationForm(FlaskForm):
    address = EmailField('Введите вашу почту или номер')
    submit = SubmitField('Отправить код')
    entrance = SubmitField('Уже зарегистрированы?')


class VerificationForm(FlaskForm):
    code = StringField('Письмо отправлено')
    submit = SubmitField('Отправить код')


class DataForm(FlaskForm):
    name = StringField('Имя:')
    surname = StringField('Фамилия:')
    password = PasswordField('Введите пароль:')
    password_exam = PasswordField('Подтвердите пароль:')
    submit = SubmitField('Готово')


class RecoveryForm(FlaskForm):
    address = EmailField('Введите почту или номер, на который зарегистрирован аккаунт:')
    submit = SubmitField('Отправить код')


class RecoveryDataForm(FlaskForm):
    password = PasswordField('Пароль')
    password_exam = PasswordField('Поторите пароль')
    submit = SubmitField('Сохранить пароль')


class EntranceForm(FlaskForm):
    email = EmailField('Почта:')
    password = PasswordField('Пароль:')
    recovery_submit = SubmitField('Забыли пароль?')
    submit = SubmitField('Войти')
    registration_submit = SubmitField('Регистрация')


class PageForm(FlaskForm):
    pass


class SearchForm(FlaskForm):
    pass


class PeopleForm(FlaskForm):
    pass
