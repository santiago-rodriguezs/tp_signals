from flask import Flask
from flask import render_template
from flask import request

import forms

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
	audioForm = forms.AudioForm(request.form)
	if request.method == "POST" and audioForm.validate():
		print(audioForm.bandwidth.data) # field = campo pasado por formulario

	return render_template("index.html", form = form)

if __name__ == "__main__":
        app.run(debug = True)
