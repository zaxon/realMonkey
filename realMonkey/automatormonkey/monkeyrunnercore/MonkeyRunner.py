# -*- coding: utf-8 -*-
'''
    @author xinjiankang|wuqiaomin in 20140414
'''
import time
import inspect, os, sys,shutil
from automatormonkey.monkeyrunnercore.action.Drag import drag
from automatormonkey.monkeyrunnercore.action.Click import click
from automatormonkey.monkeyrunnercore.MonkeyDevice import MonkeyDevice
from automatormonkey.monkeyrunnercore.info.SystemProperty import SystemProperty
from automatormonkey.monkeyrunnercore.MonkeyDevice import MonkeyDevice
from automatormonkey.monkeyrunnercore.UiSelector import UiSelector
from automatormonkey.monkeyrunnercore.info.Enum import *
from automatormonkey.report.reportcoloect import reportcoloect
from automatormonkey.monkeyrunnercore.action.AdbCommand import AdbCommand

class rMonkeyRunner(object) :

    def __init__(self, scriptPath) :
        print 'initializing...'
        
        self.device = MonkeyDevice()
        self.__adbCmd = AdbCommand()
        
        
        self.__reportcoloect = None
        
        INFO.DEVICE = self.__adbCmd.getDeviceSerial()
        INFO.DEVICENAME = self.__adbCmd.getSystemProp('ro.product.model')

        self.__scriptPath = '%s_%s' %(scriptPath[0:len(scriptPath)-3],INFO.DEVICENAME)
        
        self.make_dir(self.__scriptPath)
        self.__reportcoloect = reportcoloect(self.__scriptPath)

        self.__uiselect = UiSelector(self.device)
        self.__systemInfo = SystemProperty(self.__uiselect)
        self.__click = click(self.device, self.__uiselect)
        self.__drag = drag(self.device, self.__systemInfo)
        
        print 'Start Case %s...' % (scriptPath)
    
    def click(self,TAG,value, match=None):
        try:                
            operator = {UIELEMENT.TEXT:lambda:self.__click.text(value, match),
                        UIELEMENT.CLASSNAME:lambda:self.__click.className(value, match),
                        UIELEMENT.INDEX:lambda:self.__click.index(value, match),
                        UIELEMENT.DESC:lambda:self.__click.description(value, match),
                        }
            operator[TAG]()
            self.__record('ClickBy%s_%s'%(TAG,value),'click')

        except Exception , e:
            self.device.takeSnapshot('click', self.__scriptPath)
            self.__reportcoloect.logcolect(picname = INFO.PICNAME,exception=e)
            raise e
        
    def clickMultCondition(self,mtext=None,mclassName=None,mindex=None):
        try:
            self.__click.multCondition(text=mtext,className=mclassName,index=mindex)
            self.__record('clickMultCondition','click')
        except Exception , e:
            self.device.takeSnapshot('click', self.__scriptPath)
            self.__reportcoloect.logcolect(picname = INFO.PICNAME,exception=e)
            raise e
        
    def drag(self,TAG):
        operator = {DIRECTION.UP:lambda:self.__drag.up(),
                    DIRECTION.DOWN:lambda:self.__drag.down(),
                    DIRECTION.LEFT:lambda:self.__drag.left(),
                    DIRECTION.RIGHT:lambda:self.__drag.right(),
                    }
        operator[TAG]()
        self.__record('drag_%s'%(TAG),'drag')

    def install(self,apkPath):
        self.device.installPackage(apkPath)
        self.__record('install %s'%(apkPath), 'install')
    
    def uninstall(self, packageName):
        self.device.removePackage(packageName)
        self.__record('uninstall %s'%(packageName), 'uninstall')
        
    def clickxy(self,x,y):
        self.device.touch(x,y)
        self.__record('clickxy_%s,%s'%(x,y), 'clickxy')
        
    def shell(self,cmd):
        self.device.shell(cmd)
        self.__record('shell_%s'%(cmd), 'shell')
        
    def dragxy(self, x,y,toX,toY,duration=''):
        self.device.drag(x,y,toX,toY,duration)
        self.__record('dragxy_%s,%s,%s,%s'%(x,y,toX,toY),'dragxy')
        
    def input(self,text):
        self.device.input(text)
        self.__record('input_%s'%(text),'input')
    
    def press(self,keycode):
        self.device.press(keycode)
        self.__record('press_%s'%(keycode),'press')
        
    def startActivity(self,component=""):
        self.device.startActivity(component)
        self.__record('startActivity_%s'%(component),'startActivity')

    def sleep(self,s) :
        time.sleep(s)
    
    def __record(self,stepName, picName):
        INFO.STEP += 1
        self.device.takeSnapshot(picName, self.__scriptPath)
        self.__reportcoloect.logcolect(INFO.STEP,stepName,INFO.PICNAME)

    def getProperty(self,TAG):
        operator = {PROPERTY.DISPLAYWIDTH:lambda:self.__systemInfo.displayWidth(),
                    PROPERTY.DISPLAYHEIGHT:lambda:self.__systemInfo.displayHeight(),
                    PROPERTY.CURRENTPACKAGE:lambda:self.__systemInfo.currentPackageName(),
                    }
        operator[TAG]()
    
    def takeSnapshot(self,picName):
        self.device.takeSnapshot(picName, self.__scriptPath)
    
    def make_dir(self,path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                os.mkdir(path)
            else:
                os.mkdir(path)
        except Exception, e:
            pass
                
        
    def __del__(self):
        if self.__reportcoloect != None:
            self.__reportcoloect.logcolect(flag='end')
            print 'End Case...'
        if INFO.PATH != None:  
            if os.path.exists(INFO.PATH):
                os.remove(INFO.PATH)
        
    
