# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140417
'''
from automatormonkey.monkeyrunnercore.info.Enum import *
class SystemProperty(object):

    def __init__(self, adbCmd):
        self.adbCmd = adbCmd

    def currentActivityName(self):
        sub = self.adbCmd.adbShell('dumpsys window -a|%s mCurrentFocus'%(INFO.GREP))
        strTemp = sub.stdout.readlines()
        strTemp = strTemp[len(strTemp)-1].split('=')[1]
        strTemp = strTemp.split(' ')
        strTemp = strTemp[len(strTemp)-1].split('}')[0]
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
        