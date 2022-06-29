from __future__ import print_function
import os
import subprocess
import webbrowser as wbb
import json
import time

import pymorphy2
import wave
from vosk import Model, KaldiRecognizer
import pyaudio
import PyQt5

from config import SOUND_FOLDER, COMMANDS


def form_request(ror, obj):
    request = ''

    print(q)
    return request


def play_audio_callback(wave_path):
    wf = wave.open(wave_path, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    # read data
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()


model = Model('vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                  frames_per_buffer=8192)
stream.start_stream()

wbb.register('chrome', None, wbb.BackgroundBrowser(r'C:\Program Files\Google'
                                                   r'\Chrome\Application'
                                                   r'\chrome.exe'))

print(COMMANDS)
morph = pymorphy2.MorphAnalyzer()
while stream.is_active():
    try:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            ror = json.loads(recognizer.Result())["text"]
            try:
                action = morph.normal_forms(ror.split()[0])[0] if len(morph.normal_forms(ror.split()[0])) == 1 else morph.normal_forms(ror.split()[0])[1]
                action_object = ror[len(action)+1::]

                if action in COMMANDS.keys():
                    if action == "выключись":
                        stream.stop_stream()
                        play_audio_callback(
                            f'{SOUND_FOLDER}bot-hanging-up.wav')
                        stream.start_stream()
                        break

                    if action == "найди":
                        action_object = "в интернете"
                        q = ror[ror.find(action_object)+len(action_object)+1::]
                        wbb.get('chrome').open_new_tab(
                            f'https://www.google.com/search?q={q}')

                    if action_object in COMMANDS[action][0].keys():
                        os.system(COMMANDS[action][0][action_object])

                        stream.stop_stream()
                        play_audio_callback(f'{SOUND_FOLDER}'
                                            f'{(COMMANDS[action][1])}')
                        stream.start_stream()
                else:
                    print("Команда не распознана")

            except IndexError:
                pass

            # for command in commands.keys():
            #     if command in result_of_recognizing:
            #         if command == "открой диспетчер задач":
            #             stream.stop_stream()
            #             play_audio_callback(f'{SOUND_FOLDER}bot-opening.wav')
            #             stream.start_stream()
            #             os.system(commands[command])
            #
            #         elif command == "найди в интернете":
            #             q = result_of_recognizing[len(command)+1::]
            #             stream.stop_stream()
            #             wbb.get('chrome').open_new_tab(
            #                 f'https://www.google.com/search?q={q}')
            #             play_audio_callback(f'{SOUND_FOLDER}bot-searching.wav')
            #             stream.start_stream()
            #
            #         elif command == "выключи звук":
            #             stream.stop_stream()
            #             play_audio_callback(
            #                 f'{SOUND_FOLDER}bot-turning-off.wav')
            #             stream.start_stream()
            #
            #         elif command == "включи звук":
            #             stream.stop_stream()
            #             play_audio_callback(
            #                 f'{SOUND_FOLDER}bot-turning-on.wav')
            #             stream.start_stream()

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        cap.terminate()
        break
