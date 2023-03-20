from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("app.html")

@app.route("/handle", methods=['POST'])
def handle_data():
    return render_template("app.html")