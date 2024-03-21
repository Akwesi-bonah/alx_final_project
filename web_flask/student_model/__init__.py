#!/usr/bin/pyhthon3
from flask import Blueprint

student_views = Blueprint('student_views', __name__, template_folder='student_templates')
from web_flask.student_model.defualt import *