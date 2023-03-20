from pickle import load
from flask import Flask, render_template, redirect, url_for, session, request
from forms.input_form import InputForm

# Load model via pickle.load
file_path = "../models/"
file_name = "model_0.pickle"
model = load(open(f"{file_path}{file_name}", "rb"))


def calc_expected(model, param):
    intercept = model.intercept_
    coef = list(model.coef_[0])

    effects = [coef * param for coef, param in zip(coef, param)]
    effects_sum = sum(effects)

    return float(intercept + effects_sum)


app = Flask(__name__)
app.config["SECRET_KEY"] = "very SECRET key"


@app.route("/", methods=["GET", "POST"])
def index():
    form = InputForm()
    expected = ""
    if form.validate_on_submit():
        # Calc bmi
        bmi_under = ""
        bmi_over = ""
        bmi_low = 18.5
        bmi_high = 25
        if len(form.length.data) > 0 and len(form.weight.data) > 0:
            bmi = int(form.weight.data) / ((int(form.length.data) / 100) ** 2)
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
        return redirect(url_for("model_0"))
    return render_template("application_html.html", form=form, expected=expected)


@app.route("/model_0", methods=["GET", "POST"])
def model_0():
    form = InputForm()
    parameters = [int(item) for item in list(session["param"].values())]

    expected_age = calc_expected(model, parameters)
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
        return redirect(url_for("index"))
    return render_template("application_html.html", form=form, expected=expected)


if __name__ == "__main__":
    app.run()
