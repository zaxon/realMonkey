# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140417
'''
class click(object):
    def __init__(self, device, uiselect):
        self.device = device
        self.uiselect = uiselect
    
    def multCondition(self,text=None,sid=None,className=None,index=None):
        x,y=self.uiselect.multCondition(mtext=text,msid=sid,mcclass=className,mindex=index).xy()
        self.device.touch(x,y)
    
    def text(self,text, match=None):
        #TODO ui parser should be added here
        x,y = self.uiselect.text(text,match).xy()
        self.device.touch(x,y)
        
    def index(self,index, match=None) :
        #TODO ui parser should be added here
        x,y = self.uiselect.index(index,match).xy()
        self.device.touch(x,y)
    
    def className(self,className, match=None) :
        #TODO ui parser should be added here
        x,y = self.uiselect.className(className,match).xy()
        self.device.touch(x,y)

    def description(self,description, match=None):
        x,y = self.uiselect.description(description,match).xy()
        self.device.touch(x,y)
        
    def sid(self, sid, match=None):
        x,y = self.uiselect.sid(sid,match).xy()
        self.device.touch(x,y)
        
    def longxy(self,x,y):
        #TODO ui parser should be added here
        self.__longClick(x,y)

    def longByClass(self,className, match=None) :
        #TODO ui parser should be added here
        x,y = self.uiselect.className(className,match).xy()
        self.__longClick(x,y);
        
    def longByText(self,text, match=None):
        #TODO ui parser should be added here
        x,y = self.uiselect.text(text, match).xy()
        self.__longClick(x,y);

    def longByIndex(self,index, match=None) :
        #TODO ui parser should be added here
        x,y = self.uiselect.index(index ,match).xy()
        self.__longClick(x,y);
    
    def __longClick(self,x,y):
        self.device.drag((x,y),(x,y),3000);