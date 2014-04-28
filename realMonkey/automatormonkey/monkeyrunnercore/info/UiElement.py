# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140416
'''
from xml.dom.minidom import Node
from automatormonkey.monkeyrunnercore.info.Rect import Rect

class UiElement(object):

    def __init__(self, element):
        self.element = element
        
    def getChildBy(self,text=None,sid=None,cclass=None,index=None):
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
            
        count = len(listTag)
        flag = 0
        
        root = self.element
        for node in root.getElementsByTagName('n node') :
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
                return UiElement(node)
            flag=0
        raise AttributeError('elements  is not found, please check you condition')
    

    def getText(self):
        return self.__getValue('text')

    def getClassName(self):
        return self.__getValue('class')

    def getIndex(self):
        return self.__getValue('index')
    
    def getPackage(self):
        return self.__getValue('package')

    def xy(self):
        rect = self.getVisibleBounds()
        x0 = (rect.right+rect.left)/2
        y0 = (rect.bottom + rect.top)/2
        return str(x0) , str(y0)

    def height(self):
        rect = self.getVisibleBounds()
        return abs(rect.bottom - rect.top)

    def width(self):
        rect = self.getVisibleBounds()
        return abs(rect.right - rect.left)
        
    def isEnabled(self):
        return self.__getValue('enabled')

    def isScrollable(self):
        return self.__getValue('scrollable')

    def isChecked(self):
        return self.__getValue('checked')

    def isSelected(self):
        return self.__getValue('selected')

    def isFocused(self):
        return self.__getValue('focused')

    def sid(self):
        return self.__getValue('enabled')

    def getElement(self):
        return self.element
    
    def getVisibleBounds(self):
        bound = self.__getValue('bounds')
        tmp = bound
        bound = bound.replace('[','')
        bound = bound.split(']')[0]
        left = int(bound.split(',')[0])
        top = int(bound.split(',')[1])
        # print x1,y1
        bound = tmp
        bound = bound.replace(']','')
        bound = bound.split('[')[2]
        right = int(bound.split(',')[0])
        bottom = int(bound.split(',')[1])
        rect = Rect(left,top,right,bottom)
        return rect
    
    def __getValue(self, tag):
        return self.element.getAttribute(tag).encode('utf-8')
    










    
