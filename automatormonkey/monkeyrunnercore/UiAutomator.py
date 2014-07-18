import os
import subprocess
import time
import itertools
import tempfile
import json
import hashlib
import socket
import re
import urllib2
import inspect
from automatormonkey.monkeyrunnercore.info.Enum import *

class Selector(dict):

    __fields = {
        "text": (0x01, None),
        "textContains": (0x02, None),
        "textMatches": (0x04, None), 
        "textStartsWith": (0x08, None),
        "className": (0x10, None), 
        "classNameMatches": (0x20, None), 
        "description": (0x40, None), 
        "descriptionContains": (0x80, None),
        "descriptionMatches": (0x0100, None), 
        "descriptionStartsWith": (0x0200, None),
        "checkable": (0x0400, False), 
        "checked": (0x0800, False),
        "clickable": (0x1000, False),
        "longClickable": (0x2000, False), 
        "scrollable": (0x4000, False), 
        "enabled": (0x8000, False), 
        "focusable": (0x010000, False), 
        "focused": (0x020000, False), 
        "selected": (0x040000, False), 
        "packageName": (0x080000, None),  
        "packageNameMatches": (0x100000, None), 
        "resourceId": (0x200000, None),
        "resourceIdMatches": (0x400000, None),
        "index": (0x800000, 0),  
        "instance": (0x01000000, 0) 
    }
    __mask = "mask"

    def __init__(self, **kwargs):
        super(Selector, self).__setitem__(self.__mask, 0)
        for k in kwargs:
            self[k] = kwargs[k]

    def __setitem__(self, k, v):
        if k in self.__fields:
            super(Selector, self).__setitem__(k, v)
            super(Selector, self).__setitem__(self.__mask, self[self.__mask] | self.__fields[k][0])
        else:
            raise ReferenceError("%s is not allowed." % k)

    def __delitem__(self, k):
        if k in self.__fields:
            super(Selector, self).__delitem__(k)
            super(Selector, self).__setitem__(self.__mask, self[self.__mask] & ~self.__fields[k][0])

class exception(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Exception: %s" % (self.message)

class UiautomatorDevice(object):

    __instance = None
    device=None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance=super(UiautomatorDevice,cls).__new__(cls)
            cls.device=UiautomatorServer()
            cmd1="forward tcp:%d tcp:9008"%(cls.device.local_port)
            cls.__instance.__runshell('adb -s %s %s'%(INFO.DEVICE,cmd1)).wait()
        return object.__new__(cls)

    def __runshell(self,cmd):
        sub2 = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return sub2   

    def method(self,method,uiselector=None,url=None):
        self.url=url
        data = {"jsonrpc": "2.0", "method": method, "id": 1}
        data["params"] = uiselector
        time.sleep(0.1)
        req = urllib2.Request(self.url,json.dumps(data).encode("utf-8"),{"Content-type": "application/json"})
        result=urllib2.urlopen(req, timeout=90)
        jsonresult = json.loads(result.read().decode("utf-8"))
        result.close()
        if "error" in jsonresult and jsonresult["error"]:
            message=jsonresult["error"]["data"]["message"][10:]
            message=message.encode("utf-8")
            message=message[1:(len(message)-1)].split(",")[0].split("=")
            raise AttributeError('%s %s is not found in %s\'s current screen'%(message[0].lower(),message[1],INFO.DEVICENAME))
        return jsonresult["result"]

    def setText(self,className,instance,text):
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=instance))
        self.method('setText',[selector,text],self.url)
        self.stop()

    def getText(self,className,instance):
        self.url=self.device.start()
        selector=[dict(Selector(className=className,instance=instance))]
        self.method('getText',selector,self.url)
        self.stop()

    def clearTextField(self,className,instance):
        self.url=self.device.start() 
        selector=dict(Selector(className=className,instance=instance))
        self.method('clearTextField',[selector],self.url)
        self.stop()

    def longByClass(self,className,instance=None):
        self.url=self.device.start()  
        selector=[dict(Selector(className=className,instance=instance))]
        self.method('longClick',selector,self.url)
        self.stop()

    def longByText(self,text, instance=None):
        self.url=self.device.start() 
        selector=[dict(Selector(text=text,instance=instance))]
        self.method('longClick',selector,self.url)
        self.stop()

    def getChildCount(self,className,instance):
        self.url=self.device.start()
        selector=[dict(Selector(className=className,instance=instance))]
        childs=self.method('objInfo',selector,self.url)
        self.stop()
        return childs['chileCount']

    def getBounds(self,className,instance):
        self.url=self.device.start()   
        selector=[dict(Selector(className=className,instance=instance))]
        rect=self.method('objInfo',selector,self.url)
        self.stop()
        return rect['bounds'].values()       

    def swipe(self,className,instance,dir,steps):
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=int(instance)))
        self.method('swipe',[selector,dir,steps],self.url)
        self.stop()

    def swipexy(self,x,y,toX,toY,steps):
        self.url=self.device.start()
        print self.url
        selector=[x,y,toX,toY,steps]
        result=self.method('swipe',selector,self.url)
        self.stop()

    def text(self,text, match=None,timeout=None):
        self.url=self.device.start()
        selector=dict(Selector(text=text,instance=match))
        self.method('clickAndWaitForNewWindow',[selector,timeout],self.url)
        self.stop()
    
    def className(self,className, match=None,timeout=None) :
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=match))
        self.method('clickAndWaitForNewWindow',[selector,timeout],self.url)
        self.stop()

    def flingToEnd(self,className,instance,isVertical,steps) :
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=instance))
        self.method('flingToEnd',[selector,isVertical,steps],self.url) 
        self.stop()

    def flingToBeginning(self,className,instance,isVertical,steps):
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=instance))
        self.method('flingToBeginning',[selector,isVertical,steps],self.url)
        self.stop()

    def flingBackward(self,className,instance,isVertical):
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=instance))
        self.method('flingBackward',[selector,isVertical],self.url)
        self.stop()

    def flingForward(self,className,instance,isVertical) :
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=instance))
        self.method('flingForward',[selector,isVertical],self.url)
        self.stop()

    def scrollForward(self,className,instance,isVertical,steps) :
        self.url=self.device.start()
        selector=dict(Selector(className=className,instance=instance))
        self.method('flingForward',[selector,isVertical,steps],self.url) 
        self.stop()

    def wakeUp(self):
        self.url=self.device.start()
        self.method('wakeUp',self.url)
        self.stop()

    def isScreenOn(self):
        self.url=self.device.start()
        self.method('isScreenOn',self.url)
        self.stop()

    def takeScreenshot(self,filename,scale,quality):
        self.url=self.device.start()
        self.method('takeScreenshot',[filename,scale,quality],self.url) 
        self.stop()

    def stop(self):
        self.device.stop()

class UiautomatorServer(object):

    __instance = None

    def __init__(self):
        self.local_port=self.next_local_port()
        print self.local_port

    def __new__(self):
        if not self.__instance:
            self.__instance=super(UiautomatorServer,self).__new__(self)
            self.lib_uipath=r'%s\libs\uiautomator-stub.jar'%(self.__instance.script_path())
            self.lib_bundlepath=r'%s\libs\bundle.jar'%(self.__instance.script_path()) 
            stub=self.__instance.__runshell('adb -s %s shell ls /data/local/tmp/ | %s uiautomator-stub.jar'%(INFO.DEVICE,INFO.GREP))
            bundle=self.__instance.__runshell('adb -s %s shell ls /data/local/tmp/ | %s bundle.jar'%(INFO.DEVICE,INFO.GREP))
            str=len(stub.stdout.readlines())
            if str==0:
                self.__instance.__runshell('adb -s %s push \"%s\" /data/local/tmp/'%(INFO.DEVICE,self.lib_uipath))
                self.__instance.__runshell('adb -s %s push \"%s\" /data/local/tmp/'%(INFO.DEVICE,self.lib_bundlepath))     
        return self.__instance

    def script_path(self):
        this_file = inspect.getfile(inspect.currentframe())
        return os.path.abspath(os.path.dirname(this_file))
    
    def next_local_port(self):
        def is_port_listening(port):
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex(('127.0.0.1', port))
            s.close()
            return result == 0
        init_local_port = 9007
        init_local_port = init_local_port + 1 if init_local_port < 32764 else 9008
        while is_port_listening(init_local_port):
            init_local_port += 1
        return init_local_port
               
    def start(self):
        cmd = "uiautomator runtest  uiautomator-stub.jar bundle.jar -c com.github.uiautomatorstub.Stub"
        self.uiautomator_process=self.__runshell('adb -s %s shell %s'%(INFO.DEVICE,cmd))
        time.sleep(1)
        self.url='http://localhost:%d/jsonrpc/0'%(self.local_port)
        return self.url

    def stop(self):
        try:
            cmd = "ps -C uiautomator"
            out=self.__runshell('adb -s %s shell %s'%(INFO.DEVICE,cmd)).stdout.readlines()
            if out:
                index=out[0].split().index('PID')
                for line in out[1:]:
                    if len(line.split()) > index:
                        cmd1="kill -9 %s"%(line.split()[index])
                        self.__runshell('adb -s %s shell %s'%(INFO.DEVICE,cmd1))
        except:
            pass

    def __runshell(self,cmd):
        sub2 = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return sub2