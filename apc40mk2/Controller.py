from os.path import dirname, join
from enum import IntFlag

class ControllerCapabilities(IntFlag):
    LEDLess = 0x0
    Track = 0x1
    LEDRing = 0x2
    Master = 0x4
    RingType = 0x8

class Controller:
    def __init__(self,
        noteNumber: int,
        capabilities: ControllerCapabilities,
        name: str,
        channel: int = 0,
        value: int = 0,
    ) -> None:
        self.noteNumber = noteNumber
        self.capabilities = capabilities
        self.name = name
        self.channel = channel
        self.value = value

def determineCapabilities(flagStr: str) -> ControllerCapabilities:
    result = ControllerCapabilities.LEDLess
    for controllerCapability in ControllerCapabilities:
        if controllerCapability.name in flagStr:
            result = result | controllerCapability
    return result
    
class Controllers:
    allControllers = None
    with open(join(dirname(__file__), 'Controllers'), 'rt') as f:
        allControllers = list(map(
            lambda entries: Controller(
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
                lambda controller: controller.name == key,
                Controllers.allControllers,
            ))[0]
        except:
            raise KeyError('Key `{}` is not a valid controller name.'.format(key))

    @staticmethod
    def byNoteNumber(key: int):
        try:
            return list(filter(
                lambda controller: controller.noteNumber == key,
                Controllers.allControllers,
            ))[0]
        except:
            raise KeyError('Note number `{}` is not a valid controller note number.'.format(key))
