# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140417
'''
#from automatormonkey.monkeyrunnercore.info.SystemProperty import SystemProperty
from automatormonkey.monkeyrunnercore.info.Enum import *
from automatormonkey.monkeyrunnercore.utils.RealListView import *
from automatormonkey.monkeyrunnercore.UiAutomator import *

class drag(object):
    def __init__(self, device, uiselect, systemInfo):
        self.device = device
        self.uiselect = uiselect
        self.uiautomatorDevice=UiautomatorDevice()

        self.systemInfo = systemInfo
        self.displayHeight=0
        self.displayWidth=0
        
    def xy(self, x, y, toX, toY):
        self.__drag(x, y, toX, toY);
    
    def up(self):
        self.__getWH()
        #get current uiautomator and dump to tmp when drag hanppens , clear it when Click or long Click hanppens
        self.__drag(self.displayWidth/2, (self.displayHeight/5)*3, self.displayWidth/2, 0,DIRECTION.UP)
        
    def down(self):
        self.__getWH()
        self.__drag(self.displayWidth/2, (self.displayHeight/5)*2, self.displayWidth/2, self.displayHeight,DIRECTION.DOWN)
            
    def left(self, duration=''):
        self.__getWH()
        self.__drag((self.displayWidth/100)*99, self.displayHeight/2, self.displayWidth/100, self.displayHeight/2,DIRECTION.LEFT, durations=duration)
    
    def right(self, duration=''):
        self.__getWH()
        self.__drag(self.displayWidth/100, self.displayHeight/2, (self.displayWidth/100)*99, self.displayHeight/2,DIRECTION.RIGHT, durations=duration)
    
    def __drag(self,x, y, toX, toY,direction=None,MODE=FLAG.DRAG,durations=''):
        '''
            MODE : SEARCH / DRAG
        '''
        if (direction==DIRECTION.UP) and (MODE==FLAG.DRAG) :
            self.uiselect.listViewConstructor()
        else :
            FLAG.RLVMODE = False
            RealListView.Content=None
        self.uiautomatorDevice.swipexy(x, y, toX, toY,10);

    def __getWH(self):
        self.displayHeight = int(self.systemInfo.displayHeight())
        self.displayWidth = int(self.systemInfo.displayWidth())

    def __swipe(self, x, y, toX, toY,direction=None):
        self.__drag(x, y, toX, toY,direction)
        
        
                                                                                        



