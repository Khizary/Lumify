import tinytuya
import colorsys
import fast_colorthief
import os
from login import API_Key, DeviceID, localkey


myBulb = tinytuya.BulbDevice(DeviceID, "0.0.0.0", local_key=localkey)
restoreBrightness, restoreColorTemp = myBulb.brightness(), myBulb.colourtemp()


async def changeLighting(name):
    found = False
    for file in os.listdir(os.curdir):
        if file.startswith(name):
            found = True
    if found:
        dominant_color = fast_colorthief.get_dominant_color(
            name + '.jpeg', quality=2)
    else:
        print("ECP1")
        dominant_color = (255, 255, 255)
    print(dominant_color)
    (h, s, v) = convert_rgb_to_hsv(
        dominant_color[0], dominant_color[1], dominant_color[2])
    if v> 0.5 and v < 0.9:
        v = v * 1.1
    print(h, s, v)
    myBulb.set_mode("colour")
    myBulb.set_hsv(h, s, v)


def convert_rgb_to_hsv(red, green, blue):

    red_percentage = red / float(255)
    green_percentage = green / float(255)
    blue_percentage = blue / float(255)

    color_hsv_percentage = colorsys.rgb_to_hsv(
        red_percentage, green_percentage, blue_percentage)
    print('color_hsv_percentage: ', color_hsv_percentage)
    color_h = color_hsv_percentage[0]
    color_s = color_hsv_percentage[1]
    color_v = color_hsv_percentage[2]
    color_hsv = (color_h, color_s, color_v)
    return color_hsv


def restorewhite():
    myBulb.set_mode("white")
    myBulb.set_brightness(restoreBrightness)
    myBulb.set_colourtemp(restoreColorTemp)


def setwhite():
    myBulb.set_mode("white")
    myBulb.set_brightness(255)
    myBulb.set_colourtemp(240)
