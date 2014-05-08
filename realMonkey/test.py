# -*- coding: utf-8 -*-

import os,sys
sys.path.append(r'E:\realMonkey')
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *
device=rMonkeyRunner(__file__)

device.click(UIELEMENT.CLASSNAME,'android.widget.TextView',0)
device.sleep(1)











