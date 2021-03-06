import time
import numpy as np
from rpi_ws281x import PixelStrip, Color
from subprocess import Popen
import settings
from pathlib import Path
from utils.stoppable_thread import StoppableThread
from utils.strip_actions import StripActions

# Singleton class as defined in:
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
class LedCore:
    class __LedCore:
        def __init__(self):
            # Create NeoPixel object with appropriate configuration.
            self.strip = PixelStrip(
                settings.LED_COUNT,
                settings.LED_PIN,
                settings.LED_FREQ_HZ,
                settings.LED_DMA,
                settings.LED_INVERT,
                settings.LED_BRIGHTNESS,
                settings.LED_CHANNEL,
            )
            # Intialize the library (must be called once before other functions).
            self.strip.begin()

            self.thread = None
            self.strip_actions = StripActions()

        def strip_action(self, name, **kwargs):
            if (
                issubclass(type(self.thread), StoppableThread) 
                and self.thread.is_alive() 
                and not self.thread.stopped()
            ):
                self.thread.stop()
                self.thread.join()
            self.thread = getattr(self.strip_actions, name)(self.strip, **kwargs)
            return self.thread

    instance = None

    def __init__(self):
        if not LedCore.instance:
            LedCore.instance = LedCore.__LedCore()

    def __getattr__(self, name):
        return getattr(self.instance, name)
