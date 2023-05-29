import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), '..'))
from apc40mk2.Controller import Controller
from apc40mk2.Button import Buttons
from apc40mk2.RGBLEDColor import RGBLEDColors
from apc40mk2.RGBLEDType import RGBLEDType
from time import sleep

if __name__ == '__main__':
    midiController = Controller()
    midiController.run()

    midiController.setRGBButtonState(Buttons.byName("CLIP LAUNCH 13"), RGBLEDColors.nearestColor('#ff0000'), RGBLEDType(0, True, False, False, False, 1))
    midiController.setRGBButtonState(Buttons.byName("CLIP LAUNCH 13"), RGBLEDColors.nearestColor('#0000ff'), RGBLEDType(0, False, False, True, False, 2))
   
    while True:
        sleep(1)
