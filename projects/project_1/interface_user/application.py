from pickle import load
from flask import Flask, render_template, redirect, url_for, session
from forms.input_form import InputForm

# Load model via pickle.load
file_path = "../train_model/models/"
file_name = "model_3.pickle"
model = load(open(f"{file_path}{file_name}", "rb"))


def calc_expected(model, param):
    intercept = model.intercept_
    coef = list(model.coef_[0])

    effects = [coef * param for coef, param in zip(coef, param)]
    effect_sum = sum(effects)

    return float(intercept + effect_sum)


app = Flask(__name__)
app.config["SECRET_KEY"] = "very SECRET key"


@app.route("/", methods=["GET", "POST"])
def index():
    form = InputForm()
    expected = ""
    if form.validate_on_submit():
        session["param"] = {
            "1_genetics": form.genetic.data,
            "2_length": form.length.data,
            "3_mass": form.weight.data,
            "4_exercise": form.exercise.data,
            "5_smoking": form.smoking.data,
            "6_alcohol": form.alcohol.data,
            "7_sugar": form.sugar.data,
        }
        return redirect(url_for("model_3"))
    return render_template("application_html.html", form=form, expected=expected)


@app.route("/model_3", methods=["GET", "POST"])
def model_3():
    form = InputForm()
    parameters = [int(item) for item in list(session["param"].values())]

    bmi = parameters[2] / (parameters[1] / 100) ** 2
    bmi_low = 18.5
    bmi_high = 25

    bmi_norm_under = 0 if bmi > bmi_low else (bmi_low - bmi)
    bmi_norm_over = 0 if bmi < bmi_high else (bmi - bmi_high)
    parameters.append(bmi_norm_under)
    parameters.append(bmi_norm_over)

    expected_age = calc_expected(model, parameters)
    # expected = list(model.coef_[0])
    expected = f"The expected age is {int(expected_age)} years and {round((expected_age % 1) * 12)} months."
    if form.validate_on_submit():
        session["param"] = {
            "1_genetics": form.genetic.data,
            "2_length": form.length.data,
            "3_mass": form.weight.data,
            "4_exercise": form.exercise.data,
            "5_smoking": form.smoking.data,
            "6_alcohol": form.alcohol.data,
            "7_sugar": form.sugar.data,
        }
        return redirect(url_for("index"))
    return render_template("application_html.html", form=form, expected=expected)


if __name__ == "__main__":
    app.run()
