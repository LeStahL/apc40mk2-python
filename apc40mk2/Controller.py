from threading import Thread
from queue import Queue
from pygame import midi
from typing import Callable
from copy import deepcopy
from .Button import Button, ButtonCapabilities, Buttons
from .RGBLEDColor import RGBLEDColor
from .RGBLEDMode import RGBLEDMode
from .MidiMessage import MidiMessage

class Controller:
    PortName = b'APC40 mkII'

    def __init__(self) -> None:
        self._thread = Thread(target=self.loop, daemon=True)
        self._abort = False
        self._buttonStateModificationQueue = Queue()
        self._buttonCallback = None

    def abort(self) -> None:
        self._abort = True

    def run(self) -> None:
        self._thread.start()

    def setButtonCallback(self, callback: Callable) -> None:
        self._buttonCallback = callback

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
                [[messageList, _]] = self.midiInput.read(1)
                message = MidiMessage.parse(bytes(messageList))
                if message.isNoteOff() or message.isNoteOn():
                    button = deepcopy(Buttons.byNoteNumber(message.noteNumber))
                    button.channel = message.channel
                    if self._buttonCallback is not None:
                        self._buttonCallback(message, button)
                else:
                    print(messageList)
