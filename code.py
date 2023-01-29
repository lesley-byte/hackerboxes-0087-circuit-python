# adapted from the code of ladyada at Adafruit Industries
# made for HackerBox 0087 Picow kit
# SPDX-License-Identifier: MIT

import time
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_ili9341
from adafruit_bme280 import basic as adafruit_bme280

# Release any resources currently in use for the displays
displayio.release_displays()
# sw1 is on GP6 sw2 is on GP18
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP0)
tft_cs = board.GP20
tft_dc = board.GP22
i2c = busio.I2C(board.GP5, board.GP4)  # SCL, SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)  ## this address is unique for this module

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25
temperature = bme280.temperature
fahrenheit = (temperature*1.8) + 32


display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP21
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)
display.rotation = 180 ## rotate the display
# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw a green background
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(280, 200, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=2, x=25, y=50)
textLabel = "CircuitPython\nIndoor BME280 Readings"
textTemp = "\n%0.1f F" % fahrenheit
textHum = "\nHumidity: %0.1f %%" % bme280.relative_humidity
textPres = "\nPressure: %0.1f hPa" % bme280.pressure
textAlt = "\nAlt = %0.2f meters" % bme280.altitude
text = textLabel + textTemp + textHum + textPres + textAlt
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling


splash.append(text_group)
while True:
    temperature = bme280.temperature
    fahrenheit = (temperature*1.8) + 32
    textLabel = "CircuitPython\nIndoor BME280 Readings"
    textTemp = "\n%0.1f F" % fahrenheit
    textHum = "\nHumidity: %0.1f %%" % bme280.relative_humidity
    textPres = "\nPressure: %0.1f hPa" % bme280.pressure
    textAlt = "\nAlt = %0.2f meters" % bme280.altitude
    text_area.text = textLabel + textTemp + textHum + textPres + textAlt
    time.sleep(5)
