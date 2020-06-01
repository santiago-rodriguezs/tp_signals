from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sineSweep as ss

import forms

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    audioForm = forms.AudioForm(request.form)
    flag = False
#    and audioForm.validate()
    if request.method == "POST":
        t = audioForm.time.data
        freq1 = audioForm.freq1.data
        freq2 = audioForm.freq2.data
        ss.sineSweep(t, freq1, freq2)
        flag = True
        redirect(url_for('.processing'))

    return render_template("index.html", flag = flag, form = audioForm)


@app.route("/processing", methods = ["GET", "POST"])
def processing():
	audioForm = forms.AudioForm(request.form)
	if request.method == "POST" and audioForm.validate():
		var = audioForm.time.data

	return render_template("processing.html", form = audioForm)

@app.route("/upload", methods = ["GET", "POST"])
def upload():
	audioForm = forms.AudioForm(request.form)
	if request.method == "POST" and audioForm.validate():
		var = audioForm.time.data

	return render_template("upload.html", form = audioForm)

@app.route("/results", methods = ["GET", "POST"])
def results():
	return render_template("results.html")

@app.route("/syntetize", methods = ["GET", "POST"])
def syntetize():
	audioForm = forms.AudioForm(request.form)
	if request.method == "POST" and audioForm.validate():
		var = audioForm.time.data

	return render_template("syntetize.html", form = audioForm)

@app.route("/calibrate", methods = ["GET","POST"])
def calibrate():
	audioForm = forms.AudioForm(request.form)
	if request.method == "POST" and audioForm.validate():
		var = audioForm.time.data

	return render_template("calibrate.html", form = audioForm)

@app.route("/about", methods = ["GET"])
def about():
	return render_template("about.html")

if __name__ == "__main__":
        app.run(debug = True, port = 9010)
