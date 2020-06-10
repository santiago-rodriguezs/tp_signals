from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from calibrate import sineSweep, pinkNoise, playRec
from process import iRObtention, filtr, logNorm, smoothing, schroeder

import forms

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    audioForm = forms.AudioForm(request.form)
    flag = False
    if request.method == "POST":
        t = audioForm.time.data
        freq1 = audioForm.freq1.data
        freq2 = audioForm.freq2.data
        #sineSweep(t, freq1, freq2)
        playRec(sineSweep(t, freq1, freq2))
        flag = True

    return render_template("index.html", flag = flag, form = audioForm)


@app.route("/processing", methods = ["GET", "POST"])
def processing():
    processingForm = forms.ProcessingForm(request.form)
    if request.method == "POST":
        bandwidth = processingForm.bandwidth.data
        if bandwidth == "octave":
            pass
        elif bandwidth == "third":
            pass

    return render_template("processing.html", form = processingForm)

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
    flag = False
    if request.method == "POST":
        t = audioForm.time.data
        pinkNoise(t)
        flag = True
        
    return render_template("calibrate.html", flag = flag, form = audioForm)

@app.route("/about", methods = ["GET"])
def about():
	return render_template("about.html")

if __name__ == "__main__":
        app.run(debug = True, port = 9011)
