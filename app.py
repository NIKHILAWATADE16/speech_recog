
import speech_recognition as sr
import pyttsx3
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from pydub import AudioSegment
from pydub.silence import split_on_silence
from os import path
import subprocess
import pandas


r = sr.Recognizer()


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS-14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static'
app.config['UPLOAD_FOLDE'] = ''


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


stri = ""


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
@app.route('/trail')
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  app.config['UPLOAD_FOLDER'], secure_filename("test.wav")))  # Then save the file
        return render_template('index1.html', form=form, result=get_large_audio_transcription(file))
    return render_template('index.html', form=form, result="")




if __name__ == '__main__':
    app.run(debug=True)
