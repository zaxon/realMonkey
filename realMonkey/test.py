# -*- coding: utf-8 -*-

import os,sys
sys.path.append(r'E:\realMonkey')
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *
device=rMonkeyRunner(__file__)

device.press('KEYCODE_HOME')
device.sleep(1.0)
device.click(UIELEMENT.DESC, '全部应用程序')
device.click(UIELEMENT.TEXT, '设置')
device.click(UIELEMENT.TEXT, '应用程序')
device.click(UIELEMENT.TEXT, '91熊猫看书')
device.click(UIELEMENT.TEXT, '清除数据')
device.click(UIELEMENT.TEXT, '确定')
device.sleep(1.0)

device.startActivity(component="com.nd.android.pandareader/com.nd.android.pandareader.home.Pandareader")
device.sleep(4.0)
device.dragxy(864, 960, 108, 960)
device.drag(DIRECTION.LEFT)
device.click(UIELEMENT.CLASSNAME,'android.widget.Button')
device.click(UIELEMENT.TEXT,'稍后')
device.click(UIELEMENT.CLASSNAME,'android.widget.ImageView')
device.click(UIELEMENT.CLASSNAME,'android.widget.RelativeLayout', 3)
LIST.VERTICAL=False
device.click('Text','下载')
device.click('Text','抢先下载')
device.click('ClassName','android.widget.EditTexts')
device.input('bird')

