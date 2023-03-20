from pickle import load
from flask import Flask, render_template, redirect, url_for, session
from forms.input_form import InputForm, CheckForm
from os import listdir
from os.path import isfile, join
from functions.try_model import try_model

# Load models via pickle.load
file_path = "../train_model/models/"
extension = ".pickle"
modelfiles = [
    f for f in listdir(file_path) if isfile(join(file_path, f)) and extension in f
]

all_models = []
for model in modelfiles:
    # Get model names without extention (can also with os.path.splittext but no priority)
    model_name = model[: -len(extension)]
    file = f"{file_path}{model}"
    all_models.append(load(open(f"{file}", "rb")))


def relevant_param(param):
    parameters = [int(item) for item in list(param.values())]
    rel_param = [parameter for parameter in parameters if len(parameter) > 0]
    return rel_param


def calc_expected(model, param):
    """Use model to calculate expected age"""
    intercept = model.intercept_
    coef = list(model.coef_[0])

    effects = [coef * param for coef, param in zip(coef, param)]
    effect_sum = sum(effects)

    return float(intercept + effect_sum)


app = Flask(__name__)
app.config["SECRET_KEY"] = "very SECRET key"


@app.route("/", methods=["GET", "POST"])
def index():
    model = all_models[0]
    form = InputForm()
    check = CheckForm()
    expected = ""
    if form.validate_on_submit():
        # Calc bmi
        bmi_under = ""
        bmi_over = ""
        bmi_low = 18.5
        bmi_high = 25
        if len(form.length.data) > 0 and len(form.weight.data) > 0:
            bmi = form.weight.data / ((form.length.data / 100) ** 2)
            bmi_under = 0 if bmi > bmi_low else (bmi_low - bmi)
            bmi_over = 0 if bmi < bmi_high else (bmi - bmi_high)

        # Save cookies
        session["param"] = {
            "0_genetics": form.genetic.data,
            "1_length": form.length.data,
            "2_mass": form.weight.data,
            "3_exercise": form.exercise.data,
            "4_smoking": form.smoking.data,
            "5_alcohol": form.alcohol.data,
            "6_sugar": form.sugar.data,
            "7_bmi_under": bmi_under,
            "8_bmi_over": bmi_over,
        }

        # Check cookies for fitting model
        model_fit, model = try_model(all_models, session["param"])
        if model_fit:
            return redirect(url_for("expected", model=model))
        else:
            expected = "The chosen parameters cannot fit in a model. Please chose different parameters."
    return render_template(
        "application_html.html", form=form, model=model, expected=expected
    )


@app.route("/<model>", methods=["GET", "POST"])
def expected(model):
    form = InputForm()
    expected_age = calc_expected(model, relevant_param(model, session["param"]))
    expected = f"The expected age is {int(expected_age)} years and {round((expected_age % 1) * 12)} months."
    if form.validate_on_submit():
        # Calc bmi
        bmi_under = ""
        bmi_over = ""
        bmi_low = 18.5
        bmi_high = 25
        if len(form.length.data) > 0 and len(form.weight.data) > 0:
            bmi = form.weight.data / ((form.length.data / 100) ** 2)
            bmi_under = 0 if bmi > bmi_low else (bmi_low - bmi)
            bmi_over = 0 if bmi < bmi_high else (bmi - bmi_high)

        # Save cookies
        session["param"] = {
            "0_genetics": form.genetic.data,
            "1_length": form.length.data,
            "2_mass": form.weight.data,
            "3_exercise": form.exercise.data,
            "4_smoking": form.smoking.data,
            "5_alcohol": form.alcohol.data,
            "6_sugar": form.sugar.data,
            "7_bmi_under": bmi_under,
            "8_bmi_over": bmi_over,
        }

        # Check cookies for fitting model
        model_fit, model = try_model(all_models, session["param"])
        if model_fit:
            return redirect(url_for("expected", model=model))
        else:
            expected = "The chosen parameters cannot fit in a model. Please chose different parameters."
        return redirect(url_for("index"))
    return render_template("application_html.html", form=form, expected=expected)


if __name__ == "__main__":
    app.run()
