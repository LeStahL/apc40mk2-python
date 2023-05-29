from os.path import join, dirname
from numpy import log2
from enum import Enum

class RGBLEDModeCapabilities(Enum):
    Primary = 'Primary'
    Oneshot = 'Oneshot'
    Pulsing = 'Pulsing'
    Blinking = 'Blinking'

class RGBLEDMode:
    def __init__(self,
        capabilities: RGBLEDModeCapabilities,
        divisor: int,
    ) -> None:
        self.capabilities = capabilities
        self.divisor = divisor

    def channel(self):
        if self.capabilities == RGBLEDModeCapabilities.Primary:
            return 0
        
        if self.capabilities == RGBLEDModeCapabilities.Oneshot:
            return 6 - int(log2(self.divisor))

        if self.capabilities == RGBLEDModeCapabilities.Pulsing:
            return 11 - int(log2(self.divisor))
        
        if self.capabilities == RGBLEDModeCapabilities.Blinking:
            return 16 - int(log2(self.divisor))

class RGBLEDModes:
    allTypes = None
    with open(join(dirname(__file__), 'RGBLEDTypes'), 'rt') as f:
        allTypes = list(map(
            lambda entries: RGBLEDMode(
                RGBLEDModeCapabilities(entries[1]),
                int(entries[2].split('/')[1]),
            ),
            list(map(
                lambda line: line.strip().split(' '),
                f.readlines(),
            ))
        ))
        f.close()
