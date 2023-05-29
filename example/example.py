import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), '..'))
from apc40mk2.Controller import Controller
from apc40mk2.Button import Buttons
from apc40mk2.RGBLEDColor import RGBLEDColors
from apc40mk2.RGBLEDMode import RGBLEDMode, RGBLEDModeCapabilities
from time import sleep

if __name__ == '__main__':
    midiController = Controller()
    midiController.run()

    midiController.setRGBButtonState(Buttons.byName("CLIP LAUNCH 13"), RGBLEDColors.nearestColor('#ff0000'), RGBLEDMode(RGBLEDModeCapabilities.Primary, 1))
    midiController.setRGBButtonState(Buttons.byName("CLIP LAUNCH 13"), RGBLEDColors.nearestColor('#00ff00'), RGBLEDMode(RGBLEDModeCapabilities.Pulsing, 2))
   
    midiController.setButtonCallback(lambda message, button: print(button.name, message.messageTypeString()))

    while True:
        sleep(1)
