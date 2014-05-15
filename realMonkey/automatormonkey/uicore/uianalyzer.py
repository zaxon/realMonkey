# -*- coding: utf-8 -*-
'''
    @author xinjiankang|wuqiaomin in 20140414
'''
import os
import xml.dom.minidom
import subprocess
import time
from xml.dom.minidom import Node
from automatormonkey.monkeyrunnercore.action.AdbCommand import AdbCommand
from automatormonkey.monkeyrunnercore.info.Enum import *
class uianalyzer(object) :
    
    def __init__(self) :
        '''
        '''
        self.adbCmd = AdbCommand()
        
    def getxyByAttribute(self,text=None,sid=None,cclass=None,index=None) :
        '''return element's X and Y co-ordinates of the specified conditions 
        you can use multi-condition to get
        '''
        tag='text'
        tmp=None
        x0 = None
        y0 = None

        if text != None :
            tag = 'text'
            tmp = text
            print 'tag is text : ' + tmp
        elif sid != None :
            tag = 'source_id'
            tmp = sid
            print 'tag is sid : ' + tmp
        elif cclass != None :
            tag = 'class'
            tmp = cclass
            print 'tag is class : ' + tmp
        elif index != None :
            tag = 'index'
            tmp = index
            print 'tag is index : ' + tmp

        file = self.pullUiTmp()

        root = xml.dom.minidom.parse(file).childNodes[0]
        for node in root.getElementsByTagName('node') :
            try :
                arrcontent = node.getAttribute(tag).encode('utf-8')
                # print arrcontent
            except Exception , e:
                print 'xml encode error , please contact with xinjiankang@baidu.com | wuqiaomin@baidu.com'
            # print arrcontent
            if arrcontent == tmp:
                
                bound = node.getAttribute('bounds').encode('utf-8')
                # print bound
                tmp = bound
                bound = bound.replace('[','')
                bound = bound.split(']')[0]
                x1 = bound.split(',')[0]
                y1 = bound.split(',')[1]
                # print x1,y1
                bound = tmp
                bound = bound.replace(']','')
                bound = bound.split('[')[2]
                x2 = bound.split(',')[0]
                y2 = bound.split(',')[1]
                # print x2,y2
                x0 = (int(x1) + int(x2))/2
                y0 = (int(y1) + int(y2))/2
                print x0 , y0
                break
            # raw_input('enter something')
        return x0 , y0

    def findElement(self,text=None,sid=None,cclass=None,index=None):
        '''return element's info of the specified conditions 
        you can use multi-condition to get
        '''
        
        tag='text'
        listTag=[]
        listTmp=[]
        
        tmpText=None
        tmpSid=None
        tmpClass=None
        tmpIndex=None
        x0 = None
        y0 = None

        if text != None :
            tag = 'text'
            tmpText = text
            listTag.append(tag)
            listTmp.append(tmpText)
        if sid != None :
            tag = 'source_id'
            tmpSid = sid
            listTag.append(tag)
            listTmp.append(tmpSid)
        if cclass != None :
            tag = 'class'
            tmpClass = cclass
            listTag.append(tag)
            listTmp.append(tmpClass)
        if index != None :
            tag = 'index'
            tmpIndex = index
            listTag.append(tag)
            listTmp.append(tmpIndex)
            
        file = self.pullUiTmp()
        count = len(listTag)
        flag = 0
        
        root = xml.dom.minidom.parse(file).childNodes[0]
        for node in root.getElementsByTagName('node') :
            try :
                for i in range(0,count):
                    if cmp(listTmp[i],node.getAttribute(listTag[i]).encode('utf-8'))==0:
                        flag+=1
                    else:
                       break;
            except Exception , e:
                print 'xml encode error , please contact with xinjiankang@baidu.com | wuqiaomin@baidu.com'
            if flag>=count:
               # print node.toxml().encode('utf-8')
                return node
            flag=0
        raise AttributeError('elements  is not found, please check you condition')
    
#    def selectElement(self, nodeName, nodeValue, file):
#        '''return element's info of the specified conditions 
#        '''
#        root = xml.dom.minidom.parse(file).childNodes[0]
#        for node in root.getElementsByTagName('node') :
#            try :
#                tmpValue = node.getAttribute(nodeName).encode('utf-8')
#            except Exception , e:
#                print 'xml encode error , please contact with xinjiankang@baidu.com | wuqiaomin@baidu.com'
#            if tmpValue == nodeValue:
#                #print node.toxml().encode('utf-8')
#                return node
#        #raise AttributeError('elements  is not found, please check you condition')
#        return None
    
    def selectElement(self, nodeName, nodeValue, file, match=None):
        '''return element's info of the specified conditions
        '''
        if match== None:
            matchTmp = 0
        else:
            matchTmp = match
        flag = 0
        root = xml.dom.minidom.parse(file).childNodes[0]
        for node in root.getElementsByTagName('node') :
            try :
                tmpValue = node.getAttribute(nodeName).encode('utf-8')
            except Exception , e:
                print 'xml encode error , please contact with xinjiankang@baidu.com | wuqiaomin@baidu.com'
            if tmpValue == nodeValue:
                if match != None:
                    FLAG.REAMINMATCH = matchTmp - flag
                if flag == matchTmp:
                    return node
                flag += 1
        #raise AttributeError('elements  is not found, please check you condition')
        return None

    def getUiRoot(self,file) :
        return xml.dom.minidom.parse(file).childNodes[0]
    
    def selectChildElement(self, nodeName, nodeValue, nodes, match=None):
        '''return element's info of the specified conditions
        '''
        if match== None:
            matchTmp = 0
        else:
            matchTmp = match
        flag = 0
    
        root = nodes
        for node in root.getElementsByTagName('node') :
            try :
                tmpValue = node.getAttribute(nodeName).encode('utf-8')
            except Exception , e:
                print 'xml encode error'
            if tmpValue == nodeValue:
                if flag == matchTmp:
                    return node
                flag += 1
        #raise AttributeError('elements  is not found, please check you condition')
        return None
    
    def selectElementCount(self, nodeName, nodeValue, nodes):
        '''return element's info of the specified conditions
        '''
        flag = 0
    
        root = nodes
        for node in root.getElementsByTagName('node') :
            try :
                tmpValue = node.getAttribute(nodeName).encode('utf-8')
            except Exception , e:
                print 'xml encode error , please contact with xinjiankang@baidu.com | wuqiaomin@baidu.com'
            if tmpValue == nodeValue:
                flag += 1
        return flag
    
    
    def pullUiTmp(self, tempStr='') :
        '''
        '''
        filePath = '/sdcard/UI_%s%s.xml' %(INFO.DEVICENAME, tempStr)
        self.adbCmd.delete(filePath)    
        self.adbCmd.uidump(filePath)
        self.adbCmd.pull(filePath)
        return os.path.abspath('UI_%s%s.xml' %(INFO.DEVICENAME, tempStr))
