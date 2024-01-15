from flask import Flask, render_template, request, send_file
from flask import Flask, render_template, request
from gtts import gTTS
import tempfile
import pyttsx3
import os
import textwrap

from IPython.display import display
from IPython.display import Markdown

import google.generativeai as genai
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', audio_url='')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    user_text = request.form['text']

    # Your chatbox function
    def chatbox(text):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(text)
        response = response.text
        return response
    
    response = chatbox(user_text)

    # Save response to an audio file
    tts = gTTS(text=response, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    tts.save(temp_file.name)

    # Play the audio using pyttsx3
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()
    #response = to_markdown(response)

    return render_template("index.html", results=response, audio_url=temp_file.name)

# Route to serve the audio file
@app.route('/audio/<filename>')
def audio(filename):
    return send_file(filename, as_attachment=True, download_name='response.mp3')

if __name__ == '__main__':
    app.run(debug=True)
