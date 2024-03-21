#!/usr/bin/python3

from flask import render_template, request, session, redirect, url_for

from models.student import Student
from web_flask.componet import staff_view
from models import storage
from web_flask.forms.student import StudentForm


@staff_view.route('/addStudent', methods=['GET'])
def add_students():
    """ Add new student """
    form = StudentForm()
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

    return render_template('addUpdateStudent.html',
                           form=form, user=user)


@staff_view.route('/studentsList')
def student_list():
    """ student list"""
    students = []
    form = StudentForm()

    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

    all_students = storage.all(Student).values()
    students = [student.to_dict() for student in all_students]

    return render_template('StudentList.html',
                           Students=students,
                           form=form, user=user)
