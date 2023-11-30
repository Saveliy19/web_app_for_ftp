from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    hostname = StringField('Адрес сервера', validators=[DataRequired()])
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class MakeDirectory(FlaskForm):
    catalog_name = StringField('Имя каталога', validators=[DataRequired()])
    submit = SubmitField('Создать')

class UploadForm(FlaskForm):
    file = FileField('Выбрать файл', validators=[DataRequired()])
    submit = SubmitField('Загрузить')