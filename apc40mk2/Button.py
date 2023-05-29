from os.path import dirname, join
from enum import IntFlag

class ButtonCapabilities(IntFlag):
    LEDLess = 0x0
    OnOff = 0x1
    Blink = 0x2
    Track = 0x4
    RGB = 0x8
    YellowOrange = 0x10

class Button:
    def __init__(self,
        noteNumber: int,
        capabilities: ButtonCapabilities,
        name: str,
        channel: int = None
    ) -> None:
        self.noteNumber = noteNumber
        self.capabilities = capabilities
        self.name = name
        self.channel = channel

def determineCapabilities(flagStr: str) -> ButtonCapabilities:
    result = ButtonCapabilities.LEDLess
    for buttonCapability in ButtonCapabilities:
        if buttonCapability.name in flagStr:
            result = result | buttonCapability
    return result

class Buttons:
    allButtons = None
    with open(join(dirname(__file__), 'Buttons'), 'rt') as f:
        allButtons = list(map(
            lambda entries: Button(
                int(entries[0], 16) if '0x' in entries[0] else int(entries[0]),
                determineCapabilities(entries[1]),
                ' '.join(entries[2:]),
            ),
            list(map(
                lambda line: line.strip().split(' '),
                f.readlines(),
            ))
        ))
        f.close()

    @staticmethod
    def byName(key: str):
        try:
            return list(filter(
                lambda button: button.name == key,
                Buttons.allButtons,
            ))[0]
        except:
            raise KeyError('Key `{}` is not a valid button name.'.format(key))

    @staticmethod
    def byNoteNumber(key: int):
        try:
            return list(filter(
                lambda button: button.noteNumber == key,
                Buttons.allButtons,
            ))[0]
        except:
            raise KeyError('Note number `{}` is not a valid button note number.'.format(key))
