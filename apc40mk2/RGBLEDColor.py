from colormath.color_objects import sRGBColor
from colormath.color_diff import delta_e_cie2000
from os.path import dirname, join

class RGBLEDColor:
    def __init__(self,
        name: int,
        color: str,
        velocity: int,
    ) -> None:
        self.name = name
        self.color = sRGBColor.new_from_rgb_hex(color)
        self.velocity = velocity


class RGBLEDColors:
    allColors = None
    with open(join(dirname(__file__), 'RGBLEDColors'), 'rt') as f:
        allColors = list(map(
            lambda entries: RGBLEDColor(
                int(entries[0], 16) if '0x' in entries[0] else int(entries[0]),
                entries[1],
                int(entries[2]),
            ),
            list(map(
                lambda line: line.strip().split(' '),
                f.readlines(),
            ))
        ))
        f.close()

    @staticmethod
    def __getitem__(key: int):
        return RGBLEDColors.allColors[key]

    @staticmethod
    def nearestColor(hex: str) -> RGBLEDColor:
        nearestColor = RGBLEDColors[0]
        nearestDeltaE = 1.e9
        for color in RGBLEDColors:
            deltaE = delta_e_cie2000(color.color, sRGBColor.new_from_rgb_hex(hex))
            if deltaE < nearestDeltaE:
                nearestColor = color
        return nearestColor

