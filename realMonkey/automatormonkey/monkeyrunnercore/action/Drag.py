# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140417
'''
#from automatormonkey.monkeyrunnercore.info.SystemProperty import SystemProperty

class drag(object):
    def __init__(self,device, systemInfo):
        self.device = device

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
        self.__drag(self.displayWidth/2, (self.displayHeight/4)*3, self.displayWidth/2, self.displayHeight/4)
        
    def down(self):
        self.__drag(self.displayWidth/2, self.displayHeight/4, self.displayWidth/2, (self.displayHeight/4)*3)
            
    def left(self, steps=5):
         self.__swipe((self.displayWidth/10)*9, self.displayHeight/2, self.displayWidth/10, self.displayHeight/2)
    
    def right(self, steps=5):
        self.__swipe(self.displayWidth/10, self.displayHeight/2, (self.displayWidth/10)*9, self.displayHeight/2)
    
    def __drag(self,x, y, toX, toY):
         self.device.drag(x, y, toX, toY);
        
    def __swipe(self, x, y, toX, toY):
        self.__drag(x, y, toX, toY)
        
        
                                                                                        



