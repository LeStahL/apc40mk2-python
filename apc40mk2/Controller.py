from threading import Thread
from queue import Queue
from pygame import midi
from .Button import Button, ButtonCapabilities
from .RGBLEDColor import RGBLEDColor
from .RGBLEDMode import RGBLEDMode
from .MidiMessage import MidiMessage

class Controller:
    PortName = b'APC40 mkII'

    def __init__(self) -> None:
        self._thread = Thread(target=self.loop, daemon=True)
        self._abort = False
        self._buttonStateModificationQueue = Queue()

    def abort(self) -> None:
        self._abort = True

    def run(self) -> None:
        self._thread.start()

    def setRGBButtonState(self,
        button: Button,
        color: RGBLEDColor,
        mode: RGBLEDMode,
    ) -> None:
        if not button.capabilities & ButtonCapabilities.RGB:
            raise ValueError("Button {} does not have the RGB capability.".format(button.name))
    
        self._buttonStateModificationQueue.put((button, color, mode))

    def loop(self) -> None:
        midi.init()

        for port in range(midi.get_count()):
            (interface, name, input, output, opened) =  midi.get_device_info(port)
            print(name)
            if input and not opened and name == Controller.PortName:
                self.midiInput = midi.Input(port)

            if output and not opened and name == Controller.PortName:
                self.midiOutput = midi.Output(port)

        while not self._abort:
            while self._buttonStateModificationQueue.qsize() != 0:
                (button, color, mode) = self._buttonStateModificationQueue.get()
                self.midiOutput.write([[list(map(
                    lambda byte: int(byte),
                    MidiMessage(MidiMessage.NoteOn, mode.channel(), button.noteNumber, color.velocity).serialize(),
                )), 20000]])

            if self.midiInput.poll():
                [events] = self.midiInput.read(1)
                print(events)

            # message = self.midiInput.read(Controller.PollInterval)
            # if message:
            #     # TODO: handle message
            #     print(message)
