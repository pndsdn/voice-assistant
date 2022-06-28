import os
import subprocess
import webbrowser as wbb
import json

from vosk import Model, KaldiRecognizer
import pyaudio
import PyQt5
import nltk
nltk.download("punkt")


model = Model('vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                  frames_per_buffer=8192)
stream.start_stream()

'''
command = {
    "action": "what an assistant should do", 
    "object": "action object"
}
'''

commands = {
    "открой": [
        "диспетчер задач",
        "панель управления",
        "проводник"
    ],
    "найди в интернете": None,
    "выключись": None,
    "выключи": "звук",
    "включи": "звук",
    "раздели": None,
}

print("я голосовой помогатор")
while stream.is_active():
    try:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result_of_recognizing = json.loads(recognizer.Result())["text"]
            word_tokenize = nltk.word_tokenize(result_of_recognizing,
                                               language="russian")

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        cap.terminate()
        break
