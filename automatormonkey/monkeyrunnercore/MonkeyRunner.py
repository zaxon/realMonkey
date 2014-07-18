# -*- coding: utf-8 -*-
'''
    @author xinjiankang|wuqiaomin in 20140414
'''
import time
import traceback
import copy
import inspect, os, sys,shutil
import platform
from automatormonkey.monkeyrunnercore.action.Drag import drag
from automatormonkey.monkeyrunnercore.action.Click import click
from automatormonkey.monkeyrunnercore.MonkeyDevice import MonkeyDevice
from automatormonkey.monkeyrunnercore.info.SystemProperty import SystemProperty
from automatormonkey.monkeyrunnercore.MonkeyDevice import MonkeyDevice
from automatormonkey.monkeyrunnercore.UiSelector import UiSelector
from automatormonkey.monkeyrunnercore.info.Enum import *
from automatormonkey.report.reportcoloect import reportcoloect
from automatormonkey.monkeyrunnercore.UiAutomator import *

class rMonkeyRunner(object) :

    def __init__(self, scriptPath, devicesList=None) :
        print 'initializing...'
        #self.t = time.time()
        INFO.SYSTEM = platform.system()
        if INFO.SYSTEM.find('Windows')>=0:
            INFO.GREP = 'findstr'
        
        self.device = MonkeyDevice()       
        self.__report = None
        self.uiautomatorDevice=None
        self.device.getDeviceSerial()
        self.device.getDeviceName()
        INFO.DEVICEVERSION = self.__getDevivceSystemVersion()
        self.uiautomatorDevice=UiautomatorDevice()
        self.__scriptPath = '%s' %(scriptPath[0:len(scriptPath)-3])
        self.__logPath = self.device.getLogPath(self.__scriptPath)

        self.device.clearLog()
        self.__make_dir(self.__logPath)
        self.__report = reportcoloect(self.__logPath)
        
        self.__uiselect = UiSelector(self.device)
        self.__systemInfo = SystemProperty()
        self.__click = click(self.device, self.__uiselect)
        self.__drag= drag(self.device, self.__uiselect, self.__systemInfo)
        
        print 'Start Case %s...' % (scriptPath)
    
    def getAllElements(self):
        return self.__uiselect.getAllElements()    
        
    def assertExist(self, TAG, value, match=None, scrollable=False):
        FLAG.SCROLLBALE = scrollable
        desc = 'verifyElementExist:%s_%s'%(TAG,value)
        func_name = '_rMonkeyRunner__verifyElement'
        self.__multiOperate(func_name, desc, TAG, value, match)

    def assertText(self, expectText, TAG, value, match=None):
        desc = 'verifyText:%s_%s\s text equal %s'%(TAG,value,expectText)
        func_name = '_rMonkeyRunner__verifyTexts'
        self.__multiOperate(func_name, desc,expectText, TAG, value, match)
    
    def assertEqual(self,actual, expected, result):
        desc = 'assertEqual:%s==%s'%(actual,expected)
        func_name = '_rMonkeyRunner__assertEquals'
        self.__multiOperate(func_name, desc, actual, 'strip',expected, result)
        
    def assertActivity(self, expected, result):
        desc = 'assertActivity:%s'%(expected)
        func_name = '_rMonkeyRunner__assertEquals'
        self.__multiOperate(func_name, desc, self.__systemInfo, 'currentActivityName', expected, result)
    
    def clearAppData(self, packageName):
        INFO.STEP += 1
        self.device.clearAppData(packageName)
    
    def clearTextField(self,TAG,className,match=None):
        desc = 'clearTextField%s_%s'%(TAG,className)
        func_name = '_rMonkeyRunner__clearTextFieldOperate'
        self.__multiOperate(func_name, desc,TAG,className,match)

    def click(self,TAG,value, match=None):
        desc = 'clickBy%s_%s'%(TAG,value)
        func_name = '_rMonkeyRunner__clickOperate'
        self.__multiOperate(func_name, desc, TAG, value, match)

    def clickAndWaitForNewWindow(self,TAG,value,match,timeout=10):
        timeout = timeout*1000
        desc = 'clickAndWaitForNewWindowBy%s_%s'%(TAG,value)
        func_name = '_rMonkeyRunner__clickAndWaitOperate'
        self.__multiOperate(func_name, desc, TAG, value, match,timeout)

    def clickxy(self,x,y):
        INFO.STEP += 1
        self.device.touch(x,y)
        self.__record('clickxy_%s,%s'%(x,y), 'clickxy')
    
    def closeApp(self, packageName):
        INFO.STEP += 1
        self.__record('closeApp_%s'%(packageName),'closeApp')
        self.device.closeApp(packageName)
    
    def drag(self, TAG, duration=''):
        INFO.STEP += 1
        operator = {DIRECTION.UP:lambda:self.__drag.up(),
                    DIRECTION.DOWN:lambda:self.__drag.down(),
                    DIRECTION.LEFT:lambda:self.__drag.left(duration),
                    DIRECTION.RIGHT:lambda:self.__drag.right(duration),
                    }
        operator[TAG]()
        self.__record('drag_%s'%(TAG),'drag')

    def dragxy(self, x,y,toX,toY,duration=''):
        INFO.STEP += 1
        self.device.drag(x,y,toX,toY,duration)
        self.__record('dragxy_%s,%s,%s,%s'%(x,y,toX,toY),'dragxy')
    
    def dragToEnd(self,TAG,className,match=None,steps=100):
        desc = 'dragToEnd%s_%s'%(TAG,className)
        func_name = '_rMonkeyRunner__dragToEnd'
        self.__multiOperate(func_name, desc, TAG, className, match,True,steps)
       
    def dragToBegin(self,TAG,className,match=None,steps=100):
        desc = 'dragToBegin%s_%s'%(TAG,className)
        func_name = '_rMonkeyRunner__dragToBegin'
        self.__multiOperate(func_name, desc, TAG, className, match,True,steps)

    def getClassName(self, TAG, value, match=None):
        return self.__getElement(TAG, value, match).getClassName()
    
    def getCurrentActivityName(self):
        INFO.STEP += 1
        self.__record('getCurrentActivityName','getCurrentActivityName')
        return self.__systemInfo.currentActivityName()
    
    def getElement(self, TAG, value, match=None):
        return self.__getElement(TAG, value, match)

    def getElements(self, TAG, value):
        return self.__getElements(TAG,value)

    def getSystemProperty(self, key):
        return self.device.getSystemProp(key)
    
    def getText(self, TAG, value, match=None):
        return self.__getElement(TAG, value, match).getText()
    
    def getXY(self, TAG, value, match=None):
        return self.__getElement(TAG, value, match).getXY()

    def input(self,text,TAG=None,className=None,match=None):
        if TAG==None or className==None:
            INFO.STEP += 1
            self.device.input(text)
            self.__record('input_%s'%(text),'input')
        else:
            desc = 'input%s_%s'%(TAG,className)
            func_name = '_rMonkeyRunner__editTextOperate'
            self.__multiOperate(func_name, desc, TAG, className, match,text)
    
    def install(self,apkPath):
        INFO.STEP += 1
        self.device.installPackage(apkPath)
        self.__record('install %s'%(apkPath), 'install')

    def longclick(self,TAG,value, match=None):
        desc = 'longclickBy%s_%s'%(TAG,value)
        func_name = '_rMonkeyRunner__longclickOperate'
        self.__multiOperate(func_name, desc, TAG, value, match) 
    
    def press(self,keycode):
        INFO.STEP += 1
        self.device.press(keycode)
        self.__record('press_%s'%(keycode),'press')
        
    def shell(self,cmd):
        INFO.STEP += 1
        sub = self.device.shell(cmd)
        self.__record('shell_%s'%(cmd), 'shell')
        return sub

    def sleep(self,s):
        time.sleep(s)

    def startActivity(self,component=''):
        desc = 'startActivity_%s'%(component)
        func_name = '_rMonkeyRunner__startActivity'
        self.__multiOperate(func_name, desc, component) 

    def swipe(self,dir,TAG,className,match,speed=10):
        desc = 'swipe%s_%s'%(TAG,className)
        func_name = '_rMonkeyRunner__swipeOperate'
        self.__multiOperate(func_name, desc, TAG, className, match,dir,speed) 
    
    def takeScreenshot(self,picName):
        INFO.STEP += 1
        self.device.takeSnapshot(picName, self.__logPath)
        self.__report.logcolect(INFO.STEP,'takeSnapshot',INFO.PICNAME) 
    
    def uninstall(self, packageName):
        INFO.STEP += 1
        self.device.uninstallPackage(packageName)
        self.__record('uninstall %s'%(packageName), 'uninstall')

    def wakeUp(self):
        INFO.STEP += 1
        self.uiautomatorDevice.wakeUp()
        self.__record('wakeUp','wakeUp')
    
    def isScreenOn(self):
        INFO.STEP += 1
        self.uiautomatorDevice.isScreenOn()
        self.__record('isScreenOn','isScreenOn') 

    def __getElement(self, TAG, value, match):
        desc = 'getElement_%s_%s'%(TAG,value)
        func_name = '_rMonkeyRunner__getElementOperate'
        return self.__multiOperate(func_name, desc, TAG, value, match)  
    
    def __getElements(self, TAG, value):
        desc = 'getElementsList_%s_%s'%(TAG,value)
        func_name = '_rMonkeyRunner__getElementsOperate'
        return self.__multiOperate(func_name, desc, TAG, value)  

    def __getElementsOperate(self, TAG, value):
        operator = {UIELEMENT.TEXT:lambda:self.__uiselect.getElementList('text',value),
                    UIELEMENT.CLASSNAME:lambda:self.__uiselect.getElementList('class', value),
                    UIELEMENT.INDEX:lambda:self.__uiselect.getElementList('index', value),
                    UIELEMENT.DESC:lambda:self.__uiselect.getElementList('content-desc', value),
                    UIELEMENT.SID:lambda:self.__uiselect.getElementList('resource-id', value),
                    UIELEMENT.ENABLE:lambda:self.__uiselect.getElementList('enabled', value)        
                    }
        return operator[TAG]()    
    
    def __getElementOperate(self,TAG, value, match):
        operator = {UIELEMENT.TEXT:lambda:self.__uiselect.text(value, match),
                    UIELEMENT.CLASSNAME:lambda:self.__uiselect.className(value, match),
                    UIELEMENT.INDEX:lambda:self.__uiselect.index(value, match),
                    UIELEMENT.DESC:lambda:self.__uiselect.description(value, match),
                    UIELEMENT.SID:lambda:self.__uiselect.sid(value, match),
                    }
        return operator[TAG]()

    def __verifyTexts(self, expectText, TAG, value, match=None):
        element = self.__getElement(TAG,value,match)
        elemenetText = element.getText()
        assert expectText==elemenetText,'this element\'s text %s!=%s in %s\' screen'%(elemenetText,expectText, INFO.DEVICENAME)
    
    def __multiOperate(self,func_name, desc, *args):
        INFO.STEP += 1
        try:
            value = getattr(self, func_name)(*args)
            self.__record(desc,'desc')
            return value
        except Exception , e:
            self.device.takeSnapshot('desc', self.__logPath)
            info = self.__formatException()      
            self.__report.logcolect(picname = INFO.PICNAME,exception=info)
            self.__report.logcolect(flag='end')
            raise

    def __record(self,stepName, picName):
        self.device.takeSnapshot(picName, self.__logPath)
        self.__report.logcolect(INFO.STEP,stepName,INFO.PICNAME)
    
    def __make_dir(self,path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                os.mkdir(path)
            else:
                os.mkdir(path)
        except Exception, e:
            pass
                    
    def __formatException(self):
        type,value,tb = sys.exc_info()
        info = traceback.format_exception_only(type,value)
        track = traceback.format_tb(tb)
        strInfo = ''
        strTrack = ''
        for i in info:
            strInfo += '%s<br><br>'%(i)
        for i in track:
            strTrack += '%s<br>'%(i)
        return '%s\n%s'%(strInfo,strTrack)
        
    def __startActivity(self, component):
        subString=component.split('/')
        PROPERTY.CURRENTPACKAGE=subString[0]
        self.device.startActivity(component)
    
    def __longclickOperate(self,TAG,value, match):
        operator = {
                    UIELEMENT.CLASSNAME:lambda:self.uiautomatorDevice.longByClass(value, match),
                    UIELEMENT.TEXT:lambda:self.uiautomatorDevice.longByText(value, match),
                    }
        operator[TAG]() 

    def __swipeOperate(self,TAG,className,match,dir,speed):
        operator={
                UIELEMENT.CLASSNAME:lambda:self.uiautomatorDevice.swipe(className,match,dir,speed)
                }
        operator[TAG]()

    def __editTextOperate(self,TAG,className,match,text):
        operator={
                 UIELEMENT.CLASSNAME:lambda:self.uiautomatorDevice.setText(className,match,text)
                }
        operator[TAG]()

    def __clickAndWaitOperate(self,TAG,value, match,timeout):
        operator = {UIELEMENT.TEXT:lambda:self.uiautomatorDevice.text(value, match,timeout),
                    UIELEMENT.CLASSNAME:lambda:self.uiautomatorDevice.className(value, match,timeout),
                    }
        operator[TAG]() 

    def __clearTextFieldOperate(self,TAG,className,match):
        operator={
                UIELEMENT.CLASSNAME:lambda:self.uiautomatorDevice.clearTextField(className,match)
                }
        operator[TAG]() 

    def __assertEquals(self, obj, getActual, expected, result):
        actual = getattr(obj ,getActual)()
        assert (actual == expected)==result, \
        '%s:%s==%s expect %s but %s'%(INFO.DEVICENAME,actual,expected,result,not result) 
                    
    def __clickOperate(self,TAG,value, match):
        operator = {UIELEMENT.TEXT:lambda:self.__click.text(value, match),
                    UIELEMENT.CLASSNAME:lambda:self.__click.className(value, match),
                    UIELEMENT.INDEX:lambda:self.__click.index(value, match),
                    UIELEMENT.DESC:lambda:self.__click.description(value, match),
                    UIELEMENT.SID:lambda:self.__click.sid(value, match),
                    }
        operator[TAG]()    

    def __verifyElement(self, TAG, value, match=None):
        self.__getElement(TAG, value, match)

    def __dragToEnd(self, TAG, className, match, isVertical, steps):
        operator = {UIELEMENT.CLASSNAME:lambda:\
                    self.uiautomatorDevice.flingToEnd(className,match,isVertical,steps),
                   }
        operator[TAG]()
        
    def __dragToBegin(self, TAG, className, match, isVertical, steps):
        operator = {UIELEMENT.CLASSNAME:lambda:\
                    self.uiautomatorDevice.flingToBeginning(className,match,isVertical,steps),
                   }
        operator[TAG]()

    def __getDevivceSystemVersion(self):
        tempList = self.device.getSystemProp('ro.build.version.release').split('.')
        version = ''
        versionNum = int(version.join(tempList))
        if versionNum < 100:
            versionNum *= 10
        return versionNum
        
    def __del__(self):
        if self.uiautomatorDevice != None:
            self.uiautomatorDevice.stop()
        if self.__report != None:
            self.__report.logcolect(flag='end')
            self.device.getLogCat(self.__logPath)
        #print time.time()-self.t
        print 'End Case...'
