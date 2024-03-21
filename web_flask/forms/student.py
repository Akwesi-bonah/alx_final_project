from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Regexp


class StudentForm(FlaskForm):
    level_choices = [
        ('', '<<Please select>>'),
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
        ('400', '400')
    ]

    gender_choices = [
        ('', '<<Please select>>'),
        ('male', 'Male'),
        ('female', 'Female')
    ]

    disability_choices = [
        ('', '<<Please select>>'),
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    max_file_size = 10 * 1024 * 1024

    def validate_profile_picture(self, profile_picture):
        if profile_picture.data:
            file_size = len(request.files['profile_picture'].read())
            if file_size > self.max_file_size:
                raise ValidationError('File size exceeds the limit (10MB)!')

    first_name = StringField('First Name', validators=[DataRequired(), Length(max=128)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=128)])
    other_name = StringField('Other Name', validators=[Length(max=128)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^[0-9()-]+$', message="Invalid phone number"),
                                                  Length(max=13, min=10)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=gender_choices, validators=[DataRequired()])
    student_number = StringField('Student Number', validators=[DataRequired(), Length(max=128)])
    program = StringField('Program', validators=[Length(max=128)])
    level = SelectField('Level', choices=level_choices, validators=[DataRequired()])
    guardian_name = StringField('Guardian Name', validators=[Length(max=128)])
    guardian_phone = StringField('Guardian Phone', validators=[Length(max=128)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    disability = SelectField('Disability', choices=disability_choices)
    address = TextAreaField('Address', validators=[Length(max=128)])
    profile_picture = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(allowed_extensions, 'Only images allowed!')])
    submit = SubmitField('Submit')
