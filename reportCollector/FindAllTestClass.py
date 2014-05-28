# -*- coding: utf-8 -*-
'''
    @author linyanyan in 20140424
'''
import os

class FindAllTestClass():

    def SearcheDirFile(self,path=None,src=None):
        listtest=[]
        if not os.path.exists(path):
            print "%s路径不存在"%path
        for root,dirs,files in os.walk(path,True):
            if -1!=root.find(src):
                print root
            for item in files:
                path=os.path.join(root,item)
                if -1!=path.find(src):
                    if os.path.splitext(item)[1]=='.py':
                        if item[0:4]==src: 
                            listtest.append(item)
        return listtest

    def ToXML(self,listcase):
         if not os.path.isdir('configure'):
             os.makedirs('configure')
         f=open('./configure/configure.xml','w')
         f.write('''<?xml version="1.0" encoding="utf-8"?>''')
         f.write('<class>')
         for case in listcase:
             f.write('<method name="%s">'%case)
             f.write('</method>')
             f.write('\n')
         f.write('</class>')
         f.close()

