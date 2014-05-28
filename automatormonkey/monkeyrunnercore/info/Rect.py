# -*- coding: utf-8 -*-
'''
   @author wuqiaomin in 20140416
'''
class Rect(object):
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
    def height(self):
        return abs(self.bottom - self.top)
    
    def width(self):
        return abs(self.right - self.left)
