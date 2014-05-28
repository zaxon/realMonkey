# -*- coding: utf-8 -*-
'''
    @author linyanyan in 20140421
'''
import os
import xml.dom.minidom
import time
from xml.etree import ElementTree

class toHtml(object):
    
    #生成html头部
    def headHtml(self,filename,scriptPath):
        if os.path.exists(scriptPath) == False:
            time.sleep(3.0)
            os.makedirs(scriptPath)
        html=open(filename,'w')
        html.write("""
                    <html>
                    <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <title>Test</title>
                    <style>img{float:left;margin:5px;}</style>
                    <script>
                    function max(id){
                    document.getElementById(id).style.pixelWidth = 480
                    document.getElementById(id).style.pixelHeight=800
                    }
                    """)
        html.write("""
                    function min(id){
                    document.getElementById(id).style.pixelWidth=60
                    document.getElementById(id).style.pixelHeight=80
                    }
                    </script>
                    </head>
                    <body align=center>
                   """)
                    
                    
        html.write('''
                   <center><h1>测试报告</h1>
                   <table border=1 borderColor=#DDDDDD width=100% style=border-collapse:collapse>
                   <tr bgcolor=#DDDDDD height=40>
                   <td align = center style=font-weight:bold>步骤</td><td align = center style=font-weight:bold>操作名称</td>
                   <td align = center style=font-weight:bold>截图</td></tr>
                   ''')
        html.flush()
        html.close()
    
    #生成html table  
    def bodyHtml(self,filename,step,casename,picname,exception):
        html=open(filename,'a')
        if exception!=None:
            html.write('<tr><td>异常</td><td style=color:#FF0033 id="exception">%s</td><td><img height=80 width=60 onmouseover="max(this.id)" onmouseout="min(this.id)" src="%s" id="image%s" /></td></tr>'%(exception,picname,picname))
        else:
            html.write('<tr>')
            html.write('<td width=100px align = center style=font-weight:bold>%s</td>'%step)
            html.write('<td width=380px>%s</td>'%casename)
            html.write('<td>')
            html.write('<img height=80 width=60 onmouseover="max(this.id)" onmouseout="min(this.id)" src="%s" id="image%s" />'%(picname,picname))
            html.write('</td>')
            html.write('</tr>')
        html.flush()
        html.close()
    #生成html尾部
    def endHtml(self,filename):
        html=open(filename,'a')
        html.write('</table>')
        html.write('</body></html>')
        html.flush()
        html.close()

    
    
