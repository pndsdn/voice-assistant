import os
import subprocess
import webbrowser as wbb
import json

import pymorphy2
from vosk import Model, KaldiRecognizer
import pyaudio
import PyQt5

commands = {
    "открой": {
        "диспетчер задач": "taskmg",
        "панель управления": "control panel",
        "проводник": "explorer"
    },
    "найди": ["в интернете"],
    "выключи": ["звук"],
    "включи": ["звук"],
    "раздели": None,
    "выключись": None
}

model = Model('vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                  frames_per_buffer=8192)
stream.start_stream()

morph = pymorphy2.MorphAnalyzer()
print("я голосовой помогатор")
while stream.is_active():
    try:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result_of_recognizing = json.loads(recognizer.Result())["text"]
            try:
                action = result_of_recognizing.split()[0]
                action_object = result_of_recognizing[len(action)+1::]

                if action in commands.keys() and action_object in commands[action].keys():
                    print(commands[action][action_object])
                else:
                    print("Команда не распознана")

            except IndexError:
                pass

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        cap.terminate()
        break
