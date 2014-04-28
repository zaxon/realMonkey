# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140416
'''
import xml.dom.minidom
from xml.dom.minidom import Node
from automatormonkey.uicore.uianalyzer import uianalyzer
from automatormonkey.monkeyrunnercore.info.UiElement import UiElement
from automatormonkey.monkeyrunnercore.info.Enum import *

class UiSelector(object):
    
    def __init__(self, device):
        self.ui = uianalyzer()
        self.device = device
    
    def text(self,text, match=None):
        return self.__findElement('text',text, match)
    
    def className(self, className, match=None):
        return self.__findElement('class', className, match)
    
    def index(self, index, match=None):
        return self.__findElement('index', index, match)

    def sid(self, sid, match=None):
        return self.__findElement('resource-id', sid, match)
    
    def description(self, description, match=None):
        return self.__findElement('content-desc', description, match)
    
    def scrollable(self, scrollable, match=None):
        return self.__findElement('scrollable', scrollable, match)

    def checked(self, checked, match=None):
        return self.__findElement('checked', checked, match)

    def selected(self, selected, match=None):
        return self.__findElement('selected', selected, match)

    def focusable(self, focusable, match=None):
        return self.__findElement('focusable', focusable, match)
    
    def focused(self, focused, match=None):
        return self.__findElement('focused', focused, match)  
    
    def packageName(self, packageName, match=None):
        return self.__findElement('packageName', packageName, match)
   
    def multCondition(self,mtext=None,msid=None,mcclass=None,mindex=None):
        '''return element's info of the specified conditions 
        you can use multi-condition to get
        '''
        element = self.__multCondition(text=mtext,sid=msid,cclass=mcclass,index=mindex)
        return UiElement(element)
    
    def __multCondition(self,text=None,sid=None,cclass=None,index=None):
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
            
        file = self.ui.pullUiTmp()
        count = len(listTag)
        flag = 0
        
        root = xml.dom.minidom.parse(file).childNodes[0]
        elementXml = self.ui.selectElement('scrollable', 'true', file)

        for i in range(0,2):
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

            if elementXml != None:
                element=UiElement(elementXml)
                if LIST.VERTICAL==True:
                    rect = element.getVisibleBounds()
                    swipeAreaAdjust = (int)(rect.height() * 0.1);
                    x = rect.right/2
                    y = rect.bottom - swipeAreaAdjust
                    toX = rect.right/2
                    toY = rect.top + swipeAreaAdjust
                    self.device.drag(x, y,toX, toY)
                else:
                    rect = element.getVisibleBounds()
                    swipeAreaAdjust = (int)(rect.width() * 0.1);
                    x = rect.right - swipeAreaAdjust
                    y = rect.bottom/2
                    toX = rect.left + swipeAreaAdjust
                    toY = rect.bottom/2
                    self.device.drag(x, y,toX, toY)
                file = self.ui.pullUiTmp()
                root = xml.dom.minidom.parse(file).childNodes[0]
            
        raise AttributeError('elements  is not found, please check you condition')
    
    
    def __findElement(self, nodeName, nodeValue, match=None):
        file = self.ui.pullUiTmp()
        node = self.ui.selectElement(nodeName, nodeValue, file, match)
        if node != None:
            return UiElement(node)
        
        elementXml = self.ui.selectElement('scrollable', 'true', file)
        if elementXml != None:
            element=UiElement(elementXml)
            for i in range(0,3):
                if LIST.VERTICAL==True:
                    rect = element.getVisibleBounds()
                    swipeAreaAdjust = (int)(rect.height() * 0.1);
                    x = rect.right/2
                    y = rect.bottom - swipeAreaAdjust
                    toX = rect.right/2
                    toY = rect.top + swipeAreaAdjust

                    self.device.drag(x, y,toX, toY)
                    file = self.ui.pullUiTmp()
                    node = self.ui.selectElement(nodeName, nodeValue, file, match)
                    if node != None:
                        #print node.toxml().encode('utf-8')
                        return UiElement(node)
                else:
                    rect = element.getVisibleBounds()
                    swipeAreaAdjust = (int)(rect.width() * 0.1);
                    x = rect.right - swipeAreaAdjust
                    y = rect.bottom/2
                    toX = rect.left + swipeAreaAdjust
                    toY = rect.bottom/2
                    
                    self.device.drag(x, y,toX, toY)
                    file = self.ui.pullUiTmp()
                    node = self.ui.selectElement(nodeName, nodeValue, file, match)
                    if node != None: 
                        #print node.toxml().encode('utf-8')
                        return UiElement(node)
                    
        raise AttributeError('%s %s is not found, please check you condition'%(nodeName , nodeValue))