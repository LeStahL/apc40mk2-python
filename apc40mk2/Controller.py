from threading import Thread
from queue import Queue
from pygame import midi
from .Button import Button, ButtonCapabilities, Buttons
from .RGBLEDColor import RGBLEDColor, RGBLEDColors
from .RGBLEDType import RGBLEDType, RGBLEDTypes
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
        _type: RGBLEDType,
    ) -> None:
        if not button.capabilities & ButtonCapabilities.RGB:
            raise ValueError("Button {} does not have the RGB capability.".format(button.name))
    
        self._buttonStateModificationQueue.put((button, color, _type))

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
                (button, color, _type) = self._buttonStateModificationQueue.get()
                message = MidiMessage(MidiMessage.NoteOn, _type.toInt(), button.noteNumber, color.velocity)
                # print(message.isNoteOn())
                byteList = list(map(
                    lambda byte: int(byte),
                    message.serialize(),
                ))
                print("bytelist:", byteList)
                self.midiOutput.write([[byteList,20000]])
                # result = self.midiOut.sendMessage(RtMidiMessage(*byteList))
                # print("sent:", result)
                pass

            if self.midiInput.poll():
                [events] = self.midiInput.read(1)
                print(events)

            # message = self.midiInput.read(Controller.PollInterval)
            # if message:
            #     # TODO: handle message
            #     print(message)
