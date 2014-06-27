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

class rMonkeyRunner(object) :

    def __init__(self, scriptPath, devicesList=['1']) :
        print 'initializing...'
        #self.t = time.time()
        INFO.SYSTEM = platform.system()
        if INFO.SYSTEM.find('Windows')>=0:
            INFO.GREP = 'findstr'

        self.device = MonkeyDevice()       
        self.__reportList = []

        self.__devicesList = self.device.getDeviceSerial(devicesList)
        self.__deviceNameList = self.device.getDeviceNameList(self.__devicesList)
        self.__scriptPath = '%s' %(scriptPath[0:len(scriptPath)-3])
        self.__logPathList = self.device.getLogPathList(self.__scriptPath, self.__deviceNameList)

        for i in xrange(len(self.__logPathList)):
            INFO.DEVICE = self.__devicesList[i]
            self.device.clearLog()
            self.__make_dir(self.__logPathList[i])
            temp = reportcoloect(self.__logPathList[i])
            self.__reportList.append(temp)
            
        self.__uiselect = UiSelector(self.device)
        self.__systemInfo = SystemProperty()
        self.__click = click(self.device, self.__uiselect)
        self.__drag = drag(self.device, self.__uiselect, self.__systemInfo)
        print 'Start Case %s...' % (scriptPath)
    
    def drag(self, TAG, duration=''):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            operator = {DIRECTION.UP:lambda:self.__drag.up(),
                        DIRECTION.DOWN:lambda:self.__drag.down(),
                        DIRECTION.LEFT:lambda:self.__drag.left(duration),
                        DIRECTION.RIGHT:lambda:self.__drag.right(duration),
                        }
            operator[TAG]()
            self.__record('drag_%s'%(TAG),'drag',i)

    def install(self,apkPath):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.installPackage(apkPath)
            self.__record('install %s'%(apkPath), 'install',i)
    
    def uninstall(self, packageName):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.uninstallPackage(packageName)
            self.__record('uninstall %s'%(packageName), 'uninstall',i)
        
    def clickxy(self,x,y):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            self.device.touch(x,y)
            self.__record('clickxy_%s,%s'%(x,y), 'clickxy',i)
        
    def shell(self,cmd):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            self.device.shell(cmd)
            self.__record('shell_%s'%(cmd), 'shell',i)
        
    def dragxy(self, x,y,toX,toY,duration=''):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            self.device.drag(x,y,toX,toY,duration)
            self.__record('dragxy_%s,%s,%s,%s'%(x,y,toX,toY),'dragxy',i)
        
    def input(self,text):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
        
            self.device.input(text)
            self.__record('input_%s'%(text),'input',i)
    
    def press(self,keycode):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.press(keycode)
            self.__record('press_%s'%(keycode),'press',i)

    def startActivity(self,component=""):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
    
            self.device.startActivity(component)
            self.__record('startActivity_%s'%(component),'startActivity',i)

    def sleep(self,s):
        time.sleep(s)
    
    def clearAppData(self, packageName):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
        
            self.device.clearAppData(packageName)
    
    def takeSnapshot(self,picName):
        INFO.STEP += 1
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.takeSnapshot(picName, self.__logPathList[i])
            self.__reportList[i].logcolect(INFO.STEP,'takeSnapshot',INFO.PICNAME)
    
    
    def click(self,TAG,value, match=None):
        desc = 'clickBy%s_%s'%(TAG,value)
        func_name = '_rMonkeyRunner__clickOperate'
        self.__multiOperate(func_name, desc, TAG, value, match)

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
    
    def __assertEquals(self, obj, getActual, expected, result):
        actual = getattr(obj ,getActual)()
        assert (actual == expected)==result, \
        '%s:%s==%s expect %s but %s'%(INFO.DEVICENAME,actual,expected,result,not result) 
                    
    def __clickOperate(self,TAG,value, match):
        operator = {UIELEMENT.TEXT:lambda:self.__click.text(value, match),
                    UIELEMENT.CLASSNAME:lambda:self.__click.className(value, match),
                    UIELEMENT.INDEX:lambda:self.__click.index(value, match),
                    UIELEMENT.DESC:lambda:self.__click.description(value, match),
                    }
        operator[TAG]()    

    def __verifyElement(self, TAG, value, match=None):
        self.__getElement(TAG, value, match)
          
    def __getElement(self, TAG, value, match=None):
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
        tempDevices = copy.copy(self.__devicesList)
        tempDeviceName = copy.copy(self.__deviceNameList)
        tempReport = copy.copy(self.__reportList)
        tempLogPath = copy.copy(self.__logPathList)
        for i in xrange(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            try:
                getattr(self, func_name)(*args)
                self.__record(desc,'desc',i)
            except Exception , e:
                self.device.takeSnapshot('desc', self.__logPathList[i])
                info = self.__formatException()      
                self.__reportList[i].logcolect(picname = INFO.PICNAME,exception=info)
                self.__reportList[i].logcolect(flag='end')
                self.device.getLogCat(self.__logPathList[i])
                try:
                    tempDevices.remove(INFO.DEVICE)
                    tempDeviceName.remove(INFO.DEVICENAME)
                    tempReport.remove(self.__reportList[i])
                    tempLogPath.remove(self.__logPathList[i])
                    traceback.print_exc()
                    print '\n'
                except:
                    print '\n'
                    pass
        self.__devicesList = tempDevices 
        self.__deviceNameList = tempDeviceName
        self.__reportList = tempReport
        self.__logPathList = tempLogPath
        
    def __record(self,stepName, picName,index=0):
        self.device.takeSnapshot(picName, self.__logPathList[index])
        self.__reportList[index].logcolect(INFO.STEP,stepName,INFO.PICNAME)
    
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
    
    def __del__(self):
        if self.__reportList != []:
            for i in xrange(len(self.__devicesList)):
                INFO.DEVICE = self.__devicesList[i]
                INFO.DEVICENAME=self.__deviceNameList[i]
                self.__reportList[i].logcolect(flag='end')
                self.device.getLogCat(self.__logPathList[i])
        #print time.time()-self.t
        print 'End Case...'
            
    
    
    
