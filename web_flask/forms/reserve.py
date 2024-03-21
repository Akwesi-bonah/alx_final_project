from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from models.block import Block
from models.room_type import RoomType
from models import storage


class ReservationForm(FlaskForm):
    """Reservation form class"""
    block = SelectField('Block', validators=[DataRequired()], coerce=str)
    room_type = SelectField('Room Type', validators=[DataRequired()], coerce=str)
    room_name = SelectField('Room Name', validators=[DataRequired()], coerce=str)
    no_of_beds = IntegerField('Number of Beds', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        # Set choices for Block field
        all_blocks = storage.all(Block).values()
        self.block.choices = [("", '<< Please Select >>')] + [(block.id, block.name)
                                                        for block in all_blocks]

        # Set choices for RoomType field
        all_room_types = storage.all(RoomType).values()
        self.room_type.choices = [("", '<< Please Select >>')] + [(room_type.id, room_type.name)
                                                            for room_type in all_room_types]

        self.room_name.choices = [("", '<< Please Select >>')]
