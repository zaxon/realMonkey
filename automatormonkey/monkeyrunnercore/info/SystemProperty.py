# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140417
'''
from automatormonkey.monkeyrunnercore.info.Enum import *
from automatormonkey.monkeyrunnercore.action.AdbCommand import AdbCommand
import time
class SystemProperty(object):

    def __init__(self):
        self.adbCmd = AdbCommand()

    def currentActivityName(self):
        sub = self.adbCmd.adbShell('dumpsys window -a|%s mCurrentFocus'%(INFO.GREP))
        strList = sub.stdout.readlines()
        strTemp = strList[len(strList)-1]
        if strTemp.find('/')<0:
            return ''
        strTemp = strTemp.split('/')[1]
        strTemp = strTemp.split('}')[0]
        strTemp = strTemp.split(' ')[0]
        return strTemp
        
    def displayWidth(self):
        x,y = self.getDisplay().split('x')
        if int(x) > int(y):
            return y
        return x

    def displayHeight(self):
        x,y = self.getDisplay().split('x')
        if int(x) > int(y):
            return x
        return y
    
    
    def getDisplay(self):
        sub = self.adbCmd.adbShell('dumpsys window|%s init'%(INFO.GREP))
        strTemp = sub.stdout.readline()
        strTemp = strTemp.split('=')[1]
        strTemp = strTemp.split(' ')[0]
        return strTemp.strip()
        