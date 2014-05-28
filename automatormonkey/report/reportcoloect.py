# -*- coding: utf-8 -*-
'''
    @author linyanyan in 20140421
'''
import os,sys
from automatormonkey.report.ToHtml import toHtml

class reportcoloect(object):
    
    def __init__(self,scriptPath):
        
        self.__scriptPath = scriptPath
        self.filename = '%s%sreport.html'%(scriptPath,os.sep)
        
        self.htm=toHtml()
        self.htm.headHtml(self.filename, scriptPath)

    def logcolect(self,step=None,casename=None,picname=None,flag=None,exception=None):
        self.picname = '%s'%(picname)
        if flag=='end':
            self.htm.endHtml(self.filename)
        else:
            self.htm.bodyHtml(self.filename,step,casename,self.picname,exception)

                       
