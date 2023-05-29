import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), '..'))
from apc40mk2.Controller import Controller

# def print_message(midi):
#     if midi.isNoteOn():
#         print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
#     elif midi.isNoteOff():
#         print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
#     elif midi.isController():
#         print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())

if __name__ == '__main__':
    midiController = Controller()
    midiController.run()
