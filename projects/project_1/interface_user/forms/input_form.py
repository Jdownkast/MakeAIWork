from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, RadioField
from wtforms.validators import InputRequired, NumberRange

error_no_input = 'Please enter valid input, or check the "No data" checkbox'
valid_dict = {
    "genetic": (40, 120),
    "length": (147, 220),
    "mass": (30, 200),
    "exercise": (0, 8),
    "smoking": (0, 60),
    "alcohol": (0, 12),
    "sugar": (0, 50),
    "lifespan": (40, 120),
}


class InputForm(FlaskForm):
    genetics = StringField(
        f"Genetic age (in years; range: {valid_dict['genetic'][0]}-{valid_dict['genetic'][1]})",
        validators=[InputRequired()],
    )
    length = StringField(
        f"Length (in cm; range: {valid_dict['length'][0]}-{valid_dict['length'][1]})",
        validators=[InputRequired()],
    )
    weight = StringField(
        f"Weight (in kg; range: {valid_dict['mass'][0]}-{valid_dict['mass'][1]})",
        validators=[InputRequired()],
    )
    exercise = StringField(
        f"Exercise (in hours / day; range: {valid_dict['exercise'][0]}-{valid_dict['exercise'][1]})",
        validators=[InputRequired()],
    )
    smoking = StringField(
        f"Smoking (in sigarettes / day; range: {valid_dict['smoking'][0]}-{valid_dict['smoking'][1]})",
        validators=[InputRequired()],
    )
    alcohol = StringField(
        f"Alcohol intake (in glasses / day; range: {valid_dict['alcohol'][0]}-{valid_dict['alcohol'][1]})",
        validators=[InputRequired()],
    )
    sugar = StringField(
        f"Sugar intake (in g / day; range: {valid_dict['sugar'][0]}-{valid_dict['sugar'][1]})",
        validators=[InputRequired()],
    )

    # available = BooleanField("Available", default="checked")
