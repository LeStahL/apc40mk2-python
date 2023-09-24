from threading import Thread
from queue import Queue
from pygame import midi, time
from typing import Callable
from copy import deepcopy
from .Button import Button, ButtonCapabilities, Buttons
from .RGBLEDColor import RGBLEDColor
from .RGBLEDMode import RGBLEDMode
from .MidiMessage import MidiMessage
from .Controller import Controller, ControllerCapabilities, Controllers
from .LEDRingType import LEDRingType

class APC40MK2:
    PortName = b'APC40 mkII'

    def __init__(self) -> None:
        self._thread = Thread(target=self.loop, daemon=True)
        self._abort = False
        self._buttonStateModificationQueue = Queue()
        self._controllerValueModificationQueue = Queue()
        self._controllerTypeModificationQueue = Queue()
        self._buttonCallback = None
        self._controllerCallback = None

    def abort(self) -> None:
        self._abort = True

    def run(self) -> None:
        self._thread.start()

    def setButtonCallback(self, callback: Callable) -> None:
        self._buttonCallback = callback

    def setControllerCallback(self, callback: Callable) -> None:
        self._controllerCallback = callback

    def setRGBButtonState(self,
        button: Button,
        color: RGBLEDColor,
        mode: RGBLEDMode,
    ) -> None:
        if not button.capabilities & ButtonCapabilities.RGB:
            raise ValueError("Button {} does not have the RGB capability.".format(button.name))
    
        self._buttonStateModificationQueue.put((button, color, mode))

    def setLEDRingControllerValue(self,
        controller: Controller,
        value: int,
        channel: int,
    ) -> None:
        if not controller.capabilities & ControllerCapabilities.LEDRing:
            raise ValueError("Controller {} does not have the LED ring capability.".format(controller.name))

        self._controllerValueModificationQueue.put((controller, value, channel))

    def setLEDRingControllerType(self,
        controller: Controller,
        _type: LEDRingType,
        channel: int,
    ) -> None:
        if not controller.capabilities & ControllerCapabilities.RingType:
            raise ValueError("Controller {} does not have the ring type capability.".format(controller.name))
    
        self._controllerTypeModificationQueue.put((controller, _type, channel))

    def loop(self) -> None:
        midi.init()
        clock = time.Clock()

        for port in range(midi.get_count()):
            (interface, name, input, output, opened) =  midi.get_device_info(port)
            if input and not opened and name == APC40MK2.PortName:
                self.midiInput = midi.Input(port)

            if output and not opened and name == APC40MK2.PortName:
                self.midiOutput = midi.Output(port)

        while not self._abort:
            while self._buttonStateModificationQueue.qsize() != 0:
                (button, color, mode) = self._buttonStateModificationQueue.get()
                self.midiOutput.write([[list(map(
                    lambda byte: int(byte),
                    MidiMessage(MidiMessage.NoteOn, mode.channel(), button.noteNumber, color.velocity).serialize(),
                )), 20000]])
            
            while self._controllerValueModificationQueue.qsize() != 0:
                (controller, value, channel) = self._controllerValueModificationQueue.get()
                self.midiOutput.write([[list(map(
                    lambda byte: int(byte),
                    MidiMessage(MidiMessage.Controller, channel, controller.noteNumber, value).serialize(),
                )), 20000]])

            while self._controllerTypeModificationQueue.qsize() != 0:
                (controller, _type, channel) = self._controllerTypeModificationQueue.get()
                self.midiOutput.write([[list(map(
                    lambda byte: int(byte),
                    MidiMessage(MidiMessage.Controller, channel, controller.noteNumber, _type.value).serialize(),
                )), 20000]])

            if self.midiInput.poll():
                [[messageList, _]] = self.midiInput.read(1)
                message = MidiMessage.parse(bytes(messageList))
                if message.isNoteOff() or message.isNoteOn():
                    button = deepcopy(Buttons.byNoteNumber(message.noteNumber))
                    button.channel = message.channel
                    if self._buttonCallback is not None:
                        self._buttonCallback(message, button)
                elif message.isController():
                    controller = deepcopy(Controllers.byNoteNumber(message.noteNumber))
                    controller.channel = message.channel
                    controller.value = message.velocity
                    if self._controllerCallback is not None:
                        self._controllerCallback(message, controller)
                else:
                    print(messageList)

            clock.tick(200)
