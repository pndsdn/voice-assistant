import os

SOUND_FOLDER = f'{os.path.join(os.path.dirname(__file__))}/sound/'

COMMANDS = {
    "открыть": [
        {
            "диспетчер задач": "taskmgr",
            "панель управления": "control panel",
            "проводник": "explorer"
        },
        "bot-opening.wav",
        "os"
    ],
    "найти": [
        {"в интернете": ""},
        "bot-searching.wav",
        "wbb"
    ],
    "выключить": [
        {"звук": ""},
        "bot-turning-off.wav"
    ],
    "включить": [
        {"звук": ""},
        "bot-turning-on.wav"
    ],
    "разделить": "",
    "выключиться": "",
}

# commands = {
#     "открой диспетчер задач": "taskmgr",
#     "открой панель управления": "control panel",
#     "открой проводник": "explorer",
#     "найди в интернете": "",
#     "выключи звук": "",
#     "включи звук": "",
#     "раздели": None,
#     "выключись": None
# }
