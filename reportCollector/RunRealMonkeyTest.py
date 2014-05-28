# -*- coding: utf-8 -*-
'''
    @author linyanyan in 20140424
'''
import os
from xml.etree import ElementTree
import subprocess
from FindAllTestClass import *
from ToHtml import ToSummaryHtml
import time
import shutil

class runTest(object):

    def parserXML(self):
        per=ElementTree.parse('./configure/configure.xml')
        root=per.getroot()
        p=root.findall('method')
        methodlist=[]
        for oneper in p:
            name=oneper.get('name')
            methodlist.append(name)
        return methodlist
    
    def __runshell(self,cmd):
        #print cmd
        sub = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print sub.stdout.read()
        while 1:
           ret1 = subprocess.Popen.poll(sub)
           if ret1 == 0:
               break
           elif ret1 is None:
               time.sleep(1)
           else:
               break
            
    def copyfiles(self,srcPath,tagPath,curTime):
        if not os.path.isdir('result'):
            os.makedirs('result')
        curpath=os.path.join('result',curTime)
        new_path=os.path.join(curpath,tagPath)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        for f in os.listdir(srcPath):
            sourceF=os.path.join(srcPath,f)
            targetF=os.path.join(new_path,f)
            if os.path.isfile(sourceF):
                if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                    open(targetF, "wb").write(open(sourceF, "rb").read())
            if os.path.isdir(sourceF):
                copyfiles(sourceF, targetF,curTime)

    def insertLogToHtml(self,path):
        file_object=open('%s\\report.html'%path,'a')
        str = '<table border=0 borderColor=#EAEAEA width=100% style=border-collapse:collapse>\
                    <tr style="text-align:right">\
                                        <td text-align=left style="font-weight:bold">'
        str+='<a href="./log.html">System.out</a>'
        str+='</td></tr></table>'
        file_object.write(str)
                
    def run(self,methodlist,curTime):
        devices=[]
        path=os.path.abspath('..')
        for method in methodlist:
            cmd='python %s\%s'%(path,method)
            self.__runshell(cmd)
            files=os.listdir(path)
            testMethod=method[0:len(method)-3]
            listItem=[]
            for item in files:
                if testMethod in item:
                    if os.path.splitext(item)[1]=='':
                        device=item[len(testMethod)+1:len(item)]
                        listItem.append(device)
                        try:
                            self.parserLogToHtml('%s\%s'%(path,item))
                            self.copyfiles('%s\%s'%(path,item),item,curTime)
                            self.insertLogToHtml('result\%s\%s'%(curTime,item))
                            time.sleep(2.0)
                            shutil.rmtree('%s\%s'%(path,item))
                        except Exception, e:
                            pass
            devices.append(listItem)
        return devices        

    def parserLogToHtml(self,path):
        file_html=open('%s\log.html'%path,'w')
        file_object=open('%s\log.txt'%path,'r')
        _logStr=file_object.read()
        str='<html>\
                    <head>\
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\
                    <title>Test</title>\
                    <style>img{float:left;margin:5px;}</style>'
        str+='</head>\
                    <body><pre>'
        str+='%s'%_logStr
        str+='</pre></body></html>'
        file_html.write(str)
        file_html.close()
        file_object.close()
        os.remove('%s\log.txt'%path)
        

    def deviceCount(self,devices):
        num=0
        deviceList=[]
        for device in devices:
            if(len(device)>num):
                num=len(device)
                deviceList=device
        return deviceList
        
    def runTestCase(self,curTime):
        listcase=[]
        methodlist=[]
        curPath=None
        devices=[]
        deviceList=[]
        if os.path.isfile(os.getcwd()+'/configure/configure.xml'):
            methodlist=self.parserXML()
        else:
            allTestCase=FindAllTestClass()
            listcase=allTestCase.SearcheDirFile(os.path.abspath('..'),'test')
            allTestCase.ToXML(listcase)
            methodlist=self.parserXML()
        deviceList=self.run(methodlist,curTime)
        devices=self.deviceCount(deviceList)
        if len(devices)>0: 
            html=ToSummaryHtml()
            path='%s\\result\\%s'%(os.getcwd(),curTime)
            html.seachHtmlFile(path,'report.html',methodlist,devices)


if __name__=='__main__':
    curTime = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(time.time()))
    test=runTest()
    test.runTestCase(curTime)
    
        



        


    
