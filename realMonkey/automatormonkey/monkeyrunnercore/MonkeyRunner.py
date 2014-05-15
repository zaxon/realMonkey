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
from automatormonkey.monkeyrunnercore.action.AdbCommand import AdbCommand

class rMonkeyRunner(object) :

    def __init__(self, scriptPath, devicesList='1') :
        print 'initializing...'
        self.t = time.time()
        INFO.SYSTEM = platform.system()
        if INFO.SYSTEM.find('Windows')>=0:
            INFO.GREP = 'findstr'

        self.device = MonkeyDevice()
        self.__adbCmd = AdbCommand()        
        self.__reportList = []

        self.__devicesList = self.__adbCmd.getDeviceSerial(devicesList)
        self.__deviceNameList = self.__adbCmd.getDeviceNameList(self.__devicesList)
        self.__scriptPath = '%s' %(scriptPath[0:len(scriptPath)-3])
        self.__logPathList = self.__adbCmd.getLogPathList(self.__scriptPath, self.__deviceNameList)
        
        for i in self.__logPathList:
            self.make_dir(i)
            temp = reportcoloect(i)
            self.__reportList.append(temp)
            
        self.__uiselect = UiSelector(self.device)
        self.__systemInfo = SystemProperty(self.__adbCmd)
        self.__click = click(self.device, self.__uiselect)
        self.__drag = drag(self.device, self.__uiselect,self.__systemInfo)
        print 'Start Case %s...\n' % (scriptPath)
    
    def click(self,TAG,value, match=None):
        INFO.STEP += 1
        tempDevices = copy.copy(self.__devicesList)
        tempDeviceName = copy.copy(self.__deviceNameList)
        tempReport = copy.copy(self.__reportList)
        tempLogPath = copy.copy(self.__logPathList)
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            try:
                operator = {UIELEMENT.TEXT:lambda:self.__click.text(value, match),
                            UIELEMENT.CLASSNAME:lambda:self.__click.className(value, match),
                            UIELEMENT.INDEX:lambda:self.__click.index(value, match),
                            UIELEMENT.DESC:lambda:self.__click.description(value, match),
                            }
                operator[TAG]()
                self.__record('ClickBy%s_%s'%(TAG,value),'click',i)
            except Exception , e:
                self.device.takeSnapshot('click', self.__logPathList[i])
                self.__reportList[i].logcolect(picname = INFO.PICNAME,exception=traceback.format_exc())
                self.__reportList[i].logcolect(flag='end')
                try:
                    tempDevices.remove(INFO.DEVICE)
                    tempDeviceName.remove(INFO.DEVICENAME)
                    tempReport.remove(self.__reportList[i])
                    tempLogPath.remove(self.__logPathList[i])
                    traceback.print_exc()
                except:
                    print '\n'
                    pass
        self.__devicesList = tempDevices 
        self.__deviceNameList = tempDeviceName
        self.__reportList = tempReport
        self.__logPathList = tempLogPath

    def drag(self,TAG):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            operator = {DIRECTION.UP:lambda:self.__drag.up(),
                        DIRECTION.DOWN:lambda:self.__drag.down(),
                        DIRECTION.LEFT:lambda:self.__drag.left(),
                        DIRECTION.RIGHT:lambda:self.__drag.right(),
                        }
            operator[TAG]()
            self.__record('drag_%s'%(TAG),'drag',i)

    def install(self,apkPath):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.installPackage(apkPath)
            self.__record('install %s'%(apkPath), 'install',i)
    
    def uninstall(self, packageName):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.uninstallPackage(packageName)
            self.__record('uninstall %s'%(packageName), 'uninstall',i)
        
    def clickxy(self,x,y):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            self.device.touch(x,y)
            self.__record('clickxy_%s,%s'%(x,y), 'clickxy',i)
        
    def shell(self,cmd):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            self.device.shell(cmd)
            self.__record('shell_%s'%(cmd), 'shell',i)
        
    def dragxy(self, x,y,toX,toY,duration=''):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            self.device.drag(x,y,toX,toY,duration)
            self.__record('dragxy_%s,%s,%s,%s'%(x,y,toX,toY),'dragxy',i)
        
    def input(self,text):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
        
            self.device.input(text)
            self.__record('input_%s'%(text),'input',i)
    
    def press(self,keycode):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.press(keycode)
            self.__record('press_%s'%(keycode),'press',i)
            
    def startActivity(self,component=""):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            self.device.startActivity(component)
            self.__record('startActivity_%s'%(component),'startActivity',i)

    def sleep(self,s):
        time.sleep(s)
    
    def assertExist(self, TAG, value,scrollable=True):
        INFO.STEP += 1
        tempDevices = copy.copy(self.__devicesList)
        tempDeviceName = copy.copy(self.__deviceNameList)
        tempReport = copy.copy(self.__reportList)
        tempLogPath = copy.copy(self.__logPathList)
        
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            try:                
                FLAG.SCROLLBALE = scrollable 
                operator = {UIELEMENT.TEXT:lambda:self.__uiselect.text(value),
                            UIELEMENT.CLASSNAME:lambda:self.__uiselect.className(value),
                            UIELEMENT.INDEX:lambda:self.__uiselect.index(value),
                            UIELEMENT.DESC:lambda:self.__uiselect.description(value),
                            UIELEMENT.SID:lambda:self.__uiselect.sid(value),
                            }
                operator[TAG]()
                self.__record('assertExsit%s_%s SCROLLABLE:%s'%(TAG,value,scrollable),'assertExist',i)

            except Exception , e:
                self.device.takeSnapshot('assertExist', self.__scriptPath)
                self.__reportList[i].logcolect(picname = INFO.PICNAME,exception='assert:%s'%(e))
                self.__reportList[i].logcolect(flag='end')
                try:
                    tempDevices.remove(INFO.DEVICE)
                    tempDeviceName.remove(INFO.DEVICENAME)
                    tempReport.remove(self.__reportList[i])
                    tempLogPath.remove(self.__logPathList[i])
                    traceback.print_exc()
                except:
                    pass
        self.__devicesList = tempDevices 
        self.__deviceNameList = tempDeviceName
        self.__reportList = tempReport
        self.__logPathList = tempLogPath
                
                
 
    def __record(self,stepName, picName,index=0):
        self.device.takeSnapshot(picName, self.__logPathList[index])
        self.__reportList[index].logcolect(INFO.STEP,stepName,INFO.PICNAME)

    def getProperty(self,TAG):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]

            operator = {PROPERTY.DISPLAYWIDTH:lambda:self.__systemInfo.displayWidth(),
                        PROPERTY.DISPLAYHEIGHT:lambda:self.__systemInfo.displayHeight(),
                        PROPERTY.CURRENTPACKAGE:lambda:self.__systemInfo.currentActivityName(),
                        }
            operator[TAG]()
    
    def takeSnapshot(self,picName):
        INFO.STEP += 1
        for i in range(len(self.__devicesList)):
            INFO.DEVICE = self.__devicesList[i]
            INFO.DEVICENAME=self.__deviceNameList[i]
            self.device.takeSnapshot(picName, self.__logPathList[i])
            self.__reportList[index].logcolect(INFO.STEP,'takeSnapshot',INFO.PICNAME)
    
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
        if self.__reportList != []:
            for i in range(len(self.__devicesList)):
                INFO.DEVICE = self.__devicesList[i]
                INFO.DEVICENAME=self.__deviceNameList[i]
                self.__reportList[i].logcolect(flag='end')
        print time.time()-self.t
        print '\n\nEnd Case...'
        
    
