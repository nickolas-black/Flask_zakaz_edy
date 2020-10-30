from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Regexp


class LoginForm(FlaskForm):
    email = StringField('E-mail', [InputRequired(message="Заполните поле"),
                                   Regexp('^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$',
                                          message="Введите корректный e-mail")])
    password = PasswordField('Пароль', [InputRequired(message="Заполните поле")])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('E-mail', [InputRequired(message="Заполните поле"),
                                   Regexp('^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$',
                                          message="Введите корректный e-mail")])
    password = PasswordField('Пароль', [InputRequired(message="Заполните поле"), Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}', message="Пароль должен быть не менее 5 символов, содержать цифры, символы нижнего и верхнего регистров")])
    submit = SubmitField('Зарегистрироваться')


class OrderForm(FlaskForm):
    name = StringField('Имя', [InputRequired(message="Заполните поле"), Regexp('^([А-Я]{1}[а-яё]{1,23}$)',
                                                                               message='Введите настоящее имя')])
    address = StringField('Адрес', [InputRequired(message="Заполните поле")])
    phone = StringField('Номер телефона', [InputRequired(message="Заполните поле"), Regexp('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', message='Введите корректный номер телефона')])
    submit = SubmitField('Оформить заказ')
