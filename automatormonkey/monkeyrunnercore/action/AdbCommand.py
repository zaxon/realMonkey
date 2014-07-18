# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140421
'''
import os,sys,tempfile
import subprocess
import time
import argparse
from automatormonkey.monkeyrunnercore.info.Enum import *
from automatormonkey.monkeyrunnercore.UiAutomator import *


reload(sys)
sys.setdefaultencoding('utf8')
class AdbCommand(object):
    def __init__(self):
        self.uiautomatorDevice=None
        
    def pull(self, fromPath, toPath=""):
        '''
        '''
        cmd = 'adb -s %s pull %s %s'%(INFO.DEVICE, fromPath,toPath)
        self.__runshell(cmd)
        
    def push(self, fromPath, toPath):
        '''
        '''
        cmd = 'adb -s %s push %s %s' %(INFO.DEVICE,fromPath,toPath)
        self.__runshell(cmd)
    
    def delete(self,filePath):
        '''
        '''
        cmd = 'rm %s' %(filePath)
        self.adbShell(cmd)

    def createDir(self,path):
        '''
        '''
        cmd='mkdir %s'%(path)
        self.adbShell(cmd)
        
    def clearAppData(self, packageName):
        sub = self.adbShell('pm list package|%s %s'%(INFO.GREP,packageName))
        if len(sub.stdout.read())==0:
            return
        self.adbShell('pm clear %s'%(packageName))
    
    def touch(self, x, y):
        self.__adbShellInput('tap %s %s'%(x, y))

    def drag(self, x, y, toX, toY, duration=''):
        self.__adbShellInput('swipe %s %s %s %s %s'%(x,y,toX,toY,duration))
    
    def input(self, text):
        self.__adbShellInput('text %s'%(text))
    
    def press(self, keycode):
        self.__adbShellInput('keyevent %s'%(keycode))

    def startActivity(self, component=""):
        cmd = 'adb -s %s shell am start -n %s'%(INFO.DEVICE, component)
        sub = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while(1):
            strTemp = sub.stdout.read()
            ret1 = subprocess.Popen.poll(sub)
            if ret1 != None:
                return
            if len(strTemp)==0:
                time.sleep(0.2)
            elif strTemp.find('Error')>0:
                raise AttributeError('Error: %s component not found!'%(component)) 
            
    def closeApp(self, packageName):
        self.adbShell('am force-stop %s'%(packageName))
        
    def takeSnapshot(self, saveName, savePath):
        count=1
        if FLAG.SCREENSHOT == True:
            #if INFO.DEVICEVERSION < 420:
            self.adbShell('/system/bin/screencap -p /sdcard/temp.png')
            self.pull('/sdcard/temp.png', savePath)
#            else:
#                self.uiautomatorDevice.takeScreenshot('temp.png',0.5,10)
#                self.pull('/data/local/tmp/temp.png', savePath)
            filename = '%s%stemp.png'%(savePath,os.sep)
            picname = '%s.png'%(saveName)
            newname = u'%s%s%s.png'%(savePath,os.sep,saveName)
            while os.path.exists(newname):
                newname = u'%s%s%s_%s.png'%(savePath,os.sep,saveName,count)
                picname = '%s_%s.png'%(saveName,count)
                count += 1
            INFO.PICNAME = picname
            os.rename(filename,newname)  
    
    def getSystemProp(self, value):
        p = self.adbShell('getprop %s' %(value))
        str = p.stdout.readlines()
        return str[0].split('\r')[0].strip().replace(' ','_')
    
    def installPackage(self,path):
        p = self.__runshell('adb -s %s install -r %s'%(INFO.DEVICE, path))
        print p.stdout.readlines(),p.stderr.readlines()
    
    def uninstallPackage(self, packageName):
        self.__runshell('adb -s %s uninstall %s'%(INFO.DEVICE, packageName))

    def shell(self,cmd):
        return self.__runshell(cmd)
        
    def uidump(self, filePath):
        self.adbShell('uiautomator dump %s' %(filePath))
   
    def adbShell(self, cmd):
        return self.__runshell('adb -s %s shell %s'%(INFO.DEVICE,cmd))
        
    def getDeviceSerial(self):
        '''
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', action='store',dest='device_serial')
        results = parser.parse_args()   
        if results.device_serial:
            p = self.__runshell('adb -s %s shell assertid' %(results.device_serial))
            info = p.stdout.read()
            if info.find('assertid: not found')<0:
                print 'device %s not found or device offline' %(results.device_serial)
                sys.exit(1)
            INFO.DEVICE = results.device_serial
        else:
            p = self.__runshell('adb devices')
            infoList = p.stdout.readlines()
            infoList.pop(len(infoList)-1)
            length = len(infoList)
            for i in xrange(length):
                if infoList[0].find('List of devices') < 0:
                    infoList.pop(0)
                else:
                    infoList.pop(0)
                    break
            deviceLen = len(infoList)
            if deviceLen <= 0:
                print 'device not found'
                sys.exit(1)
            for i in xrange(deviceLen):
                if infoList[i].find('device') >= 0:
                    INFO.DEVICE = infoList[i].split('\t')[0]
                    break
            if INFO.DEVICE == None:
                print 'devices offline'
                sys.exit(1)
        self.uiautomatorDevice=UiautomatorDevice()
                    
    
    def getLogCat(self, logPath):
        path = '%s%slog.txt'%(logPath,os.sep)
        self.adbShell('logcat -v time -d %s:I *:W > %s'%((PROPERTY.CURRENTPACKAGE,path)))
    
    def getDeviceName(self):
        '''
        '''
        if INFO.DEVICE == None:
            print 'device serial is null'
            sys.exit(1)
        INFO.DEVICENAME = self.getSystemProp('ro.product.model')


    def clearLog(self):
        self.adbShell('logcat -c')

    def getLogPath(self,scriptPath):
        '''
        '''
        logPath = '%s_%s'%(scriptPath, INFO.DEVICENAME)
        return logPath
      
    def __deletefiles(self,src):
        '''delete files and folders'''
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                pass
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc=os.path.join(src,item)
                delete_file_folder(itemsrc) 
            try:
                os.rmdir(src)
            except:
                pass

    def __path(self):
        return tempfile.gettempdir()
        '''
        path = os.path.realpath(sys.path[2])
        print sys.path
        if os.path.isfile(path):
            path = os.path.dirname(path)
        return os.path.abspath(path)
        '''
        
    def __runshell(self,cmd):
        print cmd
        sub2 = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while 1:
          ret1 = subprocess.Popen.poll(sub2)
          if ret1 == 0:
              #print sub2.pid,'end'
              break
          elif ret1 is None:
              #print  'running'
              time.sleep(0.2)
          else:
              #print sub2.pid,'term'
              break
        return sub2

    def __adbShellInput(self,cmd):
        return self.adbShell('input %s'%(cmd))
           
    
