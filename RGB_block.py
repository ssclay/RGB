from nio.block.base import Block
from nio.properties import VersionProperty
from nio.signal.base import Signal
import time
import Adafruit_TCS34725


class RGB(Block):

    version = VersionProperty('0.1.0')

    def __init__(self):
        super().__init__()
        self.tcs = None

    def configure(self, context):
        super().configure(context)
        self.tcs = Adafruit_TCS34725.TCS34725()
        self.tcs.set_interrupt(False)

    def process_signals(self, signals):
        new_signals = []
        for signal in signals:
            _signal = signal.to_dict()
            r, g, b, c = self.tcs.get_raw_data()
            color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)
            lux = Adafruit_TCS34725.calculate_lux(r, g, b)
            new_signals.append([Signal({"red": r,
                                        "green": g,
                                        "blue": b,
                                        "clear": c,
                                        **_signal})])
        self.notify_signals(new_signals)
