from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password", message="Пароли должны совпадать")],
    )
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class NoteForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(min=2, max=120)])
    content = TextAreaField("Текст заметки", validators=[DataRequired(), Length(min=2, max=2000)])
    submit = SubmitField("Добавить заметку")


class UploadForm(FlaskForm):
    file = FileField("Файл", validators=[DataRequired(), FileAllowed(["png", "jpg", "jpeg", "pdf", "txt", "docx"])])
    submit = SubmitField("Загрузить файл")


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Описание')
    submit = SubmitField('Обновить профиль')