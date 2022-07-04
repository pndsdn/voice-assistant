from __future__ import print_function
import os
import webbrowser as wbb
import json
import time

import pymorphy2
import wave
from vosk import Model, KaldiRecognizer
import pyaudio

from winsound.sound import Sound
from w2n import extractor

SOUND_FOLDER = f'{os.path.join(os.path.dirname(__file__))}/replicas/'

COMMANDS = {
    "открыть": {
        "диспетчер задач": ["taskmgr", "bot-task-manager.mp3"],
        "панель управления": ["control panel", "bot-opening.wav"],
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


def play_assistant_replica(act, obj):
    stream.stop_stream()
    play_audio_callback(f'{SOUND_FOLDER}'
                        f'{(COMMANDS[act][obj][1])}')
    stream.start_stream()


def command_execution(text):
    action = morph.normal_forms(text.split()[0])[0] if len(morph.normal_forms(text.split()[0])) == 1 else morph.normal_forms(ror.split()[0])[1]
    action_object = text[len(text.split()[0]) + 1::]

    if action in COMMANDS.keys():
        if action == "выключиться":
            stream.stop_stream()
            play_audio_callback(f'{SOUND_FOLDER}bot-hanging-up.wav')
            stream.start_stream()
            return False

        if action == "найти":
            action_object = "в интернете"
            q = ror[ror.find(action_object) + len(action_object) + 1::]
            os.system(f"python -m webbrowser -t "
                      f"https://www.google.com/search?q={q}")
            play_assistant_replica(action, action_object)

        if action == "выключить":
            if action_object == "звук":
                play_assistant_replica(action, action_object)

                if not Sound.is_muted():
                    Sound.mute()

        if action == "включить":
            if action_object == "звук":
                if Sound.is_muted():
                    Sound.mute()
                    play_assistant_replica(action, action_object)

        if action == "разделить":
            ext = extractor.NumberExtractor()
            num1 = ext.replace_groups(ror[len(ror.split()[0]) + 1:])[0]
            num2 = ext.replace_groups(ror[len(ror.split()[0]) + 1:])[1]
            _frac = num1 / num2
            play_assistant_replica(action, action_object)

        if action == "открыть":
            os.system(COMMANDS[action][0][action_object])
            play_assistant_replica(action, action_object)
    else:
        print("Команда не распознана")

    return True


model = Model('vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                  frames_per_buffer=8192)
stream.start_stream()

wbb.register('chrome', None, wbb.BackgroundBrowser(r'C:\Program Files\Google'
                                                   r'\Chrome\Application'
                                                   r'\chrome.exe'))

morph = pymorphy2.MorphAnalyzer()

while stream.is_active():
    try:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            ror = json.loads(recognizer.Result())["text"]
            print(ror)
            try:
                if command_execution(ror):
                    pass
                else:
                    break

            except IndexError:
                pass

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        cap.terminate()
        break
