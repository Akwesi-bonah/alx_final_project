from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


class AddBlock(FlaskForm):
    """Block form"""
    status_choices = [
        ('', '<<Please select>>'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]
    campus_choices = [
        ('', '<<Please select>>'),
        ('North Campus', 'North Campus'),
        ('Central Campus', 'Central Campus'),
        ('South Campus', 'South Campus')
    ]

    campus = SelectField('Campus', choices=campus_choices, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=255)])
    status = SelectField('Status', choices=status_choices, validators=[Optional()])

    submit = SubmitField('Submit')
