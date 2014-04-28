# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140421
'''
import os,sys
import subprocess
import time
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
        self.__adbShell(cmd)

    def createDir(self,path):
        '''
        '''
        cmd='mkdir %s'%(path)
        self.__adbShell(cmd)
    
    def touch(self, x, y):
        self.__adbShellInput('tap %s %s'%(x, y))

    def drag(self, x, y, toX, toY, duration=''):
        self.__adbShellInput('swipe %s %s %s %s %s'%(x,y,toX,toY,duration))
    
    def input(self, text):
        self.__adbShellInput('text %s'%(text))
    
    def press(self, keycode):
        self.__adbShellInput('keyevent %s'%(keycode))

    def startActivity(self, component=""):
        self.__adbShell('am start -n %s'%(component))
        
    def takeSnapshot(self, saveName, savePath):
        count=1
        if FLAG.SCREENSHOT == True:
            self.__adbShell('/system/bin/screencap -p /sdcard/temp.png')
            self.pull('/sdcard/temp.png', savePath)
            
            filename = '%s\\temp.png'%(savePath)
            newname = u'%s\\%s.png'%(savePath,saveName)
        while os.path.exists(newname):
            newname = u'%s\\%s_%s.png'%(savePath,saveName,count)
            count += 1
        INFO.PICNAME = newname
        os.rename(filename,newname)  
    
    def getSystemProp(self, value):
        p = self.__adbShell('getprop %s' %(value))
        str = p.stdout.readlines()
        return str[0].split('\r')[0].strip().replace(' ','_')
    
    def installPackage(self,path):
        self.__runshell('adb -s %s install -r %s'%(INFO.DEVICE, path))
    
    def uninstallPackage(self, packageName):
        self.__runshell('adb -s %s uninstall %s'%(INFO.DEVICE, packageName))

    def shell(self,cmd):
        self.__runshell(cmd)
        
    def uidump(self, filePath):
        self.__adbShell('uiautomator dump %s' %(filePath))

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
        self.__adbShell('input %s'%(cmd))
        
    def __adbShell(self, cmd):
        return self.__runshell('adb -s %s shell %s'%(INFO.DEVICE,cmd))

    def getDeviceSerial(self):
        p = self.__runshell('adb devices')
        deviceList = p.stdout.readlines()
        deviceList.pop(len(deviceList)-1)
        deviceList.pop(0)
        for i in deviceList:
            i = i.split('\t')[0]
            INFO.PATH = '%s\\%s' %(self.__path(), i)
            #print INFO.PATH
            if os.path.exists(INFO.PATH) == False:
                f = file(INFO.PATH,'w')
                f.close()
                #print i
                return i
        print 'Please check you have idle device!!!'
        sys.exit(1)
    
    def __path(self):
       path = os.path.realpath(sys.path[2])
       if os.path.isfile(path):
           path = os.path.dirname(path)
       return os.path.abspath(path)

        
        
