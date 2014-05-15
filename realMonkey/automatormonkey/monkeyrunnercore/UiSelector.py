# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140416
'''
import xml.dom.minidom
from xml.dom.minidom import Node
from automatormonkey.uicore.uianalyzer import uianalyzer
from automatormonkey.monkeyrunnercore.info.UiElement import UiElement
from automatormonkey.monkeyrunnercore.info.Enum import *
from automatormonkey.monkeyrunnercore.utils.RealListView import *
import time , re

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
    

    def listViewConstructor(self) :

        #TODO handle drag vertical then drag horizon
        #set RLVMODE every time
        FLAG.RLVMODE = True

        file = self.ui.pullUiTmp('tmp')
        scrollableNode = self.__getListView(file)

        if scrollableNode ==None :
            return

        if RealListView.Content==None:
            print 'init RealListView'
            RealListView.Content = scrollableNode
        else :
            print 'append new listview'
            passMatch = self.__realgetSameNodeNum(RealListView.Content, scrollableNode)
            for i in range(passMatch):
                scrollableNode.removeChild(scrollableNode.childNodes[0])
            for tmp in scrollableNode.childNodes :
                RealListView.Content.childNodes.append(tmp)

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
        scrollableNone = self.ui.selectElement('scrollable', 'true', file)

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

            if scrollableNone != None:
                element=UiElement(scrollableNone)
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
    def __findElementInRLVMODE(self, nodeName, nodeValue, match=None):
        '''
            TODO : 1、merge NORMALMODE&&TLVMODE;
        '''
        node = self.ui.selectChildElement(nodeName, nodeValue, RealListView.Content,match)
        if node ==None:
            for i in range(0,100):
                self.__mdrag(True,UiElement(RealListView.Content))
                self.listViewConstructor()
                node = self.ui.selectChildElement(nodeName,nodeValue,RealListView.Content,match)
                if node != None :
                    break
        return node

    def __findElement(self, nodeName, nodeValue, match=None):


        if RealListView.Content != None :
            print 'enter RLVMODE'
            self.listViewConstructor()
            node = self.__findElementInRLVMODE(nodeName,nodeValue,match)
            FLAG.RLVMODE = False
            RealListView.Content=None
            return UiElement(node)
        else :

            file = self.ui.pullUiTmp('tmp')
            node = self.ui.selectElement(nodeName, nodeValue, file, match)
            if node != None:
                FLAG.SCROLLBALE = True 
                return UiElement(node)
            if FLAG.SCROLLBALE == False:
                FLAG.SCROLLBALE = True 
                raise AttributeError('%s %s is not found in current screen'%(nodeName , nodeValue))

            scrollableNode = self.ui.selectElement('scrollable', 'true', file)
            if scrollableNode != None:
                self.listViewConstructor()
                node = self.__findElementInRLVMODE(nodeName,nodeValue,match)
                RealListView.Content = None
                return UiElement(node)
            else : 
                '''
                '''
                #handle views as can be scrolled but scrollable="false"
                #TODO
                # root = self.ui.getUiRoot(file)
                # element = UiElement(root.childNodes[0])
                # node = root
                # for i in range(0,100) :
                #     self.__mdrag(True,element)
                #     filetmp = self.ui.pullUiTmp('tmp')
                #     root1=self.ui.getUiRoot(filetmp)
                #     node = self.__nodeMerge(node,root1)
                #     tmp = self.ui.selectChildElement(nodeName,nodeValue,node,match)
                #     if tmp != None :
                #         print node.toxml()
                #         # return UiElement(tmp)
                #         return
        raise AttributeError('%s %s is not found in current screen'%(nodeName , nodeValue))

    def __mdrag(self,vertical,element):

        rect = element.getVisibleBounds()
        if vertical==True :
            swipeAreaAdjust = (int)(rect.height() * 0.1);
            x = rect.right/2
            y = rect.bottom - swipeAreaAdjust
            toX = rect.right/2
            toY = rect.top + swipeAreaAdjust
        else :
            swipeAreaAdjust = (int)(rect.width() * 0.1);
            x = rect.right - swipeAreaAdjust
            y = rect.bottom/2
            toX = rect.left + swipeAreaAdjust
            toY = rect.bottom/2
        self.device.drag(x, y, toX, toY*2)

    def __realgetSameNodeNum(self, node1, node2):

        node1.removeChild(node1.childNodes[len(node1.childNodes)-1])
        node2.removeChild(node2.childNodes[0])
        rootLen = len(node1.childNodes)
        for i in range(rootLen):
            if self.__nodeCompare(node1.childNodes[rootLen-i-1],node2.childNodes[0]) == True:
                return i+1
            
        return 0

    def __singlenodecompare(self, node1, node2):

        if len(node1.attributes.keys())!=len(node2.attributes.keys()):
            return False
        else :
            for key in node1.attributes.keys():

                if key=='bounds' :
                    continue
                if node1.getAttribute(key)!=node2.getAttribute(key):
                    return False
        return True
    
    def __nodeCompare(self, node, nodeTemp):
        '''
            hold this method , may be in use
        '''
        mlen = len(node.childNodes)
        mlenTemp = len(nodeTemp.childNodes)

        if mlen != mlenTemp:
            return False
        if node.hasChildNodes() == True:
            flag = False
            for i in range (mlen):
                flag = self.__nodeCompare(node.childNodes[i], nodeTemp.childNodes[i])
                if flag == False:
                    return False
            return flag
        else:
            return self.__singlenodecompare(node,nodeTemp)
            

    def __getListView(self,file) :
        tag = 0
        root = self.ui.getUiRoot(file)
        tmp = self.ui.selectChildElement('scrollable','true',root)
        while True :
            if tmp==None :
                break
            if tmp.getAttribute('class').encode('utf-8')!='android.widget.HorizontalScrollView' and len(tmp.childNodes)>1:
                break
            else :
                tag = tag + 1
                tmp = self.ui.selectChildElement('scrollable','true',root,tag)
                print tmp.getAttribute('class').encode('utf-8')
        return tmp
        