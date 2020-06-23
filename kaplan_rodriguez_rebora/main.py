import soundfile as sf
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import numpy as np

from calibrate import sineSweep, pinkNoise, playRec
from process import iRObtention, filtr, logNorm, smoothing, schroeder, plotting, lundeby
from process import edt, t60, d50, c80
from process import iRSynth
import forms

UPLOAD_FOLDER = "./static/audio"
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

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
    bandwidth = ""
    freqs = []
    edtResult = []
    t60Result = []
    d50Result = []
    c80Result = []
    if request.method == "POST":
        bandwidth = processingForm.bandwidth.data
        t60Method = processingForm.t60Method.data 
        
        try:
            record, fs = sf.read("./static/audio/record.wav")
            inv, fs = sf.read("./static/audio/invFilter.wav")
            impulseResponse = iRObtention(record, inv)   
            
        except RuntimeError:
            impulseResponse, fs = sf.read("./static/audio/impulseResponse.wav")
            index = np.where(abs(impulseResponse) == max(abs(impulseResponse)))[0][0]
            impulseResponse = impulseResponse[index:]
            
        impulseResponse = impulseResponse[:fs]
        
        plotting(impulseResponse)
        
        filteredList = filtr(impulseResponse, bandwidth) 
        
        if bandwidth == "octave":
            freqs = [62.5, 125, 250, 500, 1000, 2000, 4000, 8000]
        elif bandwidth == "third":
            freqs = [62.50, 78.75, 99.21,
                    125, 157.5, 198.4, 250, 315, 396.9, 500, 630, 793.7, 1000,
                    1260, 1587, 2000, 2520, 3175, 4000, 5040, 6350, 8000]
        
        edtResult = []
        t60Result = []
        d50Result = []
        c80Result = []
        
        for band in filteredList: 

            smoothBand = smoothing(band, "hilbert")
            smoothBand = smoothing(smoothBand, "median")
            smoothBand = smoothing(smoothBand, "savgol")
            
            crosspoint = lundeby(logNorm(smoothBand))
            
            schroederBand = schroeder(logNorm(smoothBand), crosspoint)

            logBand = logNorm(schroederBand)
        
            edtResult.append(np.round(edt(logBand), 3))
            t60Result.append(np.round(t60(logBand, t60Method), 3))
            d50Result.append(np.round(d50(logBand)*100, 1))
            c80Result.append(-1 * np.round(c80(logBand), 1))
        
    file1 = open("./static/txt/data.txt","w")
    file1.write("Frequencies: [" + ", ".join(map(str, freqs)) + "]\nEDT: [" + ", ".join(map(str, edtResult)) + "]\nT60: [" + ", ".join(map(str, t60Result)) + "]\nD50: [" + ", ".join(map(str, d50Result)) + "]\nC80: [" + ", ".join(map(str, c80Result))+ "]\n")
    file1.close() 
    

    return render_template("results.html", freqs = freqs, bandwidth = bandwidth, edtResult = edtResult, t60Result = t60Result, d50Result = d50Result, c80Result = c80Result)

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
            filename = "impulseResponse.wav"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/processing")
    return render_template("upload.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/synthesize", methods = ["GET", "POST"])
def synthesize():
    sintForm = forms.SynthesizeForm(request.form)
    if request.method == "POST":
        t = sintForm.time.data
        bandwidth = sintForm.bandwidth.data
        iRSynth(t, bandwidth)
        return redirect("/processing")

    return render_template("synthesize.html", form = sintForm)

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
        app.run(debug = True, port = 3000)
