# -*- coding: utf-8 -*-
'''
    @author wuqiaomin in 20140417
'''

class SystemProperty(object):

    def __init__(self, uiselect):
        self.uiselect = uiselect
        self.element = self.uiselect.index('0')

    def currentPackageName(self):
        self.element = self.uiselect.index('0')
        return self.element.getPackage()

    def displayWidth(self):
        return self.element.width()

    def displayHeight(self):
        return self.element.height()