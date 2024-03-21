#!/usr/bin/python3

from flask import Blueprint, render_template, session, redirect, url_for

import models
from models.staff import Staff
from web_flask.componet import staff_view
from web_flask.forms.staff import StaffForm


@staff_view.route('/user/profile')
def profile_info():
    form = StaffForm()
    own = None
    user = None
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))

    else:

        try:
            id = session['user_id']
            own = models.storage.get(Staff, id)
            own = own.to_dict()

            form.campus.data = own['campus']
            form.staffName.data = own['name']
            form.staffEmail.data = own['email']
            form.staffPhone.data = own['phone']
            user = session['user']

        except Exception as e:
            pass

        return render_template('profile.html',
                               own=own, form=form, user=user)
