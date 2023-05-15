
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
import requests
import moviepy.editor as mp
import shutil

r = sr.Recognizer()


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    sound = AudioSegment.from_wav(path)
    chunks = split_on_silence(sound,
                              min_silence_len=500,
                              silence_thresh=sound.dBFS-14,
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                whole_text += text
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
        # print(type(file))
        return render_template('index1.html', form=form, result=get_large_audio_transcription(file),st=0)
    return render_template('index.html', form=form, result="")

@app.route('/video',methods=['GET', "POST"])
def video():
    form=UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  app.config['UPLOAD_FOLDE'], secure_filename("sample.mp4")))
        clip = mp.VideoFileClip("sample.mp4")
        clip.audio.write_audiofile("test.wav")
        shutil.move(os.path.join("", "test.wav"), os.path.join("F:\\Desktop\\speech_recognition\\static", "test.wav"))
        shutil.copy2(os.path.join("", "sample.mp4"), os.path.join("F:\\Desktop\\speech_recognition\\static", "sample.mp4"))
        return render_template('index1.html', form=form, result=get_large_audio_transcription("F:\\Desktop\\speech_recognition\\static\\test.wav"),st=1)
    return render_template('index.html', form=form, result="")
        
    


#hello

if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=5000)
    app.run(debug=True)
