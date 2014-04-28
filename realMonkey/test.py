# -*- coding: utf-8 -*-

import os,sys
sys.path.append(r'E:\realMonkey')
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *
device=rMonkeyRunner(__file__)

device.shell('adb shell am start -a com.baidu.searchbox.MainActivity')
device.sleep(3)

device.click(UIELEMENT.CLASSNAME,'android.widget.Button')
device.sleep(1)

device.input('bird')
device.sleep(1)

device.click(UIELEMENT.TEXT,'搜索')
device.sleep(5)









