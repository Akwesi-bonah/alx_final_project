#!/usr/bin/python3
""" staff management"""

from web_flask.componet import staff_view
from flask import render_template, redirect, url_for, session
from models.staff import Staff
from web_flask.forms.staff import StaffForm
from models import storage


@staff_view.route('/staff', methods=['GET'], strict_slashes=False)
def users():
    """ staff management"""
    role = ""
    form = StaffForm()
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']
        user_id = session['user_id']
        roles = storage.session.query(
            Staff.role).filter_by(id=user_id).first()
        role = roles[0] if roles else None

        all_staff = storage.all(Staff).values()
        staff = [staff.to_dict() for staff in all_staff]
    return render_template('manageStaff.html',
                           users=staff, form=form,
                           user=user, role=role)


