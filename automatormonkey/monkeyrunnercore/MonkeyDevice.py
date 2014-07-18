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
        return self.adbCmd.shell(cmd)
    
    def input(self,text):
        self.adbCmd.input(text)
        
    def clearLog(self):
        self.adbCmd.clearLog()
        
    def clearAppData(self, packageName):
        self.adbCmd.clearAppData(packageName)
    
    def getLogCat(self, logPath):
        self.adbCmd.getLogCat(logPath)
    
    def getDeviceSerial(self):
        return self.adbCmd.getDeviceSerial()
    
    def getDeviceName(self):
        return self.adbCmd.getDeviceName()
    
    def getLogPath(self,scriptPath):
        return self.adbCmd.getLogPath(scriptPath)

    def closeApp(self, packageName):
        self.adbCmd.closeApp(packageName)
    
    def getSystemProp(self, value):
        return self.adbCmd.getSystemProp(value)
    