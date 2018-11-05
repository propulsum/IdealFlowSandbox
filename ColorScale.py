import math


class ColorScale:
    @staticmethod
    def scale_to_color(value, low, high):
        if value <= low:
            scale = 0
        elif value >= high:
            scale = 1
        else:
            scale = (value - low) / (high - low)

        c = 255 * scale
        return '#{:02X}00{:02X}'.format(math.ceil(c), math.ceil(255 - c))
