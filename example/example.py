import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), '..'))
from apc40mk2.APC40MK2 import APC40MK2
from apc40mk2.Button import Buttons
from apc40mk2.RGBLEDColor import RGBLEDColors
from apc40mk2.RGBLEDMode import RGBLEDMode, RGBLEDModeCapabilities
from apc40mk2.Controller import Controllers
from apc40mk2.LEDRingType import LEDRingType
from time import sleep

if __name__ == '__main__':
    midiController = APC40MK2()
    midiController.run()

    midiController.setRGBButtonState(Buttons.byName("CLIP LAUNCH 13"), RGBLEDColors.nearestColor('#ff0000'), RGBLEDMode(RGBLEDModeCapabilities.Primary, 1))
    midiController.setRGBButtonState(Buttons.byName("CLIP LAUNCH 13"), RGBLEDColors.nearestColor('#00ff00'), RGBLEDMode(RGBLEDModeCapabilities.Pulsing, 2))
   
    midiController.setButtonCallback(lambda message, button: print(button.name, '(Channel: {})'.format(button.channel), message.messageTypeString()))

    midiController.setLEDRingControllerType(Controllers.byName("DEVICE KNOB 2 LED RING TYPE"), LEDRingType.VolumeStyle, 1)
    midiController.setLEDRingControllerValue(Controllers.byName("DEVICE KNOB 2"), 0x7F, 1)

    while True:
        sleep(1)
