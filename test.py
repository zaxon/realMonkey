# -*- coding: utf-8 -*-

import os,sys
sys.path.append(r'E:\realMonkey') #this is your realMonkey path on pc
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *
#
deviceName=['1'] #choice your devices
device=rMonkeyRunner(__file__,deviceName)

device.press('KEYCODE_HOME')
device.sleep(4.0)
device.click(UIELEMENT.TEXT,'电话')
