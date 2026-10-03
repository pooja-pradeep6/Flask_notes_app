from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Note', validators=[DataRequired()])
    category = StringField('Category', validators=[Optional(), Length(max=80)])
    pinned = BooleanField('Pin this note')
    submit = SubmitField('Save')
