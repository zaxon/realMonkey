# -*- coding: utf-8 -*-

import os,sys
sys.path.append(r'E:\realMonkey')
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *
#
deviceName='2','c0e17bc7','1','c0e17bc7'
device=rMonkeyRunner(__file__,deviceName)
#
#FLAG.SCREENSHOT = False
device.startActivity('com.dragon.android.pandaspace/com.dragon.android.pandaspace.guid.GuidOneKeyActivity')
#device.click(UIELEMENT.TEXT,'短信')
#device.press('KEYCODE_HOME')
#device.click(UIELEMENT.TEXT,'百度')
#device.press('KEYCODE_HOME')
device.click(UIELEMENT.TEXT,'下载',8)
#device.sleep(1)
#device.startActivity(component="com.baidu.shucheng91/com.baidu.shucheng91.home.ShuCheng")

