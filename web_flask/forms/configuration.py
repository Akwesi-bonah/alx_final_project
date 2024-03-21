#!/usr/bin/python3
""" Define Configuration Form """
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.fields.choices import SelectField
from wtforms.validators import InputRequired


class ConfigForm(FlaskForm):
    """ Represent Configuration Form """
    start_date = DateField('Start Date', validators=[InputRequired()])
    end_date = DateField('End Date', validators=[InputRequired()])
    submit = SubmitField('Save Configuration')
