from wtforms import Form
from wtforms import StringField, TextField
from wtforms.html5 import EmailField

from wtforms import validators

class AudioForm(Form)
	bandwidth = StringField("Bandwidth",
				[validators.Required(message = "The bandwidth is required.")
				]) 
