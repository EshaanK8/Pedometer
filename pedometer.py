# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import displayio
import terminalio
from adafruit_gizmo import tft_gizmo
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_apple_media import AppleMediaService
from adafruit_ble_apple_media import UnsupportedCommand
from adafruit_circuitplayground import cp


#------------DISPLAY#------------
BACKGROUND_COLOR = 0x49523b  # Gray
TEXT_COLOR = 0xFF0000  # Red
BORDER_COLOR = 0xAAAAAA  # Light Gray
STATUS_COLOR = BORDER_COLOR

def wrap_in_tilegrid(filename:str):
    # CircuitPython 6 & 7 compatible
    odb = displayio.OnDiskBitmap(open(filename, "rb"))
    return displayio.TileGrid(
        odb, pixel_shader=getattr(odb, 'pixel_shader', displayio.ColorConverter())
    )

def make_background(width, height, color):
    color_bitmap = displayio.Bitmap(width, height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = color

    return displayio.TileGrid(color_bitmap,
                              pixel_shader=color_palette,
                              x=0, y=0)

def load_font(fontname, text):
    font = bitmap_font.load_font(fontname)
    font.load_glyphs(text.encode('utf-8'))
    return font

def make_label(text, x, y, color, font=terminalio.FONT):
    if isinstance(font, str):
        font = load_font(font, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,?()")
    text_area = Label(font, text=text, color=color)
    text_area.x = x
    text_area.y = y
    return text_area

def set_label(label, value, max_length):
    text = "{}".format(value)
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    label.text = text

def set_status(label, action_text, player):
    label.text = "{} on {}".format(action_text, player)
    _, _, label_width, _ = label.bounding_box
    label.x = display.width - 10 - label_width

display = tft_gizmo.TFT_Gizmo()
group = displayio.Group()
display.show(group)



while True:
    '''
    if cp.shake(shake_threshold=12):
        print("Shake detected more easily than before!")'''
    print("here")

    # Draw the text fields
    #group.append(wrap_in_tilegrid("/A_black_image.bmp"))
    title_label = make_label("None", 12, 30, TEXT_COLOR, font="/fonts/Arial-Bold-18.bdf")
    group.pop()
    group.append(make_background(240, 240, BACKGROUND_COLOR))
    border = Rect(4, 4, 232, 200, outline=BORDER_COLOR, stroke=2)
    group.append(title_label)



'''

while True:
    # wait for shake
    while not cpb.shake(shake_threshold=SHAKE_THRESHOLD):
        pass
    if cp.shake(shake_threshold=12):
        display.show(print("Number"))
'''
