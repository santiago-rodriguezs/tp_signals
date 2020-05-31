from wtforms import Form
from wtforms import StringField, FloatField, FileField, SelectField, IntegerField
#from wtforms.html5 import EmailField

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
    pass

class SintetizeForm(Form):
    pass

#UPLOAD INTERNET

#class UploadForm(Form):
#    audio = FileField(u'Audio File', [validators.regexp(u'^[^/\\]\.wav$')])
#
#    def validate_audio(form, field):
#        if field.data:
#            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

#def upload(request):
#    form = UploadForm(request.POST)
#    if form.audio.data:
#        audio_data = request.FILES[form.audio.name].read()
#        open(os.path.join(UPLOAD_PATH, form.audio.data), 'w').write(audio_data)