# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140417
'''
#from automatormonkey.monkeyrunnercore.info.SystemProperty import SystemProperty
from automatormonkey.monkeyrunnercore.info.Enum import *
from automatormonkey.monkeyrunnercore.utils.RealListView import *

class drag(object):
    def __init__(self, device, uiselect, systemInfo):
        self.device = device
        self.uiselect = uiselect

        self.systemInfo = systemInfo
        self.displayHeight = self.systemInfo.displayHeight()
        self.displayWidth = self.systemInfo.displayWidth()
        
    def xy(self, x, y, toX, toY):
        self.__drag(x, y, toX, toY);
    
    def swipeUp(self, steps=5):
        self.__swipe(self.displayWidth/2, (self.displayHeight/4)*3, self.displayWidth/2, self.displayHeight/4)
        
    def swipeDown(self, steps=5):
        self.__swipe(self.displayWidth/2, self.displayHeight/4, self.displayWidth/2, (self.displayHeight/4)*3)
    
    def swipeLeft(self, steps=5):
        self.__swipe((self.displayWidth/4)*3, self.displayHeight/2, self.displayWidth/4, self.displayHeight/2)

    def swipeRight(self, steps=5):
        self.__swipe(self.displayWidth/4, self.displayHeight/2, (self.displayWidth/4)*3, self.displayHeight/2)

    def up(self):
        #get current uiautomator and dump to tmp when drag hanppens , clear it when Click or long Click hanppens
        self.__drag(self.displayWidth/2, (self.displayHeight/4)*3, self.displayWidth/2, self.displayHeight/4,DIRECTION.UP)
        
    def down(self):
        self.__drag(self.displayWidth/2, self.displayHeight/4, self.displayWidth/2, (self.displayHeight/4)*3,DIRECTION.DOWN)
            
    def left(self, steps=5):
         self.__swipe((self.displayWidth/10)*9, self.displayHeight/2, self.displayWidth/10, self.displayHeight/2,DIRECTION.LEFT)
    
    def right(self, steps=5):
        self.__swipe(self.displayWidth/10, self.displayHeight/2, (self.displayWidth/10)*9, self.displayHeight/2,DIRECTION.RIGHT)
    
    def __drag(self,x, y, toX, toY,direction=None,MODE=FLAG.DRAG):
        '''
            MODE : SEARCH / DRAG
        '''
        if (direction==DIRECTION.UP or direction==DIRECTION.DOWN) and (MODE==FLAG.DRAG) :
            self.uiselect.listViewConstructor()
        else :
            FLAG.RLVMODE = False
            RealListView.Content=None
        self.device.drag(x, y, toX, toY);

    def __swipe(self, x, y, toX, toY,direction=None):
        self.__drag(x, y, toX, toY,direction)
        
        
                                                                                        



