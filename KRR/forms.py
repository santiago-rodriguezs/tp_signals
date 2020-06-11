from wtforms import Form
from wtforms import StringField, FloatField, FileField, SelectField, IntegerField

from wtforms import validators

class AudioForm(Form):
    bandwidth = SelectField('Bandwidth', choices=[('octave', 'octave'), ('third', 'third')])          
    time = IntegerField("Time", [validators.DataRequired(message = "The time is required.")
	])
    freq1 = IntegerField("Freq1", [validators.DataRequired(message = "The freq1 is required.")
	])
    freq2 = IntegerField("Freq2", [validators.DataRequired(message = "The freq2 is required.")
	])
    audio = FileField('Audio File')
     
class ProcessingForm(Form):
    bandwidth = SelectField('Bandwidth', choices=[('octave', 'octave'), ('third', 'third')])          
    smtMethod = SelectField('Smoothing Method', choices=[('hilbert', 'hilbert'), ('median', 'median'), ('savgol', 'savgol')])          
    t60Method = SelectField('T60 Method', choices=[('t10', 't10'), ('t20', 't20'), ('t30', 't30')])

class SintetizeForm(Form):
    time = IntegerField("Time", [validators.DataRequired(message = "The time is required.")
	])
    bandwidth = SelectField('Bandwidth', choices=[('octave', 'octave'), ('third', 'third')])          