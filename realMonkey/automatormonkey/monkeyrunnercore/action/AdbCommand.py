# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140421
'''
import os,sys,tempfile
import subprocess
import time
import argparse
from automatormonkey.monkeyrunnercore.info.Enum import *

reload(sys)
sys.setdefaultencoding('utf8')
class AdbCommand(object):

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
    
    def touch(self, x, y):
        self.__adbShellInput('tap %s %s'%(x, y))

    def drag(self, x, y, toX, toY, duration=''):
        self.__adbShellInput('swipe %s %s %s %s %s'%(x,y,toX,toY,duration))
    
    def input(self, text):
        self.__adbShellInput('text %s'%(text))
    
    def press(self, keycode):
        self.__adbShellInput('keyevent %s'%(keycode))

    def startActivity(self, component=""):
        self.adbShell('am start -n %s'%(component))
        
    def takeSnapshot(self, saveName, savePath):
        count=1
        if FLAG.SCREENSHOT == True:
            self.adbShell('/system/bin/screencap -p /sdcard/temp.png')
            self.pull('/sdcard/temp.png', savePath)
            
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
        self.__runshell('adb -s %s install -r %s'%(INFO.DEVICE, path))
    
    def uninstallPackage(self, packageName):
        self.__runshell('adb -s %s uninstall %s'%(INFO.DEVICE, packageName))

    def shell(self,cmd):
        return self.__runshell(cmd)
        
    def uidump(self, filePath):
        self.adbShell('uiautomator dump %s' %(filePath))

    def __runshell(self,cmd):
        #print cmd
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
        # print time.time()
        return sub2

    def __adbShellInput(self,cmd):
        return self.adbShell('input %s'%(cmd))
        
    def adbShell(self, cmd):
        return self.__runshell('adb -s %s shell %s'%(INFO.DEVICE,cmd))

#    def _getDeviceSerial(self):
#        p = self.__runshell('adb devices')
#        deviceList = p.stdout.readlines()
#        deviceList.pop(len(deviceList)-1)
#        deviceList.pop(0)
#        for i in deviceList:
#            i = i.split('\t')[0]
#            INFO.PATH = '%s%s%s' %(self.__path(),os.sep,i)
#            #print INFO.PATH
#            if os.path.exists(INFO.PATH) == False:
#                f = file(INFO.PATH,'w')
#                f.close()
#                #print i
#                return i
#        print 'Please check you have idle device!!!'
#        sys.exit(1)
        
    def getDeviceSerial(self, devices):
        '''
        '''
        p = self.__runshell('adb devices')
        deviceList = p.stdout.readlines()
        deviceList.pop(len(deviceList)-1)
        deviceList.pop(0)
        if len(deviceList)== 0:
            print 'device not found'
            sys.exit(1)
        deviceTemp = []
        for i in deviceList:
            if i.find('device')>=0:
                deviceTemp.append(i.split('\t')[0].strip())
        deviceList = deviceTemp
        serialList = []
        tempList = list(set(devices))
        for i in tempList:
            if len(i)==1:
                if int(i)<=len(deviceList):
                    serialList.append(deviceList[int(i)-1])
                continue
            for j in deviceList:
                j = j.split('\t')[0].strip()
                if j==i.strip():
                    serialList.append(j)
                    break
        if len(serialList)==0:
            print 'device not found or device offline'
            sys.exit(1)
        serialList = list(set(serialList))
        return serialList
      
    def getDeviceNameList(self, devicesList):
        '''
        '''
        deviceNameList = []
        for i in devicesList:
            INFO.DEVICE = i
            deviceNameList.append(self.getSystemProp('ro.product.model'))
        return deviceNameList

    def getLogPathList(self,scriptPath, devicesNameList):
        '''
        '''
        logList = []
        for i in devicesNameList:
            logList.append('%s_%s'%(scriptPath, i))
        return logList
      
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
        
        
