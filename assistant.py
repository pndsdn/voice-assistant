from __future__ import print_function
import os
import sys
import webbrowser as wbb
import json
import time

import pymorphy2
import wave
from vosk import Model, KaldiRecognizer
import pyaudio
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from winsound.sound import Sound
from w2n import extractor

SOUND_FOLDER = f'{os.path.join(os.path.dirname(__file__))}/replicas/'

COMMANDS = {
    "открыть": {
        "диспетчер задач": ["taskmgr", "bot-task-manager.wav"],
        "панель управления": ["control panel", "bot-control-panel.wav"],
        "проводник": ["explorer", "bot-opening.wav"]
    },
    "найти": {
        "в интернете": ["", "bot-searching.wav"]
    },
    "выключить": {
        "звук": ["", "bot-turning-off.wav"]
    },
    "включить": {
        "звук": ["", "bot-turning-on.wav"]
    },
    "разделить": "bot-pull-out-calculator.wav",
    "выключиться": "bot-pull-out-calculator.wav"
}


class Assistant(object):
    def __init__(self):
        self.model = Model('vosk-model-small-ru-0.22')
        self.recognizer = KaldiRecognizer(self.model, 16000)

        self.cap = pyaudio.PyAudio()
        self.stream = self.cap.open(format=pyaudio.paInt16, channels=1,
                                    rate=16000,
                                    input=True,
                                    frames_per_buffer=8192)
        self.stream.start_stream()

        wbb.register('chrome', None,
                     wbb.BackgroundBrowser(r'C:\Program Files\Google'
                                           r'\Chrome\Application'
                                           r'\chrome.exe'))

        self.morph = pymorphy2.MorphAnalyzer()

    def recognizing(self):
        self.stream.stop_stream()
        play_audio_callback(f'{SOUND_FOLDER}bot-start.wav')
        self.stream.start_stream()
        while self.stream.is_active():
            try:
                data = self.stream.read(4096)
                if self.recognizer.AcceptWaveform(data):
                    ror = json.loads(self.recognizer.Result())["text"]
                    print(ror)
                    try:
                        if self.command_execution(ror):
                            pass
                        else:
                            break

                    except IndexError:
                        pass

            except KeyboardInterrupt:
                self.stream.stop_stream()
                self.stream.close()
                self.cap.terminate()
                break

    def play_assistant_replica(self, act, obj):
        self.stream.stop_stream()
        play_audio_callback(f'{SOUND_FOLDER}'
                            f'{(COMMANDS[act][obj][1])}')
        self.stream.start_stream()

    def command_execution(self, text):
        action = self.morph.normal_forms(text.split()[0])[0] if len(self.morph.normal_forms(text.split()[0])) == 1 else self.morph.normal_forms(text.split()[0])[1]
        action_object = text[len(text.split()[0]) + 1::]

        if action in COMMANDS.keys():
            if action == "выключиться":
                self.stream.stop_stream()
                play_audio_callback(f'{SOUND_FOLDER}bot-hanging-up.wav')
                self.stream.start_stream()
                return False

            if action == "найти":
                if action_object in COMMANDS[action].keys():
                    action_object = "в интернете"
                    q = text[text.find(action_object) + len(
                        action_object) + 1::]
                    os.system(f"python -m webbrowser -t "
                              f"https://www.google.com/search?q={q}")
                    self.play_assistant_replica(action, action_object)

                else:
                    print("Команда не распознана")

            if action == "выключить":
                if action_object == "звук":
                    self.play_assistant_replica(action, action_object)

                    if not Sound.is_muted():
                        Sound.mute()

                else:
                    print("Команда не распознана")

            if action == "включить":
                if action_object == "звук":
                    if Sound.is_muted():
                        Sound.mute()
                        self.play_assistant_replica(action, action_object)

                else:
                    print("Команда не распознана")

            if action == "разделить":
                ext = extractor.NumberExtractor()
                num1 = ext.replace_groups(text[len(text.split()[0]) + 1:])[
                    0]
                num2 = ext.replace_groups(text[len(text.split()[0]) + 1:])[
                    1]
                _frac = num1 / num2
                self.play_assistant_replica(action, action_object)

            if action == "открыть":
                if action_object in COMMANDS[action].keys():
                    os.system(COMMANDS[action][action_object][0])
                    self.play_assistant_replica(action, action_object)

                else:
                    print("Команда не распознана")

        else:
            print("Команда не распознана")

        return True


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Голосовой помощник")
        self.setGeometry(100, 80, 400, 250)

        self.header = QtWidgets.QLabel(self)
        self.header.move(10, 10)
        self.header.setText("Слушаю:")
        self.header.adjustSize()

        self.recognizing = QtWidgets.QLabel(self)
        self.recognizing.move(30, 20)

    def set_recognized_text(self, text):
        self.recognizing.setText(text)
        self.recognizing.adjustSize()

    def winrec(self):
        self.assistant = Assistant()
        self.assistant.recognizing()


def play_audio_callback(wave_path):
    wf = wave.open(wave_path, 'rb')

    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    try:
        assistant = Assistant()
        assistant.recognizing()

    except KeyboardInterrupt:
        pass

