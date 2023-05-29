from os.path import join, dirname
from numpy import log2

class RGBLEDType:
    def __init__(self,
        channel: int,
        primary: bool,
        oneshot: bool,
        pulsing: bool,
        blinking: bool,
        divisor: int,
    ) -> None:
        self.channel = channel
        self.primary = primary
        self.oneshot = oneshot
        self.pulsing = pulsing
        self.blinking = blinking
        self.divisor = divisor

    def toInt(self):
        if self.primary:
            return 0
        
        if self.oneshot:
            return 6 - int(log2(self.divisor))

        if self.pulsing:
            return 11 - int(log2(self.divisor))
        
        if self.blinking:
            return 16 - int(log2(self.divisor))

class RGBLEDTypes:
    allTypes = None
    with open(join(dirname(__file__), 'RGBLEDTypes'), 'rt') as f:
        allTypes = list(map(
            lambda entries: RGBLEDType(
                int(entries[0]),
                'Primary' in ''.join(entries),
                'Oneshot' in ''.join(entries),
                'Pulsing' in ''.join(entries),
                'Blinking' in ''.join(entries),
                int(entries[-1].split('/')[-1]),
            ),
            list(map(
                lambda line: line.strip().split(' '),
                f.readlines(),
            ))
        ))
        f.close()
