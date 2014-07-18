import threading as thread
import subprocess
import os
import time
import sys
from RunRealMonkeyTest import runTest

def getDeviceSerial(devices):
    p = __runshell('adb devices')
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
    
def __runshell(cmd):
    sub2 = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while 1:
        ret1 = subprocess.Popen.poll(sub2)
        if ret1 == 0:
            break
        elif ret1 is None:
            time.sleep(0.2)
        else:
            break
    return sub2

class Thread(thread.Thread):
    def __init__(self,serial,curTime,serialList):
        thread.Thread.__init__(self)
        self.test=runTest()
        self.serial=serial
        self.curTime=curTime
        self.serialList=serialList
        
    def run(self):
        self.test.runTestCase(self.curTime,self.serial,self.serialList)
    
if __name__=='__main__':
    global mutex
    threads = []
    mutex=thread.Lock()
    curTime = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(time.time()))
    deviceList=[]
    if len(sys.argv)==1:
        sys.argv.append(1)
        deviceList.append(sys.argv[1])
    else:
        del sys.argv[0]
        deviceList=sys.argv
    serialList=[]
    serialList=getDeviceSerial(deviceList)
    for serial in serialList:
        threads.append(Thread(serial,curTime,serialList))
    for t in threads:
        t.start()
        time.sleep(3)
       

    
        
