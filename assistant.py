import os
import subprocess
import webbrowser as wbb
import json

from vosk import Model, KaldiRecognizer
import pyaudio
import PyQt5

model = Model('vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                  frames_per_buffer=8192)
stream.start_stream()

command_list = {
    "открой диспетчер задач": "taskmgr",
    "открой панель управления": "control panel"
}

print("я голосовой помогатор")
while stream.is_active():
    try:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result_of_recognizing = json.loads(recognizer.Result())["text"]

            if result_of_recognizing in command_list.keys():
                print('Секунду...')
                os.system(command_list[result_of_recognizing])

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        cap.terminate()
        break
