from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
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
    def nearestColor(hex: str) -> RGBLEDColor:
        nearestColor = RGBLEDColors.allColors[0]
        nearestDeltaE = 1.e9
        hexColor = sRGBColor.new_from_rgb_hex(hex)
        for color in RGBLEDColors.allColors:
            # FIXME: This is bugged in colormath because of a numpy deprecation.
            # Also: colormath is unmaintained as of now, so this is a dead end.
            # Will use euclidean distance until this resolves; keep commented code
            # to enable CIELAB distance again as soon as they fix it.
            # deltaE = delta_e_cie2000(
            #     convert_color(color.color, LabColor),
            #     convert_color(sRGBColor.new_from_rgb_hex(hex), LabColor),
            # )
            deltaE = pow(color.color.rgb_r - hexColor.rgb_r, 2) + \
                pow(color.color.rgb_g - hexColor.rgb_g, 2) + \
                pow(color.color.rgb_b - hexColor.rgb_b, 2)
            if deltaE < nearestDeltaE:
                nearestColor = color
                nearestDeltaE = deltaE
        return nearestColor

