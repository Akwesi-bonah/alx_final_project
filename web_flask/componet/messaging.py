#!/usr/bin/python3
""" mail setup """
from flask_mail import Message

from flask import render_template, request, session, redirect, url_for

from web_flask.componet import staff_view
from web_flask.componet.mail import mail
from web_flask.forms.message import MessageForm


@staff_view.route('/mail', methods=['GET'], strict_slashes=False)
def messaging():
    """ send mail """
    form = MessageForm()
    user = None
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

    return render_template('message.html',
                           form=form, user=user)
