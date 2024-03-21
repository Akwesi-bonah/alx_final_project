#!/usr/bin/env python3
"""" send mail """
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import InputRequired


class MessageForm(FlaskForm):
    """ message form """
    level = SelectField('Level', choices=[
        ('All', 'All'),
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
        ('400', '400'),
        ('500', '500'),
        ('600', '600'),

    ], validators=[InputRequired()])

    to_pending_pay = SelectField('Send to Pending Payment Only', choices=[
        ('', 'Select Option'),
        ('1', 'Yes'),
        ('0', 'No'),
    ], validators=[InputRequired()])

    message = TextAreaField('Message', validators=[InputRequired()])

    submit = SubmitField('Submit')
