from flask_wtf import FlaskForm
from wtforms import StringField, URLField, IntegerField, PasswordField, EmailField, ValidationError
from wtforms.validators import DataRequired, URL, NumberRange, Email

# Code to write custom validator to check that field input meets database criteria

# My idea is to make sure the input will work before we have to query the database
# We will have to query anyway when we check if a username exists
# Easier to do what is in the videos


# def length_check(form, field, max):
#     if len(field.data) > 20:
#         raise ValidationError(f'{field} must be less than {max} characters')
    
# def length(min=1, max=-1):
#     message = f'Must be between %d and %d characters long.' % (min, max)

#     def _length(form, field):
#         l = field.data and len(field.data) or 0
#         if l < min or max != -1 and l > max:
#             raise ValidationError(message)

#     return _length

class NewUserForm(FlaskForm):
    '''Form class to register new users'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

class LoginForm(FlaskForm):
    '''Form class for users to login'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class FeedbackForm(FlaskForm):
    '''Form class for new feedback'''
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])