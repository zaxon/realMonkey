# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140416
'''
import sys
from xml.dom.minidom import Node
from automatormonkey.monkeyrunnercore.info.Rect import Rect
reload(sys)
sys.setdefaultencoding('utf8')


class UiElement(object):

    def __init__(self, element):
        self.element = element

    def getText(self):
        return self.__getValue('text')

    def getClassName(self):
        return self.__getValue('class')

    def getIndex(self):
        return self.__getValue('index')
    
    def getPackage(self):
        return self.__getValue('package')

    def getXY(self):
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
        return self.__getBoolValue(self.__getValue('enabled'))

    def isScrollable(self):
        return self.__getBoolValue(self.__getValue('scrollable'))

    def isChecked(self):
        return self.__getBoolValue(self.__getValue('checked'))

    def isSelected(self):
        return self.__getBoolValue(self.__getValue('selected'))

    def isFocused(self):
        return self.__getBoolValue(self.__getValue('focused'))

    def sid(self):
        return self.__getValue('resource-id')

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
        return self.element.getAttribute(tag)

    def __getBoolValue(self, value):
        if value=='true':
            return True
        return False
    










    
