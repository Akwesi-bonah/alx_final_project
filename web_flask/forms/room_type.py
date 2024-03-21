from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Optional, Length


class AddRoomType(FlaskForm):
    """Block form"""
    status_choices = [
        ('', '<<Please select>>'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]

    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=255)])
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    status = SelectField('Status', choices=status_choices, validators=[Optional()])

    submit = SubmitField('Submit')
