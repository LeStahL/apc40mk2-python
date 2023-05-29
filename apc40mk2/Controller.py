from threading import Thread
from rtmidi import RtMidiIn, RtMidiOut


class Controller:
    PortName = 'APC40 mkII'
    PollInterval = 250

    def __init__(self) -> None:
        self._thread = Thread(target=self.run)
        self._abort = False

    def abort(self) -> None:
        self._abort = True

    def run(self) -> None:
        self.midiIn = RtMidiIn()
        for port in range(self.midiIn.getPortCount()):
            if self.midiIn.getPortName(port).startswith(Controller.PortName):
                self.midiIn.openPort(port)

        self.midiOut = RtMidiOut()
        for port in range(self.midiOut.getPortCount()):
            if self.midiOut.getPortName(port).startswith(Controller.PortName):
                self.midiOut.openPort(port)

        while not self._abort:
            message = self.midiIn.getMessage(Controller.PollInterval)
            if message:
                # TODO: handle message
                print(message)
