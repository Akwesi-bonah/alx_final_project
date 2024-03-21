#!/usr/bin/pyhthon3
""" view Blue Print for staff"""
from flask import Blueprint

staff_view = Blueprint('staff_view', __name__)

from web_flask.componet.staff import *
from web_flask.componet.rooms import *
from web_flask.componet.messaging import *
from web_flask.componet.profile import *
from web_flask.componet.reservation import *
from web_flask.componet.student import *
from web_flask.componet.management import *
