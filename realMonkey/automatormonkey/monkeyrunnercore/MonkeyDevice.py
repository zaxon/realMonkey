# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140414
'''
from automatormonkey.monkeyrunnercore.action.AdbCommand import AdbCommand
from automatormonkey.monkeyrunnercore.info.Enum import *

class MonkeyDevice(object):
    def __init__(self):
        self.adbCmd = AdbCommand()
    
    def press(self,keycode):
        self.adbCmd.press(keycode)
        
    def touch(self, x, y):
        self.adbCmd.touch(x,y)

    def drag(self, x, y, toX, toY, duration=''):
        self.adbCmd.drag(x, y, toX, toY, duration)
    
    def startActivity(self, component=''):
        self.adbCmd.startActivity(component)
    
    def takeSnapshot(self, fileName, pathName):
        self.adbCmd.takeSnapshot(fileName, pathName)
    
    def installPackage(self, path):
        self.adbCmd.installPackage(path)
    
    def uninstallPackage(self, packageName):
        self.adbCmd.uninstallPackage(packageName)
        
    def shell(self, cmd):
        self.adbCmd.shell(cmd)
    
    def input(self,text):
        self.adbCmd.input(text)
        
    