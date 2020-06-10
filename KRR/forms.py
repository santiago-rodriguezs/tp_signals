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
    method = SelectField('Method', choices=[('hilbert', 'hilbert'), ('median', 'median'), ('savgol', 'savgol')])          
class SintetizeForm(Form):
    pass
