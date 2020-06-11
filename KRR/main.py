import soundfile as sf
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os

from calibrate import sineSweep, pinkNoise, playRec
from process import iRObtention, filtr, logNorm, smoothing, schroeder
from process import edt, t60, d50, c80
from process import iRSynth
import forms

UPLOAD_FOLDER = "./static/audio"
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods = ["GET", "POST"])
def index():
    audioForm = forms.AudioForm(request.form)
    flag = False
    if request.method == "POST":
        t = audioForm.time.data
        freq1 = audioForm.freq1.data
        freq2 = audioForm.freq2.data
        sineSweep(t, freq1, freq2, True)
        playRec(sineSweep(t, freq1, freq2))
        flag = True

    return render_template("index.html", flag = flag, form = audioForm)


@app.route("/processing", methods = ["GET", "POST"])
def processing():
    processingForm = forms.ProcessingForm(request.form)
    
    return render_template("processing.html", form = processingForm)

@app.route("/results", methods = ["GET","POST"])
def results():
    processingForm = forms.ProcessingForm(request.form)
    if request.method == "POST":
        bandwidth = processingForm.bandwidth.data
        smtMethod = processingForm.smtMethod.data
        t60Method = processingForm.t60Method.data 
        
        try:
            record, fs = sf.read("./static/audio/record.wav")
            inv, fs = sf.read("./static/audio/invFilter.wav")
            impulseResponse = iRObtention(record, inv)   
            
        except RuntimeError:
            impulseResponse, fs = sf.read("./static/audio/iRSynth.wav")
            
        logNormAudio = logNorm(impulseResponse)
#        filteredAudio = filtr(logNormAudio, bandwidth)

        smtAudio = smoothing(logNormAudio, smtMethod)
        schroederImpulse = schroeder(smtAudio, 3)
        
#        edtResult = edt(impulseResponse)
#        t60Result = t60(schroederImpulse, t60Method)
#        d50Result = d50(schroederImpulse)
#        c80Result = c80(schroederImpulse)
#, edtResult = edtResult, t60Result = t60Result, d50Result = d50Result, c80Result = c80Result

    return render_template("results.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = "record.wav"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/processing")
    return render_template("upload.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/syntetize", methods = ["GET", "POST"])
def syntetize():
    sintForm = forms.SintetizeForm(request.form)
    if request.method == "POST":
        t = sintForm.time.data
        bandwidth = sintForm.bandwidth.data
        iRSynth(t, bandwidth)

    return render_template("syntetize.html", form = sintForm)

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
        app.run(debug = True, port = 4000)
