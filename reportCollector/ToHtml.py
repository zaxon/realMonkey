# -*- coding: utf-8 -*-
'''
    @author linyanyan in 20140424
'''
import os
import re
from LogParser import LogParser

class ToSummaryHtml(object):

    def seachHtmlFile(self,curpath=None,filename=None,methodlist=None,devices=None):

        listcontent=[]
        _failCount=0
        _sucessCount=0
        failCase=[]
        content=None
        dictcontent={}
        if not os.path.exists(curpath):
            print "%s路径不存在"%curpath
        for root,dirs,files in os.walk(curpath,True):
            if -1!=root.find(filename):
                print root
            for item in files:
                path=os.path.join(root,item)
                if -1!=path.find(filename):
                    if os.path.splitext(item)[1]=='.html':
                        testcase=os.path.split(path)[0].split('\\')[-1]
                        listcontent=self.parseHtml(path)
                        log=LogParser()
                        _str=log.parser('%s\\%s\\log.html'%(curpath,testcase))
                        if _str=='crash':
                            _failCount=_failCount+1
                            dictcontent['%s'%testcase]='crash'
                        else:
                            if len(listcontent)>0:
                                _failCount=_failCount+1
                                content=listcontent[0]
                                dictcontent['%s'%testcase]=content
                            else:
                                content='Success'
                                dictcontent['%s'%testcase]=content
                                _sucessCount=_sucessCount+1
                            
        self.headHtml('%s\sumHtml.html'%curpath)
        for device in devices:
            total=0
            _fail=0
            _success=0
            for key in dictcontent.keys():
                if device in key:
                    total=total+1
                    if dictcontent[key]!='Success':
                        _fail=_fail+1
                        failCase.append(key)
                    else:
                        _success=_success+1
            self.titleHtml('%s\sumHtml.html'%curpath,device)
            self.getSummaryHtml(curpath,'%s\sumHtml.html'%curpath,total,_success,_fail,failCase,device)
        for device in devices:
            dic={}
            dicf={}
            for key in dictcontent.keys():
                if device in key:
                    dic['%s'%key]=dictcontent[key]
                    if dictcontent[key]!='Success':
                        dicf['%s'%key]=dictcontent[key]
            self.failDetailHtml(curpath,'%s\\%s_FailHtml.html'%(curpath,device),dicf,device)
            self.titleHtml('%s\sumHtml.html'%curpath,device)
            self.getDetailHtml(curpath,'%s\sumHtml.html'%curpath,dic,device)
        self.endHtml('%s\sumHtml.html'%curpath)

    def headHtml(self,filename):
        
        f=open(filename,'w')
        str='<html>\
                    <head>\
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\
                    <title>Test</title>\
                    <style>img{float:left;margin:5px;}</style>'
        str+='</head>\
                    <body align=center>'
        str+='<center><h1>测试报告</h1>'
        f.write(str)

    def endHtml(self,filename):

        f=open(filename,'a')
        str='</body></html>'
        f.write(str)
        f.close()
        
    def titleHtml(self,filename,title):
        f=open(filename,'a')
        str = '<table border=0 borderColor=#EAEAEA width=100% style=border-collapse:collapse>\
                    <tr style="text-align:left">\
                                        <td text-align=left style="font-weight:bold">'
        str+='%s'%title
        str+='</td></tr></table>'
        f.write(str)
        return str
    
    def getSummaryHtml(self,curpath,filename,total,sucessCount,failCount,failCase,device):
        f=open(filename,'a')
        str = '<table border=1 borderColor=#EAEAEA width=100% style=border-collapse:collapse>\
                    <tr>\
                        <th width=350>用例总数</th>\
                        <th>用例通过</th>\
                        <th>用例失败</th>\
                    </tr>' 
        
        str += '<tr>\
                    <th>%d</th>\
                    <th>%s</th>'% (total,sucessCount)
        if failCount>0:
            str+='<th><a href="./%s_FailHtml.html">%s</a>'%(device,failCount)
        else:
            str+='<th>%s'%(failCount)
        str+='</th></tr>'
        str += '</table><hr/><br/>'
        f.write(str)
        return str
    
    def getDetailHtml(self,curpath,filename,dictcontent,device):
        log=LogParser()
        f=open(filename,'a')
        str = '<table border=1 borderColor=#EAEAEA width=100% style=border-collapse:collapse>\
                    <tr>\
                        <th width=350>用例名称</th>\
                        <th>结果</th>\
                    </tr>' 
        for key in dictcontent.keys():
##            _str=log.parser('%s\\%s\\log.html'%(curpath,key))
            case=key[0:len(key)-len(device)-1]
            str += '<tr>\
                        <th><a href="./%s/report.html">%s</a></th>'%(key,case)
            if dictcontent[key]!="Success":
                if dictcontent[key]=="crash":
                     str+='<th style=color:#FF0033 id="e">%s:<a href="./%s/log.html">System.out</a></th></tr>'%(dictcontent[key],key)
                else:
                     str+='<th style=color:#FF0033 id="e">Exception:%s</th></tr>'%(dictcontent[key])
            else:
                str+='<th id="e">%s</th></tr>'%(dictcontent[key])
        str += '</table><hr/><br/>'
        f.write(str)
    
    def failDetailHtml(self,curpath,filename,dictcontent,device):
        log=LogParser()
        f=open(filename,'w')
        str='<html>\
                    <head>\
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\
                    <title>Test</title>\
                    <style>img{float:left;margin:5px;}</style>'
        str+='</head>\
                    <body align=center>'
        str+='<center><h1>失败测试报告</h1>'
        str+= '<table border=1 borderColor=#EAEAEA width=100% style=border-collapse:collapse>\
                    <tr>\
                        <th width=350>用例名称</th>\
                        <th>结果</th>\
                    </tr>' 
        for key in dictcontent.keys():
##            _str=log.parser('%s\\%s\\log.html'%(curpath,key))
            case=key[0:len(key)-len(device)-1]
            str += '<tr>\
                        <th><a href="./%s/report.html">%s</a></th>'%(key,case)
            if dictcontent[key]!="Success":
                if dictcontent[key]=="crash":
                     str+='<th style=color:#FF0033 id="e">%s:<a href="./%s/log.html">System.out</a></th></tr>'%(dictcontent[key],key)
                else:
                     str+='<th style=color:#FF0033 id="e">Exception:%s</th></tr>'%(dictcontent[key])
            else:
                str+='<th id="e">%s</th></tr>'%(dictcontent[key])
        str += '</table><hr/><br/></html>'
        f.write(str)


    def parseHtml(self,filename):
        npos=0
        flag=False
        listcontent=[]
        f=open(filename,'r')
        line=f.read()
        pattern = re.search(re.compile('<td style=color:#FF0033 id="exception">(.*?)\\n'), line)
        if pattern:
            content=pattern.group(1)
            listcontent.append(content)
        row=line.find('td')
        npos=line.find('异常')
        if -1!=npos:
            flag=True
            listcontent.append(flag)
        f.close()
        return listcontent


        
