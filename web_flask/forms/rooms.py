#!/usr/bin/python3
""" This module defines the RoomType form """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

from models.block import Block
from models.room_type import RoomType
from models import storage


class RoomForm(FlaskForm):
    """This class defines the RoomType form"""
    room_name = StringField('Room Name', validators=[DataRequired(), Length(max=128)])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[
        ('', '<< Please Select >>'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    floor = SelectField('Floor', validators=[DataRequired()], coerce=str)
    no_of_beds = IntegerField('Number of Beds', validators=[DataRequired()])
    block = SelectField('Block', validators=[DataRequired()], coerce=str)
    room_type = SelectField('Room Type', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        # Set choices for Block field
        all_blocks = storage.all(Block).values()
        self.block.choices = [("", '<< Please Select >>')] + [(block.id, block.name)
                                                        for block in all_blocks]

        # Set choices for RoomType field
        all_room_types = storage.all(RoomType).values()
        self.room_type.choices = [("", '<< Please Select >>')] + [(room_type.id, room_type.name)
                                                            for room_type in all_room_types]

        # Set choices for Floor field
        self.floor.choices = [("", '<< Please Select >>')] + [(i, str(i) + "  floor") for i in range(1, 6)]

