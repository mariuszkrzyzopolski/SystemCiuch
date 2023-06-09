import time

from rpi_ws281x import Color, PixelStrip

LED_COUNT = 30  # Number of LED pixels.
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

strip1 = PixelStrip(LED_COUNT, 12, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 0)
strip1.begin()

strip2 = PixelStrip(LED_COUNT, 13, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 1)
strip2.begin()

strips = [strip1, strip2]


def show_set(set: []):
    r = 0
    g = 0
    b = 0
    for i in range(1024):
        if 256 > i:
            r = i
        elif 256 <= i < 512:
            r = 512 - i - 1
            g = i - 256
        elif 512 <= i < 768:
            g = 768 - i - 1
            b = i - 512
        elif 768 <= i < 1024:
            b = 1024 - i - 1

        for item in set:
            if int(item["LED_PIN"]) == 12:
                strip1.setPixelColor(int(item["position"]), Color(r, g, b))
                strip1.show()
            elif int(item["LED_PIN"]) == 13:
                strip2.setPixelColor(int(item["position"]), Color(r, g, b))
                strip2.show()
        time.sleep(0.05)
    off_all()


def off_all():
    for i in range(strip1.numPixels()):
        strip1.setPixelColor(i, Color(0, 0, 0))
    for i in range(strip2.numPixels()):
        strip2.setPixelColor(i, Color(0, 0, 0))
    strip1.show()
    strip2.show()


def pixel_rainbow(strip, pixel):
    r = 0
    g = 0
    b = 0
    for i in range(1024):
        if 256 > i:
            r = i
        elif 256 <= i < 512:
            r = 512 - i - 1
            g = i - 256
        elif 512 <= i < 768:
            g = 768 - i - 1
            b = i - 512
        elif 768 <= i < 1024:
            b = 1024 - i - 1
        strip.setPixelColor(pixel, Color(r, g, b))
        strip.show()
        time.sleep(0.05)


def start_rainbow():
    r = 0
    g = 0
    b = 0
    for i in range(1024):
        for pixel in range(strip1.numPixels()):
            if 256 > i:
                r = i
            elif 256 <= i < 512:
                r = 512 - i - 1
                g = i - 256
            elif 512 <= i < 768:
                g = 768 - i - 1
                b = i - 512
            elif 768 <= i < 1024:
                b = 1024 - i - 1
            strip1.setPixelColor(pixel, Color(r, g, b))
            strip2.setPixelColor(pixel, Color(r, g, b))
        strip1.show()
        strip2.show()
        time.sleep(0.05)
    off_all()


"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    print("Press Ctrl-C to quit.")
    dictionary = [
        {"LED_PIN": 12, "position": 0},
        {"LED_PIN": 12, "position": 1},
        {"LED_PIN": 13, "position": 2},
    ]
    off_all()
    # start_rainbow()
    # pixel_rainbow(strip1, 5)
    show_set(dictionary)
"""
