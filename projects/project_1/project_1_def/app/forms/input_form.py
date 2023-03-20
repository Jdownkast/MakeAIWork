from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

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
    genetic = StringField("Genetic age", validators=[InputRequired()])
    genetic_unit = StringField("in years")
    genetic_range = StringField(
        f"range: {valid_dict['genetic'][0]} - {valid_dict['genetic'][1]}"
    )

    length = StringField("Length", validators=[InputRequired()])
    length_unit = StringField("in centimeters")
    length_range = StringField(
        f"range: {valid_dict['length'][0]} - {valid_dict['length'][1]}"
    )

    weight = StringField("Weight", validators=[InputRequired()])
    weight_unit = StringField("in kilogramms")
    weight_range = StringField(
        f"range: {valid_dict['mass'][0]} - {valid_dict['mass'][1]}"
    )

    exercise = StringField("Exercise", validators=[InputRequired()])
    exercise_unit = StringField("in hours / day")
    exercise_range = StringField(
        f"range: {valid_dict['genetic'][0]} - {valid_dict['genetic'][1]}"
    )

    smoking = StringField("Smoking", validators=[InputRequired()])
    smoking_unit = StringField("in sigarettes / day")
    smoking_range = StringField(
        f"range: {valid_dict['smoking'][0]} - {valid_dict['smoking'][1]}"
    )

    alcohol = StringField(f"Alcohol intake", validators=[InputRequired()])
    alcohol_unit = StringField("in glasses / day")
    alcohol_range = StringField(
        f"range: {valid_dict['alcohol'][0]} - {valid_dict['alcohol'][1]}"
    )

    sugar = StringField(f"Sugar intake", validators=[InputRequired()])
    sugar_unit = StringField("in gramms / day")
    sugar_range = StringField(
        f"range: {valid_dict['sugar'][0]} - {valid_dict['sugar'][1]}"
    )

    # available = BooleanField("Available", default="checked")
