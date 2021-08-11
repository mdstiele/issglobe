# -*- coding: utf-8 -*-

import atexit


def Color(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16) | (green << 8) | blue


class PixelStrip(object):
    def __init__(
        self,
        num,
        pin,
        freq_hz=800000,
        dma=10,
        invert=False,
        brightness=255,
        channel=0,
        strip_type=None,
        gamma=None,
    ):
        """Class to represent a SK6812/WS281x LED display.  Num should be the
        number of pixels in the display, and pin should be the GPIO pin connected
        to the display signal line (must be a PWM pin like 18!).  Optional
        parameters are freq, the frequency of the display signal in hertz (default
        800khz), dma, the DMA channel to use (default 10), invert, a boolean
        specifying if the signal line should be inverted (default False), and
        channel, the PWM channel to use (defaults to 0).
        """

        # Create the led data array.
        self._led_buffer = [0] * num
        self._leds = [0] * num
        self._brightness = brightness

        self._cleaned_up = False
        atexit.register(self.check_cleanup)
        # Substitute for __del__, traps an exit condition and cleans up properly
        atexit.register(self._cleanup)

        self.started = False

    def check_cleanup(self):
        assert self._cleaned_up

    def _cleanup(self):
        # Clean up memory used by the library when not needed anymore.
        self._cleaned_up = True

    def begin(self):
        """Initialize library, must be called once before other functions are
        called.
        """
        assert self.started == False
        self.started = True

    def show(self):
        """Update the display with the data from the LED buffer."""
        assert self.started
        self._leds = self._led_buffer.copy()

    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        assert self.started
        self._led_buffer[n] = color

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        """Set LED at position n to the provided red, green, and blue color.
        Each color component should be a value from 0 to 255 (where 0 is the
        lowest intensity and 255 is the highest intensity).
        """
        assert self.started
        self.setPixelColor(n, Color(red, green, blue, white))

    def getBrightness(self):
        assert self.started
        return self._brightness

    def setBrightness(self, brightness):
        """Scale each LED in the buffer by the provided brightness.  A brightness
        of 0 is the darkest and 255 is the brightest.
        """
        assert self.started
        self._brightness = brightness
        updated_buffer = []
        for pixel in self._led_buffer:
            new_value = int(pixel * brightness / 255)
            updated_buffer.append(new_value)
        self._led_buffer = updated_buffer

    def getPixels(self):
        """Return an object which allows access to the LED display data as if
        it were a sequence of 24-bit RGB values.
        """
        assert self.started
        return self._led_buffer

    def numPixels(self):
        """Return the number of pixels in the display."""
        assert self.started
        return len(self._led_buffer)

    def getPixelColor(self, n):
        """Get the 24-bit RGB color value for the LED at position n."""
        assert self.started
        return self._led_buffer[n]

    def getPixelColorRGB(self, n):
        assert self.started
        c = lambda: None
        setattr(c, "r", self._led_buffer[n] >> 16 & 0xFF)
        setattr(c, "g", self._led_buffer[n] >> 8 & 0xFF)
        setattr(c, "b", self._led_buffer[n] & 0xFF)
        return c


# Shim for back-compatibility
class Adafruit_NeoPixel(PixelStrip):
    pass


class ws:
    WS2811_TARGET_FREQ = "_rpi_ws281x.WS2811_TARGET_FREQ"
    SK6812_STRIP_RGBW = "_rpi_ws281x.SK6812_STRIP_RGBW"
    SK6812_STRIP_RBGW = "_rpi_ws281x.SK6812_STRIP_RBGW"
    SK6812_STRIP_GRBW = "_rpi_ws281x.SK6812_STRIP_GRBW"
    SK6812_STRIP_GBRW = "_rpi_ws281x.SK6812_STRIP_GBRW"
    SK6812_STRIP_BRGW = "_rpi_ws281x.SK6812_STRIP_BRGW"
    SK6812_STRIP_BGRW = "_rpi_ws281x.SK6812_STRIP_BGRW"
    SK6812_SHIFT_WMASK = "_rpi_ws281x.SK6812_SHIFT_WMASK"
    WS2811_STRIP_RGB = "_rpi_ws281x.WS2811_STRIP_RGB"
    WS2811_STRIP_RBG = "_rpi_ws281x.WS2811_STRIP_RBG"
    WS2811_STRIP_GRB = "_rpi_ws281x.WS2811_STRIP_GRB"
    WS2811_STRIP_GBR = "_rpi_ws281x.WS2811_STRIP_GBR"
    WS2811_STRIP_BRG = "_rpi_ws281x.WS2811_STRIP_BRG"
    WS2811_STRIP_BGR = "_rpi_ws281x.WS2811_STRIP_BGR"
    WS2812_STRIP = "_rpi_ws281x.WS2812_STRIP"
    SK6812_STRIP = "_rpi_ws281x.SK6812_STRIP"
    SK6812W_STRIP = "_rpi_ws281x.SK6812W_STRIP"