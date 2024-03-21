from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Regexp, Optional, Length, Email


class StaffForm(FlaskForm):
    """login for staff"""
    campus_choices = [
        ('', '<<Please select>>'),
        ('North Campus', 'North Campus'),
        ('Central Campus', 'Central Campus'),
        ('South Campus', 'South Campus')
    ]

    role_choices = [
        ('', '<<Please select>>'),
        ('JCR', 'JCR'),
        ('Porter', 'Porter'),
        ('Facility Manager', 'Facility Manager'),
        ('Administrator', 'Administrator'),
        ('Account Officer', 'Account Officer')
    ]

    status_choices = [
        ('', '<<Please select>>'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]

    campus = SelectField('Campus', choices=campus_choices, validators=[DataRequired()])
    staffName = StringField('Name', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z\- ]+$', message="Only alphabets, hyphens, and spaces are allowed")
    ])
    staffEmail = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    staffPhone = StringField('Phone', validators=[DataRequired(), Regexp(r'^[0-9()-]+$', message="Invalid phone number"),
                                                  Length(max=13, min=10)])
    userPwd = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    role = SelectField('Role', choices=role_choices, validators=[DataRequired()])
    status = SelectField('Status', choices=status_choices, validators=[Optional()])

    submit = SubmitField('Submit')
